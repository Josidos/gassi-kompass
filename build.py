#!/usr/bin/env python3
"""Baut gassi-kompass.ch aus den Dateien in data/ (nur Python-Standardbibliothek).

    python3 build.py          prüft die Daten und schreibt alle Seiten
    python3 build.py --check  prüft nur, schreibt nichts

Erzeugt werden: index.html, 404.html, sitemap.xml, robots.txt, ueber/,
<kanton>/ und <kanton>/<gemeinde>/. Diese Ausgaben nie von Hand ändern:
Daten in data/ oder dieses Skript anpassen und neu bauen.
"""
import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SITE = "https://gassi-kompass.ch"
MARKE = ".erzeugt"  # liegt in jedem erzeugten Ordner, damit er beim Neubau ersetzt werden darf

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]
MON3 = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
TAGE = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
TOENE = {"must", "none", "note", "free"}
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MMTT = re.compile(r"^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")
RESERVIERT = {"assets", "data", "tests", "ueber"}
VERGLEICH = [("wald", "Leine im Wald"), ("haft", "Haftpflicht"), ("kurs", "Kurs"),
             ("rassen", "Rassen"), ("steuer", "Hundesteuer"), ("anm", "Anmeldung")]
MIN_LOKAL = 3  # so viele belegte lokale Angaben braucht eine Gemeinde für eine eigene Seite
# Feste Dateien, die nie fehlen dürfen: Domain, Pages-Schalter, Bestätigung für die Google Search Console
FEST = ["CNAME", ".nojekyll", "google49e2be530ce3822a.html"]

e = html.escape


# ---------------------------------------------------------------- Daten laden

def lies(pfad):
    daten = json.loads(pfad.read_text("utf-8"))
    daten["_datei"] = str(pfad.relative_to(ROOT))
    return daten


def lade():
    quellen = json.loads((DATA / "quellen.json").read_text("utf-8"))
    kantone = [lies(p) for p in sorted((DATA / "kantone").glob("*.json"))]
    gemeinden = [lies(p) for p in sorted((DATA / "gemeinden").glob("*/*.json"))]
    kantone.sort(key=lambda k: k.get("name", ""))
    gemeinden.sort(key=lambda g: g.get("ort", ""))
    return quellen, kantone, gemeinden


# ------------------------------------------------------------------- Prüfung

def pruefe(quellen, kantone, gemeinden):
    fehler = []

    def qs(keys, wo):
        if not keys:
            fehler.append(f"{wo}: keine Quelle angegeben")
            return
        for key in keys:
            if key not in quellen:
                fehler.append(f"{wo}: Quelle '{key}' fehlt in data/quellen.json")

    def datum(wert, wo):
        try:
            d = date.fromisoformat(str(wert))
        except ValueError:
            fehler.append(f"{wo}: 'geprueft' ist kein Datum im Format JJJJ-MM-TT")
            return
        if d > date.today():
            fehler.append(f"{wo}: 'geprueft' liegt in der Zukunft")

    def karte(k, wo, marke_pflicht):
        name = k.get("titel", "?")
        for feld in ("titel", "wert", "text"):
            if not str(k.get(feld, "")).strip():
                fehler.append(f"{wo}: Karte '{name}' ohne '{feld}'")
        if marke_pflicht or "marke" in k:
            if not k.get("marke"):
                fehler.append(f"{wo}: Karte '{name}' ohne 'marke'")
            if k.get("ton") not in TOENE:
                fehler.append(f"{wo}: Karte '{name}' hat keinen gültigen 'ton' {sorted(TOENE)}")
        if "mehr" in k and not (k["mehr"].get("titel") and k["mehr"].get("punkte")):
            fehler.append(f"{wo}: Karte '{name}': 'mehr' braucht 'titel' und 'punkte'")
        qs(k.get("quellen"), f"{wo}, Karte '{name}'")

    for key, q in quellen.items():
        for feld in ("kurz", "lang", "url"):
            if not str(q.get(feld, "")).strip():
                fehler.append(f"data/quellen.json: '{key}' ohne '{feld}'")
        if not str(q.get("url", "")).startswith("https://"):
            fehler.append(f"data/quellen.json: '{key}': URL muss mit https:// beginnen")

    ids = set()
    for k in kantone:
        wo = k["_datei"]
        fehlt = [f for f in ("id", "name", "kurz", "im", "des", "geprueft", "wald", "leine",
                             "verbot", "karten", "vergleich") if f not in k]
        if fehlt:
            fehler.append(f"{wo}: Felder fehlen: {', '.join(fehlt)}")
            continue
        kid = k["id"]
        if not SLUG.match(kid) or kid in RESERVIERT:
            fehler.append(f"{wo}: id '{kid}' ist ungültig oder reserviert")
        if Path(wo).stem != kid:
            fehler.append(f"{wo}: Dateiname und id stimmen nicht überein")
        ids.add(kid)
        datum(k["geprueft"], wo)
        w = k["wald"]
        qs(w.get("quellen"), f"{wo}, wald")
        if w.get("saison"):
            if not (MMTT.match(str(w.get("von", ""))) and MMTT.match(str(w.get("bis", "")))):
                fehler.append(f"{wo}, wald: 'von' und 'bis' im Format MM-TT angeben")
            elif w["von"] >= w["bis"]:
                fehler.append(f"{wo}, wald: 'von' muss vor 'bis' liegen")
            if not w.get("wo"):
                fehler.append(f"{wo}, wald: 'wo' fehlt")
        elif not w.get("text"):
            fehler.append(f"{wo}, wald: ohne Saison braucht es 'text'")
        for teil in ("leine", "verbot"):
            if not k[teil].get("punkte"):
                fehler.append(f"{wo}, {teil}: 'punkte' fehlt")
            qs(k[teil].get("quellen"), f"{wo}, {teil}")
        for c in k["karten"]:
            karte(c, wo, True)
        for key, titel in VERGLEICH:
            if not str(k["vergleich"].get(key, "")).strip():
                fehler.append(f"{wo}, vergleich: '{key}' ({titel}) fehlt")
        if "umzug" in k:
            if not k["umzug"].get("text"):
                fehler.append(f"{wo}, umzug: 'text' fehlt")
            qs(k["umzug"].get("quellen"), f"{wo}, umzug")

    gesehen = set()
    for g in gemeinden:
        wo = g["_datei"]
        fehlt = [f for f in ("id", "kanton", "name", "ort", "in_ort", "geprueft", "karten") if f not in g]
        if fehlt:
            fehler.append(f"{wo}: Felder fehlen: {', '.join(fehlt)}")
            continue
        if g["kanton"] not in ids:
            fehler.append(f"{wo}: Kanton '{g['kanton']}' hat keine Datei in data/kantone/")
        if Path(wo).parent.name != g["kanton"]:
            fehler.append(f"{wo}: Datei liegt nicht im Ordner ihres Kantons")
        if not SLUG.match(g["id"]) or Path(wo).stem != g["id"]:
            fehler.append(f"{wo}: id ungültig oder ungleich Dateiname")
        if (g["kanton"], g["id"]) in gesehen:
            fehler.append(f"{wo}: Gemeinde doppelt vorhanden")
        gesehen.add((g["kanton"], g["id"]))
        datum(g["geprueft"], wo)
        zonen = g.get("freilaufzonen", [])
        if zonen:
            qs(g.get("freilaufzonen_quellen"), f"{wo}, freilaufzonen")
            for z in zonen:
                if not (z.get("name") and z.get("text")):
                    fehler.append(f"{wo}: Freilaufzone braucht 'name' und 'text'")
        for c in g["karten"]:
            karte(c, wo, False)
        if len(zonen) + len(g["karten"]) < MIN_LOKAL:
            fehler.append(f"{wo}: weniger als {MIN_LOKAL} belegte lokale Angaben. "
                          "Für diese Gemeinde keine eigene Seite anlegen.")
    for name in FEST:
        if not (ROOT / name).is_file():
            fehler.append(f"{name}: feste Datei fehlt. Nicht löschen, siehe CLAUDE.md.")
    return fehler


# ------------------------------------------------------------------ Bausteine

def de_datum(iso):
    d = date.fromisoformat(iso)
    return f"{d.day:02d}.{d.month:02d}.{d.year}"


def tag_monat(mmtt):
    m, t = mmtt.split("-")
    return f"{int(t)}. {MONATE[int(m) - 1]}"


def tag_im_jahr(mmtt):
    m, t = (int(x) for x in mmtt.split("-"))
    return sum(TAGE[:m - 1]) + t - 1


def qlinks(keys, Q, benutzt):
    for key in keys:
        if key not in benutzt:
            benutzt.append(key)
    wort = "Quellen:" if len(keys) > 1 else "Quelle:"
    links = "".join(f'<a href="{e(Q[k]["url"])}" target="_blank" rel="noopener">{e(Q[k]["kurz"])}</a>'
                    for k in keys)
    return f'<div class="src"><span>{wort}</span>{links}</div>'


def karte(c, Q, benutzt):
    marke = f'<span class="chip {e(c["ton"])}">{e(c["marke"])}</span>' if c.get("marke") else ""
    mehr = ""
    if c.get("mehr"):
        punkte = "".join(f"<li>{e(p)}</li>" for p in c["mehr"]["punkte"])
        mehr = f'<details class="more"><summary>{e(c["mehr"]["titel"])}</summary><ul>{punkte}</ul></details>'
    return (f'<article class="card"><div class="card-top"><span class="card-k">{e(c["titel"])}</span>{marke}</div>'
            f'<p class="card-v">{e(c["wert"])}</p><p>{e(c["text"])}</p>{mehr}'
            f'{qlinks(c["quellen"], Q, benutzt)}</article>')


def wald(k, Q, benutzt, hinweis=None):
    w = k["wald"]
    spalten = " ".join(f"{t}fr" for t in TAGE)
    zellen = '<span class="m"></span>' * 12
    monate = "".join(f"<span>{m}</span>" for m in MON3)
    if w.get("saison"):
        von, bis = tag_monat(w["von"]), tag_monat(w["bis"])
        links = tag_im_jahr(w["von"]) / 365 * 100
        breite = (tag_im_jahr(w["bis"]) + 1 - tag_im_jahr(w["von"])) / 365 * 100
        band = f'<div class="band" style="left:{links:.2f}%;width:{breite:.2f}%"><span>Leine</span></div>'
        attrs = f' data-saison="1" data-von="{w["von"]}" data-bis="{w["bis"]}" data-wo="{e(w["wo"])}"'
        gross = f"Leinenpflicht im Wald vom {von} bis {bis}"
        text = (f"Gilt jedes Jahr {w['wo']}. Ausserhalb dieser Zeit muss dein Hund trotzdem "
                "unter Kontrolle bleiben, und Schilder vor Ort gehen vor.")
        unter = f"Markiert: Leinenpflicht im Wald, {von} bis {bis}"
        aria = f"Jahresbalken: Leinenpflicht im Wald vom {von} bis {bis}."
    else:
        band, attrs = "", ' data-saison="0"'
        gross, text = "Keine Saisonregel im Wald", w["text"]
        unter = f"Keine saisonale Leinenpflicht {k['im']}"
        aria = "Jahresbalken ohne saisonale Leinenpflicht."
    note = f'<p class="today-note">{e(hinweis)}</p>' if hinweis else ""
    return (f'<section class="today" data-wald{attrs}>'
            f'<div class="today-head"><span class="eyebrow">Leine im Wald · {e(k["name"])}</span>'
            '<span class="today-date" data-heute-datum></span></div>'
            '<div class="today-body"><div class="today-status">'
            f'<p class="big" data-heute-gross>{e(gross)}</p><p data-heute-text>{e(text)}</p>{note}'
            f'{qlinks(w["quellen"], Q, benutzt)}</div>'
            f'<div class="bar" role="img" aria-label="{e(aria)}">'
            f'<div class="track" style="grid-template-columns:{spalten}">{zellen}{band}</div>'
            f'<div class="months" style="grid-template-columns:{spalten}" aria-hidden="true">{monate}</div>'
            f'<p class="bar-cap">{e(unter)}</p></div></div></section>')


def regeln(k, Q, benutzt):
    def li(punkte):
        return "".join(f"<li>{e(p)}</li>" for p in punkte)
    lead = f'<p>{e(k["verbot"]["einleitung"])}</p>' if k["verbot"].get("einleitung") else ""
    return (f'<section class="sec"><div class="sec-head"><span class="eyebrow">{e(k["name"])}</span>'
            '<h2>Leine und Zutritt</h2></div><div class="split">'
            '<div class="list-card leash"><h3><span class="chip must">Leine</span>Immer an die Leine</h3>'
            f'<ul>{li(k["leine"]["punkte"])}</ul>{qlinks(k["leine"]["quellen"], Q, benutzt)}</div>'
            '<div class="list-card"><h3><span class="chip none">Verbot</span>Kein Zutritt für Hunde</h3>'
            f'{lead}<ul>{li(k["verbot"]["punkte"])}</ul>{qlinks(k["verbot"]["quellen"], Q, benutzt)}</div>'
            '</div></section>')


def pflichten(k, Q, benutzt):
    karten = "".join(karte(c, Q, benutzt) for c in k["karten"])
    umzug = ""
    if k.get("umzug"):
        umzug = (f'<div class="callout"><p><strong>Umzug in den {e(k["name"])}:</strong> '
                 f'{e(k["umzug"]["text"])}</p>{qlinks(k["umzug"]["quellen"], Q, benutzt)}</div>')
    return (f'<section class="sec"><div class="sec-head"><span class="eyebrow">{e(k["name"])}</span>'
            f'<h2>Pflichten für Hundehaltende</h2></div><div class="cards">{karten}</div>{umzug}</section>')


def lokal(g, Q, benutzt):
    intro = f'<p>{e(g["einleitung"])}</p>' if g.get("einleitung") else ""
    zonen = ""
    if g.get("freilaufzonen"):
        teile = []
        for z in g["freilaufzonen"]:
            marken = "".join(f'<span class="chip free">{e(m)}</span>' for m in z.get("marken", []))
            marken = f'<div class="tags">{marken}</div>' if marken else ""
            teile.append(f'<article class="zone"><div class="zone-name">{e(z["name"])}</div>{marken}'
                         f'<p>{e(z["text"])}</p></article>')
        zonen = (f'<h3 class="sub">Freilaufzonen</h3><div class="zones">{"".join(teile)}</div>'
                 f'{qlinks(g["freilaufzonen_quellen"], Q, benutzt)}')
    karten = "".join(karte(c, Q, benutzt) for c in g["karten"])
    return (f'<section class="sec"><div class="sec-head"><span class="eyebrow">{e(g["name"])}</span>'
            f'<h2>Das gilt zusätzlich {e(g["in_ort"])}</h2>{intro}</div>{zonen}'
            f'<div class="cards">{karten}</div></section>')


def tafel(href, name, unter, aktiv=False, such=""):
    cur = ' aria-current="page"' if aktiv else ""
    return (f'<a class="dest" href="{href}"{cur} data-such="{e(such.lower())}">'
            f'<span class="dest-name">{e(name)}</span><span class="dest-sub">{e(unter)}</span></a>')


def vergleich(kantone):
    kopf = "".join(f'<th scope="col">{e(t)}</th>' for _, t in VERGLEICH)
    zeilen = []
    for k in kantone:
        zellen = "".join(f'<td>{e(k["vergleich"][key])}</td>' for key, _ in VERGLEICH)
        zeilen.append(f'<tr><th scope="row"><a href="/{k["id"]}/">{e(k["name"])}</a></th>{zellen}</tr>')
    return ('<div class="table-wrap"><table class="wide"><thead><tr><th scope="col">Kanton</th>'
            f'{kopf}</tr></thead><tbody>{"".join(zeilen)}</tbody></table></div>')


def seite(pfad, titel, beschr, inhalt, krumen, stand, benutzt, Q, index=True):
    """pfad: Adresse ab Wurzel, z. B. '/zh/zuerich/'. krumen: Liste (Name, Pfad)."""
    crumbs, ld = "", ""
    if krumen:
        teile = []
        for i, (name, href) in enumerate(krumen):
            if i == len(krumen) - 1:
                teile.append(f'<span aria-current="page">{e(name)}</span>')
            else:
                teile.append(f'<a href="{href}">{e(name)}</a><span aria-hidden="true">›</span>')
        crumbs = f'<nav class="crumbs" aria-label="Pfad">{"".join(teile)}</nav>'
        liste = [{"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + href}
                 for i, (name, href) in enumerate(krumen)]
        ld = ('<script type="application/ld+json">'
              + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                            "itemListElement": liste}, ensure_ascii=False)
              + '</script>')
    stempel = f'<span class="stamp">Angaben geprüft am {de_datum(stand)}</span>' if stand else ""
    quellen = ""
    if benutzt:
        punkte = "".join(f'<li><a href="{e(Q[k]["url"])}" target="_blank" rel="noopener">{e(Q[k]["lang"])}</a></li>'
                         for k in benutzt)
        quellen = f'<p>Angaben auf dieser Seite geprüft am {de_datum(stand)}. Quellen:</p><ol>{punkte}</ol>'
    robots = "" if index else '<meta name="robots" content="noindex">\n'
    return f"""<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschr)}">
{robots}<link rel="canonical" href="{SITE}{pfad}">
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschr)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{pfad}">
<meta property="og:locale" content="de_CH">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
{ld}
</head>
<body>
<div class="wrap">
<header class="top"><a class="brand" href="/">Gassi-Kompass</a>{stempel}</header>
{inhalt.replace("<!--KRUMEN-->", crumbs)}
<footer class="foot">
<p><strong>Keine Rechtsberatung.</strong> Massgebend sind Gesetz, Verordnung und die Schilder vor Ort. Gassi-Kompass ist ein privates Projekt und kein Angebot eines Kantons oder einer Gemeinde.</p>
{quellen}
<nav aria-label="Fussnavigation"><a href="/">Start</a><a href="/#vergleich">Kantone im Vergleich</a><a href="/ueber/">Über diese Seite</a></nav>
</footer>
</div>
<script src="/assets/heute.js" defer></script>
</body>
</html>
"""


# --------------------------------------------------------------------- Seiten

def seite_start(Q, kantone, gemeinden):
    gruppen = []
    for k in kantone:
        tafeln = "".join(
            tafel(f'/{k["id"]}/{g["id"]}/', g["name"], f'Kanton {k["kurz"]}',
                  such=f'{g["name"]} {g["ort"]} {k["name"]} {k["kurz"]}')
            for g in gemeinden if g["kanton"] == k["id"])
        tafeln += tafel(f'/{k["id"]}/', "Übrige Gemeinden", k["name"], such=f'{k["name"]} {k["kurz"]}')
        gruppen.append(f'<div class="group" data-gruppe><h3><a href="/{k["id"]}/">{e(k["name"])}</a></h3>'
                       f'<div class="plates">{tafeln}</div></div>')
    namen = ", ".join(k["name"].replace("Kanton ", "") for k in kantone)
    stand = min(k["geprueft"] for k in kantone)
    inhalt = f"""<section class="hero">
<h1>Was gilt für deinen Hund hier?</h1>
<p class="lede">Hunderegeln der Schweiz nach Kanton und Gemeinde. Zu jeder Angabe findest du die amtliche Quelle. Bisher erfasst: {namen}.</p>
</section>
<section class="sec" id="orte">
<div class="sec-head"><span class="eyebrow">Ort wählen</span><h2>Kanton oder Gemeinde</h2></div>
<div class="filter" data-filter hidden><label for="ortsfilter">Gemeinde oder Kanton suchen</label><input id="ortsfilter" type="search" autocomplete="off" placeholder="z. B. Luzern"></div>
<p class="empty" id="kein-treffer" hidden>Kein Treffer. Wähle deinen Kanton: Dort stehen die Regeln, die in allen Gemeinden gelten.</p>
{"".join(gruppen)}
</section>
<section class="sec" id="vergleich">
<div class="sec-head"><span class="eyebrow">Umzug</span><h2>Kantone im Vergleich</h2><p>Was sich ändert, wenn du mit deinem Hund in einen anderen Kanton ziehst.</p></div>
{vergleich(kantone)}
</section>"""
    return seite("/", "Hunderegeln Schweiz nach Kanton und Gemeinde | Gassi-Kompass",
                 "Leinenpflicht, Haftpflicht, Kurse und Hundesteuer nach Kanton und Gemeinde. "
                 "Mit amtlicher Quelle zu jeder Angabe.",
                 inhalt, None, stand, [], Q)


def seite_kanton(k, Q, gemeinden):
    benutzt = []
    eigene = [g for g in gemeinden if g["kanton"] == k["id"]]
    tafeln = "".join(tafel(f'/{k["id"]}/{g["id"]}/', g["name"], f'Kanton {k["kurz"]}') for g in eigene)
    orte = (f'<div class="plates">{tafeln}</div>' if tafeln else "")
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>Hunderegeln {e(k["im"])}</h1>
<p class="lede">Diese Regeln gelten in allen Gemeinden {e(k["des"])}. Gemeinden können zusätzliche Orte mit Leinenpflicht oder Hundeverbot festlegen.</p>
</section>
{wald(k, Q, benutzt)}
{regeln(k, Q, benutzt)}
{pflichten(k, Q, benutzt)}
<section class="sec">
<div class="sec-head"><span class="eyebrow">Gemeinden</span><h2>Lokale Regeln {e(k["im"])}</h2><p>Fehlt deine Gemeinde, gelten die Regeln auf dieser Seite und die Schilder vor Ort. Weitere Gemeinden kommen laufend dazu.</p></div>
{orte}
<p><a class="text-link" href="/#vergleich">Mit anderen Kantonen vergleichen</a></p>
</section>"""
    return seite(f'/{k["id"]}/',
                 f'Hunderegeln {k["im"]}: Leinenpflicht, Haftpflicht, Hundesteuer | Gassi-Kompass',
                 f'Was für Hunde {k["im"]} gilt: Leinenpflicht, Zutrittsverbote, Haftpflicht, Kurse, '
                 'Hundesteuer und Rassenregeln. Mit amtlicher Quelle zu jeder Angabe.',
                 inhalt, [("Start", "/"), (k["name"], f'/{k["id"]}/')], k["geprueft"], benutzt, Q)


def seite_gemeinde(g, k, Q, gemeinden):
    benutzt = []
    andere = "".join(tafel(f'/{k["id"]}/{x["id"]}/', x["name"], f'Kanton {k["kurz"]}')
                     for x in gemeinden if x["kanton"] == k["id"] and x["id"] != g["id"])
    andere += tafel(f'/{k["id"]}/', "Übrige Gemeinden", k["name"])
    stand = min(g["geprueft"], k["geprueft"])
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>Hunderegeln {e(g["in_ort"])}</h1>
<p class="lede">Die lokalen Regeln {e(g["in_ort"])} und die Vorschriften {e(k["des"])}, die im ganzen Kanton gelten.</p>
</section>
{wald(k, Q, benutzt, g.get("hinweis_heute"))}
{lokal(g, Q, benutzt)}
{regeln(k, Q, benutzt)}
{pflichten(k, Q, benutzt)}
<section class="sec">
<div class="sec-head"><span class="eyebrow">{e(k["name"])}</span><h2>Weitere Orte {e(k["im"])}</h2></div>
<div class="plates">{andere}</div>
</section>"""
    pfad = f'/{k["id"]}/{g["id"]}/'
    return seite(pfad,
                 f'Hunderegeln {g["in_ort"]}: Leinenpflicht, Hundesteuer, Freilauf | Gassi-Kompass',
                 f'Was für Hunde {g["in_ort"]} gilt: lokale Regeln, Leinenpflicht, Hundesteuer und die '
                 f'Vorschriften {k["des"]}. Mit amtlicher Quelle zu jeder Angabe.',
                 inhalt, [("Start", "/"), (k["name"], f'/{k["id"]}/'), (g["name"], pfad)], stand, benutzt, Q)


def seite_ueber(Q):
    inhalt = """<section class="hero"><!--KRUMEN-->
<h1>Über Gassi-Kompass</h1>
<p class="lede">Gassi-Kompass sammelt die Regeln für Hunde in der Schweiz an einem Ort: pro Kanton und pro Gemeinde, mit der amtlichen Quelle zu jeder Angabe.</p>
</section>
<section class="prose">
<h2>Woher die Angaben stammen</h2>
<p>Alle Angaben kommen aus amtlichen Quellen: Gesetze und Verordnungen der Kantone, Merkblätter der Veterinärdienste, Websites und offene Daten der Gemeinden. Wo ein politischer Entscheid nur in den Medien dokumentiert ist, steht das bei der Quelle.</p>
<h2>Wie geprüft wird</h2>
<p>Die Angaben werden automatisiert mit KI-Unterstützung zusammengestellt und regelmässig mit den Quellen abgeglichen. Auf jeder Seite steht, wann sie zuletzt geprüft wurde. Eine Gemeinde bekommt erst dann eine eigene Seite, wenn mindestens drei lokale Angaben amtlich belegt sind.</p>
<h2>Was die Seite nicht ist</h2>
<p>Gassi-Kompass ist keine Rechtsberatung und kein Angebot eines Kantons oder einer Gemeinde. Massgebend sind Gesetz, Verordnung und die Schilder vor Ort. Regeln können sich ändern, und Fehler sind möglich. Im Zweifel gilt die verlinkte Quelle.</p>
<p>Gassi-Kompass ist ein privates Projekt aus der Schweiz.</p>
</section>"""
    return seite("/ueber/", "Über Gassi-Kompass: Quellen und Prüfung",
                 "Woher die Angaben auf Gassi-Kompass stammen, wie sie geprüft werden und was die Seite nicht ist.",
                 inhalt, [("Start", "/"), ("Über diese Seite", "/ueber/")], None, [], Q)


def seite_404(Q):
    inhalt = """<section class="hero">
<h1>Diese Seite gibt es nicht</h1>
<p class="lede">Vielleicht wurde die Adresse geändert. Auf der Startseite findest du alle Kantone und Gemeinden.</p>
<p><a class="text-link" href="/">Zur Startseite</a></p>
</section>"""
    return seite("/404.html", "Seite nicht gefunden | Gassi-Kompass",
                 "Diese Seite gibt es nicht.", inhalt, None, None, [], Q, index=False)


# ---------------------------------------------------------------------- Bauen

def schreibe(rel, text):
    ziel = ROOT / rel
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, "utf-8")


def baue(Q, kantone, gemeinden):
    for ordner in ROOT.iterdir():
        if ordner.is_dir() and (ordner / MARKE).exists():
            shutil.rmtree(ordner)
    nach_id = {k["id"]: k for k in kantone}
    urls = [("/", min(k["geprueft"] for k in kantone)), ("/ueber/", None)]
    schreibe("index.html", seite_start(Q, kantone, gemeinden))
    schreibe("404.html", seite_404(Q))
    schreibe("ueber/index.html", seite_ueber(Q))
    schreibe(f"ueber/{MARKE}", "")
    for k in kantone:
        schreibe(f'{k["id"]}/index.html', seite_kanton(k, Q, gemeinden))
        schreibe(f'{k["id"]}/{MARKE}', "")
        urls.append((f'/{k["id"]}/', k["geprueft"]))
    for g in gemeinden:
        k = nach_id[g["kanton"]]
        schreibe(f'{k["id"]}/{g["id"]}/index.html', seite_gemeinde(g, k, Q, gemeinden))
        urls.append((f'/{k["id"]}/{g["id"]}/', min(g["geprueft"], k["geprueft"])))
    eintraege = "".join(
        f"  <url><loc>{SITE}{pfad}</loc>" + (f"<lastmod>{stand}</lastmod>" if stand else "") + "</url>\n"
        for pfad, stand in urls)
    schreibe("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + eintraege + "</urlset>\n")
    schreibe("robots.txt", "User-agent: *\nAllow: /\nDisallow: /data/\nDisallow: /build.py\n"
             "Disallow: /tests/\nDisallow: /CLAUDE.md\nDisallow: /BACKLOG.md\nDisallow: /CHANGELOG.md\nDisallow: /README.md\n\n"
             f"Sitemap: {SITE}/sitemap.xml\n")
    return len(urls)


def main():
    quellen, kantone, gemeinden = lade()
    fehler = pruefe(quellen, kantone, gemeinden)
    if fehler:
        print(f"FEHLER ({len(fehler)}). Nichts wurde geschrieben:")
        for f in fehler:
            print("  -", f)
        return 1
    benutzt = set()

    def sammle(obj):
        if isinstance(obj, dict):
            for key, wert in obj.items():
                if key.endswith("quellen") and isinstance(wert, list):
                    benutzt.update(wert)
                else:
                    sammle(wert)
        elif isinstance(obj, list):
            for wert in obj:
                sammle(wert)

    sammle(kantone)
    sammle(gemeinden)
    unbenutzt = sorted(set(quellen) - benutzt)
    if unbenutzt:
        print("Hinweis: unbenutzte Quellen in data/quellen.json:", ", ".join(unbenutzt))
    if "--check" in sys.argv:
        print(f"Daten in Ordnung: {len(kantone)} Kantone, {len(gemeinden)} Gemeinden, {len(quellen)} Quellen.")
        return 0
    anzahl = baue(quellen, kantone, gemeinden)
    print(f"Gebaut: {anzahl} Seiten ({len(kantone)} Kantone, {len(gemeinden)} Gemeinden, {len(quellen)} Quellen).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
