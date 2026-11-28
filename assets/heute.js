/* Gassi-Kompass: Tagesstatus zur Wald-Leinenpflicht. Die Ortssuche steht in suche.js.
   Ohne dieses Skript zeigen die Seiten die Regel neutral an (kein veralteter "Heute"-Text).
   Alle Texte stehen als JSON im Attribut data-texte, erzeugt von build.py aus der Tabelle TEXTE.
   Dieses Skript kennt keine Sprache. Weil es auf jeder Seite läuft, öffnet es am Ende auch die Zeilen vor dem Drucken. */
(function () {
  var DAY = 864e5;
  function mid(d) { return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function diff(a, b) { return Math.round((mid(b) - mid(a)) / DAY); }
  function md(s, y) { var p = s.split("-"); return new Date(y, +p[0] - 1, +p[1]); }

  var now = new Date(), t = mid(now), y = now.getFullYear();
  var schalt = (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
  var pos = (diff(new Date(y, 0, 1), t) + 0.5) / (schalt ? 366 : 365) * 100;

  document.querySelectorAll("[data-wald]").forEach(function (el) {
    var X = null;
    try { X = JSON.parse(el.getAttribute("data-texte")); } catch (e) { /* ohne Texte bleibt die Seite neutral */ }
    if (!X) return;
    function tage(n, form) { return n === 1 ? form[0] : form[1].replace("{n}", n); }
    var datum = el.querySelector("[data-heute-datum]");
    if (datum) {
      datum.textContent = X.datum.replace("{wt}", X.wt[now.getDay()])
        .replace("{t}", now.getDate() === 1 && X.erster ? X.erster : now.getDate() + X.punkt)
        .replace("{mon}", X.mon[now.getMonth()]).replace("{j}", y);
    }
    var track = el.querySelector(".track");
    if (track) {
      var m = document.createElement("div");
      m.className = "now" + (pos > 88 ? " r" : pos < 12 ? " l" : "");
      m.style.left = pos.toFixed(2) + "%";
      var s = document.createElement("span");
      s.textContent = X.heute;
      m.appendChild(s);
      track.appendChild(m);
    }
    if (el.getAttribute("data-saison") !== "1") return;
    var gross = el.querySelector("[data-heute-gross]"), text = el.querySelector("[data-heute-text]");
    if (!gross || !text) return;
    var von = md(el.getAttribute("data-von"), y), bis = md(el.getAttribute("data-bis"), y);
    if (t >= von && t <= bis) {
      var rest = diff(t, bis);
      gross.textContent = X.in_gross;
      gross.className = "big must";
      text.textContent = X.in_text + (rest === 0 ? X.letzter : X.noch.replace("{n}", tage(rest, X.tage)));
    } else {
      var naechste = t < von ? von : md(el.getAttribute("data-von"), y + 1);
      gross.textContent = X.aus_gross;
      gross.className = "big free";
      text.textContent = X.aus_text.replace("{j}", naechste.getFullYear())
        .replace("{n}", tage(diff(t, naechste), X.tagen));
    }
  });

})();

/* Drucken: Vor dem Druck gehen alle zugeklappten Zeilen (details) auf, danach wieder zu. So stehen auf dem Papier auch
   die Kantone der Themenseiten, die Punkte unter «Mehr» und die Quellenliste im Fuss. */
(function () {
  // Die Marke data-druck-zu hält fest, was vorher zu war. Kommt beforeprint zweimal (Chromium beim Speichern als PDF),
  // bleibt sie stehen, und nach dem Druck geht genau das wieder zu.
  window.addEventListener("beforeprint", function () {
    document.querySelectorAll("details:not([open])").forEach(function (d) {
      d.setAttribute("data-druck-zu", "");
      d.open = true;
    });
  });
  window.addEventListener("afterprint", function () {
    document.querySelectorAll("details[data-druck-zu]").forEach(function (d) {
      d.removeAttribute("data-druck-zu");
      d.open = false;
    });
  });
})();
