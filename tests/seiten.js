// Prüft die gebauten Seiten in einem echten Browser (Playwright), schmal (390 px) und breit (1280 px).
//   node tests/seiten.js                            prüft alle Seiten aus sitemap.xml und 404.html
//   node tests/seiten.js /lu/luzern/ bild.png       macht zusätzlich ein Bildschirmfoto dieser Seite (390 px)
//   node tests/seiten.js /lu/luzern/ bild.png 1280  dasselbe in 1280 px Breite
// Geprüft wird: Seite lädt, keine Skriptfehler, kein seitliches Überlaufen, genau eine Hauptüberschrift,
// alle internen Links und Dateien existieren, der Wald-Status wird gesetzt, die Ortssuche findet Orte
// und führt auf die richtige Seite.
// Der Test bricht auch ab, wenn eine Adresse aus dem letzten Commit in der Sitemap fehlt.
// Soll eine Seite wirklich verschwinden: node tests/seiten.js --entfernen-erlaubt
const http = require('http'), fs = require('fs'), path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
const TYP = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.xml': 'application/xml', '.txt': 'text/plain' };
const lies = (...teile) => JSON.parse(fs.readFileSync(path.join(ROOT, ...teile), 'utf8'));

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

  // Keine veröffentlichte Adresse darf verschwinden (Vergleich mit der Sitemap im letzten Commit)
  if (!process.argv.includes('--entfernen-erlaubt')) {
    let alt = '';
    try { alt = execFileSync('git', ['show', 'HEAD:sitemap.xml'], { cwd: ROOT, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }); } catch (e) { /* kein Git: nichts zu vergleichen */ }
    for (const m of alt.matchAll(/<loc>https:\/\/[^/]+([^<]*)<\/loc>/g)) {
      if (!seiten.includes(m[1])) fehler.push(`${m[1]}: Adresse war veröffentlicht und fehlt jetzt. Adressen nie ändern, siehe CLAUDE.md.`);
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
        links: [...document.querySelectorAll('a[href^="/"], link[href^="/"], script[src^="/"]')].map(x => x.getAttribute('href') || x.getAttribute('src')),
        wald: [...document.querySelectorAll('[data-wald]')].map(x => ({ saison: x.getAttribute('data-saison'), gross: x.querySelector('[data-heute-gross]').textContent, heute: !!x.querySelector('.now'), datum: x.querySelector('[data-heute-datum]').textContent }))
      }));
      if (info.ueberlauf > 0) fehler.push(`${wo}: läuft seitlich über (${info.ueberlauf}px)`);
      if (info.h1 !== 1) fehler.push(`${wo}: ${info.h1} Hauptüberschriften statt 1`);
      if (!info.titel) fehler.push(`${wo}: kein Seitentitel`);
      for (const l of new Set(info.links)) if (!datei(l)) fehler.push(`${wo}: Link ohne Ziel: ${l}`);
      for (const w of info.wald) {
        if (!w.heute || !w.datum) fehler.push(`${wo}: Heute-Markierung oder Datum fehlt`);
        if (w.saison === '1' && !/^Heute /.test(w.gross)) fehler.push(`${wo}: Wald-Status wurde nicht gesetzt`);
      }
      if (s === fotoSeite && fotoDatei && breite === Number(fotoBreite || 390)) await page.screenshot({ path: fotoDatei, fullPage: true });
      await page.close();
    }
    await ctx.close();
  }

  // Ortssuche: Die Erwartungen kommen aus den Daten, damit der Test mit jedem neuen Kanton weiter stimmt.
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  const orte = lies('data', 'orte.json');
  const erfasst = fs.readdirSync(path.join(ROOT, 'data', 'kantone')).filter(f => f.endsWith('.json')).map(f => f.slice(0, -5));
  const eigene = [];
  for (const kt of fs.readdirSync(path.join(ROOT, 'data', 'gemeinden'))) {
    for (const f of fs.readdirSync(path.join(ROOT, 'data', 'gemeinden', kt))) if (f.endsWith('.json')) eigene.push(lies('data', 'gemeinden', kt, f));
  }
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
    const t = (await such(o2[1])).find(x => x.href.startsWith(`/${o2[2]}/#ort=`));
    if (!t) fehler.push(`Suche: «${o2[1]}» führt nicht auf die Seite des Kantons ${o2[2].toUpperCase()}`);
    else {
      const h = await hinweis(t.href);
      if (!h.sichtbar || !h.text.includes(o2[1])) fehler.push(`${t.href}: Hinweis zum Ort fehlt`);
    }
    // Ein Ortsname aus der Adresse darf nie als HTML ausgeführt werden
    const h = await hinweis(`/${o2[2]}/#ort=` + encodeURIComponent('<img src=x onerror=alert(1)>'));
    if (h.dialog || h.kinder !== 'STRONG') fehler.push(`/${o2[2]}/: Der Hinweis zum Ort setzt HTML aus der Adresse ein`);
    const ohne = await hinweis(`/${o2[2]}/`);
    if (ohne.sichtbar) fehler.push(`/${o2[2]}/: Hinweis zum Ort erscheint ohne Ort`);
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
  if (erfasst.length && !(await such(erfasst[0])).some(x => x.href === `/${erfasst[0]}/`)) fehler.push(`Suche: Kürzel «${erfasst[0]}» findet den Kanton nicht`);
  if (!(await such('Genf')).some(x => x.text.includes('Genève'))) fehler.push('Suche: «Genf» findet Genève nicht');
  if ((await such('qqqq')).length || !(await start.textContent('#such-status')).trim()) fehler.push('Suche: Bei «qqqq» fehlt die Meldung «Kein Ort gefunden»');
  const ueber = await start.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  await such('Sankt');
  if (ueber > 0 || await start.evaluate(() => document.documentElement.scrollWidth - window.innerWidth) > 0) fehler.push('/: Die Trefferliste läuft seitlich über');

  await browser.close();
  server.close();
  if (fehler.length) { console.log(`FEHLER (${fehler.length}):`); fehler.forEach(f => console.log('  - ' + f)); process.exit(1); }
  console.log(`In Ordnung: ${seiten.length} Seiten in 2 Breiten und die Ortssuche geprüft.`);
})();
