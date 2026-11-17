/* Gassi-Kompass: Ortssuche (Gemeinde, Ort, Postleitzahl, Kanton) und Hinweis zum gewählten Ort.
   Alle Texte stehen als data-Attribute im HTML, dieses Skript kennt keine Sprache.
   Daten: /assets/orte.json, erzeugt von build.py aus data/orte.json. */
(function () {
  function norm(s) {
    return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/ß/g, "ss").replace(/[^a-z0-9]+/g, " ").trim();
  }

  /* Hinweis zum Ort. Die Suche hängt den Ort an die Adresse: /zh/#ort=Uster oder /schweiz/#kt=ag&ort=Wettingen.
     Der Name kommt aus der Adresse und wird deshalb nur als Text eingesetzt, nie als HTML. */
  var hin = document.querySelector("[data-ort-hinweis]");
  function zeigeHinweis() {
    var p = {};
    location.hash.replace(/^#/, "").split("&").forEach(function (teil) {
      var i = teil.indexOf("=");
      if (i < 1) return;
      try { p[teil.slice(0, i)] = decodeURIComponent(teil.slice(i + 1)).slice(0, 60); } catch (e) { /* ungültig */ }
    });
    var text = hin.getAttribute("data-text") || "", liste = hin.getAttribute("data-kantone"), ort = (p.ort || "").trim();
    if (liste) {
      var kanton = "";
      try { kanton = JSON.parse(liste)[p.kt] || ""; } catch (e) { /* ungültig */ }
      if (!kanton) { hin.hidden = true; return; }
      text = text.replace("{kanton}", kanton);
    } else if (!ort) { hin.hidden = true; return; }
    hin.textContent = "";
    if (ort) {
      var stark = document.createElement("strong");
      stark.textContent = ort + ":";
      hin.appendChild(stark);
      text = " " + text;
    }
    hin.appendChild(document.createTextNode(text));
    hin.hidden = false;
  }
  if (hin) {
    zeigeHinweis();
    /* Wechselt nur der Ort in der Adresse (Kantonswahl auf derselben Seite), zum Hinweis springen. */
    window.addEventListener("hashchange", function () {
      zeigeHinweis();
      if (!hin.hidden && hin.scrollIntoView) hin.scrollIntoView({ block: "center" });
    });
  }

  /* Suche */
  var box = document.querySelector("[data-suche]"), feld = document.getElementById("ortssuche");
  var liste = document.getElementById("treffer"), status = document.getElementById("such-status");
  if (!box || !feld || !liste || !status || !window.fetch) return;
  var MAX = 8, daten = null, laedt = false;
  function T(name) { return box.getAttribute("data-" + name) || ""; }
  box.hidden = false;

  function bereite(d) {
    var e = [], hatOrt = {}, nachName = {};
    d.k.forEach(function (k, i) {
      e.push({ n: T("kt") + " " + k[1], s: norm(k[1]), kz: k[0], k: i, g: -1, plz: "" });
    });
    d.o.forEach(function (o) {
      var g = d.g[o[2]], name = o[0] || g[0];
      e.push({ n: name, s: norm(name), plz: String(o[1]), g: o[2], k: g[1] });
      if (!o[0]) hatOrt[o[2]] = 1;
    });
    d.g.forEach(function (g, i) {
      nachName[g[0]] = i;
      if (!hatOrt[i]) e.push({ n: g[0], s: norm(g[0]), plz: "", g: i, k: g[1] });
    });
    var andere = [];
    Object.keys(d.a).forEach(function (getippt) {
      var i = nachName[d.a[getippt]];
      if (i !== undefined) andere.push({ s: getippt, x: { n: d.g[i][0], s: getippt, plz: "", g: i, k: d.g[i][1] } });
    });
    return { d: d, e: e, andere: andere };
  }

  function ziel(x) {
    var d = daten.d, k = d.k[x.k];
    if (x.g < 0) return { href: k[2] ? "/" + k[0] + "/" : "/schweiz/#kt=" + k[0], art: k[2] ? "kanton" : "bund" };
    var g = d.g[x.g], ort = encodeURIComponent(x.n);
    if (g[2]) return { href: g[2], art: "lokal" };
    if (k[2]) return { href: "/" + k[0] + "/#ort=" + ort, art: "kanton" };
    return { href: "/schweiz/#kt=" + k[0] + "&ort=" + ort, art: "bund" };
  }

  function suche() {
    var q = norm(feld.value);
    liste.textContent = "";
    if (!q) { status.textContent = ""; return; }
    if (!daten) { status.textContent = T("lade"); lade(); return; }
    var zahl = /^[0-9]/.test(q), roh = [];
    daten.e.forEach(function (x) {
      var r = -1;
      if (zahl) { if (x.plz && x.plz.indexOf(q) === 0) r = 0; }
      else if (x.s === q || x.kz === q) r = 0;
      else if (x.s.indexOf(q) === 0) r = 1;
      else if (x.s.indexOf(" " + q) !== -1) r = 2;
      else if (q.length >= 4 && x.s.indexOf(q) !== -1) r = 3;
      if (r >= 0) roh.push({ x: x, r: r });
    });
    if (!zahl && q.length >= 3) daten.andere.forEach(function (a) {
      if (a.s.indexOf(q) === 0) roh.push({ x: a.x, r: a.s === q ? 0 : 1 });
    });
    /* Gleicher Ort mit gleichem Ziel erscheint nur einmal, auch wenn er mehrere Postleitzahlen hat
       oder in mehrere Gemeinden hineinreicht. */
    var gesehen = {}, treffer = [];
    roh.forEach(function (t) {
      var x = t.x;
      t.z = ziel(x);
      var key = (zahl ? x.plz + "|" : "") + x.n + "|" + x.k + "|" + t.z.href;
      if (gesehen[key]) { if (x.plz && x.plz !== gesehen[key].x.plz) gesehen[key].mehr = true; return; }
      gesehen[key] = t;
      treffer.push(t);
    });
    var rang = { lokal: 0, kanton: 1, bund: 2 };
    treffer.sort(function (a, b) {
      return a.r - b.r || rang[a.z.art] - rang[b.z.art] || a.x.s.length - b.x.s.length ||
        a.x.n.localeCompare(b.x.n) || a.x.plz.localeCompare(b.x.plz);
    });
    if (!treffer.length) { status.textContent = T("leer"); return; }
    status.textContent = (treffer.length > MAX ? T("viele") : T("treffer"))
      .replace("{n}", treffer.length).replace("{max}", MAX);
    treffer.slice(0, MAX).forEach(function (t) {
      var x = t.x, a = document.createElement("a"), name = document.createElement("span"), unter = document.createElement("span");
      a.className = "dest " + (t.z.art === "bund" ? "wait" : "ok");
      a.href = t.z.href;
      name.className = "dest-name";
      name.textContent = (zahl ? x.plz + " " : "") + x.n;
      unter.className = "dest-sub";
      var teile = [];
      if (!zahl && x.plz && !t.mehr) teile.push(x.plz);
      if (t.z.art === "lokal" && daten.d.g[x.g][0] !== x.n) teile.push(T("gemeinde") + " " + daten.d.g[x.g][0]);
      if (x.g >= 0) teile.push(T("kt") + " " + daten.d.k[x.k][1]);
      teile.push(T(t.z.art));
      unter.textContent = teile.join(" · ");
      a.appendChild(name);
      a.appendChild(unter);
      liste.appendChild(a);
    });
  }

  function lade() {
    if (daten || laedt) return;
    laedt = true;
    fetch("/assets/orte.json").then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function (d) {
      daten = bereite(d);
      box.setAttribute("data-stand", "bereit");
      suche();
    }).catch(function () {
      laedt = false;
      status.textContent = T("fehler");
    });
  }

  feld.addEventListener("focus", lade);
  feld.addEventListener("input", suche);
  feld.addEventListener("keydown", function (ev) {
    if (ev.key !== "Enter") return;
    var erster = liste.querySelector("a");
    if (erster) { ev.preventDefault(); location.href = erster.href; }
  });
  if (feld.value) suche();
})();
