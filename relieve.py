#!/usr/bin/env python3
"""Reproyecta el relieve sombreado de Natural Earth a la proyección del afiche.

El relieve viene en equirectangular —la cuadrícula cruda de latitud y
longitud— y el afiche está en Equal Earth, así que no alcanza con pegarlo:
hay que invertir la proyección. Para cada píxel de salida se calcula a qué
punto de la Tierra corresponde y se va a buscar ahí el valor de sombra.

La inversa de Equal Earth no es cerrada: la latitud auxiliar sale por Newton,
tres iteraciones bastan para quedar por debajo del píxel.

El gris se tiñe con los dos tonos del afiche, para que la cordillera aparezca
sin que el mapa cambie de color.
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
AQUI = Path(__file__).parent
ORIGEN = Path("/tmp/ne/SR_50M.tif")
SALIDA = AQUI / "assets/geo/relieve.jpg"

A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
X0, Y0, SEMIANCHO = 423.0, 272.0, 395.0
PPP = 150                       # resolución de salida, en puntos por pulgada
CLARO = np.array([0xF7, 0xF2, 0xE4], float)   # cumbres iluminadas
OSCURO = np.array([0x8A, 0x7C, 0x60], float)  # laderas en sombra


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
    k = escala()
    ancho_mm = 2 * SEMIANCHO
    alto_mm = 2 * k * directa(0.0, math.pi / 2)[1]   # del polo al polo
    W = round(ancho_mm / 25.4 * PPP)
    H = round(alto_mm / 25.4 * PPP)
    print(f"salida: {W}×{H} px para {ancho_mm:.1f}×{alto_mm:.1f} mm a {PPP} ppp")

    # Suavizo la fuente antes de muestrear: vamos de 30 px por grado a 13,
    # y sin este paso las cordilleras aparecen dentadas.
    src = Image.open(ORIGEN).resize((5400, 2700), Image.LANCZOS)
    g = np.asarray(src, dtype=np.float32)
    sh, sw = g.shape

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
    tc = (col - c0).clip(0, 1)[..., None][..., 0]
    tf = (fil - f0).clip(0, 1)
    muestra = ((g[f0, c0] * (1 - tc) + g[f0, c1] * tc) * (1 - tf)
               + (g[f1, c0] * (1 - tc) + g[f1, c1] * tc) * tf)

    # Estiro el contraste: el relieve crudo vive en una franja estrecha de grises.
    lo, hi = np.percentile(muestra[dentro], [2, 98])
    t = np.clip((muestra - lo) / (hi - lo), 0, 1)[..., None]
    rgb = OSCURO + (CLARO - OSCURO) * t
    # Va en JPEG: el relieve es tono continuo y en el afiche se recorta contra
    # la silueta de la tierra, así que no hace falta transparencia. En PNG
    # pesaba 6 MB; así pesa una fracción y no se nota la diferencia impreso.
    rgb[~dentro] = CLARO
    Image.fromarray(rgb.astype(np.uint8)).save(SALIDA, quality=88, subsampling=0)
    print(f"{SALIDA.name}: {SALIDA.stat().st_size/1e6:.1f} MB · "
          f"gris original entre {lo:.0f} y {hi:.0f}")


if __name__ == "__main__":
    main()
