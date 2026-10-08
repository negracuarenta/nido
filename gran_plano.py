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
    return svg[:cierre] + f'<g id="arbol">{bloque}</g>' + svg[cierre:]


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
        ruta.write_text(svg)
        print(f"{nombre}: ampliado, detalle fuera")


if __name__ == "__main__":
    main()
