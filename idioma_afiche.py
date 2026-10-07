#!/usr/bin/env python3
"""Genera la versión alemana del afiche a partir de la castellana.

Cambia el texto y los códigos QR. La geometría es idéntica: cada código ocupa
exactamente el mismo recuadro, en el mismo lugar.

Los QR del afiche castellano no fuerzan idioma —la misma dirección sirve para
los tres y el sitio elige según el navegador—, pero los del alemán llevan
`?lang=de`. Quien está parado frente a un afiche en alemán y escanea un código
espera que la ficha abra en alemán, no en castellano.

Va después de afiche.py y planisferio.py, porque traduce lo que ellos dejaron.

Los nombres de los lugares salen de nido_lugares.json y las frases que ya
existen en el sitio, de content/site.json, para no traducir dos veces lo mismo
y que el afiche y la web no se contradigan.
"""
import json
import re

import etiquetas
import expresividad
from pathlib import Path

AQUI = Path(__file__).parent
VERSIONES = {"MAPA_FINAL_es_bn.svg": "MAPA_FINAL_de_bn.svg",
             "MAPA_FINAL_es_color.svg": "MAPA_FINAL_de_color.svg"}

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
GRUPO_QR = re.compile(
    r'<g class="qr" id="qr-([^"]+)" transform="translate\(([\d.]+) ([\d.]+)\) '
    r'scale\(([\d.]+)\)"><path d="[^"]*"([^/]*)/></g>')


def modulos(ruta: Path) -> tuple:
    """Lado en módulos y trazo de un QR, tal como lo deja segno."""
    f = ruta.read_text()
    ancho = int(re.search(r'width="(\d+)"', f).group(1))
    escala = int(re.search(r"scale\((\d+)\)", f).group(1))
    return ancho // escala, re.search(r'\sd="([^"]+)"', f).group(1)


def cambiar_qr(svg: str) -> tuple:
    """Pone los códigos alemanes en el mismo recuadro que ocupaban los otros.

    El QR alemán puede tener otra cantidad de módulos —la dirección es más
    larga—, así que la escala se recalcula para que el recuadro no se mueva ni
    cambie de tamaño: el diseño del índice no se entera.
    """
    cambiados = []

    def uno(m):
        codigo, x, y, k, resto = m.groups()
        mods_es, _ = modulos(AQUI / "qr" / f"{codigo}.svg")
        lado = float(k) * mods_es
        mods_de, trazo = modulos(AQUI / "qr/de" / f"{codigo}.svg")
        cambiados.append(codigo)
        return (f'<g class="qr" id="qr-{codigo}" transform="translate({x} {y}) '
                f'scale({lado / mods_de:.6f})"><path d="{trazo}"{resto}/></g>')

    return GRUPO_QR.sub(uno, svg), cambiados


def diccionario() -> dict:
    d = dict(PROPIAS)
    site = json.loads((AQUI / "content/site.json").read_text())
    d["Los vuelos de la golondrina"] = site["subtitulo"]["de"]
    d["Otros vuelos"] = site["viajes"]["OV"]["de"]
    d["Lo que también vio"] = site["ui"]["capa_tragica"]["de"]
    d["Punto 0 · el árbol"] = site["ui"]["punto_cero"]["de"]
    d["Con"] = site["ui"]["con_apoyo"]["de"]
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
        # Los nombres de mar no se traducen a mano: se vuelven a generar desde
        # Natural Earth, que los trae en alemán. Se apartan antes de traducir
        # para que el control de textos sin traducir no los marque.
        pal = expresividad.PALETAS["color" if "#D9822B" in svg else "bn"]
        svg = re.sub(r'<g id="mares">.*?</g>', "<!--MARES-->", svg,
                     count=1, flags=re.S)
        svg = re.sub(r'<g id="rotulos">.*?</g>', "", svg, count=1, flags=re.S)
        alemán, faltan = traducir(svg, d)
        alemán = alemán.replace("<!--MARES-->", expresividad.mares(pal, "de"), 1)
        # Los rótulos se recalculan en alemán: otro largo, otras posiciones.
        alemán = alemán.replace('<g id="otros-vuelos">',
                                etiquetas.grupo(alemán, "de") + '<g id="otros-vuelos">', 1)
        alemán, qr_cambiados = cambiar_qr(alemán)
        if faltan:
            raise SystemExit(
                f"{origen}: quedaron {len(faltan)} textos sin traducir, y un "
                f"afiche a medio traducir no sirve:\n  "
                + "\n  ".join(repr(t) for t in dict.fromkeys(faltan)))
        if "golondrina" in alemán or "Viaje al" in alemán:
            raise SystemExit(f"{destino}: quedó castellano suelto.")
        total_qr = len(re.findall(r'<g class="qr"', alemán))
        if len(qr_cambiados) != total_qr:
            raise SystemExit(
                f"{destino}: cambié {len(qr_cambiados)} de {total_qr} códigos; "
                f"un afiche con códigos mezclados manda a la ficha equivocada.")
        (AQUI / destino).write_text(alemán)
        print(f"{destino}: {len(re.findall(r'<text', alemán))} textos traducidos · "
              f"{total_qr} QR cambiados a ?lang=de")


if __name__ == "__main__":
    main()
