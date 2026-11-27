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
        wald: [...document.querySelectorAll('[data-wald]')].map(x => ({ saison: x.getAttribute('data-saison'), gross: x.querySelector('[data-heute-gross]').className, heute: !!x.querySelector('.now'), datum: x.querySelector('[data-heute-datum]').textContent }))
      }));
      if (info.ueberlauf > 0) fehler.push(`${wo}: läuft seitlich über (${info.ueberlauf}px)`);
      if (info.h1 !== 1) fehler.push(`${wo}: ${info.h1} Hauptüberschriften statt 1`);
      if (!info.titel) fehler.push(`${wo}: kein Seitentitel`);
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
        }
      }
      if (sprache && s.endsWith('/thema/vermisst/')) {
        const soll = ordner(...sprache[2], 'kantone').filter(f => f.endsWith('.json') && lies(...sprache[2], 'kantone', f).vermisst).length;
        const t = await page.evaluate(() => ({ kantone: document.querySelectorAll('[data-vermisst]').length, mitQuelle: [...document.querySelectorAll('[data-vermisst]')].filter(x => x.querySelector('.src a') && x.querySelector('h3 a')).length, bund: document.querySelectorAll('.card .src a').length, tabellen: document.querySelectorAll('table').length }));
        if (t.kantone !== soll || t.mitQuelle !== soll) fehler.push(`${wo}: ${t.kantone} Kantone, davon ${t.mitQuelle} mit Quelle und Link, statt ${soll} (jeder Kanton mit dem Feld 'vermisst')`);
        if (!t.bund || t.tabellen) fehler.push(`${wo}: Karte des Bundes mit Quelle fehlt, oder die Seite hat eine Tabelle`);
      } else if (sprache) {
        const kantone = ordner(...sprache[2], 'kantone').filter(f => f.endsWith('.json')).length;
        const t = await page.evaluate(() => ({ zeilen: document.querySelectorAll('tbody tr').length, karten: document.querySelectorAll('.card').length, quellen: document.querySelectorAll('.card .src a').length }));
        if (t.zeilen !== kantone || t.karten !== kantone) fehler.push(`${wo}: ${t.zeilen} Zeilen und ${t.karten} Karten statt je ${kantone} (eine pro Kanton in dieser Sprache)`);
        if (t.quellen < kantone) fehler.push(`${wo}: Karte ohne Quelle`);
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
    const soll = datei(quelle) ? JSON.parse(fs.readFileSync(datei(quelle), 'utf8')).zonen.length : -1;
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
      const erste = await p.$('[data-karte-zeige]');
      if (!erste) fehler.push(`${s}: Die Liste der Freilaufzonen fehlt`);
      else {
        const name = (await erste.textContent()).trim();
        await erste.click();
        await p.waitForSelector('[data-karte-info]:not([hidden])', { timeout: 5000 }).catch(() => {});
        const info = await p.$eval('[data-karte-info]', x => x.hidden ? '' : x.textContent);
        if (!name || !info.includes(name)) fehler.push(`${s}: Ein Tipp auf «${name}» zeigt die Zone nicht an`);
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

  // 5. Sprachen: Die deutsche Startseite führt bei einer Gemeinde ohne deutsche Seite auf die Fassung in der
  // anderen Sprache und nennt die Sprache. Jede Startseite einer anderen Sprache führt auf ihre eigenen Seiten,
  // bei einem Kanton ohne Fassung in ihrer Sprache auf die deutsche Seite.
  const name = g => orte.gemeinden.find(x => x[0] === g.bfs)[1];
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
    if (nurDe && !(await suchHier(nurDe)).some(x => x.href === `/${nurDe}/`)) fehler.push(`${pre}/: Kürzel «${nurDe}» führt nicht auf die deutsche Seite /${nurDe}/`);
    if (await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth) > 0) fehler.push(`${pre}/: Die Trefferliste läuft seitlich über`);
    await p.close();
  }

  await browser.close();
  server.close();
  if (fehler.length) { console.log(`FEHLER (${fehler.length}):`); fehler.forEach(f => console.log('  - ' + f)); process.exit(1); }
  console.log(`In Ordnung: ${seiten.length} Seiten in 2 Breiten und die Ortssuche geprüft.`);
})();
