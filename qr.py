#!/usr/bin/env python3
"""Genera un QR en SVG por lugar, más el de inicio y el del árbol.

Las direcciones salen del mismo nido_lugares.json que usa el sitio, así que
los QR y las páginas no se pueden desincronizar. Van impresos en el afiche A0:
una vez impresos la dirección no se puede cambiar.
"""
import csv
import json
from pathlib import Path

import segno

BASE = "https://negracuarenta.github.io/nido"
AQUI = Path(__file__).parent
SALIDA = AQUI / "qr"

# Slug de la página del árbol. Fijo, como el de cualquier lugar.
SLUG_ORIGEN = "heidelberg"


def url_de(slug: str) -> str:
    return f"{BASE}/lugares/{slug}/"


def escribir(codigo: str, url: str) -> None:
    # Corrección de errores M: aguanta ~15% del código dañado, que es lo
    # razonable para un afiche que se mira de cerca. Negro sobre transparente
    # (light=None) para poder imprimirlo sobre el fondo beige del mapa.
    segno.make(url, error="m").save(
        str(SALIDA / f"{codigo}.svg"),
        kind="svg",
        dark="#000000",
        light=None,
        scale=10,
        border=4,
    )


def main() -> None:
    SALIDA.mkdir(exist_ok=True)
    datos = json.loads((AQUI / "nido_lugares.json").read_text(encoding="utf-8"))

    filas = [
        ("inicio", "Mapa de los vuelos", f"{BASE}/"),
        ("heidelberg", datos["origin"]["name"], url_de(SLUG_ORIGEN)),
    ]
    for viaje in datos["trips"]:
        for lugar in viaje["places"]:
            filas.append((lugar["id"], lugar["name"], url_de(lugar["slug"])))

    for codigo, _, url in filas:
        escribir(codigo, url)

    with (SALIDA / "indice.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["codigo", "nombre", "url"])
        w.writerows(filas)

    print(f"{len(filas)} códigos QR en {SALIDA}/")


if __name__ == "__main__":
    main()
