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
