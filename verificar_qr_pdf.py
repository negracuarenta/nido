#!/usr/bin/env python3
"""Extrae la banda de QR del PDF que va a imprenta y la deja lista para decodificar.

No mira el SVG ni los qr/*.svg sueltos: rasteriza el PDF, que es el artefacto
real, y escribe qrs.png + qrs.json para que verificar-pdf.html los lea.
"""
import json, re, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ESC = 8                      # píxeles por milímetro en el raster
PT = 72 / 25.4               # puntos por milímetro

def modulos(ident: str, carpeta: Path) -> int:
    """Cuántos módulos de lado tiene ese QR, leídos de su archivo original.

    Contarlos sobre el trazo no sirve: segno dibuja con comandos relativos y la
    mayor coordenada no es la extensión.
    """
    fuente = (carpeta / f"{ident}.svg").read_text()
    ancho = int(re.search(r'width="(\d+)"', fuente).group(1))
    return ancho // int(re.search(r"scale\((\d+)\)", fuente).group(1))


def qrs_del_svg(svg: str, carpeta: Path) -> list:
    fuera = []
    for m in re.finditer(r'<g class="qr" id="qr-([^"]+)" '
                         r'transform="translate\(([-\d.]+) ([-\d.]+)\) '
                         r'scale\(([\d.]+)\)"', svg):
        ident, x, y, k = m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4))
        fuera.append({"id": ident, "x": x, "y": y, "l": k * modulos(ident, carpeta)})
    return fuera

def main(nombre: str) -> None:
    svg = (AQUI / f"{nombre}.svg").read_text()
    carpeta = AQUI / ("qr/de" if "_de_" in nombre else "qr")
    qrs = qrs_del_svg(svg, carpeta)
    if not qrs:
        raise SystemExit("no encontré ningún QR en el SVG")
    x0 = min(q["x"] for q in qrs) - 3
    y0 = min(q["y"] for q in qrs) - 3
    x1 = max(q["x"] + q["l"] for q in qrs) + 3
    y1 = max(q["y"] + q["l"] for q in qrs) + 3
    # el PDF tiene el origen abajo a la izquierda
    alto_mm = 841.0
    subprocess.run(["/tmp/render", str(AQUI / f"{nombre}.pdf"),
                    str(AQUI / "qrs.png"), str(ESC / PT),
                    f"{x0 * PT:.2f}", f"{(alto_mm - y1) * PT:.2f}",
                    f"{(x1 - x0) * PT:.2f}", f"{(y1 - y0) * PT:.2f}"], check=True)
    (AQUI / "qrs.json").write_text(json.dumps(
        {"esc": ESC, "mm": 1, "x0": x0, "y0": y0, "qrs": qrs}))
    print(f"{nombre}: {len(qrs)} QR · banda {x1-x0:.0f} × {y1-y0:.0f} mm")

main(sys.argv[1])
