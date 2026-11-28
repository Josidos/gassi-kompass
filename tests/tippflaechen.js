// Prüft die Tippflächen auf dem Telefon (Emulation eines iPhone 13, Zeiger «Finger»).
//   node tests/tippflaechen.js                 prüft je eine Seite jeder Seitenart in den drei Sprachen
//   node tests/tippflaechen.js /zh/ /ueber/    prüft nur diese Seiten
// Gemessen wird durch die Mitte jedes Ziels (Link, Knopf, Feld, summary): wie viele Pixel nach oben und unten
// ein Tipp noch dieses Ziel trifft. Das ist die wirkliche Tippfläche, auch wenn sie unsichtbar über das Ziel
// hinausreicht oder ein Nachbar einen Teil davon nimmt. Links mitten im Lauftext zählen getrennt.
// Fehler: ein freies Ziel unter 28 Pixeln Tipphöhe, oder die Seite läuft seitlich über. Hinweis: unter 40 Pixeln.
// Laufen lassen nach jeder Änderung an assets/site.css oder an den Bausteinen in build.py, siehe
// «Telefon und Berührung» in handbuch/generator.md. Der tägliche Lauf braucht ihn nicht.
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium, devices } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
const TYP = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2' };
const MUSTER = ['/', '/zh/', '/zh/zuerich/', '/lu/luzern/', '/thema/hundesteuer/', '/thema/vermisst/', '/schweiz/', '/ueber/', '/fr-ch/', '/fr-ch/ge/', '/fr-ch/ge/geneve/', '/fr-ch/thema/hundesteuer/', '/it-ch/', '/it-ch/ti/', '/it-ch/ti/lugano/', '/it-ch/schweiz/'];
const FEHLER_UNTER = 28, HINWEIS_UNTER = 40;

function datei(url) {
  let p = decodeURIComponent(url.split('#')[0].split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const voll = path.join(ROOT, p);
  return voll.startsWith(ROOT) && fs.existsSync(voll) && fs.statSync(voll).isFile() ? voll : null;
}

(async () => {
  const server = http.createServer((req, res) => {
    const f = datei(req.url);
    if (!f) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': TYP[path.extname(f)] || 'application/octet-stream' });
    res.end(fs.readFileSync(f));
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const basis = 'http://127.0.0.1:' + server.address().port;
  const gewuenscht = process.argv.slice(2).filter(a => a.startsWith('/'));
  const seiten = (gewuenscht.length ? gewuenscht : MUSTER).filter(s => { if (datei(s)) return true; console.log(`Übersprungen, Seite fehlt: ${s}`); return false; });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ ...devices['iPhone 13'] });
  const fehler = [], hinweise = [];
  let ziele = 0, knapp = 0;
  for (const s of seiten) {
    const page = await ctx.newPage();
    await page.goto(basis + s, { waitUntil: 'networkidle' });
    const grob = await page.evaluate(() => matchMedia('(pointer:coarse)').matches);
    if (!grob) fehler.push(`${s}: Die Emulation meldet keinen Finger als Zeiger, die Messung gilt nicht.`);
    const hoehe = await page.evaluate(() => document.documentElement.scrollHeight);
    await page.setViewportSize({ width: 390, height: Math.min(hoehe + 20, 30000) });
    await page.waitForTimeout(120);
    const r = await page.evaluate(() => {
      const sichtbar = el => { const st = getComputedStyle(el), q = el.getBoundingClientRect(); return st.display !== 'none' && st.visibility !== 'hidden' && q.width > 0 && q.height > 0; };
      const vw = document.documentElement.clientWidth;
      const trifft = (el, x, y) => { const t = document.elementFromPoint(x, y); return !!t && (t === el || el.contains(t) || (t.tagName === 'LABEL' && t.control === el)); };
      const liste = [];
      for (const el of [...document.querySelectorAll('a[href], button, input, select, textarea, summary')].filter(sichtbar)) {
        if (el.classList.contains('skip')) continue;
        const q = el.getBoundingClientRect();
        if (q.top > 29900) continue;
        const cx = Math.min(vw - 1, Math.max(0, q.left + Math.min(q.width / 2, 40))), cy = q.top + q.height / 2;
        let oben = 0, unten = 0;
        const mitte = trifft(el, cx, cy);
        if (mitte) { while (oben < 60 && trifft(el, cx, cy - oben - 1)) oben++; while (unten < 60 && trifft(el, cx, cy + unten + 1)) unten++; }
        const eltern = el.parentElement;
        const imText = !!eltern && getComputedStyle(el).display.startsWith('inline') && !['inline-flex', 'inline-block', 'inline-grid'].includes(getComputedStyle(el).display) && [...eltern.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
        liste.push({ t: (el.innerText || el.value || el.getAttribute('aria-label') || el.tagName).trim().replace(/\s+/g, ' ').slice(0, 40), wo: (el.className || (eltern && (eltern.className || eltern.tagName)) || '').toString().slice(0, 24), th: mitte ? oben + unten + 1 : 0, imText });
      }
      return { liste, ueberlauf: document.documentElement.scrollWidth > vw };
    });
    if (r.ueberlauf) fehler.push(`${s}: Die Seite läuft bei 390 Pixeln seitlich über.`);
    for (const z of r.liste) {
      if (z.imText) continue;
      ziele++;
      if (z.th < FEHLER_UNTER) fehler.push(`${s}: Tippfläche von «${z.t}» (${z.wo}) ist nur ${z.th} Pixel hoch.`);
      else if (z.th < HINWEIS_UNTER) { knapp++; hinweise.push(`${s}: «${z.t}» (${z.wo}) ${z.th} Pixel`); }
    }
    await page.close();
  }
  await browser.close();
  server.close();
  if (hinweise.length) { console.log(`Hinweis, ${knapp} Ziele unter ${HINWEIS_UNTER} Pixeln:`); for (const h of hinweise.slice(0, 12)) console.log('  ' + h); if (hinweise.length > 12) console.log(`  und ${hinweise.length - 12} weitere`); }
  if (fehler.length) { console.log(`FEHLER (${fehler.length}):`); for (const f of fehler.slice(0, 40)) console.log('  ' + f); process.exit(1); }
  console.log(`In Ordnung: ${seiten.length} Seiten, ${ziele} freie Ziele, keines unter ${FEHLER_UNTER} Pixeln Tipphöhe, ${knapp} unter ${HINWEIS_UNTER}.`);
})();
