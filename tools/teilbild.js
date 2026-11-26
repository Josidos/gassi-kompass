// Erzeugt die Vorschaubilder für geteilte Links (og:image), eines je Sprache:
// assets/teilen-de.png, assets/teilen-fr.png, assets/teilen-it.png (1200 x 630).
// Aufruf: node tools/teilbild.js   Nur nötig, wenn sich Texte, Farben oder Schriften ändern.
// Farben und Schriften aus DESIGN.md: Einband-Moosgrün, Kürzel im Rost-Quadrat, Archivo schmal, Source Serif 4.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
// Schriften als Daten einbetten: Eine Seite aus setContent darf keine Dateien vom Datenträger laden.
const schrift = name => 'data:font/woff2;base64,' + fs.readFileSync(path.join(ROOT, 'assets', 'fonts', name)).toString('base64');
const KANTONE = 'ZH BE LU UR SZ OW NW GL ZG FR SO BS BL SH AR AI SG GR AG TG TI VD VS NE GE JU'.split(' ');
const TEXTE = {
  de: ['Was gilt für deinen Hund hier?', 'Hunderegeln der Schweiz nach Kanton und Gemeinde. Mit amtlicher Quelle zu jeder Angabe.'],
  fr: ['Quelles règles pour votre chien ici ?', 'Les règles pour les chiens en Suisse, par canton et par commune. Avec la source officielle de chaque indication.'],
  it: ['Cosa vale qui per il tuo cane?', 'Le regole per i cani in Svizzera, per Cantone e Comune. Con la fonte ufficiale per ogni indicazione.'],
};
const seite = (lang, [titel, satz]) => `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><style>
@font-face{font-family:"Archivo";src:url("${schrift('archivo.woff2')}") format("woff2");font-weight:100 900;font-stretch:62% 125%}
@font-face{font-family:"Source Serif 4";src:url("${schrift('sourceserif4.woff2')}") format("woff2");font-weight:200 900}
html,body{margin:0}
body{width:1200px;height:630px;box-sizing:border-box;padding:60px 72px 56px;background:#1E3B2C;color:#F1F5EF;display:flex;flex-direction:column;justify-content:space-between}
.marke{font:700 30px "Archivo",sans-serif;font-stretch:90%;letter-spacing:.08em;text-transform:uppercase;color:#BFD0C3}
h1{font:800 96px/1.02 "Archivo",sans-serif;font-stretch:76%;margin:0;max-width:1000px;text-wrap:balance}
p{font:400 35px/1.34 "Source Serif 4",serif;margin:24px 0 0;max-width:940px}
.register{display:flex;gap:6px}
.kz{flex:1;height:40px;display:grid;place-items:center;background:#B8451F;color:#FFF8F4;font:800 18px "Archivo",sans-serif;font-stretch:78%;border-radius:2px}
</style></head><body>
<div class="marke">Gassi-Kompass</div>
<div><h1>${titel}</h1><p>${satz}</p></div>
<div class="register">${KANTONE.map(k => `<span class="kz">${k}</span>`).join('')}</div>
</body></html>`;
(async () => {
  const b = await chromium.launch();
  for (const lang of Object.keys(TEXTE)) {
    const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
    await p.setContent(seite(lang, TEXTE[lang]));
    await p.evaluate(() => document.fonts.ready);
    const geladen = await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).join(', '));
    if (!/Archivo/.test(geladen) || !/Source Serif/.test(geladen)) throw new Error('Schriften nicht geladen: ' + geladen);
    await p.waitForTimeout(200);
    const ziel = path.join(ROOT, 'assets', `teilen-${lang}.png`);
    await p.screenshot({ path: ziel, type: 'png' });
    console.log(ziel);
    await p.close();
  }
  await b.close();
})();
