#!/usr/bin/env python3
"""Pasa los grabados de lámina fotografiada a viñeta para el mapa.

Vienen como foto de la lámina entera: fondo oscuro de la mesa, hoja de montaje,
anotaciones a lápiz y, en algún lugar del medio, el animal. Hay que quedarse
sólo con la figura, sacarle el papel y pasarla a la tinta del afiche.

El recorte no se hace a ojo: se busca la mancha de tinta más grande de la
lámina, que es el animal, y se recorta alrededor de ella.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

AQUI = Path(__file__).parent
CRUDO = AQUI / ".grabados-cache/crudo"
SALIDA = AQUI / "assets/grabados"
TINTA = np.array([0x3A, 0x33, 0x28], float)     # la tinta del afiche
ALTO = 420                                       # alto final de la viñeta, en px

# El recorte automático sirve para encontrar la lámina dentro de la foto, pero
# se queda con el pie impreso y las notas a lápiz. Estos encuadres —en fracción
# de la imagen— aíslan al animal, leídos uno por uno sobre una cuadrícula.
# Tres quedaron afuera: el elefante, que es una escena nocturna entera y no una
# figura separable del fondo; el canguro, cuya lámina está fotografiada en
# diagonal y con otros animales encima; y la vicuña, que es pálida sobre un
# cielo pálido y al quitarle el fondo pierde la cabeza.
ENCUADRES = {
    "Aptenodytes": (0.32, 0.32, 0.64, 0.67),
    "Camelus": (0.06, 0.03, 0.88, 0.87),
    "Diomedea": (0.15, 0.08, 0.89, 0.63),
    "Hirundo": (0.37, 0.23, 0.66, 0.64),
}


def recortar(im: Image.Image) -> Image.Image:
    """Se queda con la mancha de tinta más grande: el animal."""
    g = np.asarray(im.convert("L"), float)
    h, w = g.shape
    m = int(min(h, w) * 0.06)
    nucleo = g[m:h - m, m:w - m]
    papel = np.percentile(nucleo, 80)            # el tono dominante es el papel
    tinta = nucleo < papel - 26

    # Se agrupa a escala gruesa para que las líneas sueltas del grabado cuenten
    # como una sola mancha y no como mil puntos.
    paso = max(1, min(h, w) // 150)
    burdo = tinta[::paso, ::paso]
    burdo = ndimage.binary_closing(burdo, np.ones((5, 5)))
    etiquetas, n = ndimage.label(burdo)
    if n == 0:
        return im
    tam = ndimage.sum(burdo, etiquetas, range(1, n + 1))
    ys, xs = np.where(etiquetas == int(np.argmax(tam)) + 1)
    y0, y1 = ys.min() * paso + m, (ys.max() + 1) * paso + m
    x0, x1 = xs.min() * paso + m, (xs.max() + 1) * paso + m
    aire = int(max(y1 - y0, x1 - x0) * 0.04)
    return im.crop((max(0, x0 - aire), max(0, y0 - aire),
                    min(w, x1 + aire), min(h, y1 + aire)))


def a_tinta(im: Image.Image) -> Image.Image:
    """El papel se vuelve transparente; el trazo, tinta del afiche.

    El tono del papel se mide en el borde de la lámina, no en toda la imagen:
    si se toma el promedio general, el cielo claro de un grabado cuenta como
    tinta y la cabeza pálida del animal cuenta como papel y desaparece.

    Encima va un desvanecido ovalado que disuelve el borde de la lámina en el
    mapa, como las viñetas de los mapas antiguos.
    """
    g = np.asarray(im.convert("L"), float)
    h, w = g.shape
    borde = np.concatenate([g[:max(1, h // 25)].ravel(), g[-max(1, h // 25):].ravel(),
                            g[:, :max(1, w // 25)].ravel(), g[:, -max(1, w // 25):].ravel()])
    papel = np.percentile(borde, 55)
    opacidad = np.clip((papel - g) / max(papel * 0.55, 1), 0, 1) ** 0.9

    yy = (np.arange(h)[:, None] - h / 2) / (h / 2)
    xx = (np.arange(w)[None, :] - w / 2) / (w / 2)
    r = np.sqrt(xx ** 2 + yy ** 2)
    opacidad *= np.clip((1.12 - r) / 0.22, 0, 1)

    rgba = np.zeros(g.shape + (4,), np.uint8)
    rgba[..., :3] = TINTA.astype(np.uint8)
    rgba[..., 3] = (opacidad * 255).astype(np.uint8)
    return Image.fromarray(rgba)


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    el = json.loads((AQUI / ".grabados-cache/elegidos.json").read_text())
    creditos = {}
    for g, d in el.items():
        if g not in ENCUADRES:
            print(f"{g:12} descartado: no da una figura limpia")
            continue
        im = Image.open(CRUDO / f"{g}.jpg")
        a, b, c, e = ENCUADRES[g]
        fig = im.crop((round(a * im.width), round(b * im.height),
                       round(c * im.width), round(e * im.height)))
        fig = fig.resize((round(fig.width * ALTO / fig.height), ALTO), Image.LANCZOS)
        a_tinta(fig).save(SALIDA / f"{g}.png", optimize=True)
        creditos[g] = {"comun": d["comun"], "lamina": d["titulo"],
                       "licencia": d["licencia"], "pagina": d["pagina"]}
        print(f"{g:12} {d['comun']:<20} {im.size} → {fig.size}")
    (SALIDA / "creditos.json").write_text(
        json.dumps(creditos, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
