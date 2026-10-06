/* Mapa de los tres vuelos.
 *
 * No hay mapa base comercial: la tierra es un GeoJSON de Natural Earth pintado
 * con los colores del afiche. Las rutas son arcos de círculo máximo, que es el
 * camino que de verdad haría un pájaro, calculados acá para no sumar otra
 * biblioteca. El cruce del antimeridiano se parte en dos tramos, si no el arco
 * cruzaría el mapa entero de lado a lado. */

(function () {
  var RAD = Math.PI / 180;

  function aCartesiano(p) {
    var la = p[1] * RAD, lo = p[0] * RAD, c = Math.cos(la);
    return [c * Math.cos(lo), c * Math.sin(lo), Math.sin(la)];
  }

  function aGrados(v) {
    return [Math.atan2(v[1], v[0]) / RAD,
            Math.atan2(v[2], Math.sqrt(v[0] * v[0] + v[1] * v[1])) / RAD];
  }

  /** Interpola el arco más corto sobre la esfera entre dos puntos [lon,lat]. */
  function circuloMaximo(a, b, pasos) {
    var A = aCartesiano(a), B = aCartesiano(b);
    var punto = A[0] * B[0] + A[1] * B[1] + A[2] * B[2];
    var d = Math.acos(Math.max(-1, Math.min(1, punto)));
    if (d < 1e-9) return [a, b];
    var out = [];
    for (var i = 0; i <= pasos; i++) {
      var f = i / pasos;
      var s1 = Math.sin((1 - f) * d) / Math.sin(d);
      var s2 = Math.sin(f * d) / Math.sin(d);
      out.push(aGrados([s1 * A[0] + s2 * B[0],
                        s1 * A[1] + s2 * B[1],
                        s1 * A[2] + s2 * B[2]]));
    }
    return out;
  }

  /** Parte la línea donde salta el antimeridiano y devuelve [[lat,lon],…] por tramo. */
  function tramos(puntos) {
    var salida = [], actual = [];
    for (var i = 0; i < puntos.length; i++) {
      if (i > 0 && Math.abs(puntos[i][0] - puntos[i - 1][0]) > 180) {
        salida.push(actual);
        actual = [];
      }
      actual.push([puntos[i][1], puntos[i][0]]);
    }
    if (actual.length > 1) salida.push(actual);
    return salida.filter(function (t) { return t.length > 1; });
  }

  function ruta(origen, lugares) {
    // La golondrina sale del árbol, pasa por los lugares en orden y vuelve.
    // Los `soloTragico` no están en el recorrido: aparecen sólo en la capa roja.
    var paradas = [origen].concat(
      lugares.filter(function (l) { return !l.soloTragico; })
             .map(function (l) { return [l.lon, l.lat]; })
    ).concat([origen]);

    var linea = [];
    for (var i = 0; i < paradas.length - 1; i++) {
      var arco = circuloMaximo(paradas[i], paradas[i + 1], 64);
      linea = linea.concat(i === 0 ? arco : arco.slice(1));
    }
    return tramos(linea);
  }

  function iniciar(datos, tierra) {
    var mapa = L.map('mapa', {
      // La tierra son más de mil polígonos. Dibujados como SVG, el navegador
      // mantiene un nodo del DOM por cada uno y los recalcula en cada zoom o
      // arrastre: se arrastra. En canvas se pintan de una sola pasada.
      preferCanvas: true,
      worldCopyJump: true,
      // Los tres vuelos abarcan 268° de longitud: en una pantalla angosta hace
      // falta llegar a zoom 1 para que entren enteros en el encuadre inicial.
      minZoom: 1,
      // Sin esto Leaflet sólo usa zooms enteros: si el 2 no entra por poco,
      // salta al 1 y el mundo queda a la mitad de tamaño, flotando en el
      // centro. Con el paso libre elige el zoom exacto que llena la caja.
      zoomSnap: 0,
      zoomDelta: 0.5,
      wheelPxPerZoomLevel: 120,
      maxZoom: 8,
      zoomControl: true,
      attributionControl: false,
    });

    L.geoJSON(tierra, {
      style: { fillColor: '#ECE5D3', fillOpacity: 1, color: '#B9AD92',
               weight: 0.6, interactive: false },
    }).addTo(mapa);

    var origen = datos.origin.c;
    var capas = {};
    var capaTragica = L.layerGroup().addTo(mapa);
    var todos = [];

    datos.trips.forEach(function (viaje) {
      var color = datos.color[viaje.key];
      var grupo = L.layerGroup().addTo(mapa);
      capas[viaje.key] = grupo;

      // "Otros vuelos" no es un recorrido: son lugares sueltos, fuera de la
      // obra. Se marcan en el mapa pero sin línea que los encadene.
      (viaje.sinRuta ? [] : ruta(origen, viaje.places)).forEach(function (tramo) {
        L.polyline(tramo, {
          color: color, weight: 2.2, opacity: 0.9,
          dashArray: datos.trazo[viaje.key], interactive: false,
        }).addTo(grupo);
      });

      viaje.places.forEach(function (lugar) {
        var pos = [lugar.lat, lugar.lon];
        todos.push(pos);
        var url = 'lugares/' + lugar.slug + '/';

        if (!lugar.soloTragico) {
          L.marker(pos, {
            icon: L.divIcon({
              className: '', iconSize: [13, 13], iconAnchor: [6.5, 6.5],
              html: '<div class="punto-lugar" style="width:13px;height:13px;' +
                    'background:' + color + '"></div>',
            }),
            keyboard: true,
            title: lugar.id + ' · ' + lugar.name,
            alt: lugar.id + ' · ' + lugar.name,
          }).bindTooltip(lugar.name, { direction: 'top', offset: [0, -8] })
            .on('click keypress', function () { location.href = url; })
            .addTo(grupo);
        }

        if (lugar.tragico || lugar.soloTragico) {
          // La ✕ va al lado del punto; sola, si el lugar es sólo trágico.
          var desp = lugar.soloTragico ? [7, 7] : [-3, 11];
          L.marker(pos, {
            icon: L.divIcon({
              className: '', iconSize: [14, 14], iconAnchor: desp,
              html: '<div class="marca-cruz">✕</div>',
            }),
            title: lugar.id + ' · ' + lugar.name,
            alt: lugar.id + ' · ' + lugar.name,
          }).bindTooltip(lugar.name, { direction: 'top', offset: [0, -8] })
            .on('click keypress', function () { location.href = url; })
            .addTo(capaTragica);
        }
      });
    });

    // Punto 0: el árbol.
    L.marker([origen[1], origen[0]], {
      icon: L.divIcon({
        className: '', iconSize: [19, 19], iconAnchor: [9.5, 9.5],
        html: '<div class="marca-cero" style="width:19px;height:19px"></div>',
      }),
      title: datos.origin.name,
      alt: datos.origin.name,
      zIndexOffset: 1000,
    }).bindTooltip(datos.origin.name + ' · ' + datos.origin.sub,
                   { direction: 'top', offset: [0, -11] })
      .on('click keypress', function () { location.href = 'lugares/heidelberg/'; })
      .addTo(mapa);

    todos.push([origen[1], origen[0]]);
    var limites = L.latLngBounds(todos).pad(0.02);
    mapa.fitBounds(limites);

    // El contenedor puede no tener su tamaño final cuando Leaflet arranca, y en
    // celular cambia al girar la pantalla. En ambos casos hay que recalcular el
    // tamaño y volver a encuadrar, o el mapa queda cortado.
    var reencuadrar = function () {
      mapa.invalidateSize({ animate: false });
      mapa.fitBounds(limites, { animate: false });
    };
    if (window.ResizeObserver) {
      var pendiente = null;
      new ResizeObserver(function () {
        clearTimeout(pendiente);
        pendiente = setTimeout(reencuadrar, 120);
      }).observe(document.getElementById('mapa'));
    } else {
      window.addEventListener('resize', reencuadrar);
    }
    requestAnimationFrame(reencuadrar);

    document.querySelectorAll('[data-viaje]').forEach(function (casilla) {
      casilla.addEventListener('change', function () {
        var g = capas[casilla.getAttribute('data-viaje')];
        if (casilla.checked) { mapa.addLayer(g); } else { mapa.removeLayer(g); }
      });
    });

    var capaCasilla = document.getElementById('capa-tragica');
    if (capaCasilla) {
      capaCasilla.addEventListener('change', function () {
        if (capaCasilla.checked) { mapa.addLayer(capaTragica); }
        else { mapa.removeLayer(capaTragica); }
      });
    }
  }

  Promise.all([
    fetch('assets/datos.json').then(function (r) { return r.json(); }),
    fetch('assets/geo/land.json').then(function (r) { return r.json(); }),
  ]).then(function (r) { iniciar(r[0], r[1]); })
    .catch(function (e) {
      document.getElementById('mapa').textContent = 'No se pudo cargar el mapa.';
      console.error(e);
    });
})();
