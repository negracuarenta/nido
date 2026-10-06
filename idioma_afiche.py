#!/usr/bin/env python3
"""Genera la versión alemana del afiche a partir de la castellana.

Sólo cambia el texto. La geometría, las posiciones y —sobre todo— los códigos
QR son exactamente los mismos: una misma dirección sirve para los tres idiomas
del sitio, que es justamente lo que permite imprimir un solo juego de códigos.
Las dos versiones del afiche se pueden comparar hoja contra hoja.

Va después de afiche.py y planisferio.py, porque traduce lo que ellos dejaron.

Los nombres de los lugares salen de nido_lugares.json y las frases que ya
existen en el sitio, de content/site.json, para no traducir dos veces lo mismo
y que el afiche y la web no se contradigan.
"""
import json
import re
from pathlib import Path

AQUI = Path(__file__).parent
VERSIONES = {"NIDO_mapa_A0.svg": "NIDO_mapa_A0_de.svg",
             "NIDO_mapa_A0_color.svg": "NIDO_mapa_A0_color_de.svg"}

# Lo que no está en el sitio y es propio del afiche.
PROPIAS = {
    "NIDO": "NIDO",
    "Heidelberg": "Heidelberg",
    "Desde un liquidámbar en Heidelberg, hacia el este, el sur y el oeste":
        "Von einem Amberbaum in Heidelberg aus nach Osten, Süden und Westen",
    "ver detalle →": "Detail ansehen →",
    "punto 0 · el árbol": "Punkt 0 · der Baum",
    "Detalle · Sudamérica": "Detail · Südamerika",
    "Referencias": "Zeichenerklärung",
    "Viaje al este": "Flug nach Osten",
    "Viaje al sur": "Flug nach Süden",
    "Viaje al oeste": "Flug nach Westen",
    "· Acto 2": "· 2. Akt",
    "· Acto 3": "· 3. Akt",
    "· Acto 4": "· 4. Akt",
    "· fuera de la obra": "· außerhalb des Stücks",
    "Lugar que vio": "Ort, den sie sah",
    "Heidelberg · el árbol": "Heidelberg · der Baum",
    "Rutas trazadas por arcos de círculo máximo, en el orden en que la "
    "golondrina las cuenta.":
        "Routen als Großkreisbögen, in der Reihenfolge, in der die Schwalbe "
        "sie erzählt.",
    "Proyección Equal Earth · detalle en acimutal equivalente de Lambert.":
        "Projektion Equal Earth · Detail in flächentreuer Azimutalprojektion "
        "nach Lambert.",
    "Índice · escaneá el código para saber más de cada lugar":
        "Verzeichnis · Code scannen für mehr zu jedem Ort",
    "Para empezar": "Zum Anfang",
    "El mapa completo": "Die ganze Karte",
    "Escaneá para abrir el mapa interactivo":
        "Scannen, um die interaktive Karte zu öffnen",
    "El liquidámbar de Heidelberg": "Der Amberbaum in Heidelberg",
}

CODIGO = re.compile(r"^(?:E|S|O|OV)\d*$")


def diccionario() -> dict:
    d = dict(PROPIAS)
    site = json.loads((AQUI / "content/site.json").read_text())
    d["Los vuelos de la golondrina"] = site["subtitulo"]["de"]
    d["Otros vuelos"] = site["viajes"]["OV"]["de"]
    d["Lo que también vio"] = site["ui"]["capa_tragica"]["de"]
    d["Punto 0 · el árbol"] = site["ui"]["punto_cero"]["de"]
    for viaje in json.loads((AQUI / "nido_lugares.json").read_text())["trips"]:
        for l in viaje["places"]:
            d[l["name"]] = (l.get("names") or {}).get("de") or l["name"]
    return d


def traducir(svg: str, d: dict) -> tuple:
    """Cambia sólo los nodos de texto; nunca atributos ni datos de trazo."""
    sin_traducir = []

    def bloque(m):
        partes = re.split(r"(<[^>]+>)", m.group(2))
        salida = []
        for p in partes:
            t = p.strip()
            if p.startswith("<") or not t:
                salida.append(p)
            elif t in d:
                salida.append(p.replace(t, d[t], 1))
            else:
                if not CODIGO.match(t) and t != "✕":
                    sin_traducir.append(t)
                salida.append(p)
        return m.group(1) + "".join(salida) + "</text>"

    return re.sub(r"(<text\b[^>]*>)(.*?)</text>", bloque, svg, flags=re.S), sin_traducir


def main() -> None:
    d = diccionario()
    for origen, destino in VERSIONES.items():
        svg = (AQUI / origen).read_text()
        alemán, faltan = traducir(svg, d)
        if faltan:
            raise SystemExit(
                f"{origen}: quedaron {len(faltan)} textos sin traducir, y un "
                f"afiche a medio traducir no sirve:\n  "
                + "\n  ".join(repr(t) for t in dict.fromkeys(faltan)))
        if "golondrina" in alemán or "Viaje al" in alemán:
            raise SystemExit(f"{destino}: quedó castellano suelto.")
        (AQUI / destino).write_text(alemán)
        print(f"{destino}: {len(re.findall(r'<text', alemán))} textos · "
              f"{len(re.findall(chr(60) + 'g class=.qr.', alemán))} QR intactos")


if __name__ == "__main__":
    main()
