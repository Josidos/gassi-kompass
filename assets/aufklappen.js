// Themenseiten: Steht in der Adresse die id einer Zeile (#kt-ag), wird sie aufgeklappt, beim Laden und bei
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
  auf();
  window.addEventListener('hashchange', auf);
})();
