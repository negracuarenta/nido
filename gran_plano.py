#!/usr/bin/env python3
"""Lleva el planisferio a todo el ancho del pliego y saca el detalle de Sudamérica.

El planisferio está dibujado a una escala fija, pero la proyección se conoce
—Equal Earth, con el ecuador midiendo 2 × 395 mm y el centro en (423, 272)— y
eso vuelve la ampliación una semejanza: multiplicar por un factor es
exactamente lo mismo que volver a proyectar a mayor escala. No hay que
redibujar nada, ni volver a deducir nada.

Por eso va al final del canal: todo lo que se genera antes —el relieve, los
mares, los accidentes, los rótulos— sigue calculando en las coordenadas
originales, y acá escala junto con el dibujo.

Con el detalle fuera, el mapa pasa de 790 × 384,5 mm a 1133 × 551,5: más del
doble de superficie.
"""
import math
import re

from afiche import HALO, ROSA
from pathlib import Path

AQUI = Path(__file__).parent
AFICHES = ("MAPA_FINAL_es_bn.svg", "MAPA_FINAL_es_color.svg",
           "MAPA_FINAL_de_bn.svg", "MAPA_FINAL_de_color.svg")

X0, Y0, SEMIANCHO = 423.0, 272.0, 395.0      # el planisferio como está dibujado
IZQUIERDA, DERECHA, ARRIBA = 28.0, 1161.0, 80.0

# La primera capa del mapa y la primera que ya no lo es: todo lo que queda en
# medio se amplía junto.
DESDE, HASTA = 'id="mapa-mundi"', 'id="referencias"'


def parametros():
    s = (DERECHA - IZQUIERDA) / 2 / SEMIANCHO
    alto = 2 * s * 192.2534                   # medio alto dibujado × 2
    cx = (IZQUIERDA + DERECHA) / 2
    cy = ARRIBA + alto / 2
    return s, cx - s * X0, cy - s * Y0, alto


def fin_de_grupo(svg: str, desde: int) -> int:
    nivel = 0
    for m in re.finditer(r"<g\b|</g>", svg[desde:]):
        nivel += 1 if m.group(0) != "</g>" else -1
        if nivel == 0:
            return desde + m.end()
    raise ValueError("no encontré el cierre del grupo")


A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
TINTA = "#2E2416"
MARCO_FUERA = 11.0           # del borde del pliego al filete exterior
MARCO_BANDA = 4.5            # ancho de la banda graduada
PLIEGO = (1189.0, 841.0)
PARALELOS = (60, 30, 0, -30, -60)
MERIDIANOS = (-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150)
# El paso de los dientes de la banda graduada, en grados.
PASO_DIENTE = 5


def equal_earth(lon_g, lat_g):
    th = math.asin(math.sqrt(3) / 2 * math.sin(math.radians(lat_g)))
    t2, t6 = th * th, th ** 6
    x = (2 * math.sqrt(3) * math.radians(lon_g) * math.cos(th)
         / (3 * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2))))
    return x, th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))


def dientes(a: float, b: float, posiciones, vertical: bool,
            x: float, ancho: float) -> str:
    """Los bloques alternados de la banda graduada, entre dos posiciones.

    Van macizos y huecos uno sí y uno no, como la regla de una lámina de
    marear. Cada diente ocupa exactamente un paso de la retícula, así que la
    banda no es un adorno: se puede medir con ella.
    """
    piezas = []
    for i, (p0, p1) in enumerate(zip(posiciones, posiciones[1:])):
        if i % 2:
            continue
        lo, hi = sorted((p0, p1))
        lo, hi = max(lo, a), min(hi, b)
        if hi - lo < 0.2:
            continue
        if vertical:
            piezas.append(f'<rect x="{x:.2f}" y="{lo:.2f}" width="{ancho:.2f}" '
                          f'height="{hi - lo:.2f}"/>')
        else:
            piezas.append(f'<rect x="{lo:.2f}" y="{x:.2f}" '
                          f'width="{hi - lo:.2f}" height="{ancho:.2f}"/>')
    return "".join(piezas)


def marco_y_grados() -> str:
    """El neto graduado del pliego y los grados en el borde, no sobre el mapa.

    En Equal Earth los meridianos no llegan al marco —el mapa termina en una
    elipse— pero la posición de cada uno *sobre el ecuador* sí gradúa el ancho
    del pliego, y la de cada paralelo gradúa su altura, porque en esta
    proyección la latitud tiene una sola ordenada en todo el mapa. Así que la
    banda es honesta: cada diente es un paso real de la retícula.

    Donde no hay mapa —por encima del polo norte y por debajo del sur— la banda
    lateral queda lisa. Dibujar dientes ahí sería inventar una graduación.
    """
    s, tx, ty, alto = parametros()
    k = s * 145.9379
    cx = (IZQUIERDA + DERECHA) / 2
    cy = ARRIBA + alto / 2
    W, H = PLIEGO
    f, b = MARCO_FUERA, MARCO_BANDA

    piezas = [f'<g id="marco" color="{TINTA}">',
              # filete exterior, banda, filete interior
              f'<rect x="{f}" y="{f}" width="{W - 2 * f}" height="{H - 2 * f}" '
              f'fill="none" stroke="currentColor" stroke-width="0.75"/>',
              f'<rect x="{f + b}" y="{f + b}" width="{W - 2 * (f + b)}" '
              f'height="{H - 2 * (f + b)}" fill="none" stroke="currentColor" '
              f'stroke-width="0.4"/>']

    # Los dientes. Arriba y abajo gradúan la longitud; a los lados, la latitud.
    lon_x = [cx + k * equal_earth(g, 0.0)[0]
             for g in range(-180, 181, PASO_DIENTE)]
    lat_y = [cy - k * equal_earth(0.0, g)[1]
             for g in range(90, -91, -PASO_DIENTE)]
    piezas.append(f'<g fill="currentColor">'
                  + dientes(f, W - f, lon_x, False, f, b)
                  + dientes(f, W - f, lon_x, False, H - f - b, b)
                  + dientes(f, H - f, lat_y, True, f, b)
                  + dientes(f, H - f, lat_y, True, W - f - b, b)
                  + '</g>')
    # Las cuatro esquinas, macizas, que es lo que cierra la regla.
    piezas.append("".join(
        f'<rect x="{x}" y="{y}" width="{b}" height="{b}" fill="currentColor"/>'
        for x in (f, W - f - b) for y in (f, H - f - b)))

    # Los grados van del lado de adentro de la banda: ya no cruzan el dibujo,
    # pero tampoco quedan al filo del pliego, donde el guillotinado se los come.
    dentro = f + b
    for lon in MERIDIANOS:
        x = cx + k * equal_earth(lon, 0.0)[0]
        letra = "" if lon == 0 else (" E" if lon > 0 else " O")
        for y in (dentro + 4.4, H - dentro - 1.9):
            piezas.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" '
                          f'class="grado">{abs(lon)}°{letra}</text>')
    for lat in PARALELOS:
        if lat == 0:
            continue
        y = cy - k * equal_earth(0.0, lat)[1]
        letra = "N" if lat > 0 else "S"
        for x, ancla in ((dentro + 2.0, "start"), (W - dentro - 2.0, "end")):
            piezas.append(f'<text x="{x:.1f}" y="{y + 1.2:.1f}" '
                          f'text-anchor="{ancla}" class="grado">'
                          f'{abs(lat)}° {letra}</text>')
    for x, ancla in ((dentro + 2.0, "start"), (W - dentro - 2.0, "end")):
        piezas.append(f'<text x="{x:.1f}" y="{cy + 1.2:.1f}" '
                      f'text-anchor="{ancla}" class="grado">0°</text>')

    piezas.append(rosa_de_los_vientos())
    piezas.append("</g>")
    return "".join(piezas)


def rosa_de_los_vientos() -> str:
    """Una rosa de treinta y dos rumbos sobre el Pacífico norte.

    Los cuatro rumbos cardinales van macizos y alternados en claro y oscuro,
    como las de las cartas portulanas: el contraste entre las dos mitades de
    cada punta es lo que les da el relieve sin sombra.
    """
    import math as _m
    cx, cy, R = ROSA
    piezas = [f'<g id="rosa" color="{TINTA}" '
              f'transform="translate({cx} {cy})">']
    # Los anillos.
    for r, w in ((R, 0.55), (R - 1.6, 0.3), (R * 0.60, 0.3), (R * 0.26, 0.3)):
        piezas.append(f'<circle cx="0" cy="0" r="{r:.2f}" fill="none" '
                      f'stroke="currentColor" stroke-width="{w}"/>')
    # Las marcas del limbo, cada 7,5° —treinta y dos rumbos.
    for i in range(32):
        a = _m.radians(i * 11.25)
        largo = 2.6 if i % 4 == 0 else 1.4
        x0, y0 = (R - 1.6) * _m.sin(a), -(R - 1.6) * _m.cos(a)
        x1, y1 = (R - 1.6 - largo) * _m.sin(a), -(R - 1.6 - largo) * _m.cos(a)
        piezas.append(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" '
                      f'y2="{y1:.2f}" stroke="currentColor" '
                      f'stroke-width="{0.45 if i % 4 == 0 else 0.25}"/>')

    def punta(a_grados, largo, ancho):
        a = _m.radians(a_grados)
        px, py = largo * _m.sin(a), -largo * _m.cos(a)
        qx, qy = ancho * _m.cos(a), ancho * _m.sin(a)
        claro = f'M0,0 L{qx:.2f},{qy:.2f} L{px:.2f},{py:.2f} Z'
        oscuro = f'M0,0 L{-qx:.2f},{-qy:.2f} L{px:.2f},{py:.2f} Z'
        return (f'<path d="{claro}" fill="#F2E6C6" stroke="currentColor" '
                f'stroke-width="0.3"/>'
                f'<path d="{oscuro}" fill="currentColor" stroke="currentColor" '
                f'stroke-width="0.3"/>')

    for i in range(8):                       # los rumbos intermedios, cortos
        if i % 2:
            piezas.append(punta(i * 45 + 22.5, R * 0.52, R * 0.055))
    for i in range(8):
        piezas.append(punta(i * 45, R * 0.60 if i % 2 else R * 0.93, R * 0.075))
    piezas.append('<circle cx="0" cy="0" r="1.5" fill="currentColor"/>')
    # La flor de lis del norte, reducida a lo que se lee a un metro.
    piezas.append(f'<path d="M0,{-R * 1.00:.2f} l2.1,3.0 l-2.1,-0.9 l-2.1,0.9 z" '
                  f'fill="currentColor"/>')
    # Las letras van fuera del limbo. Adentro las tapaba la propia punta, que
    # es el problema que tienen todas las rosas dibujadas de memoria.
    for letra, a in (("N", 0), ("E", 90), ("S", 180), ("O", 270)):
        r = R + 4.6
        x, y = r * _m.sin(_m.radians(a)), -r * _m.cos(_m.radians(a))
        piezas.append(f'<text x="{x:.2f}" y="{y + 1.6:.2f}" text-anchor="middle" '
                      f'class="rumbo">{letra}</text>')
    piezas.append("</g>")
    return "".join(piezas)


def velo() -> str:
    """Un velo cálido sobre el mapa, para la pátina de lámina antigua.

    Va en las coordenadas del dibujo sin ampliar, porque se inserta dentro del
    grupo que luego se escala: el recorte contra el marco del mapa sólo calza
    si los dos están en el mismo sistema.
    """
    return ('<g id="velo" clip-path="url(#solo-mapa)">'
            '<rect x="28" y="79.747" width="790" height="384.506" '
            'fill="#C9A869" opacity="0.07"/></g>')


ESTILO_GRADO = (".grado{font-family:'TeX Gyre Pagella','Palatino',serif;"
                "font-style:italic;font-size:3.4px;fill:%s;opacity:0.85}"
                ".rumbo{font-family:'TeX Gyre Pagella','Palatino',serif;"
                "font-size:4.2px;letter-spacing:0.3px;fill:%s}" % (TINTA, TINTA))


def despejar_el_arbol(svg: str) -> str:
    """Pone el rótulo de Heidelberg por encima de todo lo demás del mapa.

    El recorrido de «Otros vuelos» se dibuja después del planisferio, así que
    pasaba por encima del nombre y lo cruzaba. Acá se saca el marcador con sus
    dos líneas de texto y se los vuelve a poner al final del grupo, ya sin nada
    encima, con el halo blanco más grueso para que corte limpio.
    """
    m = re.search(
        r'<circle cx="[\d.]+" cy="[\d.]+" r="3\.4"[^>]*/>'
        r'<circle[^>]*r="1\.5"[^>]*/>'
        r'<text[^>]*class="lab origin"[^>]*>.*?</text>'
        r'<text[^>]*class="small"[^>]*>.*?</text>', svg, re.S)
    if not m:
        return svg
    bloque = m.group(0).replace('class="lab origin"',
                                'class="lab origin" style="stroke-width:1.9px"')
    bloque = bloque.replace('class="small"',
                            f'class="small" style="paint-order:stroke;stroke:{HALO};'
                            'stroke-width:1.5px;stroke-linejoin:round"', 1)
    svg = svg[:m.start()] + svg[m.end():]
    # Va al final del rango que se amplía, justo antes del cuadro de
    # referencias: ahí no le queda nada encima.
    cierre = svg.rindex("<g", 0, svg.index(HASTA))
    # El velo entra acá, dentro del rango que se amplía, para que su recorte
    # contra el marco del mapa siga valiendo.
    return svg[:cierre] + velo() + f'<g id="arbol">{bloque}</g>' + svg[cierre:]


def a_una_tinta(svg: str) -> str:
    """Lleva todos los colores del dibujo a su gris, en la versión a una tinta.

    Ir módulo por módulo cambiando cada sepia y cada crema por su equivalente
    gris es la forma segura de olvidarse de uno. Esto pasa una sola vez al
    final, sobre el archivo ya armado, y por construcción no puede dejar nada
    coloreado. Los rásteres no entran acá —no son colores sino imágenes— y van
    por su propio filtro en expresividad.py.

    Los colores de los viajes ya vienen elegidos en gris desde afiche.py: sus
    valores están separados a propósito, y pasarlos por luminancia los habría
    juntado. Al ser ya grises, esto los deja intactos.
    """
    def gris(m):
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        v = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
        return f"#{v:02x}{v:02x}{v:02x}"

    return re.sub(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", gris, svg)


def main() -> None:
    s, tx, ty, alto = parametros()
    print(f"ampliación ×{s:.5f} · el mapa pasa a "
          f"{DERECHA - IZQUIERDA:.0f} × {alto:.1f} mm")

    for nombre in AFICHES:
        ruta = AQUI / nombre
        svg = ruta.read_text()
        if 'id="plano"' in svg:
            print(f"{nombre}: ya estaba ampliado")
            continue

        # Fuera el detalle y las dos marcas que lo anunciaban en el planisferio.
        if 'id="detalle-sudamerica"' in svg:
            i = svg.rindex("<g", 0, svg.index('id="detalle-sudamerica"'))
            svg = svg[:i] + svg[fin_de_grupo(svg, i):]
        svg = re.sub(r'<rect[^>]*x="217\.93"[^>]*/>', "", svg, count=1)
        svg = re.sub(r"<text[^>]*>[^<]*ver detalle[^<]*</text>", "", svg,
                     count=1, flags=re.I)

        svg = despejar_el_arbol(svg)
        a = svg.rindex("<g", 0, svg.index(DESDE))
        b = svg.rindex("<g", 0, svg.index(HASTA))
        svg = (svg[:a]
               + f'<g id="plano" transform="translate({tx:.3f} {ty:.3f}) '
                 f'scale({s:.5f})">' + svg[a:b] + "</g>" + svg[b:])
        # El velo va dentro del grupo ampliado, recortado al marco del mapa;
        # el neto del pliego y los grados, fuera, en coordenadas finales.
        svg = svg.replace("</svg>", marco_y_grados() + "</svg>")
        if ".grado{" not in svg:
            svg = svg.replace("</style>", ESTILO_GRADO + "</style>", 1)
        if "_bn" in nombre:
            svg = a_una_tinta(svg)
        ruta.write_text(svg)
        print(f"{nombre}: ampliado, detalle fuera, marco y grados puestos")


if __name__ == "__main__":
    main()
