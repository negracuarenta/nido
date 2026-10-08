#!/usr/bin/env python3
"""Suma al planisferio el relieve, la hidrografía y los nombres de los mares.

Hasta acá el mapa tenía la costa y nada más: una silueta plana. Esto le agrega
los accidentes del terreno —cordilleras, mesetas, fosas— con el relieve
sombreado de Natural Earth ya reproyectado por relieve.py, los ríos y lagos
principales, y los nombres de los océanos y mares.

Los nombres salen del propio Natural Earth, que los trae en castellano y en
alemán, así que la versión alemana del afiche no necesita traducirlos a mano.

Va después de planisferio.py y antes de idioma_afiche.py.
"""
import base64
import json
import math
import re
from pathlib import Path

import numpy as np

from afiche import cartela_sin_ampliar

AQUI = Path(__file__).parent
AFICHES = ("MAPA_FINAL_es_bn.svg", "MAPA_FINAL_es_color.svg")
NE = Path("/tmp/ne")

A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
X0, Y0, SEMIANCHO = 423.0, 272.0, 395.0
MAPA = (28.0, 79.75, 790.0, 384.5)      # x, y, ancho, alto del planisferio

RIOS_HASTA = 5          # rango de importancia de Natural Earth: 1 es el Amazonas
LAGOS = 45              # cuántos lagos, de mayor a menor


def directa(lon_rad, lat_rad):
    th = math.asin(math.sqrt(3) / 2 * math.sin(lat_rad))
    t2, t6 = th * th, th ** 6
    x = (2 * math.sqrt(3) * lon_rad * math.cos(th)
         / (3 * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2))))
    return x, th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))


ESCALA = SEMIANCHO / directa(math.pi, 0.0)[0]


def proyectar(lon, lat):
    x, y = directa(math.radians(((lon + 180) % 360) - 180), math.radians(lat))
    return X0 + ESCALA * x, Y0 - ESCALA * y


def inversa(x, y):
    """De milímetros del afiche a longitud y latitud. Devuelve None si el punto
    cae fuera del mapa, que en Equal Earth no es un rectángulo sino una elipse
    achatada: hacia los polos sobra papel a los costados."""
    Y = (Y0 - y) / ESCALA
    th = Y
    for _ in range(6):
        t2, t6 = th * th, th ** 6
        f = th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2)) - Y
        d = A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)
        th -= f / d
    sen = math.sin(th) / (math.sqrt(3) / 2)
    if abs(sen) > 1:
        return None
    t2, t6 = th * th, th ** 6
    D = A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)
    lon = math.degrees(3 * (x - X0) / ESCALA * D / (2 * math.sqrt(3) * math.cos(th)))
    return (lon, math.degrees(math.asin(sen))) if abs(lon) <= 180 else None


def cabe_en_el_mapa(x, y, ancho, alto) -> bool:
    """Los cuatro extremos del rótulo tienen que caer dentro del dibujo."""
    return all(inversa(px, py) is not None
               for px, py in ((x - ancho / 2, y), (x + ancho / 2, y),
                              (x, y - alto), (x, y + alto * 0.3)))


def adentro(pt, ancho, alto, pasos=14):
    """Empuja el rótulo hacia el centro del mapa hasta que entre entero."""
    x, y = pt
    for i in range(pasos):
        if cabe_en_el_mapa(x, y, ancho, alto):
            return (x, y)
        t = (i + 1) / pasos * 0.6
        x = x + (X0 - x) * t * 0.5
        y = y + (Y0 - y) * t * 0.5
    return None


def anillos(geom):
    """Todas las listas de coordenadas de una geometría, sin importar el tipo."""
    salida = []

    def rec(c):
        if not c:
            return                       # Natural Earth trae algún anillo vacío
        if isinstance(c[0], (int, float)):
            return
        if isinstance(c[0][0], (int, float)):
            salida.append(c)
        else:
            for x in c:
                rec(x)

    rec(geom["coordinates"])
    return salida


def trazo(coords, cerrar=False, minimo=0.25):
    """Un anillo proyectado, partido en el antimeridiano y aligerado.

    El aligerado tira los puntos que quedan a menos de un cuarto de milímetro
    del anterior: a escala mundial no se ven y abultan el archivo.
    """
    partes, actual, ultimo = [], [], None
    for lon, lat in coords:
        if ultimo is not None and abs(lon - ultimo) > 180:
            partes.append(actual); actual = []
        ultimo = lon
        x, y = proyectar(lon, lat)
        if not actual or cerrar or math.hypot(x - actual[-1][0], y - actual[-1][1]) > minimo:
            actual.append((x, y))
    partes.append(actual)
    d = ""
    for p in partes:
        if len(p) < 2:
            continue
        d += "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in p) + ("Z" if cerrar else "")
    return d


def area(coords):
    s = 0.0
    for (x1, y1), (x2, y2) in zip(coords, coords[1:] + coords[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def orla(pal) -> str:
    """La banda de sombra que los mapas antiguos dibujaban bordeando la costa.

    Son tres trazos cada vez más finos y más oscuros sobre la silueta de la
    tierra. Como se dibujan *antes* del relleno, la mitad interior queda tapada
    y sólo se ve la mitad que da al agua: una orla que se desvanece.
    """
    capas = ((2.6, 0.10), (1.5, 0.14), (0.7, 0.18))
    return ('<g id="orla" fill="none">' + "".join(
        f'<use href="#tierra" stroke="{pal["orla"]}" stroke-width="{w}" '
        f'opacity="{o}"/>' for w, o in capas) + "</g>")


def creditos_mapa(lang="es") -> str:
    texto = {
        "es": "Relieve, hidrografía y mares: Natural Earth. Viñetas: grabados "
              "de la Iconographia Zoologica, dominio público.",
        "de": "Relief, Gewässer und Meere: Natural Earth. Vignetten: Stiche aus "
              "der Iconographia Zoologica, gemeinfrei.",
    }[lang]
    return (f'<g id="fuentes-mapa"><text x="845" y="804" class="small">'
            f'{texto}</text></g>')


def capa_raster(ident: str, archivo: str, pal, recorte=None) -> str:
    datos = base64.b64encode((AQUI / "assets/geo" / archivo).read_bytes()).decode()
    x, y, w, h = MAPA
    clip = f' clip-path="url(#{recorte})"' if recorte else ""
    return (f'<g id="{ident}"{clip}>'
            f'<image x="{x}" y="{y}" width="{w}" height="{h}" '
            f'preserveAspectRatio="none" opacity="{pal["relieve"]}" '
            f'href="data:image/jpeg;base64,{datos}"/></g>')


def relieve(pal) -> str:
    return capa_raster("relieve", "relieve.jpg", pal, "recorte-tierra")


def batimetria(pal) -> str:
    """El fondo del océano: dorsales, fosas y plataformas continentales."""
    return capa_raster("batimetria", "batimetria.jpg", pal, "solo-mapa")


def hidrografia(pal) -> str:
    rios = json.loads((NE / "ne_50m_rivers_lake_centerlines.geojson").read_text())
    piezas = [f'<g id="hidrografia" fill="none">']
    for rango in range(RIOS_HASTA, 0, -1):       # los menores primero, debajo
        d = ""
        for f in rios["features"]:
            if f["properties"].get("scalerank") != rango:
                continue
            for c in anillos(f["geometry"]):
                d += trazo(c)
        if d:
            grosor = 0.10 + 0.055 * (RIOS_HASTA - rango)
            piezas.append(f'<path d="{d}" stroke="{pal["agua"]}" '
                          f'stroke-width="{grosor:.3f}" stroke-linecap="round" '
                          f'stroke-linejoin="round"/>')

    lagos = json.loads((NE / "ne_50m_lakes.geojson").read_text())
    conSup = []
    for f in lagos["features"]:
        aa = anillos(f["geometry"])
        conSup.append((max(area(c) for c in aa), aa))
    conSup.sort(key=lambda t: -t[0])
    d = "".join(trazo(c, cerrar=True) for _, aa in conSup[:LAGOS] for c in aa)
    piezas.append(f'<path d="{d}" fill="{pal["lago"]}" stroke="{pal["agua"]}" '
                  f'stroke-width="0.12"/>')
    piezas.append("</g>")
    return "".join(piezas)


def _dentro(pt, anillo) -> bool:
    x, y = pt
    dentro = False
    for (x1, y1), (x2, y2) in zip(anillo, anillo[1:] + anillo[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            dentro = not dentro
    return dentro


def _lejos_de_la_costa(anillo, arbol):
    """El punto del polígono más alejado de cualquier costa.

    El centroide no sirve: el del Pacífico Norte cae sobre México. Lo que se
    busca es el centro de la mancha de agua, que es donde un cartógrafo
    pondría el nombre.
    """
    xs = [c[0] for c in anillo]; ys = [c[1] for c in anillo]
    mejor, mejor_d = None, -1.0
    paso = 48
    for i in range(paso + 1):
        for j in range(paso + 1):
            pt = (min(xs) + (max(xs) - min(xs)) * i / paso,
                  min(ys) + (max(ys) - min(ys)) * j / paso)
            if not _dentro(pt, anillo):
                continue
            d = arbol.query([pt])[0][0]
            if d > mejor_d:
                mejor, mejor_d = pt, d
    return mejor, mejor_d


def mares(pal, lang="es") -> str:
    """Los nombres de océanos y mares, en itálica espaciada."""
    from scipy.spatial import cKDTree

    tierra = json.loads((AQUI / "assets/geo/land.json").read_text())
    geo = (tierra["features"][0]["geometry"] if "features" in tierra else tierra)
    costa = [proyectar(*c) for a in anillos(geo) for c in a]
    arbol = cKDTree(costa)

    datos = json.loads((NE / "ne_50m_geography_marine_polys.geojson").read_text())
    campo = "name_es" if lang == "es" else "name_de"
    # La cartela del título se apoya sobre el Pacífico: ahí no va ningún
    # nombre de mar, o quedaría debajo.
    ocupado = [cartela_sin_ampliar()]
    piezas = ['<g id="mares">']
    for f in datos["features"]:
        p = f["properties"]
        rango = p.get("scalerank", 9)
        if rango > 1:
            continue
        nombre = (p.get(campo) or p.get("name") or "").strip()
        if not nombre:
            continue
        proy = [[proyectar(*c) for c in a] for a in anillos(f["geometry"])]
        grande = max(proy, key=area)
        pt, holgura = _lejos_de_la_costa(grande, arbol)
        if pt is None:
            continue
        # El cuerpo se ajusta al hueco: un nombre que no entra se mete debajo
        # de la tierra y se lee cortado, que es peor que no ponerlo. Con la
        # letra espaciada, cada carácter avanza unos 0,92 del cuerpo.
        tam = min(5.2 if rango == 0 else 3.2,
                  holgura / (len(nombre) * 0.46))
        if tam < 2.2:
            continue
        ancho = len(nombre) * tam * 0.95
        for _ in range(6):
            sitio = adentro(pt, ancho, tam)
            if sitio:
                break
            tam *= 0.82                 # si no entra, se achica y se reintenta
            ancho = len(nombre) * tam * 0.95
        if not sitio or tam < 2.0:
            continue
        caja = (sitio[0] - ancho / 2, sitio[1] - tam,
                sitio[0] + ancho / 2, sitio[1] + tam * 0.4)
        if any(_chocan(caja, c) for c in ocupado):
            continue
        ocupado.append(caja)
        piezas.append(f'<text x="{sitio[0]:.1f}" y="{sitio[1]:.1f}" '
                      f'text-anchor="middle" class="mar" '
                      f'style="font-size:{tam:.2f}px;'
                      f'letter-spacing:{tam * 0.3:.2f}px">{nombre.upper()}</text>')
    piezas.append("</g>")
    return "".join(piezas)



# Qué accidentes se nombran y hasta qué rango de importancia de Natural Earth.
ACCIDENTES = {
    "Range/mtn": (2, 3.6), "Desert": (3, 3.4), "Basin": (2, 3.4),
    "Plateau": (2, 3.2), "Plain": (2, 3.2), "Geoarea": (2, 3.2),
    "Wetlands": (3, 3.0), "Valley": (3, 3.0), "Tundra": (2, 3.0),
}


def _eje(anillo):
    """Dirección en la que se estira el accidente, y cuánto mide en ella."""
    xs = np.array([c[0] for c in anillo]); ys = np.array([c[1] for c in anillo])
    cx, cy = xs.mean(), ys.mean()
    cov = np.cov(np.vstack([xs - cx, ys - cy]))
    val, vec = np.linalg.eigh(cov)
    v = vec[:, int(np.argmax(val))]
    ang = math.degrees(math.atan2(v[1], v[0]))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    proy = (xs - cx) * v[0] + (ys - cy) * v[1]
    return ang, float(proy.max() - proy.min())


def accidentes(pal, lang="es", ocupado=None) -> str:
    """Nombra cordilleras, desiertos, cuencas y mesetas, como un atlas.

    El nombre se tumba siguiendo la dirección en que se estira el accidente
    —los Andes van casi verticales, el Himalaya casi horizontal— y el cuerpo de
    letra se ajusta a lo que mide por ahí. Si no entra, no se pone.
    """
    from scipy.spatial import cKDTree

    datos = json.loads((NE / "ne_50m_geography_regions_polys.geojson").read_text())
    campo = "NAME_ES" if lang == "es" else "NAME_DE"
    puestos = list(ocupado or []) + [cartela_sin_ampliar()]
    piezas = ['<g id="accidentes">']
    rasgos = []
    for f in datos["features"]:
        p = f["properties"]
        tope = ACCIDENTES.get(p.get("FEATURECLA"))
        if not tope or (p.get("SCALERANK") or 9) > tope[0]:
            continue
        nombre = (p.get(campo) or p.get("NAME") or "").strip()
        if nombre:
            rasgos.append((p.get("SCALERANK") or 9, nombre, tope[1], f["geometry"]))
    rasgos.sort(key=lambda r: r[0])

    for _, nombre, base, geom in rasgos:
        proy = [[proyectar(*c) for c in a] for a in anillos(geom)]
        grande = max(proy, key=area)
        if len(grande) < 8:
            continue
        ang, largo = _eje(grande)
        pt, holgura = _lejos_de_la_costa(grande, cKDTree(grande))
        if pt is None:
            continue
        # 0,90 por carácter: medido sobre el afiche ya compuesto, con la
        # versalita espaciada. La estimación anterior se quedaba un 40 % corta
        # y por eso algunos nombres terminaban encimados.
        cuenta = max(len(nombre), 4)
        tam = min(base, largo / (cuenta * 0.90), holgura * 1.9)
        if tam < 2.1:
            continue
        ancho = cuenta * tam * 0.90
        # El rótulo va tumbado, así que la caja que ocupa de verdad es la del
        # rectángulo girado, no la del texto en horizontal.
        rad = math.radians(ang)
        anc = abs(ancho * math.cos(rad)) + abs(tam * 1.4 * math.sin(rad))
        alt = abs(ancho * math.sin(rad)) + abs(tam * 1.4 * math.cos(rad))
        caja = (pt[0] - anc / 2 - 1, pt[1] - alt / 2 - 1,
                pt[0] + anc / 2 + 1, pt[1] + alt / 2 + 1)
        if any(_chocan(caja, c) for c in puestos):
            continue
        if not cabe_en_el_mapa(pt[0], pt[1], anc, alt):
            sitio = adentro(pt, anc, alt)
            if not sitio:
                continue
            pt = sitio
        puestos.append(caja)
        giro = (f' transform="rotate({ang:.1f} {pt[0]:.1f} {pt[1]:.1f})"'
                if abs(ang) > 4 else "")
        piezas.append(
            f'<text x="{pt[0]:.1f}" y="{pt[1]:.1f}" text-anchor="middle"{giro} '
            f'class="accidente" style="font-size:{tam:.2f}px;'
            f'letter-spacing:{tam * 0.16:.2f}px">{nombre.upper()}</text>')
    piezas.append("</g>")
    return "".join(piezas)


def _chocan(a, b):
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


PALETAS = {
    "color": {"agua": "#7E9FB8", "lago": "#D7E6EF", "mar": "#8FA6B6",
              "relieve": "1", "orla": "#6E8EA6"},
    "bn": {"agua": "#9a9a9a", "lago": "#f2f2f2", "mar": "#9a9a9a",
           "relieve": "0.85", "orla": "#777777"},
}
ESTILO_MAR = (".mar{font-family:'TeX Gyre Pagella','Palatino',serif;"
              "font-style:italic;fill:%s;opacity:0.85}"
              ".accidente{font-family:'TeX Gyre Pagella','Palatino',serif;"
              "font-style:italic;fill:#6B5B43;opacity:0.72}")


def fin_de_grupo(svg: str, desde: int) -> int:
    nivel = 0
    for m in re.finditer(r"<g\b|</g>", svg[desde:]):
        nivel += 1 if m.group(0) != "</g>" else -1
        if nivel == 0:
            return desde + m.end()
    raise ValueError("no encontré el cierre del grupo")


def quitar(svg: str, ident: str) -> str:
    marca = f'<g id="{ident}"'
    while marca in svg:
        i = svg.index(marca)
        svg = svg[:i] + svg[fin_de_grupo(svg, i):]
    return svg


AGUA_FRIA, AGUA_CALIDA = "#EAF1F5", "#E9EFEE"   # un punto menos azul, más papel


def main() -> None:
    for nombre in AFICHES:
        ruta = AQUI / nombre
        svg = ruta.read_text()
        pal = PALETAS["color" if "#D9822B" in svg else "bn"]

        for ident in ("relieve", "batimetria", "hidrografia", "mares", "orla",
                      "fuentes-mapa", "accidentes"):
            svg = quitar(svg, ident)
        svg = re.sub(r'<defs id="recorte(-marco)?">.*?</defs>', "", svg, flags=re.S)

        # La costa es el trazo con más vértices del planisferio; le pongo id
        # para poder recortar el relieve contra ella sin duplicar 700 KB.
        a, b = svg.index('id="mapa-mundi"'), svg.index('id="detalle-sudamerica"')
        tierra = max(re.findall(r'd="([^"]{200,})"', svg[a:b]), key=len)
        i = svg.index(tierra, a) - len('d="')
        ini = svg.rindex("<path", 0, i)
        fin = svg.index("/>", i) + 2
        if 'id="tierra"' not in svg:
            svg = svg[:ini] + '<path id="tierra"' + svg[ini + len("<path"):]
            fin += len(' id="tierra"')

        # El fondo del océano va justo encima del relleno del mar y debajo de
        # todo lo demás: la tierra se dibuja después y lo tapa donde
        # corresponde, sin necesidad de un recorte inverso. Se recorta contra
        # el marco del planisferio para que no desborde la elipse.
        # El marco es el primer trazo del planisferio: la silueta del mapa
        # rellena con el color del agua. En la versión en blanco y negro ese
        # relleno es blanco, así que no sirve buscarlo por color.
        ini_marco = svg.index("<path", a)
        fin_marco = svg.index("/>", ini_marco) + 2
        if 'id="marco-mapa"' not in svg:
            svg = svg[:ini_marco] + '<path id="marco-mapa"' + svg[ini_marco + len("<path"):]
            crece = len(' id="marco-mapa"')
            fin_marco += crece; ini += crece; fin += crece
        capa_fondo = ('<defs id="recorte-marco"><clipPath id="solo-mapa">'
                      '<use href="#marco-mapa"/></clipPath></defs>'
                      + batimetria(pal))
        svg = svg[:fin_marco] + capa_fondo + svg[fin_marco:]
        ini += len(capa_fondo); fin += len(capa_fondo)

        capa_mar, capa_agua = mares(pal), hidrografia(pal)
        # La orla necesita que #tierra ya exista, así que va después del trazo.
        svg = (svg[:ini] + capa_mar + svg[ini:fin] + orla(pal)
               + '<defs id="recorte"><clipPath id="recorte-tierra">'
                 '<use href="#tierra"/></clipPath></defs>'
               + relieve(pal) + capa_agua + svg[fin:])
        # Los nombres de los accidentes van sobre el relieve, pero esquivando
        # lo que ya está escrito en el mapa.
        from etiquetas import obstaculos
        acc = accidentes(pal, "es", obstaculos(svg))
        svg = svg.replace('<g id="otros-vuelos">', acc + '<g id="otros-vuelos">', 1)

        if ".mar{" not in svg:
            svg = svg.replace("</style>", ESTILO_MAR % pal["mar"] + "</style>", 1)
        else:
            svg = re.sub(r"\.mar\{[^}]*\}", ESTILO_MAR % pal["mar"], svg, count=1)

        if "#D9822B" in svg:
            svg = svg.replace(AGUA_FRIA, AGUA_CALIDA)
        ruta.write_text(svg)
        print(f"{nombre}: relieve y batimetría + "
              f"{len(re.findall(r'<text', capa_mar))} mares + "
              f"{len(re.findall(r'<text', acc))} accidentes · "
              f"{ruta.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
