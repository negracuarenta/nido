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
