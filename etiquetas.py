#!/usr/bin/env python3
"""Pone nombre a los lugares que en el planisferio sólo tenían un punto.

Veintitrés de los cuarenta y cuatro están amontonados en Sudamérica, que por
eso tiene su propio recuadro de detalle. Pero un punto sin nombre en el mapa
grande obliga a buscarlo en otro lado, así que acá se nombran todos.

No se puede poner el nombre pegado al punto: se pisarían entre ellos. Lo que
hace esto es buscarle sitio a cada uno —probando posiciones en anillos cada vez
más amplios alrededor del punto, como haría un cartógrafo— y, cuando el nombre
queda lejos, tirar una línea de guía fina que lo ate a su punto.

Se respeta todo lo que ya está dibujado: las etiquetas a mano, los nombres de
mar y el recuadro de detalle.
"""
import json
import math
import re
from pathlib import Path

from expresividad import proyectar

AQUI = Path(__file__).parent
AFICHES = ("MAPA_FINAL_es_bn.svg", "MAPA_FINAL_es_color.svg")

COLOR = {"E": "#D9822B", "S": "#2B6CB0", "O": "#2F8F5B", "OV": "#6B4E9B"}
CUERPO = 3.1            # cuerpo de letra, como las etiquetas ya dibujadas
AVANCE = 0.53           # ancho de un carácter en fracción del cuerpo, medido
                        # sobre el render: la estimación a ojo se quedaba corta
MARGEN = 0.9            # aire mínimo entre dos rótulos, en mm
GUIA_DESDE = 7.0        # a partir de esta distancia se dibuja la línea

# Posiciones a probar: primero cerca y de costado, después cada vez más lejos.
RADIOS = (4.5, 9, 15, 22, 30, 40, 52, 66, 82)
ANGULOS = (0, 180, -20, 200, 20, 160, -40, 220, 40, 140, -65, 245, 65, 115,
           -90, 270)


def caja_texto(nombre, codigo, x, y, ancla):
    ancho = (len(codigo) + 1 + len(nombre)) * CUERPO * AVANCE
    alto = CUERPO * 1.15
    x0 = x if ancla == "start" else x - ancho
    return (x0 - MARGEN, y - alto * 0.8 - MARGEN,
            x0 + ancho + MARGEN, y + alto * 0.25 + MARGEN)


def chocan(a, b):
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


# Ancho de un carácter en fracción del cuerpo, medido sobre el afiche ya
# compuesto. Cada clase tiene el suyo: la versalita espaciada de los accidentes
# ocupa casi el doble que el texto corriente de un rótulo.
AVANCES = {"accidente": 0.90, "mar": 0.95, "lab": 0.53}


def obstaculos(svg: str) -> list:
    """Lo que ya ocupa sitio en el planisferio, con su caja real."""
    a = svg.index('id="mapa-mundi"')
    # El planisferio termina donde empieza lo que venga después: el detalle de
    # Sudamérica mientras exista, y si no, el cuadro de referencias.
    b = next(svg.index(x) for x in ('id="detalle-sudamerica"', 'id="referencias"')
             if x in svg)
    m, cajas = svg[a:b], []
    for t in re.finditer(r'<text x="([-\d.]+)" y="([-\d.]+)"([^>]*)>(.*?)</text>',
                         m, re.S):
        x, y, attrs, cuerpo = float(t.group(1)), float(t.group(2)), t.group(3), t.group(4)
        texto = re.sub(r"<[^>]+>", "", cuerpo)
        if not texto.strip():
            continue
        tam = float(re.search(r"font-size:([\d.]+)", attrs).group(1)) \
            if "font-size:" in attrs else CUERPO
        clase = next((c for c in AVANCES if f'class="{c}"' in attrs), "lab")
        ancho = len(texto) * tam * AVANCES[clase]
        alto = tam * 1.3
        ancla = re.search(r'text-anchor="(\w+)"', attrs)
        ancla = ancla.group(1) if ancla else "start"
        x0 = {"start": x, "end": x - ancho, "middle": x - ancho / 2}[ancla]
        y0 = y - tam
        giro = re.search(r"rotate\(([-\d.]+)", attrs)
        if giro:
            # Tumbado: la caja que ocupa es la del rectángulo girado.
            rad = math.radians(float(giro.group(1)))
            cx, cy = x0 + ancho / 2, y0 + alto / 2
            anc = abs(ancho * math.cos(rad)) + abs(alto * math.sin(rad))
            alt = abs(ancho * math.sin(rad)) + abs(alto * math.cos(rad))
            x0, y0, ancho, alto = cx - anc / 2, cy - alt / 2, anc, alt
        cajas.append((x0, y0, x0 + ancho, y0 + alto))
    return cajas


def grupo(svg: str, lang: str = "es") -> str:
    """Arma el grupo de rótulos para un idioma, sobre el afiche que se le pase.

    Se calcula por idioma y no se traduce: los nombres alemanes tienen otro
    largo, así que las posiciones que sirven en castellano no tienen por qué
    servir en alemán.
    """
    lugares = json.loads((AQUI / "nido_lugares.json").read_text())
    a, b = svg.index('id="mapa-mundi"'), svg.index('id="detalle-sudamerica"')
    ya = set(re.findall(r'<tspan class="code"[^>]*>([A-Z]+\d+)</tspan>', svg[a:b]))
    ocupado = obstaculos(svg)

    faltan = []
    for viaje in lugares["trips"]:
        for l in viaje["places"]:
            if l["id"] not in ya:
                nombre = (l.get("names") or {}).get(lang) or l["name"]
                x, y = proyectar(l["lon"], l["lat"])
                faltan.append((viaje["key"], l["id"], nombre, x, y))
    faltan.sort(key=lambda t: t[4])

    piezas, sin_sitio = ['<g id="rotulos">'], []
    for clave, ident, nombre, px, py in faltan:
        puesto = False
        for r in RADIOS:
            for ang in ANGULOS:
                dx = r * math.cos(math.radians(ang))
                dy = r * math.sin(math.radians(ang)) * 0.55      # anillo achatado
                ancla = "start" if dx >= 0 else "end"
                x, y = px + dx, py + dy + CUERPO * 0.35
                caja = caja_texto(nombre, ident, x, y, ancla)
                if any(chocan(caja, c) for c in ocupado):
                    continue
                ocupado.append(caja)
                if r >= GUIA_DESDE:
                    ex = x - (1.2 if ancla == "start" else -1.2)
                    piezas.append(
                        f'<path d="M{px:.1f},{py:.1f}L{ex:.1f},{y - 1:.1f}" '
                        f'fill="none" stroke="{COLOR[clave]}" stroke-width="0.18" '
                        f'opacity="0.65"/>')
                piezas.append(
                    f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{ancla}" '
                    f'class="lab" style="font-size:{CUERPO}px">'
                    f'<tspan class="code" style="font-size:{CUERPO * 0.72:.2f}px">'
                    f'{ident}</tspan> {nombre}</text>')
                puesto = True
                break
            if puesto:
                break
        if not puesto:
            sin_sitio.append(ident)
    if sin_sitio:
        raise SystemExit(f"no les encontré sitio a {sin_sitio} en {lang}. "
                         f"Un punto sin nombre es justo lo que había que arreglar.")
    piezas.append("</g>")
    return "".join(piezas)


def main() -> None:
    for nombre_archivo in AFICHES:
        ruta = AQUI / nombre_archivo
        svg = re.sub(r'<g id="rotulos">.*?</g>', "", ruta.read_text(),
                     count=1, flags=re.S)
        g = grupo(svg, "es")
        ruta.write_text(svg.replace('<g id="otros-vuelos">', g + '<g id="otros-vuelos">', 1))
        print(f"{nombre_archivo}: {len(re.findall(chr(60) + 'text', g))} nombres nuevos, "
              f"{len(re.findall(chr(60) + 'path', g))} con línea de guía")


if __name__ == "__main__":
    main()
