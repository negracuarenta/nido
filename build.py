#!/usr/bin/env python3
"""Genera el sitio estático de NIDO a partir de content/ y nido_lugares.json.

No hay framework ni dependencias: se corre con `python3 build.py` y deja todo
en dist/, listo para GitHub Pages.

Dos decisiones que conviene tener presentes al leer esto:

1. Cada página lleva los tres idiomas adentro y el selector sólo cambia cuál se
   ve. Es la única forma de que un mismo QR impreso sirva para ES, DE e EN sin
   redirecciones. Sin JavaScript se ve el castellano.
2. Todo lugar de nido_lugares.json genera página, tenga contenido o no. Los QR
   ya están impresos en el afiche: una ficha sin terminar tiene que mostrar
   "en preparación", nunca un 404.
"""
import json
import shutil
from html import escape
from pathlib import Path

AQUI = Path(__file__).parent
DIST = AQUI / "dist"
IDIOMAS = ("es", "de", "en")

COLOR = {"E": "#D9822B", "S": "#2B6CB0", "O": "#2F8F5B", "OV": "#6B4E9B"}
TRAZO = {"E": "6 5", "S": "14 6", "O": "12 4 2 4", "OV": "2 4"}


# ---------------------------------------------------------------- utilidades

def t(nodo, lang):
    """Devuelve la variante de idioma, cayendo al castellano si falta."""
    if not isinstance(nodo, dict):
        return nodo or ""
    return nodo.get(lang) or nodo.get("es") or ""


def por_idioma(constructor, clase=""):
    """Envuelve el mismo bloque en sus tres idiomas; el CSS muestra uno."""
    partes = []
    for lang in IDIOMAS:
        contenido = constructor(lang)
        if not contenido:
            continue
        partes.append(f'<div class="i18n {clase}" data-lang="{lang}">{contenido}</div>')
    return "\n".join(partes)


def parrafos(nodo, lang):
    return "\n".join(f"<p>{escape(p)}</p>" for p in (nodo.get(lang) or nodo.get("es") or []))


# ------------------------------------------------------------------ plantilla

def pie_sitio(site, base):
    """Autoría de la obra y las instituciones que la acompañan.

    Va en todas las páginas: cada ficha puede llegarse directo por su QR, sin
    pasar nunca por la portada, así que la autoría tiene que viajar con ella.
    """
    logos = [
        ("negra40.png", "negra40", "negra40"),
        ("ceac.png", "CEAC · Centro de Arte y Ciencia, UTN Regional Mar del Plata", "ceac"),
        ("vpst.png", "Völkerkundemuseum vPST", "vpst"),
    ]
    marcas = "".join(
        f'<li><img class="logo logo--{clase}" src="{base}assets/logos/{archivo}" '
        f'alt="{escape(alt)}" loading="lazy"></li>'
        for archivo, alt, clase in logos
    )
    return f"""
<footer class="pie-sitio">
  <div class="pie-sitio__obra">
    <p class="pie-sitio__titulo">NIDO</p>
    {por_idioma(lambda l: f'<p class="pie-sitio__autores">{escape(t(site["ui"]["autores"], l))}</p>')}
  </div>
  <div class="pie-sitio__marcas">
    {por_idioma(lambda l: f'<p class="pie-sitio__con">{escape(t(site["ui"]["con_apoyo"], l))}</p>')}
    <ul class="pie-sitio__logos">{marcas}</ul>
  </div>
</footer>
"""


def pagina(titulo, cuerpo, *, base, clase="", head="", site=None):
    nav_idiomas = "".join(
        f'<button type="button" class="sel-idioma" data-set-lang="{l}" '
        f'lang="{l}">{l.upper()}</button>' for l in IDIOMAS
    )
    pie = pie_sitio(site, base) if site else ""
    return f"""<!doctype html>
<html lang="es" data-lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(titulo)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/nido.css">
{head}
</head>
<body class="{clase}">
<header class="barra">
  <a class="marca" href="{base}">NIDO</a>
  <nav class="idiomas" aria-label="Idioma / Sprache / Language">{nav_idiomas}</nav>
</header>
{cuerpo}
{pie}
<script src="{base}assets/js/idioma.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- ficha lugar

def ficha(lugar, viaje, contenido, site, vecinos, base):
    clave = viaje["key"] if viaje else None
    color = COLOR.get(clave, "#6B5F4B")
    nombre = lugar["name"]
    ui = site["ui"]

    cabecera = por_idioma(lambda l: (
        f'<p class="codigo" style="--c:{color}">'
        f'<span class="pastilla"></span>{escape(lugar["id"])} · '
        f'{escape(t(site["viajes"].get(clave, {}), l)) if clave else escape(t(ui["punto_cero"], l))}</p>'
    ))

    if contenido:
        cita = por_idioma(lambda l: (
            f'<blockquote class="cita">{escape(t(contenido["cita"], l)).replace(chr(10), "<br>")}</blockquote>'
            if t(contenido["cita"], l) else ""
        ))
        info = por_idioma(lambda l: (
            f'<h2>{escape(t(ui["informacion"], l))}</h2>{parrafos(contenido["info"], l)}'
            if contenido.get("info") else ""
        ))
        galeria = bloque_galeria(contenido, lugar["slug"], ui, base)
        tragico = bloque_tragico(contenido, ui)
        fuentes = bloque_fuentes(contenido.get("fuentes", []), ui)
    else:
        cita = ""
        info = por_idioma(lambda l: f'<p class="aviso">{escape(t(ui["en_preparacion"], l))}</p>')
        galeria = tragico = fuentes = ""

    anterior, siguiente = vecinos
    def enlace(v, etiqueta, clase):
        if not v:
            return ""
        return por_idioma(lambda l, v=v: (
            f'<a class="{clase}" href="{base}lugares/{v["slug"]}/">'
            f'{escape(t(ui[etiqueta], l))}<span>{escape(v["name"])}</span></a>'
        ))

    cuerpo = f"""
<main class="ficha">
  <article>
    {cabecera}
    <h1>{escape(nombre)}</h1>
    {cita}
    {info}
    {tragico}
    {galeria}
    {fuentes}
  </article>
  <nav class="pie">
    {enlace(anterior, "anterior", "anterior")}
    {por_idioma(lambda l: f'<a class="volver" href="{base}">{escape(t(ui["volver"], l))}</a>')}
    {enlace(siguiente, "siguiente", "siguiente")}
  </nav>
</main>
"""
    return pagina(f"{nombre} · NIDO", cuerpo, base=base, clase="pagina-ficha", site=site)


def bloque_galeria(contenido, slug, ui, base):
    fotos = contenido.get("fotos") or []
    if not fotos:
        return ""
    piezas = []
    for f in fotos:
        epi = por_idioma(lambda l, f=f: escape(t(f["epigrafe"], l)))
        credito = (f'{escape(f["autor"])} · {escape(f["licencia"])} · '
                   f'<a href="{escape(f["origen"])}" rel="noopener">Wikimedia Commons</a>')
        alt = t(f["epigrafe"], "es")
        piezas.append(
            f'<figure><img src="{base}assets/fotos/{slug}/{f["archivo"]}" '
            f'alt="{escape(alt)}" loading="lazy" decoding="async">'
            f'<figcaption>{epi}<span class="credito">{credito}</span></figcaption></figure>'
        )
    titulo = por_idioma(lambda l: f'<h2>{escape(t(ui["galeria"], l))}</h2>')
    return f'<section class="galeria">{titulo}{"".join(piezas)}</section>'


def bloque_tragico(contenido, ui):
    tr = contenido.get("tragico")
    if not tr:
        return ""
    cita = por_idioma(lambda l: (
        f'<blockquote class="cita cita-tragica">{escape(t(tr["cita"], l))}</blockquote>'
        if tr.get("cita") else ""
    ))
    info = por_idioma(lambda l: parrafos(tr.get("info", {}), l))
    boton = por_idioma(lambda l: escape(t(ui["ver_tragico"], l)))
    return f"""
<section class="tragico">
  <button type="button" class="abrir-tragico" aria-expanded="false" aria-controls="panel-tragico">
    <span class="cruz" aria-hidden="true">✕</span>{boton}
  </button>
  <div class="panel-tragico" id="panel-tragico" hidden>{cita}{info}</div>
</section>
"""


def bloque_fuentes(fuentes, ui):
    if not fuentes:
        return ""
    filas = []
    for f in fuentes:
        txt = f'<strong>{escape(f["institucion"])}</strong>, {escape(f["titulo"])}'
        if f.get("url"):
            txt += f' — <a href="{escape(f["url"])}" rel="noopener">{escape(f["url"])}</a>'
        cons = por_idioma(lambda l, f=f: f'{escape(t(ui["consultado"], l))} {escape(f["consultado"])}')
        filas.append(f"<li>{txt} <span class='consultado'>{cons}</span></li>")
    titulo = por_idioma(lambda l: f'<h2>{escape(t(ui["fuentes"], l))}</h2>')
    return f'<section class="fuentes">{titulo}<ol>{"".join(filas)}</ol></section>'


# ------------------------------------------------------------------ el mapa

def indice(datos, site):
    ui = site["ui"]
    leyenda_viajes = "".join(
        f'<li><label><input type="checkbox" checked data-viaje="{v["key"]}">'
        f'<svg width="34" height="10" aria-hidden="true"><line x1="1" y1="5" x2="33" y2="5" '
        f'stroke="{COLOR[v["key"]]}" stroke-width="2.5" stroke-dasharray="{TRAZO[v["key"]]}"/></svg>'
        + por_idioma(lambda l, v=v: escape(t(site["viajes"][v["key"]], l)))
        + "</label></li>"
        for v in datos["trips"]
    )
    cuerpo = f"""
<div class="mapa-zona">
<div id="mapa" role="application" aria-label="Mapa de los vuelos"></div>
<aside class="leyenda">
  <h1 class="titulo">{por_idioma(lambda l: escape(t(site["titulo"], l)))}</h1>
  {por_idioma(lambda l: f'<p class="subtitulo">{escape(t(site["subtitulo"], l))}</p>')}
  {por_idioma(lambda l: f'<p class="bajada">{escape(t(site["bajada"], l))}</p>')}
  <h2>{por_idioma(lambda l: escape(t(ui["viajes"], l)))}</h2>
  <ul class="filtros">{leyenda_viajes}</ul>
  <h2>{por_idioma(lambda l: escape(t(ui["simbolos"], l)))}</h2>
  <ul class="simbolos">
    <li><span class="s-punto"></span>{por_idioma(lambda l: escape(t(ui["lugar"], l)))}</li>
    <li><label><input type="checkbox" checked id="capa-tragica">
      <span class="s-cruz">✕</span>{por_idioma(lambda l: escape(t(ui["capa_tragica"], l)))}</label></li>
    <li><span class="s-cero"></span>{por_idioma(lambda l: escape(t(ui["punto_cero"], l)))}</li>
  </ul>
</aside>
</div>
"""
    head = ('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n'
            '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" defer></script>\n'
            '<script src="assets/js/mapa.js" defer></script>')
    return pagina("NIDO · Los vuelos de la golondrina", cuerpo,
                  base="", clase="pagina-mapa", head=head, site=site)



# --------------------------------------------------------- resumen de viaje

def resumen_viaje(viaje, textos, contenidos, site, base):
    """El recorrido completo de un acto, en una sola lectura.

    Va en orden de vuelo e incluye los lugares `soloTragico`, que en el mapa no
    están sobre la ruta: acá sí corresponden, porque son parte de lo que la
    golondrina contó.
    """
    clave = viaje["key"]
    color = COLOR[clave]
    ui = site["ui"]

    entradas = []
    for lugar in viaje["places"]:
        c = contenidos.get(lugar["slug"])
        foto = ""
        if c and c.get("fotos"):
            f = c["fotos"][0]
            foto = (f'<img src="{base}assets/fotos/{lugar["slug"]}/{f["archivo"]}" '
                    f'alt="{escape(t(f["epigrafe"], "es"))}" loading="lazy" decoding="async">')
        cita = por_idioma(lambda l, c=c: (
            f'<p class="cita-corta">{escape(t(c["cita"], l))}</p>'
            if c and t(c["cita"], l) else ""
        ))
        resumen = por_idioma(lambda l, c=c: (
            f'<p>{escape((c["info"].get(l) or c["info"].get("es") or [""])[0])}</p>'
            if c and (c["info"].get(l) or c["info"].get("es")) else ""
        ))
        marca = ('<span class="cruz-chica" title="Lo que también vio">✕</span>'
                 if lugar.get("tragico") or lugar.get("soloTragico") else "")
        entradas.append(f"""
<article class="parada">
  <a class="parada__foto" href="{base}lugares/{lugar['slug']}/">{foto}</a>
  <div class="parada__texto">
    <p class="codigo" style="--c:{color}"><span class="pastilla"></span>{escape(lugar['id'])}{marca}</p>
    <h2><a href="{base}lugares/{lugar['slug']}/">{escape(lugar['name'])}</a></h2>
    {cita}
    {resumen}
  </div>
</article>""")

    def linea(campo, clase):
        return por_idioma(lambda l: (
            f'<p class="{clase}">{escape(t(textos[campo], l))}</p>'
            if t(textos.get(campo, {}), l) else ""
        ))

    nombre = por_idioma(lambda l: escape(t(site["viajes"][clave], l)))
    cuerpo = f"""
<main class="viaje" style="--c:{color}">
  <header class="viaje__cabecera">
    <p class="codigo" style="--c:{color}"><span class="pastilla"></span>{escape(textos['acto'])}</p>
    <h1>{nombre}</h1>
    {linea('apertura', 'apertura')}
  </header>
  <div class="paradas">{''.join(entradas)}</div>
  <footer class="viaje__cierre">
    {linea('cierre', 'cierre')}
    {linea('cierre_tragico', 'cierre cierre--tragico')}
    {por_idioma(lambda l: f'<a class="volver" href="{base}">{escape(t(ui["volver"], l))}</a>')}
  </footer>
</main>
"""
    titulo = t(site["viajes"][clave], "es")
    return pagina(f"{titulo} · NIDO", cuerpo, base=base, clase="pagina-viaje", site=site)


# --------------------------------------------------------------------- build

def main() -> None:
    datos = json.loads((AQUI / "nido_lugares.json").read_text(encoding="utf-8"))
    site = json.loads((AQUI / "content/site.json").read_text(encoding="utf-8"))

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    # El mapa necesita los datos de lugares y los colores del afiche.
    (DIST / "assets").mkdir()
    for sub in ("css", "js", "geo", "fotos", "logos"):
        origen = AQUI / "assets" / sub
        if origen.exists():
            shutil.copytree(origen, DIST / "assets" / sub)
    (DIST / "assets/datos.json").write_text(json.dumps(
        {"origin": datos["origin"], "trips": datos["trips"],
         "color": COLOR, "trazo": TRAZO,
         "viajes": site["viajes"]}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")

    (DIST / "index.html").write_text(indice(datos, site), encoding="utf-8")

    # Una página por lugar, más la del árbol.
    paginas = [(json.loads((AQUI / "content/heidelberg.json").read_text(encoding="utf-8")),
                dict(datos["origin"], slug="heidelberg", id="P0",
                     name=datos["origin"]["name"]), None, (None, None))]

    for viaje in datos["trips"]:
        lista = viaje["places"]
        for i, lugar in enumerate(lista):
            ruta = AQUI / f"content/lugares/{lugar['slug']}.json"
            contenido = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None
            vecinos = (lista[i - 1] if i > 0 else None,
                       lista[i + 1] if i < len(lista) - 1 else None)
            paginas.append((contenido, lugar, viaje, vecinos))

    # Las páginas de resumen reusan el contenido ya leído de cada ficha.
    contenidos = {}
    for carpeta_json in (AQUI / "content/lugares").glob("*.json"):
        contenidos[carpeta_json.stem] = json.loads(carpeta_json.read_text(encoding="utf-8"))

    for viaje in datos["trips"]:
        textos_ruta = AQUI / "content/viajes"
        for archivo in textos_ruta.glob("*.json"):
            textos = json.loads(archivo.read_text(encoding="utf-8"))
            if textos["key"] != viaje["key"]:
                continue
            destino = DIST / "viajes" / textos["slug"]
            destino.mkdir(parents=True, exist_ok=True)
            (destino / "index.html").write_text(
                resumen_viaje(viaje, textos, contenidos, site, base="../../"),
                encoding="utf-8")

    hechas, pendientes = 0, []
    for contenido, lugar, viaje, vecinos in paginas:
        carpeta = DIST / "lugares" / lugar["slug"]
        carpeta.mkdir(parents=True, exist_ok=True)
        html = ficha(lugar, viaje, contenido, site, vecinos, base="../../")
        (carpeta / "index.html").write_text(html, encoding="utf-8")
        if contenido:
            hechas += 1
        else:
            pendientes.append(lugar["id"])

    print(f"dist/ · {len(paginas)} páginas · {hechas} con contenido · "
          f"{len(pendientes)} en preparación")
    if pendientes:
        print("  pendientes:", " ".join(pendientes))


if __name__ == "__main__":
    main()
