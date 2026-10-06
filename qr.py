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


# El afiche castellano no fuerza idioma: la misma dirección sirve para los
# tres, y el sitio elige según el navegador o lo que el visitante haya pedido.
# El afiche alemán sí lo fuerza, porque lo lee alguien parado frente a un
# afiche en alemán: ahí no tiene sentido que la ficha abra en castellano.
IDIOMAS = {"": "", "de": "?lang=de"}

# El título del código de portada, en cada idioma.
PORTADA = {"": "Mapa de los vuelos", "de": "Karte der Flüge"}


def nombre_de(lugar: dict, lang: str) -> str:
    return (lugar.get("names") or {}).get(lang) or lugar["name"]


def url_de(slug: str, sufijo: str = "") -> str:
    return f"{BASE}/lugares/{slug}/{sufijo}"


def escribir(codigo: str, url: str, salida: Path) -> None:
    # Corrección de errores M: aguanta ~15% del código dañado, que es lo
    # razonable para un afiche que se mira de cerca. Negro sobre transparente
    # (light=None) para poder imprimirlo sobre el fondo beige del mapa.
    segno.make(url, error="m").save(
        str(salida / f"{codigo}.svg"),
        kind="svg",
        dark="#000000",
        light=None,
        scale=10,
        border=4,
    )


def main() -> None:
    datos = json.loads((AQUI / "nido_lugares.json").read_text(encoding="utf-8"))

    for lang, sufijo in IDIOMAS.items():
        salida = SALIDA / lang if lang else SALIDA
        salida.mkdir(parents=True, exist_ok=True)
        filas = [
            ("inicio", PORTADA[lang], f"{BASE}/{sufijo}"),
            ("heidelberg", datos["origin"]["name"], url_de(SLUG_ORIGEN, sufijo)),
        ]
        for viaje in datos["trips"]:
            for lugar in viaje["places"]:
                filas.append((lugar["id"], nombre_de(lugar, lang),
                              url_de(lugar["slug"], sufijo)))
        for codigo, _, url in filas:
            escribir(codigo, url, salida)
        with (salida / "indice.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["codigo", "nombre", "url"])
            w.writerows(filas)
        print(f"{len(filas)} códigos QR en {salida}/"
              + (f"  (con {sufijo})" if sufijo else "  (sin idioma forzado)"))


if __name__ == "__main__":
    main()
