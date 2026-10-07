#!/usr/bin/env python3
"""Busca y prepara grabados antiguos de animales para el planisferio.

Los mapas viejos llevaban animales dibujados donde se sabía que vivían. Acá se
hace lo mismo, pero sin inventar: se usan grabados de historia natural del
siglo XIX que están en dominio público, buscados en Wikimedia Commons con el
mismo criterio que las fotos de las fichas.

Sólo dominio público: una licencia Creative Commons obliga a atribuir en el
propio afiche, y un pie de autor por bicho no entra en un mapa.

El grabado viene como un escaneo de página: papel amarillento, manchas, marco.
`preparar` lo pasa a tinta sobre transparente para que se integre al mapa.
"""
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

AQUI = Path(__file__).parent
SALIDA = AQUI / "assets/grabados"
CACHE = AQUI / ".grabados-cache"
API = "https://commons.wikimedia.org/w/api.php"
ANCHO = 1400
MINIMO = 600

PD = re.compile(r"public\s*domain|^pd[-\s]|dominio\s*p|gemeinfrei|cc0", re.I)


def pedir(params: dict) -> dict:
    params = dict(params, format="json", formatversion="2")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "User-Agent": "NIDO-mapa/1.0 (afiche; contacto via github.com/negracuarenta/nido)"})
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=40, context=ctx) as r:
        return json.loads(r.read().decode())


def buscar(clave: str, terminos: list) -> None:
    vistos, filas = set(), []
    for t in terminos:
        try:
            d = pedir({"action": "query", "generator": "search", "gsrsearch": t,
                       "gsrnamespace": 6, "gsrlimit": 40, "prop": "imageinfo",
                       "iiprop": "url|extmetadata|size", "iiurlwidth": ANCHO})
        except Exception as e:
            print(f"  (falló «{t}»: {e})"); continue
        for p in d.get("query", {}).get("pages", []):
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {})
            lic = (em.get("LicenseShortName", {}).get("value") or "").strip()
            titulo = p["title"].replace("File:", "")
            if (titulo in vistos or not PD.search(lic)
                    or not re.search(r"\.(jpe?g|png)$", titulo, re.I)
                    or (ii.get("width") or 0) < MINIMO):
                continue
            vistos.add(titulo)
            autor = re.sub(r"<[^>]+>", "", em.get("Artist", {}).get("value") or "")
            filas.append({"titulo": titulo, "licencia": lic,
                          "url": (ii.get("thumburl") or ii.get("url")).replace(
                              "//thumb.wikimedia", "//upload.wikimedia"),
                          "w": ii.get("width"), "h": ii.get("height"),
                          "autor": re.sub(r"\s+", " ", autor).strip()[:50],
                          "pagina": ii.get("descriptionurl")})
    CACHE.mkdir(exist_ok=True)
    (CACHE / f"{clave}.json").write_text(json.dumps(filas, ensure_ascii=False))
    print(f"\n=== {clave}: {len(filas)} grabados en dominio público")
    for i, r in enumerate(filas[:14]):
        print(f"{i:>3} {r['w']}x{r['h']:<6} {r['licencia'][:18]:<20} {r['titulo'][:62]}")


if __name__ == "__main__":
    for clave, *terminos in [a.split("|") for a in sys.argv[1:]]:
        buscar(clave, terminos)
