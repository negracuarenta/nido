#!/usr/bin/env python3
"""Reproyecta el relieve sombreado de Natural Earth a la proyección del afiche.

El relieve viene en equirectangular —la cuadrícula cruda de latitud y
longitud— y el afiche está en Equal Earth, así que no alcanza con pegarlo:
hay que invertir la proyección. Para cada píxel de salida se calcula a qué
punto de la Tierra corresponde y se va a buscar ahí el valor de sombra.

La inversa de Equal Earth no es cerrada: la latitud auxiliar sale por Newton,
tres iteraciones bastan para quedar por debajo del píxel.

El color se vira a pergamino: cada píxel se lleva a un punto de una rampa de
dos tonos según su valor, con una pizca del color original encima para que la
selva, el desierto y el hielo sigan distinguiéndose.
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
AQUI = Path(__file__).parent
# Dos rásteres de Natural Earth: la tierra con su color real —verdes de bosque,
# ocres de desierto, blanco de hielo— y el fondo del océano, que trae las
# dorsales, las fosas y las plataformas continentales.
CAPAS = {
    "relieve": Path("/tmp/ne/NE1_50M_SR_W/NE1_50M_SR_W.tif"),
    "batimetria": Path("/tmp/ne/OB_50M/OB_50M.tif"),
}

A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
X0, Y0, SEMIANCHO = 423.0, 272.0, 395.0
PPP = 150                       # resolución de salida, en puntos por pulgada
# El color de Natural Earth es más saturado y más frío que el afiche. Se lo
# acerca al papel: se mezcla con el tono de tierra del mapa y se le baja la
# saturación, para que el verde de la selva se note sin que el mapa cambie de
# familia de color.
PAPEL = np.array([0xE9, 0xD4, 0xA4], float)   # el mismo del pergamino
# El viraje a pergamino. En vez de mezclar el color de Natural Earth con el
# papel —que lo aclara pero lo deja en su propia familia de color— se lo pasa
# por una rampa de dos tonos: el valor de cada píxel elige un punto entre el
# sepia oscuro y el crema claro. Eso es lo que hace que una lámina antigua se
# lea como una lámina antigua: toda la información está en el valor, no en el
# matiz.
#
# Del color original se devuelve una pizca —RESIDUO— para que el verde de la
# selva, el ocre del desierto y el blanco del hielo sigan distinguiéndose. Sin
# eso el mapa queda bonito y pierde la mitad de lo que dice.
#
# La tierra va a una rampa de ámbar y la del mar a una casi blanca: en los
# mapas viejos el agua es el tono liviano y la tierra la que pesa, al revés de
# lo que hace un mapa moderno con el mar azul. Invertirlo —que es lo que salía
# al principio— deja el continente flotando en blanco sobre un mar de color.
RAMPA = {
    "relieve": (np.array([0x5A, 0x3E, 0x18], float),
                np.array([0xE4, 0xCE, 0x9A], float)),
    "batimetria": (np.array([0xCB, 0xB9, 0x93], float),
                   np.array([0xF2, 0xE9, 0xD0], float)),
}
RESIDUO = {"relieve": 0.30, "batimetria": 0.05}
# Cuánto se estira el rango de valores antes de entrar a la rampa. El relieve
# de Natural Earth vive casi todo en la mitad clara y sin estirar sale lavado.
CONTRASTE = {"relieve": (0.20, 1.00), "batimetria": (0.20, 0.95)}


def directa(lon_rad, lat_rad):
    th = math.asin(math.sqrt(3) / 2 * math.sin(lat_rad))
    t2, t6 = th * th, th ** 6
    x = (2 * math.sqrt(3) * lon_rad * math.cos(th)
         / (3 * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2))))
    return x, th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))


def escala() -> float:
    """El ecuador entero mide 2 × 395 mm en el afiche."""
    return SEMIANCHO / directa(math.pi, 0.0)[0]


def inversa(X, Y):
    """De coordenadas de proyección a longitud y latitud, en grados."""
    th = Y.copy()
    for _ in range(6):
        t2, t6 = th * th, th ** 6
        f = th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2)) - Y
        d = A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)
        th -= f / d
    t2, t6 = th * th, th ** 6
    D = A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)
    sen = np.sin(th) / (math.sqrt(3) / 2)
    dentro = np.abs(sen) <= 1
    lat = np.degrees(np.arcsin(np.clip(sen, -1, 1)))
    lon = np.degrees(3 * X * D / (2 * math.sqrt(3) * np.cos(th)))
    return lon, lat, dentro & (np.abs(lon) <= 180.0001)


def main() -> None:
    for nombre, origen in CAPAS.items():
        convertir(nombre, origen)


def convertir(nombre: str, origen: Path) -> None:
    k = escala()
    ancho_mm = 2 * SEMIANCHO
    alto_mm = 2 * k * directa(0.0, math.pi / 2)[1]   # del polo al polo
    W = round(ancho_mm / 25.4 * PPP)
    H = round(alto_mm / 25.4 * PPP)
    print(f"{nombre}: {W}×{H} px para {ancho_mm:.1f}×{alto_mm:.1f} mm a {PPP} ppp")

    # Suavizo la fuente antes de muestrear: vamos de 30 px por grado a 13,
    # y sin este paso las cordilleras aparecen dentadas.
    src = Image.open(origen).convert("RGB").resize((5400, 2700), Image.LANCZOS)
    g = np.asarray(src, dtype=np.float32)
    sh, sw = g.shape[:2]

    xs = (np.arange(W) + 0.5) / W * ancho_mm + (X0 - SEMIANCHO)
    ys = (np.arange(H) + 0.5) / H * alto_mm + (Y0 - alto_mm / 2)
    X = (xs[None, :] - X0) / k
    Y = (Y0 - ys[:, None]) / k
    lon, lat, dentro = inversa(np.broadcast_to(X, (H, W)).astype(np.float64),
                               np.broadcast_to(Y, (H, W)).astype(np.float64))

    col = (lon + 180) / 360 * sw - 0.5
    fil = (90 - lat) / 180 * sh - 0.5
    c0 = np.clip(np.floor(col), 0, sw - 1).astype(np.int32)
    f0 = np.clip(np.floor(fil), 0, sh - 1).astype(np.int32)
    c1 = np.minimum(c0 + 1, sw - 1); f1 = np.minimum(f0 + 1, sh - 1)
    tc = (col - c0).clip(0, 1)[..., None]
    tf = (fil - f0).clip(0, 1)[..., None]
    muestra = ((g[f0, c0] * (1 - tc) + g[f0, c1] * tc) * (1 - tf)
               + (g[f1, c0] * (1 - tc) + g[f1, c1] * tc) * tf)

    # Luminancia perceptual, no promedio de canales: el verde de la selva y el
    # azul de la fosa tienen el mismo promedio y pesos muy distintos en el ojo.
    luz = (muestra * np.array([0.2126, 0.7152, 0.0722])).sum(axis=2, keepdims=True)
    lo, hi = CONTRASTE[nombre]
    t = np.clip((luz / 255.0 - lo) / (hi - lo), 0, 1)
    sombra, brillo = RAMPA[nombre]
    rgb = sombra + (brillo - sombra) * t
    rgb += (muestra - luz) * RESIDUO[nombre]      # la pizca de color que queda
    rgb[~dentro] = PAPEL
    rgb = np.clip(rgb, 0, 255)

    guardar(rgb.astype(np.uint8), f"{nombre}.jpg")
    # La versión a una tinta lleva su propio raster en gris. Desaturarlo con un
    # filtro de SVG también funcionaba, pero Chrome rasteriza el grupo filtrado
    # entero al imprimir y el PDF pasaba de 8 a 42 MB.
    luz = (rgb * np.array([0.2126, 0.7152, 0.0722])).sum(axis=2, keepdims=True)
    guardar(np.repeat(np.clip(luz, 0, 255), 3, axis=2).astype(np.uint8),
            f"{nombre}_bn.jpg")


def guardar(rgb, nombre: str) -> None:
    salida = AQUI / "assets/geo" / nombre
    Image.fromarray(rgb).save(salida, quality=88, subsampling=0)
    print(f"{salida.name}: {salida.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
