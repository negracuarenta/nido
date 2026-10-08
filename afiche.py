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
# El canal parte siempre del dibujo a mano, que vive en base/ y no se toca.
# Antes reescribía el entregable encima de sí mismo y dejaba de poder
# re-ejecutarse: cada pasada arrastraba lo que había dejado la anterior.
BASES = {"MAPA_FINAL_es_bn.svg": "base/MAPA_BASE_bn.svg",
         "MAPA_FINAL_es_color.svg": "base/MAPA_BASE_color.svg"}
AFICHES = tuple(BASES)

TINTA = "#2E2416"      # la tinta ferrogálica del afiche

# Los cuatro viajes, en tintas de época. Sobre pergamino los colores del sitio
# —naranja, azul brillante, verde esmeralda— cantan como una pantalla: no hay
# tinta del XVIII que haga esos tonos. Se mantienen las cuatro familias (cálida,
# azul, verde, violeta) para que el afiche y la web se sigan leyendo juntos,
# pero llevadas al rojo de óxido, el azul de Prusia, el verdigrís y el morado
# de campeche. Es un cambio del impreso solamente; la web conserva los suyos.
COLOR = {"E": "#A2411D", "S": "#2A4A78", "O": "#4A6B33", "OV": "#5C3C68"}
ROJO = "#9E2B23"
# La versión a una tinta no puede usar los colores de los viajes: impresa en
# negro los cuatro caerían en el mismo gris. Se separan por valor, y el dibujo
# de la línea —el patrón de guiones— sigue distinguiéndolos.
GRIS = {"E": "#262626", "S": "#4A4A4A", "O": "#6E6E6E", "OV": "#909090"}
GRIS_ROJO = "#555555"


def paleta(nombre: str):
    """Los colores de los viajes y de la cruz, según la versión del afiche."""
    return (GRIS, GRIS_ROJO) if "_bn" in nombre else (COLOR, ROJO)
# El halo que separa cada rótulo de lo que tiene debajo. Era blanco puro y
# sobre el papel ámbar se veía como un parche recortado.
HALO = "#F0E2BE"

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
NAV_X, NAV_Y, NAV_LADO, NAV_PASO = 1010.0, 666.0, 32.0, 46.0

# ---------------------------------------------------------------- referencias
# El cuadro se rehace entero en cada corrida, con las filas calculadas de cero.
# Antes se parcheaba el que venía dibujado y cada pasada lo corría 9 mm hacia
# abajo: las notas habían llegado a 833 mm, al borde del pliego.
# Los cuerpos van un tercio más grandes que los de antes.
LEY_X, LEY_Y, LEY_PASO = 845.0, 650.0, 12.0
LEY_TEXTO = LEY_X + 36.0
LEY_MUESTRA = 30.0                      # largo del trocito de línea
CUERPO_SECT, CUERPO_LEG, CUERPO_NOTA = 6.1, 5.05, 3.45

VIAJES_LEY = (
    ("E", COLOR["E"], "Viaje al este", "Acto 2", 1.5, "0 2.6", "round"),
    ("S", COLOR["S"], "Viaje al sur", "Acto 3", 1.2, "6.6 2.9", "butt"),
    ("O", COLOR["O"], "Viaje al oeste", "Acto 4", 1.2, "9 2.6 0 2.6", "round"),
    ("OV", COLOR["OV"], "Otros vuelos", "fuera de la obra", 1.2, "2.6 5.3", "round"),
)
NOTAS = (
    "Rutas trazadas por arcos de círculo máximo, en el orden en que la "
    "golondrina las cuenta.",
    "Proyección Equal Earth. Relieve, batimetría, hidrografía y nombres "
    "geográficos: Natural Earth.",
)


def referencias(col, rojo) -> str:
    y = LEY_Y
    piezas = [f'<g id="referencias">'
              f'<text x="{LEY_X}" y="{y}" class="sect" '
              f'style="font-size:{CUERPO_SECT}px">Referencias</text>']
    for clave, _, titulo, acto, grosor, trazo, punta in VIAJES_LEY:
        color = col[clave]
        y += LEY_PASO
        piezas.append(
            f'<line x1="{LEY_X}" y1="{y - 1.4}" x2="{LEY_X + LEY_MUESTRA}" '
            f'y2="{y - 1.4}" stroke="{color}" stroke-width="{grosor}" '
            f'stroke-dasharray="{trazo}" stroke-linecap="{punta}"/>'
            f'<text x="{LEY_TEXTO}" y="{y}" class="leg" '
            f'style="font-size:{CUERPO_LEG}px">'
            f'<tspan class="code" style="fill:{color};font-weight:bold">{clave}</tspan>'
            f'  {titulo} <tspan class="small" style="font-size:{CUERPO_NOTA}px">'
            f'· {acto}</tspan></text>')

    cx = LEY_X + 14
    y += LEY_PASO * 1.5
    piezas.append("".join(
        f'<circle cx="{LEY_X + 9 + i * 8}" cy="{y - 1.4}" r="2.15" fill="{c}" '
        f'stroke="{HALO}" stroke-width="0.7"/>'
        for i, c in enumerate((col["E"], col["S"], col["O"])))
        + f'<text x="{LEY_TEXTO}" y="{y}" class="leg" '
          f'style="font-size:{CUERPO_LEG}px">Lugar que vio</text>')

    y += LEY_PASO
    a, b = cx - 1.7, y - 3.1
    cruz = (f'<line x1="{a}" y1="{b}" x2="{a + 3.4}" y2="{b + 3.4}"/>'
            f'<line x1="{a}" y1="{b + 3.4}" x2="{a + 3.4}" y2="{b}"/>')
    piezas.append(
        f'<g stroke="{HALO}" stroke-width="1.8" stroke-linecap="round">{cruz}</g>'
        f'<g stroke="{rojo}" stroke-width="0.9" stroke-linecap="round">{cruz}</g>'
        f'<text x="{LEY_TEXTO}" y="{y}" class="leg" '
        f'style="font-size:{CUERPO_LEG}px">Lo que también vio</text>')

    y += LEY_PASO
    piezas.append(
        f'<circle cx="{cx}" cy="{y - 1.4}" r="4.5" fill="{HALO}" stroke="{TINTA}" '
        f'stroke-width="0.66"/><circle cx="{cx}" cy="{y - 1.4}" r="2" fill="#111"/>'
        f'<text x="{LEY_TEXTO}" y="{y}" class="leg" '
        f'style="font-size:{CUERPO_LEG}px">Heidelberg · el árbol</text>')

    y += LEY_PASO * 1.4
    for nota in NOTAS:
        piezas.append(f'<text x="{LEY_X}" y="{y}" class="small" '
                      f'style="font-size:{CUERPO_NOTA}px">{nota}</text>')
        y += CUERPO_NOTA * 1.7
    piezas.append("</g>")
    return "".join(piezas)

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


def entrada(lugar: dict, clave: str, x: float, y: float, col, rojo) -> str:
    color = col[clave]
    # Los nombres largos se achican para no invadir la columna de al lado.
    # Sólo unos pocos lo necesitan; el resto va al cuerpo normal.
    cuerpo = min(CUERPO_IDX,
                 ancho_columna() / (len(lugar["name"]) * AVANCE_IDX))
    estilo = (f' style="font-size:{cuerpo:.2f}px"'
              if cuerpo < CUERPO_IDX - 0.05 else "")
    cruz = (f'  <tspan style="fill:{rojo}">✕</tspan>'
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


def indice(datos: dict, col, rojo) -> str:
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
            f'<tspan class="code" style="fill:{col[clave]};font-weight:bold">{clave}</tspan>'
            f'  {viaje["name"] if clave == "OV" else "Viaje al " + viaje["name"].lower()}</text>')
        i = 0
        for columna, cupo in zip(cols, cupos):
            for fila in range(cupo):
                piezas.append(entrada(lugares[i], clave, COLUMNAS[columna],
                                      Y0 + fila * PASO, col, rojo))
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


# ------------------------------------------------------------------ cabecera
# El título va en una cartela puesta sobre el Pacífico, a media altura del
# mapa, como la de las láminas del XVIII: doble filete, un florón en cada
# esquina y el texto centrado sobre un paño de papel.
#
# La escala tipográfica es pareja a propósito. Antes NIDO iba a 23 y la última
# línea a 6: casi cuatro veces. Ahora el salto es de una vez y media entre una
# línea y la siguiente, que es como respiran las cartelas antiguas.
PAPEL = "#F2E6C6"              # el paño de la cartela, más claro que el pliego
TINTA_CART = "#2E2416"

CARTELA = (45.0, 316.0, 300.0, 394.0)    # izquierda, arriba, derecha, abajo
CART_AIRE = 2.8

# La rosa de los vientos, en el Pacífico norte: mar abierto, lejos de Hawái y
# de las Aleutianas. Centro en coordenadas finales del pliego y radio exterior.
ROSA = (163.0, 232.0, 36.0)
CABECERA = (
    ("Nido", "title", 17.0, 344.0),
    ("Los vuelos de la golondrina", "subtitle", 11.0, 364.0),
    ("Desde un liquidámbar en Heidelberg, hacia el este, el sur y el oeste",
     "subtitle2", 7.2, 380.0),
)

# El mismo rectángulo, en las coordenadas del mapa sin ampliar, para que los
# rótulos del planisferio sepan que ese sitio está ocupado.
AMPLIACION, DESPLAZO = 1.43418, (-12.157, -34.371)


def _sin_ampliar(x0, y0, x1, y1, margen):
    tx, ty = DESPLAZO
    return ((x0 - margen - tx) / AMPLIACION, (y0 - margen - ty) / AMPLIACION,
            (x1 + margen - tx) / AMPLIACION, (y1 + margen - ty) / AMPLIACION)


def cartela_sin_ampliar(margen: float = 3.0):
    return _sin_ampliar(*CARTELA, margen)


def rosa_sin_ampliar(margen: float = 3.0):
    cx, cy, r = ROSA
    r += 8.0                       # el limbo más las cuatro letras de rumbo
    return _sin_ampliar(cx - r, cy - r, cx + r, cy + r, margen)


def zonas_ocupadas(margen: float = 3.0):
    """Lo que ya está puesto sobre el mapa y los rótulos tienen que esquivar."""
    return [cartela_sin_ampliar(margen), rosa_sin_ampliar(margen)]


def floron(x: float, y: float, sx: int, sy: int) -> str:
    """Un remate de esquina: una curva que se abre y un punto."""
    r = 5.6
    return (f'<path d="M{x + sx * r:.2f},{y} q{-sx * r * 0.55:.2f},0 '
            f'{-sx * r * 0.78:.2f},{sy * r * 0.42:.2f} q{-sx * r * 0.22:.2f},'
            f'{sy * r * 0.2:.2f} {-sx * r * 0.22:.2f},{sy * r * 0.58:.2f}" '
            f'fill="none" stroke="currentColor" stroke-width="0.4"/>'
            f'<circle cx="{x + sx * 2:.2f}" cy="{y + sy * 2:.2f}" r="0.6" '
            f'fill="currentColor"/>')


def voluta(x: float, y: float, sy: int) -> str:
    """El ornamento del medio del filete: dos espirales enfrentadas y un rombo.

    Es lo que remata las cartelas de las láminas del XVIII, arriba y abajo del
    recuadro. Se dibuja chico a propósito: tiene que leerse como un remate, no
    competir con el título que encierra.
    """
    b, h = 13.0, 3.4 * sy
    return (f'<path d="M{x - b:.1f},{y} q{b * 0.42:.1f},0 {b * 0.60:.1f},{h:.1f} '
            f'q{b * 0.12:.1f},{-h * 0.62:.1f} {b * 0.40:.1f},{-h * 0.62:.1f} '
            f'q{b * 0.28:.1f},0 {b * 0.40:.1f},{h * 0.62:.1f} '
            f'q{b * 0.18:.1f},{-h:.1f} {b * 0.60:.1f},{-h:.1f}" '
            f'fill="none" stroke="currentColor" stroke-width="0.38" '
            f'stroke-linecap="round"/>'
            f'<path d="M{x:.1f},{y - 1.5 * sy} l1.5,{1.5 * sy} l-1.5,{1.5 * sy} '
            f'l-1.5,{-1.5 * sy} z" fill="currentColor"/>')


def cabecera() -> str:
    x0, y0, x1, y1 = CARTELA
    a = CART_AIRE
    cxm = (x0 + x1) / 2
    piezas = [f'<g id="cabecera" color="{TINTA_CART}">',
              # La sombra del paño sobre el papel: lo despega del mapa sin
              # recuadro duro, como una hoja apoyada encima.
              f'<rect x="{x0 + 1.4}" y="{y0 + 1.4}" width="{x1 - x0}" '
              f'height="{y1 - y0}" fill="#6B4F2A" fill-opacity="0.16"/>',
              f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
              f'fill="{PAPEL}" fill-opacity="0.93" stroke="currentColor" '
              f'stroke-width="0.7"/>',
              f'<rect x="{x0 + a}" y="{y0 + a}" width="{x1 - x0 - 2 * a}" '
              f'height="{y1 - y0 - 2 * a}" fill="none" stroke="currentColor" '
              f'stroke-width="0.24"/>',
              voluta(cxm, y0 + a, 1), voluta(cxm, y1 - a, -1)]
    for x, sx in ((x0 + a, 1), (x1 - a, -1)):
        for y, sy in ((y0 + a, 1), (y1 - a, -1)):
            piezas.append(floron(x, y, sx, sy))
    for texto, clase, cuerpo, y in CABECERA:
        estilo = f"font-size:{cuerpo}px"
        if clase == "title":
            estilo += f";letter-spacing:{cuerpo * 0.14:.2f}px"
            texto = texto.upper()
        piezas.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{y}" '
                      f'text-anchor="middle" class="{clase}" '
                      f'style="{estilo}">{texto}</text>')
    piezas.append("</g>")
    return "".join(piezas)


def fondo(archivo: str = "pergamino.jpg", liso: str = "#E7D6AE") -> str:
    """El pliego: el pergamino manchado que genera pergamino.py.

    Un color plano no alcanza. Lo que hace que una lámina se lea como antigua
    es la irregularidad del papel, y ésa hay que dibujarla. Debajo del raster
    queda un relleno liso del mismo tono, por si el raster no cargara.
    """
    datos = base64.b64encode(
        (AQUI / "assets/geo" / archivo).read_bytes()).decode()
    return (f'<g id="papel"><rect x="0" y="0" width="1189" height="841" '
            f'fill="{liso}"/>'
            f'<image x="0" y="0" width="1189" height="841" '
            f'preserveAspectRatio="none" '
            f'href="data:image/jpeg;base64,{datos}"/></g>')


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
    nueva_nav, fila_logos, nueva_cab = navegacion(), logos(), cabecera()
    total = sum(len(v["places"]) for v in datos["trips"]) + len(NAVEGACION)

    for nombre in AFICHES:
        ruta = AQUI / nombre
        col, rojo = paleta(nombre)
        nuevo_indice = indice(datos, col, rojo)
        nueva_ley = referencias(col, rojo)
        svg = (AQUI / BASES[nombre]).read_text()
        for ident in ("indice", "navegacion", "logos", "cabecera", "referencias"):
            svg = quitar(svg, ident)
        # La cabecera vieja estaba suelta, sin grupo: se la lleva por su clase.
        svg = re.sub(r'<text[^>]*class="(title|subtitle2?)"[^>]*>.*?</text>',
                     "", svg, flags=re.S)
        # Fuera la regla horizontal que cruzaba bajo el título: la cartela
        # ya encierra el texto y la línea sobraba.
        svg = re.sub(r'<line x1="28" y1="62"[^>]*/>', "", svg, count=1)
        # La tinta pasa de gris a sepia. Los QR no se tocan: son negro puro y
        # cualquier desvío les quita contraste al escanearlos.
        # Los colores de las rutas vienen dibujados en el original con la
        # paleta del sitio. Acá pasan a las tintas de época, y con ellos el
        # rojo de las cruces.
        for vivo, tinta in (("#D9822B", col["E"]), ("#2B6CB0", col["S"]),
                            ("#2F8F5B", col["O"]), ("#6B4E9B", col["OV"]),
                            ("#C62828", rojo)):
            svg = svg.replace(vivo, tinta).replace(vivo.lower(), tinta)
        for gris, sepia in (("#111", TINTA), ("#444", "#5A4B38"),
                            ("#555", "#6B5A44")):
            svg = svg.replace(f'fill:{gris}', f"fill:{sepia}")
            svg = svg.replace(f'stroke="{gris}"', f'stroke="{sepia}"')
            svg = svg.replace(f'fill="{gris}"', f'fill="{sepia}"')
        svg = re.sub(r'<g id="ref-ov">.*?</g>', "", svg, count=1, flags=re.S)
        svg = re.sub(r'<g id="fuentes-mapa">.*?</g>', "", svg, count=1, flags=re.S)
        # La cabecera va la última a propósito: gran_plano.py amplía todo lo
        # que hay entre el planisferio y el cuadro de referencias, y si la
        # cabecera quedaba ahí en medio se escalaba junto con el mapa.
        # El papel va primero de todo, debajo del dibujo.
        svg = quitar(svg, "papel")
        svg = re.sub(r'<rect id="papel"[^>]*/>', "", svg, count=1)
        # El dibujo a mano trae su propio fondo blanco, sin identificar, y
        # tapaba el pergamino: se ve el papel sólo si éste se va.
        svg = re.sub(r'<rect width="1189" height="841" fill="#fff"/>', "",
                     svg, count=1)
        # Los halos de los rótulos eran blanco puro: sobre el papel ámbar se
        # recortaban como un parche. Pasan al crema del pergamino.
        svg = svg.replace("stroke:#fff", f"stroke:{HALO}")
        svg = svg.replace('stroke="#fff"', f'stroke="{HALO}"')
        svg = svg.replace('fill="#fff"', f'fill="{HALO}"')
        papel = (fondo("pergamino_bn.jpg", "#D9D9D9") if "_bn" in nombre
                 else fondo())
        svg = re.sub(r"(<svg[^>]*>)", r"\1" + papel, svg, count=1)
        svg = svg.replace("</svg>", nueva_ley + nuevo_indice + nueva_nav
                          + fila_logos + nueva_cab + "</svg>")

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
