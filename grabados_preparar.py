#!/usr/bin/env python3
"""Elige, baja y prepara los grabados de animales para el planisferio.

Cada animal está atado a un lugar que la golondrina visitó y que la ficha
nombra: el guacamayo jacinto y el carpincho del Pantanal, el pirarucú del
Amazonas, el tapir de Iguazú, el rinoceronte del Okavango, el flamenco del
delta del Ebro.

El punto fino es cómo se prepara la imagen. Un grabado en talla dulce ya es un
dibujo: el gris lo hacen las rayas. Tratarlo como fotografía —recortarle el
fondo por brillo— dejaba un parche de tono pegado encima del mapa. Acá se
extrae la línea: se compara cada píxel con el fondo local, estimado
desenfocando mucho la lámina. Queda el trazo, y el papel, el cielo y las
manchas desaparecen solos porque forman parte de ese fondo.

Se elige por especie, no por género. La colección usa nombres del siglo XIX y
hay trampas: *Trichechus rosmarus* es la morsa, no el manatí, y *Harpyia
cephalotes* es un murciélago, no la harpía.
"""
import json
import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

AQUI = Path(__file__).parent
CACHE = AQUI / ".grabados-cache"
CRUDO = CACHE / "crudo"
SALIDA = AQUI / "assets/grabados"
TINTA = np.array([0x3A, 0x33, 0x28], float)
ALTO = 460

# clave → (categoría de la colección, especie exacta, nombre común, dónde vive)
ANIMALES = {
    "golondrina": ("Hirundo", r"Hirundo rustica", "golondrina común"),
    "pinguino": ("Aptenodytes", r"Aptenodytes forsteri", "pingüino emperador"),
    "albatros": ("Diomedea", r"Diomedea exulans", "albatros errante"),
    "camello": ("Camelus", r"Camelus bactrianus", "camello bactriano"),
    "guacamayo": ("Anodorhynchus", r"Ara hyacinthina", "guacamayo jacinto"),
    "carpincho": ("Hydrochoerus", r"Hydrochoerus capybara", "carpincho"),
    "tapir": ("Tapirus", r"Tapirus americanus", "tapir"),
    "pirarucu": ("Arapaima", r"Arapaima gigas", "pirarucú"),
    "rinoceronte": ("Rhinoceros", r"Rhinoceros bicornis", "rinoceronte negro"),
    "flamenco": ("Phoenicopterus", r"Phoenicopterus", "flamenco"),
    "vicuna": ("Auchenia", r"Auchenia vicugna", "vicuña"),
    "elefante": ("Elephas", r"Elephas africanus", "elefante africano"),
    "canguro": ("Halmaturus", r"Macropus|Halmaturus", "canguro"),
}

# Láminas de anatomía, que la colección trae a montones.
PARTES = re.compile(r"skelet|ingewand|gebit|tong|hoeven|schedel|anatom|embryo|"
                    r"\bei\b|schaal|poot|kop\b", re.I)

# Encuadres a mano, en fracción de la lámina, para los que el recorte
# automático no acierta. Los demás se encuadran solos.
ENCUADRES = {
    # La lámina del rinoceronte trae media columna de texto impreso encima.
    "rinoceronte": (0.0, 0.28, 1.0, 1.0),
}

# Cuando la lámina mejor resuelta resulta ser un cráneo o una anatomía —y el
# título no lo dice— se toma otra de la misma especie. El número es la posición
# en la lista ordenada por tamaño.
ALTERNATIVA = {
    "rinoceronte": 2,   # las dos primeras son cráneos, y el título no lo dice
    "tapir": 1,         # idem
    "canguro": 3,       # las primeras están fotografiadas en diagonal
    "elefante": 4,      # las primeras son escenas nocturnas, sin línea
}


def elegir() -> dict:
    elegidos = {}
    for clave, (cat, especie, comun) in ANIMALES.items():
        f = CACHE / f"{cat}.json"
        if not f.exists():
            print(f"  (sin datos de {cat})"); continue
        pags = json.loads(f.read_text()).get("query", {}).get("pages", [])
        cand = []
        for p in pags:
            t = p["title"].replace("File:", "")
            ii = (p.get("imageinfo") or [{}])[0]
            if PARTES.search(t) or not re.search(especie, t, re.I):
                continue
            cand.append(((ii.get("width", 0) or 0) * (ii.get("height", 0) or 0), t, ii))
        if not cand:
            print(f"  ({clave}: ninguna lámina de {especie})"); continue
        cand.sort(key=lambda c: -c[0])
        _, t, ii = cand[min(ALTERNATIVA.get(clave, 0), len(cand) - 1)]
        elegidos[clave] = {
            "comun": comun, "titulo": t, "licencia": "Dominio público",
            "url": (ii.get("thumburl") or ii["url"]).replace(
                "//thumb.wikimedia", "//upload.wikimedia"),
            "pagina": ii.get("descriptionurl")}
    return elegidos


def bajar(elegidos: dict) -> None:
    CRUDO.mkdir(parents=True, exist_ok=True)
    for clave, d in elegidos.items():
        destino = CRUDO / f"{clave}.jpg"
        if destino.exists():
            continue
        subprocess.run(["curl", "-sL", "--max-time", "120", "-A", "NIDO-mapa/1.0",
                        "-o", str(destino), d["url"]], check=True)


def linea(im: Image.Image) -> np.ndarray:
    """La línea del grabado, separada del fondo local."""
    g = np.asarray(im.convert("L"), float)
    radio = max(6, min(g.shape) // 14)
    fondo = np.asarray(Image.fromarray(g.astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(radio)), float)
    realce = np.clip(fondo - g, 0, None)
    fuerte = float(np.percentile(realce, 99.4)) or 1.0
    return np.clip((realce - fuerte * 0.10) / (fuerte * 0.62), 0, 1)


def recortar(tinta: np.ndarray):
    """Encuadra la mancha de trazo más grande que no toque el borde.

    Lo que toca el borde es el marco de la lámina o el canto de la hoja de
    montaje, y si se los deja ganan siempre por tamaño y el encuadre termina
    abarcando la página entera con su pie impreso.
    """
    h, w = tinta.shape
    paso = max(1, min(h, w) // 170)
    burdo = ndimage.binary_closing(tinta[::paso, ::paso] > 0.30, np.ones((7, 7)))
    etiquetas, n = ndimage.label(burdo)
    if n == 0:
        return 0, 0, w, h
    borde = set(etiquetas[0]) | set(etiquetas[-1]) | set(etiquetas[:, 0]) | set(etiquetas[:, -1])
    tam = ndimage.sum(burdo, etiquetas, range(1, n + 1))
    for i in borde:
        if i:
            tam[i - 1] = 0
    if not tam.any():                      # todo tocaba el borde
        tam = ndimage.sum(burdo, etiquetas, range(1, n + 1))
    ys, xs = np.where(etiquetas == int(np.argmax(tam)) + 1)
    y0, y1 = ys.min() * paso, (ys.max() + 1) * paso
    x0, x1 = xs.min() * paso, (xs.max() + 1) * paso
    aire = int(max(y1 - y0, x1 - x0) * 0.05)
    return (max(0, x0 - aire), max(0, y0 - aire),
            min(w, x1 + aire), min(h, y1 + aire))


def sin_marco(tinta: np.ndarray) -> np.ndarray:
    """Quita las líneas de marco que rodean muchas láminas.

    Una línea de marco se reconoce sola: es una fila o columna entintada casi
    de punta a punta, pegada al borde. Un animal nunca lo está.
    """
    for _ in range(2):
        h, w = tinta.shape
        if h < 20 or w < 20:
            break
        recorte = [0, 0, w, h]
        for eje, largo in ((0, h), (1, w)):
            cobertura = (tinta > 0.35).mean(axis=1 - eje)
            limite = max(2, int(largo * 0.07))
            ini, fin = 0, largo
            for i in range(limite):
                if cobertura[i] > 0.6:
                    ini = i + 1
            for i in range(largo - 1, largo - limite - 1, -1):
                if cobertura[i] > 0.6:
                    fin = i
            if eje == 0:
                recorte[1], recorte[3] = ini, fin
            else:
                recorte[0], recorte[2] = ini, fin
        x0, y0, x1, y1 = recorte
        if (x0, y0, x1, y1) == (0, 0, w, h):
            break
        tinta = tinta[y0:y1, x0:x1]
    return tinta


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    for viejo in SALIDA.glob("*.png"):
        viejo.unlink()
    elegidos = elegir()
    bajar(elegidos)
    creditos = {}
    for clave, d in elegidos.items():
        im = Image.open(CRUDO / f"{clave}.jpg")
        if clave in ENCUADRES:
            a, b, c, e = ENCUADRES[clave]
            im = im.crop((round(a * im.width), round(b * im.height),
                          round(c * im.width), round(e * im.height)))
        tinta = linea(im)
        x0, y0, x1, y1 = recortar(tinta)
        tinta = sin_marco(tinta[y0:y1, x0:x1])
        rgba = np.zeros(tinta.shape + (4,), np.uint8)
        rgba[..., :3] = TINTA.astype(np.uint8)
        rgba[..., 3] = (tinta * 255).astype(np.uint8)
        fig = Image.fromarray(rgba)
        fig = fig.resize((max(1, round(fig.width * ALTO / fig.height)), ALTO),
                         Image.LANCZOS)
        fig.save(SALIDA / f"{clave}.png", optimize=True)
        creditos[clave] = {"comun": d["comun"], "lamina": d["titulo"],
                           "licencia": d["licencia"], "pagina": d["pagina"]}
        print(f"{clave:14} {d['comun']:<22} {fig.size}")
    (SALIDA / "creditos.json").write_text(
        json.dumps(creditos, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
