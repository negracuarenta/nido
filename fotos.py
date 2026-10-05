#!/usr/bin/env python3
"""Busca, verifica y descarga fotos de Wikimedia Commons para un lugar.

Sólo baja imágenes cuya licencia permita reutilizarlas: CC BY, CC BY-SA, CC0 y
dominio público. El resto se descarta, aunque sean públicas. Las deja ya
optimizadas en assets/fotos/<slug>/ y escribe los créditos en pantalla para
pegarlos en el JSON del lugar.

    python3 fotos.py buscar <slug> "término" ["otro término"…]
    python3 fotos.py bajar  <slug> <n> <n> <n>

`buscar` lista candidatas numeradas; `bajar` toma los números de esa lista.
El paso en dos tiempos es a propósito: las fotos se eligen mirándolas, no
automáticamente.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).parent
CACHE = AQUI / ".fotos-cache"
AGENTE = "NIDO-negra40/1.0 (negracuarenta@gmail.com)"
ANCHO_MAX = 1600
ANCHO_MIN = 1200

API = "https://commons.wikimedia.org/w/api.php"


def libre(licencia: str) -> bool:
    """Sólo licencias que permiten reutilizar. 'Público' no alcanza."""
    n = re.sub(r"[^a-z0-9]", "", licencia.lower())
    return n.startswith(("ccby", "cc0", "publicdomain", "pd"))


def normalizar(url: str) -> str:
    """Commons a veces devuelve thumb.wikimedia.org, que no resuelve.
    El host servible es upload.wikimedia.org. De paso saca el utm_."""
    if not url:
        return url
    url = url.replace("//thumb.wikimedia.org/", "//upload.wikimedia.org/")
    return url.split("?")[0]


def pedir(params: dict) -> dict:
    params.update(format="json", formatversion="2")
    url = API + "?" + "&".join(
        f"{k}={subprocess.run(['python3','-c','import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))',str(v)],capture_output=True,text=True).stdout.strip()}"
        for k, v in params.items())
    out = subprocess.run(["curl", "-s", "-A", AGENTE, url],
                         capture_output=True, text=True).stdout
    return json.loads(out) if out.strip().startswith("{") else {}


def buscar(slug: str, terminos: list[str]) -> None:
    vistos, filas = set(), []
    for termino in terminos:
        d = pedir({"action": "query", "generator": "search", "gsrsearch": termino,
                   "gsrnamespace": 6, "gsrlimit": 40,
                   "prop": "imageinfo", "iiprop": "url|extmetadata|size",
                   "iiurlwidth": ANCHO_MAX})
        for p in d.get("query", {}).get("pages", []):
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {})
            lic = (em.get("LicenseShortName", {}).get("value") or "").strip()
            titulo = p["title"].replace("File:", "")
            if (not libre(lic) or titulo in vistos
                    or not re.search(r"\.(jpe?g|png|tif)$", titulo, re.I)
                    or (ii.get("width") or 0) < ANCHO_MIN):
                continue
            vistos.add(titulo)
            autor = re.sub(r"<[^>]+>", "", em.get("Artist", {}).get("value") or "")
            filas.append({
                "titulo": titulo,
                # thumburl ya viene a ANCHO_MAX; url es el original, que puede
                # pesar decenas de megas.
                "url": normalizar(ii.get("thumburl") or ii.get("url")),
                "w": ii.get("width"), "h": ii.get("height"), "licencia": lic,
                "autor": re.sub(r"\s+", " ", autor).strip()[:60],
                "pagina": ii.get("descriptionurl"),
            })
    filas.sort(key=lambda r: -(r["w"] or 0))
    CACHE.mkdir(exist_ok=True)
    (CACHE / f"{slug}.json").write_text(json.dumps(filas, ensure_ascii=False), encoding="utf-8")
    print(f"{len(filas)} candidatas con licencia libre para {slug}\n")
    for i, r in enumerate(filas[:28]):
        print(f"{i:>3} {r['w']}x{r['h']:<6} {r['licencia']:<15} "
              f"{r['autor'][:26]:<28} {r['titulo'][:52]}")


def bajar(slug: str, indices: list[int]) -> None:
    filas = json.loads((CACHE / f"{slug}.json").read_text(encoding="utf-8"))
    destino = AQUI / "assets/fotos" / slug
    destino.mkdir(parents=True, exist_ok=True)
    creditos = []
    for n, idx in enumerate(indices, 1):
        r = filas[idx]
        tmp = CACHE / "tmp.bin"
        subprocess.run(["curl", "-sL", "-A", AGENTE, "-o", str(tmp), r["url"]], check=True)
        im = Image.open(tmp)
        if im.width > ANCHO_MAX:
            f = ANCHO_MAX / im.width
            im = im.resize((ANCHO_MAX, round(im.height * f)), Image.LANCZOS)
        nombre = f"{n:02d}.webp"
        im.convert("RGB").save(destino / nombre, "WEBP", quality=82, method=6)
        kb = (destino / nombre).stat().st_size / 1024
        creditos.append({"archivo": nombre,
                         "epigrafe": {"es": "", "de": "", "en": ""},
                         "autor": r["autor"], "licencia": r["licencia"],
                         "origen": r["pagina"]})
        print(f"{nombre}  {im.width}x{im.height:<6} {kb:5.0f} KB  {r['titulo'][:46]}")
        tmp.unlink(missing_ok=True)
    print("\n--- pegar en el JSON del lugar ---")
    print(json.dumps(creditos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
    elif sys.argv[1] == "buscar":
        buscar(sys.argv[2], sys.argv[3:])
    elif sys.argv[1] == "bajar":
        bajar(sys.argv[2], [int(x) for x in sys.argv[3:]])
