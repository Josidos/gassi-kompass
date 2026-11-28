// Quellenverzeichnis (/quellen/): Suchfeld, Wahl des Geltungsbereichs (Bund oder Kanton) und Sortierung nach Kanton
// oder Name, alles im Browser. Ohne Skript steht die ganze Liste nach Kanton geordnet da. Kennt keine Sprache:
// Die Texte der Statuszeile kommen als data-texte aus build.py. Ruft nichts ab.
// Übersicht: Ohne Wahl und ohne Suchwort steht je Kanton nur eine Zeile mit der Zahl seiner Quellen da. Ein Tipp
// auf die Zeile wählt den Kanton, ein zweiter führt zurück. Die ganze Liste wäre am Telefon rund 150 Bildschirme lang.
(function () {
  var wahl = document.querySelector('[data-quellen]');
  var liste = document.querySelector('[data-q-liste]');
  if (!wahl || !liste) return;
  var T = JSON.parse(wahl.getAttribute('data-texte'));
  var feld = document.getElementById('quellensuche');
  var status = document.getElementById('q-status');
  var alle = [].slice.call(liste.children);           // Reihenfolge nach Kanton, wie gebaut
  var quellen = alle.filter(function (li) { return li.classList.contains('q'); });
  var gruppen = alle.filter(function (li) { return li.classList.contains('q-gruppe'); });
  var kt = '', sort = 'kanton', zahl = {};
  quellen.forEach(function (li) { var k = li.getAttribute('data-kt'); zahl[k] = (zahl[k] || 0) + 1; });
  // Die Überschrift jedes Kantons wird ein Knopf mit der Zahl seiner Quellen.
  gruppen.forEach(function (li) {
    var h = li.querySelector('h2'), k = li.getAttribute('data-gruppe');
    var b = document.createElement('button'), name = document.createElement('span'), n = document.createElement('span');
    b.type = 'button';
    b.className = 'q-g';
    b.setAttribute('data-kt', k);
    name.textContent = h.textContent;
    n.className = 'q-g-zahl';
    n.textContent = zahl[k] === 1 ? T.g_eins : T.g_viele.replace('{n}', zahl[k] || 0);
    h.textContent = '';
    b.appendChild(name);
    b.appendChild(n);
    h.appendChild(b);
  });
  // wie such_norm() in build.py: klein, ohne Akzente, alles ausser Buchstaben und Ziffern als Leerzeichen
  function norm(s) {
    return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ß/g, 'ss')
      .replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function setze(text, n, m) { return text.replace('{n}', n).replace('{m}', m); }
  function zeige() {
    var woerter = norm(feld.value).split(' ').filter(Boolean);
    var n = 0, offen = {};
    var kurz = sort === 'kanton' && !kt && !woerter.length;  // Übersicht: nur die Zeilen der Kantone
    quellen.forEach(function (li) {
      var s = ' ' + li.getAttribute('data-s');
      var ok = (!kt || li.getAttribute('data-kt') === kt) &&
        woerter.every(function (w) { return s.indexOf(w) !== -1; });
      li.hidden = kurz || !ok;
      if (ok) { n++; offen[li.getAttribute('data-kt')] = true; }
    });
    gruppen.forEach(function (li) {
      li.hidden = sort !== 'kanton' || !offen[li.getAttribute('data-gruppe')];
      li.querySelector('button').setAttribute('aria-expanded', kurz ? 'false' : 'true');
    });
    liste.classList.toggle('q-kurz', kurz);
    var m = quellen.length;
    status.textContent = !n ? T.s_keine : n === m ? setze(T.s_alle, n, m) : n === 1 ? setze(T.s_eins, n, m) : setze(T.s_teil, n, m);
  }
  function ordne() {
    var reihe = sort === 'kanton' ? alle : quellen.slice().sort(function (a, b) {
      return a.getAttribute('data-n') - b.getAttribute('data-n');
    });
    reihe.forEach(function (li) { liste.appendChild(li); });
    if (sort === 'name') alle.forEach(function (li) { if (li.classList.contains('q-gruppe')) liste.appendChild(li); });
  }
  function druecke(gruppe, knopf) {
    [].forEach.call(wahl.querySelectorAll(gruppe), function (b) { b.setAttribute('aria-pressed', b === knopf ? 'true' : 'false'); });
  }
  wahl.addEventListener('click', function (ev) {
    var b = ev.target.closest('button');
    if (!b) return;
    if (b.hasAttribute('data-kt')) {
      kt = b.getAttribute('data-kt') === kt ? '' : b.getAttribute('data-kt');
      druecke('[data-kt]', wahl.querySelector('[data-kt="' + kt + '"]'));
    } else if (b.hasAttribute('data-sort')) {
      sort = b.getAttribute('data-sort');
      druecke('[data-sort]', b);
      ordne();
    }
    zeige();
  });
  // Tipp auf die Zeile eines Kantons: nur dieser Kanton. Noch ein Tipp: zurück zu allen.
  liste.addEventListener('click', function (ev) {
    var b = ev.target.closest('button.q-g');
    if (!b) return;
    kt = b.getAttribute('data-kt') === kt ? '' : b.getAttribute('data-kt');
    druecke('[data-kt]', wahl.querySelector('[data-kt="' + kt + '"]'));
    zeige();
    var li = b.closest('li');
    if (li.scrollIntoView) li.scrollIntoView({ block: 'start' });
  });
  feld.addEventListener('input', zeige);
  wahl.hidden = false;
  zeige();
})();
