// Steht in der Adresse die id eines details (Zeile einer Themenseite wie #kt-ag, Quellenliste im Fuss #quellen), wird es aufgeklappt, beim Laden und bei
// jedem Wechsel des Ankers. Ohne Skript bleiben die Zeilen zu und lassen sich von Hand öffnen. Kennt keine Sprache.
(function () {
  function auf() {
    var id = location.hash.slice(1);
    if (!id) return;
    try { id = decodeURIComponent(id); } catch (x) { return; }
    var d = document.getElementById(id);
    if (!d || d.tagName !== 'DETAILS') return;
    d.open = true;
    d.scrollIntoView();
  }
  // Lange Quellenliste im Fuss: am Telefon zu, am breiten Bildschirm von Anfang an offen.
  if (window.matchMedia && window.matchMedia('(min-width: 860px)').matches) {
    var breit = document.querySelectorAll('details[data-breit-offen]');
    for (var i = 0; i < breit.length; i++) breit[i].open = true;
  }
  auf();
  window.addEventListener('hashchange', auf);
})();
