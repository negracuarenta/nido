#!/usr/bin/env python3
"""Genera el pergamino del pliego: el papel manchado sobre el que se imprime todo.

Un color plano no da la sensación de lámina antigua; lo que la da es la
irregularidad. Acá se construye por capas, como se ensucia un papel de verdad:
la fibra (ruido fino), las aguas del batido (ruido grande), las manchas de
humedad (manchones difusos) y el borde oscurecido por el manoseo.

Todo sale de una semilla fija. Si cada corrida inventara manchas nuevas, dos
tiradas del mismo afiche no serían el mismo afiche.

La banda de abajo —el índice, las referencias, los 46 códigos— se deja
deliberadamente más limpia y más clara. Es la zona que hay que *leer*, y un QR
sobre un manchón pierde justamente el contraste del que vive.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

AQUI = Path(__file__).parent
PLIEGO = (1189.0, 841.0)         # mm
PPP = 85                         # suficiente para una mancha difusa en A0
SEMILLA = 20261008

# Los dos extremos del papel: el tono del centro y el de los bordes gastados.
CLARO = np.array([0xE9, 0xD4, 0xA4], float)
OSCURO = np.array([0xA8, 0x7D, 0x45], float)
MANCHA = np.array([0x7C, 0x55, 0x28], float)

# La banda inferior que se mantiene limpia, en milímetros.
LECTURA = (18.0, 628.0, 1171.0, 820.0)


def ruido(rng, alto, ancho, celda):
    """Ruido de valor: una grilla gruesa interpolada suave, no grano de sal."""
    h = max(2, round(alto / celda))
    w = max(2, round(ancho / celda))
    crudo = rng.random((h, w)).astype(np.float32)
    chico = Image.fromarray((crudo * 255).astype(np.uint8))
    return np.asarray(chico.resize((ancho, alto), Image.BICUBIC),
                      dtype=np.float32) / 255.0


def fbm(rng, alto, ancho, celda, octavas=5):
    """Varias capas de ruido, cada una al doble de frecuencia y la mitad de peso."""
    suma = np.zeros((alto, ancho), np.float32)
    peso = 0.0
    for i in range(octavas):
        a = 0.5 ** i
        suma += a * ruido(rng, alto, ancho, celda / 2 ** i)
        peso += a
    return suma / peso


def manchas(rng, alto, ancho, pxmm):
    """Los manchones de humedad: elipses difusas, más y mayores hacia el borde."""
    capa = np.zeros((alto, ancho), np.float32)
    ys, xs = np.mgrid[0:alto, 0:ancho].astype(np.float32)
    for _ in range(34):
        # El centro se sortea con sesgo hacia afuera: elevar a la cuarta una
        # uniforme y mandarla a los extremos amontona las manchas en el borde,
        # que es donde un papel viejo se ensucia.
        u, v = rng.random(2)
        cx = ancho * (0.5 + 0.5 * np.sign(u - 0.5) * abs(2 * u - 1) ** 0.55)
        cy = alto * (0.5 + 0.5 * np.sign(v - 0.5) * abs(2 * v - 1) ** 0.55)
        rx = rng.uniform(22, 95) * pxmm
        ry = rx * rng.uniform(0.45, 1.5)
        giro = rng.uniform(0, np.pi)
        dx, dy = xs - cx, ys - cy
        x = dx * np.cos(giro) + dy * np.sin(giro)
        y = -dx * np.sin(giro) + dy * np.cos(giro)
        d = (x / rx) ** 2 + (y / ry) ** 2
        capa += rng.uniform(0.35, 0.95) * np.exp(-1.6 * d)
    return np.clip(capa, 0, 1.6)


def borde(alto, ancho, pxmm):
    """Cuánto está gastado cada punto por su distancia al borde del pliego."""
    fx = np.minimum(np.arange(ancho), ancho - 1 - np.arange(ancho)) / pxmm
    fy = np.minimum(np.arange(alto), alto - 1 - np.arange(alto)) / pxmm
    d = np.minimum(fx[None, :], fy[:, None])          # mm hasta el borde
    return np.clip(1.0 - d / 95.0, 0, 1) ** 1.5


def limpiar(alto, ancho, pxmm):
    """Máscara suave de la banda de lectura: 1 adentro, 0 afuera."""
    x0, y0, x1, y1 = (v * pxmm for v in LECTURA)
    m = np.zeros((alto, ancho), np.float32)
    m[round(y0):round(y1), round(x0):round(x1)] = 1.0
    img = Image.fromarray((m * 255).astype(np.uint8))
    return np.asarray(img.filter(ImageFilter.GaussianBlur(14 * pxmm)),
                      dtype=np.float32) / 255.0


def main() -> None:
    pxmm = PPP / 25.4
    ancho = round(PLIEGO[0] * pxmm)
    alto = round(PLIEGO[1] * pxmm)
    rng = np.random.default_rng(SEMILLA)
    print(f"pergamino: {ancho}×{alto} px para {PLIEGO[0]:.0f}×{PLIEGO[1]:.0f} mm")

    fibra = fbm(rng, alto, ancho, 3.0 * pxmm, 4)          # el grano del papel
    aguas = fbm(rng, alto, ancho, 110.0 * pxmm, 4)        # las vetas del batido
    humedad = manchas(rng, alto, ancho, pxmm)
    gastado = borde(alto, ancho, pxmm)
    limpio = limpiar(alto, ancho, pxmm)

    # Cuánto se aparta cada punto del tono claro hacia el oscuro.
    sucio = np.clip(0.30 * (aguas - 0.5) * 2 + 0.70 * gastado, 0, 1)
    sucio = np.clip(sucio + 0.10 * (fibra - 0.5) * 2, 0, 1)
    # La banda de lectura no se limpia del todo: sigue siendo el mismo papel,
    # pero sin manchones. Un QR sobre un manchón pierde contraste, y un nombre
    # de lugar a cuerpo 4,4 sobre una veta oscura deja de leerse.
    sucio *= 1.0 - 0.45 * limpio
    humedad = humedad * (1.0 - 0.80 * limpio)

    base = CLARO + (OSCURO - CLARO) * sucio[..., None]
    rgb = base + (MANCHA - base) * np.clip(humedad, 0, 1)[..., None] * 0.42
    # Un último grano, ya sobre el color, para que no se vea plano al ampliar.
    rgb += (fibra[..., None] - 0.5) * 14.0
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    guardar(rgb, "pergamino.jpg")
    # La versión en blanco y negro se imprime a una tinta: el mismo papel,
    # mismas manchas, mismo desgaste, pero sin color. Desaturar el ámbar es
    # más fiel que inventar una textura aparte, porque es literalmente el
    # mismo pliego visto en gris.
    luz = (rgb.astype(np.float32)
           * np.array([0.2126, 0.7152, 0.0722])).sum(axis=2, keepdims=True)
    gris = np.repeat(np.clip(luz * 1.02, 0, 255), 3, axis=2)
    guardar(gris.astype(np.uint8), "pergamino_bn.jpg")


def guardar(rgb, nombre: str) -> None:
    salida = AQUI / "assets/geo" / nombre
    Image.fromarray(rgb).save(salida, quality=84, subsampling=0)
    print(f"{salida.name}: {salida.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
