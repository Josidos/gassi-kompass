/* Gassi-Kompass: Suche (Gemeinde, Ort, Postleitzahl, Kanton, dazu Stichworte auf allen Seiten) und Hinweis
   zum gewählten Ort.
   Alle Texte stehen als data-Attribute im HTML, dieses Skript kennt keine Sprache.
   Daten: /assets/orte.json, erzeugt von build.py aus data/orte.json. Ein Verzeichnis für alle Sprachen:
   Ein Treffer führt auf die Seite in der Sprache der Startseite (data-lang), wenn es sie gibt,
   sonst auf die Fassung in einer anderen Sprache. Dann nennt der Treffer die Sprache.
   Stichworte: /assets/suche-<Sprache>.json, ebenfalls von build.py erzeugt, geladen beim ersten Tastendruck.
   Nichts wird an einen Server gesendet oder gespeichert: Gesucht wird im Browser. */
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
  var MAX = 8, daten = null, laedt = false, ortFehler = false;
  var LANG = box.getAttribute("data-lang") || "de";
  function T(name) { return box.getAttribute("data-" + name) || ""; }
  /* seiten: {Sprache: Adresse}. Liefert die Fassung in der Sprache der Seite, sonst die erste andere. */
  function waehle(seiten) {
    if (!seiten) return null;
    if (seiten[LANG]) return { href: seiten[LANG], l: LANG };
    for (var l in seiten) return { href: seiten[l], l: l };
    return null;
  }
  box.hidden = false;

  function bereite(d) {
    var e = [], hatOrt = {}, nachName = {};
    d.k.forEach(function (k, i) {
      /* Der Kanton ist unter seinem Namen in jeder Sprache zu finden, angezeigt wird die Sprache der Seite. */
      var name = T("kt").replace("{name}", k[2][LANG] || k[2].de), schon = {};
      for (var l in k[2]) {
        var s = norm(k[2][l]);
        if (schon[s]) continue;
        schon[s] = 1;
        e.push({ n: name, s: s, kz: k[0], k: i, g: -1, plz: "" });
      }
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
    var kt = waehle(k[1]);
    if (x.g < 0) return kt ? { href: kt.href, art: "kanton", l: kt.l } : { href: (T("schweiz") || "/schweiz/") + "#kt=" + k[0], art: "bund" };
    var g = d.g[x.g], ort = encodeURIComponent(x.n), lokal = waehle(g[2]);
    if (lokal) return { href: lokal.href, art: "lokal", l: lokal.l };
    if (kt) return { href: kt.href + "#ort=" + ort, art: "kanton", l: kt.l };
    return { href: (T("schweiz") || "/schweiz/") + "#kt=" + k[0] + "&ort=" + ort, art: "bund" };
  }

  function orte(q) {
    if (!q) return 0;
    if (!daten) { lade(); return -1; }
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
    treffer.slice(0, MAX).forEach(function (t) {
      var x = t.x, a = document.createElement("a"), name = document.createElement("span"), unter = document.createElement("span");
      a.className = "dest " + (t.z.art === "bund" ? "wait" : "ok");
      a.href = t.z.href;
      name.className = "dest-name";
      name.textContent = (zahl ? x.plz + " " : "") + x.n;
      unter.className = "dest-sub";
      var teile = [];
      if (!zahl && x.plz && !t.mehr) teile.push(x.plz);
      var kn = daten.d.k[x.k][2];
      if (t.z.art === "lokal" && daten.d.g[x.g][0] !== x.n) teile.push(T("gemeinde").replace("{name}", daten.d.g[x.g][0]));
      if (x.g >= 0) teile.push(T("kt").replace("{name}", kn[LANG] || kn.de));
      teile.push(T(t.z.art));
      if (t.z.l && t.z.l !== LANG) teile.push(T("in-" + t.z.l));
      unter.textContent = teile.join(" · ");
      a.appendChild(name);
      a.appendChild(unter);
      liste.appendChild(a);
    });
    return treffer.length;
  }

  /* Suche auf den Seiten. snorm() ändert die Länge nicht: Jedes Zeichen wird klein und ohne Akzent,
     alles ausser Buchstaben und Ziffern wird ein Leerzeichen. So zeigt eine Stelle im normierten Text
     auf dieselbe Stelle im Original, für Ausschnitt und Hervorhebung. */
  var sbox = document.getElementById("seitentreffer"), sliste = sbox && sbox.querySelector(".topics");
  var seiten = null, syn = [], sLaedt = false, sFehler = false;
  var ARTRANG = { thema: 0, bund: 1, kanton: 2, gemeinde: 3, ueber: 4 };
  function snorm(s) {
    var out = "";
    for (var i = 0; i < s.length; i++) {
      var c = s.charAt(i).toLowerCase().normalize("NFD").charAt(0);
      out += /[a-z0-9]/.test(c) ? c : " ";
    }
    return out;
  }
  /* Ein Wort der Eingabe und seine gleichbedeutenden Wörter aus der Liste in build.py. */
  function formen(w) {
    var f = [w];
    syn.forEach(function (g) {
      var passt = g.some(function (m) { return w.indexOf(m) === 0 || (w.length >= 5 && m.indexOf(w) === 0); });
      if (passt) g.forEach(function (m) { if (f.indexOf(m) < 0) f.push(m); });
    });
    return f;
  }
  /* Erste Stelle, an der ein Wort mit einer der Formen beginnt. hay beginnt mit einem Leerzeichen. */
  function stelle(hay, f) {
    var best = -1;
    f.forEach(function (x) { var i = hay.indexOf(" " + x); if (i >= 0 && (best < 0 || i < best)) best = i; });
    return best;
  }
  function markiert(el, text, alle) {
    var n = snorm(text), hay = " " + n, ab = [];
    alle.forEach(function (x) {
      var i = hay.indexOf(" " + x);
      while (i >= 0) {
        var ende = i + x.length;
        while (ende < n.length && n.charAt(ende) !== " ") ende++;
        ab.push([i, ende]);
        i = hay.indexOf(" " + x, i + 1);
      }
    });
    ab.sort(function (a, b) { return a[0] - b[0]; });
    var pos = 0;
    ab.forEach(function (r) {
      if (r[0] < pos) return;
      if (r[0] > pos) el.appendChild(document.createTextNode(text.slice(pos, r[0])));
      var m = document.createElement("mark");
      m.textContent = text.slice(r[0], r[1]);
      el.appendChild(m);
      pos = r[1];
    });
    if (pos < text.length) el.appendChild(document.createTextNode(text.slice(pos)));
  }
  function ausschnitt(text, i) {
    var start = i > 40 ? i - 40 : 0;
    if (start > 0) { var sp = text.indexOf(" ", start); start = sp >= 0 && sp < i ? sp + 1 : i; }
    var ende = start + 130;
    if (ende < text.length) { var sp2 = text.lastIndexOf(" ", ende); if (sp2 > start) ende = sp2; } else ende = text.length;
    return (start > 0 ? "… " : "") + text.slice(start, ende) + (ende < text.length ? " …" : "");
  }
  function seitenSuche(roh) {
    sliste.textContent = "";
    sbox.hidden = true;
    var woerter = [];
    snorm(roh).split(" ").forEach(function (w) { if (w && woerter.indexOf(w) < 0 && woerter.length < 6) woerter.push(w); });
    if (!woerter.length) return 0;
    if (!seiten) { ladeSeiten(); return -1; }
    var f = woerter.map(formen), alle = [].concat.apply([], f), treffer = [];
    seiten.forEach(function (s) {
      var summe = 0, rest = [];
      for (var j = 0; j < f.length; j++) {
        var ort = stelle(s.tn, f[j]) >= 0 ? 0 : -1;
        if (ort < 0) rest.push(f[j]);
        if (ort < 0 && s.b.some(function (b) { return stelle(b.hn, f[j]) >= 0; })) ort = 1;
        if (ort < 0 && s.b.some(function (b) { return stelle(b.xn, f[j]) >= 0; })) ort = 2;
        if (ort < 0) return;
        summe += ort;
      }
      /* Der Abschnitt mit den meisten Wörtern der Eingabe, bei Gleichstand der mit mehr Wörtern in der Überschrift.
         Wörter, die schon im Titel stehen, zählen dabei nicht. Der erste Abschnitt (Titel und Einleitung) nur,
         wenn kein anderer passt. */
      var fb = rest.length ? rest : f;
      var wahl = s.b[0], wz = 0, wk = 0, mit = 0;
      s.b.forEach(function (b, bi) {
        if (!bi) return;
        var z = 0, k = 0;
        fb.forEach(function (x) {
          var imKopf = stelle(b.hn, x) >= 0;
          if (imKopf) k++;
          if (imKopf || stelle(b.xn, x) >= 0) z++;
        });
        if (z) mit++;
        if (z > wz || (z === wz && k > wk)) { wahl = b; wz = z; wk = k; }
      });
      treffer.push({ s: s, r: summe, b: wahl, mit: mit });
    });
    treffer.sort(function (a, b) {
      return a.r - b.r || b.mit - a.mit || ARTRANG[a.s.a] - ARTRANG[b.s.a] || a.s.t.length - b.s.t.length;
    });
    treffer.slice(0, MAX).forEach(function (t) {
      var a = document.createElement("a"), name = document.createElement("span"), text = document.createElement("span");
      a.className = "topic";
      a.setAttribute("role", "listitem");
      a.href = t.s.u + (t.b && t.b.id ? "#" + t.b.id : "");
      name.className = "topic-name";
      markiert(name, t.s.t, alle);
      a.appendChild(name);
      if (t.b && t.b.h && t.b !== t.s.b[0]) {
        var ab = document.createElement("span");
        ab.className = "such-ab";
        markiert(ab, t.b.h, alle);
        a.appendChild(ab);
      }
      if (t.b && t.b.x) {
        text.className = "topic-text";
        var i = stelle(t.b.xn, alle);
        markiert(text, ausschnitt(t.b.x, i < 0 ? 0 : i), alle);
        a.appendChild(text);
      }
      sliste.appendChild(a);
    });
    sbox.hidden = !treffer.length;
    return treffer.length;
  }

  function suche() {
    var q = norm(feld.value);
    liste.textContent = "";
    if (sliste) { sliste.textContent = ""; sbox.hidden = true; }
    if (!q) { status.textContent = ""; return; }
    var n = orte(q), m = sliste ? seitenSuche(feld.value) : 0, teile = [];
    if (n < 0) teile.push(T(ortFehler ? "fehler" : "lade"));
    else if (n > 0) teile.push((n > MAX ? T("viele") : T("treffer")).replace("{n}", n).replace("{max}", MAX));
    if (m < 0) teile.push(T(sFehler ? "s_fehler" : "s_lade"));
    else if (m > 0) teile.push((m > MAX ? T("s_viele") : m === 1 ? T("s_eins") : T("s_treffer")).replace("{n}", m).replace("{max}", MAX));
    if (n === 0 && m === 0) teile.push(T("nichts"));
    status.textContent = teile.map(function (t) { return /[.!?…]$/.test(t) ? t : t + "."; }).join(" ");
  }

  function ladeSeiten() {
    if (seiten || sLaedt) return;
    sLaedt = true;
    fetch("/assets/suche-" + LANG + ".json").then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function (d) {
      syn = d.syn || [];
      seiten = d.s.map(function (s) {
        return { u: s[0], t: s[1], a: s[2], tn: " " + snorm(s[1]), b: s[3].map(function (b) {
          return { h: b[0], id: b[1], x: b[2], hn: " " + snorm(b[0]), xn: " " + snorm(b[2]) };
        }) };
      });
      box.setAttribute("data-seiten", "bereit");
      suche();
    }).catch(function () {
      sFehler = true;
      box.setAttribute("data-seiten", "fehler");
      suche();
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
      ortFehler = true;
      suche();
    });
  }

  feld.addEventListener("focus", function () {
    lade();
    /* Am Telefon rückt das Feld an den oberen Rand, damit die Treffer über der Tastatur Platz haben. */
    if (window.matchMedia && window.matchMedia("(max-width: 640px)").matches && box.scrollIntoView) {
      setTimeout(function () { box.scrollIntoView({ block: "start" }); }, 250);
    }
  });
  feld.addEventListener("input", suche);
  feld.addEventListener("keydown", function (ev) {
    if (ev.key !== "Enter") return;
    var erster = liste.querySelector("a") || (sliste && sliste.querySelector("a"));
    if (erster) { ev.preventDefault(); location.href = erster.href; }
  });
  if (feld.value) suche();
})();
