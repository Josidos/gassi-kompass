// Prüft die gebauten Seiten in einem echten Browser (Playwright, 390 px breit).
//   node tests/seiten.js                 prüft alle Seiten aus sitemap.xml und 404.html
//   node tests/seiten.js /lu/luzern/ bild.png   macht zusätzlich ein Bildschirmfoto dieser Seite
// Geprüft wird: Seite lädt, keine Skriptfehler, kein seitliches Überlaufen,
// alle internen Links und Dateien existieren, der Wald-Status wird gesetzt.
// Der Test bricht auch ab, wenn eine Adresse aus dem letzten Commit in der Sitemap fehlt.
// Soll eine Seite wirklich verschwinden: node tests/seiten.js --entfernen-erlaubt
const http = require('http'), fs = require('fs'), path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
const TYP = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.xml': 'application/xml', '.txt': 'text/plain' };

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
  const [fotoSeite, fotoDatei] = process.argv.slice(2).filter(a => !a.startsWith('--'));
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  const fehler = [];
  // Keine veröffentlichte Adresse darf verschwinden (Vergleich mit der Sitemap im letzten Commit)
  if (!process.argv.includes('--entfernen-erlaubt')) {
    let alt = '';
    try { alt = execFileSync('git', ['show', 'HEAD:sitemap.xml'], { cwd: ROOT, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }); } catch (e) { /* kein Git: nichts zu vergleichen */ }
    for (const m of alt.matchAll(/<loc>https:\/\/[^/]+([^<]*)<\/loc>/g)) {
      if (!seiten.includes(m[1])) fehler.push(`${m[1]}: Adresse war veröffentlicht und fehlt jetzt. Adressen nie ändern, siehe CLAUDE.md.`);
    }
  }
  for (const s of seiten) {
    const page = await ctx.newPage();
    const meldungen = [];
    page.on('console', m => { if (m.type() === 'error') meldungen.push(m.text()); });
    page.on('pageerror', err => meldungen.push('Skriptfehler: ' + err.message));
    page.on('requestfailed', r => meldungen.push('Laden fehlgeschlagen: ' + r.url()));
    const antwort = await page.goto(basis + s, { waitUntil: 'load' });
    if (!antwort || antwort.status() !== 200) fehler.push(`${s}: Status ${antwort && antwort.status()}`);
    for (const m of meldungen) fehler.push(`${s}: ${m}`);
    const info = await page.evaluate(() => ({
      ueberlauf: document.documentElement.scrollWidth - window.innerWidth,
      h1: document.querySelectorAll('h1').length,
      titel: document.title,
      links: [...document.querySelectorAll('a[href^="/"], link[href^="/"], script[src^="/"]')].map(x => x.getAttribute('href') || x.getAttribute('src')),
      wald: [...document.querySelectorAll('[data-wald]')].map(x => ({ saison: x.getAttribute('data-saison'), gross: x.querySelector('[data-heute-gross]').textContent, heute: !!x.querySelector('.now'), datum: x.querySelector('[data-heute-datum]').textContent }))
    }));
    if (info.ueberlauf > 0) fehler.push(`${s}: läuft seitlich über (${info.ueberlauf}px)`);
    if (info.h1 !== 1) fehler.push(`${s}: ${info.h1} Hauptüberschriften statt 1`);
    if (!info.titel) fehler.push(`${s}: kein Seitentitel`);
    for (const l of new Set(info.links)) if (!datei(l)) fehler.push(`${s}: Link ohne Ziel: ${l}`);
    for (const w of info.wald) {
      if (!w.heute || !w.datum) fehler.push(`${s}: Heute-Markierung oder Datum fehlt`);
      if (w.saison === '1' && !/^Heute /.test(w.gross)) fehler.push(`${s}: Wald-Status wurde nicht gesetzt`);
    }
    if (s === fotoSeite && fotoDatei) await page.screenshot({ path: fotoDatei, fullPage: true });
    await page.close();
  }
  // Ortsfilter der Startseite
  const start = await ctx.newPage();
  await start.goto(basis + '/');
  await start.fill('#ortsfilter', 'luzern');
  const sichtbar = await start.$$eval('.dest', xs => xs.filter(x => !x.hidden && x.offsetParent !== null).length);
  if (sichtbar < 1) fehler.push('/: Ortsfilter findet «luzern» nicht');
  await start.fill('#ortsfilter', 'qqqq');
  if (await start.isHidden('#kein-treffer')) fehler.push('/: Hinweis «Kein Treffer» erscheint nicht');
  await browser.close();
  server.close();
  if (fehler.length) { console.log(`FEHLER (${fehler.length}):`); fehler.forEach(f => console.log('  - ' + f)); process.exit(1); }
  console.log(`In Ordnung: ${seiten.length} Seiten geprüft.`);
})();
