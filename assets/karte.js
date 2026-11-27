/* Karte der Hundezonen. Bis zum Klick auf «Karte laden» ruft die Seite nichts ab. Erst dann kommen das
   Kartenprogramm (Leaflet, liegt unter /assets/karte/), die Flächen (zonen.json) und die Kartenbilder von
   swisstopo. Das Skript kennt keine Sprache: Alle Texte kommen aus build.py im Attribut data-texte.
   Der Standort bleibt im Browser, die Seite sendet und speichert ihn nicht. */
(function () {
  'use strict';
  var wurzel = document.querySelector('[data-karte]');
  if (!wurzel) return;
  var T = JSON.parse(wurzel.getAttribute('data-texte'));
  var feld = wurzel.querySelector('[data-karte-feld]');
  var start = wurzel.querySelector('[data-karte-start]');
  var knopf = wurzel.querySelector('[data-karte-laden]');
  var status = wurzel.querySelector('[data-karte-status]');
  var info = wurzel.querySelector('[data-karte-info]');
  var ortKnopf = wurzel.querySelector('[data-karte-ort]');
  var wahl = wurzel.querySelectorAll('[data-karte-art]');
  var zeiger = document.querySelectorAll('[data-karte-zeige]');
  var ART = { 7: 'frei', 3: 'leine', 8: 'leine', 9: 'leine', 12: 'leine', 1: 'verbot' };
  // Graue swissTLM-Karte von swisstopo, abgeschwächt, damit die Flächen hervortreten
  var KACHELN = 'https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.swisstlm3d-karte-grau/default/current/3857/{z}/{x}/{y}.png';
  var ruhig = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var karte = null, gruppen = {}, formen = [], punkte = null, gewaehlt = null, ladung = null, grenzen = null;
  var wache = null, ortPunkt = null, ortKreis = null, ortGezeigt = false;

  function melde(text) { status.textContent = text; }
  function stand(s) { wurzel.setAttribute('data-stand', s); }

  function hole(tag, attribute) {
    return new Promise(function (ok, nein) {
      var el = document.createElement(tag);
      Object.keys(attribute).forEach(function (k) { el.setAttribute(k, attribute[k]); });
      el.onload = ok;
      el.onerror = function () { nein(new Error(attribute.src || attribute.href)); };
      document.head.appendChild(el);
    });
  }

  function farbe(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }

  function ring(flach) {
    var x = flach[0], y = flach[1], aus = [[y / 1e5, x / 1e5]];
    for (var i = 2; i < flach.length; i += 2) { x += flach[i]; y += flach[i + 1]; aus.push([y / 1e5, x / 1e5]); }
    return aus;
  }

  function stil(zone, stark) {
    var art = ART[zone], f = farbe('--k-' + art);
    return {
      renderer: stil.leinwand, color: f, fillColor: f,
      weight: stark ? 4 : (art === 'verbot' ? 1.5 : 2),
      fillOpacity: stark ? 0.6 : (art === 'leine' ? 0.3 : 0.45),
      dashArray: (zone === 8 || zone === 9 || zone === 12) && !stark ? '6 5' : null
    };
  }

  function zeigeInfo(z) {
    info.textContent = '';
    var kopf = document.createElement('h3'), regel = document.createElement('p');
    kopf.textContent = z.n;
    regel.textContent = T.zone[z.z];
    info.appendChild(kopf);
    info.appendChild(regel);
    if (z.b) {
      var bem = document.createElement('p');
      bem.className = 'karte-bem';
      bem.textContent = T.bemerkung + ': ' + z.b;
      info.appendChild(bem);
    }
    var zu = document.createElement('button');
    zu.type = 'button';
    zu.className = 'karte-zu';
    zu.textContent = T.schliessen;
    zu.addEventListener('click', function () { waehle(null); });
    info.appendChild(zu);
    info.hidden = false;
  }

  function waehle(form) {
    if (gewaehlt) gewaehlt.setStyle(stil(gewaehlt.zone.z, false));
    gewaehlt = form;
    if (!form) { info.hidden = true; return; }
    form.setStyle(stil(form.zone.z, true));
    form.bringToFront();
    zeigeInfo(form.zone);
  }

  function zeigeZone(form) {
    karte.fitBounds(form.getBounds().pad(0.6), { maxZoom: 17, animate: !ruhig });
    waehle(form);
  }

  function baue(daten) {
    var L = window.L;
    var el = document.createElement('div');
    el.className = 'karte-blatt';
    start.hidden = true;
    stand('bereit');  // gibt dem Feld seine Höhe, bevor das Kartenprogramm rechnet
    feld.insertBefore(el, info);
    karte = L.map(el, {
      attributionControl: false, fadeAnimation: false, zoomAnimation: !ruhig, markerZoomAnimation: !ruhig,
      inertia: !ruhig, minZoom: 11, maxZoom: 19
    });
    L.tileLayer(KACHELN, { minZoom: 11, maxZoom: 19, opacity: 0.6 }).addTo(karte);
    stil.leinwand = L.canvas({ padding: 0.3, tolerance: 8 });
    ['verbot', 'leine', 'frei'].forEach(function (art) { gruppen[art] = L.layerGroup().addTo(karte); });
    daten.zonen.forEach(function (z, i) {
      var form = L.polygon(z.g.map(function (teil) { return teil.map(ring); }), stil(z.z, false));
      form.zone = z;
      form.on('click', function (ereignis) {
        L.DomEvent.stopPropagation(ereignis);
        if (ART[z.z] === 'frei' && karte.getZoom() < 15) zeigeZone(form); else waehle(form);
      });
      formen[i] = form;
    });
    // Reihenfolge der Ebenen: Verbote zuunterst, Freilaufzonen zuoberst
    ['verbot', 'leine', 'frei'].forEach(function (art) {
      formen.forEach(function (form) { if (ART[form.zone.z] === art) form.addTo(gruppen[art]); });
    });
    // Freilaufzonen sind klein: Aus der Ferne steht an ihrer Stelle ein Punkt
    punkte = L.layerGroup();
    formen.forEach(function (form) {
      if (ART[form.zone.z] !== 'frei') return;
      var punkt = L.circleMarker(form.getBounds().getCenter(), { renderer: stil.leinwand, radius: 6, color: '#fff', weight: 2, fillColor: farbe('--k-frei'), fillOpacity: 1 });
      punkt.on('click', function (ereignis) { L.DomEvent.stopPropagation(ereignis); zeigeZone(form); });
      punkt.addTo(punkte);
    });
    var zeigePunkte = function () {
      var soll = karte.getZoom() < 15 && karte.hasLayer(gruppen.frei);
      if (soll && !karte.hasLayer(punkte)) punkte.addTo(karte);
      if (!soll && karte.hasLayer(punkte)) karte.removeLayer(punkte);
    };
    grenzen = L.featureGroup(formen).getBounds();
    karte.fitBounds(grenzen);
    // erst jetzt, damit die Punkte nach den Flächen auf die Karte kommen und über ihnen liegen
    karte.on('zoomend', zeigePunkte);
    karte.setMaxBounds(grenzen.pad(1));
    karte.on('click', function () { waehle(null); });
    Array.prototype.forEach.call(wahl, function (kasten) {
      var schalte = function () {
        var g = gruppen[kasten.getAttribute('data-karte-art')];
        if (kasten.checked) g.addTo(karte); else { karte.removeLayer(g); if (gewaehlt && ART[gewaehlt.zone.z] === kasten.getAttribute('data-karte-art')) waehle(null); }
      };
      kasten.addEventListener('change', function () { schalte(); zeigePunkte(); });
      schalte();
    });
    zeigePunkte();
    wurzel._karte = karte;  // für den Test und die Fehlersuche
    wurzel.setAttribute('data-flaechen', String(formen.length));
    ortKnopf.parentNode.hidden = false;
    melde(T.bereit);
  }

  function lade() {
    if (ladung) return ladung;
    stand('laedt');
    melde(T.laedt);
    knopf.disabled = true;
    ladung = Promise.all([
      window.L ? null : hole('link', { rel: 'stylesheet', href: '/assets/karte/leaflet.css' }),
      window.L ? null : hole('script', { src: '/assets/karte/leaflet.js' }),
      fetch(wurzel.getAttribute('data-daten')).then(function (a) { if (!a.ok) throw new Error('zonen'); return a.json(); })
    ]).then(function (teile) { baue(teile[2]); }).catch(function () {
      ladung = null;
      knopf.disabled = false;
      start.hidden = false;
      stand('fehler');
      melde(T.fehler);
      throw new Error('karte');
    });
    return ladung;
  }

  function ortAus() {
    if (wache !== null) navigator.geolocation.clearWatch(wache);
    wache = null;
    ortGezeigt = false;
    if (ortPunkt) { karte.removeLayer(ortPunkt); karte.removeLayer(ortKreis); ortPunkt = ortKreis = null; }
    ortKnopf.setAttribute('aria-pressed', 'false');
    ortKnopf.textContent = T.standort;
  }

  function ortAn() {
    if (!navigator.geolocation) { melde(T.standort_fehlt); return; }
    ortKnopf.setAttribute('aria-pressed', 'true');
    ortKnopf.textContent = T.standort_aus;
    wache = navigator.geolocation.watchPosition(function (p) {
      var L = window.L, wo = [p.coords.latitude, p.coords.longitude];
      if (!ortPunkt) {
        ortKreis = L.circle(wo, { radius: p.coords.accuracy, stroke: false, fillColor: farbe('--k-ort'), fillOpacity: 0.15, interactive: false }).addTo(karte);
        ortPunkt = L.circleMarker(wo, { radius: 7, color: '#fff', weight: 2, fillColor: farbe('--k-ort'), fillOpacity: 1, interactive: false }).addTo(karte);
      } else {
        ortKreis.setLatLng(wo).setRadius(p.coords.accuracy);
        ortPunkt.setLatLng(wo);
      }
      if (!ortGezeigt) {
        ortGezeigt = true;
        if (grenzen.pad(0.1).contains(wo)) { karte.setView(wo, Math.max(karte.getZoom(), 16)); melde(T.standort_da); }
        else melde(T.standort_aussen);
      }
    }, function () { ortAus(); melde(T.standort_fehlt); }, { enableHighAccuracy: true, maximumAge: 10000, timeout: 20000 });
  }

  knopf.hidden = false;
  knopf.addEventListener('click', function () { lade().catch(function () {}); });
  ortKnopf.addEventListener('click', function () { if (wache === null) ortAn(); else { ortAus(); melde(T.bereit); } });
  Array.prototype.forEach.call(zeiger, function (z) {
    z.addEventListener('click', function () {
      lade().then(function () {
        var form = formen[Number(z.getAttribute('data-karte-zeige'))];
        var art = ART[form.zone.z];
        Array.prototype.forEach.call(wahl, function (kasten) {
          if (kasten.getAttribute('data-karte-art') === art && !kasten.checked) { kasten.checked = true; gruppen[art].addTo(karte); }
        });
        feld.scrollIntoView({ block: 'center' });
        zeigeZone(form);
      }).catch(function () {});
    });
  });
})();
