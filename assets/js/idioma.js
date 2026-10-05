/* Selector de idioma y panel "Lo que también vio".
 *
 * La misma dirección sirve para los tres idiomas: eso es lo que permite que un
 * solo QR impreso en el afiche funcione para cualquier visitante. El idioma
 * sale, en este orden, de ?lang=, de lo que eligió antes, o del navegador. */

(function () {
  var IDIOMAS = ['es', 'de', 'en'];
  var CLAVE = 'nido:lang';

  function elegir() {
    var pedido = new URLSearchParams(location.search).get('lang');
    if (IDIOMAS.indexOf(pedido) > -1) return pedido;

    try {
      var guardado = localStorage.getItem(CLAVE);
      if (IDIOMAS.indexOf(guardado) > -1) return guardado;
    } catch (e) { /* navegación privada: seguimos sin recordar */ }

    var navegador = (navigator.languages || [navigator.language || 'es']);
    for (var i = 0; i < navegador.length; i++) {
      var corto = String(navegador[i]).slice(0, 2).toLowerCase();
      if (IDIOMAS.indexOf(corto) > -1) return corto;
    }
    return 'es';
  }

  function aplicar(lang) {
    document.documentElement.setAttribute('data-lang', lang);
    document.documentElement.setAttribute('lang', lang);
    var botones = document.querySelectorAll('[data-set-lang]');
    for (var i = 0; i < botones.length; i++) {
      var activo = botones[i].getAttribute('data-set-lang') === lang;
      botones[i].setAttribute('aria-current', activo ? 'true' : 'false');
    }
    document.dispatchEvent(new CustomEvent('nido:idioma', { detail: lang }));
  }

  aplicar(elegir());

  document.addEventListener('click', function (ev) {
    var boton = ev.target.closest && ev.target.closest('[data-set-lang]');
    if (!boton) return;
    var lang = boton.getAttribute('data-set-lang');
    aplicar(lang);
    try { localStorage.setItem(CLAVE, lang); } catch (e) { /* idem */ }
  });

  // Panel trágico: oculto por defecto, se abre a pedido. Nunca de entrada.
  document.addEventListener('click', function (ev) {
    var boton = ev.target.closest && ev.target.closest('.abrir-tragico');
    if (!boton) return;
    var panel = document.getElementById(boton.getAttribute('aria-controls'));
    if (!panel) return;
    var abierto = boton.getAttribute('aria-expanded') === 'true';
    boton.setAttribute('aria-expanded', abierto ? 'false' : 'true');
    panel.hidden = abierto;
  });
})();
