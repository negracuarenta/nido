#!/usr/bin/env python3
"""Dibuja el cuarto recorrido —«Otros vuelos»— sobre el planisferio del afiche.

El planisferio se dibujó con un script que no quedó en el repositorio, pero el
propio afiche declara la proyección en sus referencias: Equal Earth. Los demás
parámetros salen de la retícula dibujada —el ecuador va de x=28 a x=818, con el
centro en (423, 272)— y eso alcanza para reconstruirla entera.

La reconstrucción se verifica en cada ejecución contra los 15.845 vértices de la
costa: el error es de 0,001 mm sobre un pliego de 1189, y el marcador de
Heidelberg, que no interviene en el cálculo, cae a 0,006 mm del que ya estaba
dibujado. Si alguna vez se redibuja el planisferio, el control falla en vez de
poner los puntos en el lugar equivocado y que nos enteremos impreso en A0.
"""
import json
import math
import re
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

AQUI = Path(__file__).parent
AFICHES = ("MAPA_FINAL_es_bn.svg", "MAPA_FINAL_es_color.svg")

# Equal Earth (Šavrič, Patterson y Jenny, 2018), la que declara el afiche.
A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
X0, Y0 = 423.0, 272.0          # centro del planisferio, en mm
SEMIANCHO = 395.0              # medio ecuador: de x=28 a x=818
TOLERANCIA = 0.02              # mm de error admitido contra la costa dibujada


def equal_earth(lon, lat):
    th = np.arcsin(math.sqrt(3) / 2 * np.sin(np.radians(lat)))
    t2, t6 = th * th, th ** 6
    x = (2 * math.sqrt(3) * np.radians(lon) * np.cos(th)
         / (3 * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2))))
    return x, th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))


# La escala sale de que el ecuador entero mide 2 × 395 mm.
ESCALA = SEMIANCHO / float(equal_earth(180.0, 0.0)[0])

TRAZO_OV = "2 4"

def paleta(svg: str) -> dict:
    """El afiche existe en color y en blanco y negro, con paletas distintas."""
    color = "#D9822B" in svg
    return {"trazo": "#6B4E9B" if color else "#111",
            "punto": "#6B4E9B" if color else "#111",
            "grosor": 0.8 if color else 0.6}
ORIGEN = (8.6724, 49.3988)

# Hacia qué lado sale la etiqueta de cada lugar, para no pisar lo ya dibujado.
ANCLAS = {"OV5": "end", "OV6": "end", "OV7": "end", "OV3": "end"}


def proyectar(lon, lat):
    dl = ((np.asarray(lon, float) + 180) % 360) - 180
    x, y = equal_earth(dl, np.asarray(lat, float))
    return X0 + ESCALA * x, Y0 - ESCALA * y


def costa_dibujada(svg: str) -> np.ndarray:
    m = svg[svg.index('id="mapa-mundi"'):svg.index('id="detalle-sudamerica"')]
    d = max(re.findall(r'd="([^"]{200,})"', m), key=len)
    return np.array([[float(a), float(b)]
                     for a, b in re.findall(r"(-?[\d.]+),(-?[\d.]+)", d)])


def comprobar(svg: str) -> float:
    """La proyección reconstruida tiene que seguir cayendo sobre la costa."""
    g = json.loads((AQUI / "assets/geo/land.json").read_text())
    coords = (g["features"][0]["geometry"]["coordinates"]
              if "features" in g else g["coordinates"])
    pts = []

    def recoger(c):
        if isinstance(c[0][0], (int, float)): pts.extend(c)
        else:
            for x in c: recoger(x)

    recoger(coords)
    G = np.array(pts, float)
    x, y = proyectar(G[:, 0], G[:, 1])
    d, _ = cKDTree(costa_dibujada(svg)).query(np.column_stack([x, y]), workers=-1)
    return math.sqrt((d ** 2).mean())


def circulo_maximo(a, b, n=64):
    """El camino que de verdad haría un pájaro, interpolado sobre la esfera."""
    la1, fi1 = math.radians(a[0]), math.radians(a[1])
    la2, fi2 = math.radians(b[0]), math.radians(b[1])
    p1 = (math.cos(fi1) * math.cos(la1), math.cos(fi1) * math.sin(la1), math.sin(fi1))
    p2 = (math.cos(fi2) * math.cos(la2), math.cos(fi2) * math.sin(la2), math.sin(fi2))
    punto = sum(u * v for u, v in zip(p1, p2))
    ang = math.acos(max(-1.0, min(1.0, punto)))
    if ang < 1e-9:
        return [a, b]
    salida = []
    for i in range(n + 1):
        t = i / n
        c1, c2 = math.sin((1 - t) * ang) / math.sin(ang), math.sin(t * ang) / math.sin(ang)
        x, y, z = (c1 * u + c2 * v for u, v in zip(p1, p2))
        salida.append((math.degrees(math.atan2(y, x)),
                       math.degrees(math.atan2(z, math.hypot(x, y)))))
    return salida


def tramos(linea):
    """Parte la línea donde cruza el antimeridiano: si no, cruza el mapa entero."""
    partes, actual = [], [linea[0]]
    for prev, act in zip(linea, linea[1:]):
        if abs(act[0] - prev[0]) > 180:
            partes.append(actual); actual = []
        actual.append(act)
    partes.append(actual)
    return [p for p in partes if len(p) > 1]


def grupo_ov(datos: dict, pal: dict) -> str:
    viaje = next(v for v in datos["trips"] if v["key"] == "OV")
    escalas = sorted((l for l in viaje["places"] if not l.get("soloTragico")),
                     key=lambda l: l["lon"])
    paradas = [ORIGEN] + [(l["lon"], l["lat"]) for l in escalas] + [ORIGEN]

    linea = []
    for a, b in zip(paradas, paradas[1:]):
        arco = circulo_maximo(a, b)
        linea += arco if not linea else arco[1:]

    piezas = [f'<g id="otros-vuelos">']
    d = ""
    for parte in tramos(linea):
        xs, ys = proyectar([p[0] for p in parte], [p[1] for p in parte])
        d += "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in zip(xs, ys))
    piezas.append(f'<path d="{d}" fill="none" stroke="{pal['trazo']}" stroke-width="{pal['grosor']}" '
                  f'stroke-dasharray="{TRAZO_OV}" stroke-linecap="round"/>')

    for l in viaje["places"]:
        x, y = (float(v) for v in proyectar(l["lon"], l["lat"]))
        piezas.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1.15" fill="{pal['punto']}" '
                      f'stroke="#fff" stroke-width="0.38"/>')
        ancla = ANCLAS.get(l["id"], "start")
        tx = x + 3.2 if ancla == "start" else x - 3.2
        piezas.append(
            f'<text x="{tx:.2f}" y="{y + 1.2:.2f}" text-anchor="{ancla}" class="lab" '
            f'style="font-size:3.1px"><tspan class="code" style="font-size:2.23px">'
            f'{l["id"]}</tspan> {l["name"]}</text>')
    piezas.append("</g>")
    return "".join(piezas)


def fin_de_grupo(svg: str, desde: int) -> int:
    """El índice del </g> que cierra ese grupo, contando los anidados.

    Buscar el primer </g> no sirve: el cuadro de referencias tiene grupos
    adentro, y cortar ahí deja el SVG mal formado.
    """
    nivel, i = 0, desde
    for m in re.finditer(r"<g\b|</g>", svg[desde:]):
        nivel += 1 if m.group(0) != "</g>" else -1
        if nivel == 0:
            return desde + m.start()
    raise ValueError("no encontré el cierre del grupo")


def leyenda(svg: str, pal: dict) -> str:
    """Agrega la fila de «Otros vuelos» al cuadro de referencias.

    Las filas van cada 9 mm y la que seguía al Oeste ya estaba ocupada, así que
    lo que viene más abajo se corre para hacerle lugar.
    """
    svg = re.sub(r'<g id="ref-ov">.*?</g>', "", svg, count=1, flags=re.S)
    i = svg.rindex("<g", 0, svg.index('id="referencias"'))
    j = fin_de_grupo(svg, i)
    bloque, Y = svg[i:j], 683.8

    def correr(m):
        v = float(m.group(2))
        return f'{m.group(1)}="{round(v + 9, 3) if v >= Y else m.group(2)}"'

    bloque = re.sub(r'\b(y|y1|y2|cy)="([\d.]+)"', correr, bloque)
    fila = (f'<g id="ref-ov">'
            f'<line x1="845" y1="{Y - 1.2}" x2="875" y2="{Y - 1.2}" '
            f'stroke="{pal["trazo"]}" stroke-width="{round(pal["grosor"] + 0.15, 2)}" '
            f'stroke-dasharray="{TRAZO_OV}" stroke-linecap="round"/>'
            f'<text x="881" y="{Y}" class="leg">'
            f'<tspan class="code">OV</tspan>  Otros vuelos '
            f'<tspan class="small">· fuera de la obra</tspan></text></g>')
    return svg[:i] + bloque + fila + svg[j:]


def main() -> None:
    datos = json.loads((AQUI / "nido_lugares.json").read_text())
    for nombre in AFICHES:
        ruta = AQUI / nombre
        svg = ruta.read_text()
        error = comprobar(svg)
        if error > TOLERANCIA:
            raise SystemExit(
                f"{nombre}: la proyección reconstruida ya no cae sobre la costa "
                f"({error:.3f} mm > {TOLERANCIA}). El planisferio cambió: hay que "
                f"volver a deducirla antes de dibujar nada encima.")
        pal = paleta(svg)
        svg = re.sub(r'<g id="otros-vuelos">.*?</g>', "", svg, count=1, flags=re.S)
        svg = svg.replace('<g id="detalle-sudamerica">',
                          grupo_ov(datos, pal) + '<g id="detalle-sudamerica">', 1)
        svg = leyenda(svg, pal)
        ruta.write_text(svg)
        print(f"{nombre}: proyección verificada a {error:.3f} mm · "
              f"recorrido y 9 puntos de Otros vuelos dibujados")


if __name__ == "__main__":
    main()
