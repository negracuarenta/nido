#!/usr/bin/env python3
"""Pone los grabados de animales sobre el planisferio, donde esos animales viven.

Los mapas antiguos llevaban bichos dibujados en las regiones donde se sabía que
habitaban. Acá se hace lo mismo con cuatro grabados del siglo XIX en dominio
público, y los cuatro son animales que la obra nombra: la golondrina que cuenta
la historia, el pingüino emperador de la Antártida, el albatros errante de las
Georgias y el camello bactriano del Gobi.

No se colocan a ojo: se les busca un hueco libre cerca de su región, con el
mismo criterio que a los nombres de los lugares.
"""
import base64
import json
import math
import re
from pathlib import Path

from etiquetas import chocan, obstaculos
from expresividad import proyectar

AQUI = Path(__file__).parent
AFICHES = ("MAPA_FINAL_es_bn.svg", "MAPA_FINAL_es_color.svg")
GRABADOS = AQUI / "assets/grabados"
ALTO = 19.0          # alto de la viñeta en el afiche, en mm

# Dónde mirar primero. Es la región del animal, no el punto exacto: desde ahí
# se busca el primer hueco libre.
DESTINOS = {
    "Hirundo": (-27, 46),        # Atlántico Norte, de camino a Heidelberg
    "Diomedea": (-18, -42),      # Atlántico Sur, cerca de las Georgias
    "Aptenodytes": (95, -64),    # océano Antártico
    "Camelus": (88, 50),         # Asia central, al norte del Gobi
}
RADIOS = (0, 10, 20, 32, 46, 62, 80, 100)
ANGULOS = (0, 45, -45, 90, -90, 135, -135, 180)


def grupo(svg: str) -> str:
    ocupado = obstaculos(svg)
    piezas = ['<g id="animales">']
    for clave, (lon, lat) in DESTINOS.items():
        archivo = GRABADOS / f"{clave}.png"
        if not archivo.exists():
            continue
        import struct
        png = archivo.read_bytes()
        w, h = struct.unpack(">II", png[16:24])
        ancho = ALTO * w / h
        cx, cy = proyectar(lon, lat)
        puesto = False
        for r in RADIOS:
            for ang in ANGULOS:
                x = cx + r * math.cos(math.radians(ang)) - ancho / 2
                y = cy + r * math.sin(math.radians(ang)) * 0.6 - ALTO / 2
                caja = (x - 2, y - 2, x + ancho + 2, y + ALTO + 2)
                if any(chocan(caja, c) for c in ocupado):
                    continue
                ocupado.append(caja)
                datos = base64.b64encode(png).decode()
                piezas.append(
                    f'<image x="{x:.1f}" y="{y:.1f}" width="{ancho:.1f}" '
                    f'height="{ALTO}" opacity="0.72" '
                    f'href="data:image/png;base64,{datos}"/>')
                puesto = True
                break
            if puesto:
                break
        if not puesto:
            print(f"   (a {clave} no le encontré hueco)")
    piezas.append("</g>")
    return "".join(piezas)


def main() -> None:
    for nombre in AFICHES:
        ruta = AQUI / nombre
        svg = re.sub(r'<g id="animales">.*?</g>', "", ruta.read_text(),
                     count=1, flags=re.S)
        g = grupo(svg)
        ruta.write_text(svg.replace('<g id="rotulos">', g + '<g id="rotulos">', 1))
        print(f"{nombre}: {len(re.findall('<image', g))} grabados colocados")


if __name__ == "__main__":
    main()
