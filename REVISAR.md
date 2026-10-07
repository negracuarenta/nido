# Para revisar

Dudas, contradicciones entre fuentes y traducciones pendientes de tu visto bueno.
Nada de esto se resolvió por cuenta propia: el guión no se toca.

---

## Contradicciones entre fuentes

### E1 · Cantidad de especies de aves en Iguazú
- **Parques Nacionales (APN)** dice «más de 450 especies de aves».
- **UNESCO** dice «around 400 bird species».

Quedó escrito como *«más de 450 especies de aves según Parques Nacionales (UNESCO
consigna alrededor de 400)»*, citando a las dos. Si preferís una sola cifra, decime cuál.

---

## Datos que no se pudieron respaldar

### E1 · La leyenda de los dos amantes (Naipí y Tarobá)
Tu frase del guión —*«un arcoíris donde dos amantes todavía se encuentran»*— remite
claramente a la leyenda guaraní de Naipí y Tarobá: la serpiente M'Boi parte el río en
dos para castigarlos, y el arcoíris los vuelve a unir. **La coincidencia con tu texto es
exacta**, incluido el río que «se rompe en dos».

El problema es la fuente. La leyenda sólo aparece en material escolar, páginas de
turismo y el sitio de la Municipalidad de Puerto Iguazú. No encontré una versión
etnográfica o académica citable. Por la regla que fijaste, **no la incluí en la
información de la ficha**.

**Decidí vos:**
- (a) Dejarla afuera, como está ahora.
- (b) Incluirla presentada como leyenda popular, sin fuente académica, aclarándolo.
- (c) Si tenés una referencia etnográfica —Métraux, Cadogan, algún registro de
  literatura oral guaraní—, pasámela y la cito como corresponde.

---

## Traducciones pendientes de revisión

Las frases del guión se tradujeron buscando conservar el tono poético, no la
literalidad. **Todas necesitan tu lectura**, sobre todo el alemán, que es el idioma del
público de Heidelberg.

### E1
| | |
|---|---|
| **ES** (original) | Un río que se rompe en dos para caer, y en la caída, dicen, un arcoíris donde dos amantes todavía se encuentran. |
| **DE** | Ein Fluss, der entzweibricht, um zu stürzen, und im Sturz, so sagt man, ein Regenbogen, in dem zwei Liebende sich noch immer begegnen. |
| **EN** | A river that breaks in two in order to fall, and in the falling, they say, a rainbow where two lovers still meet. |

Dudas puntuales:
- «se rompe en dos» → *entzweibricht* es fuerte y algo literario. Alternativa más llana:
  *der sich teilt, um zu stürzen*. ¿Cuál preferís?
- «dicen» → *so sagt man* / *they say*: mantiene el tono de relato oral. Si querés algo
  más neutro, se puede sacar.

### Acto 1 · Heidelberg
El pacto entre el árbol y la golondrina está traducido en
`content/heidelberg.json`. Mismo pedido de revisión, con una duda:
- «Yo te voy a dar mi quietud» → *Ich schenke dir meine Stille*. *Stille* es silencio;
  *Ruhe* sería más «quietud/reposo». Me inclino por *Ruhe*, pero es tu texto.

---

## Textos trágicos marcados «(a confirmar)»

Tu Anexo marca como última versión de trabajo los textos trágicos de:

**Sur:** S1, S2, S3, S5, S10, S11, S12, S17
**Oeste:** O1, O2, O3, O5, O6, O7, O8

Están transcriptos tal cual los escribiste y no se van a tocar. Pero conviene cerrarlos
antes de que se investiguen y traduzcan: cada cambio posterior implica rehacer la
información trágica, sus fuentes y las dos traducciones.

---

## Decisiones que tomé y conviene que sepas

### La dirección de la página del árbol
`nido_lugares.json` no le da `slug` al origen. Le puse **`heidelberg`**, así que la
página es `/lugares/heidelberg/` y su QR es `qr/heidelberg.svg`. **Esta dirección ya
está grabada en el QR**: si querés otra (`/el-arbol/`, por ejemplo), hay que cambiarla
antes de imprimir.

### Las fichas sin contenido no dan 404
Los QR se imprimen ahora y las 34 fichas restantes llegan después. Para que ningún
código escaneado caiga en un error, el generador crea igual la página de cada lugar,
con el nombre, el viaje y el aviso «ficha en preparación». A medida que se completen,
el aviso desaparece solo.

### Los lugares «sólo trágicos» no están en la ruta dibujada
E10, S16 y S17 están marcados `soloTragico` en el JSON. La línea del vuelo los saltea
—no son escalas de la maravilla— y aparecen en el mapa únicamente como ✕ roja, en la
capa trágica. Si alguno debería estar en el recorrido, avisá.

---

## Contradicciones entre el guión y las fuentes (viaje Este)

Ninguna de estas se corrigió: el guión no se toca. Quedan acá para que decidas.

### E6 · La altura de la Cachoeira da Fumaça
El guión dice **«trescientos ochenta metros»**. ICMBio y el Ministerio de Turismo
de Brasil la dan en **unos 340 metros**, y la describen como la segunda cascada
más alta del país. La ficha dice 340 y cita la fuente; el guión sigue diciendo 380.

### E9 · Cuántos años estuvo ausente el yaguareté
El guión dice **«el primero en volver, en cien años»**. Parques Nacionales habla
de **«más de 70 años»** de ausencia en Corrientes: los primeros cachorros nacieron
en 2018 y en enero de 2021 una hembra con dos crías pasó a vivir en libertad plena.
La ficha usa la cifra de Parques Nacionales.

### E2 · Cuánto se quemó el Pantanal en 2020
Las fuentes difieren bastante: entre el 26 % y el 40 % del bioma según la
metodología. La ficha toma la cifra del Observatorio de la Tierra de la NASA
—unos 43.000 km², cerca del 28 %— por ser la mejor documentada. Si preferís otra,
decime.

---

## Fichas del Este que quedaron a medias

Tienen fotos y su frase del guión, pero **todavía no tienen información ni
fuentes**, porque no encontré respaldo institucional suficiente:

- **E5 · Bonito.** Las lagunas y cavernas de Bonito están repartidas en
  propiedades privadas y monumentos naturales municipales; no hay una ficha de
  ICMBio equivalente a la de un parque nacional. Hace falta buscar en la
  Secretaría de Medio Ambiente de Mato Grosso do Sul.
- **E10 · Bosque Atlántico.** El dato del guión —«de cada diez árboles que había,
  hoy queda uno»— coincide a grandes rasgos con lo que reportan SOS Mata
  Atlântica e INPE (alrededor del 12 % remanente), pero no pude confirmarlo en
  una publicación citable. Lo mismo con el desplazamiento de familias guaraníes
  por el avance de la soja, que necesita una fuente académica o de un organismo
  de derechos humanos, no de prensa.

---

## Viaje Sur · estado

Los 17 lugares tienen fotos con licencia libre. **Diez tienen información con
fuente**, todas de UNESCO salvo la Gran Barrera, que suma AIMS y un artículo de
*Nature* con DOI.

### Siete que quedaron con fotos pero sin información
No encontré todavía una fuente institucional con la que sostener el texto, y
prefiero dejarlos vacíos antes que improvisar:

**S1 Antártida** · **S2 Islas Georgias del Sur** · **S3 Cordillera de los
Andes** · **S4 Bosques de araucarias** · **S6 Estepa patagónica** ·
**S16 Bosques andino-patagónicos** · **S17 Sudeste australiano**

Ninguno es Patrimonio Mundial, que es de donde salió la mayor parte del material
del resto. Para estos hace falta ir a otras fuentes: SCAR y el Tratado
Antártico, BirdLife y la Lista Roja de la UICN para el albatros y el cóndor,
CONAF y Parques Nacionales para las araucarias y el huemul.

### Partes trágicas pendientes
Sólo está escrita la de la Gran Barrera. Faltan las de **S1, S2, S3, S5, S10,
S11, S16 y S17**. Varias de esas son las que tenías marcadas «(a confirmar)» en
el guión, así que conviene cerrarlas antes de que las investigue.

### El guión y las fuentes, sin contradicciones esta vez
- **S8** · «casi dos kilómetros» de cortina de agua: UNESCO dice que el Zambeze
  tiene más de dos kilómetros de ancho en ese punto. Coincide.
- **S12** · «cinco veces en ocho años»: exacto. AIMS y GBRMPA registran blanqueos
  masivos en 2016, 2017, 2020, 2022 y 2024.
- **S14** · «ya era selva cuando caminaban los dinosaurios»: UNESCO fecha el
  bosque de Gondwana entre 50 y 100 millones de años atrás, y los dinosaurios se
  extinguieron hace 66. El extremo más antiguo del rango se superpone. Se sostiene.
- **S11** · «un millón y medio de animales»: UNESCO dice dos millones de ñus más
  cientos de miles de gacelas y cebras, aunque en otro párrafo habla de «más de
  un millón». La ficha usa las cifras de UNESCO; el guión queda como está.

---

## Estado tras completar el Sur y empezar el Oeste

### Sur: los 17 cerrados
Los siete que faltaban ya tienen información y fuente: Antártida (British Antarctic
Survey y *Communications Earth & Environment*), Georgias del Sur (BirdLife y BAS),
cóndor (Ministerio de Ambiente y el Sistema de Información de Biodiversidad),
araucaria (Ministerio del Medio Ambiente de Chile y SIB), estepa patagónica
(Parques Nacionales), huemul (Parques Nacionales y SIB) y los incendios
australianos (WWF-Australia).

**Partes trágicas que siguen sin escribir: S5, S10 y S11.** Las tres están
marcadas «(a confirmar)» en tu guión, así que conviene que las cierres antes.

### Oeste: fotos en los ocho, información en tres
Con fuente: **O1** El Chaltén (UNESCO), **O3** Salinas Grandes (CONICET, la parte
del litio) y **O8** Secuoyas (Servicio de Parques Nacionales de EE.UU.).

Faltan información y fuente en **O2** Aconcagua, **O4** Cerro de los Siete
Colores, **O5** Páramo de Sumapaz, **O6** Laguna de Guatavita y **O7** Wirikuta,
y las partes trágicas de O1, O2, O5, O6 y O7.

Para esos hace falta: el Parque Provincial Aconcagua (Mendoza), la Quebrada de
Humahuaca como sitio UNESCO, el Instituto Humboldt para el páramo y el
frailejón, y fuentes etnográficas o del Estado mexicano para Wirikuta y el
pueblo wixárika. Son fuentes más dispersas que UNESCO.

### Más cifras del guión que resultaron exactas
- **S1** · el hielo que se rompe antes de que las crías aprendan a nadar: en 2022,
  cuatro de cinco colonias del mar de Bellingshausen perdieron toda la cría.
- **S3** · «un cebo que era para otro»: en Mendoza, 2018, murieron 34 cóndores
  por un solo cadáver envenenado para matar depredadores del ganado.
- **S4** · araucarias «de más de mil años»: se midieron ejemplares de 1.021 años.
- **S17** · «tres mil millones de animales»: casi tres mil millones, según WWF.
- **O8** · «casi una de cada cinco»: entre el 13 % y el 19 % de las secuoyas
  grandes del mundo murieron en los incendios de 2020 y 2021.

### Fotos que no ilustran lo que dicen
Dos quedaron marcadas en el epígrafe como lo que realmente son, porque no
encontré con licencia libre la planta en su lugar de origen:
- **E3** · la *Victoria amazonica* está fotografiada en cultivo, no en el Amazonas.
- **O7** · el peyote está fotografiado en maceta, no en Wirikuta.

---

## Oeste completo, con una contradicción seria

Los ocho lugares tienen ya información con fuente. Pero apareció algo que **no
puedo resolver yo**.

### O2 · Aconcagua — RESUELTO

Mi objeción anterior estaba mal planteada. Eran **dos cosas distintas que
pasaron casi a la vez**, y yo las había mezclado:

1. **El parque creció.** En 2024 una ley actualizó la zonificación del Parque
   Provincial Aconcagua y **amplió** el área protegida un 21 %, de 67.438 a
   85.699 hectáreas, sumando zonas como la Quebrada de Matienzo.
2. **Y en el mismo corredor se habilitó una mina.** El proyecto San Jorge —un
   pórfido de cobre con oro, a cielo abierto, en la estancia Yalguaraz, distrito
   de Uspallata, **departamento de Las Heras, el mismo del parque**, unos 37 km
   al norte de Uspallata— había sido **rechazado por la Legislatura en 2011**. En
   **2025 la Legislatura aprobó su Declaración de Impacto Ambiental**, ratificada
   por la **Ley provincial 9684**.

Tu lectura era la correcta: la ley votada existe y es de 2025. Lo único que no
se sostiene es que le quite protección *al parque*, porque el parque se amplió.
La ficha ahora cuenta las dos cosas y cita las dos leyes.

**Si querés, podés dejar tu frase como está** —«una ley que le quita protección»
funciona como síntesis poética de lo que pasa en la zona— **o ajustarla** a algo
como «votar una ley que deja entrar las máquinas». Es tu texto; la ficha ya
aporta el dato preciso.

### Lo que sí dio exacto en el Oeste
- **O6** · «una herida abierta en el borde: la cortaron para vaciarla». Desde 1580
  los encomenderos intentaron desaguar la laguna de Guatavita. Antonio de
  Sepúlveda, con quien la Corona había firmado un acuerdo en 1562, hizo un
  segundo intento con instrumentos construidos para eso y sacó una esmeralda
  asentada en los libros reales. El corte todavía se ve.
- **O7** · «minas pedidas sobre la tierra sagrada». Las concesiones mineras sobre
  Wirikuta están documentadas por el INAH y fueron parte de lo que motivó la
  postulación del sitio ante la UNESCO.
- **O5** · «pudrirse de pie, comido por larvas y hongos que el calor dejó subir».
  El Instituto Humboldt viene registrando un daño extraño en los frailejones,
  con el aumento de temperatura del páramo como hipótesis principal.

### Pendiente menor
**O4** · la geología del cerro de los Siete Colores —«millones de años de mar, de
barro y de hierro apilados en capas»— no la pude respaldar: UNESCO describe la
Quebrada de Humahuaca por su valor cultural, no geológico. La ficha cuenta la
quebrada y el Camino Inca. Para las capas haría falta SEGEMAR.

---

## Traducciones · las 51 frases del guión

**Todas las frases del guión están ahora en los tres idiomas**, incluidas las 19
partes trágicas y los textos de apertura y cierre de cada acto. **Todas necesitan
tu lectura**, especialmente el alemán.

Las traduje buscando conservar el tono, no la literalidad. Dudas concretas:

- **«se rompe en dos»** (E1) → *entzweibricht*. Es fuerte y literario. Alternativa
  más llana: *der sich teilt*.
- **«el arca de Noé, ardiendo»** (E2) → *Die Arche Noah, brennend*. En alemán el
  participio solo suena casi como un titular. Se podría decir *die brannte*.
- **«blanco como el fuego de las estrella»** (S1) → mantuve el singular raro de
  «estrella» como *das Feuer der Sterne*, que lo normaliza. Si el singular es
  deliberado, decime y lo dejo raro también en alemán.
- **«la puerta negra»** (cierre del Oeste) → *das schwarze Tor*. Si es una
  referencia a algo concreto, puede necesitar otra palabra.
- **«caminatas de poder»** y **«ríos voladores»** (O5) → traduje *ríos voladores*
  literal, *fliegende Flüsse* / *flying rivers*, porque es el término que usan los
  hidrólogos. Confirmame si en tu texto significa eso.
- **«Maradooó»** y las onomatopeyas no aparecen en las fichas, pero si las usás en
  el sitio hay que decidir si se traducen o no.

### Lo que todavía está sólo en castellano
Los párrafos de información, los epígrafes de las fotos y los nombres de las
fuentes. Son unas diez mil palabras por idioma. Las frases del guión, que son la
obra, ya están.

---

## Cierre: los 44 lugares, completos

Las 19 partes trágicas están escritas y los 44 lugares tienen fotos, información
y fuentes. Quedan dos cosas donde el guión y las fuentes no coinciden del todo,
y las dos las decidís vos.

### S5 · El Perito Moreno es la excepción, no el ejemplo
Tu frase dice: *«Vi el hielo —el mismo hielo que te dije que era hermoso—
derretirse más rápido que nunca»*.

El dato es real pero apunta al vecindario, no al glaciar. Entre 2000 y 2012 los
glaciares del Campo de Hielo Patagónico Sur perdieron en promedio **casi un
metro de espesor por año**. Pero **el Perito Moreno es una de las pocas
excepciones**: se mantuvo estable mientras casi todos los demás retrocedían.

La ficha lo cuenta así, con la aclaración. Si en la obra te interesa que el
hielo que se derrite sea exactamente el que la golondrina acaba de nombrar,
quizá convenga que la frase diga «el hielo de alrededor» o que el acto trágico
mire al Upsala o al Viedma, que sí retroceden fuerte.

### O2 · La frase del Aconcagua, ajustada
Me pediste ajustarla y lo hice, con el cambio más chico posible:

| | |
|---|---|
| **Antes** | Y vi a los hombres votar una ley **que le quita protección**, para que las máquinas puedan llegar más cerca. |
| **Ahora** | Y vi a los hombres votar una ley para que las máquinas puedan llegar más cerca. |

Saqué sólo la parte que las fuentes contradicen —el parque no perdió
protección, se amplió un 21 %— y dejé intacto lo demás: la ley existe, es la
**9684 de 2025**, y es la que habilita la mina de cobre a cielo abierto en
Uspallata, el mismo departamento del parque. El ritmo de la frase no cambia.

Está traducida a los tres idiomas. **Si preferís la versión original, se vuelve
en un minuto.**

---

## "Lo que también vio" en los lugares que no lo tenían

Eran 25 sin el apartado. **Quedaron 15 escritos; faltan 10.**

La fuente principal es la **Perspectiva del Patrimonio Mundial de la UICN**, que
evalúa cada sitio con una metodología uniforme y una categoría explícita. Las
evaluaciones usadas son las del ciclo cerrado el 11 de octubre de 2025. Las
fuentes van **dentro del panel**, debajo del texto, como pediste.

### Dos donde la noticia es buena, y lo dice así
No todo lugar tiene una catástrofe. En estos dos la UICN evalúa el estado como
**bueno**, y la ficha lo dice en esos términos en vez de forzar un drama:

- **S9 · Namib** — su propia inhospitalidad lo protege: casi no hay caminos ni
  instalaciones. Lo que requiere manejo es el agua de los pocos ríos
  estacionales.
- **S15 · Uluru** — los valores están en buen estado y la protección se
  considera muy eficaz. Tierra de propiedad aborigen, manejada en conjunto y
  guiada por el Tjukurpa.

**Si preferís que estos dos no lleven el apartado, se sacan.** Me pareció más
honesto decir que están bien que inventarles una amenaza.

### Hallazgos que dialogan con tus frases
- **E1** · la amenaza mayor de Iguazú son **las represas aguas arriba**, que
  alteran el caudal. El río que se rompe en dos para caer está siendo regulado
  antes de llegar.
- **S7** · además de la mortandad creciente de ballenas francas, la **gripe
  aviar H5N1** provocó una mortandad masiva de elefantes marinos.
- **S8** · la sequía de 2019-2020, una de las peores en un siglo, **redujo
  drásticamente el agua que caía** por las cataratas Victoria.
- **OV8** · el mangle **sundri**, el que le da nombre a los Sundarbans, está hoy
  en peligro a escala global.

### Los 10 que faltan
No son Patrimonio Mundial natural, así que no tienen evaluación de la UICN y hay
que buscarlos uno por uno en fuentes dispersas:

**E4** Lençóis · **E5** Bonito · **E6** Cachoeira da Fumaça · **E9** Iberá ·
**S6** Estepa patagónica · **O4** Cerro de los Siete Colores ·
**OV4** Gobi · **OV5** Zumaia · **OV6** Delta del Ebro · **OV7** Dolomitas

Para esos hace falta ICMBio, Imasul, Parques Nacionales, el Geoparque de la
Costa Vasca, la Generalitat y la Fundación Dolomitas Patrimonio Mundial.

---

## Cuatro actos o cinco · resuelto

Lo dejo anotado porque hubo un cambio real. La sinopsis que mandaste dice, en castellano
y en alemán, que la obra es **en cinco actos**: *invierno, primavera, verano, otoño,
invierno*. La ficha de NIDO en la web de negra40, en cambio, decía «cuatro actos
—invierno, primavera, verano, otoño—»: eso lo había escrito yo a partir de los documentos
viejos del proyecto.

Como me pasaste el mismo texto dos veces con cinco actos, **tomé tu versión como la buena
y alineé la ficha de negra40**, en castellano y en inglés. `content/obra.json` ya la tenía
así. Si el cambio no era intencional, decímelo y lo vuelvo atrás en los dos lugares.

El mapa no se toca en ninguno de los dos casos: los vuelos son tres.

### Un nombre incompleto
En la ficha técnica, **Video: Andrés** quedó sin apellido, tal como me lo pasaste.

---

## Los últimos cuatro: E4, E5, O4 y OV5

Cerrados. Los 44 lugares tienen ahora «Lo que también vio», todos con fuente oficial
a la vista. Lo que conviene que sepas de estos cuatro:

**E4 · Lençóis Maranhenses.** La UICN publicó su primera evaluación del sitio en octubre
de 2025, un año después de la inscripción: «bueno, con algunas preocupaciones», pero con
la amenaza general en nivel **alto**. Lo más fuerte lo dice el propio expediente de
nominación: los parques eólicos del borde oriental de la zona de amortiguación se
levantaron **sin** el estudio de impacto ambiental que exige la ley federal brasileña.
Eso está citado tal cual, sin adjetivos míos.

**E5 · Bonito.** Todo sale del plan de manejo del Imasul. El dato del cupo —225 visitantes
por día desde 1995, guía obligatorio desde 1993— es verificable y es, me parece, lo más
interesante: el límite no se calcula por metros cuadrados sino por **temperatura del aire**
dentro de la cueva.

**O4 · Cerro de los Siete Colores.** Dos cosas. La primera: whc.unesco.org me bloqueó otra
vez con una verificación anti-bots, así que **no pude leer los informes de estado de
conservación de UNESCO** sobre la Quebrada (el del tren Jujuy–La Quiaca, entre otros).
Quedan pendientes si te interesan; habría que abrirlos a mano. La segunda: fui por otro
lado y apareció algo mejor para tu frase. El cerro era privado; se volvió público en 2019
porque los dueños quisieron cerrarlo, y la provincia expropió unas 149 hectáreas. Y un
trabajo de investigadores del CONICET señala que la declaratoria protege al cerro **no por
la roca sino como escenario de procesos históricos** — justo lo contrario de lo que mira
la golondrina. Lo dejé escrito así porque la tensión es real y está documentada.

**OV5 · Zumaia.** Confirmado en la Comisión Internacional de Estratigrafía: Zumaia tiene
**dos** «clavos de oro» (Selandiense y Thanetiense, ratificados en 2008). El decreto vasco
de 2009 protege expresamente los procesos de erosión, no sólo la roca.

### Una trampa que esquivé
Buscando la geología del cerro de los Siete Colores, una fuente me devolvió una
descripción —«tobas triásicas alteradas»— que corresponde a **otro** cerro Siete Colores,
el de Mendoza. No la usé. Es el mismo tipo de homonimia que ya nos había pasado con la
Cachoeira da Fumaça.

### Lo que sigue pendiente de traducción
Los párrafos de información y los epígrafes de las fotos siguen sólo en castellano. Las 51
frases del guión sí están en los tres idiomas.

---

## Traducción completa · los tres idiomas

Ya no queda castellano sin traducir. Los 44 lugares tienen en alemán y en inglés los
párrafos de información, el bloque «Lo que también vio» y los epígrafes de las fotos.
Las 51 frases del guión ya lo estaban.

**Lo traduje yo, no una máquina.** Conviene que alguien que hable alemán le dé una
pasada, sobre todo a los términos técnicos: los nombres de especies, las figuras de
protección (Biotopo Protegido → *Geschütztes Biotop*, Monumento Natural → *Naturdenkmal*)
y las categorías de la UICN, que traduje de forma consistente pero que tienen
equivalentes oficiales en alemán que quizá convenga usar tal cual.

### Los nombres de los lugares también cambian de idioma
Agregué un campo `names` en `nido_lugares.json` con el nombre de cada lugar en alemán y
en inglés: «Serengueti» ahora es *Serengeti*, «Cataratas del Iguazú» es *Iguazú Falls*.
Cambian el título de la ficha, el listado de cada viaje y los rótulos del mapa, que se
reescriben al vuelo cuando tocás el selector de idioma.

**Los ids, los slugs y las coordenadas no se tocaron**, y lo verifiqué contra el commit
anterior antes de publicar: son los que están impresos en los QR del afiche. Los 46 QR
siguen llegando a una página que existe.

### Decisiones de traducción que podés querer revisar
- Dejé en castellano los nombres propios que funcionan como tales en cualquier idioma:
  *Pantanal*, *Salinas Grandes*, *Cerro de los Siete Colores*, *El Chaltén*, *Wirikuta*.
- El título de cada página (la pestaña del navegador) quedó en castellano en los tres
  idiomas. Es un solo texto por página y no cambia con el selector; me pareció preferible
  a inventar un mecanismo aparte.
- «Lo que también vio» quedó como *Was sie außerdem sah* / *What it also saw*, que ya
  estaba definido en `site.json`.

---

## El afiche A0 · los 46 QR puestos y verificados

Encontré dos cosas al abrir el afiche:

1. **Los QR nunca se habían colocado.** Donde van los códigos había recuadros
   punteados vacíos, uno por lugar, con su id (`qr-E1`, `qr-E2`…). Los 46 archivos
   existían en `qr/`, pero el afiche no los tenía adentro.
2. **El índice se había quedado en 35 lugares**, de cuando el mapa no tenía todavía
   el grupo «Otros vuelos».

Ahora el índice se genera con `afiche.py` desde el mismo `nido_lugares.json` que usa
el sitio, igual que los QR. Son 44 lugares en seis columnas, más un bloque nuevo
«Para empezar» abajo a la derecha con el código del mapa completo y el del árbol.
El planisferio, el detalle de Sudamérica y las referencias no se tocaron: eso está
dibujado a mano y se respeta.

**Verificación:** rasterizé los 46 códigos tal como quedaron incrustados en el afiche
y los volví a leer con un decodificador. Los 46 decodifican, y los 46 coinciden con la
URL que les corresponde en `qr/indice.csv`. Está en `verificar-qr.html`, para que se
pueda repetir antes de mandar a imprenta. Comprobar que el archivo existe no sirve:
lo que importa es que el código impreso lleve adonde tiene que llevar.

**Tamaño:** el QR más denso tiene 45 módulos de lado. A 24 mm da 0,53 mm por módulo,
por encima del mínimo de 0,4 mm que pide la imprenta. Los dos de navegación van a 32 mm.

### Tres cosas que quedan abiertas

**El planisferio no dibuja los nueve de «Otros vuelos».** El índice ahora los lista,
pero en el mapa no aparecen ni ellos ni su recorrido. Hay que decidir si se agregan
—habría que deducir la proyección del dibujo, que no tiene script— o si el mapa se
queda con los tres vuelos de la obra y el bloque OV del índice lleva una nota que lo
aclare. **No lo resolví por mi cuenta.**

**El ✕ quedó desactualizado.** Marca los lugares donde «lo que también vio» son malas
noticias, y está puesto en 19 de los 44. Pero los nueve de «Otros vuelos» no lo tienen
ninguno, y varios sí son malas noticias: el Baikal, los Sundarbans, el delta del Ebro.
Al revés, hay lugares donde la noticia es buena —Namib, Uluru— y ahí el ✕ no
correspondería. Es una marca de contenido, no mía: decime cuáles llevan ✕ y lo ajusto
en `nido_lugares.json`, que es de donde lo toman el mapa web y el afiche.

**Los PDF quedaron viejos.** `NIDO_mapa_A0.pdf` y `NIDO_mapa_A0_color.pdf` siguen
teniendo el índice de 35 recuadros vacíos. En esta máquina no hay conversor de SVG a
PDF. El SVG es el archivo bueno; el PDF hay que rehacerlo antes de imprimir.

### El planisferio ya dibuja «Otros vuelos»

Resuelto. Los nueve lugares y su recorrido están ahora sobre el planisferio, con
su línea punteada violeta y su fila en las referencias.

Para poder dibujarlos había que saber la proyección, y el script del planisferio
no quedó en el repositorio. La respuesta estaba a la vista, en el pie de las
propias referencias del afiche: **Equal Earth**. El resto salió de la retícula
dibujada —el ecuador va de x=28 a x=818, el centro en (423, 272)—.

`planisferio.py` verifica esa reconstrucción en cada ejecución contra los 15.845
vértices de la costa dibujada: el error es de **0,001 mm** sobre un pliego de
1189 mm. Como control independiente, el marcador de Heidelberg —que no
interviene en el cálculo— queda a 0,006 mm del que ya estaba. Si alguna vez se
redibuja el planisferio, el control falla en vez de poner los puntos mal.

El orden del recorrido es el mismo que usa el mapa web: de oeste a este
(Zumaia, Ebro, Dolomitas, Saimaa, Sundarbans, Jiuzhaigou, Gobi, Baikal, Mulu),
saliendo del árbol y volviendo a él, por arcos de círculo máximo.

Queda pendiente de tu ojo: la ubicación de las nueve etiquetas. Las puse con una
regla simple —a la derecha del punto, salvo cuatro en Europa que van a la
izquierda— y revisé que no se pisen, pero es justo el tipo de ajuste fino que
conviene hacer con el diseño delante.

---

## El afiche en alemán

`idioma_afiche.py` genera `NIDO_mapa_A0_de.svg` y `NIDO_mapa_A0_color_de.svg` a
partir de los castellanos. **Sólo cambia el texto**: lo verifiqué comparando los
dos archivos con los nodos de texto vaciados, y la geometría es idéntica byte a
byte. Los 46 códigos QR son los mismos, porque la dirección de cada ficha sirve
para los tres idiomas: por eso alcanza con imprimir un solo juego de códigos.

Las frases que ya existían en el sitio salen de `content/site.json` —el
subtítulo, «Andere Flüge», «Was sie auch sah», «Punkt 0 · der Baum»— y los
nombres de los lugares, del campo `names` de `nido_lugares.json`. Lo propio del
afiche está traducido en el script, a la vista.

El script falla si queda algún texto sin traducir: un afiche a medio traducir no
sirve de nada.

**Medido, no mirado:** el alemán es más largo, así que comprobé en el navegador
el ancho real de cada texto. Ninguno desborda su columna del índice, ninguno se
sale del pliego, y no hay dos etiquetas del planisferio que se pisen. Lo mismo
en la versión castellana.

Traducciones que conviene que mire alguien de allá: «Zeichenerklärung» para
Referencias, «Ort, den sie sah», «Verzeichnis · Code scannen für mehr zu jedem
Ort» y el pie técnico de la proyección.

---

## Los PDF: cuatro archivos, A0 exacto, verificados

`pdf_afiche.py` convierte los SVG a PDF con Chrome en modo headless —el mismo
motor con el que vengo verificando el afiche en pantalla, así que lo que se ve
es lo que se imprime—. El SVG va incrustado en el HTML, no como `<img>`, para
que el texto llegue al PDF **como texto** y no como dibujo.

Los cuatro salen en 1189 × 841 mm, una sola página, con las fuentes incrustadas:
Palatino y Courier New, que son las que el afiche declara y que están instaladas
en esta máquina.

**Verificación de los QR sobre el PDF, no sobre el SVG.** Rastericé la franja
del índice de cada PDF con Core Graphics, recorté cada código por sus
coordenadas y lo decodifiqué: **46 de 46 en los cuatro archivos**, todos
apuntando a la URL que les corresponde. Es la prueba que importa, porque es el
archivo que va a imprenta. Se repite con `verificar-pdf.html`.

### Antes de mandar a imprenta
- El PDF es RGB. El taller va a pedir CMYK, sangrado y marcas de corte: eso se
  resuelve abriendo el SVG o el PDF en Illustrator.
- Aparecen dos tipografías de reserva, Times New Roman Italic y Menlo, para unos
  pocos glifos que Palatino y Courier no cubren. No lo vi romper nada, pero vale
  mirarlo con el archivo abierto.

---

## El afiche alemán ahora manda a las fichas en alemán

Hasta acá el afiche alemán llevaba los mismos códigos que el castellano, que no
fuerzan idioma: el sitio elegía según el navegador del visitante. Para alguien
parado frente a un afiche en alemán eso estaba mal — podía escanear y abrir la
ficha en castellano.

`qr.py` genera ahora **dos juegos de códigos**:

- `qr/` — sin idioma forzado, para el afiche castellano. **No cambiaron ni un
  byte**: lo verifiqué contra el commit anterior.
- `qr/de/` — con `?lang=de`, para el afiche alemán.

Las direcciones son ocho caracteres más largas pero los códigos siguen en 45
módulos, así que a 24 mm el módulo mide los mismos 0,53 mm de antes. Cada código
alemán entra exactamente en el recuadro que ocupaba el otro: la escala se
recalcula para que el índice no se mueva.

**Verificado sobre los cuatro PDF**, rasterizando y decodificando: los 46 del
castellano siguen apuntando a la dirección sin idioma, y los 46 del alemán a la
misma dirección con `?lang=de`.

También corregí `qr/de/indice.csv`, que listaba los nombres de los lugares en
castellano aunque fuera el índice alemán. Ahora usa los nombres en alemán.

### Lo que sigue en castellano, y por qué
La dirección misma: `/lugares/e1-cataratas-del-iguazu/?lang=de`. El *slug* es
castellano en los tres idiomas, a propósito — cada ficha vive en una sola
dirección y el idioma es una preferencia, no una página distinta. Es lo que
permite que un visitante cambie de idioma sin que se le rompa el enlace, y que
el afiche castellano y el alemán apunten a la misma ficha. Si preferís
direcciones en alemán habría que duplicar las 46 páginas, una por idioma; se
puede hacer, pero es otra arquitectura. Decime y lo vemos.

### Dos arreglos de camino
- `afiche.py` borraba los grupos buscando el primer `</g>`, que desde que los QR
  van incrustados cae dentro del índice y dejaba medio índice en pie. Ahora
  cuenta los grupos anidados.
- Validaba el resultado *después* de escribir el archivo. Ahora valida antes: si
  los códigos no están todos, no escribe nada.

---

## Los tres logos en el afiche

Abajo a la derecha, alineados al margen derecho (x=1161) y a la base del
índice: negra40, CEAC y el Völkerkundemuseum, en el mismo orden que en la web,
con el rótulo «Con» / «Mit» encima, alineado con el borde izquierdo de negra40.

Van a 9 mm de alto. Los archivos miden 120 px, así que impresos dan 339 ppp
—por encima de los 300 que pide una imprenta—. Comprobé además que los tres
PNG son **gris puro**, sin un solo píxel de color: por eso el mismo archivo
sirve para la versión en color y para la de blanco y negro, sin filtros.

Van incrustados en el SVG como datos, no enlazados, así que el archivo sigue
siendo autónomo: se abre en Illustrator sin perder las imágenes.

El rótulo se traduce solo, porque sale de `ui.con_apoyo` de `site.json`, que es
de donde lo toma también la web.

---

## Logos más grandes y archivos renombrados

Los logos pasaron de 9 a 14 mm de alto. La fila ocupa ahora 151 mm, alineada al
margen derecho (28 mm, el mismo que el resto del afiche) y 4 mm por encima de
la base del índice.

**Hay un techo de resolución y conviene que lo sepas.** Los tres archivos de
logo miden 120 px de alto. A 9 mm daban 339 ppp; a 14 mm dan **218 ppp**. Para
un A0, que se mira a un metro de distancia, 218 alcanza y en el PDF se ven
limpios —lo verifiqué rasterizando—. Pero están por debajo de los 300 ppp de
manual, y si querés agrandarlos más, ahí sí empieza a notarse.

La solución no es escalar el PNG: es conseguir los archivos vectoriales.
**El de negra40 ya lo tenés**: `NEGRA40/negra40_logo.pdf` es vector puro, 10 KB,
sin un solo píxel rasterizado. Los del CEAC y el museo habría que pedírselos a
las instituciones (un SVG, un EPS o un PDF vectorial). Con los tres en vector,
el tamaño deja de tener límite. Decime y los integro.

### Nombres de archivo
Los cuatro archivos finales empiezan ahora por `MAPA_FINAL`, con el idioma y la
versión a la vista:

| archivo | idioma | versión |
|---|---|---|
| `MAPA_FINAL_es_color` | castellano | color |
| `MAPA_FINAL_es_bn` | castellano | blanco y negro |
| `MAPA_FINAL_de_color` | alemán | color |
| `MAPA_FINAL_de_bn` | alemán | blanco y negro |

Cada uno en `.svg` y en `.pdf`. Los `NIDO_mapa_A0*` viejos se borraron para que
no quede ninguna duda sobre cuál es el bueno.

---

## Los logos: orden nuevo y tamaños equilibrados

Orden: Völkerkundemuseum a la izquierda, CEAC al centro, negra40 a la derecha.
Centrados sobre una misma línea horizontal, alineados al margen derecho.

**No van los tres a la misma altura, y es a propósito.** Igualar la altura era
justamente lo que hacía que negra40 pesara de más: es un logotipo ancho —4,7:1—
y los otros dos son sellos casi cuadrados, así que a igual altura cubría el
triple de superficie. Ahora cada uno se escala para igualar la raíz del área que
ocupa, que es la medida que más se parece a cómo el ojo compara dos marcas de
formas distintas:

| logo | factor | alto | ancho | ppp impresos |
|---|---|---|---|---|
| Völkerkundemuseum | 1,00 | 20,0 mm | 31,3 mm | 152 |
| CEAC | 0,75 | 15,0 mm | 41,6 mm | 203 |
| negra40 | 0,58 | 11,6 mm | 54,7 mm | 263 |

Respecto de antes, el museo creció un 43 % y el CEAC un 7 %; negra40 bajó un
17 %, que era el ajuste que pedía la vista.

### Por qué no pueden ser más grandes todavía
Los 20 mm del museo son el techo: con un archivo de 120 px eso da 152 ppp, que
a un metro —la distancia a la que se mira un A0— está justo en el límite de lo
que el ojo resuelve. Y acá la gente se va a acercar más que eso, porque va a
escanear códigos.

**Probé vectorizar los PNG con Adobe y no sirve.** El resultado pierde el
dibujo: en el sello del museo se empasta el edificio y desaparece el «VPST» del
frontón. Un archivo de 188 px no tiene detalle que trazar.

La única forma de agrandarlos más es conseguir los originales vectoriales.
**El de negra40 ya lo tenés**: `NEGRA40/negra40_logo.pdf` es vector puro, 10 KB.
Los del CEAC y del museo hay que pedírselos a las instituciones —un SVG, un EPS
o un PDF vectorial—. Con los tres en vector el tamaño deja de tener techo.

---

## El planisferio deja de ser una silueta

Tenía la costa y nada más. Ahora tiene relieve, hidrografía y nombres de mar.

**El relieve es real, no dibujado.** Es el sombreado de Natural Earth, que viene
en equirectangular —la cuadrícula cruda de latitud y longitud— mientras el
afiche está en Equal Earth. No alcanzaba con pegarlo: `relieve.py` invierte la
proyección y para cada uno de los 10,6 millones de píxeles de salida calcula a
qué punto de la Tierra corresponde. La inversa de Equal Earth no tiene fórmula
cerrada; la latitud auxiliar sale por Newton. Lo comprobé superponiendo la costa
ya dibujada sobre el relieve reproyectado: calzan.

Se ven los Andes, el Himalaya, las Rocosas, el Atlas, la Gran Cordillera
Divisoria, la fosa del Rift. El gris original se tiñe con los dos tonos del
afiche, así que el mapa no cambia de color.

**Ríos y lagos** salen del mismo Natural Earth: los 255 ríos de rango 1 a 5 —el
1 es el Amazonas— con el trazo más grueso cuanto más importante, y los 45 lagos
mayores.

**Los nombres de mar se ubican solos.** El centroide no servía: el del Pacífico
Norte cae sobre México. Cada nombre va en el punto del polígono más alejado de
cualquier costa, que es donde lo pondría un cartógrafo, y el cuerpo de letra se
ajusta al hueco disponible. Si un mar no tiene sitio para su nombre sin meterse
debajo de la tierra, no se escribe: leerlo cortado es peor que no ponerlo. Van
además por debajo de la capa de tierra, nunca encima.

Los nombres vienen traducidos en el propio Natural Earth, así que la versión
alemana no los traduce: los vuelve a generar. Afiche y dato oficial no se pueden
separar.

### Orden del canal
`qr.py` → `afiche.py` → `planisferio.py` → `expresividad.py` → `idioma_afiche.py`
→ `pdf_afiche.py`.

---

## Los 44 lugares, todos con nombre en el planisferio

Faltaban 23: los de Sudamérica, que sólo se nombraban en el recuadro de
detalle. Un punto sin nombre en el mapa grande obliga a buscarlo en otro lado.

`etiquetas.py` le busca sitio a cada uno probando posiciones en anillos cada vez
más amplios alrededor del punto, de más cerca a más lejos y prefiriendo los
costados, que es el orden en que lo haría un cartógrafo. Respeta lo que ya está:
las etiquetas puestas a mano, los nombres de mar y el recuadro de detalle. Si un
nombre queda a más de 7 mm de su punto, se le tira una línea de guía fina del
color de su viaje.

Salió mejor de lo que esperaba: de los 23, **21 entraron pegados a su punto** y
sólo 2 necesitaron línea de guía.

**Verificado midiendo, no mirando:** cero solapes entre los 60 textos del
planisferio, en castellano y en alemán.

Los rótulos no se traducen: se vuelven a calcular. Los nombres alemanes tienen
otro largo, así que las posiciones que sirven en castellano no tienen por qué
servir en alemán, y de hecho salen distintas.

---

## Animales: cuatro grabados del siglo XIX

Los mapas antiguos llevaban bichos dibujados donde se sabía que vivían. Acá hay
cuatro, y **los cuatro son animales que la obra nombra**: la golondrina que
cuenta la historia (Atlántico Norte, de camino a Heidelberg), el pingüino
emperador de la Antártida, el albatros errante de las Georgias y el camello
bactriano del Gobi.

Son grabados de la **Iconographia Zoologica**, en dominio público, bajados de
Commons con el mismo criterio que las fotos. Dominio público y no Creative
Commons a propósito: una licencia CC obliga a atribuir en el propio afiche, y un
pie de autor por bicho no entra en un mapa. Vienen fotografiados con su hoja de
montaje, así que `grabados_preparar.py` los recorta, les saca el papel y los pasa
a la tinta del afiche con un desvanecido ovalado, como las viñetas antiguas.

### Tres que descarté, y por qué
- **El cóndor andino.** La categoría *Vultur* de la colección son todos *Vultur
  monachus*, el buitre negro europeo. El cóndor es *Vultur gryphus* y no está.
  Poner el buitre como cóndor habría sido el mismo error que la Cachoeira da
  Fumaça de Mato Grosso.
- **El elefante**, que es una escena nocturna entera y no una figura que se
  pueda separar del fondo.
- **El canguro y la vicuña.** El canguro está fotografiado en diagonal con otros
  animales encima. La vicuña es pálida sobre un cielo pálido: al quitarle el
  fondo pierde la cabeza, y preferí no publicar un animal decapitado.

Si conseguís un grabado limpio de cóndor o de yaguareté, los sumo.

## La estética antigua, contenida
- **Orla de costa**: la banda de sombra que los mapas viejos dibujaban bordeando
  la tierra. Son tres trazos sobre la propia silueta, dibujados *antes* del
  relleno, así que sólo se ve la mitad que da al agua.
- **Agua un punto más cálida**: de #EAF1F5 a #E9EFEE, menos azul y más papel.
- **Nombres de mar** en itálica espaciada, que ya estaban.

Sin rosa de los vientos ni marco: elegiste la versión contenida.

## Estado
Los cuatro PDF pesan ahora unos 8,4 MB cada uno, por el relieve. Los 46 códigos
siguen verificados sobre los cuatro.

---

## Trece animales, dibujados en vez de pegados

**El problema era el método, no el tamaño.** Los grabados se trataban como
fotografías: se les quitaba el fondo por brillo y quedaba un parche de tono
pegado encima del mapa. Pero un grabado en talla dulce ya es un dibujo — el
gris lo hacen las rayas. Ahora se extrae la línea: se compara cada píxel con el
fondo local, estimado desenfocando mucho la lámina. Queda el trazo, y el papel,
el cielo y las manchas desaparecen solos porque forman parte de ese fondo.

De paso, eso rescató láminas que antes no servían. La vicuña, que es pálida
sobre cielo pálido, con el método viejo perdía la cabeza; ahora sale entera.

**Los trece, y el lugar donde la golondrina los vio:**

| grabado | lugar |
|---|---|
| golondrina común | el árbol de Heidelberg |
| flamenco | OV6 · delta del Ebro |
| pingüino emperador | S1 · Antártida |
| albatros errante | S2 · Georgias del Sur |
| vicuña | O3 · Salinas Grandes |
| tapir | E1 · Iguazú y E3 · Amazonas |
| pirarucú | E3 · Amazonas |
| guacamayo jacinto | E2 · Pantanal |
| carpincho | E2 · Pantanal |
| rinoceronte negro | S10 · delta del Okavango |
| elefante africano | S10 y S11 · Serengueti |
| camello bactriano | OV4 · desierto de Gobi |
| canguro | S14 y S17 · Australia |

Los trece están nombrados en la ficha de su lugar. Ninguno es decorativo.

### Dos trampas de nomenclatura
La colección usa nombres del siglo XIX y hay que mirar la lámina, no el título:
**Trichechus rosmarus es la morsa**, no el manatí del Amazonas, y **Harpyia
cephalotes es un murciélago**, no la harpía de Iguazú. Las dos las descarté.
Y los títulos tampoco avisan cuándo la lámina es un cráneo: las mejores de
*Rhinoceros bicornis* y *Tapirus americanus* lo eran, y hubo que mirarlas.

El cóndor andino sigue sin estar: la colección sólo tiene *Vultur monachus*, el
buitre negro europeo, y *Sarcoramphus papa*, el jote real. Ninguno es *Vultur
gryphus*.

## Color
El relieve pasó de la versión en gris a **Natural Earth 1**, que trae el color
del terreno: verdes de bosque, ocres de desierto, blanco de hielo. Se le baja la
saturación y se lo mezcla con el tono de papel del afiche, para que la selva se
note sin que el mapa cambie de familia de color.

## Verificado
Cero solapes entre los 60 textos y los 13 grabados, en los dos idiomas. Los 46
códigos siguen bien en los cuatro PDF, que ahora pesan 11,6 MB por el relieve en
color.
