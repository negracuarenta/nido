#!/usr/bin/env python3
"""Convierte los afiches de SVG a PDF, en tamaño A0 real y con el texto vivo.

Usa Chrome en modo headless, que es el mismo motor con el que vengo
verificando el afiche en pantalla: lo que se ve es lo que se imprime. El SVG va
incrustado en el HTML —no como <img>— para que el texto llegue al PDF como
texto y no como dibujo, y para que resuelva las fuentes reales del sistema:
Palatino y Courier New, que son las que declara el afiche.

El PDF sale en vectores. Para imprenta conviene igual abrirlo en Illustrator y
ajustar ahí lo que pida el taller (sangrado, perfil de color, marcas de corte).
"""
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).parent
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
ANCHO_MM, ALTO_MM = 1189, 841

ENVOLTORIO = """<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: {w}mm {h}mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
svg {{ display: block; width: {w}mm; height: {h}mm; }}
</style></head><body>{svg}</body></html>"""


def convertir(svg_path: Path) -> Path:
    svg = svg_path.read_text()
    # Fuera la declaración XML: adentro de un HTML sobra y molesta.
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    html = AQUI / f".tmp-{svg_path.stem}.html"
    pdf = svg_path.with_suffix(".pdf")
    html.write_text(ENVOLTORIO.format(w=ANCHO_MM, h=ALTO_MM, svg=svg))
    try:
        subprocess.run(
            [str(CHROME), "--headless=new", "--disable-gpu", "--no-sandbox",
             "--run-all-compositor-stages-before-draw",
             "--virtual-time-budget=20000", "--no-pdf-header-footer",
             f"--print-to-pdf={pdf}", html.resolve().as_uri()],
            check=True, capture_output=True, timeout=180)
    finally:
        html.unlink(missing_ok=True)
    return pdf


def medidas(pdf: Path) -> str:
    """El tamaño de página que quedó, leído del propio PDF."""
    crudo = pdf.read_bytes()
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", crudo)
    if not m:
        return "no pude leer el MediaBox"
    x0, y0, x1, y1 = (float(v) for v in m.groups())
    # PDF mide en puntos: 1 pt = 1/72 pulgada = 0,352778 mm
    return f"{(x1-x0)*25.4/72:.1f} × {(y1-y0)*25.4/72:.1f} mm"


def main() -> None:
    if not CHROME.exists():
        raise SystemExit("No encuentro Google Chrome, que es lo que imprime el PDF.")
    archivos = sys.argv[1:] or [
        "MAPA_FINAL_es_color.svg", "MAPA_FINAL_de_color.svg", "MAPA_FINAL_es_bn.svg", "MAPA_FINAL_de_bn.svg"]
    for nombre in archivos:
        pdf = convertir(AQUI / nombre)
        peso = pdf.stat().st_size / 1_000_000
        print(f"{pdf.name}: {medidas(pdf)} · {peso:.1f} MB")


if __name__ == "__main__":
    main()
