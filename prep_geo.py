#!/usr/bin/env python3
"""Simplifica el GeoJSON de Natural Earth para que el mapa pese poco en celular.

Natural Earth 50m viene con un detalle pensado para imprenta: 2,7 MB. Acá el
mapa se mira a escala mundial o de continente, así que se puede bajar mucho sin
que se note. Se corre a mano cuando cambia el origen; el resultado se versiona.
"""
import json
from pathlib import Path

AQUI = Path(__file__).parent
ENTRADA = AQUI / "assets/geo/ne_50m_land.json"
SALIDA = AQUI / "assets/geo/land.json"

EPSILON = 0.06      # grados (~6 km): a escala mundial no se nota, y pesa un tercio
AREA_MINIMA = 0.05  # grados²: descarta islotes que a esta escala son un píxel
DECIMALES = 3


def douglas_peucker(puntos, eps):
    if len(puntos) < 3:
        return puntos
    # Distancia perpendicular de cada punto a la recta extremo-extremo.
    (x1, y1), (x2, y2) = puntos[0], puntos[-1]
    dx, dy = x2 - x1, y2 - y1
    norma = (dx * dx + dy * dy) ** 0.5
    peor, idx = 0.0, 0
    for i in range(1, len(puntos) - 1):
        x, y = puntos[i]
        d = (abs(dy * x - dx * y + x2 * y1 - y2 * x1) / norma) if norma else (
            ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5)
        if d > peor:
            peor, idx = d, i
    if peor <= eps:
        return [puntos[0], puntos[-1]]
    return douglas_peucker(puntos[:idx + 1], eps)[:-1] + douglas_peucker(puntos[idx:], eps)


def area(anillo):
    # Área por la fórmula del cordón de zapato; sólo para descartar islotes.
    s = sum(anillo[i][0] * anillo[i + 1][1] - anillo[i + 1][0] * anillo[i][1]
            for i in range(len(anillo) - 1))
    return abs(s) / 2


def limpiar_anillo(anillo):
    simple = douglas_peucker([tuple(p) for p in anillo], EPSILON)
    if len(simple) < 4 or area(simple) < AREA_MINIMA:
        return None
    red = [[round(x, DECIMALES), round(y, DECIMALES)] for x, y in simple]
    if red[0] != red[-1]:
        red.append(red[0])
    return red


def limpiar_poligono(poli):
    anillos = [r for r in (limpiar_anillo(a) for a in poli) if r]
    return anillos or None


def main() -> None:
    datos = json.loads(ENTRADA.read_text())
    salida = []
    for f in datos["features"]:
        g = f["geometry"]
        if g["type"] == "Polygon":
            nuevo = limpiar_poligono(g["coordinates"])
            if nuevo:
                salida.append({"type": "Polygon", "coordinates": nuevo})
        elif g["type"] == "MultiPolygon":
            partes = [p for p in (limpiar_poligono(x) for x in g["coordinates"]) if p]
            if partes:
                salida.append({"type": "MultiPolygon", "coordinates": partes})

    # Todo en un único MultiPolygon. Repartido en mil features, Leaflet creaba
    # mil capas y hacía mil llamadas de dibujo por cuadro al hacer zoom; con una
    # sola capa el costo por cuadro cae de golpe.
    partes = []
    for g in salida:
        if g["type"] == "Polygon":
            partes.append(g["coordinates"])
        else:
            partes.extend(g["coordinates"])
    fc = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {},
         "geometry": {"type": "MultiPolygon", "coordinates": partes}}]}
    SALIDA.write_text(json.dumps(fc, separators=(",", ":")))
    antes = ENTRADA.stat().st_size / 1024
    despues = SALIDA.stat().st_size / 1024
    vertices = sum(len(a) for p in partes for a in p)
    print(f"{len(datos['features'])} features → 1 capa con {len(partes)} polígonos "
          f"y {vertices} vértices | {antes:.0f} KB → {despues:.0f} KB ({despues/antes:.0%})")


if __name__ == "__main__":
    main()
