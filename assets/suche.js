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

  /* genau: nur Orte, die genau so heissen (oder genau diese Postleitzahl haben). ortKt nennt danach die
     Kantone der gefundenen Orte und ortSeiten ihre eigenen Seiten, für die Suche «Thema Ort». */
  var ortKt = [], ortSeiten = [];
  function orte(q, genau) {
    ortKt = [];
    ortSeiten = [];
    if (!q) return 0;
    if (!daten) { lade(); return -1; }
    var zahl = /^[0-9]/.test(q), roh = [];
    daten.e.forEach(function (x) {
      var r = -1;
      if (zahl) { if (x.plz && (genau ? x.plz === q : x.plz.indexOf(q) === 0)) r = 0; }
      else if (x.s === q || x.kz === q) r = 0;
      else if (genau) r = -1;
      else if (x.s.indexOf(q) === 0) r = 1;
      else if (x.s.indexOf(" " + q) !== -1) r = 2;
      else if (q.length >= 4 && x.s.indexOf(q) !== -1) r = 3;
      if (r >= 0) roh.push({ x: x, r: r });
    });
    if (!zahl && q.length >= 3) daten.andere.forEach(function (a) {
      if (genau ? a.s === q : a.s.indexOf(q) === 0) roh.push({ x: a.x, r: a.s === q ? 0 : 1 });
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
      if (ortKt.indexOf(x.k) < 0) ortKt.push(x.k);
      if (t.z.art === "lokal" && t.z.l === LANG) ortSeiten.push(t.z.href);
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
  var wortDa = {}, stopp = {}, themaZuerst = false;  /* wortDa: jedes Wort, das auf einer Seite steht */
  var ARTRANG = { thema: 0, bund: 1, kanton: 2, gemeinde: 3, ueber: 4 };
  function snorm(s) {
    var out = "";
    for (var i = 0; i < s.length; i++) {
      var c = s.charAt(i).toLowerCase().normalize("NFD").charAt(0);
      out += /[a-z0-9]/.test(c) ? c : " ";
    }
    return out;
  }
  /* Dasselbe Wort mit anderer Endung: gleicher Anfang (mindestens vier Buchstaben, bei kürzeren Wörtern das ganze
     Wort), danach zusammen höchstens zwei Buchstaben. «listenhunde» und «listenhund», «pericolose» und
     «pericolosi», aber nicht «chippis» und «chip» oder «chippen». */
  function nah(w, m) {
    if (w === m) return true;
    var p = 0;
    while (p < w.length && p < m.length && w.charAt(p) === m.charAt(p)) p++;
    return p >= Math.min(4, m.length) && w.length + m.length - 2 * p <= 2;
  }
  /* Ein Wort der Eingabe und die gleichbedeutenden Wörter aus der Liste in build.py. Eine Gruppe zählt, wenn das
     Wort eines ihrer Wörter ist (auch mit anderer Endung) oder mit mindestens fünf Buchstaben der Anfang eines
     ihrer Wörter, sofern das nur auf eine Gruppe zutrifft: «hunde» ist der Anfang von «hundesteuer», «hundekot»
     und «hundekurs» und zählt darum für keine. g.a: alle Wörter der Gruppe, g.f: die Wörter, die gesucht werden
     (ohne die mit «=»). */
  function formen(w) {
    var f = [w], fest = [], anfang = [];
    syn.forEach(function (g) {
      if (g.a.some(function (m) { return nah(w, m); })) fest.push(g);
      else if (w.length >= 5 && g.a.some(function (m) { return m.indexOf(w) === 0; })) anfang.push(g);
    });
    if (anfang.length === 1) fest.push(anfang[0]);
    fest.forEach(function (g) { g.f.forEach(function (m) { if (f.indexOf(m) < 0) f.push(m); }); });
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
  /* Ausschnitt um die Fundstelle. Liegt sie in den ersten 90 Zeichen, beginnt er am Anfang des Abschnitts: Dort
     steht bei einer Karte die Antwort («Pflicht · mind. CHF 3 Mio.»). */
  function ausschnitt(text, i) {
    var start = i > 90 ? i - 40 : 0;
    if (start > 0) { var sp = text.indexOf(" ", start); start = sp >= 0 && sp < i ? sp + 1 : i; }
    while (start > 0 && start < i && /[·\s]/.test(text.charAt(start))) start++;
    var ende = start + 130;
    if (ende < text.length) { var sp2 = text.lastIndexOf(" ", ende); if (sp2 > start) ende = sp2; } else ende = text.length;
    return (start > 0 ? "… " : "") + text.slice(start, ende) + (ende < text.length ? " …" : "");
  }
  /* Kantons-, Gemeinde- und Bundesseite: Jedes Wort muss irgendwo auf der Seite stehen. Stehen alle im Titel,
     führt der Treffer an den Anfang der Seite. Sonst auf den Abschnitt mit den meisten übrigen Wörtern, bei
     Gleichstand auf den mit mehr Wörtern in der Überschrift. */
  function seiteTreffer(s, f) {
    var summe = 0, rest = [];
    for (var j = 0; j < f.length; j++) {
      if (stelle(s.tn, f[j]) >= 0) continue;
      rest.push(f[j]);
      if (s.b.some(function (b) { return stelle(b.hn, f[j]) >= 0; })) summe += 1;
      else if (s.b.some(function (b) { return stelle(b.xn, f[j]) >= 0; })) summe += 2;
      else return null;
    }
    var wahl = s.b[0], wz = 0, wk = 0, mit = 0;
    if (rest.length) s.b.forEach(function (b, bi) {
      if (!bi) return;
      var z = 0, k = 0;
      rest.forEach(function (x) {
        var imKopf = stelle(b.hn, x) >= 0;
        if (imKopf) k++;
        if (imKopf || stelle(b.xn, x) >= 0) z++;
      });
      if (z) mit++;
      if (z > wz || (z === wz && k > wk)) { wahl = b; wz = z; wk = k; }
    });
    return { s: s, r: summe, b: wahl, mit: mit };
  }
  /* Themenseite: Jede Zeile gilt für einen Kanton. Wörter, die nicht im Titel stehen, müssen darum in derselben
     Zeile stehen. Nennt die Eingabe den Kanton, führt der Treffer zu dessen Zeile. Steht das Wort bei mehreren
     Kantonen, führt er an den Anfang der Seite, nennt die Zahl der Kantone und zeigt eine Zeile als Beispiel.
     ids: nur die Zeilen dieser Kantone (Suche «Thema Ort»). */
  function themaTreffer(s, f, ids) {
    var rest = f.filter(function (x) { return stelle(s.tn, x) < 0; });
    if (!rest.length && !ids) return { s: s, r: 0, b: s.b[0], mit: 0 };
    var passend = [], best = null, bk = -1, br = 0;
    s.b.forEach(function (b, bi) {
      if (!bi || (ids && ids.indexOf(b.id) < 0)) return;
      var k = 0, r = 0;
      for (var j = 0; j < rest.length; j++) {
        if (stelle(b.hn, rest[j]) >= 0) { k++; r += 1; }
        else if (stelle(b.xn, rest[j]) >= 0) r += 2;
        else return;
      }
      passend.push(b);
      if (k > bk) { best = b; bk = k; br = r; }
    });
    if (!passend.length) {
      var b0 = s.b[0];
      if (ids || !rest.every(function (x) { return stelle(b0.xn, x) >= 0; })) return null;
      return { s: s, r: 2 * rest.length, b: b0, mit: 0 };
    }
    var kantone = passend.filter(function (b) { return b.id.indexOf("kt-") === 0; });
    if (ids || bk > 0 || passend.length === 1 || kantone.length < 2) return { s: s, r: br, b: best, mit: passend.length };
    return { s: s, r: br, b: kantone[0], mit: kantone.length, oben: kantone.length };
  }
  /* nur: {seiten: [Adresse, ...], ids: ["kt-be", ...]} beschränkt die Suche auf diese Seiten (Kantonsseite und
     eigene Seite des Orts) und auf die Zeilen dieser Kantone auf den Themenseiten. */
  function seitenSuche(roh, nur) {
    sliste.textContent = "";
    sbox.hidden = true;
    /* Wörter, die nichts eingrenzen («mein», «Hund», «in»), fallen weg, solange ein anderes übrig bleibt. */
    var alleW = [];
    snorm(roh.replace(/ß/g, "ss")).split(" ").forEach(function (w) { if (w && alleW.indexOf(w) < 0) alleW.push(w); });
    var woerter = alleW.filter(function (w) { return !stopp[w]; });
    if (!woerter.length) woerter = alleW;
    woerter = woerter.slice(0, 6);
    if (!woerter.length) return 0;
    if (!seiten) { ladeSeiten(); return -1; }
    var f = woerter.map(formen), alle = [].concat.apply([], f), treffer = [];
    seiten.forEach(function (s) {
      var t = null;
      if (s.a === "thema") t = themaTreffer(s, f, nur && nur.ids);
      else if (!nur || nur.seiten.indexOf(s.u) >= 0) t = seiteTreffer(s, f);
      if (t) treffer.push(t);
    });
    treffer.sort(function (a, b) {
      return a.r - b.r || b.mit - a.mit || ARTRANG[a.s.a] - ARTRANG[b.s.a] || a.s.t.length - b.s.t.length;
    });
    treffer.slice(0, MAX).forEach(function (t) {
      var a = document.createElement("a"), name = document.createElement("span"), text = document.createElement("span");
      a.className = "topic";
      a.setAttribute("role", "listitem");
      a.href = t.s.u + (!t.oben && t.b.id ? "#" + t.b.id : "");
      name.className = "topic-name";
      markiert(name, t.s.t, alle);
      a.appendChild(name);
      if (t.oben || (t.b.h && t.b !== t.s.b[0])) {
        var ab = document.createElement("span");
        ab.className = "such-ab";
        if (t.oben) ab.textContent = T("s_kantone").replace("{n}", t.oben);
        else markiert(ab, t.b.h, alle);
        a.appendChild(ab);
      }
      if (t.b.x) {
        text.className = "topic-text";
        var i = stelle(t.b.xn, alle);
        markiert(text, (t.oben ? t.b.h + ": " : "") + ausschnitt(t.b.x, i < 0 ? 0 : i), alle);
        a.appendChild(text);
      }
      sliste.appendChild(a);
    });
    sbox.hidden = !treffer.length;
    return treffer.length;
  }
  /* «Thema Ort», zum Beispiel «Haftpflicht Lyss» oder «Hundesteuer Ipsach»: Die Suche sucht in der Eingabe einen
     Ort (genauer Name, Postleitzahl oder Kürzel eines Kantons, die längste Wortfolge zuerst) und die übrigen
     Wörter dort: auf der Seite des Orts, auf der Kantonsseite und in der Zeile des Kantons auf den Themenseiten.
     streng: nur Orte, deren Name auf den Seiten nicht als Wort vorkommt («Ipsach», aber nicht «Wald»). So bleibt
     «Leine Wald» eine Suche nach zwei Stichworten. Ohne streng läuft sie erst, wenn die ganze Eingabe nichts
     findet. Liefert [Orte, Seiten] oder null. Findet sich nur der Ort, bleibt er stehen: [Orte, 0]. */
  function ortUndThema(q, streng) {
    var w = q.split(" "), erster = null;
    if (w.length < 2 || w.length > 6 || !daten || !seiten) return null;
    for (var len = w.length - 1; len >= 1; len--) {
      for (var ab = 0; ab + len <= w.length; ab++) {
        var teil = w.slice(ab, ab + len);
        if (streng && teil.every(function (x) { return wortDa[x]; })) continue;
        liste.textContent = "";
        var n = orte(teil.join(" "), true);
        if (n < 1) continue;
        if (!erster) erster = teil.join(" ");
        var nur = { seiten: ortSeiten.slice(), ids: [] };
        ortKt.forEach(function (i) {
          var k = daten.d.k[i], z = waehle(k[1]);
          if (z && z.l === LANG) nur.seiten.push(z.href);
          nur.ids.push("kt-" + k[0]);
        });
        var m = seitenSuche(w.slice(0, ab).concat(w.slice(ab + len)).join(" "), nur);
        if (m > 0) return [n, m];
      }
    }
    liste.textContent = "";
    return erster && !streng ? [orte(erster, true), 0] : null;
  }

  function suche() {
    var q = norm(feld.value);
    liste.textContent = "";
    if (sliste) { sliste.textContent = ""; sbox.hidden = true; }
    if (!q) { status.textContent = ""; return; }
    var n = orte(q), m = 0, teile = [];
    var zwei = n === 0 && sliste ? ortUndThema(q, true) : null;
    if (!zwei && sliste) {
      m = seitenSuche(feld.value);
      if (n === 0 && m === 0) zwei = ortUndThema(q, false);
    }
    themaZuerst = !!zwei && zwei[1] > 0;
    if (zwei) { n = zwei[0]; m = zwei[1]; }
    if (n < 0) teile.push(T(ortFehler ? "fehler" : "lade"));
    else if (n > 0) teile.push((n > MAX ? T("viele") : T("treffer")).replace("{n}", n).replace("{max}", MAX));
    if (m < 0) teile.push(T(sFehler ? "s_fehler" : "s_lade"));
    else if (m > 0) teile.push((m > MAX ? T("s_viele") : m === 1 ? T("s_eins") : T("s_treffer")).replace("{n}", m).replace("{max}", MAX));
    if (zwei && m === 0) teile.push(T("s_ohne"));
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
      (d.stop || []).forEach(function (w) { stopp[w] = 1; });
      syn = (d.syn || []).map(function (g) {
        return { a: g.map(function (m) { return m.replace(/^=/, ""); }),
          f: g.filter(function (m) { return m.charAt(0) !== "="; }) };
      });
      seiten = d.s.map(function (s) {
        return { u: s[0], t: s[1], a: s[2], tn: " " + snorm(s[1]), b: s[3].map(function (b) {
          var e = { h: b[0], id: b[1], x: b[2], hn: " " + snorm(b[0]), xn: " " + snorm(b[2]) };
          (e.hn + e.xn).split(" ").forEach(function (w) { if (w) wortDa[w] = 1; });
          return e;
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
    /* Bei «Thema Ort» zuerst der Treffer zum Thema, sonst zuerst der Ort. */
    var ort = liste.querySelector("a"), seite = sliste && sliste.querySelector("a");
    var erster = themaZuerst ? seite || ort : ort || seite;
    if (erster) { ev.preventDefault(); location.href = erster.href; }
  });
  if (feld.value) suche();
})();
