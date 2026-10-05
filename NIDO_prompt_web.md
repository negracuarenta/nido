# Prompt para Claude Code — Web interactiva "NIDO · Los vuelos de la golondrina"

Copiá todo lo que sigue y pegalo en Claude Code, abierto en la carpeta `~/Desktop/Nido/mapa`.

---

## Contexto

NIDO es una obra escénica de Martín Virgili (plataforma Negra40). Un liquidámbar de 146 años, en Heidelberg (Alemania), recibe a una golondrina que hace tres viajes —al **Este**, al **Sur** y al **Oeste**— y vuelve cada vez a contarle lo que vio. Cada viaje tiene dos caras: las maravillas y "lo que también vio" (catástrofes ambientales y especies amenazadas).

Ya existe un afiche A0 con el mapa de esos vuelos (`NIDO_mapa_A0_color.pdf` / `.svg`, en esta carpeta). Ahora quiero una **página web interactiva** con el mismo mapa: al hacer clic en cada lugar se abre su ficha con textos y fotos. Cada ficha tiene una dirección fija, porque de esas direcciones salen los **códigos QR** que van impresos en el afiche.

## Datos de partida

- `nido_lugares.json` (en esta carpeta). Contiene:
  - Heidelberg como origen.
  - Los tres viajes, cada uno con su color y su orden.
  - Los 35 lugares, con código (E1…E10, S1…S17, O1…O8), nombre, `slug`, coordenadas, `tragico` (tiene "lo que también vio") y `soloTragico` (aparece sólo en la parte trágica, no es una maravilla).
  - El orden de los lugares dentro de cada viaje es el **orden del recorrido**: la ruta sale de Heidelberg, pasa por ellos en ese orden (salteando los `soloTragico`) y vuelve a Heidelberg.
- Los textos del guión por lugar están al final de este documento (Anexo).

## Qué quiero

### 1. Mapa interactivo (página de inicio)
- Un mapa del mundo con **zoom y desplazamiento**, que funcione bien en celular.
- Usá **Leaflet** o **MapLibre GL**. Sin servicios pagos ni claves de API.
- **Estética igual al afiche**:
  - Tierra beige `#ECE5D3`, mar celeste pálido `#EAF1F5`, contornos `#B9AD92`.
  - Tipografía serif clásica, por ejemplo TeX Gyre Pagella o EB Garamond.
  - Preferí dibujar la tierra con un GeoJSON de Natural Earth (50m) en vez de un mapa base comercial, para mantener el estilo.
- **Rutas** como arcos de círculo máximo (podés usar Turf `greatCircle`). Cuidado con el cruce del antimeridiano.
  - Este: ocre `#D9822B`, punteado.
  - Sur: azul `#2B6CB0`, rayado.
  - Oeste: verde `#2F8F5B`, raya y punto.
- **Marcadores**:
  - Un punto del color de su viaje para cada lugar.
  - Una ✕ roja `#C62828` junto al punto si el lugar es trágico, y sólo la ✕ si es `soloTragico`.
  - Heidelberg con un símbolo propio (círculo con punto central): "Punto 0 · el árbol".
- Al pasar el mouse por un lugar se ve el nombre. Al hacer clic se abre su ficha.
- **Leyenda**:
  - Los tres viajes, con color y tipo de línea.
  - Las dos clases de símbolo.
  - Filtros para mostrar u ocultar cada viaje y la capa trágica.

### 2. Ficha de cada lugar (una página estática por lugar)
- Dirección fija y legible: `/lugares/<slug>/` (usar el `slug` del JSON). **Esta dirección no puede cambiar después**, porque va en los QR.
- **Contenido, en este orden**:
  1. Nombre del lugar, código y viaje (con su color).
  2. **La frase del guión**, destacada como cita. Está en el Anexo.
  3. **Información** sobre el lugar: 2 o 3 párrafos breves con datos concretos (geografía, ecosistema, especies, cultura, datos notables).
  4. **Galería de fotos**: de 3 a 6 imágenes, cada una con epígrafe y crédito.
  5. **Botón "Lo que también vio"**, sólo en los lugares trágicos. Abre un panel aparte con:
     - el texto trágico del guión;
     - información sobre la amenaza o catástrofe concreta: qué pasó, cuándo, cifras, causas y estado actual;
     - sus fuentes.
  6. **Fuentes**: lista completa al pie.
  7. Navegación: anterior y siguiente dentro del viaje, y volver al mapa.
- **Página de Heidelberg / el árbol**: presenta el liquidámbar y la golondrina con los textos del Acto 1 que están en el Anexo.

### 3. Fuentes: regla estricta
- Cada dato de la información tiene que venir de una **fuente confiable**. Ejemplos:
  - Centros de investigación y universidades; CONICET.
  - Organismos científicos o de conservación: UICN / Lista Roja, UNESCO Patrimonio Mundial, WWF.
  - Parques nacionales: APN Argentina, ICMBio Brasil, NPS Estados Unidos, Parks Australia, SANParks, etc.
  - Agencias como NASA Earth Observatory, NOAA, AIMS o GBRMPA.
  - Artículos científicos con DOI.
- **No** usar blogs, sitios de turismo ni Wikipedia como fuente de datos. Wikipedia sirve sólo para orientarse y para las fotos.
- Cada fuente se cita con: institución, título, enlace y fecha de consulta.
- Si un dato no se puede respaldar, no va. Si el guión dice algo que las fuentes contradicen, **no corrijas el guión**: anotalo en un archivo `REVISAR.md` para que yo lo decida.

### 4. Fotos
- Sólo imágenes con **licencia libre**:
  - Wikimedia Commons;
  - Flickr con licencia Creative Commons;
  - dominio público de agencias como NASA, USGS o NPS;
  - otros sitios públicos que declaren explícitamente una licencia libre.
- "Público" no alcanza: **la licencia tiene que permitir reutilizar la imagen**.
- **Descargá las imágenes al repositorio** (no enlazarlas desde otros sitios). Optimizalas para web (WebP o JPG, con un ancho máximo de unos 1600 px).
- Guardá autor, licencia y enlace de origen de cada foto en un archivo de créditos. Mostralos en el epígrafe con el formato "título · autor · licencia · fuente".

### 5. Idiomas
- **Castellano** (original), **alemán** e **inglés**.
- Selector ES / DE / EN visible en todas las páginas.
- El idioma inicial se toma del navegador. Se puede forzar con `?lang=de`, y la misma dirección vale para los tres idiomas (así un solo QR sirve para todos).
- Las frases del guión se traducen respetando su tono poético. Marcá las traducciones como pendientes de revisión en `REVISAR.md`.

### 6. Estructura técnica y publicación
- **Sitio estático** que funcione en **GitHub Pages**, sin servidor.
- El contenido va separado del código: un archivo por lugar, por ejemplo `content/lugares/<slug>.json` o `.md`. Cada archivo tiene los campos por idioma: cita, información, texto trágico, información trágica, fuentes y fotos.
- Un script sencillo genera las páginas a partir del contenido.
- **Repositorio**: es un proyecto más de **Negra40**. Antes de crear nada:
  - preguntame en qué cuenta u organización de GitHub va y cómo se llama el repositorio (sugerencia: `nido`);
  - decime cuál va a ser la **dirección final** del sitio.
- Configurá la publicación automática con GitHub Pages.
- Accesible y liviano: textos alternativos en las fotos, contraste suficiente y uso con teclado.

### 7. Códigos QR para el afiche
- Cuando la dirección del sitio esté definida, generá un **QR en SVG por lugar**, más uno para la página de inicio y otro para Heidelberg.
- Guardalos en `qr/` con el nombre `<código>.svg` (por ejemplo `qr/E1.svg`). Deben ser vectoriales, en negro sobre transparente y con corrección de errores nivel M.
- Agregá un `qr/indice.csv` con código, nombre y dirección.

## Forma de trabajo
1. Primero proponé un plan y la estructura de carpetas, y preguntame lo que necesites.
2. Armá **una sola ficha completa como muestra**: E1, Cataratas del Iguazú, con información, fuentes, fotos, botón trágico (si corresponde) y los tres idiomas. También el mapa funcionando localmente. Esperá mi aprobación.
3. Recién después completá los 35 lugares, de a un viaje por vez, y mostrame cada viaje terminado.
4. Al final:
   - `REVISAR.md` con dudas, contradicciones y traducciones a revisar;
   - la lista de créditos de fotos;
   - las instrucciones para actualizar contenido sin tocar código.

---

## Anexo — Textos del guión por lugar

Nota: los textos trágicos marcados **(a confirmar)** son la última versión de trabajo y pueden cambiar. Respetá la redacción tal como está.

### Heidelberg · el árbol (Acto 1)
- Árbol: "En un bosque del mundo nació este liquidambar hace ciento cuarenta y seis años. […] Es un árbol de hoja caduca. Sus hojas tienen forma de estrella, de tres a cinco puntas, y en otoño se vuelven naranjas, rojas, casi violetas: el liquidambar es de los pocos árboles que en su despedida anual se pone más hermoso, no menos."
- Golondrina: "El pájaro es una golondrina. Nació en un nido de barro que sus padres armaron pluma a pluma en apenas diez días. […] Una golondrina puede volar a más de cien kilómetros por hora cuando hace falta, y cruzar doce mil kilómetros dos veces por año."
- Pacto: "—Quedate. Tengo lugar entre mis ramas para vos y para cualquier nido que quieras hacer. Yo te voy a dar mi quietud. —Y yo te voy a dar el mundo. Cada vez que vuelva, te voy a contar todo lo que vi."

### ESTE (Acto 2) — "Fui al este. Y vi:"
- **E1 Cataratas del Iguazú**: "Un río que se rompe en dos para caer, y en la caída, dicen, un arcoíris donde dos amantes todavía se encuentran."
- **E2 Pantanal**: "Vi un pantano tan grande que le dicen el arca de Noé: ahí cabe casi todo lo que respira."
  - Trágico: "El arca de Noé, ardiendo, durante meses."
- **E3 Amazonas**: "Vi una flor de agua, ancha como una mesa, que se abre de noche y huele a durazno."
- **E4 Lençóis Maranhenses**: "Vi un desierto que en verano se llena de lagunas, como si la lluvia ahí no supiera que los desiertos no deberían tener sed."
- **E5 Bonito**: "Vi piscinas de agua azul adentro de cuevas de piedra"
- **E6 Cachoeira da Fumaça**: "y una cascada que cae trescientos ochenta metros sin tocar nada."
- **E7 Delta del Paraná**: "Vi islas nuevas, hechas de barro, que un río le regala al mar todos los días."
  - Trágico: "Un río, el más ancho de todos, que un año se secó tanto que se podía cruzar caminando."
- **E8 Fernando de Noronha**: "Vi tortugas, delfines, pájaros de mar, en un archipiélago que se cuida dejando entrar a muy pocos."
- **E9 Esteros del Iberá**: "Y vi un yaguareté —el primero en volver, en cien años, a un pastizal que ya lo daba por perdido."
- **E10 Bosque Atlántico** (sólo trágico): "Un bosque que ya casi no está: de cada diez árboles que había, hoy queda uno. Y en lo que quedaba de ese bosque, gente que tampoco encontró su lugar: familias guaraníes corridas de su propia tierra por el avance de la soja."
- Cierre trágico del Este: "Eso también vi."

### SUR (Acto 3) — "Fui al sur. Y vi…"
- **S1 Antártida**: "Vi un continente blanco como el fuego de las estrella. Allí el pingüino emperador pasa dos meses sin comer a cuarenta grados bajo cero."
  - Trágico (a confirmar): "Vi al pingüino emperador perder a todas sus crías porque el hielo se rompió antes de que aprendieran a nadar."
- **S2 Islas Georgias del Sur**: "Sobre el mar más frío de la Tierra vi planear al albatros errante que me contó que hacía 5 años que no tocaba la tierra."
  - Trágico (a confirmar): "Vi al albatros, el que no tocaba tierra, tragarse el anzuelo de un barco y hundirse con él. […] Vi el mar, que siempre fue de los más fríos, entibiarse como una fiebre que no baja."
- **S3 Cordillera de los Andes**: "En los Andes vi al cóndor subir por espirales de aire caliente que sólo él ve."
  - Trágico (a confirmar): "Vi al cóndor caer envenenado por un cebo que era para otro."
- **S4 Bosques de araucarias**: "Vi bosques de araucarias de más de mil años"
- **S5 Glaciar Perito Moreno**: "y un glaciar gigante soltar pedazos de hielo del tamaño de una casa."
  - Trágico (a confirmar): "Vi el hielo —el mismo hielo que te dije que era hermoso— derretirse más rápido que nunca. Es desesperante, árbol."
- **S6 Estepa patagónica**: "Vi pumas y guanacos correr por la estepa de la Patagonia"
- **S7 Península Valdés**: "y ballenas que les cantan a sus crías."
- **S8 Cataratas Victoria**: "Crucé el océano. En las cataratas Victoria vi una cortina de agua de casi dos kilómetros: los que viven ahí la llaman Mosi Tunya, el humo que truena."
- **S9 Desierto del Namib**: "En el Namib, el desierto más viejo del mundo, vi dunas rojas como la sangre de trescientos metros de altura y un escarabajo que bebe de la niebla."
- **S10 Delta del Okavango**: "Vi el Okavango, un río que no llega al mar porque se pierde en el desierto. De esa escasa agua viven elefantes e hipopótamos, y flores que nacen del barro."
  - Trágico (a confirmar): "Vi elefantes morir junto a charcas que el calor volvió veneno, y máquinas buscando petróleo en el río que alimenta al Okavango."
- **S11 Serengueti**: "En el Serengueti vi un millón y medio de animales cruzar juntos la sabana. […] Escuché la risa de las hienas y el rugido del leopardo."
  - Trágico (a confirmar): "Vi que en veinticinco años se fue casi la mitad de los leones."
- **S12 Gran Barrera de Coral**: "Y seguí hasta Australia. Vi la Gran Barrera de Coral: más de dos mil kilómetros construidos por animales más chicos que una uña."
  - Trágico (a confirmar): "Vi la Gran Barrera de Coral ponerse blanca como un hueso, cinco veces en ocho años."
- **S13 Shark Bay**: "En Shark Bay vi piedras vivas, construidas por seres diminutos que existen desde hace tres mil millones de años."
- **S14 Selva de Daintree**: "Conocí la selva de Daintree, más antigua que el Amazonas, que ya era selva cuando caminaban los dinosaurios."
- **S15 Uluru**: "Vi el Uluru, una roca sagrada del tamaño de una montaña."
- **S16 Bosques andino-patagónicos** (sólo trágico): "Vi bosques centenarios convertidos en cenizas por manos que después vinieron a comprar la tierra ennegrecida. Entre las cenizas vi sufrir al improbable huemul, un ciervo que ya casi se ha ido."
- **S17 Sudeste australiano** (sólo trágico, a confirmar): "Vi en Australia un verano de fuego que mató o dejó sin casa a tres mil millones de animales."
- Cierre del Sur: "El sur, árbol, es hermoso." / Cierre trágico: "Eso también vi, árbol. No te mentí en la primera parte. Tampoco te voy a mentir en esta."

### OESTE (Acto 4) — "Fui al oeste,"
- **O1 El Chaltén**: "Y vi el Chaltén, un pueblo de montañas, glaciares y ríos y noches."
  - Trágico (a confirmar): "Vi el hielo del Chaltén y del Aconcagua, ese oro blanco que te conté, retroceder año tras año."
- **O2 Aconcagua**: "Y subí hasta el Aconcagua y descubrí el oro blanco de la nieve y comprendí América."
  - Trágico (a confirmar): "Y vi a los hombres votar una ley que le quita protección, para que las máquinas puedan llegar más cerca."
- **O3 Salinas Grandes**: "Vi las Salinas Grandes, un desierto de sal interminable que de noche parece que uno puede caminar por las estrellas. Conocí a las vicuñas y los zorros responderse sus cantos."
  - Trágico (a confirmar): "Vi el mismo desierto de sal perforado, buscando el litio que duerme debajo. Donde ya lo sacan, los salares se hunden y el agua se evapora por millones de litros, mientras a los que viven ahí se les seca el pozo. Vi a los flamencos quedarse sin las lagunas donde anidaban. Y vi a los que cortan la sal a mano salir a la ruta a defender su agua, y los vi golpeados. Vi a la vicuña, que estuvo a punto de desaparecer y volvió, caer otra vez por su lana. Vi zorros colgados de los alambrados."
- **O4 Cerro de los Siete Colores**: "Vi el cerro de los Siete Colores: millones de años de mar, de barro y de hierro apilados en capas: te juro que vi un arcoíris incrustado en la piedra."
- **O5 Páramo de Sumapaz**: "En los páramos vi el frailejón, una planta maravillosa que bebe de los ríos voladores para llevarlos a la tierra. Crece apenas un centímetro por año, y entre ellos vi al oso de anteojos."
  - Trágico (a confirmar): "En el páramo vi al frailejón, el que bebe de las nubes, pudrirse de pie, comido por larvas y hongos que el calor dejó subir. Vi que debajo de él buscan oro. Y vi al oso de anteojos, el único oso de toda Sudamérica, morir a tiros cuando baja a comer cerca del ganado."
- **O6 Laguna de Guatavita**: "Vi una laguna misteriosa en medio de los Andes, que cuenta la leyenda que allí los hombres entregaban el oro a los dioses."
  - Trágico (a confirmar): "Vi la laguna del oro con una herida abierta en el borde: la cortaron para vaciarla y robarles a los dioses sus ofrendas."
- **O7 Wirikuta**: "En el desierto de Wirikuta vi un pueblo caminar cientos de kilómetros hasta el lugar donde, dicen, nació el sol. Allí, vi el milagro del Peyote."
  - Trágico (a confirmar): "En Wirikuta, donde nació el sol, vi minas pedidas sobre la tierra sagrada, y manos arrancando el peyote para venderlo más rápido de lo que tarda en crecer."
- **O8 Secuoyas gigantes**: "Subí con mucha fuerza y vi las secuoyas gigantes, árbol. Abuelos tuyos de ochenta metros de alto y tres mil años de vida. Me contaron que tienen una corteza tan gruesa que resiste el fuego, y piñas que sólo se abren con el calor del incendio. Vi Osos, águilas y ardillas."
  - Trágico (a confirmar): "Y vi a las secuoyas, árbol, tus abuelas, las que resistieron el fuego tres mil años, arder como antorchas. En dos veranos murió casi una de cada cinco. El fuego que antes abría sus piñas, ahora las mata."
- Cierre del Oeste: "Me enamoré, árbol. El oeste, la puerta negra, es maravilloso." / Cierre trágico: "Dolor. Mucho dolor. Vi la pobreza más difícil de todas: la de los corazones que ya no se conmueven."
