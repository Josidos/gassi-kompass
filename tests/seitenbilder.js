// Speichert ganze Seiten als Bild, damit sich zwei Stände Byte für Byte vergleichen lassen, ohne dass
// jemand die Bilder ansieht.
//   node tests/seitenbilder.js <ordner>                 je eine Seite jeder Seitenart, 1280 und 390 Pixel, Zeiger Maus
//   node tests/seitenbilder.js <ordner> 1280 /zh/ /     nur diese Breite und diese Seiten
// Gebrauch vor und nach einer Änderung an assets/site.css oder build.py:
//   node tests/seitenbilder.js /tmp/vorher   (alter Stand)     node tests/seitenbilder.js /tmp/nachher   (neuer Stand)
//   diff -rq /tmp/vorher /tmp/nachher        nennt nur die Bilder, die sich unterscheiden
// Als Bild ansehen muss man danach nur, was sich geändert hat. Die Tafel «Leine im Wald» zeigt das heutige Datum:
// Beide Stände am selben Tag aufnehmen. Siehe «Telefon und Berührung» in handbuch/generator.md.
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
const TYP = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2' };
const MUSTER = ['/', '/zh/', '/zh/zuerich/', '/lu/luzern/', '/thema/hundesteuer/', '/thema/vermisst/', '/schweiz/', '/ueber/', '/fr-ch/', '/fr-ch/ge/', '/fr-ch/ge/geneve/', '/fr-ch/thema/hundesteuer/', '/it-ch/', '/it-ch/ti/', '/it-ch/ti/lugano/', '/it-ch/schweiz/'];

function datei(url) {
  let p = decodeURIComponent(url.split('#')[0].split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const voll = path.join(ROOT, p);
  return voll.startsWith(ROOT) && fs.existsSync(voll) && fs.statSync(voll).isFile() ? voll : null;
}

(async () => {
  const [ordner, ...rest] = process.argv.slice(2);
  if (!ordner) { console.log('Aufruf: node tests/seitenbilder.js <ordner> [breite ...] [pfad ...]'); process.exit(1); }
  const breiten = rest.filter(a => /^\d+$/.test(a)).map(Number);
  const pfade = rest.filter(a => a.startsWith('/'));
  fs.mkdirSync(ordner, { recursive: true });
  const server = http.createServer((req, res) => {
    const f = datei(req.url);
    if (!f) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': TYP[path.extname(f)] || 'application/octet-stream' });
    res.end(fs.readFileSync(f));
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const basis = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch();
  let n = 0;
  for (const breite of (breiten.length ? breiten : [1280, 390])) {
    const ctx = await browser.newContext({ viewport: { width: breite, height: 900 }, deviceScaleFactor: 1 });
    for (const s of (pfade.length ? pfade : MUSTER).filter(datei)) {
      const page = await ctx.newPage();
      await page.goto(basis + s, { waitUntil: 'networkidle' });
      await page.screenshot({ path: path.join(ordner, (s.replace(/\//g, '_') || '_') + '-' + breite + '.png'), fullPage: true });
      await page.close(); n++;
    }
    await ctx.close();
  }
  await browser.close();
  server.close();
  console.log(`${n} Bilder in ${ordner}`);
})();
