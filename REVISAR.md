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
