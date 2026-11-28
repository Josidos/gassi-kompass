// Prüft die gebauten Seiten in einem echten Browser (Playwright), schmal (390 px) und breit (1280 px).
//   node tests/seiten.js                            prüft alle Seiten aus sitemap.xml und 404.html
//   node tests/seiten.js /lu/luzern/ bild.png       macht zusätzlich ein Bildschirmfoto dieser Seite (390 px)
//   node tests/seiten.js /lu/luzern/ bild.png 1280  dasselbe in 1280 px Breite
// Geprüft wird: Seite lädt, keine Skriptfehler, kein seitliches Überlaufen, genau eine Hauptüberschrift,
// alle internen Links und Dateien existieren, der Wald-Status wird gesetzt, die Ortssuche findet Orte
// und führt auf die richtige Seite, jede Themenseite führt jeden Kanton ihrer Sprache mit Quelle auf,
// jede Startseite zeigt 26 Kantonstafeln, das Gemeindeverzeichnis und sieben Thementafeln.
// Die Themenseite «vermisst» führt die Karte des Bundes und jeden Kanton mit dem Feld 'vermisst' samt Quelle,
// eine Kantonsseite zeigt den Abschnitt genau dann, wenn ihre Datei das Feld hat.
// Jede Kantonsseite hat genau einen Abschnitt #neuer-hund mit sechs Schritten, deren Links auf eine id derselben
// Seite führen, die es genau einmal gibt. Keine id kommt auf einer Seite doppelt vor. Jede Seite beginnt mit dem
// Sprunglink «Zum Inhalt», und sein Ziel gibt es. Jede Gemeindeseite hat «Auf einen Blick» mit einer Zeile je lokaler
// Karte (plus Freilaufzonen), die sechs Karten des Kantons in einem details und sechs Kurzzeilen auf Anker der Kantonsseite.
// Kantonsseiten und Seiten des Bundes haben genau eine Sprungleiste (nav.sprung) mit mindestens drei Links auf Ziele,
// die es genau einmal gibt, und eine Übersicht vor den Karten. Jede Karte hat ein h3.
// Sprachen: Seiten unter /fr-ch/ tragen lang="fr-CH", unter /it-ch/ lang="it-CH", alle anderen lang="de-CH".
// hreflang muss in beide Richtungen stimmen, und die Ortssuche jeder Startseite wird mitgeprüft.
// Übersetzte Seiten (Feld uebersetzt_aus) tragen den Hinweis «Übersetzung», Originalfassungen nicht.
// Karte der Hundezonen (Adressen auf /karte/): Vor dem Klick auf «Karte laden» ruft die Seite nichts Fremdes ab.
// Nach dem Klick stehen alle Flächen aus zonen.json auf der Karte, fremd sind nur die Kartenbilder von swisstopo
// (im Test durch ein leeres Bild ersetzt), und ein Name aus der Liste der Freilaufzonen zeigt die Zone an.
// Der Test bricht auch ab, wenn eine Adresse aus dem letzten Commit in der Sitemap fehlt.
// Soll eine Seite wirklich verschwinden: node tests/seiten.js --entfernen-erlaubt
const http = require('http'), fs = require('fs'), path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
const TYP = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2', '.xml': 'application/xml', '.txt': 'text/plain' };
const lies = (...teile) => JSON.parse(fs.readFileSync(path.join(ROOT, ...teile), 'utf8'));
// Sprachen in der Reihenfolge, in der die Suche ausweicht: [Sprache, Präfix der Adresse, Datenordner, lang im HTML]
const SPRACHEN = [['de', '', ['data'], 'de-CH'], ['fr', '/fr-ch', ['data', 'fr-ch'], 'fr-CH'], ['it', '/it-ch', ['data', 'it-ch'], 'it-CH']];
const sollLang = s => (SPRACHEN.find(x => x[1] && s.startsWith(x[1] + '/')) || SPRACHEN[0])[3];
const ordner = (...teile) => { const p = path.join(ROOT, ...teile); return fs.existsSync(p) ? fs.readdirSync(p) : []; };

function datei(url) {
  let p = decodeURIComponent(url.split('#')[0].split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const voll = path.join(ROOT, p);
  return voll.startsWith(ROOT) && fs.existsSync(voll) && fs.statSync(voll).isFile() ? voll : null;
}

(async () => {
  const server = http.createServer((req, res) => {
    const f = datei(req.url);
    if (!f) { res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' }); res.end(fs.readFileSync(path.join(ROOT, '404.html'))); return; }
    res.writeHead(200, { 'Content-Type': TYP[path.extname(f)] || 'application/octet-stream' });
    res.end(fs.readFileSync(f));
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const basis = 'http://127.0.0.1:' + server.address().port;
  const seiten = [...fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8').matchAll(/<loc>https:\/\/[^/]+([^<]*)<\/loc>/g)].map(m => m[1]);
  seiten.push('/404.html');
  const [fotoSeite, fotoDatei, fotoBreite] = process.argv.slice(2).filter(a => !a.startsWith('--'));
  const browser = await chromium.launch();
  const fehler = [];
  const alternativen = {};

  // Keine veröffentlichte Adresse darf verschwinden (Vergleich mit der Sitemap im letzten Commit)
  if (!process.argv.includes('--entfernen-erlaubt')) {
    let alt = '';
    try { alt = execFileSync('git', ['show', 'HEAD:sitemap.xml'], { cwd: ROOT, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }); } catch (e) { /* kein Git: nichts zu vergleichen */ }
    for (const m of alt.matchAll(/<loc>https:\/\/[^/]+([^<]*)<\/loc>/g)) {
      if (!seiten.includes(m[1])) fehler.push(`${m[1]}: Adresse war veröffentlicht und fehlt jetzt. Adressen nie ändern, siehe CLAUDE.md.`);
    }
  }

  // Übersetzte Seiten (Feld uebersetzt_aus in der Datendatei) tragen den Hinweis «Übersetzung», alle anderen nicht.
  const uebersetzt = new Set();
  for (const [, pre, dir] of SPRACHEN) {
    for (const f of ordner(...dir, 'kantone')) if (f.endsWith('.json') && lies(...dir, 'kantone', f).uebersetzt_aus) uebersetzt.add(`${pre}/${f.slice(0, -5)}/`);
    for (const kt of ordner(...dir, 'gemeinden')) {
      for (const f of ordner(...dir, 'gemeinden', kt)) if (f.endsWith('.json') && lies(...dir, 'gemeinden', kt, f).uebersetzt_aus) uebersetzt.add(`${pre}/${kt}/${f.slice(0, -5)}/`);
    }
  }

  // Jede Seite, schmal und breit
  for (const breite of [390, 1280]) {
    const ctx = await browser.newContext({ viewport: { width: breite, height: 844 }, deviceScaleFactor: 1 });
    for (const s of seiten) {
      const wo = `${s} (${breite} px)`;
      const page = await ctx.newPage();
      const meldungen = [];
      page.on('console', m => { if (m.type() === 'error') meldungen.push(m.text()); });
      page.on('pageerror', err => meldungen.push('Skriptfehler: ' + err.message));
      page.on('requestfailed', r => meldungen.push('Laden fehlgeschlagen: ' + r.url()));
      const antwort = await page.goto(basis + s, { waitUntil: 'load' });
      if (!antwort || antwort.status() !== 200) fehler.push(`${wo}: Status ${antwort && antwort.status()}`);
      for (const m of meldungen) fehler.push(`${wo}: ${m}`);
      const info = await page.evaluate(() => ({
        ueberlauf: document.documentElement.scrollWidth - window.innerWidth,
        h1: document.querySelectorAll('h1').length,
        titel: document.title,
        lang: document.documentElement.lang,
        hinweis: !!document.querySelector('[data-uebersetzung]'),
        alt: [...document.querySelectorAll('link[rel="alternate"][hreflang]')].map(x => [x.hreflang, new URL(x.href).pathname]),
        links: [...document.querySelectorAll('a[href^="/"], link[href^="/"], script[src^="/"]')].map(x => x.getAttribute('href') || x.getAttribute('src')),
        doppelt: (() => { const z = {}; for (const x of document.querySelectorAll('[id]')) z[x.id] = (z[x.id] || 0) + 1; return Object.keys(z).filter(i => z[i] > 1); })(),
        sprung: (() => { const a = document.body.firstElementChild; const h = a && a.matches('a.skip[href^="#"]') ? a.getAttribute('href').slice(1) : null; return { da: !!h, ziel: !!h && !!document.getElementById(h) }; })(),
        wald: [...document.querySelectorAll('[data-wald]')].map(x => ({ saison: x.getAttribute('data-saison'), gross: x.querySelector('[data-heute-gross]').className, heute: !!x.querySelector('.now'), datum: x.querySelector('[data-heute-datum]').textContent }))
      }));
      if (info.ueberlauf > 0) fehler.push(`${wo}: läuft seitlich über (${info.ueberlauf}px)`);
      if (info.h1 !== 1) fehler.push(`${wo}: ${info.h1} Hauptüberschriften statt 1`);
      if (!info.titel) fehler.push(`${wo}: kein Seitentitel`);
      for (const d of info.doppelt) fehler.push(`${wo}: id="${d}" kommt mehrfach vor`);
      if (!info.sprung.da) fehler.push(`${wo}: Der Sprunglink «Zum Inhalt» ist nicht das erste Element im body`);
      else if (!info.sprung.ziel) fehler.push(`${wo}: Das Ziel des Sprunglinks fehlt`);
      for (const l of new Set(info.links)) if (!datei(l)) fehler.push(`${wo}: Link ohne Ziel: ${l}`);
      for (const w of info.wald) {
        if (!w.heute || !w.datum) fehler.push(`${wo}: Heute-Markierung oder Datum fehlt`);
        if (w.saison === '1' && !/ (must|free)$/.test(w.gross)) fehler.push(`${wo}: Wald-Status wurde nicht gesetzt`);
      }
      if (info.lang !== sollLang(s)) fehler.push(`${wo}: lang="${info.lang}" statt "${sollLang(s)}"`);
      if (info.hinweis !== uebersetzt.has(s)) fehler.push(`${wo}: ${info.hinweis ? 'trägt den Hinweis «Übersetzung», ist aber eine Originalfassung' : 'ist eine Übersetzung, der Hinweis fehlt'}`);
      if (breite === 390) {
        alternativen[s] = info.alt;
        if (info.alt.length && !info.alt.some(a => a[0] === info.lang && a[1] === s)) fehler.push(`${s}: hreflang nennt die eigene Seite nicht`);
        for (const a of info.alt) if (!seiten.includes(a[1])) fehler.push(`${s}: hreflang ${a[0]} zeigt auf ${a[1]}, die Seite gibt es nicht`);
      }
      const sprache = SPRACHEN.find(x => s.startsWith(x[1] + '/thema/'));
      if (s === (SPRACHEN.find(x => x[1] && s.startsWith(x[1] + '/')) || SPRACHEN[0])[1] + '/') {
        const st = await page.evaluate(() => ({ kantone: document.querySelectorAll('.raster a').length, themen: document.querySelectorAll('.topics a').length, gemeinden: document.querySelectorAll('.index a').length, tabellen: document.querySelectorAll('table').length }));
        if (st.kantone !== 26 || st.themen !== 7 || !st.gemeinden || st.tabellen) fehler.push(`${wo}: Startseite mit ${st.kantone} Kantonstafeln, ${st.themen} Thementafeln, ${st.gemeinden} Links im Gemeindeverzeichnis, ${st.tabellen} Tabellen (soll: 26, 7, mindestens 1, 0)`);
      }
      const kt = s.match(/^(\/fr-ch|\/it-ch)?\/([a-z]{2})\/$/);
      if (kt) {
        const dir = SPRACHEN.find(x => x[1] === (kt[1] || ''))[2];
        if (fs.existsSync(path.join(ROOT, ...dir, 'kantone', kt[2] + '.json'))) {
          const soll = lies(...dir, 'kantone', kt[2] + '.json').vermisst ? 1 : 0;
          const ist = await page.evaluate(() => document.querySelectorAll('[data-vermisst]').length);
          if (ist !== soll) fehler.push(`${wo}: ${ist} Abschnitte «vermisst», die Datei verlangt ${soll}`);
          const sollD = lies(...dir, 'kantone', kt[2] + '.json').durchsicht ? 1 : 0;
          const istD = await page.evaluate(() => document.querySelectorAll('[data-durchsicht]').length);
          if (istD !== sollD) fehler.push(`${wo}: ${istD} Hinweise «durchsicht», die Datei verlangt ${sollD}`);
          // «Neu einen Hund»: genau ein Abschnitt mit sechs Schritten, jeder Link führt auf eine id, die es genau einmal gibt
          const nh = await page.evaluate(() => {
            const a = document.querySelectorAll('#neuer-hund');
            const links = a.length ? [...a[0].querySelectorAll('ol > li a[href^="#"]')].map(x => x.getAttribute('href').slice(1)) : [];
            return { abschnitte: a.length, schritte: a.length ? a[0].querySelectorAll('ol > li').length : 0,
                     ohneZiel: links.filter(i => document.querySelectorAll('[id="' + i + '"]').length !== 1), links: links.length };
          });
          if (nh.abschnitte !== 1 || nh.schritte !== 6 || nh.links !== 6) fehler.push(`${wo}: «Neu einen Hund» mit ${nh.abschnitte} Abschnitten, ${nh.schritte} Schritten und ${nh.links} Links (soll: 1, 6, 6)`);
          for (const i of nh.ohneZiel) fehler.push(`${wo}: «Neu einen Hund» verlinkt #${i}, das es nicht genau einmal gibt`);
        }
      }
      // Kantonsseite und Seite des Bundes: genau eine Sprungleiste mit mindestens drei Links, jedes Ziel genau einmal,
      // und die Übersicht vor den Karten (Kanton: sechs Zeilen, Bund: eine je Karte). Andere Seiten haben keine Sprungleiste.
      const istKt = kt && fs.existsSync(path.join(ROOT, ...SPRACHEN.find(x => x[1] === (kt[1] || ''))[2], 'kantone', kt[2] + '.json'));
      const istBund = /^(\/fr-ch|\/it-ch)?\/schweiz\/$/.test(s);
      const sp = await page.evaluate(() => {
        const n = document.querySelectorAll('nav.sprung');
        const links = n.length ? [...n[0].querySelectorAll('a')].map(x => x.getAttribute('href')) : [];
        const sec = document.getElementById('pflichten');
        const blick = sec ? sec.querySelector(':scope > [data-blick]') : null;
        const karten = sec ? sec.querySelector(':scope > .cards') : null;
        return { navs: n.length, links: links.length,
                 ohneZiel: links.filter(h => !h.startsWith('#') || document.querySelectorAll('[id="' + h.slice(1) + '"]').length !== 1),
                 zeilen: blick ? blick.querySelectorAll('li').length : 0,
                 zuerst: !!(blick && karten && (blick.compareDocumentPosition(karten) & Node.DOCUMENT_POSITION_FOLLOWING)),
                 kartenZahl: karten ? karten.querySelectorAll('.card').length : 0,
                 zeilenOhneZiel: blick ? [...blick.querySelectorAll('a')].map(x => x.getAttribute('href')).filter(h => document.querySelectorAll('[id="' + h.slice(1) + '"]').length !== 1) : [] };
      });
      if (istKt || istBund) {
        if (sp.navs !== 1 || sp.links < 3) fehler.push(`${wo}: Sprungleiste ${sp.navs}-mal mit ${sp.links} Links (soll: 1, mindestens 3)`);
        for (const h of sp.ohneZiel) fehler.push(`${wo}: Die Sprungleiste verlinkt ${h}, das es nicht genau einmal gibt`);
        const sollZ = istKt ? 6 : sp.kartenZahl;
        if (!sp.zuerst || sp.zeilen !== sollZ || !sollZ) fehler.push(`${wo}: Übersicht vor den Karten mit ${sp.zeilen} Zeilen (soll: ${sollZ}, vor den Karten)`);
        for (const h of sp.zeilenOhneZiel) fehler.push(`${wo}: Die Übersicht verlinkt ${h}, das es nicht genau einmal gibt`);
      } else if (sp.navs) fehler.push(`${wo}: Sprungleiste auf einer Seite, die keine haben soll`);
      const ohneH3 = await page.evaluate(() => [...document.querySelectorAll('.card')].filter(c => !c.querySelector(':scope > .card-top > h3.card-k')).length);
      if (ohneH3) fehler.push(`${wo}: ${ohneH3} Karten ohne Überschrift h3`);
      // Gemeindeseite: «Auf einen Blick» mit einer Zeile je lokaler Karte (plus Freilaufzonen), jedes Ziel genau einmal.
      // Die sechs Karten des Kantons stehen in einem details, die sechs Kurzzeilen führen auf Anker der Kantonsseite.
      const gm = s.match(/^(\/fr-ch|\/it-ch)?\/([a-z]{2})\/([a-z0-9-]+)\/$/);
      if (gm) {
        const dir = SPRACHEN.find(x => x[1] === (gm[1] || ''))[2];
        const df = path.join(ROOT, ...dir, 'gemeinden', gm[2], gm[3] + '.json');
        if (fs.existsSync(df)) {
          const g = lies(...dir, 'gemeinden', gm[2], gm[3] + '.json');
          const soll = g.karten.length + (g.freilaufzonen && g.freilaufzonen.length ? 1 : 0);
          const b = await page.evaluate(() => {
            const l = document.querySelectorAll('.hero [data-blick]');
            const links = l.length ? [...l[0].querySelectorAll('li a')].map(x => x.getAttribute('href')) : [];
            const kk = document.querySelectorAll('details[data-kanton-karten]');
            const kurz = kk.length ? [...kk[0].closest('section').querySelectorAll('[data-blick] li a')].map(x => x.getAttribute('href')) : [];
            return { listen: l.length, zeilen: l.length ? l[0].querySelectorAll('li').length : 0,
                     ohneZiel: links.filter(h => !h.startsWith('#') || document.querySelectorAll('[id="' + h.slice(1) + '"]').length !== 1),
                     kk: kk.length, karten: kk.length ? kk[0].querySelectorAll('.card').length : 0, kurz };
          });
          if (b.listen !== 1 || b.zeilen !== soll) fehler.push(`${wo}: «Auf einen Blick» mit ${b.listen} Listen und ${b.zeilen} Zeilen (soll: 1, ${soll})`);
          for (const h of b.ohneZiel) fehler.push(`${wo}: «Auf einen Blick» verlinkt ${h}, das es auf der Seite nicht genau einmal gibt`);
          if (b.kk !== 1 || b.karten !== 6) fehler.push(`${wo}: Karten des Kantons: ${b.kk} details mit ${b.karten} Karten (soll: 1, 6)`);
          if (b.kurz.length !== 6) fehler.push(`${wo}: ${b.kurz.length} Kurzzeilen zum Kanton statt 6`);
          for (const h of b.kurz) {
            const [p, anker] = h.split('#'), f = datei(p);
            if (!f || !anker || !fs.readFileSync(f, 'utf8').includes(`id="${anker}"`)) fehler.push(`${wo}: Kurzzeile zum Kanton führt auf ${h}, den Anker gibt es dort nicht`);
          }
        }
      }
      if (sprache && s.endsWith('/thema/vermisst/')) {
        const soll = ordner(...sprache[2], 'kantone').filter(f => f.endsWith('.json') && lies(...sprache[2], 'kantone', f).vermisst).length;
        const t = await page.evaluate(() => ({ kantone: document.querySelectorAll('details.kt-zeile[data-vermisst]').length, mitQuelle: [...document.querySelectorAll('details.kt-zeile[data-vermisst]')].filter(x => x.querySelector('.kt-inhalt .src a') && x.querySelector('.kt-inhalt a.text-link')).length, bund: document.querySelectorAll('.card .src a').length, zuerst: !!document.querySelector('.card') && !!document.querySelector('.kt-zeile') && !!(document.querySelector('.card').compareDocumentPosition(document.querySelector('.kt-zeile')) & Node.DOCUMENT_POSITION_FOLLOWING), tabellen: document.querySelectorAll('table').length }));
        if (t.kantone !== soll || t.mitQuelle !== soll) fehler.push(`${wo}: ${t.kantone} Zeilen, davon ${t.mitQuelle} mit Quelle und Link, statt ${soll} (jeder Kanton mit dem Feld 'vermisst')`);
        if (!t.bund || !t.zuerst || t.tabellen) fehler.push(`${wo}: Karte des Bundes mit Quelle fehlt oder steht nicht zuoberst, oder die Seite hat eine Tabelle`);
      } else if (sprache) {
        const kantone = ordner(...sprache[2], 'kantone').filter(f => f.endsWith('.json')).map(f => f.slice(0, -5));
        const t = await page.evaluate(() => ({ zeilen: [...document.querySelectorAll('details.kt-zeile')].map(x => x.id), mitQuelle: [...document.querySelectorAll('details.kt-zeile')].filter(x => x.querySelector('.kt-inhalt .src a') && x.querySelector('.kt-inhalt a.text-link') && x.querySelector('summary .chip') && !x.querySelector('summary a')).length, karten: document.querySelectorAll('.card').length, tabellen: document.querySelectorAll('table').length }));
        const fehlt = kantone.filter(k => !t.zeilen.includes('kt-' + k));
        if (t.zeilen.length !== kantone.length || fehlt.length) fehler.push(`${wo}: ${t.zeilen.length} Zeilen statt ${kantone.length}, es fehlen: ${fehlt.join(', ')}`);
        if (t.mitQuelle !== kantone.length) fehler.push(`${wo}: ${kantone.length - t.mitQuelle} Zeilen ohne Quelle, Marke oder Link zur Kantonsseite, oder mit Link in der summary`);
        if (t.karten || t.tabellen) fehler.push(`${wo}: ${t.karten} Karten und ${t.tabellen} Tabellen (soll: keine)`);
      }
      if (sprache && breite === 390) {
        // Sprung auf einen Kanton: …/#kt-zh klappt genau diese Zeile auf
        await page.goto(basis + s + '#kt-zh', { waitUntil: 'load' });
        await page.waitForTimeout(100);
        const a = await page.evaluate(() => ({ zh: !!(document.getElementById('kt-zh') || {}).open, offen: document.querySelectorAll('details.kt-zeile[open]').length }));
        if (!a.zh || a.offen !== 1) fehler.push(`${wo}: #kt-zh klappt die Zeile von Zürich nicht auf (offen: ${a.offen})`);
      }
      if (s === fotoSeite && fotoDatei && breite === Number(fotoBreite || 390)) await page.screenshot({ path: fotoDatei, fullPage: true });
      await page.close();
    }
    await ctx.close();
  }

  // hreflang in beide Richtungen: Nennt Seite A die Seite B, muss B auch A nennen, mit der richtigen Sprache.
  for (const [s, alt] of Object.entries(alternativen)) {
    for (const [l, ziel] of alt) {
      if (l !== sollLang(ziel)) fehler.push(`${s}: hreflang ${l} zeigt auf ${ziel} (dort gilt ${sollLang(ziel)})`);
      if (ziel !== s && !(alternativen[ziel] || []).some(a => a[1] === s)) fehler.push(`${s}: hreflang nennt ${ziel}, aber nicht umgekehrt`);
    }
  }

  // Ortssuche: Die Erwartungen kommen aus den Daten, damit der Test mit jedem neuen Kanton weiter stimmt.
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });

  // Karte der Hundezonen
  const LEER = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP48OHDfwAJMQPcbdP1VQAAAABJRU5ErkJggg==', 'base64');
  const KACHELN = 'https://wmts.geo.admin.ch/';
  for (const s of seiten.filter(x => x.endsWith('/karte/'))) {
    const p = await ctx.newPage();
    const fremd = [];
    p.on('pageerror', err => fehler.push(`${s}: Skriptfehler in der Karte: ` + err.message));
    p.on('request', r => { if (!r.url().startsWith(basis) && !r.url().startsWith('data:')) fremd.push(r.url()); });
    await p.route(KACHELN + '**', r => r.fulfill({ status: 200, contentType: 'image/png', body: LEER }));
    await p.goto(basis + s, { waitUntil: 'load' });
    if (fremd.length) fehler.push(`${s}: ruft vor dem Klick auf «Karte laden» fremde Adressen ab: ${fremd[0]}`);
    const quelle = await p.getAttribute('[data-karte]', 'data-daten');
    const zonen = datei(quelle) ? JSON.parse(fs.readFileSync(datei(quelle), 'utf8')).zonen : [];
    const soll = zonen.length || -1;
    if (soll < 1) fehler.push(`${s}: Die Flächen fehlen (${quelle})`);
    if (await p.isHidden('[data-karte-laden]')) fehler.push(`${s}: Der Knopf «Karte laden» ist nicht sichtbar`);
    else {
      await p.click('[data-karte-laden]');
      await p.waitForSelector('[data-karte][data-stand="bereit"]', { timeout: 15000 }).catch(() => {});
      const k = await p.evaluate(() => ({
        stand: document.querySelector('[data-karte]').getAttribute('data-stand'),
        flaechen: Number(document.querySelector('[data-karte]').getAttribute('data-flaechen')),
        blatt: !!document.querySelector('.karte-blatt.leaflet-container canvas'),
        startWeg: document.querySelector('[data-karte-start]').hidden,
        ort: !document.querySelector('[data-karte-ort]').parentNode.hidden,
        status: document.querySelector('[data-karte-status]').textContent.trim(),
        ueberlauf: document.documentElement.scrollWidth - window.innerWidth
      }));
      if (k.stand !== 'bereit' || !k.blatt || !k.startWeg || !k.ort || !k.status) fehler.push(`${s}: Die Karte wird nach dem Klick nicht fertig (Stand ${k.stand})`);
      if (k.flaechen !== soll) fehler.push(`${s}: ${k.flaechen} Flächen auf der Karte, zonen.json hat ${soll}`);
      if (k.ueberlauf > 0) fehler.push(`${s}: läuft mit geladener Karte seitlich über (${k.ueberlauf}px)`);
      const andere = fremd.filter(u => !u.startsWith(KACHELN));
      if (andere.length) fehler.push(`${s}: Die Karte ruft ausser den Kartenbildern von swisstopo noch ab: ${andere[0]}`);
      if (!fremd.some(u => u.startsWith(KACHELN))) fehler.push(`${s}: Die Karte hat keine Kartenbilder angefordert`);
      // Der Punkt einer Freilaufzone liegt über den Flächen: Ein Tipp darauf holt die Zone heran und nennt sie.
      const frei = zonen.find(z => z.z === 7);
      if (frei && k.stand === 'bereit') {
        await p.locator('.karte-blatt').scrollIntoViewIfNeeded();
        const wo = await p.evaluate(z => {
          let a = Infinity, b = -Infinity, c = Infinity, d = -Infinity;
          for (const teil of z.g) for (const r of teil) {
            let x = r[0], y = r[1];
            for (let i = 0; i < r.length; i += 2) { if (i) { x += r[i]; y += r[i + 1]; } a = Math.min(a, x); b = Math.max(b, x); c = Math.min(c, y); d = Math.max(d, y); }
          }
          const q = document.querySelector('[data-karte]')._karte.latLngToContainerPoint([(c + d) / 2e5, (a + b) / 2e5]);
          const f = document.querySelector('.karte-blatt').getBoundingClientRect();
          return { x: f.left + q.x, y: f.top + q.y };
        }, frei);
        await p.mouse.click(wo.x, wo.y);
        await p.waitForFunction(() => document.querySelector('[data-karte]')._karte.getZoom() >= 15, null, { timeout: 5000 }).catch(() => {});
        const nach = await p.evaluate(() => ({ zoom: document.querySelector('[data-karte]')._karte.getZoom(), info: document.querySelector('[data-karte-info]').hidden ? '' : document.querySelector('[data-karte-info]').textContent }));
        if (nach.zoom < 15 || !nach.info.includes(frei.n)) fehler.push(`${s}: Ein Tipp auf den Punkt der Freilaufzone «${frei.n}» holt sie nicht heran (Zoom ${nach.zoom})`);
      }
      const knoepfe = await p.$$('[data-karte-zeige]');
      if (!knoepfe.length) fehler.push(`${s}: Die Liste der Freilaufzonen fehlt`);
      else {
        const zweite = knoepfe[Math.min(1, knoepfe.length - 1)];
        const name = (await zweite.textContent()).trim();
        await zweite.click();
        await p.waitForFunction(n => { const x = document.querySelector('[data-karte-info]'); return !x.hidden && x.textContent.includes(n); }, name, { timeout: 5000 }).catch(() => {});
        const info = await p.$eval('[data-karte-info]', x => x.hidden ? '' : x.textContent);
        if (!name || !info.includes(name)) fehler.push(`${s}: Ein Tipp auf «${name}» in der Liste zeigt die Zone nicht an`);
      }
    }
    await p.close();
  }
  const orte = lies('data', 'orte.json');
  // Kantone und Gemeinden aller Sprachen. Die deutsche Startseite führt auf die deutsche Fassung, sonst auf die nächste.
  const kantonSeite = {}, eigene = [];
  for (const [l, pre, dir] of SPRACHEN) {
    for (const f of ordner(...dir, 'kantone')) if (f.endsWith('.json') && !kantonSeite[f.slice(0, -5)]) kantonSeite[f.slice(0, -5)] = `${pre}/${f.slice(0, -5)}/`;
    for (const kt of ordner(...dir, 'gemeinden')) {
      for (const f of ordner(...dir, 'gemeinden', kt)) if (f.endsWith('.json')) eigene.push({ ...lies(...dir, 'gemeinden', kt, f), l, pre });
    }
  }
  const erfasst = Object.keys(kantonSeite);
  const start = await ctx.newPage();
  start.on('pageerror', err => fehler.push('Suche: Skriptfehler: ' + err.message));
  const fremdSuche = [];
  start.on('request', r => { if (!r.url().startsWith(basis) && !r.url().startsWith('data:')) fremdSuche.push(r.url()); });
  await start.goto(basis + '/');
  if (await start.isHidden('#ortssuche')) fehler.push('/: Das Suchfeld ist nicht sichtbar');
  async function such(text) {
    await start.fill('#ortssuche', String(text));
    await start.waitForSelector('[data-suche][data-stand="bereit"]', { timeout: 8000 }).catch(() => {});
    return start.$$eval('#treffer a', xs => xs.map(x => ({ text: x.textContent, href: x.getAttribute('href') })));
  }
  async function hinweis(adresse) {
    const p = await ctx.newPage();
    let dialog = false;
    p.on('dialog', d => { dialog = true; d.dismiss(); });
    await p.goto(basis + adresse);
    const h = await p.$eval('[data-ort-hinweis]', x => ({ sichtbar: !x.hidden, text: x.textContent, kinder: [...x.children].map(c => c.tagName).join(',') }));
    await p.close();
    return { ...h, dialog };
  }

  // 1. Gemeinde mit eigener Seite: über den Namen und über die Postleitzahl
  if (eigene.length) {
    const g = eigene[0], soll = `/${g.kanton}/${g.id}/`;
    const name = orte.gemeinden.find(x => x[0] === g.bfs)[1], plz = orte.orte.find(x => x[2] === g.bfs)[1];
    if (!(await such(name)).some(x => x.href === soll)) fehler.push(`Suche: «${name}» führt nicht auf ${soll}`);
    if (!(await such(plz)).some(x => x.href === soll)) fehler.push(`Suche: Postleitzahl ${plz} führt nicht auf ${soll}`);
    // Eingabetaste öffnet den ersten Treffer
    const erste = (await such(name))[0];
    await start.press('#ortssuche', 'Enter');
    await start.waitForURL(u => u.pathname !== '/', { timeout: 5000 }).catch(() => {});
    if (erste && new URL(start.url()).pathname !== erste.href.split('#')[0]) fehler.push(`Suche: Eingabetaste öffnet nicht den ersten Treffer (${erste.href})`);
    await start.goto(basis + '/');
  }
  // 2. Ort in einem erfassten Kanton ohne eigene Seite: Kantonsseite mit Hinweis zum Ort
  const mitSeite = new Set(eigene.map(g => g.bfs));
  const o2 = orte.gemeinden.find(x => erfasst.includes(x[2]) && !mitSeite.has(x[0]));
  if (o2) {
    const t = (await such(o2[1])).find(x => x.href.startsWith(`${kantonSeite[o2[2]]}#ort=`));
    if (!t) fehler.push(`Suche: «${o2[1]}» führt nicht auf die Seite des Kantons ${o2[2].toUpperCase()}`);
    else {
      const h = await hinweis(t.href);
      if (!h.sichtbar || !h.text.includes(o2[1])) fehler.push(`${t.href}: Hinweis zum Ort fehlt`);
    }
    // Ein Ortsname aus der Adresse darf nie als HTML ausgeführt werden
    const h = await hinweis(`${kantonSeite[o2[2]]}#ort=` + encodeURIComponent('<img src=x onerror=alert(1)>'));
    if (h.dialog || h.kinder !== 'STRONG') fehler.push(`${kantonSeite[o2[2]]}: Der Hinweis zum Ort setzt HTML aus der Adresse ein`);
    const ohne = await hinweis(kantonSeite[o2[2]]);
    if (ohne.sichtbar) fehler.push(`${kantonSeite[o2[2]]}: Hinweis zum Ort erscheint ohne Ort`);
  }
  // 3. Ort in einem Kanton, der noch nicht erfasst ist: Regeln des Bundes mit Hinweis
  const o3 = orte.gemeinden.find(x => !erfasst.includes(x[2]));
  if (o3) {
    const t = (await such(o3[1])).find(x => x.href.startsWith(`/schweiz/#kt=${o3[2]}`));
    if (!t) fehler.push(`Suche: «${o3[1]}» führt nicht auf /schweiz/ (Kanton ${o3[2].toUpperCase()} ist nicht erfasst)`);
    else if (!(await hinweis(t.href)).sichtbar) fehler.push(`${t.href}: Hinweis «Kanton noch nicht erfasst» fehlt`);
  }
  if (erfasst.length && (await hinweis(`/schweiz/#kt=${erfasst[0]}`)).sichtbar) fehler.push(`/schweiz/: meldet den erfassten Kanton ${erfasst[0].toUpperCase()} als nicht erfasst`);
  // 4. Kanton über das Kürzel, andere Schreibweise, kein Treffer
  if (erfasst.length && !(await such(erfasst[0])).some(x => x.href === kantonSeite[erfasst[0]])) fehler.push(`Suche: Kürzel «${erfasst[0]}» findet den Kanton nicht`);
  if (!(await such('Genf')).some(x => x.text.includes('Genève'))) fehler.push('Suche: «Genf» findet Genève nicht');
  if ((await such('qqqq')).length || !(await start.textContent('#such-status')).trim()) fehler.push('Suche: Bei «qqqq» fehlt die Meldung «Kein Ort gefunden»');
  const ueber = await start.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  await such('Sankt');
  if (ueber > 0 || await start.evaluate(() => document.documentElement.scrollWidth - window.innerWidth) > 0) fehler.push('/: Die Trefferliste läuft seitlich über');

  const name = g => orte.gemeinden.find(x => x[0] === g.bfs)[1];
  // 4b. Suche auf den Seiten: Stichworte, Reihenfolge, Orte zuerst, nichts Fremdes
  async function seitenSuche(p, text) {
    await p.fill('#ortssuche', String(text));
    await p.waitForSelector('[data-suche][data-seiten]', { timeout: 8000 }).catch(() => {});
    if ((await p.getAttribute('[data-suche]', 'data-seiten')) !== 'bereit') fehler.push(`Suche: Verzeichnis der Seiten lädt nicht (${p.url()})`);
    return p.$$eval('#seitentreffer a', xs => xs.map(x => ({ href: x.getAttribute('href'), mark: x.querySelectorAll('mark').length })));
  }
  const maul = await seitenSuche(start, 'Maulkorb');
  if (!maul.length) fehler.push('Suche: «Maulkorb» findet keine Seite');
  else if (maul.length > 8) fehler.push('Suche: mehr als 8 Treffer auf den Seiten');
  else if (!maul.every(x => x.mark)) fehler.push('Suche: Ein Treffer für «Maulkorb» hebt das Wort nicht hervor');
  if (await start.isHidden('#seitentreffer')) fehler.push('Suche: Die Treffer auf den Seiten sind nicht sichtbar');
  for (const t of maul) {
    const [pfad, anker] = t.href.split('#');
    const datei = path.join(ROOT, pfad, 'index.html');
    if (!fs.existsSync(datei)) fehler.push(`Suche: Treffer führt auf ${t.href}, die Seite gibt es nicht`);
    else if (anker && !fs.readFileSync(datei, 'utf8').includes(`id="${anker}"`)) fehler.push(`Suche: Treffer führt auf ${t.href}, den Anker gibt es nicht`);
  }
  if (fs.existsSync(path.join(ROOT, 'be', 'lyss', 'index.html'))) {
    const lyss = await seitenSuche(start, 'Hundesteuer Lyss');
    if (!lyss.length || !lyss[0].href.startsWith('/be/lyss/')) fehler.push(`Suche: «Hundesteuer Lyss» nennt zuerst ${lyss[0] ? lyss[0].href : 'nichts'} statt /be/lyss/`);
  }
  // «Thema Ort» bei einem Ort ohne eigene Seite: der Ort und das Thema in seinem Kanton, nichts aus anderen Kantonen
  if (o2 && kantonSeite[o2[2]] === `/${o2[2]}/`) {
    const frage = `Hundesteuer ${o2[1]}`, t = await seitenSuche(start, frage);
    const ortsTreffer = await start.$$eval('#treffer a', xs => xs.map(x => x.getAttribute('href')));
    if (!ortsTreffer.some(h => h.startsWith(`/${o2[2]}/#ort=`))) fehler.push(`Suche: «${frage}» nennt den Ort nicht`);
    if (!t.some(x => x.href === `/${o2[2]}/#hundesteuer`)) fehler.push(`Suche: «${frage}» führt nicht auf /${o2[2]}/#hundesteuer`);
    if (t.some(x => x.href.split('#')[0] !== `/${o2[2]}/` && !x.href.endsWith(`#kt-${o2[2]}`))) fehler.push(`Suche: «${frage}» nennt Seiten ausserhalb des Kantons`);
    // Steht zum Thema nichts auf den Seiten, bleibt der Ort stehen, und die Statuszeile sagt es
    if ((await seitenSuche(start, `qqqq ${o2[1]}`)).length || !(await start.$$('#treffer a')).length) fehler.push(`Suche: «qqqq ${o2[1]}» zeigt nicht nur den Ort`);
  }
  // Ein Wort, das auf keiner Seite steht, führt über die Liste der gleichbedeutenden Wörter zu den Seiten
  if (!(await seitenSuche(start, 'Kampfhund')).some(x => x.href === '/thema/rassen/')) fehler.push('Suche: «Kampfhund» führt nicht auf /thema/rassen/');
  // Steht ein Wort auf einer Themenseite bei mehreren Kantonen, führt der Treffer an den Anfang der Seite
  if (maul.some(x => /^\/thema\/rassen\/#kt-/.test(x.href))) fehler.push('Suche: «Maulkorb» führt auf die Zeile eines Kantons statt auf /thema/rassen/');
  // Wörter, die nichts eingrenzen, fallen weg: Die Themenseite steht trotz «mein Hund» zuoberst
  const frei = await seitenSuche(start, 'mein Hund ist entlaufen');
  if (!frei.length || frei[0].href !== '/thema/vermisst/') fehler.push(`Suche: «mein Hund ist entlaufen» nennt zuerst ${frei[0] ? frei[0].href : 'nichts'} statt /thema/vermisst/`);
  const winti = eigene.find(g => g.l === 'de' && g.id === 'winterthur') ? 'Winterthur' : (eigene[0] && name(eigene[0]));
  if (winti) {
    await seitenSuche(start, winti);
    const erster = await start.$eval('#treffer, #seitentreffer', x => x.id).catch(() => '');
    if (!(await start.$$('#treffer a')).length || erster !== 'treffer') fehler.push(`Suche: «${winti}» zeigt nicht zuerst die Treffer für Orte`);
  }
  if ((await seitenSuche(start, 'qqqq')).length) fehler.push('Suche: «qqqq» findet Seiten');
  if (fremdSuche.length) fehler.push(`Suche: ruft fremde Adressen ab: ${fremdSuche[0]}`);
  if (await start.evaluate(() => document.documentElement.scrollWidth - window.innerWidth) > 0) fehler.push('/: Die Treffer auf den Seiten laufen seitlich über');

  // 5. Sprachen: Die deutsche Startseite führt bei einer Gemeinde ohne deutsche Seite auf die Fassung in der
  // anderen Sprache und nennt die Sprache. Jede Startseite einer anderen Sprache führt auf ihre eigenen Seiten,
  // bei einem Kanton ohne Fassung in ihrer Sprache auf die deutsche Seite.
  const fremd = eigene.find(g => g.l !== 'de' && !eigene.some(x => x.l === 'de' && x.bfs === g.bfs));
  if (fremd) {
    const t = (await such(name(fremd))).find(x => x.href === `${fremd.pre}/${fremd.kanton}/${fremd.id}/`);
    if (!t) fehler.push(`Suche: «${name(fremd)}» führt auf der deutschen Startseite nicht auf ${fremd.pre}/${fremd.kanton}/${fremd.id}/`);
    else if (!/auf (Französisch|Italienisch)/.test(t.text)) fehler.push(`Suche: Treffer «${name(fremd)}» nennt die Sprache der Seite nicht`);
  }
  for (const [l, pre] of SPRACHEN.slice(1)) {
    if (!seiten.includes(pre + '/')) continue;
    const p = await ctx.newPage();
    p.on('pageerror', err => fehler.push(`${pre}/: Skriptfehler in der Suche: ` + err.message));
    await p.goto(basis + pre + '/');
    const suchHier = async text => {
      await p.fill('#ortssuche', String(text));
      await p.waitForSelector('[data-suche][data-stand="bereit"]', { timeout: 8000 }).catch(() => {});
      return p.$$eval('#treffer a', xs => xs.map(x => ({ text: x.textContent, href: x.getAttribute('href') })));
    };
    if (await p.isHidden('#ortssuche')) fehler.push(`${pre}/: Das Suchfeld ist nicht sichtbar`);
    const g = eigene.find(x => x.l === l);
    if (g && !(await suchHier(name(g))).some(x => x.href === `${pre}/${g.kanton}/${g.id}/`)) fehler.push(`${pre}/: Suche «${name(g)}» führt nicht auf ${pre}/${g.kanton}/${g.id}/`);
    const nurDe = erfasst.find(kt => kantonSeite[kt] === `/${kt}/` && !fs.existsSync(path.join(ROOT, pre.slice(1), kt, 'index.html')));
    const wort = { fr: 'muselière', it: 'museruola' }[l];
    if (wort && !(await seitenSuche(p, wort)).length) fehler.push(`${pre}/: Suche «${wort}» findet keine Seite`);
    if (nurDe && !(await suchHier(nurDe)).some(x => x.href === `/${nurDe}/`)) fehler.push(`${pre}/: Kürzel «${nurDe}» führt nicht auf die deutsche Seite /${nurDe}/`);
    if (await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth) > 0) fehler.push(`${pre}/: Die Trefferliste läuft seitlich über`);
    await p.close();
  }

  // 6. Quellenverzeichnis: je Sprache genau die Quellen, die Seiten dieser Sprache zitieren (jeder Link mit
  // target="_blank" auf einer Seite ausser dem Verzeichnis selbst). Die Links unter «zitiert auf» prüft die
  // Linkprüfung oben wie jeden internen Link. Wahl «ZH», Suche «Hundegesetz», nichts Fremdes.
  const extern = html => new Set([...html.matchAll(/<a href="(https?:\/\/[^"]+)" target="_blank"/g)].map(m => m[1]));
  for (const [l, pre] of SPRACHEN) {
    const qpfad = `${pre}/quellen/`;
    if (!seiten.includes(qpfad)) { if (seiten.includes(pre + '/')) fehler.push(`${qpfad}: Das Quellenverzeichnis fehlt`); continue; }
    const soll = new Set();
    for (const s of seiten) {
      if (s === qpfad || s === '/404.html' || sollLang(s) !== SPRACHEN.find(x => x[0] === l)[3]) continue;
      for (const u of extern(fs.readFileSync(datei(s), 'utf8'))) soll.add(u);
    }
    const qhtml = fs.readFileSync(datei(qpfad), 'utf8');
    const ist = new Set([...qhtml.matchAll(/<p class="q-lang"><a href="([^"]+)"/g)].map(m => m[1]));
    for (const u of soll) if (!ist.has(u)) fehler.push(`${qpfad}: Quelle fehlt im Verzeichnis: ${u}`);
    for (const u of ist) if (!soll.has(u)) fehler.push(`${qpfad}: Quelle steht im Verzeichnis, aber auf keiner Seite: ${u}`);
    const p = await ctx.newPage();
    const fremdQ = [];
    p.on('request', r => { if (!r.url().startsWith(basis)) fremdQ.push(r.url()); });
    p.on('pageerror', err => fehler.push(`${qpfad}: Skriptfehler: ` + err.message));
    await p.goto(basis + qpfad);
    if (await p.isHidden('#quellensuche')) fehler.push(`${qpfad}: Das Suchfeld ist nicht sichtbar`);
    const sichtbar = () => p.$$eval('.q-liste > li.q', xs => xs.filter(x => !x.hidden).map(x => x.getAttribute('data-kt')));
    await p.click('.q-k[data-kt="zh"]');
    const zh = await sichtbar();
    if (!zh.length || zh.some(k => k !== 'zh')) fehler.push(`${qpfad}: Die Wahl «ZH» zeigt ${zh.length} Quellen, davon ${zh.filter(k => k !== 'zh').length} aus anderen Kantonen`);
    // «Alle» ohne Suchwort ist die Übersicht: je Kanton eine Zeile mit der Zahl seiner Quellen, keine Quelle offen.
    // Die Zahlen ergeben zusammen alle Quellen. Ein Tipp auf die Zeile wählt den Kanton, ein zweiter führt zurück.
    const alleQ = (qhtml.match(/<li class="q" /g) || []).length;
    await p.click('.q-k[data-kt=""]');
    if ((await sichtbar()).length) fehler.push(`${qpfad}: «Alle» zeigt ohne Suchwort Quellen statt der Übersicht`);
    const zeilen = await p.$$eval('.q-gruppe', xs => xs.filter(x => !x.hidden).map(x => parseInt(x.querySelector('.q-g-zahl').textContent, 10)));
    if (zeilen.reduce((a, b) => a + b, 0) !== alleQ) fehler.push(`${qpfad}: Die Übersicht zählt ${zeilen.reduce((a, b) => a + b, 0)} statt ${alleQ} Quellen`);
    await p.click('.q-gruppe[data-gruppe="zh"] button');
    const zh2 = await sichtbar();
    if (zh2.length !== zh.length || zh2.some(k => k !== 'zh')) fehler.push(`${qpfad}: Die Zeile «Zürich» der Übersicht zeigt nicht die Quellen des Kantons`);
    if ((await p.getAttribute('.q-k[data-kt="zh"]', 'aria-pressed')) !== 'true') fehler.push(`${qpfad}: Die Zeile «Zürich» drückt das Quadrat ZH nicht`);
    await p.click('.q-gruppe[data-gruppe="zh"] button');
    if ((await sichtbar()).length) fehler.push(`${qpfad}: Der zweite Tipp auf die Zeile führt nicht zur Übersicht zurück`);
    if (l === 'de') {
      await p.fill('#quellensuche', 'Hundegesetz');
      if (!(await sichtbar()).length) fehler.push(`${qpfad}: Die Suche nach «Hundegesetz» findet keine Quelle`);
      await p.fill('#quellensuche', 'qqqq');
      if ((await sichtbar()).length) fehler.push(`${qpfad}: Die Suche nach «qqqq» findet Quellen`);
      await p.fill('#quellensuche', '');
    }
    await p.click('[data-sort="name"]');
    const namen = await p.$$eval('.q-liste > li.q', xs => xs.map(x => +x.getAttribute('data-n')));
    if (namen.some((n, i) => i && n < namen[i - 1])) fehler.push(`${qpfad}: «Nach Name» sortiert nicht`);
    if ((await sichtbar()).length !== alleQ) fehler.push(`${qpfad}: «Nach Name» zeigt nicht alle Quellen`);
    if (!(await p.$$eval('.q-gruppe', xs => xs.every(x => x.hidden)))) fehler.push(`${qpfad}: «Nach Name» zeigt die Überschriften der Kantone`);
    if (await p.$eval('#q-status', x => !x.textContent)) fehler.push(`${qpfad}: Die Statuszeile ist leer`);
    if (fremdQ.length) fehler.push(`${qpfad}: ruft fremde Adressen ab: ${fremdQ[0]}`);
    await p.close();
  }

  await browser.close();
  server.close();
  if (fehler.length) { console.log(`FEHLER (${fehler.length}):`); fehler.forEach(f => console.log('  - ' + f)); process.exit(1); }
  console.log(`In Ordnung: ${seiten.length} Seiten in 2 Breiten und die Suche geprüft.`);
})();
