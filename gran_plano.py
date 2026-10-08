#!/usr/bin/env python3
"""Lleva el planisferio a todo el ancho del pliego y saca el detalle de Sudamérica.

El planisferio está dibujado a una escala fija, pero la proyección se conoce
—Equal Earth, con el ecuador midiendo 2 × 395 mm y el centro en (423, 272)— y
eso vuelve la ampliación una semejanza: multiplicar por un factor es
exactamente lo mismo que volver a proyectar a mayor escala. No hay que
redibujar nada, ni volver a deducir nada.

Por eso va al final del canal: todo lo que se genera antes —el relieve, los
mares, los accidentes, los rótulos— sigue calculando en las coordenadas
originales, y acá escala junto con el dibujo.

Con el detalle fuera, el mapa pasa de 790 × 384,5 mm a 1133 × 551,5: más del
doble de superficie.
"""
import math
import re

from afiche import CARTELA
from pathlib import Path

AQUI = Path(__file__).parent
AFICHES = ("MAPA_FINAL_es_bn.svg", "MAPA_FINAL_es_color.svg",
           "MAPA_FINAL_de_bn.svg", "MAPA_FINAL_de_color.svg")

X0, Y0, SEMIANCHO = 423.0, 272.0, 395.0      # el planisferio como está dibujado
IZQUIERDA, DERECHA, ARRIBA = 28.0, 1161.0, 80.0

# La primera capa del mapa y la primera que ya no lo es: todo lo que queda en
# medio se amplía junto.
DESDE, HASTA = 'id="mapa-mundi"', 'id="referencias"'


def parametros():
    s = (DERECHA - IZQUIERDA) / 2 / SEMIANCHO
    alto = 2 * s * 192.2534                   # medio alto dibujado × 2
    cx = (IZQUIERDA + DERECHA) / 2
    cy = ARRIBA + alto / 2
    return s, cx - s * X0, cy - s * Y0, alto


def fin_de_grupo(svg: str, desde: int) -> int:
    nivel = 0
    for m in re.finditer(r"<g\b|</g>", svg[desde:]):
        nivel += 1 if m.group(0) != "</g>" else -1
        if nivel == 0:
            return desde + m.end()
    raise ValueError("no encontré el cierre del grupo")


A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
TINTA = "#3A3024"
MARGEN_MARCO = 14.0          # del borde del pliego al filete exterior
PLIEGO = (1189.0, 841.0)
PARALELOS = (60, 30, 0, -30, -60)
MERIDIANOS = (-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150)


def equal_earth(lon_g, lat_g):
    th = math.asin(math.sqrt(3) / 2 * math.sin(math.radians(lat_g)))
    t2, t6 = th * th, th ** 6
    x = (2 * math.sqrt(3) * math.radians(lon_g) * math.cos(th)
         / (3 * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2))))
    return x, th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))


def marco_y_grados() -> str:
    """El neto del pliego y los grados sobre la propia retícula.

    En Equal Earth los meridianos no llegan al marco —el mapa termina en una
    elipse— así que la graduación no puede ir en el borde como en una lámina
    rectangular. La latitud se escribe en los extremos de cada paralelo, en el
    papel que queda libre, y la longitud sobre el ecuador, que sí cruza el
    mapa de lado a lado.
    """
    s, tx, ty, alto = parametros()
    k = s * 145.9379
    cx = (IZQUIERDA + DERECHA) / 2
    cy = ARRIBA + alto / 2
    m, W, H = MARGEN_MARCO, *PLIEGO

    piezas = [f'<g id="marco" color="{TINTA}">'
              f'<rect x="{m}" y="{m}" width="{W - 2 * m}" height="{H - 2 * m}" '
              f'fill="none" stroke="currentColor" stroke-width="0.6"/>'
              f'<rect x="{m + 3}" y="{m + 3}" width="{W - 2 * m - 6}" '
              f'height="{H - 2 * m - 6}" fill="none" stroke="currentColor" '
              f'stroke-width="0.22"/>']

    for lat in PARALELOS:
        if lat == 0:
            continue
        xb, yb = equal_earth(180.0, lat)
        x_izq, y = cx - k * xb, cy - k * yb
        letra = "N" if lat > 0 else "S"
        for xx, ancla, signo in ((x_izq - 3.2, "end", -1), (2 * cx - x_izq + 3.2, "start", 1)):
            piezas.append(f'<text x="{xx:.1f}" y="{y + 1.3:.1f}" '
                          f'text-anchor="{ancla}" class="grado">'
                          f'{abs(lat)}° {letra}</text>')

    cx0, cy0, cx1, cy1 = CARTELA
    for lon in MERIDIANOS:
        if lon == 0:
            continue
        xb, _ = equal_earth(lon, 0.0)
        x = cx + k * xb
        # La cartela se apoya sobre el ecuador: los grados que caerían debajo
        # de ella no se escriben.
        if cx0 - 4 < x < cx1 + 4 and cy0 - 6 < cy < cy1 + 6:
            continue
        letra = "E" if lon > 0 else "O"
        piezas.append(f'<text x="{x:.1f}" y="{cy - 2.4:.1f}" '
                      f'text-anchor="middle" class="grado">{abs(lon)}° {letra}</text>')
    piezas.append("</g>")
    return "".join(piezas)


def velo() -> str:
    """Un velo cálido sobre el mapa, para la pátina de lámina antigua.

    Va en las coordenadas del dibujo sin ampliar, porque se inserta dentro del
    grupo que luego se escala: el recorte contra el marco del mapa sólo calza
    si los dos están en el mismo sistema.
    """
    return ('<g id="velo" clip-path="url(#solo-mapa)">'
            '<rect x="28" y="79.747" width="790" height="384.506" '
            'fill="#C9A869" opacity="0.07"/></g>')


ESTILO_GRADO = (".grado{font-family:'TeX Gyre Pagella','Palatino',serif;"
                "font-style:italic;font-size:3.2px;fill:%s;opacity:0.75}"
                % TINTA)


def despejar_el_arbol(svg: str) -> str:
    """Pone el rótulo de Heidelberg por encima de todo lo demás del mapa.

    El recorrido de «Otros vuelos» se dibuja después del planisferio, así que
    pasaba por encima del nombre y lo cruzaba. Acá se saca el marcador con sus
    dos líneas de texto y se los vuelve a poner al final del grupo, ya sin nada
    encima, con el halo blanco más grueso para que corte limpio.
    """
    m = re.search(
        r'<circle cx="[\d.]+" cy="[\d.]+" r="3\.4"[^>]*/>'
        r'<circle[^>]*r="1\.5"[^>]*/>'
        r'<text[^>]*class="lab origin"[^>]*>.*?</text>'
        r'<text[^>]*class="small"[^>]*>.*?</text>', svg, re.S)
    if not m:
        return svg
    bloque = m.group(0).replace('class="lab origin"',
                                'class="lab origin" style="stroke-width:1.9px"')
    bloque = bloque.replace('class="small"',
                            'class="small" style="paint-order:stroke;stroke:#fff;'
                            'stroke-width:1.5px;stroke-linejoin:round"', 1)
    svg = svg[:m.start()] + svg[m.end():]
    # Va al final del rango que se amplía, justo antes del cuadro de
    # referencias: ahí no le queda nada encima.
    cierre = svg.rindex("<g", 0, svg.index(HASTA))
    # El velo entra acá, dentro del rango que se amplía, para que su recorte
    # contra el marco del mapa siga valiendo.
    return svg[:cierre] + velo() + f'<g id="arbol">{bloque}</g>' + svg[cierre:]


def main() -> None:
    s, tx, ty, alto = parametros()
    print(f"ampliación ×{s:.5f} · el mapa pasa a "
          f"{DERECHA - IZQUIERDA:.0f} × {alto:.1f} mm")

    for nombre in AFICHES:
        ruta = AQUI / nombre
        svg = ruta.read_text()
        if 'id="plano"' in svg:
            print(f"{nombre}: ya estaba ampliado")
            continue

        # Fuera el detalle y las dos marcas que lo anunciaban en el planisferio.
        if 'id="detalle-sudamerica"' in svg:
            i = svg.rindex("<g", 0, svg.index('id="detalle-sudamerica"'))
            svg = svg[:i] + svg[fin_de_grupo(svg, i):]
        svg = re.sub(r'<rect[^>]*x="217\.93"[^>]*/>', "", svg, count=1)
        svg = re.sub(r"<text[^>]*>[^<]*ver detalle[^<]*</text>", "", svg,
                     count=1, flags=re.I)

        svg = despejar_el_arbol(svg)
        a = svg.rindex("<g", 0, svg.index(DESDE))
        b = svg.rindex("<g", 0, svg.index(HASTA))
        svg = (svg[:a]
               + f'<g id="plano" transform="translate({tx:.3f} {ty:.3f}) '
                 f'scale({s:.5f})">' + svg[a:b] + "</g>" + svg[b:])
        # El velo va dentro del grupo ampliado, recortado al marco del mapa;
        # el neto del pliego y los grados, fuera, en coordenadas finales.
        svg = svg.replace("</svg>", marco_y_grados() + "</svg>")
        if ".grado{" not in svg:
            svg = svg.replace("</style>", ESTILO_GRADO + "</style>", 1)
        ruta.write_text(svg)
        print(f"{nombre}: ampliado, detalle fuera, marco y grados puestos")


if __name__ == "__main__":
    main()
