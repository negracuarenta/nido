# NIDO · Los vuelos de la golondrina

Mapa interactivo de la obra **NIDO**, de Martín Virgili (Negra40). Un liquidámbar de
146 años, en Heidelberg, recibe a una golondrina que hace tres viajes —Este, Sur y
Oeste— y vuelve cada vez a contarle lo que vio.

**Sitio:** <https://negracuarenta.github.io/nido/>

De cada ficha sale un código QR impreso en el afiche A0. **Las direcciones
`/lugares/<slug>/` no se pueden cambiar**: romperían los QR ya impresos.

---

## Cambiar contenido sin tocar código

Todo el texto vive en `content/`. No hace falta entender el código para editarlo.

```
content/
├─ site.json              textos de la interfaz (leyenda, botones) en ES/DE/EN
├─ heidelberg.json        la página del árbol
└─ lugares/<slug>.json    una ficha por lugar
```

Para completar una ficha, creá `content/lugares/<slug>.json` copiando el de Iguazú
(`e1-cataratas-del-iguazu.json`) y reemplazando el contenido. El `<slug>` tiene que ser
exactamente el que figura en `nido_lugares.json`.

Cada ficha lleva:

| campo | qué es |
|---|---|
| `cita` | la frase del guión, en los tres idiomas |
| `info` | lista de párrafos, en los tres idiomas |
| `tragico` | `null`, o un objeto con `cita`, `info` y sus fuentes |
| `fotos` | archivo, epígrafe en tres idiomas, autor, licencia y origen |
| `fuentes` | institución, título, enlace y fecha de consulta |

Las fotos van en `assets/fotos/<slug>/`. Deben tener **licencia libre**, estar
descargadas (nunca enlazadas a otro servidor) y escaladas a 1600 px de ancho máximo.
Anotá cada una en `CREDITOS.md`.

**Una ficha sin archivo de contenido no rompe nada**: su página se genera igual con el
aviso «en preparación», para que el QR impreso nunca dé 404.

Al guardar y pushear a `main`, GitHub Actions regenera y publica el sitio solo.

---

## Correr el sitio en la computadora

Sólo hace falta Python 3.

```bash
python3 build.py
python3 -m http.server 8788 --directory dist
```

Y abrir <http://127.0.0.1:8788/>.

## Los códigos QR

```bash
python3 qr.py
```

Deja en `qr/` un SVG por lugar (`E1.svg` … `O8.svg`), más `inicio.svg` y
`heidelberg.svg`, en negro sobre transparente y con corrección de errores nivel M.
`qr/indice.csv` lista código, nombre y dirección de cada uno.

## El mapa

`prep_geo.py` simplifica el GeoJSON de Natural Earth 50m (2,7 MB → 640 KB). Se corre a
mano sólo si cambia el archivo de origen; el resultado está versionado.

Las rutas son arcos de círculo máximo calculados en `assets/js/mapa.js`, sin
bibliotecas extra. El cruce del antimeridiano se parte en dos tramos.

## Idiomas

Cada página lleva **los tres idiomas adentro** y el selector sólo cambia cuál se ve.
Es lo que permite que un mismo QR impreso sirva para ES, DE e EN sin redirecciones.
Sin JavaScript se ve el castellano, que es el original.

El idioma sale, en este orden: `?lang=de` en la dirección, lo que el visitante eligió
antes, o el idioma del navegador.
