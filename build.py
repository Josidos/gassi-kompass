#!/usr/bin/env python3
"""Baut gassi-kompass.ch aus den Dateien in data/ (nur Python-Standardbibliothek).

    python3 build.py                      prüft die Daten und schreibt alle Seiten
    python3 build.py --check              prüft nur, schreibt nichts
    python3 build.py --fehlend            listet fehlende und veraltete Übersetzungen auf
    python3 build.py --pruefsumme DATEI   Prüfsumme einer Originalfassung für das Feld 'original'

Erzeugt werden: index.html, 404.html, sitemap.xml, robots.txt, ueber/, schweiz/,
assets/orte.json, thema/<name>/, <kanton>/ und <kanton>/<gemeinde>/, dazu die französischen Seiten
unter fr-ch/ und die italienischen unter it-ch/, jeweils mit eigener Startseite, schweiz/, thema/
und ueber/. Diese Ausgaben nie von Hand ändern:
Daten in data/ oder dieses Skript anpassen und neu bauen.

Sprachen: Deutsch liegt an der Wurzel (Daten in data/kantone/ und data/gemeinden/), Französisch
unter /fr-ch/ (data/fr-ch/), Italienisch unter /it-ch/ (data/it-ch/). Alle festen Texte stehen
in der Tabelle TEXTE je Sprache.

Originalfassung und Übersetzung: Eine Datei ohne das Feld 'uebersetzt_aus' ist eine Originalfassung,
ihre Texte stammen aus den amtlichen Quellen in ihrer Sprache. Eine Datei mit 'uebersetzt_aus' ist
die Übersetzung der Originalfassung in dieser Sprache. Sie hat denselben Aufbau, dieselben Quellen
und dieselben Zahlen, das prüft pruefe_uebersetzung(). Der Generator ändert nie selbst einen Text.
"""
import unicodedata
import hashlib
import html
import html.parser
import json
import re
import shutil
import sys
from datetime import date, datetime
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
RESERVIERT = {"assets", "data", "tests", "tools", "ueber", "schweiz", "thema", "quellen", "fr-ch", "it-ch"}
VERGLEICH = [("wald", "Leine im Wald"), ("haft", "Haftpflicht"), ("kurs", "Kurs"),
             ("rassen", "Rassen"), ("steuer", "Hundesteuer"), ("anm", "Anmeldung")]
# Sprachen der Seite. Deutsch an der Wurzel, die anderen unter ihrem Präfix. Nicht /fr/: das ist Freiburg.
SPRACHEN = ["de", "fr", "it"]
PRAEFIX = {"de": "", "fr": "/fr-ch", "it": "/it-ch"}
HTMLLANG = {"de": "de-CH", "fr": "fr-CH", "it": "it-CH"}
# Die sechs Karten jedes Kantons, in dieser Reihenfolge. Die Themenseiten greifen über die Position zu.
KARTEN_TITEL = {
    "de": ["Haftpflicht", "Kurs", "Anmeldung", "Hundesteuer", "Rassen", "Unterwegs"],
    "fr": ["Responsabilité civile", "Cours", "Annonce", "Impôt sur les chiens", "Races", "En promenade"],
    "it": ["Responsabilità civile", "Corso", "Notifica", "Imposta sui cani", "Razze", "A passeggio"],
}
# Themenseiten unter /thema/<id>/ und in den anderen Sprachen unter /fr-ch/thema/<id>/ und /it-ch/thema/<id>/:
# Vergleich aller Kantone, die es in der Sprache der Seite gibt, erzeugt aus den Kantonsdateien.
# key: Schlüssel in 'vergleich'. karte: Position der Karte in 'karten' (None: Feld 'wald').
# zaehlt: Die Seite nennt, in wie vielen Kantonen ton == must gilt. Bei Hundesteuer und Anmeldung
# drückt 'ton' keine Pflicht aus, dort steht stattdessen der Satz 'sonst'.
# Name, Sätze und Beschreibung jedes Themas stehen je Sprache in TEXTE unter "themen".
# Ein Thema mit 'feld' statt 'key' und 'karte' hat keine Tabelle und zählt nicht: Zuoberst steht die Karte
# des Bundes mit derselben 'id' aus schweiz.json, darunter jeder Kanton, der das Feld hat.
THEMEN = [
    {"id": "leinenpflicht-wald", "key": "wald", "karte": None},
    {"id": "haftpflicht", "key": "haft", "karte": 0, "zaehlt": True},
    {"id": "hundekurs", "key": "kurs", "karte": 1, "zaehlt": True},
    {"id": "rassen", "key": "rassen", "karte": 4, "zaehlt": True},
    {"id": "hundesteuer", "key": "steuer", "karte": 3},
    {"id": "anmeldung", "key": "anm", "karte": 2},
    # feld: Die Seite vergleicht nicht, sie führt je Kanton das wahlweise Feld dieses Namens auf (seite_thema_feld).
    {"id": "vermisst", "feld": "vermisst"},
    {"id": "gewerbe", "feld": "gewerbe"},
]
# Wahlweise Felder der Kantone mit eigener Themenseite und eigenem Abschnitt auf der Kantonsseite.
FELDER = [t["feld"] for t in THEMEN if t.get("feld")]
# Feste Anker der sechs Karten auf der Kantonsseite, nach Position (nicht nach Titel), in jeder Sprache gleich.
# Der Kasten zur Leine im Wald heisst dort "wald". Nur auf der Kantonsseite, sonst stünden sie mehrfach.
KARTEN_ANKER = ["haftpflicht", "kurs", "anmeldung", "hundesteuer", "rassen", "unterwegs"]
# Abschnitt «Neu einen Hund» (#neuer-hund): die Schritte in dieser Reihenfolge, je (Position der Karte, Schlüssel
# in 'vergleich'). None: der Kasten zur Leine im Wald.
# Schlüssel in 'vergleich' je Kartenposition. «Unterwegs» hat keinen, dort steht der 'wert' der Karte.
VERGLEICH_POS = ["haft", "kurs", "anm", "steuer", "rassen", None]
AUFKLAPPEN = '<script src="/assets/aufklappen.js" defer></script>\n'  # Themenseiten: Zeile aus der Adresse aufklappen
FUSS_OFFEN = 6  # Hat eine Seite mehr Quellen, steht die Liste im Fuss zum Aufklappen (am Bildschirm öffnet sie das Skript)
WALD_KURZ = 300  # Gemeindeseite: längere Texte zur Leine im Wald (ohne feste Leinenzeit) stehen zum Aufklappen
NEU_SCHRITTE = [(4, "rassen"), (2, "anm"), (0, "haft"), (1, "kurs"), (3, "steuer"), (None, "wald")]
MIN_LOKAL = 3  # so viele belegte lokale Angaben braucht eine Gemeinde für eine eigene Seite
# Feste Dateien, die nie fehlen dürfen: Domain, Pages-Schalter, Bestätigung für die Google Search Console,
# Schlüssel für IndexNow (tools/indexnow.py) und die Vorschaubilder für geteilte Links (tools/teilbild.js)
FEST = ["CNAME", ".nojekyll", "google49e2be530ce3822a.html", "153c0b46fbcd82162492ea0b2d9f2b72.txt",
        "assets/teilen-de.png", "assets/teilen-fr.png", "assets/teilen-it.png"]
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
# Namen der Kantone auf Französisch und Italienisch, für Kantonsraster und Ortssuche dieser Sprachen.
KANTONSNAMEN = {
    "de": dict(KANTONE_ALLE),
    "fr": {"ag": "Argovie", "ar": "Appenzell Rhodes-Extérieures", "ai": "Appenzell Rhodes-Intérieures",
           "bl": "Bâle-Campagne", "bs": "Bâle-Ville", "be": "Berne", "fr": "Fribourg", "ge": "Genève",
           "gl": "Glaris", "gr": "Grisons", "ju": "Jura", "lu": "Lucerne", "ne": "Neuchâtel",
           "nw": "Nidwald", "ow": "Obwald", "sh": "Schaffhouse", "sz": "Schwytz", "so": "Soleure",
           "sg": "Saint-Gall", "ti": "Tessin", "tg": "Thurgovie", "ur": "Uri", "vd": "Vaud",
           "vs": "Valais", "zg": "Zoug", "zh": "Zurich"},
    "it": {"ag": "Argovia", "ar": "Appenzello Esterno", "ai": "Appenzello Interno",
           "bl": "Basilea Campagna", "bs": "Basilea Città", "be": "Berna", "fr": "Friburgo",
           "ge": "Ginevra", "gl": "Glarona", "gr": "Grigioni", "ju": "Giura", "lu": "Lucerna",
           "ne": "Neuchâtel", "nw": "Nidvaldo", "ow": "Obvaldo", "sh": "Sciaffusa", "sz": "Svitto",
           "so": "Soletta", "sg": "San Gallo", "ti": "Ticino", "tg": "Turgovia", "ur": "Uri",
           "vd": "Vaud", "vs": "Vallese", "zg": "Zugo", "zh": "Zurigo"},
}
# Die drei Formen des Kantonsnamens, die die Seiten brauchen. In Originalfassungen stehen sie in der
# Datei (name, im, des). Bei Übersetzungen setzt der Generator sie aus dieser Tabelle ein.
_FR_VOR = {"ag": "d'", "ar": "d'", "ai": "d'", "gr": "des ", "ju": "du ", "ow": "d'", "ti": "du ",
           "ur": "d'", "vs": "du "}
_IT_VOR = {"gr": "dei ", "ju": "del ", "vs": "del ", "ti": ""}


def kantonsformen(lang, kid):
    n = KANTONSNAMEN[lang][kid]
    if lang == "de":
        return {"name": f"Kanton {n}", "im": f"im Kanton {n}", "des": f"des Kantons {n}"}
    if lang == "fr":
        v = _FR_VOR.get(kid, "de ")
        return {"name": f"Canton {v}{n}", "im": f"dans le canton {v}{n}", "des": f"du canton {v}{n}"}
    v = _IT_VOR.get(kid, "di ")
    return {"name": f"Cantone {v}{n}", "im": f"nel Cantone {v}{n}", "des": f"del Cantone {v}{n}"}


# Reihenfolge der Liste --fehlend: ungefähr nach Einwohnerzahl, damit grosse Kantone zuerst übersetzt werden.
KANTONE_GROESSE = ["zh", "be", "vd", "ag", "sg", "ge", "lu", "ti", "vs", "fr", "bl", "so", "tg", "gr",
                   "bs", "ne", "sz", "zg", "sh", "ju", "ar", "nw", "gl", "ow", "ur", "ai"]
# Übersetzungen: Diese Felder sind in jeder Sprache gleich, alle anderen Texte werden übersetzt.
GLEICH = {"id", "kanton", "kurz", "bfs", "ton", "saison", "ganzjaehrig", "von", "bis", "datum"}
TAUSENDER = re.compile(r"(?<=\d)['’\u00a0\u202f ](?=\d{3}(?!\d))")
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


# ------------------------------------------------------------ Texte je Sprache

# Alle festen Texte der Seiten. Platzhalter in geschweiften Klammern setzt build.py ein.
# Die Texte unter "suche" und "heute" gehen als data-Attribute ins HTML: assets/suche.js und
# assets/heute.js kennen keine Sprache. Dort ersetzt das Skript {n}, {max}, {name} und {j}.
TEXTE = {
    "de": {
        "name": "Deutsch",
        "sprache": {"de": "deutsch", "fr": "französisch", "it": "italienisch"},
        "ueb": {"fr": "Übersetzung aus dem Französischen. Die amtlichen Quellen sind auf Französisch.",
                "it": "Übersetzung aus dem Italienischen. Die amtlichen Quellen sind auf Italienisch."},
        "ueb_link": {"fr": "Zur Originalfassung auf Französisch", "it": "Zur Originalfassung auf Italienisch"},
        "durchsicht": "Eine Zusammenfassung dieser Regeln wurde am {datum} {wer} durchgesehen. Spätere Ergänzungen sind nicht Teil dieser Durchsicht. Die Seite ist ein privates Angebot.",
        "ueb_alt": "Die Originalfassung wurde seither geändert und ist aktueller als diese Übersetzung.",
        "monate": MONATE, "mon3": MON3,
        "wochentage": ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
        "start": "Start", "pfad": "Pfad", "sprachwahl": "Sprache",
        "teilbild": "Gassi-Kompass: Hunderegeln der Schweiz nach Kanton und Gemeinde",
        "stempel": "Angaben geprüft am {d}",
        "quelle": "Quelle:", "quellen": "Quellen:",
        "sprung": {"label": "Auf dieser Seite", "wald": "Wald", "leine": "Leine und Zutritt", "pflichten": "Pflichten",
                   "neuer-hund": "Neu einen Hund", "vermisst": "Vermisst", "gewerbe": "Beruf", "gemeinden": "Gemeinden", "themen": "Themen",
                   "kantone": "Kantone", "quellen": "Quellen"},
        "fuss_recht": "<strong>Keine Rechtsberatung.</strong> Massgebend sind Gesetz, Verordnung und die Schilder vor Ort. Gassi-Kompass ist ein privates Projekt und kein Angebot eines Kantons oder einer Gemeinde.",
        "fuss_fehler": "Stimmt etwas nicht oder fehlt etwas? Schreib an {mail}.",
        "betreff": "Hinweis zu ",
        "fuss_quellen": "Angaben auf dieser Seite geprüft am {d}. Quellen:",
        "fuss_alle": "Alle {n} Quellen anzeigen",
        "fussnav": "Fussnavigation",
        "nav_suche": "Ort oder Stichwort suchen", "nav_schweiz": "Ganze Schweiz", "nav_vergleich": "Kantone im Vergleich",
        "nav_ueber": "Über diese Seite",
        "nav_quellen": "Alle Quellen",
        "qv": {
            "titel": "Amtliche Quellen zu Hunderegeln in der Schweiz: Hundegesetze der Kantone",
            "beschr": "Alle amtlichen Quellen von Gassi-Kompass: Hundegesetze und Verordnungen der Kantone, Reglemente der Gemeinden und Seiten des Bundes, je mit Link und den Seiten, die sie zitieren.",
            "pfad": "Quellen", "h1": "Amtliche Quellen",
            "lede": "Hier stehen alle Quellen, auf die sich die Seiten von Gassi-Kompass stützen, mit Link zur Quelle und zu den Seiten, die sie zitieren. Massgebend ist immer die Quelle selbst.",
            "label": "Quelle suchen", "beispiel": "z. B. Hundegesetz, Winterthur",
            "wahl": "Geltungsbereich", "alle": "Alle", "sort": "Sortieren", "nach_kanton": "Nach Kanton", "nach_name": "Nach Name",
            "bund": "Bund", "kanton": "Kanton", "zitiert": "Zitiert auf", "abgeglichen": "Zuletzt abgeglichen am {d}",
            "s_alle": "{n} Quellen", "s_teil": "{n} von {m} Quellen", "s_eins": "1 von {m} Quellen",
            "g_eins": "1 Quelle", "g_viele": "{n} Quellen",
            "s_keine": "Keine Quelle gefunden. Prüfe die Schreibweise oder wähle «Alle».",
        },
        "kanton_kurz": "Kanton {kurz}",
        "n_gemeinden": ["1 Gemeinde", "{n} Gemeinden"],
        "fakten": ["Kantone", "Gemeinden mit lokalen Regeln", "verlinkte Quellen"],
        "wald_kopf": "Leine im Wald",
        "wald_band": "Leine",
        "wald_gross": "Leinenpflicht im Wald vom {von} bis {bis}",
        "wald_text": "Gilt jedes Jahr {wo}. Ausserhalb dieser Zeit muss dein Hund trotzdem unter Kontrolle bleiben, und Schilder vor Ort gehen vor.",
        "wald_unter": "Markiert: Leinenpflicht im Wald, {von} bis {bis}",
        "wald_aria": "Jahresbalken: Leinenpflicht im Wald vom {von} bis {bis}.",
        "wald_ohne_gross": "Keine feste Leinenzeit im Wald",
        "wald_immer_gross": "Leinenpflicht im Wald das ganze Jahr",
        "wald_immer_unter": "Markiert: Leinenpflicht im Wald, das ganze Jahr",
        "wald_immer_aria": "Jahresbalken: Leinenpflicht im Wald das ganze Jahr.",
        "wald_ohne_unter": "Keine saisonale Leinenpflicht {im}",
        "wald_ohne_aria": "Jahresbalken ohne saisonale Leinenpflicht.",
        "heute": {
            "heute": "heute", "datum": "{wt}, {t} {mon} {j}", "punkt": ".", "erster": "",
            "tage": ["1 Tag", "{n} Tage"], "tagen": ["1 Tag", "{n} Tagen"],
            "in_gross": "Heute Leinenpflicht im Wald",
            "in_text": "Bis {bis} gilt die Leinenpflicht {wo}. ",
            "letzter": "Heute ist der letzte Tag.", "noch": "Noch {n}.",
            "aus_gross": "Heute keine Leinenpflicht im Wald",
            "aus_text": "Die Leinenpflicht {wo} gilt wieder ab {von} {{j}}, also in {{n}}. Bis dahin muss dein Hund trotzdem unter Kontrolle bleiben, und Schilder vor Ort gehen vor.",
        },
        "regeln_h2": "Leine und Zutritt", "leine_chip": "Leine", "leine_h3": "Immer an die Leine",
        "verbot_chip": "Verbot", "verbot_h3": "Kein Zutritt für Hunde",
        "pflichten_h2": "Pflichten für Hundehaltende",
        "umzug": "Umzug in den {name}:",
        "vermisst_h2": "Hund vermisst oder gefunden {im}",
        "gewerbe_h2": "Hunde betreuen und ausbilden als Beruf {im}",
        "neu_h2": "Neu einen Hund {im}: die Schritte",
        "neu_p": "Du hast einen Hund übernommen oder holst bald einen zu dir? Hier stehen die Angaben dieser Seite in der Reihenfolge, in der sie für dich wichtig werden. Einzelheiten und Quellen findest du beim jeweiligen Punkt.",
        "neu_wald": "Leine im Wald",
        "blick_wald": "Was {im} im Wald gilt", "kt_alle": "Alle Einzelheiten und Quellen",
        "zum_inhalt": "Zum Inhalt",
        "lokal_h2": "Das gilt zusätzlich {in_ort}", "freilauf": "Freilaufzonen",
        "suche": {
            "lade": "Das Ortsverzeichnis wird geladen.",
            "fehler": "Die Ortssuche lässt sich gerade nicht laden. Wähle unten deinen Kanton.",
            "treffer": "{n} Treffer",
            "viele": "Die ersten {max} von {n} Treffern. Tippe weiter, um einzugrenzen.",
            "kt": "Kanton {name}",
            "gemeinde": "Gemeinde {name}",
            "lokal": "lokale Regeln",
            "kanton": "Regeln des Kantons",
            "bund": "Regeln des Bundes",
            "in-de": "auf Deutsch", "in-fr": "auf Französisch", "in-it": "auf Italienisch",
            "seiten_h": "Auf den Seiten gefunden",
            "s_lade": "Die Seiten werden durchsucht.",
            "s_eins": "Auf 1 Seite gefunden.", "s_treffer": "Auf {n} Seiten gefunden.",
            "s_viele": "Auf {n} Seiten gefunden, hier die ersten {max}.",
            "nichts": "Nichts gefunden. Prüfe die Schreibweise, versuche ein anderes Wort oder wähle unten deinen Kanton.",
            "s_fehler": "Die Suche auf den Seiten lässt sich gerade nicht laden.",
            "s_kantone": "Steht bei {n} Kantonen",
            "s_ohne": "Zu den übrigen Wörtern steht nichts auf den Seiten.",
        },
        "suche_label": "Ort, Postleitzahl oder Stichwort",
        "suche_beispiel": "z. B. Wettingen, 5430 oder Maulkorb",
        "suche_noscript": "Die Suche braucht JavaScript. Ohne JavaScript wählst du unten deinen Kanton.",
        "start_h1": "Was gilt für deinen Hund hier?",
        "start_lede": "Gib deine Gemeinde, deine Postleitzahl oder ein Stichwort wie Hundesteuer ein. Du siehst, was dort gilt: die Regeln des Bundes, deines Kantons und, wo es sie gibt, die lokalen Regeln deiner Gemeinde. Zu jeder Angabe findest du die amtliche Quelle.",
        "start_kt_h2": "Alle 26 Kantone",
        "start_kt_p": "Wähle deinen Kanton. Was der Bund für alle Hunde vorschreibt, steht unter <a href=\"{schweiz}\">Ganze Schweiz</a>{in_sprache}.",
        "start_gm_h2": "Gemeinden mit lokalen Regeln",
        "start_gm_p": "Für diese Gemeinden findest du zusätzlich lokale Angaben, zum Beispiel Hundetaxe, Leinenzonen oder Freilaufzonen. Für alle anderen gelten die Regeln des Kantons.",
        "start_vg_h2": "Kantone vergleichen",
        "start_vg_p": "Jedes Thema Kanton für Kanton. Hilfreich, wenn du umziehst oder wissen willst, wie es anderswo geregelt ist.",
        "vg_kanton": "Kanton",
        "start_titel": "Hunderegeln Schweiz nach Kanton und Gemeinde | Gassi-Kompass",
        "start_beschr": "Gemeinde oder Postleitzahl eingeben und sehen, was für Hunde gilt: Leinenpflicht, Haftpflicht, Kurse und Hundesteuer. Mit amtlicher Quelle zu jeder Angabe.",
        "kt_h1": "Hunderegeln {im}",
        "kt_lede": "Diese Regeln gelten in allen Gemeinden {des}. Gemeinden können zusätzliche Orte mit Leinenpflicht oder Hundeverbot festlegen.",
        "kt_hinweis": "Für diesen Ort haben wir noch keine lokalen Angaben. Auf dieser Seite stehen die Regeln, die im ganzen {name} gelten. Die Gemeinde kann zusätzliche Regeln haben.",
        "kt_gm_h2": "Lokale Regeln {im}",
        "kt_gm_p": "Fehlt deine Gemeinde, gelten die Regeln auf dieser Seite und die Schilder vor Ort.",
        "link_schweiz": "Was zusätzlich in der ganzen Schweiz gilt",
        "kt_themen_h2": "Ein Thema, alle Kantone", "kt_themen_p": "So regeln es die anderen Kantone.",
        "gm_kanton": "Alle Regeln {des}", "gm_weiter_h2": "Weiterlesen",
        "link_suche": "Anderen Ort suchen",
        "kt_titel": "Hunderegeln {im}: Leinenpflicht, Haftpflicht, Hundesteuer | Gassi-Kompass",
        "kt_beschr": "Was für Hunde {im} gilt: Leinenpflicht, Zutrittsverbote, Haftpflicht, Kurse, Hundesteuer und Rassenregeln. Mit amtlicher Quelle zu jeder Angabe.",
        "gm_h1": "Hunderegeln {in_ort}",
        "gm_weitere": "Weitere Orte {im}", "gm_uebrige": "Übrige Gemeinden",
        "gm_titel": "Hunderegeln {in_ort}: Leinenpflicht, Hundesteuer, Freilauf | Gassi-Kompass",
        "gm_beschr": "Was für Hunde {in_ort} gilt: lokale Regeln, Leinenpflicht, Hundesteuer und die Vorschriften {des}. Mit amtlicher Quelle zu jeder Angabe.",
        "bund": {
            "h1": "Das gilt in der ganzen Schweiz",
            "lede": "Diese Regeln des Bundes gelten in jedem Kanton und in jeder Gemeinde. Leinenpflicht, Haftpflichtversicherung, Rasselisten und Kurse sind je nach Kanton verschieden und stehen auf den Kantonsseiten.",
            "h2": "Pflichten für alle Hundehaltenden",
            "kt_h2": "Dazu kommt dein Kanton",
            "kt_p": "Leinenpflicht, Haftpflicht, Kurse und Rasselisten regelt dein Kanton. Wähle ihn aus.",
            "suche": "Gemeinde oder Postleitzahl suchen",
            "hinweis": "Der Kanton {kanton} hat noch keine eigene Seite. Auf dieser Seite steht, was in der ganzen Schweiz gilt. Kanton und Gemeinde können zusätzliche Regeln haben.",
            "titel": "Hunderegeln Schweiz: Was in allen Kantonen gilt | Gassi-Kompass",
            "beschr": "Was der Bund für alle Hunde in der Schweiz vorschreibt: Mikrochip, AMICUS, Anmeldung, Hundesteuer, Haltung und verbotene Hilfsmittel. Mit amtlicher Quelle zu jeder Angabe."
        },
        "thema": {
            "h1": "{name}: alle Kantone im Vergleich",
            "titel": "{name}: alle Kantone im Vergleich | Gassi-Kompass",
            "teil": "Diese Seite vergleicht {n} Kantone. Die übrigen findest du weiter unten.",
            "bund": "Was der Bund für alle Hunde vorschreibt, steht unter <a href=\"{schweiz}\">Ganze Schweiz</a>{in_sprache}.",
            "uebersetzt": "Bei Kantonen, in denen Deutsch keine Amtssprache ist, sind die Texte übersetzt. Die amtlichen Quellen sind in der Sprache des Kantons.",
            "ueberblick_h2": "{spalte} nach Kanton",
            "blick": "Auf einen Blick",
            "andere": "Weitere Kantone, auf ihrer Seite in der Sprache des Kantons:",
            "liste_p": "Wähle einen Kanton für Einzelheiten und Quellen. Gemeinden können zusätzliche Regeln haben.",
            "zum_kanton": "Alle Regeln {im}",
            "uebrige": "Die übrigen Kantone, mit allen Regeln auf ihrer Seite:",
            "alle_kt": "Alle Regeln jedes Kantons stehen auf seiner Seite:",
            "weitere_h2": "Weitere Themen",
            "alle": "alle Kantone",
            "wald_zahl": "In {m} der {n} Kantone gilt im Wald eine Leinenpflicht zu festen Daten{zeit}.",
            "wald_zeit": ", überall vom {von} bis {bis}",
            "wald_immer_zahl": " Das ganze Jahr gilt sie in {g} der {n} Kantone.",
            "wald_immer_wert": "Das ganze Jahr",
            "wald_rest": " Bei den übrigen nennt das kantonale Recht keine feste Leinenzeit. Was dort gilt, zum Beispiel Regeln der Gemeinden, steht beim Kanton.",
            "wald_wert": "{von} bis {bis}",
            "wald_text": "Leinenpflicht jedes Jahr {wo}.",
            "wald_ohne": "keine feste Zeit"
        },
        "themen": {
            "leinenpflicht-wald": {
                "name": "Leinenpflicht im Wald",
                "spalte": "Leine im Wald",
                "kurz": "Wo und von wann bis wann Hunde im Wald an die Leine müssen.",
                "beschr": "Leinenpflicht im Wald in der Schweiz: in welchen Kantonen sie gilt, von wann bis wann und wie weit ab Waldrand. Mit amtlicher Quelle zu jeder Angabe."
            },
            "haftpflicht": {
                "name": "Haftpflichtversicherung für Hunde",
                "spalte": "Haftpflicht",
                "kurz": "Wo die Versicherung Pflicht ist und welche Deckung verlangt wird.",
                "pflicht": "In {m} der {n} Kantone ist eine Haftpflichtversicherung für Hunde vorgeschrieben.",
                "beschr": "Haftpflichtversicherung für Hunde in der Schweiz: in welchen Kantonen sie Pflicht ist und welche Deckung verlangt wird. Mit amtlicher Quelle zu jeder Angabe."
            },
            "hundekurs": {
                "name": "Kurspflicht für Hundehaltende",
                "spalte": "Kurs",
                "kurz": "Wo ein Kurs Pflicht ist, für wen und in welcher Frist.",
                "pflicht": "In {m} der {n} Kantone ist ein Kurs für Hundehaltende vorgeschrieben. Bei den übrigen steht beim Kanton, ob ein Kurs für einzelne Hunde verlangt wird.",
                "beschr": "Hundekurs in der Schweiz: in welchen Kantonen ein Kurs Pflicht ist, für wen und in welcher Frist. Mit amtlicher Quelle zu jeder Angabe."
            },
            "rassen": {
                "name": "Rasselisten und Hundeverbote",
                "spalte": "Rassen",
                "kurz": "Welche Kantone Rassen verbieten oder eine Bewilligung verlangen.",
                "pflicht": "In {m} der {n} Kantone gilt für bestimmte Rassen eine Bewilligungspflicht oder ein Verbot.",
                "beschr": "Listenhunde in der Schweiz: welche Kantone Rassen verbieten oder eine Bewilligung verlangen und welche Rassen betroffen sind. Mit amtlicher Quelle zu jeder Angabe."
            },
            "hundesteuer": {
                "name": "Hundesteuer",
                "spalte": "Hundesteuer",
                "kurz": "Was ein Hund pro Jahr kostet und wer den Betrag festlegt.",
                "sonst": "Je nach Kanton legt der Kanton oder die Gemeinde den Betrag fest.",
                "beschr": "Hundesteuer in der Schweiz: was ein Hund pro Jahr kostet und wer den Betrag festlegt, Kanton für Kanton. Mit amtlicher Quelle zu jeder Angabe."
            },
            "gewerbe": {
                "name": "Hunde betreuen und ausbilden als Beruf",
                "kurz": "Wann Hundepension, Hundesitting oder Zucht eine Bewilligung brauchen und wo du sie beantragst.",
                "unter": "nach Kanton",
                "h1": "Hunde betreuen und ausbilden als Beruf: Bewilligungen",
                "titel": "Hundepension, Hundesitter, Hundeschule: Bewilligung nach Kanton | Gassi-Kompass",
                "lede": "Was gilt, wenn du gegen Entgelt fremde Hunde betreust, ausführst, ausbildest oder Hunde züchtest: wann es eine Bewilligung braucht und bei welcher Stelle du sie beantragst.",
                "bund_h2": "In der ganzen Schweiz",
                "kt_h2": "Nach Kanton",
                "kt_p": "Wähle einen Kanton für Einzelheiten und Quellen.",
                "beschr": "Hundepension, Hundetagesstätte, Hundesitter und Hundeschule in der Schweiz: wann es eine Bewilligung braucht und wo du sie beantragst. Mit amtlicher Quelle zu jeder Angabe."
            },
            "vermisst": {
                "name": "Hund vermisst oder gefunden",
                "kurz": "Wo du einen entlaufenen oder einen gefundenen Hund meldest.",
                "unter": "nach Kanton",
                "h1": "Hund vermisst oder gefunden: wo du es meldest",
                "titel": "Hund vermisst oder gefunden: Meldestellen nach Kanton | Gassi-Kompass",
                "lede": "Wo du einen entlaufenen Hund als vermisst meldest und wem du einen gefundenen Hund melden musst. Die Meldestelle ist je nach Kanton verschieden.",
                "bund_h2": "In der ganzen Schweiz",
                "kt_h2": "Nach Kanton",
                "kt_p": "Wähle einen Kanton für Einzelheiten und Quellen.",
                "beschr": "Hund entlaufen oder gefunden: wo du es in der Schweiz meldest, Kanton für Kanton. Mit amtlicher Quelle zu jeder Angabe."
            },
            "anmeldung": {
                "name": "Hund anmelden",
                "spalte": "Anmeldung",
                "kurz": "Bei welcher Stelle und in welcher Frist du deinen Hund meldest.",
                "sonst": "Wo und in welcher Frist du deinen Hund melden musst, ist je nach Kanton verschieden.",
                "beschr": "Hund anmelden in der Schweiz: bei welcher Stelle und in welcher Frist, Kanton für Kanton. Mit amtlicher Quelle zu jeder Angabe."
            }
        },
        "nf": {
            "h1": "Diese Seite gibt es nicht",
            "lede": "Vielleicht wurde die Adresse geändert. Such deinen Ort gleich hier oder geh zur Startseite.",
            "start": "Zur Startseite",
            "kurz": "Diese Seite gibt es nicht.",
            "titel": "Seite nicht gefunden | Gassi-Kompass"
        },
        "ueber": {
            "h1": "Über Gassi-Kompass",
            "lede": "Gassi-Kompass sammelt die Regeln für Hunde in der Schweiz an einem Ort: pro Kanton und pro Gemeinde, mit der amtlichen Quelle zu jeder Angabe.",
            "teile": [
                ("Woher die Angaben stammen", "Alle Angaben kommen aus amtlichen Quellen: Informationen des Bundes, Gesetze und Verordnungen der Kantone, Merkblätter der Veterinärdienste, Websites und offene Daten der Gemeinden. Wo ein politischer Entscheid nur in den Medien dokumentiert ist, steht das bei der Quelle."),
                ("In welcher Sprache", "Jede Seite ist aus den amtlichen Quellen in einer Amtssprache des Ortes zusammengestellt. In den anderen Sprachen ist sie eine Übersetzung. Das steht oben auf der Seite, mit einem Link zur Originalfassung. Die Namen der Quellen bleiben in der Originalsprache. Auch die Übersetzungen entstehen automatisiert mit KI-Unterstützung, dabei wird jede Zahl mit der Originalfassung verglichen."),
                ("Wie die Ortssuche funktioniert", "Die Suche kennt alle Gemeinden, Ortschaften und Postleitzahlen der Schweiz und ordnet sie dem Kanton zu. Sie zeigt dir die genaueste Seite, die es für deinen Ort schon gibt: die Gemeinde, sonst den Kanton, sonst die Regeln des Bundes. Grundlage ist das {swisstopo}Amtliche Ortschaftenverzeichnis</a>. Quelle: Bundesamt für Landestopografie swisstopo."),
                ("Wie geprüft wird", "Die Angaben werden automatisiert mit KI-Unterstützung zusammengestellt und regelmässig mit den Quellen abgeglichen. Auf jeder Seite steht, wann sie zuletzt geprüft wurde. Eine Gemeinde bekommt erst dann eine eigene Seite, wenn mindestens drei lokale Angaben amtlich belegt sind."),
                ("Fehler melden", "Stimmt eine Angabe nicht mehr oder fehlt etwas? Schreib an {mail}. Nenn bitte den Ort und, wenn du sie hast, die amtliche Quelle."),
                ("Was die Seite nicht ist", "Gassi-Kompass ist keine Rechtsberatung und kein Angebot eines Kantons oder einer Gemeinde. Massgebend sind Gesetz, Verordnung und die Schilder vor Ort. Regeln können sich ändern, und Fehler sind möglich. Im Zweifel gilt die verlinkte Quelle."),
            ],
            "schluss": "Gassi-Kompass ist ein privates Projekt aus der Schweiz.",
            "titel": "Über Gassi-Kompass: Quellen und Prüfung",
            "beschr": "Woher die Angaben auf Gassi-Kompass stammen, wie sie geprüft werden und was die Seite nicht ist.",
        },
    },
    "fr": {
        "name": "Français",
        "sprache": {"de": "en allemand", "fr": "en français", "it": "en italien"},
        "ueb": {"de": "Traduction de l'allemand. Les sources officielles sont en allemand.",
                "it": "Traduction de l'italien. Les sources officielles sont en italien."},
        "ueb_link": {"de": "Version originale en allemand", "it": "Version originale en italien"},
        "durchsicht": "Un résumé de ces règles a été relu le {datum} {wer}. Les ajouts ultérieurs ne font pas partie de cette relecture. Ce site est une offre privée.",
        "ueb_alt": "La version originale a été modifiée depuis et est plus récente que cette traduction.",
        "monate": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
                   "septembre", "octobre", "novembre", "décembre"],
        "mon3": ["janv", "févr", "mars", "avr", "mai", "juin", "juil", "août", "sept", "oct", "nov", "déc"],
        "wochentage": ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"],
        "start": "Accueil", "pfad": "Fil d'Ariane", "sprachwahl": "Langue",
        "teilbild": "Gassi-Kompass : les règles pour les chiens en Suisse, par canton et par commune",
        "stempel": "Vérifié le {d}",
        "quelle": "Source :", "quellen": "Sources :",
        "sprung": {"label": "Sur cette page", "wald": "Forêt", "leine": "Laisse et accès", "pflichten": "Obligations",
                   "neuer-hund": "Nouveau chien", "vermisst": "Chien perdu", "gewerbe": "Métier", "gemeinden": "Communes", "themen": "Thèmes",
                   "kantone": "Cantons", "quellen": "Sources"},
        "fuss_recht": "<strong>Pas un conseil juridique.</strong> Font foi la loi, l'ordonnance et la signalisation sur place. Gassi-Kompass est un projet privé et non une offre d'un canton ou d'une commune.",
        "fuss_fehler": "Une erreur ou un oubli ? Écrivez à {mail}.",
        "betreff": "Remarque sur ",
        "fuss_quellen": "Indications de cette page vérifiées le {d}. Sources :",
        "fuss_alle": "Afficher les {n} sources",
        "fussnav": "Navigation de pied de page",
        "nav_suche": "Chercher un lieu ou un mot", "nav_schweiz": "Toute la Suisse",
        "nav_vergleich": "Les cantons en comparaison", "nav_ueber": "À propos",
        "nav_quellen": "Toutes les sources",
        "qv": {
            "titel": "Sources officielles des règles sur les chiens en Suisse : lois cantonales sur les chiens",
            "beschr": "Toutes les sources officielles de Gassi-Kompass : lois et ordonnances cantonales sur les chiens, règlements communaux et pages de la Confédération, avec lien et pages qui les citent.",
            "pfad": "Sources", "h1": "Sources officielles",
            "lede": "Voici toutes les sources sur lesquelles s'appuient les pages de Gassi-Kompass, avec un lien vers la source et vers les pages qui la citent. Seule la source fait foi.",
            "label": "Chercher une source", "beispiel": "p. ex. loi sur les chiens, Sion",
            "wahl": "Champ d'application", "alle": "Toutes", "sort": "Trier", "nach_kanton": "Par canton", "nach_name": "Par nom",
            "bund": "Confédération", "kanton": "Canton", "zitiert": "Citée sur", "abgeglichen": "Dernière vérification le {d}",
            "s_alle": "{n} sources", "s_teil": "{n} sources sur {m}", "s_eins": "1 source sur {m}",
            "g_eins": "1 source", "g_viele": "{n} sources",
            "s_keine": "Aucune source trouvée. Vérifiez l'orthographe ou choisissez « Toutes ».",
        },
        "kanton_kurz": "Canton {kurz}",
        "n_gemeinden": ["1 commune", "{n} communes"],
        "fakten": ["cantons", "communes avec règles locales", "sources citées"],
        "wald_kopf": "Laisse en forêt",
        "wald_band": "Laisse",
        "wald_gross": "Laisse obligatoire en forêt du {von} au {bis}",
        "wald_text": "S'applique chaque année {wo}. En dehors de cette période, votre chien doit tout de même rester sous contrôle, et la signalisation sur place prime.",
        "wald_unter": "En couleur : laisse obligatoire en forêt, du {von} au {bis}",
        "wald_aria": "Barre annuelle : laisse obligatoire en forêt du {von} au {bis}.",
        "wald_ohne_gross": "Pas de période fixe en forêt",
        "wald_immer_gross": "Laisse obligatoire en forêt toute l'année",
        "wald_immer_unter": "En couleur : laisse obligatoire en forêt, toute l'année",
        "wald_immer_aria": "Barre annuelle : laisse obligatoire en forêt toute l'année.",
        "wald_ohne_unter": "Pas de laisse obligatoire saisonnière {im}",
        "wald_ohne_aria": "Barre annuelle sans laisse obligatoire saisonnière.",
        "heute": {
            "heute": "aujourd'hui", "datum": "{wt} {t} {mon} {j}", "punkt": "", "erster": "1er",
            "tage": ["1 jour", "{n} jours"], "tagen": ["1 jour", "{n} jours"],
            "in_gross": "Aujourd'hui, laisse obligatoire en forêt",
            "in_text": "Jusqu'au {bis}, la laisse est obligatoire {wo}. ",
            "letzter": "C'est le dernier jour.", "noch": "Encore {n}.",
            "aus_gross": "Aujourd'hui, pas de laisse obligatoire en forêt",
            "aus_text": "La laisse redevient obligatoire {wo} dès le {von} {{j}}, soit dans {{n}}. D'ici là, votre chien doit tout de même rester sous contrôle, et la signalisation sur place prime.",
        },
        "regeln_h2": "Laisse et accès", "leine_chip": "Laisse", "leine_h3": "Toujours en laisse",
        "verbot_chip": "Interdit", "verbot_h3": "Accès interdit aux chiens",
        "pflichten_h2": "Obligations des détenteurs de chiens",
        "umzug": "Déménagement {im} :",
        "vermisst_h2": "Chien perdu ou trouvé {im}",
        "gewerbe_h2": "Garder et éduquer des chiens à titre professionnel {im}",
        "neu_h2": "Nouveau chien {im} : les étapes",
        "neu_p": "Vous avez pris en charge un chien ou vous en accueillez bientôt un ? Voici les informations de cette page dans l'ordre où elles deviennent importantes pour vous. Les détails et les sources se trouvent sous chaque point.",
        "neu_wald": "Laisse en forêt",
        "blick_wald": "Ce qui s'applique en forêt {im}", "kt_alle": "Tous les détails et les sources",
        "zum_inhalt": "Aller au contenu",
        "lokal_h2": "Règles supplémentaires {in_ort}", "freilauf": "Espaces de liberté pour chiens",
        "suche": {
            "lade": "Le répertoire des localités se charge.",
            "fehler": "La recherche ne peut pas être chargée pour l'instant. Choisissez votre canton ci-dessous.",
            "treffer": "Résultats : {n}",
            "viele": "Les {max} premiers résultats sur {n}. Continuez à taper pour préciser.",
            "kt": "{name} (canton)",
            "gemeinde": "commune : {name}",
            "lokal": "règles locales",
            "kanton": "règles du canton",
            "bund": "règles fédérales",
            "in-de": "en allemand", "in-fr": "en français", "in-it": "en italien",
            "seiten_h": "Trouvé dans les pages",
            "s_lade": "Recherche dans les pages en cours.",
            "s_eins": "Trouvé sur 1 page.", "s_treffer": "Trouvé sur {n} pages.",
            "s_viele": "Trouvé sur {n} pages, voici les {max} premières.",
            "nichts": "Aucun résultat. Vérifiez l'orthographe, essayez un autre mot ou choisissez votre canton ci-dessous.",
            "s_fehler": "La recherche dans les pages ne peut pas être chargée pour l'instant.",
            "s_kantone": "Mentionné pour {n} cantons",
            "s_ohne": "Rien dans les pages pour les autres mots.",
        },
        "suche_label": "Localité, code postal ou mot-clé",
        "suche_beispiel": "p. ex. Montreux, 1820 ou muselière",
        "suche_noscript": "La recherche a besoin de JavaScript. Sans JavaScript, choisissez votre canton ci-dessous.",
        "start_h1": "Quelles règles pour votre chien ici ?",
        "start_lede": "Saisissez votre commune, votre code postal ou un mot-clé comme impôt. Vous voyez ce qui s'y applique : les règles fédérales, celles de votre canton et, lorsqu'elles existent, les règles locales de votre commune. Chaque indication renvoie à sa source officielle.",
        "start_kt_h2": "Les 26 cantons",
        "start_kt_p": "Choisissez votre canton. Ce que la Confédération prescrit pour tous les chiens figure sur la page <a href=\"{schweiz}\">Toute la Suisse</a>{in_sprache}.",
        "start_gm_h2": "Communes avec règles locales",
        "start_gm_p": "Pour ces communes, vous trouvez en plus des indications locales, par exemple l'impôt sur les chiens, les lieux où la laisse est obligatoire ou les espaces de liberté. Pour toutes les autres, les règles du canton s'appliquent.",
        "start_vg_h2": "Comparer les cantons",
        "start_vg_p": "Chaque thème, canton par canton. Utile si vous déménagez ou si vous voulez savoir comment c'est réglé ailleurs.",
        "vg_kanton": "Canton",
        "start_titel": "Règles pour les chiens en Suisse par canton et par commune | Gassi-Kompass",
        "start_beschr": "Saisissez une commune ou un code postal et voyez ce qui vaut pour les chiens : laisse obligatoire, assurance responsabilité civile, cours et impôt sur les chiens. Avec la source officielle de chaque indication.",
        "kt_h1": "Règles pour les chiens {im}",
        "kt_lede": "Ces règles valent dans toutes les communes {des}. Les communes peuvent désigner d'autres lieux où la laisse est obligatoire ou les chiens interdits.",
        "kt_hinweis": "Nous n'avons pas encore d'indications locales pour ce lieu. Cette page présente les règles valables partout {im}. La commune peut avoir des règles supplémentaires.",
        "kt_gm_h2": "Règles locales {im}",
        "kt_gm_p": "Si votre commune manque, les règles de cette page et la signalisation sur place s'appliquent.",
        "link_schweiz": "Ce qui vaut en plus dans toute la Suisse",
        "kt_themen_h2": "Un thème, tous les cantons", "kt_themen_p": "Voici comment les autres cantons règlent la question.",
        "gm_kanton": "Toutes les règles {des}", "gm_weiter_h2": "Pour aller plus loin",
        "link_suche": "Chercher un autre lieu",
        "kt_titel": "Règles pour les chiens {im} : laisse obligatoire, assurance RC, impôt | Gassi-Kompass",
        "kt_beschr": "Ce qui vaut pour les chiens {im} : laisse obligatoire, lieux interdits, assurance responsabilité civile, cours, impôt sur les chiens et races. Avec la source officielle de chaque indication.",
        "gm_h1": "Règles pour les chiens {in_ort}",
        "gm_weitere": "Autres lieux {im}", "gm_uebrige": "Autres communes",
        "gm_titel": "Règles pour les chiens {in_ort} : laisse obligatoire, impôt, espaces de liberté | Gassi-Kompass",
        "gm_beschr": "Ce qui vaut pour les chiens {in_ort} : règles locales, laisse obligatoire, impôt sur les chiens et prescriptions {des}. Avec la source officielle de chaque indication.",
        "bund": {
            "h1": "Ce qui vaut dans toute la Suisse",
            "lede": "Ces règles fédérales valent dans chaque canton et dans chaque commune. La laisse obligatoire, l'assurance responsabilité civile, les listes de races et les cours varient selon le canton et figurent sur les pages des cantons.",
            "h2": "Obligations de tous les détenteurs de chiens",
            "kt_h2": "S'y ajoutent les règles de votre canton",
            "kt_p": "La laisse, l'assurance responsabilité civile, les cours et les listes de races relèvent de votre canton. Choisissez-le.",
            "suche": "Chercher une commune ou un code postal",
            "hinweis": "Le canton {kanton} n'a pas encore sa propre page. Cette page présente ce qui vaut dans toute la Suisse. Le canton et la commune peuvent avoir des règles supplémentaires.",
            "titel": "Règles pour les chiens en Suisse : ce qui vaut dans tous les cantons | Gassi-Kompass",
            "beschr": "Ce que la Confédération prescrit pour tous les chiens en Suisse : puce électronique, AMICUS, annonce, taxe sur les chiens, détention et moyens auxiliaires interdits. Avec la source officielle de chaque indication."
        },
        "thema": {
            "h1": "{name} : tous les cantons en comparaison",
            "titel": "{name} : tous les cantons en comparaison | Gassi-Kompass",
            "teil": "Cette page compare {n} cantons. Les autres figurent plus bas.",
            "bund": "Ce que la Confédération prescrit pour tous les chiens figure sur la page <a href=\"{schweiz}\">Toute la Suisse</a>{in_sprache}.",
            "uebersetzt": "Pour les cantons où le français n'est pas une langue officielle, les textes sont traduits. Les sources officielles sont dans la langue du canton.",
            "ueberblick_h2": "{spalte} par canton",
            "blick": "En bref",
            "andere": "Autres cantons, sur leur page dans la langue du canton :",
            "liste_p": "Choisissez un canton pour les détails et les sources. Les communes peuvent avoir des règles supplémentaires.",
            "zum_kanton": "Toutes les règles {im}",
            "uebrige": "Les autres cantons, avec toutes leurs règles sur leur page :",
            "alle_kt": "Toutes les règles de chaque canton figurent sur sa page :",
            "weitere_h2": "Autres thèmes",
            "alle": "tous les cantons",
            "wald_zahl": "Dans {m} des {n} cantons, la laisse est obligatoire en forêt à des dates fixes{zeit}.",
            "wald_zeit": ", partout du {von} au {bis}",
            "wald_immer_zahl": " Elle vaut toute l'année dans {g} des {n} cantons.",
            "wald_immer_wert": "Toute l'année",
            "wald_rest": " Dans les autres, le droit cantonal ne fixe pas de période. Ce qui s'y applique, par exemple des règles communales, figure sur la page du canton.",
            "wald_wert": "du {von} au {bis}",
            "wald_text": "Laisse obligatoire chaque année {wo}.",
            "wald_ohne": "pas de période"
        },
        "themen": {
            "leinenpflicht-wald": {
                "name": "Laisse obligatoire en forêt",
                "spalte": "Laisse en forêt",
                "kurz": "Où et de quand à quand les chiens doivent être tenus en laisse en forêt.",
                "beschr": "Laisse obligatoire en forêt en Suisse : dans quels cantons elle s'applique, de quand à quand et jusqu'à quelle distance de la lisière. Avec la source officielle de chaque indication."
            },
            "haftpflicht": {
                "name": "Assurance responsabilité civile pour chiens",
                "spalte": "Responsabilité civile",
                "kurz": "Où l'assurance est obligatoire et quelle couverture est exigée.",
                "pflicht": "Dans {m} des {n} cantons, une assurance responsabilité civile pour chiens est obligatoire.",
                "beschr": "Assurance responsabilité civile pour chiens en Suisse : dans quels cantons elle est obligatoire et quelle couverture est exigée. Avec la source officielle de chaque indication."
            },
            "hundekurs": {
                "name": "Cours obligatoires pour détenteurs de chiens",
                "spalte": "Cours",
                "kurz": "Où un cours est obligatoire, pour qui et dans quel délai.",
                "pflicht": "Dans {m} des {n} cantons, un cours est obligatoire pour les détenteurs de chiens. Pour les autres, la page du canton indique si un cours est exigé pour certains chiens.",
                "beschr": "Cours pour chiens en Suisse : dans quels cantons un cours est obligatoire, pour qui et dans quel délai. Avec la source officielle de chaque indication."
            },
            "rassen": {
                "name": "Listes de races et chiens interdits",
                "spalte": "Races",
                "kurz": "Quels cantons interdisent des races ou exigent une autorisation.",
                "pflicht": "Dans {m} des {n} cantons, certaines races sont soumises à autorisation ou interdites.",
                "beschr": "Chiens de races listées en Suisse : quels cantons interdisent des races ou exigent une autorisation, et quelles races sont concernées. Avec la source officielle de chaque indication."
            },
            "hundesteuer": {
                "name": "Impôt sur les chiens",
                "spalte": "Impôt sur les chiens",
                "kurz": "Ce que coûte un chien par an et qui fixe le montant.",
                "sonst": "Selon le canton, le montant est fixé par le canton ou par la commune.",
                "beschr": "Impôt sur les chiens en Suisse : ce que coûte un chien par an et qui fixe le montant, canton par canton. Avec la source officielle de chaque indication."
            },
            "gewerbe": {
                "name": "Garder et éduquer des chiens à titre professionnel",
                "kurz": "Quand une pension, la garde de chiens ou l'élevage demandent une autorisation et où la demander.",
                "unter": "par canton",
                "h1": "Garder et éduquer des chiens à titre professionnel : autorisations",
                "titel": "Pension pour chiens, garde, éducation canine : autorisation par canton | Gassi-Kompass",
                "lede": "Ce qui s'applique si vous gardez, promenez ou éduquez des chiens de tiers contre rémunération, ou si vous élevez des chiens : quand il faut une autorisation et à quel service la demander.",
                "bund_h2": "Dans toute la Suisse",
                "kt_h2": "Par canton",
                "kt_p": "Choisissez un canton pour les détails et les sources.",
                "beschr": "Pension pour chiens, garderie, garde de chiens et éducation canine en Suisse : quand il faut une autorisation et où la demander. Avec la source officielle de chaque indication."
            },
            "vermisst": {
                "name": "Chien perdu ou trouvé",
                "kurz": "Où annoncer un chien qui s'est échappé ou un chien trouvé.",
                "unter": "par canton",
                "h1": "Chien perdu ou trouvé : où l'annoncer",
                "titel": "Chien perdu ou trouvé : où l'annoncer, canton par canton | Gassi-Kompass",
                "lede": "Où annoncer la disparition de votre chien et à qui annoncer un chien trouvé. Le service compétent varie selon le canton.",
                "bund_h2": "Dans toute la Suisse",
                "kt_h2": "Par canton",
                "kt_p": "Choisissez un canton pour les détails et les sources.",
                "beschr": "Chien perdu ou trouvé : où l'annoncer en Suisse, canton par canton. Avec la source officielle de chaque indication."
            },
            "anmeldung": {
                "name": "Annoncer son chien",
                "spalte": "Annonce",
                "kurz": "Auprès de quel service et dans quel délai annoncer votre chien.",
                "sonst": "Le service auquel annoncer votre chien et le délai varient selon le canton.",
                "beschr": "Annoncer son chien en Suisse : auprès de quel service et dans quel délai, canton par canton. Avec la source officielle de chaque indication."
            }
        },
        "nf": {
            "h1": "Cette page n'existe pas",
            "lede": "L'adresse a peut-être changé. Cherchez votre lieu ici ou retournez à l'accueil.",
            "start": "Vers l'accueil en français",
            "kurz": "Cette page n'existe pas.",
            "titel": "Page introuvable | Gassi-Kompass"
        },
        "ueber": {
            "h1": "À propos de Gassi-Kompass",
            "lede": "Gassi-Kompass réunit les règles pour les chiens en Suisse en un seul endroit : par canton et par commune, avec la source officielle de chaque indication.",
            "teile": [
                ("D'où viennent les indications", "Toutes les indications proviennent de sources officielles : informations de la Confédération, lois et ordonnances des cantons, aide-mémoire des services vétérinaires, sites et données ouvertes des communes. Lorsqu'une décision politique n'est documentée que dans les médias, la source le précise."),
                ("Dans quelle langue", "Chaque page est rédigée à partir des sources officielles dans une langue officielle du lieu. Dans les autres langues, la page est une traduction. C'est indiqué en haut de la page, avec un lien vers la version originale. Les noms des sources restent dans la langue d'origine. Les traductions sont elles aussi réalisées de manière automatisée avec l'aide de l'IA, et chaque chiffre est comparé à la version originale."),
                ("Comment fonctionne la recherche", "La recherche connaît toutes les communes, localités et codes postaux de Suisse et les rattache au canton. Elle vous montre la page la plus précise qui existe déjà pour votre lieu : la commune, sinon le canton, sinon les règles fédérales. Elle s'appuie sur le {swisstopo}Répertoire officiel des localités</a>. Source : Office fédéral de topographie swisstopo."),
                ("Comment les indications sont vérifiées", "Les indications sont réunies de manière automatisée avec l'aide de l'IA et comparées régulièrement aux sources. Chaque page indique la date de la dernière vérification. Une commune n'obtient sa propre page que si au moins trois indications locales sont attestées par une source officielle."),
                ("Signaler une erreur", "Une indication n'est plus exacte ou il manque quelque chose ? Écrivez à {mail}. Indiquez le lieu et, si vous l'avez, la source officielle."),
                ("Ce que le site n'est pas", "Gassi-Kompass n'est ni un conseil juridique ni une offre d'un canton ou d'une commune. Font foi la loi, l'ordonnance et la signalisation sur place. Les règles peuvent changer et des erreurs sont possibles. En cas de doute, la source indiquée fait foi."),
            ],
            "schluss": "Gassi-Kompass est un projet privé de Suisse.",
            "titel": "À propos de Gassi-Kompass : sources et vérification",
            "beschr": "D'où viennent les indications de Gassi-Kompass, comment elles sont vérifiées et ce que le site n'est pas.",
        },
    },
    "it": {
        "name": "Italiano",
        "sprache": {"de": "in tedesco", "fr": "in francese", "it": "in italiano"},
        "ueb": {"de": "Traduzione dal tedesco. Le fonti ufficiali sono in tedesco.",
                "fr": "Traduzione dal francese. Le fonti ufficiali sono in francese."},
        "ueb_link": {"de": "Versione originale in tedesco", "fr": "Versione originale in francese"},
        "durchsicht": "Un riassunto di queste regole è stato esaminato il {datum} {wer}. Le aggiunte successive non fanno parte di questo esame. Questo sito è un'offerta privata.",
        "ueb_alt": "La versione originale è stata modificata nel frattempo ed è più recente di questa traduzione.",
        "monate": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
                   "settembre", "ottobre", "novembre", "dicembre"],
        "mon3": ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"],
        "wochentage": ["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"],
        "start": "Inizio", "pfad": "Percorso", "sprachwahl": "Lingua",
        "teilbild": "Gassi-Kompass: le regole per i cani in Svizzera, per Cantone e Comune",
        "stempel": "Verificato il {d}",
        "quelle": "Fonte:", "quellen": "Fonti:",
        "sprung": {"label": "In questa pagina", "wald": "Bosco", "leine": "Guinzaglio e accesso", "pflichten": "Obblighi",
                   "neuer-hund": "Nuovo cane", "vermisst": "Cane smarrito", "gewerbe": "Professione", "gemeinden": "Comuni", "themen": "Temi",
                   "kantone": "Cantoni", "quellen": "Fonti"},
        "fuss_recht": "<strong>Nessuna consulenza legale.</strong> Fanno stato la legge, l'ordinanza e la segnaletica sul posto. Gassi-Kompass è un progetto privato e non un'offerta di un Cantone o di un Comune.",
        "fuss_fehler": "Qualcosa non è corretto o manca? Scrivi a {mail}.",
        "betreff": "Segnalazione su ",
        "fuss_quellen": "Indicazioni di questa pagina verificate il {d}. Fonti:",
        "fuss_alle": "Mostra le {n} fonti",
        "fussnav": "Navigazione a piè di pagina",
        "nav_suche": "Cerca un luogo o una parola", "nav_schweiz": "Tutta la Svizzera",
        "nav_vergleich": "Cantoni a confronto", "nav_ueber": "Informazioni",
        "nav_quellen": "Tutte le fonti",
        "qv": {
            "titel": "Fonti ufficiali sulle regole per i cani in Svizzera: leggi cantonali sui cani",
            "beschr": "Tutte le fonti ufficiali di Gassi-Kompass: leggi e ordinanze cantonali sui cani, regolamenti comunali e pagine della Confederazione, con link e pagine che le citano.",
            "pfad": "Fonti", "h1": "Fonti ufficiali",
            "lede": "Qui trovi tutte le fonti su cui si basano le pagine di Gassi-Kompass, con un link alla fonte e alle pagine che la citano. Fa stato solo la fonte.",
            "label": "Cerca una fonte", "beispiel": "p. es. legge sui cani, Lugano",
            "wahl": "Ambito", "alle": "Tutte", "sort": "Ordina", "nach_kanton": "Per cantone", "nach_name": "Per nome",
            "bund": "Confederazione", "kanton": "Cantone", "zitiert": "Citata in", "abgeglichen": "Ultima verifica il {d}",
            "s_alle": "{n} fonti", "s_teil": "{n} fonti su {m}", "s_eins": "1 fonte su {m}",
            "g_eins": "1 fonte", "g_viele": "{n} fonti",
            "s_keine": "Nessuna fonte trovata. Controlla l'ortografia o scegli «Tutte».",
        },
        "kanton_kurz": "Cantone {kurz}",
        "n_gemeinden": ["1 Comune", "{n} Comuni"],
        "fakten": ["Cantoni", "Comuni con regole locali", "fonti citate"],
        "wald_kopf": "Guinzaglio nel bosco",
        "wald_band": "Guinzaglio",
        "wald_gross": "Obbligo di guinzaglio nel bosco {dal_von} {al_bis}",
        "wald_text": "Vale ogni anno {wo}. Fuori da questo periodo il tuo cane deve comunque restare sotto controllo, e la segnaletica sul posto ha la precedenza.",
        "wald_unter": "Evidenziato: obbligo di guinzaglio nel bosco, {dal_von} {al_bis}",
        "wald_aria": "Barra annuale: obbligo di guinzaglio nel bosco {dal_von} {al_bis}.",
        "wald_ohne_gross": "Nessun periodo fisso nel bosco",
        "wald_immer_gross": "Obbligo di guinzaglio nel bosco tutto l'anno",
        "wald_immer_unter": "Evidenziato: obbligo di guinzaglio nel bosco, tutto l'anno",
        "wald_immer_aria": "Barra annuale: obbligo di guinzaglio nel bosco tutto l'anno.",
        "wald_ohne_unter": "Nessun obbligo stagionale di guinzaglio {im}",
        "wald_ohne_aria": "Barra annuale senza obbligo stagionale di guinzaglio.",
        "heute": {
            "heute": "oggi", "datum": "{wt} {t} {mon} {j}", "punkt": "", "erster": "1°",
            "tage": ["1 giorno", "{n} giorni"], "tagen": ["1 giorno", "{n} giorni"],
            "in_gross": "Oggi obbligo di guinzaglio nel bosco",
            "in_text": "Fino {al_bis} vale l'obbligo di guinzaglio {wo}. ",
            "letzter": "Oggi è l'ultimo giorno.", "noch": "Ancora {n}.",
            "aus_gross": "Oggi nessun obbligo di guinzaglio nel bosco",
            "aus_text": "L'obbligo di guinzaglio {wo} torna a valere {dal_von} {{j}}, cioè tra {{n}}. Fino ad allora il tuo cane deve comunque restare sotto controllo, e la segnaletica sul posto ha la precedenza.",
        },
        "regeln_h2": "Guinzaglio e accesso", "leine_chip": "Guinzaglio", "leine_h3": "Sempre al guinzaglio",
        "verbot_chip": "Divieto", "verbot_h3": "Accesso vietato ai cani",
        "pflichten_h2": "Obblighi per chi detiene un cane",
        "umzug": "Trasloco {im}:",
        "vermisst_h2": "Cane smarrito o trovato {im}",
        "gewerbe_h2": "Custodire ed educare cani per professione {im}",
        "neu_h2": "Un nuovo cane {im}: i passi",
        "neu_p": "Hai preso a carico un cane o ne accogli presto uno? Qui trovi le indicazioni di questa pagina nell'ordine in cui diventano importanti per te. Dettagli e fonti si trovano al punto corrispondente.",
        "neu_wald": "Guinzaglio nel bosco",
        "blick_wald": "Cosa vale nel bosco {im}", "kt_alle": "Tutti i dettagli e le fonti",
        "zum_inhalt": "Vai al contenuto",
        "lokal_h2": "Regole supplementari {in_ort}", "freilauf": "Aree di svago per cani",
        "suche": {
            "lade": "L'elenco delle località è in caricamento.",
            "fehler": "La ricerca non può essere caricata in questo momento. Scegli il tuo Cantone qui sotto.",
            "treffer": "Risultati: {n}",
            "viele": "I primi {max} risultati su {n}. Continua a scrivere per restringere.",
            "kt": "{name} (Cantone)",
            "gemeinde": "Comune di {name}",
            "lokal": "regole locali",
            "kanton": "regole del Cantone",
            "bund": "regole federali",
            "in-de": "in tedesco", "in-fr": "in francese", "in-it": "in italiano",
            "seiten_h": "Trovato nelle pagine",
            "s_lade": "Ricerca nelle pagine in corso.",
            "s_eins": "Trovato in 1 pagina.", "s_treffer": "Trovato in {n} pagine.",
            "s_viele": "Trovato in {n} pagine, ecco le prime {max}.",
            "nichts": "Nessun risultato. Controlla l'ortografia, prova un'altra parola o scegli il tuo Cantone qui sotto.",
            "s_fehler": "La ricerca nelle pagine non può essere caricata in questo momento.",
            "s_kantone": "Citato per {n} Cantoni",
            "s_ohne": "Nulla nelle pagine per le altre parole.",
        },
        "suche_label": "Luogo, numero postale o parola chiave",
        "suche_beispiel": "p. es. Mendrisio, 6850 o museruola",
        "suche_noscript": "La ricerca ha bisogno di JavaScript. Senza JavaScript scegli il tuo Cantone qui sotto.",
        "start_h1": "Cosa vale qui per il tuo cane?",
        "start_lede": "Inserisci il tuo Comune, il numero postale di avviamento o una parola chiave come imposta. Vedi cosa vale lì: le regole federali, quelle del tuo Cantone e, dove esistono, le regole locali del tuo Comune. Per ogni indicazione trovi la fonte ufficiale.",
        "start_kt_h2": "Tutti i 26 Cantoni",
        "start_kt_p": "Scegli il tuo Cantone. Cosa prescrive la Confederazione per tutti i cani si trova sulla pagina <a href=\"{schweiz}\">Tutta la Svizzera</a>{in_sprache}.",
        "start_gm_h2": "Comuni con regole locali",
        "start_gm_p": "Per questi Comuni trovi anche indicazioni locali, per esempio l'imposta sui cani, i luoghi con obbligo di guinzaglio o le aree di svago per cani. Per tutti gli altri valgono le regole del Cantone.",
        "start_vg_h2": "Confrontare i Cantoni",
        "start_vg_p": "Ogni tema, Cantone per Cantone. Utile se ti trasferisci o vuoi sapere com'è regolato altrove.",
        "vg_kanton": "Cantone",
        "start_titel": "Regole per i cani in Svizzera per Cantone e Comune | Gassi-Kompass",
        "start_beschr": "Inserisci un Comune o un numero postale di avviamento e vedi cosa vale per i cani: obbligo di guinzaglio, responsabilità civile, corsi e imposta sui cani. Con la fonte ufficiale per ogni indicazione.",
        "kt_h1": "Regole per i cani {im}",
        "kt_lede": "Queste regole valgono in tutti i Comuni {des}. I Comuni possono stabilire altri luoghi con obbligo di guinzaglio o divieto per i cani.",
        "kt_hinweis": "Per questo luogo non abbiamo ancora indicazioni locali. Questa pagina riporta le regole che valgono ovunque {im}. Il Comune può avere regole supplementari.",
        "kt_gm_h2": "Regole locali {im}",
        "kt_gm_p": "Se il tuo Comune manca, valgono le regole di questa pagina e la segnaletica sul posto.",
        "link_schweiz": "Cosa vale in più in tutta la Svizzera",
        "kt_themen_h2": "Un tema, tutti i Cantoni", "kt_themen_p": "Ecco come lo regolano gli altri Cantoni.",
        "gm_kanton": "Tutte le regole {des}", "gm_weiter_h2": "Per saperne di più",
        "link_suche": "Cerca un altro luogo",
        "kt_titel": "Regole per i cani {im}: obbligo di guinzaglio, responsabilità civile, imposta | Gassi-Kompass",
        "kt_beschr": "Cosa vale per i cani {im}: obbligo di guinzaglio, luoghi vietati, responsabilità civile, corsi, imposta sui cani e razze. Con la fonte ufficiale per ogni indicazione.",
        "gm_h1": "Regole per i cani {in_ort}",
        "gm_weitere": "Altri luoghi {im}", "gm_uebrige": "Altri Comuni",
        "gm_titel": "Regole per i cani {in_ort}: obbligo di guinzaglio, imposta, aree per cani | Gassi-Kompass",
        "gm_beschr": "Cosa vale per i cani {in_ort}: regole locali, obbligo di guinzaglio, imposta sui cani e prescrizioni {des}. Con la fonte ufficiale per ogni indicazione.",
        "bund": {
            "h1": "Cosa vale in tutta la Svizzera",
            "lede": "Queste regole federali valgono in ogni Cantone e in ogni Comune. L'obbligo di guinzaglio, l'assicurazione di responsabilità civile, gli elenchi di razze e i corsi cambiano da Cantone a Cantone e si trovano sulle pagine dei Cantoni.",
            "h2": "Obblighi per tutti i detentori di cani",
            "kt_h2": "Si aggiungono le regole del tuo Cantone",
            "kt_p": "Guinzaglio, responsabilità civile, corsi ed elenchi di razze sono regolati dal tuo Cantone. Sceglilo.",
            "suche": "Cerca un Comune o un numero postale di avviamento",
            "hinweis": "Il Cantone {kanton} non ha ancora una pagina propria. Questa pagina riporta ciò che vale in tutta la Svizzera. Il Cantone e il Comune possono avere regole supplementari.",
            "titel": "Regole per i cani in Svizzera: cosa vale in tutti i Cantoni | Gassi-Kompass",
            "beschr": "Cosa prescrive la Confederazione per tutti i cani in Svizzera: microchip, AMICUS, notifica, imposta sui cani, detenzione e mezzi ausiliari vietati. Con la fonte ufficiale per ogni indicazione."
        },
        "thema": {
            "h1": "{name}: tutti i Cantoni a confronto",
            "titel": "{name}: tutti i Cantoni a confronto | Gassi-Kompass",
            "teil": "Questa pagina confronta {n} Cantoni. Gli altri si trovano più in basso.",
            "bund": "Cosa prescrive la Confederazione per tutti i cani si trova sulla pagina <a href=\"{schweiz}\">Tutta la Svizzera</a>{in_sprache}.",
            "uebersetzt": "Per i Cantoni in cui l'italiano non è lingua ufficiale, i testi sono tradotti. Le fonti ufficiali sono nella lingua del Cantone.",
            "ueberblick_h2": "{spalte} per Cantone",
            "blick": "In breve",
            "andere": "Altri Cantoni, sulla loro pagina nella lingua del Cantone:",
            "liste_p": "Scegli un Cantone per i dettagli e le fonti. I Comuni possono avere regole supplementari.",
            "zum_kanton": "Tutte le regole {im}",
            "uebrige": "Gli altri Cantoni, con tutte le regole sulla loro pagina:",
            "alle_kt": "Tutte le regole di ogni Cantone sono sulla sua pagina:",
            "weitere_h2": "Altri temi",
            "alle": "tutti i Cantoni",
            "wald_zahl": "In {m} dei {n} Cantoni vale nel bosco un obbligo di guinzaglio a date fisse{zeit}.",
            "wald_zeit": ", ovunque {dal_von} {al_bis}",
            "wald_immer_zahl": " Vale tutto l'anno in {g} dei {n} Cantoni.",
            "wald_immer_wert": "Tutto l'anno",
            "wald_rest": " Negli altri il diritto cantonale non fissa un periodo. Ciò che vale lì, per esempio regole comunali, si trova sulla pagina del Cantone.",
            "wald_wert": "{dal_von} {al_bis}",
            "wald_text": "Obbligo di guinzaglio ogni anno {wo}.",
            "wald_ohne": "nessun periodo"
        },
        "themen": {
            "leinenpflicht-wald": {
                "name": "Obbligo di guinzaglio nel bosco",
                "spalte": "Guinzaglio nel bosco",
                "kurz": "Dove e da quando a quando i cani vanno tenuti al guinzaglio nel bosco.",
                "beschr": "Obbligo di guinzaglio nel bosco in Svizzera: in quali Cantoni vale, da quando a quando e fino a che distanza dal margine del bosco. Con la fonte ufficiale per ogni indicazione."
            },
            "haftpflicht": {
                "name": "Assicurazione di responsabilità civile per cani",
                "spalte": "Responsabilità civile",
                "kurz": "Dove l'assicurazione è obbligatoria e quale copertura è richiesta.",
                "pflicht": "In {m} dei {n} Cantoni è obbligatoria un'assicurazione di responsabilità civile per i cani.",
                "beschr": "Assicurazione di responsabilità civile per cani in Svizzera: in quali Cantoni è obbligatoria e quale copertura è richiesta. Con la fonte ufficiale per ogni indicazione."
            },
            "hundekurs": {
                "name": "Corsi obbligatori per chi detiene un cane",
                "spalte": "Corso",
                "kurz": "Dove un corso è obbligatorio, per chi ed entro quale termine.",
                "pflicht": "In {m} dei {n} Cantoni è obbligatorio un corso per chi detiene un cane. Per gli altri, la pagina del Cantone indica se un corso è richiesto per singoli cani.",
                "beschr": "Corsi per cani in Svizzera: in quali Cantoni un corso è obbligatorio, per chi ed entro quale termine. Con la fonte ufficiale per ogni indicazione."
            },
            "rassen": {
                "name": "Elenchi di razze e cani vietati",
                "spalte": "Razze",
                "kurz": "Quali Cantoni vietano alcune razze o richiedono un'autorizzazione.",
                "pflicht": "In {m} dei {n} Cantoni alcune razze sono soggette ad autorizzazione o vietate.",
                "beschr": "Razze soggette a restrizioni in Svizzera: quali Cantoni vietano alcune razze o richiedono un'autorizzazione e quali razze sono interessate. Con la fonte ufficiale per ogni indicazione."
            },
            "hundesteuer": {
                "name": "Imposta sui cani",
                "spalte": "Imposta sui cani",
                "kurz": "Quanto costa un cane all'anno e chi fissa l'importo.",
                "sonst": "A seconda del Cantone, l'importo è fissato dal Cantone o dal Comune.",
                "beschr": "Imposta sui cani in Svizzera: quanto costa un cane all'anno e chi fissa l'importo, Cantone per Cantone. Con la fonte ufficiale per ogni indicazione."
            },
            "gewerbe": {
                "name": "Custodire ed educare cani per professione",
                "kurz": "Quando pensione, custodia di cani o allevamento richiedono un'autorizzazione e dove chiederla.",
                "unter": "per Cantone",
                "h1": "Custodire ed educare cani per professione: autorizzazioni",
                "titel": "Pensione per cani, dog sitter, educazione cinofila: autorizzazione per Cantone | Gassi-Kompass",
                "lede": "Cosa vale se custodisci, porti a passeggio o educhi cani di terzi dietro compenso, o se allevi cani: quando serve un'autorizzazione e a quale servizio chiederla.",
                "bund_h2": "In tutta la Svizzera",
                "kt_h2": "Per Cantone",
                "kt_p": "Scegli un Cantone per i dettagli e le fonti.",
                "beschr": "Pensione per cani, asilo, dog sitter ed educazione cinofila in Svizzera: quando serve un'autorizzazione e dove chiederla. Con la fonte ufficiale per ogni indicazione."
            },
            "vermisst": {
                "name": "Cane smarrito o trovato",
                "kurz": "Dove segnalare un cane scappato o un cane trovato.",
                "unter": "per Cantone",
                "h1": "Cane smarrito o trovato: dove segnalarlo",
                "titel": "Cane smarrito o trovato: dove segnalarlo, Cantone per Cantone | Gassi-Kompass",
                "lede": "Dove segnalare la scomparsa del tuo cane e a chi annunciare un cane trovato. Il servizio competente cambia da Cantone a Cantone.",
                "bund_h2": "In tutta la Svizzera",
                "kt_h2": "Per Cantone",
                "kt_p": "Scegli un Cantone per i dettagli e le fonti.",
                "beschr": "Cane smarrito o trovato: dove segnalarlo in Svizzera, Cantone per Cantone. Con la fonte ufficiale per ogni indicazione."
            },
            "anmeldung": {
                "name": "Notificare il cane",
                "spalte": "Notifica",
                "kurz": "Presso quale ufficio ed entro quale termine notificare il tuo cane.",
                "sonst": "L'ufficio a cui notificare il cane e il termine variano a seconda del Cantone.",
                "beschr": "Notificare il cane in Svizzera: presso quale ufficio ed entro quale termine, Cantone per Cantone. Con la fonte ufficiale per ogni indicazione."
            }
        },
        "nf": {
            "h1": "Questa pagina non esiste",
            "lede": "Forse l'indirizzo è cambiato. Cerca il tuo luogo qui o torna alla pagina iniziale.",
            "start": "Alla pagina iniziale in italiano",
            "kurz": "Questa pagina non esiste.",
            "titel": "Pagina non trovata | Gassi-Kompass"
        },
        "ueber": {
            "h1": "Informazioni su Gassi-Kompass",
            "lede": "Gassi-Kompass raccoglie in un unico posto le regole per i cani in Svizzera: per Cantone e per Comune, con la fonte ufficiale per ogni indicazione.",
            "teile": [
                ("Da dove vengono le indicazioni", "Tutte le indicazioni provengono da fonti ufficiali: informazioni della Confederazione, leggi e ordinanze dei Cantoni, promemoria dei servizi veterinari, siti e dati aperti dei Comuni. Se una decisione politica è documentata solo dai media, la fonte lo indica."),
                ("In quale lingua", "Ogni pagina è redatta a partire dalle fonti ufficiali in una lingua ufficiale del luogo. Nelle altre lingue la pagina è una traduzione. È indicato in cima alla pagina, con un link alla versione originale. I nomi delle fonti restano nella lingua d'origine. Anche le traduzioni sono realizzate in modo automatizzato con il supporto dell'IA, e ogni cifra viene confrontata con la versione originale."),
                ("Come funziona la ricerca", "La ricerca conosce tutti i Comuni, le località e i numeri postali di avviamento della Svizzera e li attribuisce al Cantone. Ti mostra la pagina più precisa che esiste già per il tuo luogo: il Comune, altrimenti il Cantone, altrimenti le regole federali. Si basa sull'{swisstopo}Elenco ufficiale delle località</a>. Fonte: Ufficio federale di topografia swisstopo."),
                ("Come si verifica", "Le indicazioni sono raccolte in modo automatizzato con il supporto dell'IA e confrontate regolarmente con le fonti. Su ogni pagina trovi la data dell'ultima verifica. Un Comune riceve una pagina propria solo se almeno tre indicazioni locali sono attestate da una fonte ufficiale."),
                ("Segnalare un errore", "Un'indicazione non è più corretta o manca qualcosa? Scrivi a {mail}. Indica il luogo e, se l'hai, la fonte ufficiale."),
                ("Cosa non è questo sito", "Gassi-Kompass non è una consulenza legale né un'offerta di un Cantone o di un Comune. Fanno stato la legge, l'ordinanza e la segnaletica sul posto. Le regole possono cambiare e gli errori sono possibili. In caso di dubbio vale la fonte indicata."),
            ],
            "schluss": "Gassi-Kompass è un progetto privato dalla Svizzera.",
            "titel": "Informazioni su Gassi-Kompass: fonti e verifica",
            "beschr": "Da dove vengono le indicazioni di Gassi-Kompass, come sono verificate e cosa non è questo sito.",
        },
    },
}

# Karte der Hundezonen (seit 27. November 2026): Flächen aus einem amtlichen Geodatensatz, eine Datei je Gemeinde
# unter data/geo/<kt>-<gemeinde>.json. Sie entsteht mit tools/hundezonen.py. ZONEN_ART sagt, was die Zonennummern
# des Datensatzes bedeuten (Stadt Zürich: 1 Hundeverbot, 3 Leinenpflicht, 7 Freilaufzone, 8 Leinenpflicht 10 bis 22 Uhr,
# 9 Leinenpflicht 1. April bis 30. September, 12 beides zusammen). Die Texte der Seite gehören zur Tabelle TEXTE.
ZONEN_ART = {7: "frei", 3: "leine", 8: "leine", 9: "leine", 12: "leine", 1: "verbot"}
GEO = {}  # {"zh-zuerich": Daten der Datei}, gesetzt in main()

TEXTE["de"]["karte"] = {
    "pfad": "Karte",
    "h1": "Karte der Hundezonen {in_ort}",
    "titel": "Karte der Hundezonen {in_ort}: Freilaufzonen, Leinenpflicht, Hundeverbot | Gassi-Kompass",
    "beschr": "Wo Hunde {in_ort} frei laufen dürfen, wo Leinenpflicht gilt und wo sie keinen Zutritt haben: {n} Flächen aus dem amtlichen Datensatz auf der Karte, auf Wunsch mit deinem Standort.",
    "lede": "Wo dein Hund frei laufen darf, wo er an die Leine muss und wo er keinen Zutritt hat. Die Karte zeigt die {n} Flächen aus dem Datensatz der Stadt, Stand {stand}.",
    "h2": "Hundezonen auf der Karte",
    "wahl": "Auf der Karte zeigen",
    "anzahl": {"frei": "{n} Freilaufzonen", "leine": "{n} Flächen mit Leinenpflicht", "verbot": "{n} Flächen mit Hundeverbot"},
    "einwilligung": "Die Karte lädt Kartenbilder vom Bundesamt für Landestopografie swisstopo. Dessen Server erfährt dabei deine IP-Adresse. Bis du die Karte lädst, ruft diese Seite nichts von fremden Servern ab.",
    "laden": "Karte laden",
    "ohne_js": "Die Karte braucht JavaScript. Die Freilaufzonen und die Orte mit Leinenpflicht stehen als Liste auf der Seite «{seite}».",
    "standort_hinweis": "Dein Standort bleibt in deinem Browser. Die Seite speichert und sendet ihn nicht.",
    "nachweis": "Kartenbild: © swisstopo. Hundezonen: Datensatz der Stadt, Stand {stand}.",
    "h2_frei": "Freilaufzonen {in_ort}",
    "frei_p": "Tippe auf einen Namen, und die Karte zeigt die Zone.",
    "h2_lesen": "So liest du die Karte",
    "h3_farben": "Farben und Linien",
    "farben": [("frei", "Grün: Freilaufzone. Hunde dürfen hier frei laufen."),
               ("leine", "Rost mit durchgezogener Linie: Leinenpflicht das ganze Jahr."),
               ("zeit", "Rost mit gestrichelter Linie: Leinenpflicht zu bestimmten Zeiten. Welche, steht beim Antippen."),
               ("verbot", "Dunkel: Hundeverbot. Hunde haben hier keinen Zutritt.")],
    "h3_grenzen": "Was die Karte nicht zeigt",
    "grenzen": ["Die Leinenpflicht im Wald und die übrigen Regeln des Kantons. Sie gelten zusätzlich.",
                "Verfügungen, die neuer sind als der Datensatz (Stand {stand}).",
                "Den genauen Verlauf: Die Umrisse sind auf rund 1 Meter vereinfacht. Vor Ort gelten die Tafeln an den Zugängen."],
    "zurueck": "Alle Hunderegeln {in_ort}",
    "link": "Karte der Hundezonen {in_ort}",
    "js": {
        "blatt": "Karte der Hundezonen",
        "laedt": "Die Karte wird geladen.",
        "fehler": "Die Karte liess sich nicht laden. Versuch es später noch einmal.",
        "bereit": "Tippe auf eine Fläche, um Name und Regel zu sehen.",
        "standort": "Meinen Standort zeigen", "standort_aus": "Standort ausblenden",
        "standort_da": "Dein Standort ist eingezeichnet.",
        "standort_aussen": "Dein Standort liegt ausserhalb der Karte.",
        "standort_fehlt": "Der Standort ist nicht freigegeben oder nicht verfügbar.",
        "schliessen": "Schliessen", "bemerkung": "Bemerkung der Stadt",
        "zone": {"7": "Freilaufzone: Hunde dürfen hier frei laufen.",
                 "3": "Leinenpflicht das ganze Jahr.",
                 "8": "Leinenpflicht das ganze Jahr von 10 bis 22 Uhr.",
                 "9": "Leinenpflicht vom 1. April bis 30. September.",
                 "12": "Leinenpflicht vom 1. April bis 30. September von 10 bis 22 Uhr.",
                 "1": "Hundeverbot: Hunde haben hier keinen Zutritt."},
    },
}
TEXTE["fr"]["karte"] = {
    "pfad": "Carte",
    "h1": "Carte des zones pour chiens {in_ort}",
    "titel": "Carte des zones pour chiens {in_ort} : espaces de liberté, laisse obligatoire, chiens interdits | Gassi-Kompass",
    "beschr": "Où les chiens peuvent courir librement {in_ort}, où la laisse est obligatoire et où ils n'ont pas accès : {n} surfaces du jeu de données officiel sur la carte, avec votre position si vous le souhaitez.",
    "lede": "Où votre chien peut courir librement, où il doit être tenu en laisse et où il n'a pas accès. La carte montre les {n} surfaces du jeu de données de la Ville, état au {stand}.",
    "h2": "Les zones pour chiens sur la carte",
    "wahl": "Afficher sur la carte",
    "anzahl": {"frei": "{n} espaces de liberté", "leine": "{n} surfaces avec laisse obligatoire", "verbot": "{n} surfaces interdites aux chiens"},
    "einwilligung": "La carte charge des images de carte de l'Office fédéral de topographie swisstopo. Son serveur apprend alors votre adresse IP. Tant que vous ne chargez pas la carte, cette page ne demande rien à des serveurs tiers.",
    "laden": "Charger la carte",
    "ohne_js": "La carte a besoin de JavaScript. Les espaces de liberté et les lieux avec laisse obligatoire figurent en liste sur la page «{seite}».",
    "standort_hinweis": "Votre position reste dans votre navigateur. Le site ne l'enregistre pas et ne l'envoie pas.",
    "nachweis": "Image de carte : © swisstopo. Zones pour chiens : jeu de données de la Ville, état au {stand}.",
    "h2_frei": "Espaces de liberté pour chiens {in_ort}",
    "frei_p": "Touchez un nom, et la carte montre la zone.",
    "h2_lesen": "Comment lire la carte",
    "h3_farben": "Couleurs et lignes",
    "farben": [("frei", "Vert : espace de liberté. Les chiens peuvent y courir librement."),
               ("leine", "Rouille avec ligne continue : laisse obligatoire toute l'année."),
               ("zeit", "Rouille avec ligne en traitillé : laisse obligatoire à certaines périodes. Lesquelles, vous le voyez en touchant la surface."),
               ("verbot", "Foncé : chiens interdits. Les chiens n'y ont pas accès.")],
    "h3_grenzen": "Ce que la carte ne montre pas",
    "grenzen": ["La laisse obligatoire en forêt et les autres règles du canton. Elles s'appliquent en plus.",
                "Les décisions plus récentes que le jeu de données (état au {stand}).",
                "Le tracé exact : les contours sont simplifiés à environ 1 mètre. Sur place, les panneaux aux accès font foi."],
    "zurueck": "Toutes les règles pour les chiens {in_ort}",
    "link": "Carte des zones pour chiens {in_ort}",
    "js": {
        "blatt": "Carte des zones pour chiens",
        "laedt": "La carte se charge.",
        "fehler": "La carte n'a pas pu être chargée. Réessayez plus tard.",
        "bereit": "Touchez une surface pour voir son nom et la règle.",
        "standort": "Afficher ma position", "standort_aus": "Masquer ma position",
        "standort_da": "Votre position est indiquée.",
        "standort_aussen": "Votre position se trouve en dehors de la carte.",
        "standort_fehlt": "La position n'est pas autorisée ou pas disponible.",
        "schliessen": "Fermer", "bemerkung": "Remarque de la Ville (en allemand)",
        "zone": {"7": "Espace de liberté : les chiens peuvent y courir librement.",
                 "3": "Laisse obligatoire toute l'année.",
                 "8": "Laisse obligatoire toute l'année de 10 h à 22 h.",
                 "9": "Laisse obligatoire du 1er avril au 30 septembre.",
                 "12": "Laisse obligatoire du 1er avril au 30 septembre de 10 h à 22 h.",
                 "1": "Chiens interdits : les chiens n'y ont pas accès."},
    },
}
TEXTE["it"]["karte"] = {
    "pfad": "Mappa",
    "h1": "Mappa delle zone per cani {in_ort}",
    "titel": "Mappa delle zone per cani {in_ort}: aree di svago, obbligo di guinzaglio, divieto per i cani | Gassi-Kompass",
    "beschr": "Dove i cani possono correre liberi {in_ort}, dove vale l'obbligo di guinzaglio e dove non hanno accesso: {n} superfici del set di dati ufficiale sulla mappa, se vuoi con la tua posizione.",
    "lede": "Dove il tuo cane può correre libero, dove va tenuto al guinzaglio e dove non ha accesso. La mappa mostra le {n} superfici del set di dati della Città, stato al {stand}.",
    "h2": "Le zone per cani sulla mappa",
    "wahl": "Mostra sulla mappa",
    "anzahl": {"frei": "{n} aree di svago", "leine": "{n} superfici con obbligo di guinzaglio", "verbot": "{n} superfici vietate ai cani"},
    "einwilligung": "La mappa carica immagini cartografiche dell'Ufficio federale di topografia swisstopo. Il suo server viene così a conoscere il tuo indirizzo IP. Finché non carichi la mappa, questa pagina non richiede nulla a server di terzi.",
    "laden": "Carica la mappa",
    "ohne_js": "La mappa ha bisogno di JavaScript. Le aree di svago e i luoghi con obbligo di guinzaglio figurano in elenco nella pagina «{seite}».",
    "standort_hinweis": "La tua posizione resta nel tuo browser. Il sito non la salva e non la invia.",
    "nachweis": "Immagine cartografica: © swisstopo. Zone per cani: set di dati della Città, stato al {stand}.",
    "h2_frei": "Aree di svago per cani {in_ort}",
    "frei_p": "Tocca un nome e la mappa mostra la zona.",
    "h2_lesen": "Come leggere la mappa",
    "h3_farben": "Colori e linee",
    "farben": [("frei", "Verde: area di svago. Qui i cani possono correre liberi."),
               ("leine", "Ruggine con linea continua: obbligo di guinzaglio tutto l'anno."),
               ("zeit", "Ruggine con linea tratteggiata: obbligo di guinzaglio in determinati periodi. Quali, lo vedi toccando la superficie."),
               ("verbot", "Scuro: divieto per i cani. Qui i cani non hanno accesso.")],
    "h3_grenzen": "Cosa la mappa non mostra",
    "grenzen": ["L'obbligo di guinzaglio nel bosco e le altre regole del Cantone. Valgono in aggiunta.",
                "Le decisioni più recenti del set di dati (stato al {stand}).",
                "Il tracciato esatto: i contorni sono semplificati a circa 1 metro. Sul posto fanno stato i cartelli agli accessi."],
    "zurueck": "Tutte le regole per i cani {in_ort}",
    "link": "Mappa delle zone per cani {in_ort}",
    "js": {
        "blatt": "Mappa delle zone per cani",
        "laedt": "La mappa si sta caricando.",
        "fehler": "Non è stato possibile caricare la mappa. Riprova più tardi.",
        "bereit": "Tocca una superficie per vedere il nome e la regola.",
        "standort": "Mostra la mia posizione", "standort_aus": "Nascondi la mia posizione",
        "standort_da": "La tua posizione è indicata.",
        "standort_aussen": "La tua posizione è fuori dalla mappa.",
        "standort_fehlt": "La posizione non è autorizzata o non è disponibile.",
        "schliessen": "Chiudi", "bemerkung": "Osservazione della Città (in tedesco)",
        "zone": {"7": "Area di svago: qui i cani possono correre liberi.",
                 "3": "Obbligo di guinzaglio tutto l'anno.",
                 "8": "Obbligo di guinzaglio tutto l'anno dalle 10 alle 22.",
                 "9": "Obbligo di guinzaglio dal 1° aprile al 30 settembre.",
                 "12": "Obbligo di guinzaglio dal 1° aprile al 30 settembre dalle 10 alle 22.",
                 "1": "Divieto per i cani: qui i cani non hanno accesso."},
    },
}

ZAHLEN = {}       # Umfang der Seite für die Startseite, gesetzt in main(): {"quellen": Zahl der verlinkten Quellen}
LANG = "de"       # Sprache der Seite, die gerade entsteht. Wird mit sprache() gesetzt.
S = TEXTE["de"]   # Texte dieser Sprache
W = {}            # Daten je Sprache: {"de": {"k": [Kantone], "g": [Gemeinden]}, ...}
ZITIERT = {}      # {Sprache: {Quelle: [(Adresse, Name der Seite), ...]}}, gefüllt von seite(), gelesen von seite_quellen()


def sprache(lang):
    global LANG, S
    LANG, S = lang, TEXTE[lang]


# ---------------------------------------------------------------- Daten laden

def lies(pfad):
    daten = json.loads(pfad.read_text("utf-8"))
    daten["_datei"] = str(pfad.relative_to(ROOT))
    return daten


def heute():
    """Heutiges Datum in der Schweiz. Die Läufe rechnen in UTC und lehnten sonst
    zwischen Mitternacht und 01:00 Uhr das neue Datum als Zukunft ab."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Zurich")).date()
    except Exception:
        return date.today()


LADEFEHLER = []


def datenordner(lang):
    return DATA if lang == "de" else DATA / PRAEFIX[lang].strip("/")


def pruefsumme(d):
    """Prüfsumme über den Inhalt einer Datei, ohne das Prüfdatum. Eine Übersetzung trägt im Feld
    'original' die Prüfsumme ihrer Originalfassung. Ändert sich die Originalfassung, gilt die
    Übersetzung als veraltet."""
    kern = {k: v for k, v in d.items() if not k.startswith("_") and k != "geprueft"}
    text = json.dumps(kern, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def schluessel(art, d):
    """Woran man dieselbe Seite in einer anderen Sprache erkennt. art: 'k' Kanton, 'g' Gemeinde."""
    return d.get("id") if art == "k" else (d.get("kanton"), d.get("id"))


def verbinde(welt):
    """Verbindet jede Übersetzung mit ihrer Originalfassung ('_original'). Die Übersetzung übernimmt
    das Prüfdatum der Originalfassung und, bei Kantonen, die Namensformen aus kantonsformen().
    '_veraltet' ist gesetzt, wenn sich die Originalfassung seit der Übersetzung geändert hat."""
    for art in ("k", "g"):
        originale = {l: {schluessel(art, d): d for d in welt[l][art] if "uebersetzt_aus" not in d}
                     for l in SPRACHEN}
        for lang in SPRACHEN:
            for d in welt[lang][art]:
                if "uebersetzt_aus" not in d:
                    continue
                if art == "k" and d.get("id") in KANTONSNAMEN[lang]:
                    d.update(kantonsformen(lang, d["id"]))
                aus = d["uebersetzt_aus"]
                o = originale[aus].get(schluessel(art, d)) if isinstance(aus, str) and aus in originale else None
                d["_original"] = o
                if o:
                    d["geprueft"] = o.get("geprueft")
                    d["_veraltet"] = d.get("original") != pruefsumme(o)


def fehlende(welt):
    """Fehlende und veraltete Übersetzungen als Liste von
    (Stand, Art, Zielsprache, Zieldatei, Sprache der Originalfassung, Originaldatei, Prüfsumme).
    Veraltete zuerst, Kantone vor Gemeinden, grosse Kantone zuerst."""
    rang = {kid: i for i, kid in enumerate(KANTONE_GROESSE)}
    zeilen = []
    for art in ("k", "g"):
        da = {}
        for l in SPRACHEN:
            for d in welt[l][art]:
                da.setdefault(schluessel(art, d), {})[l] = d
        for key in sorted(da, key=lambda x: (rang.get(x if art == "k" else x[0], 99), str(x))):
            fassungen = da[key]
            orig = [l for l in SPRACHEN if l in fassungen and "uebersetzt_aus" not in fassungen[l]]
            if not orig:
                continue
            o = fassungen[orig[0]]
            rel = (ROOT / o["_datei"]).relative_to(datenordner(orig[0]))
            for l in SPRACHEN:
                ziel = str((datenordner(l) / rel).relative_to(ROOT))
                if l not in fassungen:
                    zeilen.append(("fehlt", art, l, ziel, orig[0], o["_datei"], pruefsumme(o)))
                elif fassungen[l].get("_veraltet"):
                    zeilen.append(("veraltet", art, l, ziel, orig[0], o["_datei"], pruefsumme(o)))
    zeilen.sort(key=lambda z: (z[0] != "veraltet", z[1] != "k"))
    return zeilen


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
    welt = {}
    for lang in SPRACHEN:
        ordner = datenordner(lang)
        kantone = [lies(p) for p in sorted((ordner / "kantone").glob("*.json"))]
        gemeinden = [lies(p) for p in sorted((ordner / "gemeinden").glob("*/*.json"))]
        welt[lang] = {"k": kantone, "g": gemeinden}
    verbinde(welt)
    for lang in SPRACHEN:  # alphabetisch nach dem Namen in der Sprache der Seite, ohne Akzente
        welt[lang]["k"].sort(key=lambda k: ohne_akzent(KANTONSNAMEN[lang].get(k.get("id"), str(k.get("name", "")))))
        welt[lang]["g"].sort(key=lambda g: ohne_akzent(str(g.get("ort", ""))))
    for lang in SPRACHEN:  # Regeln des Bundes: je Sprache eine Originalfassung, wenn es sie gibt
        pfad = datenordner(lang) / "schweiz.json"
        welt[lang]["b"] = lies(pfad) if pfad.is_file() else None
    orte = json.loads((DATA / "orte.json").read_text("utf-8"))
    return quellen, welt, welt["de"]["b"], orte


def lade_geo(quellen, welt, fehler):
    """Geodaten für die Karten der Hundezonen: data/geo/<kt>-<gemeinde>.json, erzeugt von tools/hundezonen.py.
    Hängt Fehler an die Liste und gibt {Name: Daten} zurück."""
    geo, ordner = {}, DATA / "geo"
    for pfad in (sorted(ordner.glob("*.json")) if ordner.is_dir() else []):
        wo = f"data/geo/{pfad.name}"
        try:
            d = json.loads(pfad.read_text("utf-8"))
        except ValueError as fehl:
            fehler.append(f"{wo}: kein gültiges JSON ({fehl})")
            continue
        if not any(f'{g["kanton"]}-{g["id"]}' == pfad.stem for l in SPRACHEN for g in welt[l]["g"]):
            fehler.append(f"{wo}: Es gibt keine Gemeinde dazu. Der Dateiname ist <kt>-<gemeinde>.json.")
        if d.get("quelle") not in quellen:
            fehler.append(f"{wo}: Quelle {d.get('quelle')!r} fehlt in den Quellendateien")
        if not d.get("stand"):
            fehler.append(f"{wo}: Stand der Daten fehlt")
        try:
            date.fromisoformat(str(d.get("abgerufen")))
        except ValueError:
            fehler.append(f"{wo}: abgerufen ist kein Datum JJJJ-MM-TT")
        zonen = d.get("zonen") or []
        if not zonen:
            fehler.append(f"{wo}: keine Flächen")
        for z in zonen:
            if z.get("z") not in ZONEN_ART or not z.get("n") or not z.get("g"):
                fehler.append(f"{wo}: Fläche ohne Namen, ohne Umriss oder mit unbekannter Zone: {str(z)[:80]}")
                break
        geo[pfad.stem] = d
    return geo


# ------------------------------------------------------------------- Prüfung

def ziffern(text):
    """Alle Zahlen eines Textes, sortiert. 20'000, 20 000 und 20000 gelten als dieselbe Zahl."""
    return sorted(int(z) for z in re.findall(r"\d+", TAUSENDER.sub("", text)))


def pruefe_uebersetzung(d, art, lang, welt, fehler):
    """Eine Übersetzung muss denselben Aufbau, dieselben Quellen und in jedem Text dieselben Zahlen
    haben wie ihre Originalfassung. Eine veraltete Übersetzung (Prüfsumme stimmt nicht mehr) wird
    nicht verglichen: Sie bekommt auf der Seite den Hinweis und steht in der Liste --fehlend."""
    wo, aus = d["_datei"], d["uebersetzt_aus"]
    andere = [l for l in SPRACHEN if l != lang]
    if aus not in andere:
        fehler.append(f"{wo}: 'uebersetzt_aus' nennt die Sprache der Originalfassung ({' oder '.join(andere)})")
        return
    key = schluessel(art, d)
    originale = [l for l in SPRACHEN
                 if any(schluessel(art, x) == key and "uebersetzt_aus" not in x for x in welt[l][art])]
    o = d.get("_original")
    if not o:
        fehler.append(f"{wo}: keine Originalfassung in der Sprache '{aus}' gefunden")
        return
    if originale[0] != aus:
        fehler.append(f"{wo}: übersetzt wird aus der Originalfassung '{originale[0]}', nicht aus '{aus}'")
    if not isinstance(d.get("original"), str):
        fehler.append(f"{wo}: Feld 'original' fehlt. Die Prüfsumme nennt: python3 build.py --pruefsumme {o['_datei']}")
        return
    if d.get("_veraltet"):
        return
    ohne = {"uebersetzt_aus", "original", "geprueft"} | ({"name", "im", "des"} if art == "k" else set())

    def felder(x):
        return {k for k in x if not k.startswith("_") and k not in ohne}

    def gleich_wie(a, pfad):
        fehler.append(f"{wo}, {pfad}: muss gleich sein wie in der Originalfassung: {json.dumps(a, ensure_ascii=False)}")

    def vergleiche(a, b, pfad):
        if isinstance(a, dict) and isinstance(b, dict):
            fehlt, zuviel = felder(a) - felder(b), felder(b) - felder(a)
            if fehlt:
                fehler.append(f"{wo}, {pfad or 'Datei'}: Felder der Originalfassung fehlen: {', '.join(sorted(fehlt))}")
            if zuviel:
                fehler.append(f"{wo}, {pfad or 'Datei'}: Felder, die die Originalfassung nicht hat: {', '.join(sorted(zuviel))}")
            for k in sorted(felder(a) & felder(b)):
                unter = f"{pfad}.{k}" if pfad else k
                if k in GLEICH or k.endswith("quellen"):
                    if a[k] != b[k] or type(a[k]) is not type(b[k]):
                        gleich_wie(a[k], unter)
                else:
                    vergleiche(a[k], b[k], unter)
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                fehler.append(f"{wo}, {pfad}: {len(b)} Einträge, die Originalfassung hat {len(a)}")
            else:
                for i, (x, y) in enumerate(zip(a, b)):
                    vergleiche(x, y, f"{pfad}[{i + 1}]")
        elif isinstance(a, str) and isinstance(b, str):
            if ziffern(a) != ziffern(b):
                fehler.append(f"{wo}, {pfad}: Zahlen weichen ab. Originalfassung {ziffern(a)}: «{a[:90]}». "
                              f"Übersetzung {ziffern(b)}: «{b[:90]}»")
            elif a.strip() and not b.strip():
                fehler.append(f"{wo}, {pfad}: Text fehlt")
            elif a == b and pfad.rsplit(".", 1)[-1] == "text" and len(a) >= 40:
                fehler.append(f"{wo}, {pfad}: Text ist nicht übersetzt")
        elif a != b or type(a) is not type(b):
            gleich_wie(a, pfad)

    vergleiche(o, d, "")


def pruefe(quellen, welt, bund, orte):
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
        if d > heute():
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
        if "uebersicht" in q and not str(q["uebersicht"]).startswith("https://"):
            # Seite, die das Dokument verlinkt. Liest nur der Änderungswächter (tools/wandel.py).
            fehler.append(f"Quelle '{key}': 'uebersicht' muss eine Adresse mit https:// sein")

    for lang in SPRACHEN:
        kantone, gemeinden = welt[lang]["k"], welt[lang]["g"]
        ordner = str(datenordner(lang).relative_to(ROOT))
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
            if k["kurz"] != kid.upper():
                fehler.append(f"{wo}: 'kurz' muss '{kid.upper()}' sein")
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
            if "ganzjaehrig" in w and (w.get("saison") or w["ganzjaehrig"] is not True):
                fehler.append(f"{wo}, wald: 'ganzjaehrig' gibt es nur als true und nur mit 'saison': false")
            if "titel" in w and (w.get("saison") or w.get("ganzjaehrig") or not str(w["titel"]).strip()):
                fehler.append(f"{wo}, wald: 'titel' gibt es nur ohne Saison und ohne 'ganzjaehrig'")
            for teil in ("leine", "verbot"):
                if not k[teil].get("punkte"):
                    fehler.append(f"{wo}, {teil}: 'punkte' fehlt")
                qs(k[teil].get("quellen"), f"{wo}, {teil}")
            for c in k["karten"]:
                karte(c, wo, True)
            if [c.get("titel") for c in k["karten"]] != KARTEN_TITEL[lang]:
                fehler.append(f"{wo}: 'karten' braucht genau diese sechs Karten in dieser Reihenfolge: "
                              + ", ".join(KARTEN_TITEL[lang]))
            for key, titel in VERGLEICH:
                if not str(k["vergleich"].get(key, "")).strip():
                    fehler.append(f"{wo}, vergleich: '{key}' ({titel}) fehlt")
            if "umzug" in k:
                if not k["umzug"].get("text"):
                    fehler.append(f"{wo}, umzug: 'text' fehlt")
                qs(k["umzug"].get("quellen"), f"{wo}, umzug")
            for feld in FELDER:
                if feld not in k:
                    continue
                v = k[feld]
                if not isinstance(v, dict) or not str(v.get("text", "")).strip():
                    fehler.append(f"{wo}, {feld}: 'text' fehlt")
                    v = {}
                if "punkte" in v and not (isinstance(v["punkte"], list) and v["punkte"]
                                          and all(isinstance(p, str) and p.strip() for p in v["punkte"])):
                    fehler.append(f"{wo}, {feld}: 'punkte' ist eine Liste mit mindestens einem Text oder fehlt ganz")
                qs(v.get("quellen"), f"{wo}, {feld}")
            if "durchsicht" in k:
                dv = k["durchsicht"]
                if not isinstance(dv, dict) or set(dv) != {"wer", "datum"}:
                    fehler.append(f"{wo}, durchsicht: genau die Schlüssel 'wer' und 'datum', zum Beispiel "
                                  '{"wer": "vom Veterinärdienst des Kantons Luzern", "datum": "2026-11-26"}')
                else:
                    if not (isinstance(dv["wer"], str) and dv["wer"].strip()):
                        fehler.append(f"{wo}, durchsicht: 'wer' fehlt oder ist leer")
                    try:
                        dd = date.fromisoformat(str(dv["datum"]))
                    except ValueError:
                        fehler.append(f"{wo}, durchsicht: 'datum' ist kein Datum im Format JJJJ-MM-TT")
                    else:
                        if dd > heute():
                            fehler.append(f"{wo}, durchsicht: 'datum' liegt in der Zukunft")

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
                fehler.append(f"{wo}: Kanton '{g['kanton']}' hat keine Datei in {ordner}/kantone/")
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
    for lang in SPRACHEN:
        for art in ("k", "g"):
            for d in welt[lang][art]:
                if "uebersetzt_aus" in d:
                    pruefe_uebersetzung(d, art, lang, welt, fehler)
    if not bund:
        fehler.append("data/schweiz.json fehlt")
    for b in (welt[lang].get("b") for lang in SPRACHEN):
        if not b:
            continue
        wo = b["_datei"]
        if "geprueft" not in b or not b.get("karten"):
            fehler.append(f"{wo}: 'geprueft' und 'karten' sind Pflicht")
        else:
            datum(b["geprueft"], wo)
            for c in b["karten"]:
                karte(c, wo, True)
            for t in THEMEN:
                if t.get("feld") and sum(1 for c in b["karten"] if c.get("id") == t["id"]) != 1:
                    fehler.append(f"{wo}: genau eine Karte braucht \"id\": \"{t['id']}\" (Themenseite /thema/{t['id']}/)")
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


# ------------------------------------------------------- Sprachen und Adressen

def k_sprachen(kid):
    """Sprachen, in denen es die Seite dieses Kantons gibt."""
    return [l for l in SPRACHEN if any(k["id"] == kid for k in W[l]["k"])]


def k_pfad(lang, kid):
    return f"{PRAEFIX[lang]}/{kid}/"


def g_pfad(lang, g):
    return f'{PRAEFIX[lang]}/{g["kanton"]}/{g["id"]}/'


def g_sprachen(bfs):
    """Adressen der Seiten dieser Gemeinde je Sprache."""
    return {l: g_pfad(l, g) for l in SPRACHEN for g in W[l]["g"] if g["bfs"] == bfs}


def karten_geo(g):
    """Geodaten zur Karte der Hundezonen dieser Gemeinde oder None."""
    return GEO.get(f'{g["kanton"]}-{g["id"]}')


def karte_pfad(lang, g):
    return g_pfad(lang, g) + "karte/"


def k_ziel(kid):
    """Beste Fassung des Kantons für die Sprache der Seite: (Sprache, Adresse) oder None."""
    da = k_sprachen(kid)
    if not da:
        return None
    lang = LANG if LANG in da else da[0]
    return lang, k_pfad(lang, kid)


def bund_ziel():
    """Seite mit den Regeln des Bundes für die Sprache der Seite: (Sprache, Adresse)."""
    lang = LANG if W[LANG].get("b") else "de"
    return lang, PRAEFIX[lang] + "/schweiz/"


def thema_pfad(tid):
    return f"{PRAEFIX[LANG]}/thema/{tid}/"


def in_sprache(lang):
    """Zusatz hinter einem Link, der auf eine Seite in einer anderen Sprache führt: « (französisch)»."""
    return "" if lang == LANG else f' ({S["sprache"][lang]})'


def gemeinden_von(kid):
    """Gemeinden eines Kantons mit lokalen Regeln, jede einmal: [(Sprache, Gemeinde)]. Bevorzugt die
    Fassung in der Sprache der Seite, alphabetisch nach dem Ortsnamen."""
    da = {}
    for lang in [LANG] + [l for l in SPRACHEN if l != LANG]:
        for g in W[lang]["g"]:
            if g["kanton"] == kid:
                da.setdefault(g["bfs"], (lang, g))
    return sorted(da.values(), key=lambda x: ohne_akzent(x[1]["ort"]))


def erfasste():
    """Kürzel aller Kantone, die in mindestens einer Sprache eine Seite haben."""
    return [kid for kid, _ in KANTONE_ALLE if k_sprachen(kid)]


def ohne_akzent(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


# ------------------------------------------------------------------ Bausteine

def de_datum(iso):
    d = date.fromisoformat(iso)
    return f"{d.day:02d}.{d.month:02d}.{d.year}"


def tag_monat(mmtt, lang="de"):
    m, t = (int(x) for x in mmtt.split("-"))
    monat = TEXTE[lang]["monate"][m - 1]
    if lang == "de":
        return f"{t}. {monat}"
    erster = TEXTE[lang]["heute"]["erster"]
    return f"{erster if t == 1 else t} {monat}"


def daten_wald(w):
    """Platzhalter für die Texte zur Leinenzeit. Italienisch braucht «dal» und «al» mit Apostroph vor 8 und 11."""
    def it(vor, mmtt):
        return (vor + "l'" if int(mmtt.split("-")[1]) in (8, 11) else vor + " ") + tag_monat(mmtt, "it")
    return {"von": tag_monat(w["von"], LANG), "bis": tag_monat(w["bis"], LANG), "wo": w["wo"],
            "dal_von": it("dal", w["von"]), "al_bis": it("al", w["bis"])}


def tag_im_jahr(mmtt):
    m, t = (int(x) for x in mmtt.split("-"))
    return sum(TAGE[:m - 1]) + t - 1


def qlinks(keys, Q, benutzt):
    for key in keys:
        if key not in benutzt:
            benutzt.append(key)
    wort = S["quellen"] if len(keys) > 1 else S["quelle"]
    links = "".join(f'<a href="{e(Q[k]["url"])}" target="_blank" rel="noopener">{e(Q[k]["kurz"])}</a>'
                    for k in keys)
    return f'<div class="src"><span>{wort}</span>{links}</div>'


def karte(c, Q, benutzt, link=None, anker=None):
    """link: Adresse, auf die der Kartentitel führt (Themenseiten: zur Kantonsseite).
    anker: feste id der Karte (nur Kantonsseite, KARTEN_ANKER)."""
    kopf = f'<a href="{link}">{e(c["titel"])}</a>' if link else e(c["titel"])
    marke = f'<span class="chip {e(c["ton"])}">{e(c["marke"])}</span>' if c.get("marke") else ""
    mehr = ""
    if c.get("mehr"):
        liste = c["mehr"]["punkte"]
        punkte = "".join(f"<li>{e(p)}</li>" for p in liste)
        # Kurze Einträge wie Rassen stehen in zwei Spalten, ganze Sätze in einer (Median über 50 Zeichen).
        saetze = ' class="saetze"' if sorted(len(p) for p in liste)[len(liste) // 2] > 50 else ""
        mehr = (f'<details class="more"><summary>{e(c["mehr"]["titel"])}</summary>'
                f'<ul{saetze}>{punkte}</ul></details>')
    kennung = f' id="{anker}"' if anker else ""
    return (f'<article class="card"{kennung}><div class="card-top"><h3 class="card-k">{kopf}</h3>{marke}</div>'
            f'<p class="card-v">{e(c["wert"])}</p><p>{e(c["text"])}</p>{mehr}'
            f'{qlinks(c["quellen"], Q, benutzt)}</article>')


def wald(k, Q, benutzt, hinweis=None, anker=False, kurz=False):
    """anker: Der Kasten bekommt id="wald" (nur Kantonsseite, Ziel im Abschnitt «Neu einen Hund»).
    kurz: Gemeindeseite. Ohne feste Leinenzeit steht ein langer Text des Kantons zum Aufklappen."""
    w = k["wald"]
    spalten = " ".join(f"{t}fr" for t in TAGE)
    zellen = '<span class="m"></span>' * 12
    monate = "".join(f"<span>{m}</span>" for m in S["mon3"])
    # Texte für assets/heute.js: Datum, Markierung «heute» und der Tagesstatus in der Sprache der Seite
    js = {key: S["heute"][key] for key in ("heute", "datum", "punkt", "erster")}
    js["mon"], js["wt"] = S["monate"], S["wochentage"]
    klasse = ""
    if w.get("saison"):
        d = daten_wald(w)
        links = tag_im_jahr(w["von"]) / 365 * 100
        breite = (tag_im_jahr(w["bis"]) + 1 - tag_im_jahr(w["von"])) / 365 * 100
        band = f'<div class="band" style="left:{links:.2f}%;width:{breite:.2f}%"><span>{S["wald_band"]}</span></div>'
        attrs = f' data-saison="1" data-von="{w["von"]}" data-bis="{w["bis"]}" data-wo="{e(w["wo"])}"'
        gross = S["wald_gross"].format(**d)
        text = S["wald_text"].format(**d)
        unter = S["wald_unter"].format(**d)
        aria = S["wald_aria"].format(**d)
        for key in ("tage", "tagen", "in_gross", "letzter", "noch", "aus_gross"):
            js[key] = S["heute"][key]
        js["in_text"] = S["heute"]["in_text"].format(**d)
        js["aus_text"] = S["heute"]["aus_text"].format(**d)
    elif w.get("ganzjaehrig"):  # Leinenpflicht im Wald das ganze Jahr: der Balken ist ganz markiert
        band = f'<div class="band" style="left:0;width:100%"><span>{S["wald_band"]}</span></div>'
        attrs, klasse = ' data-saison="0"', " must"
        gross, text = S["wald_immer_gross"], w["text"]
        unter, aria = S["wald_immer_unter"], S["wald_immer_aria"]
    else:
        band, attrs = "", ' data-saison="0"'
        gross, text = w.get("titel") or S["wald_ohne_gross"], w["text"]
        unter = S["wald_ohne_unter"].format(im=k["im"])
        aria = S["wald_ohne_aria"]
    attrs += f' data-texte="{e(json.dumps(js, ensure_ascii=False, separators=(",", ":")))}"'
    note = f'<p class="today-note">{e(hinweis)}</p>' if hinweis else ""
    kennung = ' id="wald"' if anker else ""
    absatz = f'<p data-heute-text>{e(text)}</p>'
    if kurz and not w.get("saison") and len(text) > WALD_KURZ:
        absatz = (f'<details class="more wald-mehr"><summary>{e(S["blick_wald"].format(im=k["im"]))}</summary>'
                  f'{absatz}</details>')
    return (f'<section class="today"{kennung} data-wald{attrs}>'
            f'<div class="today-head"><span class="eyebrow">{S["wald_kopf"]} · {e(k["name"])}</span>'
            '<span class="today-date" data-heute-datum></span></div>'
            '<div class="today-body"><div class="today-status">'
            f'<p class="big{klasse}" data-heute-gross>{e(gross)}</p>{absatz}{note}'
            f'{qlinks(w["quellen"], Q, benutzt)}</div>'
            f'<div class="bar" role="img" aria-label="{e(aria)}">'
            f'<div class="track" style="grid-template-columns:{spalten}">{zellen}{band}</div>'
            f'<div class="months" style="grid-template-columns:{spalten}" aria-hidden="true">{monate}</div>'
            f'<p class="bar-cap">{e(unter)}</p></div></div></section>')


def regeln(k, Q, benutzt):
    def li(punkte):
        return "".join(f"<li>{e(p)}</li>" for p in punkte)
    lead = f'<p>{e(k["verbot"]["einleitung"])}</p>' if k["verbot"].get("einleitung") else ""
    return (f'<section class="sec" id="leine"><div class="sec-head">'
            f'<h2>{S["regeln_h2"]} {e(k["im"])}</h2></div><div class="split">'
            f'<div class="list-card leash"><h3><span class="chip must">{S["leine_chip"]}</span>{S["leine_h3"]}</h3>'
            f'<ul>{li(k["leine"]["punkte"])}</ul>{qlinks(k["leine"]["quellen"], Q, benutzt)}</div>'
            f'<div class="list-card"><h3><span class="chip none">{S["verbot_chip"]}</span>{S["verbot_h3"]}</h3>'
            f'{lead}<ul>{li(k["verbot"]["punkte"])}</ul>{qlinks(k["verbot"]["quellen"], Q, benutzt)}</div>'
            '</div></section>')


def kurz_zeilen(k, ziel=""):
    """Die sechs Karten eines Kantons als Zeilen für blick(): Titel, Marke und Kurztext aus 'vergleich'.
    ziel: Adresse der Kantonsseite vor dem Anker (Gemeindeseite), leer auf der Kantonsseite selbst."""
    zeilen = []
    for i, c in enumerate(k["karten"]):
        marke = f'<span class="chip {e(c["ton"])}">{e(c["marke"])}</span>' if c.get("marke") else ""
        key = VERGLEICH_POS[i]
        zeilen.append((f"{ziel}#{KARTEN_ANKER[i]}", c["titel"], marke, k["vergleich"][key] if key else c["wert"]))
    return zeilen


def pflichten(k, Q, benutzt):
    """Kantonsseite: zuerst die Übersicht (sechs Zeilen mit Link auf die Karte), dann die Karten mit Ankern."""
    karten = "".join(karte(c, Q, benutzt, anker=KARTEN_ANKER[i]) for i, c in enumerate(k["karten"]))
    umzug = ""
    if k.get("umzug"):  # callout-k: Überschrift für das Verzeichnis der Suche (SuchLeser), ohne eigene Darstellung
        umzug = (f'<div class="callout" id="umzug"><p><strong class="callout-k">'
                 f'{e(S["umzug"].format(name=k["name"], im=k["im"]))}</strong> '
                 f'{e(k["umzug"]["text"])}</p>{qlinks(k["umzug"]["quellen"], Q, benutzt)}</div>')
    titel = f'{S["pflichten_h2"]} {k["im"]}'
    return (f'<section class="sec" id="pflichten"><div class="sec-head">'
            f'<h2>{e(titel)}</h2></div>{blick(kurz_zeilen(k), titel, marken=True)}'
            f'<div class="cards">{karten}</div>{umzug}</section>')


def sprungleiste(ziele):
    """Leiste «Auf dieser Seite»: beim Bund nach der Einleitung, beim Kanton nach der Tafel «Leine im Wald»,
    damit deren Status am Telefon im ersten Bildschirm bleibt. ziele: Schlüssel aus S["sprung"],
    zugleich die id des Abschnitts, in der Reihenfolge der Seite."""
    sp = S["sprung"]
    links = "".join(f'<a href="#{z}">{e(sp[z])}</a>' for z in ziele)
    return (f'<nav class="sprung" aria-label="{e(sp["label"])}"><span class="sprung-k" aria-hidden="true">'
            f'{e(sp["label"])}</span>{links}</nav>')


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
        zonen = (f'<h3 class="sub" id="freilauf">{S["freilauf"]}</h3><div class="zones">{"".join(teile)}</div>'
                 f'{qlinks(g["freilaufzonen_quellen"], Q, benutzt)}')
    zur_karte = ""
    if karten_geo(g):
        zur_karte = (f'<p><a class="text-link" href="{karte_pfad(LANG, g)}">'
                     f'{e(S["karte"]["link"].format(in_ort=g["in_ort"]))}</a></p>')
    karten = "".join(karte(c, Q, benutzt, anker=f"lokal-{i + 1}") for i, c in enumerate(g["karten"]))
    return (f'<section class="sec" data-lokal><div class="sec-head">'
            f'<h2>{e(S["lokal_h2"].format(in_ort=g["in_ort"]))}</h2>{intro}</div>{zonen}{zur_karte}'
            f'<div class="cards">{karten}</div></section>')


def blick(zeilen, label, marken=False):
    """Linienliste «Auf einen Blick»: je Zeile ein Link mit Titel, wahlweise eine Marke, dazu ein Kurztext.
    zeilen: (href, titel, marke_html, text). marken: Spalte für Marken (Kanton kurz auf der Gemeindeseite)."""
    li = "".join(f'<li class="blick-z"><a class="blick-k" href="{e(h)}">{e(t)}</a>{m}'
                 f'<span class="blick-t">{e(x)}</span></li>' for h, t, m, x in zeilen)
    klasse = "blick mit-marke" if marken else "blick"
    return f'<ul class="{klasse}" role="list" aria-label="{e(label)}" data-blick>{li}</ul>'


def blick_gemeinde(g):
    """Gemeindeseite: eine Zeile je lokaler Karte, dazu eine für die Freilaufzonen."""
    zeilen = [(f"#lokal-{i + 1}", c["titel"], "", c["wert"]) for i, c in enumerate(g["karten"])]
    if g.get("freilaufzonen"):
        zeilen.append(("#freilauf", S["freilauf"], "", str(len(g["freilaufzonen"]))))
    return blick(zeilen, S["lokal_h2"].format(in_ort=g["in_ort"]))


def pflichten_kurz(k, Q, benutzt):
    """Gemeindeseite: die sechs Karten des Kantons als Kurzzeilen mit Link auf die Kantonsseite,
    darunter alle Karten und der Kasten zum Umzug unverändert zum Aufklappen."""
    zeilen = kurz_zeilen(k, k_pfad(LANG, k["id"]))
    karten = "".join(karte(c, Q, benutzt) for c in k["karten"])
    umzug = ""
    if k.get("umzug"):
        umzug = (f'<div class="callout"><p><strong>{e(S["umzug"].format(name=k["name"], im=k["im"]))}</strong> '
                 f'{e(k["umzug"]["text"])}</p>{qlinks(k["umzug"]["quellen"], Q, benutzt)}</div>')
    titel = f'{S["pflichten_h2"]} {k["im"]}'
    return (f'<section class="sec"><div class="sec-head"><h2>{e(titel)}</h2></div>'
            f'{blick(zeilen, titel, marken=True)}'
            f'<details class="more alle-karten" data-kanton-karten><summary>{e(S["kt_alle"])}</summary>'
            f'<div class="cards">{karten}</div>{umzug}</details></section>')


def hinweis_uebersetzung(d, art):
    """Hinweis unter dem Titel einer übersetzten Seite, mit Link zur Originalfassung. art: 'k' oder 'g'."""
    aus = d.get("uebersetzt_aus")
    if not aus:
        return ""
    ziel = k_pfad(aus, d["id"]) if art == "k" else g_pfad(aus, d)
    alt = f' <strong>{S["ueb_alt"]}</strong>' if d.get("_veraltet") else ""
    return (f'<p class="transl" data-uebersetzung>{S["ueb"][aus]}{alt} '
            f'<a href="{ziel}" hreflang="{HTMLLANG[aus]}">{S["ueb_link"][aus]}</a></p>')


def hinweis_durchsicht(k):
    """Hinweis, dass ein Amt die Zusammenfassung durchgesehen hat (wahlweises Feld 'durchsicht').
    Nur mit schriftlichem Einverständnis des Amts, siehe Handbuch, «Datenfelder Kanton»."""
    d = k.get("durchsicht")
    if not d:
        return ""
    j, m, t = (int(x) for x in d["datum"].split("-"))
    datum = tag_monat(f"{m:02d}-{t:02d}", LANG) + f" {j}"
    return (f'<p class="transl" data-durchsicht>'
            f'{e(S["durchsicht"].format(datum=datum, wer=d["wer"]))}</p>')


def tafel(href, name, unter="", aktiv=False, klasse="", code=""):
    """code: Kürzel des Kantons, steht im Register als Kennung vor dem Namen."""
    cur = ' aria-current="page"' if aktiv else ""
    art = f"dest {klasse}".strip()
    sub = f'<span class="dest-sub">{e(unter)}</span>' if unter else ""
    kenn = f'<span class="dest-code" aria-hidden="true">{e(code)}</span>' if code else ""
    return f'<a class="{art}" href="{href}"{cur}>{kenn}<span class="dest-name">{e(name)}</span>{sub}</a>'


def gemeinde_tafeln(kid, ohne=None):
    """Tafeln zu den Gemeinden eines Kantons mit ihrem kurzen Ortsnamen. Führt eine Tafel auf eine
    Seite in einer anderen Sprache, nennt sie die Sprache. ohne: BFS-Nummer der Gemeinde, auf deren
    Seite die Tafeln stehen."""
    return "".join(tafel(g_pfad(lang, g), g["ort"], "" if lang == LANG else S["sprache"][lang])
                   for lang, g in gemeinden_von(kid) if g["bfs"] != ohne)


def suche():
    """Suchfeld für Gemeinde, Ort, Postleitzahl oder Kanton. Ohne Skript bleibt es unsichtbar.
    Alle Texte stehen in TEXTE, assets/suche.js kennt keine Sprache."""
    attrs = "".join(f' data-{k}="{e(v)}"' for k, v in S["suche"].items())
    return (f'<div class="search" data-suche data-lang="{LANG}" data-schweiz="{bund_ziel()[1]}"{attrs} hidden>'
            f'<label for="ortssuche">{S["suche_label"]}</label>'
            '<input id="ortssuche" type="search" autocomplete="off" enterkeyhint="search" '
            f'placeholder="{S["suche_beispiel"]}" aria-describedby="such-status">'
            '<p class="search-status" id="such-status" role="status"></p>'
            '<div class="plates" id="treffer"></div>'
            f'<div class="such-seiten" id="seitentreffer" hidden><p class="such-h" id="seiten-h">{S["suche"]["seiten_h"]}</p>'
            '<div class="topics" role="list" aria-labelledby="seiten-h"></div></div></div>'
            f'<noscript><p>{S["suche_noscript"]}</p></noscript>')


# Suche auf den Seiten: gleichbedeutende Wörter je Sprache, normiert wie such_norm() (klein, ohne Akzente).
# Tippt jemand ein Wort der Gruppe (auch mit anderer Endung, siehe nah() in assets/suche.js, oder mindestens fünf
# Buchstaben seines Anfangs), sucht die Suche jedes Wort der Gruppe. Die Gruppe darf Wörter enthalten, die auf keiner
# Seite stehen: Sie sind das, was Leute tippen («kampfhund», «hundeschule»), und führen zu den Wörtern der Seiten.
# Ein Wort mit «=» löst die Gruppe nur aus und wird selbst nicht gesucht, weil es als Wortanfang zu viel
# Fremdes träfe («=perso» träfe «persona»). Mindestens ein Wort jeder Gruppe muss auf den Seiten stehen,
# sonst lässt build.py die Gruppe weg und nennt sie.
SYNONYME = {
    "de": [["hundesteuer", "hundetaxe", "hundeabgabe", "hundegebuhr", "steuer", "taxe", "hundemarke", "kontrollmarke",
            "=kostet", "=kosten", "=preis", "=teuer"],
           ["leine", "leinenpflicht", "leinenzwang", "leinengebot", "anleinen", "angeleint", "anleinpflicht"],
           ["maulkorb", "maulkorbpflicht", "maulkorbzwang", "beisskorb"],
           ["kot", "hundekot", "hundehaufen", "haufchen", "kotbeutel", "kotsack", "robidog"],
           ["rasse", "rasseliste", "rassenliste", "rassetypenliste", "listenhund", "kampfhund", "hunderasse", "rasseverbot"],
           ["pitbull", "pit"],
           ["haftpflicht", "haftpflichtversicherung", "hundehaftpflicht", "versicherung", "versichern",
            "hundeversicherung"],
           ["kurs", "hundekurs", "kurspflicht", "sachkundenachweis", "skn", "hundeschule", "welpenkurs",
            "erziehungskurs", "hundehalterkurs", "brevet"],
           ["anmeldung", "anmelden", "registrieren", "registrierung", "amicus", "mikrochip", "chip", "chippen",
            "abmelden", "ummelden"],
           ["vermisst", "entlaufen", "weggelaufen", "verloren", "zugelaufen", "fundtier", "findeltier", "fundhund",
            "tiermeldezentrale", "stmz"],
           # Thema «Hunde als Beruf», zwei Gruppen: Betreuen und Züchten. «beruf» steht im Titel der Themenseite und
           # bringt sie nach oben. Nicht in die Gruppe: «bewilligung», «betreuung», «tierheim». Sie stehen auch bei
           # Rassen und bei vermissten Hunden, «Hundepension» fände sonst zuerst die Rasselisten.
           ["hundepension", "tierpension", "pension", "hundetagesstatte", "tagesstatte", "hundehort", "hundesitter",
            "hundesitting", "petsitting", "tiersitter", "hundebetreuung", "betreuungsdienst", "dogwalker", "dogsitter",
            "spazierdienst", "laufdienst", "gewerbsmassig", "beruf", "=sitter", "=sitting", "=walker", "=dog"],
           ["hundezucht", "zucht", "zuchter", "zuchten", "beruf"],
           ["brutzeit", "setzzeit", "schonzeit", "wald"],
           ["freilauf", "freilaufzone", "hundezone", "hundewiese", "hundepark", "hundeauslauf", "auslauf",
            "hundefreilauf", "freilaufflache"],
           ["busse", "ordnungsbusse", "strafe", "bussgeld"],
           ["umzug", "umziehen", "zuzug", "zuziehen", "wegzug", "zugezogen"]],
    "fr": [["impot", "taxe", "medaille", "marque", "vignette", "=coute", "=cout", "=prix", "=combien"],
           ["laisse", "attache", "attacher"],
           ["museliere", "museler", "muselee"],
           ["crotte", "dejections", "excrements", "caca", "ramasser", "sachet", "souillures"],
           ["race", "liste", "dangereux", "dangereuse", "molosse", "combat", "pitbull"],
           ["assurance", "rc", "responsabilite"],
           ["cours", "formation", "education", "attestation", "educateur", "=ecole"],
           ["annoncer", "annonce", "inscription", "inscrire", "enregistrer", "enregistrement", "amicus", "puce",
            "identification", "declarer", "declaration"],
           ["perdu", "disparu", "egare", "errant", "fugue", "=trouve", "=retrouve"],
           ["pension", "garderie", "dogsitter", "petsitting", "promeneur", "=garde", "=gardien", "professionnel",
            "=sitter", "=sitting", "=dog", "=pet"],
           ["elevage", "eleveur", "professionnel"],
           ["foret", "lisiere", "bois"],
           ["amende", "contravention", "sanction", "penalite"],
           ["liberte", "ebats"],
           ["demenagement", "demenager", "arrivee", "emmenager"]],
    "it": [["imposta", "imposte", "tassa", "tasse", "contrassegno", "medaglietta", "=costa", "=costo", "=prezzo",
            "=quanto"],
           ["guinzaglio", "legato", "legare"],
           ["escrementi", "deiezioni", "feci", "bisogni", "cacca", "raccogliere", "sacchetto", "sacchetti"],
           ["razze", "razza", "elenco", "lista", "pericolosi", "pericoloso", "pitbull", "combattimento"],
           ["assicurazione", "assicurazioni", "rc", "responsabilita"],
           ["corso", "corsi", "formazione", "educazione", "attestato", "=scuola"],
           ["notifica", "notificare", "registrazione", "registrare", "annunciare", "annuncio", "iscrizione",
            "amicus", "microchip", "chip"],
           ["smarrito", "scomparso", "fuggito", "scappato", "=perso", "=trovato", "=ritrovato"],
           ["pensione", "asilo", "dogsitter", "petsitter", "accudimento", "=custodia", "profession", "=sitter",
            "=sitting", "=dog", "=pet"],
           ["allevamento", "allevatore", "profession"],
           ["bosco", "boschi", "foresta"],
           ["multa", "multe", "contravvenzione", "sanzione"],
           ["svago", "sgambamento", "sgambatura", "liberta"],
           ["trasloco", "traslocare", "trasferimento", "arrivo"]],
}
# Wörter, die in einer Frage nichts eingrenzen: das Wort für Hund (jede Seite handelt von Hunden) und
# Funktionswörter. Die Suche auf den Seiten lässt sie weg, solange ein anderes Wort übrig bleibt: Aus «Wo darf
# mein Hund frei laufen» wird «frei laufen», aus «cani smarriti» wird «smarriti». Normiert wie such_norm().
# Keine Kürzel von Kantonen und keine Namen von Orten: Die Ortssuche bekommt immer die ganze Eingabe.
STOPPWOERTER = {
    "de": ["hund", "hunde", "hunden", "hundes", "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen",
           "einem", "einer", "mein", "meine", "meinen", "meinem", "und", "oder", "in", "im", "an", "am", "auf", "mit",
           "fur", "bei", "von", "vom", "zu", "zum", "zur", "ist", "sind", "wo", "wie", "was", "wann", "darf", "muss",
           "kann", "ich", "man", "es", "gibt", "gilt", "gelten"],
    "fr": ["chien", "chiens", "mon", "ma", "mes", "le", "la", "les", "un", "une", "des", "du", "de", "d", "l", "en",
           "au", "aux", "a", "et", "ou", "pour", "dans", "sur", "avec", "est", "que", "quoi", "comment", "je", "on",
           "peut", "puis", "quel", "quelle", "quelles", "quels", "faut", "il"],
    "it": ["cane", "cani", "il", "lo", "la", "i", "gli", "le", "un", "uno", "una", "di", "del", "della", "dei",
           "delle", "a", "al", "alla", "da", "in", "nel", "nella", "con", "su", "per", "e", "o", "mio", "mia", "che",
           "come", "dove", "posso", "si", "puo", "devo", "quando"],
}
# Zeichen Text je Abschnitt im Verzeichnis der Suche. Der längste Abschnitt hat rund 2300 Zeichen: Die Grenze
# schneidet heute nichts ab, damit die Suche jedes Wort der Seite findet und auf den Themenseiten richtig zählt,
# bei wie vielen Kantonen es steht. Bis 28. November 2026 waren es 450 Zeichen, «Rottweiler» stand so bei 3 statt
# bei 12 Kantonen.
SUCH_TEXT = 4000
SUCH_ARTEN = ("kanton", "gemeinde", "thema", "bund", "ueber")


def such_norm(text):
    """Wie assets/suche.js: klein, ohne Akzente, alles ausser Buchstaben und Ziffern als Leerzeichen."""
    t = unicodedata.normalize("NFD", text.lower())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in t if not unicodedata.combining(c))).strip()


class SuchLeser(html.parser.HTMLParser):
    """Liest aus einer erzeugten Seite die Abschnitte für das Verzeichnis der Suche: je Überschrift
    (h1 bis h3, Name einer Kantonszeile, Status der Tafel «Leine im Wald», Name einer Freilaufzone) den Text bis
    zur nächsten Überschrift und die id des nächsten Elements, das eine trägt. Übergangen werden Skripte,
    Navigation, Quellenzeilen, Jahresbalken, Tafeln und die Listen «Auf einen Blick», weil sie nur wiederholen
    oder auf andere Seiten zeigen."""
    LEER = {"br", "img", "input", "meta", "link", "hr", "source", "wbr"}
    WEG_TAGS = {"script", "style", "nav", "noscript", "svg", "button", "template"}
    WEG_KLASSEN = {"src", "bar", "today-head", "kt-kopf", "blick", "plates", "facts", "transl", "months", "index", "schritte",
                   "text-link", "q-wahl", "q-liste"}
    KOPF_KLASSEN = {"kt-name", "big", "zone-name", "callout-k"}
    TRENN_KLASSEN = {"card-v", "kt-wert", "kt-kurz", "chip"}  # nach diesen Elementen steht im Text ein Mittelpunkt

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stapel, self.weg, self.kopf, self.zonen = [], 0, None, False
        self.bloecke = []  # [Überschrift, id, Text]

    def handle_starttag(self, tag, attrs):
        if tag in self.LEER:
            return
        a = dict(attrs)
        klassen = set((a.get("class") or "").split())
        weg = tag in self.WEG_TAGS or bool(klassen & self.WEG_KLASSEN) or "data-blick" in a
        kopf = self.weg == 0 and (tag in ("h1", "h2", "h3") or bool(klassen & self.KOPF_KLASSEN))
        self.stapel.append((tag, a.get("id"), weg, bool(klassen & self.TRENN_KLASSEN)))
        self.zonen = self.zonen or a.get("id") == "freilauf"
        if weg:
            self.weg += 1
        elif kopf and self.kopf is None:
            ziel = next((i for _, i, _, _ in reversed(self.stapel) if i and i != "inhalt"), "")
            if not ziel and self.zonen and "zone-name" in klassen:
                ziel = "freilauf"  # eine Freilaufzone hat keinen eigenen Anker: zur Überschrift der Zonen
            self.bloecke.append(["", ziel, ""])
            self.kopf = len(self.stapel)
        self.handle_data(" ")

    def handle_endtag(self, tag):
        if tag in self.LEER:
            return
        while self.stapel:
            t, _, weg, trenn = self.stapel.pop()
            if weg:
                self.weg -= 1
            if trenn:
                self.handle_data(" · ")
            if self.kopf is not None and len(self.stapel) < self.kopf:
                self.kopf = None
            if t == tag:
                break
        self.handle_data(" ")

    def handle_data(self, data):
        if self.weg or not self.bloecke:
            return
        self.bloecke[-1][0 if self.kopf is not None else 2] += data


def such_eintrag(pfad, art, seite_html):
    """Ein Eintrag des Verzeichnisses: [Adresse, Titel, Art, [[Überschrift, id, Text], ...]].
    Auf der Gemeindeseite zählt nur, was lokal gilt (Titel und Abschnitt data-lokal): Die Regeln des
    Kantons stehen schon auf dessen Seite."""
    main = seite_html[seite_html.index("<main"):seite_html.index("</main>")]
    if art == "gemeinde":
        h1 = re.search(r"<h1>.*?</h1>", main, re.S)
        lokal = re.search(r"<section[^>]*data-lokal.*?</section>", main, re.S)
        main = (h1.group(0) if h1 else "") + (lokal.group(0) if lokal else "")
    leser = SuchLeser()
    leser.feed(main)
    leser.close()
    zusammen = lambda t: re.sub(r"\s+", " ", t).strip()
    bloecke = []
    for h, i, t in leser.bloecke:
        h, t = zusammen(h).rstrip(" :"), zusammen(t)
        if len(t) > SUCH_TEXT:
            t = t[:SUCH_TEXT].rsplit(" ", 1)[0] + " …"
        if h or t:
            bloecke.append([h, i, t])
    titel = bloecke[0][0] if bloecke else ""
    return [pfad, titel, art, bloecke]


def such_verzeichnis(lang, eintraege):
    """Inhalt von assets/suche-<sprache>.json: Seiten und gleichbedeutende Wörter. Eine Gruppe bleibt ganz,
    auch mit Wörtern, die auf keiner Seite stehen: Sie führen von dem, was Leute tippen, zu den Wörtern der
    Seiten. Steht kein Wort der Gruppe auf einer Seite dieser Sprache, fällt sie weg und wird genannt."""
    woerter = set()
    for _, titel, _, bloecke in eintraege:
        woerter.update(such_norm(titel).split())
        for h, _, t in bloecke:
            woerter.update(such_norm(h + " " + t).split())
    gruppen = []
    for gruppe in SYNONYME[lang]:
        if any(x.startswith(w) for w in gruppe if not w.startswith("=") for x in woerter):
            gruppen.append(gruppe)
        else:
            print(f"Hinweis: Suche {lang}: Kein Wort der Gruppe «{', '.join(gruppe)}» steht auf einer Seite, sie fällt weg.")
    return json.dumps({"s": eintraege, "syn": gruppen, "stop": STOPPWOERTER[lang]}, ensure_ascii=False, separators=(",", ":"))


def kantonsraster():
    """Alle 26 Kantone, alphabetisch in der Sprache der Seite. Jede Tafel nennt das Kürzel und die Zahl
    der Gemeinden mit lokalen Regeln. Gibt es die Kantonsseite in der Sprache der Seite nicht, führt
    die Tafel zur Fassung in einer anderen Sprache und nennt diese."""
    namen = KANTONSNAMEN[LANG]
    teile = []
    for kid, _ in sorted(KANTONE_ALLE, key=lambda x: ohne_akzent(namen[x[0]])):
        ziel = k_ziel(kid)
        if not ziel:  # Kanton ohne Seite: Regeln des Bundes
            teile.append(tafel(f"{bund_ziel()[1]}#kt={kid}", namen[kid], "", klasse="wait", code=kid.upper()))
            continue
        unter, n = "", len(gemeinden_von(kid))
        if ziel[0] != LANG:
            unter = S["sprache"][ziel[0]]
        elif n:
            unter = S["n_gemeinden"][n > 1].format(n=n)
        teile.append(tafel(ziel[1], namen[kid], unter, klasse="ok", code=kid.upper()))
    return f'<div class="plates small raster">{"".join(teile)}</div>'


def ortsindex(orte):
    """Kompakte Liste für die Suche im Browser (assets/orte.json), eine für alle Sprachen.
    k: [Kürzel, {Sprache: Adresse der Kantonsseite}, {Sprache: Name}],
    g: [Gemeindename, Kanton-Nr., {Sprache: Adresse der Gemeinde-Seite} oder 0],
    o: [Ortsname oder 0 (gleich wie Gemeinde), PLZ, Gemeinde-Nr.], a: andere Schreibweisen."""
    codes = [kid for kid, _ in KANTONE_ALLE]
    reihen = sorted(orte["gemeinden"], key=lambda x: x[0])
    nr = {x[0]: i for i, x in enumerate(reihen)}
    g = [[name, codes.index(kt), g_sprachen(bfs) or 0] for bfs, name, kt in reihen]
    k = [[kid, {l: k_pfad(l, kid) for l in k_sprachen(kid)}, {l: KANTONSNAMEN[l][kid] for l in SPRACHEN}]
         for kid in codes]

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


def feld_liste(k, feld, Q, benutzt):
    """Wahlweises Feld eines Kantons ('vermisst', 'gewerbe') als Linienliste mit Text, Schritten und Quellen."""
    v = k[feld]
    punkte = ("<ul>" + "".join(f"<li>{e(p)}</li>" for p in v["punkte"]) + "</ul>") if v.get("punkte") else ""
    return (f'<div class="list-card" data-{feld}><p>{e(v["text"])}</p>{punkte}'
            f'{qlinks(v["quellen"], Q, benutzt)}</div>')


def kt_zeile(k, Q, benutzt, kopf, inhalt, attr="", quellen=()):
    """Themenseite: ein Kanton als Zeile zum Aufklappen (<details id="kt-<kürzel>">). kopf: Inhalt der summary
    nach dem Namen (Marke, Kurztext), ohne Link. inhalt: Absätze unter der summary. Darunter Quellen und der Link
    auf die Kantonsseite. attr: weitere Attribute des details (Seite nach Feld: data-<feld>)."""
    link = (f'<p><a class="text-link" href="{k_pfad(LANG, k["id"])}">'
            f'{e(S["thema"]["zum_kanton"].format(im=kantonsformen(LANG, k["id"])["im"]))}</a></p>')
    return (f'<details class="kt-zeile" id="kt-{k["id"]}"{attr}><summary><span class="kt-name">'
            f'{e(KANTONSNAMEN[LANG][k["id"]])}</span>{kopf}</summary>'
            f'<div class="kt-inhalt">{inhalt}{qlinks(list(quellen), Q, benutzt)}{link}</div></details>')


def uebrige_kantone(ohne, alle=False):
    """Eine Zeile mit Links auf die Kantone dieser Sprache, die auf einer Seite nach Feld keinen Eintrag haben.
    alle: Kein Kanton hat einen Eintrag, die Zeile führt alle auf (Satz 'alle_kt')."""
    if not ohne:
        return ""
    links = ", ".join(f'<a href="{k_pfad(LANG, k["id"])}">{e(KANTONSNAMEN[LANG][k["id"]])}</a>' for k in ohne)
    return f'<p class="more-kt">{S["thema"]["alle_kt" if alle else "uebrige"]} {links}.</p>'


def wald_karte(w):
    """Leine im Wald als Karte für die Themenseite und den Abschnitt «Neu einen Hund»: marke, ton, wert, text."""
    T = S["thema"]
    if w.get("saison"):
        d = daten_wald(w)
        wert = T["wald_wert"].format(**d)
        c = {"marke": S["wald_band"], "ton": "must", "wert": wert[0].upper() + wert[1:],
             "text": T["wald_text"].format(**d)}
    elif w.get("ganzjaehrig"):
        c = {"marke": S["wald_band"], "ton": "must", "wert": T["wald_immer_wert"], "text": w["text"]}
    else:
        c = {"marke": T["wald_ohne"], "ton": "none", "wert": w.get("titel") or S["wald_ohne_gross"],
             "text": w["text"]}
    c["quellen"] = w["quellen"]
    return c


def abschnitt_neuer_hund(k):
    """Abschnitt der Kantonsseite (#neuer-hund): sechs Schritte aus 'karten' und 'vergleich', ohne neue Angaben.
    Ob etwas Pflicht ist, sagen nur Marke und Text des Kantons."""
    zeilen = []
    for pos, key in NEU_SCHRITTE:
        if pos is None:
            c, titel, ziel = wald_karte(k["wald"]), S["neu_wald"], "wald"
        else:
            c = k["karten"][pos]
            titel, ziel = c["titel"], KARTEN_ANKER[pos]
        marke = f'<span class="chip {e(c["ton"])}">{e(c["marke"])}</span>' if c.get("marke") else ""
        zeilen.append(f'<li class="schritt"><a class="schritt-k" href="#{ziel}">{e(titel)}</a>{marke}'
                      f'<span class="schritt-t">{e(k["vergleich"][key])}</span></li>')
    return (f'<section class="sec" id="neuer-hund" data-neuer-hund><div class="sec-head">'
            f'<h2>{e(S["neu_h2"].format(im=k["im"]))}</h2><p>{e(S["neu_p"])}</p></div>'
            f'<ol class="schritte" role="list">{"".join(zeilen)}</ol></section>')


def abschnitt_feld(k, feld, Q, benutzt):
    """Abschnitt der Kantonsseite zu einem wahlweisen Feld (id = Name des Felds), nur wenn der Kanton es hat.
    Überschrift aus TEXTE unter '<feld>_h2'."""
    if not k.get(feld):
        return ""
    return (f'<section class="sec" id="{feld}"><div class="sec-head"><h2>{e(S[feld + "_h2"].format(im=k["im"]))}</h2></div>'
            f'{feld_liste(k, feld, Q, benutzt)}</section>')


def themenleiste(ohne=None):
    """Tafeln zu den Themenseiten in der Sprache der Seite. ohne: id der Seite, auf der die Leiste steht."""
    return ('<div class="plates small liste">'
            + "".join(tafel(thema_pfad(t["id"]), S["themen"][t["id"]]["name"],
                                    S["themen"][t["id"]].get("unter", S["thema"]["alle"]))
                      for t in THEMEN if t["id"] != ohne)
            + '</div>')


def andere_kantone(text):
    """Eine Zeile mit den erfassten Kantonen, die es in der Sprache der Seite nicht gibt:
    Link auf ihre Seite und Angabe der Sprache. Leer, wenn es keine gibt."""
    teile = []
    for kid in erfasste():
        lang, pfad = k_ziel(kid)
        if lang != LANG:
            teile.append(f'<a href="{pfad}" hreflang="{HTMLLANG[lang]}">{e(KANTONSNAMEN[LANG][kid])}</a> '
                         f'({S["sprache"][lang]})')
    return f'<p class="more-kt">{text} {", ".join(teile)}.</p>' if teile else ""


def themenkacheln():
    """Startseite: eine Tafel pro Themenseite, mit einem Satz, was man dort findet."""
    teile = []
    for t in THEMEN:
        tt = S["themen"][t["id"]]
        teile.append(f'<a class="topic" href="{thema_pfad(t["id"])}"><span class="topic-name">{e(tt["name"])}</span>'
                     f'<span class="topic-text">{e(tt["kurz"])}</span></a>')
    return f'<div class="topics">{"".join(teile)}</div>'


def gemeindeverzeichnis():
    """Startseite: pro Kanton eine Zeile mit seinen Gemeinden, alphabetisch in der Sprache der Seite."""
    namen = KANTONSNAMEN[LANG]
    zeilen = []
    for kid in sorted(erfasste(), key=lambda x: ohne_akzent(namen[x])):
        gemeinden = gemeinden_von(kid)
        if not gemeinden:
            continue
        links = []
        for lang, g in gemeinden:
            if lang == LANG:
                links.append(f'<li><a href="{g_pfad(lang, g)}">{e(g["ort"])}</a></li>')
            else:
                links.append(f'<li><a href="{g_pfad(lang, g)}" hreflang="{HTMLLANG[lang]}">{e(g["ort"])}</a> '
                             f'<span class="lg">{S["sprache"][lang]}</span></li>')
        zeilen.append(f'<div><dt><a href="{k_ziel(kid)[1]}">{e(namen[kid])}</a></dt>'
                      f'<dd><ul>{"".join(links)}</ul></dd></div>')
    return f'<dl class="index">{"".join(zeilen)}</dl>'


def seite(pfad, titel, beschr, inhalt, krumen, stand, benutzt, Q, index=True, alt=None, skripte=""):
    """pfad: Adresse ab Wurzel, z. B. '/zh/zuerich/'. krumen: Liste (Name, Pfad).
    alt: {Sprache: Adresse} aller Sprachfassungen dieser Seite, die eigene eingeschlossen.
    skripte: weitere Skripte nur für diese Seite (Karte der Hundezonen)."""
    crumbs, ld = "", ""
    start = PRAEFIX[LANG] + "/"
    if krumen:
        teile = []
        for i, (name, href) in enumerate(krumen):
            if i == len(krumen) - 1:
                teile.append(f'<span aria-current="page">{e(name)}</span>')
            else:
                teile.append(f'<a href="{href}">{e(name)}</a><span aria-hidden="true">›</span>')
        crumbs = f'<nav class="crumbs" aria-label="{S["pfad"]}">{"".join(teile)}</nav>'
        liste = [{"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + href}
                 for i, (name, href) in enumerate(krumen)]
        ld = ('<script type="application/ld+json">'
              + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                            "itemListElement": liste}, ensure_ascii=False)
              + '</script>')
    if pfad == "/":
        ld = ('<script type="application/ld+json">'
              + json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": "Gassi-Kompass",
                            "url": SITE + "/"}, ensure_ascii=False)
              + '</script>')
    stempel = f'<span class="stamp">{S["stempel"].format(d=de_datum(stand))}</span>' if stand else ""
    # Sprachfassungen derselben Seite: hreflang im Kopf und ein Sprachwechsel, nur wo es die Seite gibt
    hreflang = ""
    if alt and len(alt) > 1:
        hreflang = "".join(f'<link rel="alternate" hreflang="{HTMLLANG[l]}" href="{SITE}{alt[l]}">\n'
                           for l in SPRACHEN if l in alt)
        wechsel = "".join(f'<a href="{alt[l]}" lang="{HTMLLANG[l]}" hreflang="{HTMLLANG[l]}">{TEXTE[l]["name"]}</a>'
                          for l in SPRACHEN if l in alt and l != LANG)
        stempel = (f'<span class="top-r">{stempel}<nav class="lang" aria-label="{S["sprachwahl"]}">'
                   f'{wechsel}</nav></span>')
    quellen = ""
    if benutzt:
        punkte = "".join(f'<li><a href="{e(Q[k]["url"])}" target="_blank" rel="noopener">{e(Q[k]["lang"])}</a></li>'
                         for k in benutzt)
        kopf = S["fuss_quellen"].format(d=de_datum(stand))
        if len(benutzt) > FUSS_OFFEN:
            quellen = (f'<p>{kopf}</p><details class="more fuss-quellen" id="quellen" data-breit-offen>'
                       f'<summary>{S["fuss_alle"].format(n=len(benutzt))}</summary><ol>{punkte}</ol></details>')
            if AUFKLAPPEN not in skripte:
                skripte += AUFKLAPPEN
        else:
            quellen = f'<p id="quellen">{kopf}</p><ol>{punkte}</ol>'
    if benutzt:  # fürs Quellenverzeichnis: welche Seite welche Quelle zitiert
        name = krumen[-1][0] if krumen else titel
        if krumen and len(krumen) > 3:  # Karte der Hundezonen: «Stadt Zürich: Karte»
            name = f"{krumen[-2][0]}: {name}"
        for key in benutzt:
            ZITIERT.setdefault(LANG, {}).setdefault(key, []).append((pfad, name))
    robots = "" if index else '<meta name="robots" content="noindex">\n'
    mail = f'<a href="mailto:{KONTAKT}?subject={quote(S["betreff"] + pfad)}">{KONTAKT}</a>'
    return f"""<!doctype html>
<html lang="{HTMLLANG[LANG]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschr)}">
{robots}<link rel="canonical" href="{SITE}{pfad}">
{hreflang}<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschr)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{pfad}">
<meta property="og:locale" content="{HTMLLANG[LANG].replace("-", "_")}">
<meta property="og:site_name" content="Gassi-Kompass">
<meta property="og:image" content="{SITE}/assets/teilen-{LANG}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(S["teilbild"])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/sourceserif4.woff2" as="font" type="font/woff2" crossorigin>
<meta name="theme-color" content="#1E3B2C">
<link rel="stylesheet" href="/assets/site.css">
{ld}
</head>
<body>
<a class="skip" href="#inhalt">{S["zum_inhalt"]}</a>
<div class="wrap">
<header class="top{" mit-pfad" if crumbs else ""}"><a class="brand" href="{start}">Gassi-Kompass</a>{stempel}{crumbs}</header>
<main id="inhalt" tabindex="-1">
{inhalt.replace("<!--KRUMEN-->", "")}
</main>
<footer class="foot">
<p>{S["fuss_recht"]}</p>
<p>{S["fuss_fehler"].format(mail=mail)}</p>
{quellen}
<nav aria-label="{S["fussnav"]}"><a href="{start}">{S["nav_suche"]}</a><a href="{bund_ziel()[1]}">{S["nav_schweiz"]}{in_sprache(bund_ziel()[0])}</a><a href="{start}#vergleich">{S["nav_vergleich"]}</a><a href="{start}quellen/">{S["nav_quellen"]}</a><a href="{start}ueber/">{S["nav_ueber"]}</a></nav>
</footer>
</div>
<script src="/assets/heute.js" defer></script>
<script src="/assets/suche.js" defer></script>
{skripte}</body>
</html>
"""


# --------------------------------------------------------------------- Seiten

def startseiten():
    """Adressen der Startseiten: Deutsch immer, die anderen Sprachen ab dem ersten Kanton."""
    return {l: PRAEFIX[l] + "/" for l in SPRACHEN if l == "de" or W[l]["k"]}


def seite_start(Q):
    kantone = W[LANG]["k"]
    start = PRAEFIX[LANG] + "/"
    bl, bpfad = bund_ziel()
    gemeinden = len({g["bfs"] for l in SPRACHEN for g in W[l]["g"]})
    zahlen = (len(erfasste()), gemeinden, ZAHLEN.get("quellen", len(Q)))
    fakten = "".join(f"<li><strong>{n}</strong> {e(text)}</li>" for n, text in zip(zahlen, S["fakten"]))
    stand = min([k["geprueft"] for k in kantone] + ([W[LANG]["b"]["geprueft"]] if W[LANG].get("b") else []))
    inhalt = f"""<section class="hero">
<h1>{S["start_h1"]}</h1>
{suche()}
<p class="lede">{S["start_lede"]}</p>
<ul class="facts">{fakten}</ul>
</section>
<section class="sec" id="orte">
<div class="sec-head"><h2>{S["start_kt_h2"]}</h2><p>{S["start_kt_p"].format(schweiz=bpfad, in_sprache=in_sprache(bl))}</p></div>
{kantonsraster()}
</section>
<section class="sec" id="gemeinden">
<div class="sec-head"><h2>{S["start_gm_h2"]}</h2><p>{S["start_gm_p"]}</p></div>
{gemeindeverzeichnis()}
</section>
<section class="sec" id="vergleich">
<div class="sec-head"><h2>{S["start_vg_h2"]}</h2><p>{S["start_vg_p"]}</p></div>
{themenkacheln()}
</section>"""
    return seite(start, S["start_titel"], S["start_beschr"], inhalt, None, stand, [], Q, alt=startseiten())


def seite_schweiz(Q):
    """Regeln des Bundes in der Sprache der Seite, aus der Originalfassung dieser Sprache."""
    bund, b = W[LANG]["b"], S["bund"]
    benutzt = []
    start = PRAEFIX[LANG] + "/"
    pfad = f"{start}schweiz/"
    ids = [c.get("id") or f"karte-{i + 1}" for i, c in enumerate(bund["karten"])]
    karten = "".join(karte(c, Q, benutzt, anker=ids[i]) for i, c in enumerate(bund["karten"]))
    uebersicht = blick([(f"#{ids[i]}", c["titel"], "", c["wert"]) for i, c in enumerate(bund["karten"])], b["h2"])
    da = erfasste()
    offen = json.dumps({kid: KANTONSNAMEN[LANG][kid] for kid, _ in KANTONE_ALLE if kid not in da}, ensure_ascii=False)
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>{b["h1"]}</h1>
<p class="lede">{b["lede"]}</p>
<p class="callout" data-ort-hinweis data-kantone="{e(offen)}" data-text="{e(b["hinweis"])}" hidden></p>
</section>
{sprungleiste(["pflichten", "kantone", "quellen"])}
<section class="sec" id="pflichten">
<div class="sec-head"><h2>{b["h2"]}</h2></div>
{uebersicht}
<div class="cards">{karten}</div>
</section>
<section class="sec" id="kantone">
<div class="sec-head"><h2>{b["kt_h2"]}</h2><p>{b["kt_p"]}</p></div>
{kantonsraster()}
<p><a class="text-link" href="{start}">{b["suche"]}</a></p>
</section>"""
    return seite(pfad, b["titel"], b["beschr"], inhalt, [(S["start"], start), (S["nav_schweiz"], pfad)],
                 bund["geprueft"], benutzt, Q,
                 alt={l: PRAEFIX[l] + "/schweiz/" for l in SPRACHEN if W[l].get("b")})


def seite_kanton(k, Q):
    benutzt = []
    start = PRAEFIX[LANG] + "/"
    pfad = k_pfad(LANG, k["id"])
    bl, bpfad = bund_ziel()
    tafeln = gemeinde_tafeln(k["id"])
    orte = (f'<div class="plates liste">{tafeln}</div>' if tafeln else "")
    f = {"im": k["im"], "des": k["des"], "name": k["name"]}
    ziele = ["leine", "pflichten", "neuer-hund"] + [f for f in FELDER if k.get(f)] + \
        ["gemeinden", "themen", "quellen"]
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>{e(S["kt_h1"].format(**f))}</h1>
<p class="lede">{e(S["kt_lede"].format(**f))}</p>
{hinweis_uebersetzung(k, "k")}{hinweis_durchsicht(k)}
<p class="callout" data-ort-hinweis data-text="{e(S["kt_hinweis"].format(**f))}" hidden></p>
</section>
{wald(k, Q, benutzt, anker=True)}
{sprungleiste(ziele)}
{regeln(k, Q, benutzt)}
{pflichten(k, Q, benutzt)}
{abschnitt_neuer_hund(k)}
{"".join(abschnitt_feld(k, f, Q, benutzt) for f in FELDER)}
<section class="sec" id="gemeinden">
<div class="sec-head"><h2>{e(S["kt_gm_h2"].format(**f))}</h2><p>{S["kt_gm_p"]}</p></div>
{orte}
<p><a class="text-link" href="{bpfad}">{S["link_schweiz"]}{in_sprache(bl)}</a></p>
<p><a class="text-link" href="{start}">{S["link_suche"]}</a></p>
</section>
<section class="sec" id="themen">
<div class="sec-head"><h2>{S["kt_themen_h2"]}</h2><p>{S["kt_themen_p"]}</p></div>
{themenleiste()}
</section>"""
    return seite(pfad, S["kt_titel"].format(**f), S["kt_beschr"].format(**f),
                 inhalt, [(S["start"], start), (k["name"], pfad)], k["geprueft"], benutzt, Q,
                 alt={l: k_pfad(l, k["id"]) for l in k_sprachen(k["id"])})


def seite_gemeinde(g, k, Q):
    benutzt = []
    start = PRAEFIX[LANG] + "/"
    bl, bpfad = bund_ziel()
    andere = gemeinde_tafeln(k["id"], ohne=g["bfs"])
    orte = f'<div class="plates liste">{andere}</div>' if andere else ""
    stand = min(g["geprueft"], k["geprueft"])
    f = {"in_ort": g["in_ort"], "im": k["im"], "des": k["des"]}
    weiter = S["gm_weitere"].format(**f) if andere else S["gm_weiter_h2"]
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>{e(S["gm_h1"].format(**f))}</h1>
{blick_gemeinde(g)}
{hinweis_uebersetzung(g, "g")}
</section>
{wald(k, Q, benutzt, g.get("hinweis_heute"), kurz=True)}
{lokal(g, Q, benutzt)}
{regeln(k, Q, benutzt)}
{pflichten_kurz(k, Q, benutzt)}
<section class="sec">
<div class="sec-head"><h2>{e(weiter)}</h2></div>
{orte}
<p><a class="text-link" href="{k_pfad(LANG, k["id"])}">{e(S["gm_kanton"].format(**f))}</a></p>
<p><a class="text-link" href="{bpfad}">{S["link_schweiz"]}{in_sprache(bl)}</a></p>
<p><a class="text-link" href="{start}">{S["link_suche"]}</a></p>
</section>"""
    pfad = g_pfad(LANG, g)
    return seite(pfad, S["gm_titel"].format(**f), S["gm_beschr"].format(**f),
                 inhalt, [(S["start"], start), (k["name"], k_pfad(LANG, k["id"])), (g["name"], pfad)],
                 stand, benutzt, Q, alt=g_sprachen(g["bfs"]))


def seite_karte(g, k, geo, Q):
    """Karte der Hundezonen einer Gemeinde. Bis zum Klick auf «Karte laden» ruft die Seite nichts Fremdes ab:
    Das Kartenprogramm liegt unter /assets/karte/, die Kartenbilder kommen danach von swisstopo."""
    K = S["karte"]
    benutzt = []
    start = PRAEFIX[LANG] + "/"
    zonen = geo["zonen"]
    je = {art: sum(1 for z in zonen if ZONEN_ART[z["z"]] == art) for art in ("frei", "leine", "verbot")}
    f = {"in_ort": g["in_ort"], "n": len(zonen), "stand": geo["stand"], "im": k["im"], "des": k["des"]}
    wahl = "".join(
        f'<label><input type="checkbox" data-karte-art="{art}" checked>'
        f'<span class="muster {art}" aria-hidden="true"></span>{e(K["anzahl"][art].format(n=je[art]))}</label>'
        for art in ("frei", "leine", "verbot"))
    frei = "".join(
        f'<button type="button" class="dest" data-karte-zeige="{i}"><span class="dest-name">{e(z["n"])}</span></button>'
        for i, z in enumerate(zonen) if ZONEN_ART[z["z"]] == "frei")
    farben = "".join(f'<li><span class="muster {art}" aria-hidden="true"></span>{e(text)}</li>'
                     for art, text in K["farben"])
    grenzen = "".join(f"<li>{e(text.format(**f))}</li>" for text in K["grenzen"])
    seite_g = g_pfad(LANG, g)
    daten = f'/{g["kanton"]}/{g["id"]}/karte/zonen.json'
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>{e(K["h1"].format(**f))}</h1>
<p class="lede">{e(K["lede"].format(**f))}</p>
</section>
<section class="sec karte" data-karte data-stand="start" data-daten="{daten}" data-texte="{e(json.dumps(K["js"], ensure_ascii=False))}">
<div class="sec-head"><h2>{e(K["h2"])}</h2></div>
<fieldset class="karte-wahl"><legend class="sr">{e(K["wahl"])}</legend>{wahl}</fieldset>
<div class="karte-feld" data-karte-feld>
<div class="karte-start" data-karte-start>
<p>{e(K["einwilligung"])}</p>
<button type="button" class="dest" data-karte-laden hidden><span class="dest-name">{e(K["laden"])}</span></button>
<noscript><p>{e(K["ohne_js"].format(seite=S["gm_h1"].format(**f)))}</p></noscript>
</div>
<div class="karte-info" data-karte-info aria-live="polite" hidden></div>
</div>
<p class="karte-status" data-karte-status role="status"></p>
<div class="karte-ort" hidden><button type="button" class="dest" data-karte-ort aria-pressed="false">{e(K["js"]["standort"])}</button><p>{e(K["standort_hinweis"])}</p></div>
<p class="src">{e(K["nachweis"].format(**f))}</p>
{qlinks([geo["quelle"]], Q, benutzt)}
</section>
<section class="sec">
<div class="sec-head"><h2>{e(K["h2_frei"].format(**f))}</h2><p>{e(K["frei_p"])}</p></div>
<div class="plates liste">{frei}</div>
</section>
<section class="sec">
<div class="sec-head"><h2>{e(K["h2_lesen"])}</h2></div>
<div class="split">
<div class="list-card legende"><h3>{e(K["h3_farben"])}</h3><ul>{farben}</ul></div>
<div class="list-card"><h3>{e(K["h3_grenzen"])}</h3><ul>{grenzen}</ul></div>
</div>
</section>
<section class="sec">
<div class="sec-head"><h2>{e(S["gm_weiter_h2"])}</h2></div>
<p><a class="text-link" href="{seite_g}">{e(K["zurueck"].format(**f))}</a></p>
<p><a class="text-link" href="{k_pfad(LANG, k["id"])}">{e(S["gm_kanton"].format(**f))}</a></p>
<p><a class="text-link" href="{start}">{S["link_suche"]}</a></p>
</section>"""
    pfad = karte_pfad(LANG, g)
    return seite(pfad, K["titel"].format(**f), K["beschr"].format(**f), inhalt,
                 [(S["start"], start), (k["name"], k_pfad(LANG, k["id"])), (g["name"], seite_g), (K["pfad"], pfad)],
                 geo["abgerufen"], benutzt, Q, alt={l: p + "karte/" for l, p in g_sprachen(g["bfs"]).items()},
                 skripte='<script src="/assets/karte.js" defer></script>\n')


def seite_thema(t, Q):
    """Vergleich aller Kantone, die es in der Sprache der Seite gibt, zu einem Thema. Alle Angaben
    stammen aus den Kantonsdateien dieser Sprache. Die übrigen Kantone stehen in einer Zeile darunter."""
    if t.get("feld"):
        return seite_thema_feld(t, Q)
    benutzt = []
    T, tt = S["thema"], S["themen"][t["id"]]
    kantone = W[LANG]["k"]
    n = len(kantone)
    start = PRAEFIX[LANG] + "/"
    bl, bpfad = bund_ziel()
    if t["karte"] is None:
        saison = [k for k in kantone if k["wald"].get("saison")]
        zeiten = {(k["wald"]["von"], k["wald"]["bis"]) for k in saison}
        zeit = ""
        if len(saison) > 1 and len(zeiten) == 1:
            von, bis = next(iter(zeiten))
            zeit = T["wald_zeit"].format(**daten_wald({"von": von, "bis": bis, "wo": ""}))
        immer = sum(1 for k in kantone if k["wald"].get("ganzjaehrig"))
        zahl = T["wald_zahl"].format(m=len(saison), n=n, zeit=zeit)
        if immer:
            zahl += T["wald_immer_zahl"].format(g=immer, n=n)
        if len(saison) + immer < n:
            zahl += T["wald_rest"]
    elif t.get("zaehlt"):
        zahl = tt["pflicht"].format(m=sum(1 for k in kantone if k["karten"][t["karte"]]["ton"] == "must"), n=n)
    else:
        zahl = tt["sonst"]
    zeilen = []
    for k in kantone:
        if t["karte"] is None:
            c = wald_karte(k["wald"])
        else:
            c = dict(k["karten"][t["karte"]])
        kopf = (f'<span class="kt-marke"><span class="chip {e(c["ton"])}">{e(c["marke"])}</span></span>'
                f'<span class="kt-kurz">{e(k["vergleich"][t["key"]])}</span>')
        mehr = ""
        if c.get("mehr"):
            liste = c["mehr"]["punkte"]
            saetze = ' class="saetze"' if sorted(len(p) for p in liste)[len(liste) // 2] > 50 else ""
            mehr = (f'<details class="more"><summary>{e(c["mehr"]["titel"])}</summary>'
                    f'<ul{saetze}>{"".join(f"<li>{e(p)}</li>" for p in liste)}</ul></details>')
        inhalt = f'<p class="kt-wert">{e(c["wert"])}</p><p>{e(c["text"])}</p>{mehr}'
        zeilen.append(kt_zeile(k, Q, benutzt, kopf, inhalt, quellen=c["quellen"]))
    teil = T["teil"].format(n=n) + " " if len(erfasste()) > n else ""
    bund = T["bund"].format(schweiz=bpfad, in_sprache=in_sprache(bl))
    uebersetzt = f'\n<p class="transl">{T["uebersetzt"]}</p>' if any("uebersetzt_aus" in k for k in kantone) else ""
    pfad = thema_pfad(t["id"])
    inhalt = f"""<section class="hero thema"><!--KRUMEN-->
<h1>{e(T["h1"].format(name=tt["name"]))}</h1>
<p class="lede">{e(teil)}{e(zahl)} {bund}</p>
</section>
<section class="sec">
<div class="sec-head"><h2>{e(T["ueberblick_h2"].format(spalte=tt["spalte"]))}</h2><p>{T["liste_p"]}</p></div>
<div class="kt-liste" data-kt-liste><div class="kt-kopf" aria-hidden="true"><span>{S["vg_kanton"]}</span><span>{T["blick"]}</span><span>{e(tt["spalte"])}</span></div>{"".join(zeilen)}</div>
{andere_kantone(T["andere"])}{uebersetzt}
</section>
<section class="sec">
<div class="sec-head"><h2>{T["weitere_h2"]}</h2></div>
{themenleiste(t["id"])}
<p><a class="text-link" href="{start}">{S["bund"]["suche"]}</a></p>
</section>"""
    return seite(pfad, T["titel"].format(name=tt["name"]), tt["beschr"], inhalt,
                 [(S["start"], start), (tt["name"], pfad)], min(k["geprueft"] for k in kantone), benutzt, Q,
                 alt={l: f'{PRAEFIX[l]}/thema/{t["id"]}/' for l in SPRACHEN if W[l]["k"]}, skripte=AUFKLAPPEN)


def seite_thema_feld(t, Q):
    """Themenseite zu einem wahlweisen Feld der Kantone ('vermisst', 'gewerbe'). Zuoberst die Karte des Bundes
    mit derselben id, darunter jeder Kanton dieser Sprache, der das Feld hat. Kein Vergleich, keine Zahl."""
    benutzt = []
    tt = S["themen"][t["id"]]
    start = PRAEFIX[LANG] + "/"
    bund = W[LANG].get("b")
    kantone = [k for k in W[LANG]["k"] if k.get(t["feld"])]
    bl, bpfad = bund_ziel()
    oben = ""
    if bund:
        c = next(c for c in bund["karten"] if c.get("id") == t["id"])
        oben = (f'<section class="sec"><div class="sec-head"><h2>{tt["bund_h2"]}</h2></div>'
                f'<div class="cards">{karte(c, Q, benutzt, link=bpfad)}</div></section>')
    zeilen = []
    for k in kantone:
        v = k[t["feld"]]
        punkte = ("<ul>" + "".join(f"<li>{e(p)}</li>" for p in v["punkte"]) + "</ul>") if v.get("punkte") else ""
        zeilen.append(kt_zeile(k, Q, benutzt, "", f'<p>{e(v["text"])}</p>{punkte}', attr=f" data-{t['feld']}",
                               quellen=v["quellen"]))
    uebersetzt = (f'\n<p class="transl">{S["thema"]["uebersetzt"]}</p>'
                  if any("uebersetzt_aus" in k for k in kantone) else "")
    ohne = uebrige_kantone([k for k in W[LANG]["k"] if not k.get(t["feld"])])
    unten = (f'<section class="sec"><div class="sec-head"><h2>{tt["kt_h2"]}</h2><p>{tt["kt_p"]}</p></div>'
             f'<div class="kt-liste nur-name" data-kt-liste>{"".join(zeilen)}</div>'
             f'{ohne}{uebersetzt}</section>') if kantone else \
        (f'<section class="sec"><div class="sec-head"><h2>{tt["kt_h2"]}</h2></div>'
         f'{uebrige_kantone(W[LANG]["k"], alle=True)}</section>')
    pfad = thema_pfad(t["id"])
    inhalt = f"""<section class="hero thema"><!--KRUMEN-->
<h1>{e(tt["h1"])}</h1>
<p class="lede">{e(tt["lede"])}</p>
</section>
{oben}
{unten}
<section class="sec">
<div class="sec-head"><h2>{S["thema"]["weitere_h2"]}</h2></div>
{themenleiste(t["id"])}
<p><a class="text-link" href="{start}">{S["bund"]["suche"]}</a></p>
</section>"""
    stand = min([k["geprueft"] for k in kantone] + ([bund["geprueft"]] if bund else [])
                or [min(k["geprueft"] for k in W[LANG]["k"])])
    return seite(pfad, tt["titel"], tt["beschr"], inhalt, [(S["start"], start), (tt["name"], pfad)],
                 stand, benutzt, Q, alt={l: f'{PRAEFIX[l]}/thema/{t["id"]}/' for l in SPRACHEN if W[l]["k"]},
                 skripte=AUFKLAPPEN)


def seite_ueber(Q):
    u = S["ueber"]
    start = PRAEFIX[LANG] + "/"
    mail = f'<a href="mailto:{KONTAKT}">{KONTAKT}</a>'
    swisstopo = f'<a href="{e(Q["ch_swisstopo_orte"]["url"])}" target="_blank" rel="noopener">'
    teile = "\n".join(f"<h2>{h2}</h2>\n<p>{p.replace('{swisstopo}', swisstopo).replace('{mail}', mail)}</p>"
                      for h2, p in u["teile"])
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>{u["h1"]}</h1>
<p class="lede">{u["lede"]}</p>
</section>
<section class="prose">
{teile}
<p>{u["schluss"]}</p>
</section>"""
    ZITIERT.setdefault(LANG, {}).setdefault("ch_swisstopo_orte", []).append((f"{start}ueber/", S["nav_ueber"]))
    return seite(f"{start}ueber/", u["titel"], u["beschr"],
                 inhalt, [(S["start"], start), (S["nav_ueber"], f"{start}ueber/")], None, [], Q,
                 alt={l: p + "ueber/" for l, p in startseiten().items()})


def quellen_von(obj):
    """Alle Quellen, die eine Datendatei zitiert (Felder, deren Name auf «quellen» endet)."""
    gefunden = set()
    if isinstance(obj, dict):
        for key, wert in obj.items():
            if key.startswith("_"):
                continue
            if key.endswith("quellen") and isinstance(wert, list):
                gefunden.update(wert)
            else:
                gefunden |= quellen_von(wert)
    elif isinstance(obj, list):
        for wert in obj:
            gefunden |= quellen_von(wert)
    return gefunden


def seite_quellen(Q):
    """Quellenverzeichnis der Sprache: jede Quelle, die eine Seite dieser Sprache zitiert (ZITIERT, gefüllt beim
    Bauen der anderen Seiten). Geltungsbereich aus dem Schlüssel und den Dateien, die sie zitieren: Bund, Kanton oder,
    wenn nur die Datei einer Gemeinde sie zitiert, diese Gemeinde. Ohne Skript steht die Liste nach Kanton geordnet da,
    assets/quellen.js filtert, sucht und sortiert."""
    qv = S["qv"]
    start = PRAEFIX[LANG] + "/"
    pfad = f"{start}quellen/"
    namen = KANTONSNAMEN[LANG]
    bund = W[LANG].get("b")
    dateien = ([("b", None, bund)] if bund else []) + [("k", k["id"], k) for k in W[LANG]["k"]] + \
        [("g", g["kanton"], g) for g in W[LANG]["g"]]
    zitiert_von = {}  # Quelle: [(Art, Kanton, Datei)]
    eigen = {}        # Adresse einer Gemeindeseite oder Karte: Quellen, die ihre eigene Datei zitiert
    for art, kt, d in dateien:
        qs = quellen_von(d)
        for key in qs:
            zitiert_von.setdefault(key, []).append((art, kt, d))
        if art == "g":
            eigen[g_pfad(LANG, d)] = qs
            geo = karten_geo(d)
            if geo:
                eigen[karte_pfad(LANG, d)] = {geo["quelle"]}
    themen = {thema_pfad(t["id"]) for t in THEMEN}
    eintraege = []
    for key, seiten in ZITIERT.get(LANG, {}).items():
        von = zitiert_von.get(key, [])
        praefix = key.split("_")[0]
        kantone = {kt for art, kt, _ in von if art == "k"}
        gemeinden = [d for art, _, d in von if art == "g"]
        if praefix == "ch" or any(art == "b" for art, _, _ in von):
            kt, wo, gm = "ch", qv["bund"], None
        elif kantone:
            kt = praefix if praefix in kantone else sorted(kantone)[0]
            wo, gm = qv["kanton"], None
        elif len(gemeinden) == 1:
            kt, gm = gemeinden[0]["kanton"], gemeinden[0]
            wo = gm["name"]
        else:
            kt = praefix if praefix in namen else (gemeinden[0]["kanton"] if gemeinden else "ch")
            wo, gm = (qv["kanton"], None) if kt != "ch" else (qv["bund"], None)
        # Gemeindeseiten zeigen auch die Quellen ihres Kantons: «zitiert auf» nennt nur die Seiten, deren Datei
        # die Quelle selbst zitiert, dazu Themenseiten, die Seite des Bundes und «Über diese Seite».
        ziele, gesehen = [], set()
        for sp, name in seiten:
            if sp in gesehen or (sp in eigen and key not in eigen[sp]):
                continue
            gesehen.add(sp)
            ziele.append((1 if sp in themen or sp.endswith("/ueber/") else 0, sp, name))
        ziele.sort(key=lambda z: z[0])
        daten = [d["geprueft"] for _, _, d in von if d.get("geprueft")]
        kanton_name = qv["bund"] if kt == "ch" else namen[kt]
        such = such_norm(" ".join([Q[key]["kurz"], Q[key]["lang"], kanton_name, kt, gm["name"] if gm else "",
                                   gm["ort"] if gm else ""]))
        eintraege.append({"key": key, "kt": kt, "wo": wo, "gm": gm, "ziele": ziele, "datum": max(daten) if daten else None,
                          "such": such, "name": ohne_akzent(Q[key]["kurz"]).lower()})
    gruppen = ["ch"] + sorted({x["kt"] for x in eintraege} - {"ch"}, key=lambda kid: ohne_akzent(namen[kid]))
    eintraege.sort(key=lambda x: (gruppen.index(x["kt"]), x["gm"] is not None,
                                  ohne_akzent(x["gm"]["ort"]).lower() if x["gm"] else "", x["name"]))
    nach_name = sorted(range(len(eintraege)), key=lambda i: (eintraege[i]["name"], eintraege[i]["key"]))
    rang = {i: r for r, i in enumerate(nach_name)}
    zeilen, gruppe = [], None
    for i, x in enumerate(eintraege):
        if x["kt"] != gruppe:
            gruppe = x["kt"]
            titel = qv["bund"] if gruppe == "ch" else kanton_titel(gruppe)
            zeilen.append(f'<li class="q-gruppe" data-gruppe="{gruppe}"><h2>{e(titel)}</h2></li>')
        c = Q[x["key"]]
        auf = "".join(f'<a href="{sp}">{e(name)}</a>' for _, sp, name in x["ziele"])
        meta = e(x["wo"]) + (" · " + e(qv["abgeglichen"].format(d=de_datum(x["datum"]))) if x["datum"] else "")
        zeilen.append(
            f'<li class="q" data-kt="{x["kt"]}" data-s="{e(x["such"])}" data-n="{rang[i]}">'
            f'<div class="q-kopf"><span class="q-code">{x["kt"].upper()}</span><span class="q-kurz">{e(c["kurz"])}</span></div>'
            f'<p class="q-lang"><a href="{e(c["url"])}" target="_blank" rel="noopener">{e(c["lang"])}</a></p>'
            f'<div class="src q-auf"><span>{qv["zitiert"]}</span>{auf}</div><p class="q-datum">{meta}</p></li>')
    knoepfe = "".join(f'<button type="button" class="q-k" data-kt="{kid}" aria-pressed="false" '
                      f'title="{e(qv["bund"] if kid == "ch" else namen[kid])}">{kid.upper()}</button>' for kid in
                      ["ch"] + sorted(set(gruppen) - {"ch"}))
    texte = {k: qv[k] for k in ("s_alle", "s_teil", "s_eins", "s_keine", "g_eins", "g_viele")}
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>{qv["h1"]}</h1>
<div class="q-wahl search" data-quellen data-texte="{e(json.dumps(texte, ensure_ascii=False))}" hidden>
<label for="quellensuche">{qv["label"]}</label>
<input id="quellensuche" type="search" autocomplete="off" enterkeyhint="search" placeholder="{e(qv["beispiel"])}" aria-describedby="q-status">
<div class="q-gruppe-wahl" role="group" aria-label="{e(qv["wahl"])}"><button type="button" class="q-k q-alle" data-kt="" aria-pressed="true">{qv["alle"]}</button>{knoepfe}</div>
<div class="q-sort" role="group" aria-label="{e(qv["sort"])}"><span>{qv["sort"]}</span><button type="button" data-sort="kanton" aria-pressed="true">{qv["nach_kanton"]}</button><button type="button" data-sort="name" aria-pressed="false">{qv["nach_name"]}</button></div>
<p class="search-status" id="q-status" role="status"></p>
</div>
<p class="lede">{qv["lede"]}</p>
</section>
<section class="sec">
<ul class="q-liste" data-q-liste>{"".join(zeilen)}</ul>
</section>"""
    return seite(pfad, qv["titel"], qv["beschr"], inhalt, [(S["start"], start), (qv["pfad"], pfad)], None, [], Q,
                 alt={l: p + "quellen/" for l, p in startseiten().items()},
                 skripte='<script src="/assets/quellen.js" defer></script>\n')


def kanton_titel(kid):
    """Name des Kantons als Zwischenüberschrift: «Kanton Zürich», «Canton de Vaud», aus den Formen der Seiten."""
    return kantonsformen(LANG, kid)["name"]


def seite_404(Q):
    """Eine Fehlerseite für alle Sprachen: deutsch mit Suche, darunter je eine Zeile auf Französisch und
    Italienisch mit dem Link zur Startseite dieser Sprache."""
    nf = S["nf"]
    andere = "".join(f'<p lang="{HTMLLANG[l]}">{TEXTE[l]["nf"]["kurz"]} <a class="text-link" href="{pfad}" '
                     f'hreflang="{HTMLLANG[l]}">{TEXTE[l]["nf"]["start"]}</a></p>'
                     for l, pfad in startseiten().items() if l != LANG)
    inhalt = f"""<section class="hero">
<h1>{nf["h1"]}</h1>
<p class="lede">{nf["lede"]}</p>
{suche()}
<p><a class="text-link" href="/">{nf["start"]}</a></p>
<div class="other-lang">{andere}</div>
</section>"""
    return seite("/404.html", nf["titel"], nf["kurz"], inhalt, None, None, [], Q, index=False)


# ---------------------------------------------------------------------- Bauen

def schreibe(rel, text):
    ziel = ROOT / rel.lstrip("/")
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, "utf-8")


def baue(Q, orte):
    for ordner in ROOT.iterdir():
        if ordner.is_dir() and (ordner / MARKE).exists():
            shutil.rmtree(ordner)
    ZITIERT.clear()
    urls = []
    for lang in SPRACHEN:
        kantone, gemeinden, bund = W[lang]["k"], W[lang]["g"], W[lang].get("b")
        if lang != "de" and not kantone:
            continue  # Seiten in einer Sprache erst ab dem ersten Kanton in dieser Sprache
        sprache(lang)
        start = PRAEFIX[lang] + "/"
        nach_id = {k["id"]: k for k in kantone}
        aeltester = min(k["geprueft"] for k in kantone)
        such = []

        def mit_suche(pfad, art, text):
            such.append(such_eintrag(pfad, art, text))
            return text
        urls.append((start, min([aeltester] + ([bund["geprueft"]] if bund else []))))
        urls.append((f"{start}ueber/", None))
        schreibe(f"{start}index.html", seite_start(Q))
        schreibe(f"{start}ueber/index.html", mit_suche(f"{start}ueber/", "ueber", seite_ueber(Q)))
        if bund:
            urls.append((f"{start}schweiz/", bund["geprueft"]))
            schreibe(f"{start}schweiz/index.html", mit_suche(f"{start}schweiz/", "bund", seite_schweiz(Q)))
        for t in THEMEN:
            schreibe(f'{start}thema/{t["id"]}/index.html', mit_suche(f'{start}thema/{t["id"]}/', "thema", seite_thema(t, Q)))
            urls.append((f'{start}thema/{t["id"]}/', aeltester))
        if lang == "de":
            schreibe("404.html", seite_404(Q))
            for ordner in ("ueber", "schweiz", "thema", "quellen"):
                schreibe(f"{ordner}/{MARKE}", "")
        else:
            schreibe(f"{start}{MARKE}", "")  # der ganze Sprachordner wird beim Neubau ersetzt
        for k in kantone:
            schreibe(f'{k_pfad(lang, k["id"])}index.html', mit_suche(k_pfad(lang, k["id"]), "kanton", seite_kanton(k, Q)))
            if lang == "de":
                schreibe(f'{k["id"]}/{MARKE}', "")
            urls.append((k_pfad(lang, k["id"]), k["geprueft"]))
        for g in gemeinden:
            k = nach_id[g["kanton"]]
            schreibe(f"{g_pfad(lang, g)}index.html", mit_suche(g_pfad(lang, g), "gemeinde", seite_gemeinde(g, k, Q)))
            urls.append((g_pfad(lang, g), min(g["geprueft"], k["geprueft"])))
            geo = karten_geo(g)
            if geo:
                schreibe(f"{karte_pfad(lang, g)}index.html", seite_karte(g, k, geo, Q))
                urls.append((karte_pfad(lang, g), geo["abgerufen"]))
        # Zuletzt: Das Quellenverzeichnis braucht die Quellen aller anderen Seiten dieser Sprache (ZITIERT).
        schreibe(f"{start}quellen/index.html", mit_suche(f"{start}quellen/", "ueber", seite_quellen(Q)))
        urls.append((f"{start}quellen/", None))
        schreibe(f"assets/suche-{lang}.json", such_verzeichnis(lang, such))
    sprache("de")
    for name, geo in GEO.items():  # die Flächen einmal für alle Sprachen, unter der deutschen Adresse
        kt, _, gid = name.partition("-")
        schreibe(f"{kt}/{gid}/karte/zonen.json",
                 json.dumps({"stand": geo["stand"], "zonen": geo["zonen"]}, ensure_ascii=False, separators=(",", ":")))
    schreibe("assets/orte.json", ortsindex(orte))
    eintraege = "".join(
        f"  <url><loc>{SITE}{pfad}</loc>" + (f"<lastmod>{stand}</lastmod>" if stand else "") + "</url>\n"
        for pfad, stand in urls)
    schreibe("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + eintraege + "</urlset>\n")
    schreibe("robots.txt", "User-agent: *\nAllow: /\nDisallow: /data/\nDisallow: /build.py\n"
             "Disallow: /tests/\nDisallow: /tools/\nDisallow: /graphify-out/\nDisallow: /.claude/\nDisallow: /handbuch/\nDisallow: /backlog/\nDisallow: /changelog/\nDisallow: /CLAUDE.md\nDisallow: /BACKLOG.md\nDisallow: /CHANGELOG.md\nDisallow: /README.md\n\n"
             f"Sitemap: {SITE}/sitemap.xml\n")
    return len(urls)


def main():
    if "--pruefsumme" in sys.argv:
        dateien = [a for a in sys.argv[1:] if not a.startswith("--")]
        for a in dateien:
            print(pruefsumme(json.loads(Path(a).read_text("utf-8"))), a)
        if not dateien:
            print("Aufruf: python3 build.py --pruefsumme data/kantone/zh.json")
        return 0 if dateien else 1
    quellen, welt, bund, orte = lade()
    fehler = pruefe(quellen, welt, bund, orte)
    GEO.update(lade_geo(quellen, welt, fehler))
    if fehler:
        print(f"FEHLER ({len(fehler)}). Nichts wurde geschrieben:")
        for f in fehler:
            print("  -", f)
        return 1
    W.update(welt)
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

    sammle({l: {art: [{k: v for k, v in d.items() if not k.startswith("_")} for d in welt[l][art]]
                    for art in ("k", "g")} | {"b": welt[l]["b"]} for l in SPRACHEN})
    benutzt.add("ch_swisstopo_orte")  # steht auf der Seite «Über diese Seite»
    benutzt.update(geo["quelle"] for geo in GEO.values())
    ZAHLEN["quellen"] = len(benutzt & set(quellen))
    unbenutzt = sorted(set(quellen) - benutzt)
    if unbenutzt:
        print("Hinweis: unbenutzte Quellen:", ", ".join(unbenutzt))
    # Ein Kanton oder eine Gemeinde zählt einmal, auch mit Seiten in zwei Sprachen.
    kantone = len(erfasste())
    gemeinden = len({g["bfs"] for l in SPRACHEN for g in welt[l]["g"]})

    def je_sprache(l):
        k, g = welt[l]["k"], welt[l]["g"]
        uk, ug = (sum(1 for d in x if "uebersetzt_aus" in d) for x in (k, g))
        return (f"{l}: {len(k)} Kantone und {len(g)} Gemeinden"
                + (f", davon {uk} und {ug} übersetzt" if uk or ug else ""))

    je = "; ".join(je_sprache(l) for l in SPRACHEN)
    offen = fehlende(welt)
    veraltet = sum(1 for z in offen if z[0] == "veraltet")
    if "--fehlend" in sys.argv:
        for stand, _, l, ziel, aus, original, summe in offen:
            print(f"{stand:<9}{l}  {ziel}  aus {aus}: {original}  Prüfsumme {summe}")
        print(f"{len(offen) - veraltet} Übersetzungen fehlen, {veraltet} sind veraltet." if offen
              else "Alle Übersetzungen sind da und aktuell.")
        return 0
    if "--check" in sys.argv:
        print(f"Daten in Ordnung: {kantone} Kantone, {gemeinden} Gemeinden, {len(quellen)} Quellen ({je}). "
              f"Übersetzungen: {len(offen) - veraltet} fehlen, {veraltet} veraltet. Karten der Hundezonen: {len(GEO)}.")
        return 0
    anzahl = baue(quellen, orte)
    print(f"Gebaut: {anzahl} Seiten ({kantone} Kantone, {gemeinden} Gemeinden, {len(quellen)} Quellen; {je}). "
          f"Ortssuche: {len(orte['gemeinden'])} Gemeinden, {len(orte['orte'])} Orte mit Postleitzahl.")
    return 0


if __name__ == "__main__":
    try:  # «python3 build.py --fehlend | head» soll ohne Fehlermeldung enden
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    sys.exit(main())
