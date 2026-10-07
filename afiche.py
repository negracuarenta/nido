#!/usr/bin/env python3
"""Arma el índice de QR del afiche A0 a partir de los mismos datos que el sitio.

El afiche se dibujó a mano —el planisferio, el detalle de Sudamérica, las
referencias— y eso no se toca. Lo que sí se genera acá es el índice: los 44
lugares con su código QR incrustado, más los dos códigos de navegación.

Hasta ahora el índice tenía recuadros punteados vacíos y se había quedado en 35
lugares. Generarlo desde nido_lugares.json es lo que evita que vuelva a
desincronizarse: una vez impreso, un QR equivocado no se arregla.
"""
import base64
import json
import re
from pathlib import Path

AQUI = Path(__file__).parent
AFICHES = ("MAPA_FINAL_es_bn.svg", "MAPA_FINAL_es_color.svg")

COLOR = {"E": "#D9822B", "S": "#2B6CB0", "O": "#2F8F5B", "OV": "#6B4E9B"}
ROJO = "#C62828"

# La grilla del índice, en milímetros. El lienzo es de 1189 × 841.
# Desde que el planisferio ocupa todo el ancho, al índice le queda una banda
# más baja y más larga: diez columnas de cinco filas en vez de seis de nueve.
COLUMNAS = tuple(28.0 + 80.0 * i for i in range(10))
Y0, PASO, FILAS = 652.0, 33.5, 5
LADO = 24.0          # lado del QR; con 45 módulos da 0,53 mm por módulo
SANGRIA = 28.0       # del borde del QR al texto
CUERPO_IDX = 4.4     # el cuerpo de los nombres, como lo define la hoja de estilo
AVANCE_IDX = 0.52    # ancho de un carácter en fracción del cuerpo, medido

# Cada viaje ocupa las columnas que necesita. El Este y el Sur son los más
# largos y se reparten en dos; el Oeste y Otros vuelos entran en una.
REPARTO = {"E": (0, 1), "S": (2, 3, 4, 5), "O": (6, 7), "OV": (8, 9)}

# Los dos códigos que no son un lugar: la portada del mapa y el árbol.
NAVEGACION = (
    ("inicio", "El mapa completo", "Escaneá para abrir el mapa interactivo"),
    ("heidelberg", "Punto 0 · el árbol", "El liquidámbar de Heidelberg"),
)
NAV_X, NAV_Y, NAV_LADO, NAV_PASO = 964.0, 652.0, 32.0, 52.0

# Los logos de las instituciones, abajo a la derecha, como en la web.
# Son grises puros, así que el mismo archivo sirve para las dos versiones.
#
# No van todos a la misma altura: igualar la altura es justo lo que hacía que
# negra40 pesara de más. Es un logotipo ancho —4,7:1— y los otros dos son
# sellos casi cuadrados, así que a igual altura ocupa el triple de superficie.
# El factor de cada uno iguala la raíz del área que cubre, que es la medida que
# más se parece a cómo el ojo compara dos marcas de formas distintas.
#
# El alto de referencia son 20 mm. Con archivos de 120 px eso da 152 ppp, que a
# la distancia a la que se mira un A0 —un metro— está en el límite de lo que el
# ojo resuelve. Más grandes habría que pedirles los vectores a las
# instituciones: vectorizar los PNG no sirve, lo probé y pierde el dibujo.
LOGOS = (("vpst.png", 1.00), ("ceac.png", 0.75), ("negra40.png", 0.58))
LOGO_ALTO, LOGO_AIRE = 20.0, 14.0
LOGO_DERECHA, LOGO_ABAJO = 1161.0, 792.0


def qr_incrustado(codigo: str, x: float, y: float, lado: float) -> str:
    """El QR como trazo vectorial, escalado a su recuadro.

    segno lo dibuja en unidades de módulo con una zona de silencio de cuatro
    módulos ya incluida, así que alcanza con escalar el lado entero.
    """
    fuente = (AQUI / "qr" / f"{codigo}.svg").read_text()
    ancho = int(re.search(r'width="(\d+)"', fuente).group(1))
    escala_interna = int(re.search(r"scale\((\d+)\)", fuente).group(1))
    modulos = ancho // escala_interna
    d = re.search(r'\sd="([^"]+)"', fuente).group(1)
    k = lado / modulos
    return (
        f'<g class="qr" id="qr-{codigo}" transform="translate({x} {y}) scale({k:.6f})">'
        f'<path d="{d}" stroke="#000" stroke-width="1" fill="none"/></g>'
    )


def ancho_columna() -> float:
    return (COLUMNAS[1] - COLUMNAS[0]) - SANGRIA - 3.0


def entrada(lugar: dict, clave: str, x: float, y: float) -> str:
    color = COLOR[clave]
    # Los nombres largos se achican para no invadir la columna de al lado.
    # Sólo unos pocos lo necesitan; el resto va al cuerpo normal.
    cuerpo = min(CUERPO_IDX,
                 ancho_columna() / (len(lugar["name"]) * AVANCE_IDX))
    estilo = (f' style="font-size:{cuerpo:.2f}px"'
              if cuerpo < CUERPO_IDX - 0.05 else "")
    cruz = (f'  <tspan style="fill:{ROJO}">✕</tspan>'
            if lugar.get("tragico") or lugar.get("soloTragico") else "")
    tx = x + SANGRIA
    return (
        qr_incrustado(lugar["id"], x, y, LADO)
        + f'<text x="{tx}" y="{y + 9}" class="code" '
          f'style="font-size:3.4px;fill:{color}">{lugar["id"]}{cruz}</text>'
        + f'<text x="{tx}" y="{y + 15.5}" class="idx"{estilo}>{lugar["name"]}</text>'
    )


def reparte(cuantos: int, columnas: int) -> list:
    """Cuántas entradas van en cada columna, lo más parejo posible."""
    if columnas == 1:
        return [cuantos]
    base, resto = divmod(cuantos, columnas)
    return [base + (1 if i < resto else 0) for i in range(columnas)]


def indice(datos: dict) -> str:
    piezas = ['<g id="indice">',
              '<text x="28" y="636" class="sect">'
              'Índice · escaneá el código para saber más de cada lugar</text>']
    for viaje in datos["trips"]:
        clave = viaje["key"]
        cols = REPARTO[clave]
        lugares = viaje["places"]
        cupos = reparte(len(lugares), len(cols))
        if max(cupos) > FILAS:
            raise SystemExit(
                f"El viaje {clave} tiene {len(lugares)} lugares y no entra en "
                f"{len(cols)} columna(s) de {FILAS} filas. Hay que rehacer el reparto.")
        piezas.append(
            f'<text x="{COLUMNAS[cols[0]]}" y="647" class="leg" style="font-size:4.6px">'
            f'<tspan class="code" style="fill:{COLOR[clave]};font-weight:bold">{clave}</tspan>'
            f'  {viaje["name"] if clave == "OV" else "Viaje al " + viaje["name"].lower()}</text>')
        i = 0
        for col, cupo in zip(cols, cupos):
            for fila in range(cupo):
                piezas.append(entrada(lugares[i], clave,
                                      COLUMNAS[col], Y0 + fila * PASO))
                i += 1
    piezas.append("</g>")
    return "".join(piezas)


def navegacion() -> str:
    piezas = ['<g id="navegacion">',
              f'<text x="{NAV_X}" y="{NAV_Y - 16}" class="sect">Para empezar</text>']
    for n, (codigo, titulo, pie) in enumerate(NAVEGACION):
        y = NAV_Y + n * NAV_PASO
        tx = NAV_X + NAV_LADO + 6
        piezas += [
            qr_incrustado(codigo, NAV_X, y, NAV_LADO),
            f'<text x="{tx}" y="{y + 13}" class="idx">{titulo}</text>',
            f'<text x="{tx}" y="{y + 19}" class="small">{pie}</text>',
        ]
    piezas.append("</g>")
    return "".join(piezas)


def fin_de_grupo(svg: str, desde: int) -> int:
    """El índice del </g> que cierra ese grupo, contando los anidados.

    Buscar el primer </g> no sirve: desde que los QR van incrustados, el índice
    tiene grupos adentro, y cortar ahí deja medio índice en pie.
    """
    nivel = 0
    for m in re.finditer(r"<g\b|</g>", svg[desde:]):
        nivel += 1 if m.group(0) != "</g>" else -1
        if nivel == 0:
            return desde + m.end()
    raise ValueError("no encontré el cierre del grupo")


def quitar(svg: str, ident: str) -> str:
    marca = f'<g id="{ident}">'
    while marca in svg:
        i = svg.index(marca)
        svg = svg[:i] + svg[fin_de_grupo(svg, i):]
    return svg


def logos() -> str:
    """La fila de logos, alineada al margen derecho y centrada en una misma línea."""
    import struct

    piezas = []
    for archivo, factor in LOGOS:
        png = (AQUI / "assets/logos" / archivo).read_bytes()
        w, h = struct.unpack(">II", png[16:24])
        alto = LOGO_ALTO * factor
        piezas.append((base64.b64encode(png).decode(), alto * w / h, alto))

    ancho_total = sum(p[1] for p in piezas) + LOGO_AIRE * (len(piezas) - 1)
    x = LOGO_DERECHA - ancho_total
    medio = LOGO_ABAJO - LOGO_ALTO / 2

    salida = [f'<g id="logos">'
              f'<text x="{x:.2f}" y="{medio - LOGO_ALTO / 2 - 5.2:.2f}" class="small" '
              f'style="font-size:3px">Con</text>']
    for datos, ancho, alto in piezas:
        salida.append(f'<image x="{x:.2f}" y="{medio - alto / 2:.2f}" '
                      f'width="{ancho:.2f}" height="{alto:.2f}" '
                      f'preserveAspectRatio="xMidYMid meet" '
                      f'href="data:image/png;base64,{datos}"/>')
        x += ancho + LOGO_AIRE
    salida.append("</g>")
    return "".join(salida)


def main() -> None:
    datos = json.loads((AQUI / "nido_lugares.json").read_text())
    nuevo_indice, nueva_nav, fila_logos = indice(datos), navegacion(), logos()
    total = sum(len(v["places"]) for v in datos["trips"]) + len(NAVEGACION)

    for nombre in AFICHES:
        ruta = AQUI / nombre
        svg = ruta.read_text()
        for ident in ("indice", "navegacion", "logos"):
            svg = quitar(svg, ident)
        svg = svg.replace("</svg>", nuevo_indice + nueva_nav + fila_logos + "</svg>")

        puestos = len(re.findall(r'<g class="qr" id="qr-', svg))
        vacios = len(re.findall(r'<rect class="qr"', svg))
        if puestos != total or vacios:
            raise SystemExit(
                f"{nombre}: {puestos} códigos puestos de {total} y {vacios} "
                f"recuadros vacíos. No lo escribo así.")
        ruta.write_text(svg)
        print(f"{nombre}: {puestos} QR incrustados, {vacios} recuadros vacíos, "
              f"{len(re.findall(r'<image ', fila_logos))} logos")


if __name__ == "__main__":
    main()
