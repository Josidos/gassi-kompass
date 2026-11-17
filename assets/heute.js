/* Gassi-Kompass: Tagesstatus zur Wald-Leinenpflicht. Die Ortssuche steht in suche.js.
   Ohne dieses Skript zeigen die Seiten die Regel neutral an (kein veralteter "Heute"-Text). */
(function () {
  var DAY = 864e5;
  var MON = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
  var WT = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
  function mid(d) { return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function diff(a, b) { return Math.round((mid(b) - mid(a)) / DAY); }
  function md(s, y) { var p = s.split("-"); return new Date(y, +p[0] - 1, +p[1]); }
  function fmt(d, mitJahr) { return d.getDate() + ". " + MON[d.getMonth()] + (mitJahr ? " " + d.getFullYear() : ""); }
  function tage(n) { return n === 1 ? "1 Tag" : n + " Tage"; }
  function tagen(n) { return n === 1 ? "1 Tag" : n + " Tagen"; }

  var now = new Date(), t = mid(now), y = now.getFullYear();
  var schalt = (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
  var pos = (diff(new Date(y, 0, 1), t) + 0.5) / (schalt ? 366 : 365) * 100;

  document.querySelectorAll("[data-wald]").forEach(function (el) {
    var datum = el.querySelector("[data-heute-datum]");
    if (datum) datum.textContent = WT[now.getDay()] + ", " + fmt(now, true);
    var track = el.querySelector(".track");
    if (track) {
      var m = document.createElement("div");
      m.className = "now" + (pos > 88 ? " r" : pos < 12 ? " l" : "");
      m.style.left = pos.toFixed(2) + "%";
      var s = document.createElement("span");
      s.textContent = "heute";
      m.appendChild(s);
      track.appendChild(m);
    }
    if (el.getAttribute("data-saison") !== "1") return;
    var gross = el.querySelector("[data-heute-gross]"), text = el.querySelector("[data-heute-text]");
    if (!gross || !text) return;
    var von = md(el.getAttribute("data-von"), y), bis = md(el.getAttribute("data-bis"), y);
    var wo = el.getAttribute("data-wo");
    if (t >= von && t <= bis) {
      var rest = diff(t, bis);
      gross.textContent = "Heute Leinenpflicht im Wald";
      gross.className = "big must";
      text.textContent = "Bis " + fmt(bis) + " gilt die Leinenpflicht " + wo + ". " +
        (rest === 0 ? "Heute ist der letzte Tag." : "Noch " + tage(rest) + ".");
    } else {
      var naechste = t < von ? von : md(el.getAttribute("data-von"), y + 1);
      gross.textContent = "Heute keine Leinenpflicht im Wald";
      gross.className = "big free";
      text.textContent = "Die Leinenpflicht " + wo + " gilt wieder ab " + fmt(naechste, true) +
        ", also in " + tagen(diff(t, naechste)) + ". Bis dahin muss dein Hund trotzdem unter Kontrolle bleiben, und Schilder vor Ort gehen vor.";
    }
  });

})();
