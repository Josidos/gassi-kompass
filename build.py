#!/usr/bin/env python3
"""Baut gassi-kompass.ch aus den Dateien in data/ (nur Python-Standardbibliothek).

    python3 build.py          prüft die Daten und schreibt alle Seiten
    python3 build.py --check  prüft nur, schreibt nichts

Erzeugt werden: index.html, 404.html, sitemap.xml, robots.txt, ueber/, schweiz/,
assets/orte.json, thema/<name>/, <kanton>/ und <kanton>/<gemeinde>/. Diese Ausgaben nie von Hand ändern:
Daten in data/ oder dieses Skript anpassen und neu bauen.
"""
import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

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
RESERVIERT = {"assets", "data", "tests", "tools", "ueber", "schweiz", "thema", "fr-ch", "it-ch"}
VERGLEICH = [("wald", "Leine im Wald"), ("haft", "Haftpflicht"), ("kurs", "Kurs"),
             ("rassen", "Rassen"), ("steuer", "Hundesteuer"), ("anm", "Anmeldung")]
# Die sechs Karten jedes Kantons, in dieser Reihenfolge. Die Themenseiten greifen über die Position zu.
# Französische und italienische Titel für Dateien, die schon vor dem Umbau Mehrsprachigkeit geprüft werden.
KARTEN_TITEL = [
    ["Haftpflicht", "Kurs", "Anmeldung", "Hundesteuer", "Rassen", "Unterwegs"],
    ["Responsabilité civile", "Cours", "Annonce", "Impôt sur les chiens", "Races", "En promenade"],
    ["Responsabilità civile", "Corso", "Notifica", "Imposta sui cani", "Razze", "A passeggio"],
]
# Themenseiten unter /thema/<id>/: Vergleich aller erfassten Kantone, erzeugt aus den Kantonsdateien.
# key: Schlüssel in 'vergleich'. karte: Position der Karte in 'karten' (None: Feld 'wald').
# pflicht: Satzende nach «In N davon …», gezählt wird ton == must. Ohne 'pflicht' wird nicht gezählt,
# weil 'ton' bei Hundesteuer und Anmeldung keine Pflicht ausdrückt. Dann steht 'sonst'.
THEMEN = [
    {"id": "leinenpflicht-wald", "name": "Leinenpflicht im Wald", "key": "wald", "karte": None,
     "spalte": "Leine im Wald",
     "beschr": "Leinenpflicht im Wald in der Schweiz: in welchen Kantonen sie gilt, von wann bis wann "
               "und wie weit ab Waldrand. Mit amtlicher Quelle zu jeder Angabe."},
    {"id": "haftpflicht", "name": "Haftpflichtversicherung für Hunde", "key": "haft", "karte": 0,
     "spalte": "Haftpflicht",
     "pflicht": "ist eine Haftpflichtversicherung für Hunde vorgeschrieben.",
     "beschr": "Haftpflichtversicherung für Hunde in der Schweiz: in welchen Kantonen sie Pflicht ist "
               "und welche Deckung verlangt wird. Mit amtlicher Quelle zu jeder Angabe."},
    {"id": "hundekurs", "name": "Kurspflicht für Hundehaltende", "key": "kurs", "karte": 1,
     "spalte": "Kurs",
     "pflicht": "ist ein Kurs für Hundehaltende vorgeschrieben. Bei den übrigen steht beim Kanton, "
                "ob ein Kurs für einzelne Hunde verlangt wird.",
     "beschr": "Hundekurs in der Schweiz: in welchen Kantonen ein Kurs Pflicht ist, für wen und in "
               "welcher Frist. Mit amtlicher Quelle zu jeder Angabe."},
    {"id": "rassen", "name": "Rasselisten und Hundeverbote", "key": "rassen", "karte": 4,
     "spalte": "Rassen",
     "pflicht": "gilt für bestimmte Rassen eine Bewilligungspflicht oder ein Verbot.",
     "beschr": "Listenhunde in der Schweiz: welche Kantone Rassen verbieten oder eine Bewilligung "
               "verlangen und welche Rassen betroffen sind. Mit amtlicher Quelle zu jeder Angabe."},
    {"id": "hundesteuer", "name": "Hundesteuer", "key": "steuer", "karte": 3,
     "spalte": "Hundesteuer",
     "sonst": "Je nach Kanton legt der Kanton oder die Gemeinde den Betrag fest.",
     "beschr": "Hundesteuer in der Schweiz: was ein Hund pro Jahr kostet und wer den Betrag festlegt, "
               "Kanton für Kanton. Mit amtlicher Quelle zu jeder Angabe."},
    {"id": "anmeldung", "name": "Hund anmelden", "key": "anm", "karte": 2,
     "spalte": "Anmeldung",
     "sonst": "Wo und in welcher Frist du deinen Hund melden musst, ist je nach Kanton verschieden.",
     "beschr": "Hund anmelden in der Schweiz: bei welcher Stelle und in welcher Frist, Kanton für "
               "Kanton. Mit amtlicher Quelle zu jeder Angabe."},
]
MIN_LOKAL = 3  # so viele belegte lokale Angaben braucht eine Gemeinde für eine eigene Seite
# Feste Dateien, die nie fehlen dürfen: Domain, Pages-Schalter, Bestätigung für die Google Search Console
FEST = ["CNAME", ".nojekyll", "google49e2be530ce3822a.html"]
# Kontaktadresse des Projekts, von Joss freigegeben (siehe CLAUDE.md, «Freigaben»). Keine andere Adresse einsetzen.
KONTAKT = "kontakt@gassi-kompass.ch"
# Alle 26 Kantone. Für Kantone ohne Datei in data/kantone/ führt die Seite zu den Regeln des Bundes.
KANTONE_ALLE = [("ag", "Aargau"), ("ar", "Appenzell Ausserrhoden"), ("ai", "Appenzell Innerrhoden"),
                ("bl", "Basel-Landschaft"), ("bs", "Basel-Stadt"), ("be", "Bern"), ("fr", "Freiburg"),
                ("ge", "Genf"), ("gl", "Glarus"), ("gr", "Graubünden"), ("ju", "Jura"), ("lu", "Luzern"),
                ("ne", "Neuenburg"), ("nw", "Nidwalden"), ("ow", "Obwalden"), ("sh", "Schaffhausen"),
                ("sz", "Schwyz"), ("so", "Solothurn"), ("sg", "St. Gallen"), ("ti", "Tessin"),
                ("tg", "Thurgau"), ("ur", "Uri"), ("vd", "Waadt"), ("vs", "Wallis"), ("zg", "Zug"),
                ("zh", "Zürich")]
# Andere Schreibweisen grosser Orte für die Suche: so getippt (klein, ohne Akzente) -> amtlicher Gemeindename
ANDERE_NAMEN = {
    "genf": "Genève", "geneva": "Genève", "ginevra": "Genève", "neuenburg": "Neuchâtel",
    "freiburg": "Fribourg", "friburgo": "Fribourg", "sitten": "Sion", "siders": "Sierre",
    "delsberg": "Delémont", "pruntrut": "Porrentruy", "martinach": "Martigny", "losanna": "Lausanne",
    "bale": "Basel", "basilea": "Basel", "berne": "Bern", "berna": "Bern", "lucerne": "Luzern",
    "lucerna": "Luzern", "zurigo": "Zürich", "coire": "Chur", "coira": "Chur", "soleure": "Solothurn",
    "soletta": "Solothurn", "saint gall": "St. Gallen", "sankt gallen": "St. Gallen",
    "san gallo": "St. Gallen", "schaffhouse": "Schaffhausen", "sciaffusa": "Schaffhausen",
    "thoune": "Thun", "bienne": "Biel/Bienne", "winterthour": "Winterthur", "bellenz": "Bellinzona",
}

e = html.escape


# ---------------------------------------------------------------- Daten laden

def lies(pfad):
    daten = json.loads(pfad.read_text("utf-8"))
    daten["_datei"] = str(pfad.relative_to(ROOT))
    return daten


LADEFEHLER = []


def lade():
    quellen = json.loads((DATA / "quellen.json").read_text("utf-8"))
    # Parallel-Läufe legen ihre Quellen in eigene Dateien, damit sich zwei Läufe nie dieselbe Datei teilen.
    for pfad in sorted((DATA / "quellen").glob("*.json")):
        wo = str(pfad.relative_to(ROOT))
        try:
            mehr = json.loads(pfad.read_text("utf-8"))
        except ValueError as e:
            LADEFEHLER.append(f"{wo}: kein gültiges JSON ({e})")
            continue
        if not isinstance(mehr, dict):
            LADEFEHLER.append(f"{wo}: muss wie data/quellen.json ein Objekt mit Schlüsseln sein")
            continue
        for key, q in mehr.items():
            if key in quellen:
                LADEFEHLER.append(f"{wo}: Quelle '{key}' gibt es schon in einer anderen Quellendatei")
            elif not isinstance(q, dict):
                LADEFEHLER.append(f"{wo}: Quelle '{key}' muss ein Objekt mit kurz, lang und url sein")
            else:
                quellen[key] = q
    kantone = [lies(p) for p in sorted((DATA / "kantone").glob("*.json"))]
    gemeinden = [lies(p) for p in sorted((DATA / "gemeinden").glob("*/*.json"))]
    kantone.sort(key=lambda k: k.get("name", ""))
    gemeinden.sort(key=lambda g: g.get("ort", ""))
    bund = lies(DATA / "schweiz.json")
    orte = json.loads((DATA / "orte.json").read_text("utf-8"))
    return quellen, kantone, gemeinden, bund, orte


# ------------------------------------------------------------------- Prüfung

def pruefe(quellen, kantone, gemeinden, bund, orte):
    fehler = list(LADEFEHLER)
    alle = {kid for kid, _ in KANTONE_ALLE}
    verzeichnis = {x[0]: x for x in orte.get("gemeinden", [])}

    def qs(keys, wo):
        if not keys:
            fehler.append(f"{wo}: keine Quelle angegeben")
            return
        for key in keys:
            if key not in quellen:
                fehler.append(f"{wo}: Quelle '{key}' fehlt in data/quellen.json und data/quellen/")

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
                fehler.append(f"Quelle '{key}' ohne '{feld}'")
        if not str(q.get("url", "")).startswith("https://"):
            fehler.append(f"Quelle '{key}': URL muss mit https:// beginnen")

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
        if kid not in alle:
            fehler.append(f"{wo}: id '{kid}' ist kein Kantonskürzel")
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
        if [c.get("titel") for c in k["karten"]] not in KARTEN_TITEL:
            fehler.append(f"{wo}: 'karten' braucht genau diese sechs Karten in dieser Reihenfolge: "
                          + ", ".join(KARTEN_TITEL[0]))
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
        fehlt = [f for f in ("id", "kanton", "bfs", "name", "ort", "in_ort", "geprueft", "karten") if f not in g]
        if fehlt:
            fehler.append(f"{wo}: Felder fehlen: {', '.join(fehlt)}")
            continue
        eintrag = verzeichnis.get(g["bfs"])
        if not eintrag:
            fehler.append(f"{wo}: 'bfs' {g['bfs']} steht nicht in data/orte.json")
        elif eintrag[2] != g["kanton"]:
            fehler.append(f"{wo}: 'bfs' {g['bfs']} ({eintrag[1]}) liegt laut data/orte.json im Kanton {eintrag[2].upper()}")
        if sum(1 for x in gemeinden if x.get("bfs") == g["bfs"]) > 1:
            fehler.append(f"{wo}: 'bfs' {g['bfs']} kommt in mehreren Gemeinde-Dateien vor")
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
    wo = bund["_datei"]
    if "geprueft" not in bund or not bund.get("karten"):
        fehler.append(f"{wo}: 'geprueft' und 'karten' sind Pflicht")
    else:
        datum(bund["geprueft"], wo)
        for c in bund["karten"]:
            karte(c, wo, True)
    if len(verzeichnis) < 2000 or {x[2] for x in verzeichnis.values()} != alle:
        fehler.append("data/orte.json: Verzeichnis ist unvollständig (weniger als 2000 Gemeinden oder nicht 26 Kantone)")
    namen = {x[1] for x in verzeichnis.values()}
    for getippt, name in ANDERE_NAMEN.items():
        if name not in namen:
            fehler.append(f"build.py, ANDERE_NAMEN: '{name}' (für '{getippt}') steht nicht in data/orte.json")
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


def karte(c, Q, benutzt, link=None):
    """link: Adresse, auf die der Kartentitel führt (Themenseiten: zur Kantonsseite)."""
    kopf = f'<a href="{link}">{e(c["titel"])}</a>' if link else e(c["titel"])
    marke = f'<span class="chip {e(c["ton"])}">{e(c["marke"])}</span>' if c.get("marke") else ""
    mehr = ""
    if c.get("mehr"):
        punkte = "".join(f"<li>{e(p)}</li>" for p in c["mehr"]["punkte"])
        mehr = f'<details class="more"><summary>{e(c["mehr"]["titel"])}</summary><ul>{punkte}</ul></details>'
    return (f'<article class="card"><div class="card-top"><span class="card-k">{kopf}</span>{marke}</div>'
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


def tafel(href, name, unter, aktiv=False, klasse=""):
    cur = ' aria-current="page"' if aktiv else ""
    art = f"dest {klasse}".strip()
    return (f'<a class="{art}" href="{href}"{cur}>'
            f'<span class="dest-name">{e(name)}</span><span class="dest-sub">{e(unter)}</span></a>')


def suche():
    """Suchfeld für Gemeinde, Ort, Postleitzahl oder Kanton. Ohne Skript bleibt es unsichtbar.
    Alle Texte stehen hier, assets/suche.js kennt keine Sprache."""
    texte = {
        "lade": "Das Ortsverzeichnis wird geladen.",
        "leer": "Kein Ort gefunden. Prüfe die Schreibweise oder gib die Postleitzahl ein.",
        "fehler": "Die Ortssuche lässt sich gerade nicht laden. Wähle unten deinen Kanton.",
        "treffer": "{n} Treffer",
        "viele": "Die ersten {max} von {n} Treffern. Tippe weiter, um einzugrenzen.",
        "kt": "Kanton",
        "gemeinde": "Gemeinde",
        "lokal": "lokale Regeln",
        "kanton": "Regeln des Kantons",
        "bund": "Kanton folgt, Regeln des Bundes",
    }
    attrs = "".join(f' data-{k}="{e(v)}"' for k, v in texte.items())
    return (f'<div class="search" data-suche{attrs} hidden>'
            '<label for="ortssuche">Gemeinde, Ort oder Postleitzahl</label>'
            '<input id="ortssuche" type="search" autocomplete="off" enterkeyhint="search" '
            'placeholder="z. B. Wettingen oder 5430" aria-describedby="such-status">'
            '<p class="search-status" id="such-status" role="status"></p>'
            '<div class="plates" id="treffer"></div></div>'
            '<noscript><p>Die Ortssuche braucht JavaScript. Ohne JavaScript wählst du unten deinen Kanton.</p></noscript>')


def kantonsraster(kantone):
    """Alle 26 Kantone: erfasste führen zur Kantonsseite, die übrigen zu den Regeln des Bundes."""
    da = {k["id"] for k in kantone}
    teile = []
    for kid, name in KANTONE_ALLE:
        if kid in da:
            teile.append(tafel(f"/{kid}/", name, f"{kid.upper()} · erfasst", klasse="ok"))
        else:
            teile.append(tafel(f"/schweiz/#kt={kid}", name, f"{kid.upper()} · folgt", klasse="wait"))
    return f'<div class="plates small raster">{"".join(teile)}</div>'


def ortsindex(kantone, gemeinden, orte):
    """Kompakte Liste für die Suche im Browser (assets/orte.json).
    k: [Kürzel, Name, erfasst], g: [Gemeindename, Kanton-Nr., Adresse der Gemeinde-Seite oder 0],
    o: [Ortsname oder 0 (gleich wie Gemeinde), PLZ, Gemeinde-Nr.], a: andere Schreibweisen."""
    codes = [kid for kid, _ in KANTONE_ALLE]
    da = {k["id"] for k in kantone}
    seiten = {g["bfs"]: f'/{g["kanton"]}/{g["id"]}/' for g in gemeinden}
    reihen = sorted(orte["gemeinden"], key=lambda x: x[0])
    nr = {x[0]: i for i, x in enumerate(reihen)}
    g = [[name, codes.index(kt), seiten.get(bfs, 0)] for bfs, name, kt in reihen]
    k = [[kid, name, 1 if kid in da else 0] for kid, name in KANTONE_ALLE]

    # Das Verzeichnis führt einen Ort bei jeder Gemeinde, in die sein Gebiet hineinreicht, oft nur
    # mit einem schmalen Streifen. Heisst der Ort wie eine Gemeinde, zählt für die Suche nur sie.
    zusatz = re.compile(r"\s*\(?\b(" + "|".join(c.upper() for c in codes) + r")\)?$")

    def kern(name):
        return zusatz.sub("", name).strip().lower()

    gleichnamig = {}
    for bfs, name, kt in reihen:
        gleichnamig.setdefault(kern(name), []).append((bfs, kt))

    def hauptgemeinde(name, bfs):
        kandidaten = gleichnamig.get(kern(name))
        if not kandidaten or any(b == bfs for b, _ in kandidaten):
            return bfs
        im_kanton = [b for b, kt in kandidaten if kt == reihen[nr[bfs]][2]]
        if len(im_kanton) == 1:
            return im_kanton[0]
        m = zusatz.search(name)
        laut_zusatz = [b for b, kt in kandidaten if m and kt == m.group(1).lower()]
        if len(laut_zusatz) == 1:
            return laut_zusatz[0]
        return kandidaten[0][0] if len(kandidaten) == 1 else bfs

    paare = {}
    for name, plz, bfs in orte["orte"]:
        paare.setdefault((plz, name), set()).add(hauptgemeinde(name, bfs))
    o = []
    for (plz, name), menge in sorted(paare.items()):
        eigene = [b for b in menge if kern(reihen[nr[b]][1]) == kern(name)]
        for b in sorted(eigene or menge):
            o.append([0 if kern(reihen[nr[b]][1]) == kern(name) else name, int(plz), nr[b]])
    return json.dumps({"k": k, "g": g, "o": o, "a": ANDERE_NAMEN}, ensure_ascii=False, separators=(",", ":"))


def themenleiste(ohne=None):
    """Tafeln zu den Themenseiten. ohne: id der Seite, auf der die Leiste steht."""
    return ('<div class="plates small">'
            + "".join(tafel(f'/thema/{t["id"]}/', t["name"], "alle Kantone") for t in THEMEN if t["id"] != ohne)
            + '</div>')


def vergleich(kantone):
    thema = {t["key"]: t["id"] for t in THEMEN}
    kopf = "".join(f'<th scope="col"><a href="/thema/{thema[key]}/">{e(t)}</a></th>' for key, t in VERGLEICH)
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
<p>Stimmt etwas nicht oder fehlt etwas? Schreib an <a href="mailto:{KONTAKT}?subject={quote("Hinweis zu " + pfad)}">{KONTAKT}</a>.</p>
{quellen}
<nav aria-label="Fussnavigation"><a href="/">Ort suchen</a><a href="/schweiz/">Ganze Schweiz</a><a href="/#vergleich">Kantone im Vergleich</a><a href="/ueber/">Über diese Seite</a></nav>
</footer>
</div>
<script src="/assets/heute.js" defer></script>
<script src="/assets/suche.js" defer></script>
</body>
</html>
"""


# --------------------------------------------------------------------- Seiten

def seite_start(Q, kantone, gemeinden, bund):
    gruppen = []
    for k in kantone:
        tafeln = "".join(tafel(f'/{k["id"]}/{g["id"]}/', g["name"], f'Kanton {k["kurz"]}')
                         for g in gemeinden if g["kanton"] == k["id"])
        if tafeln:
            gruppen.append(f'<div class="group"><h3><a href="/{k["id"]}/">{e(k["name"])}</a></h3>'
                           f'<div class="plates">{tafeln}</div></div>')
    stand = min([k["geprueft"] for k in kantone] + [bund["geprueft"]])
    inhalt = f"""<section class="hero">
<h1>Was gilt für deinen Hund hier?</h1>
<p class="lede">Gib deine Gemeinde oder deine Postleitzahl ein. Du siehst, was dort gilt: die Regeln des Bundes, deines Kantons und, wo schon erfasst, deiner Gemeinde. Zu jeder Angabe findest du die amtliche Quelle.</p>
{suche()}
</section>
<section class="sec" id="orte">
<div class="sec-head"><span class="eyebrow">Kanton wählen</span><h2>Alle 26 Kantone</h2><p>{len(kantone)} von 26 Kantonen sind erfasst, weitere kommen laufend dazu. Bei den übrigen siehst du, <a href="/schweiz/">was in der ganzen Schweiz gilt</a>.</p></div>
{kantonsraster(kantone)}
</section>
<section class="sec" id="gemeinden">
<div class="sec-head"><span class="eyebrow">Lokale Regeln</span><h2>Gemeinden mit eigener Seite</h2><p>Für diese Gemeinden sind zusätzlich lokale Angaben erfasst, zum Beispiel Hundetaxe, Leinenzonen oder Freilaufzonen.</p></div>
{"".join(gruppen)}
</section>
<section class="sec" id="vergleich">
<div class="sec-head"><span class="eyebrow">Umzug</span><h2>Kantone im Vergleich</h2><p>Was sich ändert, wenn du mit deinem Hund in einen anderen Kanton ziehst.</p></div>
{vergleich(kantone)}
<h3 class="sub">Ein Thema, alle Kantone</h3>
{themenleiste()}
</section>"""
    return seite("/", "Hunderegeln Schweiz nach Kanton und Gemeinde | Gassi-Kompass",
                 "Gemeinde oder Postleitzahl eingeben und sehen, was für Hunde gilt: Leinenpflicht, "
                 "Haftpflicht, Kurse und Hundesteuer. Mit amtlicher Quelle zu jeder Angabe.",
                 inhalt, None, stand, [], Q)


def seite_schweiz(bund, Q, kantone):
    benutzt = []
    karten = "".join(karte(c, Q, benutzt) for c in bund["karten"])
    da = {k["id"] for k in kantone}
    offen = json.dumps({kid: name for kid, name in KANTONE_ALLE if kid not in da}, ensure_ascii=False)
    hinweis = (f'<p class="callout" data-ort-hinweis data-kantone="{e(offen)}" data-text="Der Kanton '
               '{kanton} ist noch nicht erfasst. Auf dieser Seite steht, was in der ganzen Schweiz gilt. '
               'Kanton und Gemeinde können zusätzliche Regeln haben." hidden></p>')
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>Das gilt in der ganzen Schweiz</h1>
<p class="lede">Diese Regeln des Bundes gelten in jedem Kanton und in jeder Gemeinde. Leinenpflicht, Haftpflichtversicherung, Rasselisten und Kurse sind je nach Kanton verschieden und stehen auf den Kantonsseiten.</p>
{hinweis}
</section>
<section class="sec">
<div class="sec-head"><span class="eyebrow">Bund</span><h2>Pflichten für alle Hundehaltenden</h2></div>
<div class="cards">{karten}</div>
</section>
<section class="sec" id="kantone">
<div class="sec-head"><span class="eyebrow">Kanton wählen</span><h2>Dazu kommt dein Kanton</h2><p>{len(kantone)} von 26 Kantonen sind erfasst, weitere kommen laufend dazu.</p></div>
{kantonsraster(kantone)}
<p><a class="text-link" href="/">Gemeinde oder Postleitzahl suchen</a></p>
</section>"""
    return seite("/schweiz/", "Hunderegeln Schweiz: Was in allen Kantonen gilt | Gassi-Kompass",
                 "Was der Bund für alle Hunde in der Schweiz vorschreibt: Mikrochip, AMICUS, Anmeldung, "
                 "Hundesteuer, Haltung und verbotene Hilfsmittel. Mit amtlicher Quelle zu jeder Angabe.",
                 inhalt, [("Start", "/"), ("Ganze Schweiz", "/schweiz/")], bund["geprueft"], benutzt, Q)


def seite_kanton(k, Q, gemeinden):
    benutzt = []
    eigene = [g for g in gemeinden if g["kanton"] == k["id"]]
    tafeln = "".join(tafel(f'/{k["id"]}/{g["id"]}/', g["name"], f'Kanton {k["kurz"]}') for g in eigene)
    orte = (f'<div class="plates">{tafeln}</div>' if tafeln else "")
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>Hunderegeln {e(k["im"])}</h1>
<p class="lede">Diese Regeln gelten in allen Gemeinden {e(k["des"])}. Gemeinden können zusätzliche Orte mit Leinenpflicht oder Hundeverbot festlegen.</p>
<p class="callout" data-ort-hinweis data-text="Für diesen Ort sind noch keine lokalen Angaben erfasst. Auf dieser Seite stehen die Regeln, die im ganzen {e(k["name"])} gelten. Die Gemeinde kann zusätzliche Regeln haben." hidden></p>
</section>
{wald(k, Q, benutzt)}
{regeln(k, Q, benutzt)}
{pflichten(k, Q, benutzt)}
<section class="sec">
<div class="sec-head"><span class="eyebrow">Gemeinden</span><h2>Lokale Regeln {e(k["im"])}</h2><p>Fehlt deine Gemeinde, gelten die Regeln auf dieser Seite und die Schilder vor Ort. Weitere Gemeinden kommen laufend dazu.</p></div>
{orte}
<p><a class="text-link" href="/schweiz/">Was zusätzlich in der ganzen Schweiz gilt</a></p>
<p><a class="text-link" href="/#vergleich">Mit anderen Kantonen vergleichen</a></p>
<p><a class="text-link" href="/">Anderen Ort suchen</a></p>
</section>
<section class="sec">
<div class="sec-head"><span class="eyebrow">Vergleich</span><h2>Ein Thema, alle Kantone</h2><p>So regeln es die anderen Kantone.</p></div>
{themenleiste()}
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
<p><a class="text-link" href="/schweiz/">Was zusätzlich in der ganzen Schweiz gilt</a></p>
<p><a class="text-link" href="/">Anderen Ort suchen</a></p>
</section>"""
    pfad = f'/{k["id"]}/{g["id"]}/'
    return seite(pfad,
                 f'Hunderegeln {g["in_ort"]}: Leinenpflicht, Hundesteuer, Freilauf | Gassi-Kompass',
                 f'Was für Hunde {g["in_ort"]} gilt: lokale Regeln, Leinenpflicht, Hundesteuer und die '
                 f'Vorschriften {k["des"]}. Mit amtlicher Quelle zu jeder Angabe.',
                 inhalt, [("Start", "/"), (k["name"], f'/{k["id"]}/'), (g["name"], pfad)], stand, benutzt, Q)


def seite_thema(t, Q, kantone):
    """Vergleich aller erfassten Kantone zu einem Thema. Alle Angaben stammen aus den Kantonsdateien."""
    benutzt = []
    n = len(kantone)

    def wieviele(m):
        return {0: "keinem", 1: "einem"}.get(m, str(m))

    zeilen, karten = [], []
    if t["karte"] is None:
        saison = [k for k in kantone if k["wald"].get("saison")]
        zeiten = {(k["wald"]["von"], k["wald"]["bis"]) for k in saison}
        zeit = ""
        if len(saison) > 1 and len(zeiten) == 1:
            von, bis = next(iter(zeiten))
            zeit = f", überall vom {tag_monat(von)} bis {tag_monat(bis)}"
        zahl = f"In {wieviele(len(saison))} davon gilt im Wald eine Leinenpflicht zu festen Daten{zeit}."
        if len(saison) < n:
            zahl += " Bei den übrigen ist keine feste Leinenzeit erfasst. Was dort gilt, steht beim Kanton."
    elif t.get("pflicht"):
        zahl = f'In {wieviele(sum(1 for k in kantone if k["karten"][t["karte"]]["ton"] == "must"))} davon {t["pflicht"]}'
    else:
        zahl = t["sonst"]
    for k in kantone:
        if t["karte"] is None:
            w = k["wald"]
            if w.get("saison"):
                c = {"marke": "Leine", "ton": "must",
                     "wert": f'{tag_monat(w["von"])} bis {tag_monat(w["bis"])}',
                     "text": f'Leinenpflicht jedes Jahr {w["wo"]}.'}
            else:
                c = {"marke": "keine Saison", "ton": "none", "wert": "Keine Saisonregel im Wald", "text": w["text"]}
            c["quellen"] = w["quellen"]
        else:
            c = dict(k["karten"][t["karte"]])
        c["titel"] = k["name"]
        zeilen.append(f'<tr><th scope="row"><a href="/{k["id"]}/">{e(k["name"])}</a></th>'
                      f'<td><span class="chip {e(c["ton"])}">{e(c["marke"])}</span></td>'
                      f'<td>{e(k["vergleich"][t["key"]])}</td></tr>')
        karten.append(karte(c, Q, benutzt, link=f'/{k["id"]}/'))
    rest = (f" Die übrigen {26 - n} folgen." if n < 25 else " Der letzte folgt." if n == 25 else "")
    pfad = f'/thema/{t["id"]}/'
    inhalt = f"""<section class="hero thema"><!--KRUMEN-->
<h1>{e(t["name"])}: alle Kantone im Vergleich</h1>
<p class="lede">{n} von 26 Kantonen sind erfasst.{rest} {e(zahl)} Was der Bund für alle Hunde vorschreibt, steht unter <a href="/schweiz/">Ganze Schweiz</a>.</p>
</section>
<section class="sec">
<div class="sec-head"><span class="eyebrow">Überblick</span><h2>{e(t["spalte"])} nach Kanton</h2></div>
<div class="table-wrap"><table><thead><tr><th scope="col">Kanton</th><th scope="col">Kurz</th><th scope="col">{e(t["spalte"])}</th></tr></thead><tbody>{"".join(zeilen)}</tbody></table></div>
</section>
<section class="sec">
<div class="sec-head"><span class="eyebrow">Im Einzelnen</span><h2>Was jeder Kanton vorschreibt</h2><p>Der Name des Kantons führt zu allen Regeln dort. Gemeinden können zusätzliche Regeln haben.</p></div>
<div class="cards">{"".join(karten)}</div>
</section>
<section class="sec">
<div class="sec-head"><span class="eyebrow">Vergleich</span><h2>Weitere Themen</h2></div>
{themenleiste(t["id"])}
<p><a class="text-link" href="/">Gemeinde oder Postleitzahl suchen</a></p>
</section>"""
    return seite(pfad, f'{t["name"]}: alle Kantone im Vergleich | Gassi-Kompass', t["beschr"], inhalt,
                 [("Start", "/"), (t["name"], pfad)], min(k["geprueft"] for k in kantone), benutzt, Q)


def seite_ueber(Q):
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>Über Gassi-Kompass</h1>
<p class="lede">Gassi-Kompass sammelt die Regeln für Hunde in der Schweiz an einem Ort: pro Kanton und pro Gemeinde, mit der amtlichen Quelle zu jeder Angabe.</p>
</section>
<section class="prose">
<h2>Woher die Angaben stammen</h2>
<p>Alle Angaben kommen aus amtlichen Quellen: Informationen des Bundes, Gesetze und Verordnungen der Kantone, Merkblätter der Veterinärdienste, Websites und offene Daten der Gemeinden. Wo ein politischer Entscheid nur in den Medien dokumentiert ist, steht das bei der Quelle.</p>
<h2>Wie die Ortssuche funktioniert</h2>
<p>Die Suche kennt alle Gemeinden, Ortschaften und Postleitzahlen der Schweiz und ordnet sie dem Kanton zu. Sie zeigt dir die genaueste Seite, die es für deinen Ort schon gibt: die Gemeinde, sonst den Kanton, sonst die Regeln des Bundes. Grundlage ist das <a href="{e(Q["ch_swisstopo_orte"]["url"])}" target="_blank" rel="noopener">Amtliche Ortschaftenverzeichnis</a>. Quelle: Bundesamt für Landestopografie swisstopo.</p>
<h2>Wie geprüft wird</h2>
<p>Die Angaben werden automatisiert mit KI-Unterstützung zusammengestellt und regelmässig mit den Quellen abgeglichen. Auf jeder Seite steht, wann sie zuletzt geprüft wurde. Eine Gemeinde bekommt erst dann eine eigene Seite, wenn mindestens drei lokale Angaben amtlich belegt sind.</p>
<h2>Fehler melden</h2>
<p>Stimmt eine Angabe nicht mehr oder fehlt etwas? Schreib an <a href="mailto:{KONTAKT}">{KONTAKT}</a>. Nenn bitte den Ort und, wenn du sie hast, die amtliche Quelle.</p>
<h2>Was die Seite nicht ist</h2>
<p>Gassi-Kompass ist keine Rechtsberatung und kein Angebot eines Kantons oder einer Gemeinde. Massgebend sind Gesetz, Verordnung und die Schilder vor Ort. Regeln können sich ändern, und Fehler sind möglich. Im Zweifel gilt die verlinkte Quelle.</p>
<p>Gassi-Kompass ist ein privates Projekt aus der Schweiz.</p>
</section>"""
    return seite("/ueber/", "Über Gassi-Kompass: Quellen und Prüfung",
                 "Woher die Angaben auf Gassi-Kompass stammen, wie sie geprüft werden und was die Seite nicht ist.",
                 inhalt, [("Start", "/"), ("Über diese Seite", "/ueber/")], None, [], Q)


def seite_404(Q):
    inhalt = f"""<section class="hero">
<h1>Diese Seite gibt es nicht</h1>
<p class="lede">Vielleicht wurde die Adresse geändert. Such deinen Ort gleich hier oder geh zur Startseite.</p>
{suche()}
<p><a class="text-link" href="/">Zur Startseite</a></p>
</section>"""
    return seite("/404.html", "Seite nicht gefunden | Gassi-Kompass",
                 "Diese Seite gibt es nicht.", inhalt, None, None, [], Q, index=False)


# ---------------------------------------------------------------------- Bauen

def schreibe(rel, text):
    ziel = ROOT / rel
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, "utf-8")


def baue(Q, kantone, gemeinden, bund, orte):
    for ordner in ROOT.iterdir():
        if ordner.is_dir() and (ordner / MARKE).exists():
            shutil.rmtree(ordner)
    nach_id = {k["id"]: k for k in kantone}
    urls = [("/", min([k["geprueft"] for k in kantone] + [bund["geprueft"]])), ("/ueber/", None),
            ("/schweiz/", bund["geprueft"])]
    schreibe("index.html", seite_start(Q, kantone, gemeinden, bund))
    schreibe("404.html", seite_404(Q))
    schreibe("ueber/index.html", seite_ueber(Q))
    schreibe(f"ueber/{MARKE}", "")
    schreibe("schweiz/index.html", seite_schweiz(bund, Q, kantone))
    schreibe(f"schweiz/{MARKE}", "")
    schreibe("assets/orte.json", ortsindex(kantone, gemeinden, orte))
    schreibe(f"thema/{MARKE}", "")
    for t in THEMEN:
        schreibe(f'thema/{t["id"]}/index.html', seite_thema(t, Q, kantone))
        urls.append((f'/thema/{t["id"]}/', min(k["geprueft"] for k in kantone)))
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
             "Disallow: /tests/\nDisallow: /tools/\nDisallow: /CLAUDE.md\nDisallow: /BACKLOG.md\nDisallow: /CHANGELOG.md\nDisallow: /README.md\n\n"
             f"Sitemap: {SITE}/sitemap.xml\n")
    return len(urls)


def main():
    quellen, kantone, gemeinden, bund, orte = lade()
    fehler = pruefe(quellen, kantone, gemeinden, bund, orte)
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
    sammle(bund)
    benutzt.add("ch_swisstopo_orte")  # steht auf der Seite «Über diese Seite»
    unbenutzt = sorted(set(quellen) - benutzt)
    if unbenutzt:
        print("Hinweis: unbenutzte Quellen:", ", ".join(unbenutzt))
    if "--check" in sys.argv:
        print(f"Daten in Ordnung: {len(kantone)} Kantone, {len(gemeinden)} Gemeinden, {len(quellen)} Quellen.")
        return 0
    anzahl = baue(quellen, kantone, gemeinden, bund, orte)
    print(f"Gebaut: {anzahl} Seiten ({len(kantone)} Kantone, {len(gemeinden)} Gemeinden, {len(quellen)} Quellen). "
          f"Ortssuche: {len(orte['gemeinden'])} Gemeinden, {len(orte['orte'])} Orte mit Postleitzahl.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
