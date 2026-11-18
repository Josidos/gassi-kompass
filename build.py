#!/usr/bin/env python3
"""Baut gassi-kompass.ch aus den Dateien in data/ (nur Python-Standardbibliothek).

    python3 build.py                      prüft die Daten und schreibt alle Seiten
    python3 build.py --check              prüft nur, schreibt nichts
    python3 build.py --fehlend            listet fehlende und veraltete Übersetzungen auf
    python3 build.py --pruefsumme DATEI   Prüfsumme einer Originalfassung für das Feld 'original'

Erzeugt werden: index.html, 404.html, sitemap.xml, robots.txt, ueber/, schweiz/,
assets/orte.json, thema/<name>/, <kanton>/ und <kanton>/<gemeinde>/, dazu die französischen Seiten
unter fr-ch/ und die italienischen unter it-ch/. Diese Ausgaben nie von Hand ändern:
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
RESERVIERT = {"assets", "data", "tests", "tools", "ueber", "schweiz", "thema", "fr-ch", "it-ch"}
VERGLEICH = [("wald", "Leine im Wald"), ("haft", "Haftpflicht"), ("kurs", "Kurs"),
             ("rassen", "Rassen"), ("steuer", "Hundesteuer"), ("anm", "Anmeldung")]
VERGLEICH_TITEL = {
    "de": [t for _, t in VERGLEICH],
    "fr": ["Laisse en forêt", "Responsabilité civile", "Cours", "Races", "Impôt sur les chiens", "Annonce"],
    "it": ["Guinzaglio nel bosco", "Responsabilità civile", "Corso", "Razze", "Imposta sui cani", "Notifica"],
}
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
GLEICH = {"id", "kanton", "kurz", "bfs", "ton", "saison", "von", "bis"}
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
        "ueb_alt": "Die Originalfassung wurde seither geändert und ist aktueller als diese Übersetzung.",
        "monate": MONATE, "mon3": MON3,
        "wochentage": ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
        "start": "Start", "pfad": "Pfad", "sprachwahl": "Sprache",
        "stempel": "Angaben geprüft am {d}",
        "quelle": "Quelle:", "quellen": "Quellen:",
        "fuss_recht": "<strong>Keine Rechtsberatung.</strong> Massgebend sind Gesetz, Verordnung und die Schilder vor Ort. Gassi-Kompass ist ein privates Projekt und kein Angebot eines Kantons oder einer Gemeinde.",
        "fuss_fehler": "Stimmt etwas nicht oder fehlt etwas? Schreib an {mail}.",
        "betreff": "Hinweis zu ",
        "fuss_quellen": "Angaben auf dieser Seite geprüft am {d}. Quellen:",
        "fussnav": "Fussnavigation",
        "nav_suche": "Ort suchen", "nav_schweiz": "Ganze Schweiz", "nav_vergleich": "Kantone im Vergleich",
        "nav_ueber": "Über diese Seite",
        "kanton_kurz": "Kanton {kurz}",
        "erfasst": "erfasst", "folgt": "folgt",
        "wald_kopf": "Leine im Wald",
        "wald_band": "Leine",
        "wald_gross": "Leinenpflicht im Wald vom {von} bis {bis}",
        "wald_text": "Gilt jedes Jahr {wo}. Ausserhalb dieser Zeit muss dein Hund trotzdem unter Kontrolle bleiben, und Schilder vor Ort gehen vor.",
        "wald_unter": "Markiert: Leinenpflicht im Wald, {von} bis {bis}",
        "wald_aria": "Jahresbalken: Leinenpflicht im Wald vom {von} bis {bis}.",
        "wald_ohne_gross": "Keine Saisonregel im Wald",
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
        "lokal_h2": "Das gilt zusätzlich {in_ort}", "freilauf": "Freilaufzonen",
        "suche": {
            "lade": "Das Ortsverzeichnis wird geladen.",
            "leer": "Kein Ort gefunden. Prüfe die Schreibweise oder gib die Postleitzahl ein.",
            "fehler": "Die Ortssuche lässt sich gerade nicht laden. Wähle unten deinen Kanton.",
            "treffer": "{n} Treffer",
            "viele": "Die ersten {max} von {n} Treffern. Tippe weiter, um einzugrenzen.",
            "kt": "Kanton {name}",
            "gemeinde": "Gemeinde {name}",
            "lokal": "lokale Regeln",
            "kanton": "Regeln des Kantons",
            "bund": "Kanton folgt, Regeln des Bundes",
            "in-de": "auf Deutsch", "in-fr": "auf Französisch", "in-it": "auf Italienisch",
        },
        "suche_label": "Gemeinde, Ort oder Postleitzahl",
        "suche_beispiel": "z. B. Wettingen oder 5430",
        "suche_noscript": "Die Ortssuche braucht JavaScript. Ohne JavaScript wählst du unten deinen Kanton.",
        "start_h1": "Was gilt für deinen Hund hier?",
        "start_lede": "Gib deine Gemeinde oder deine Postleitzahl ein. Du siehst, was dort gilt: die Regeln des Bundes, deines Kantons und, wo es sie gibt, die lokalen Regeln deiner Gemeinde. Zu jeder Angabe findest du die amtliche Quelle.",
        "start_kt_eb": "Kanton wählen", "start_kt_h2": "Alle 26 Kantone",
        "start_kt_p": "Wähle deinen Kanton. Was der Bund für alle Hunde vorschreibt, steht unter <a href=\"/schweiz/\">Ganze Schweiz</a>.",
        "start_gm_eb": "Lokale Regeln", "start_gm_h2": "Gemeinden mit eigener Seite",
        "start_gm_p": "Für diese Gemeinden findest du zusätzlich lokale Angaben, zum Beispiel Hundetaxe, Leinenzonen oder Freilaufzonen.",
        "start_vg_eb": "Umzug", "start_vg_h2": "Kantone im Vergleich",
        "start_vg_p": "Was sich ändert, wenn du mit deinem Hund in einen anderen Kanton ziehst.",
        "vg_kanton": "Kanton",
        "vg_andere": "Weitere Kantone, in einer anderen Sprache:",
        "start_titel": "Hunderegeln Schweiz nach Kanton und Gemeinde | Gassi-Kompass",
        "start_beschr": "Gemeinde oder Postleitzahl eingeben und sehen, was für Hunde gilt: Leinenpflicht, Haftpflicht, Kurse und Hundesteuer. Mit amtlicher Quelle zu jeder Angabe.",
        "kt_h1": "Hunderegeln {im}",
        "kt_lede": "Diese Regeln gelten in allen Gemeinden {des}. Gemeinden können zusätzliche Orte mit Leinenpflicht oder Hundeverbot festlegen.",
        "kt_hinweis": "Für diesen Ort haben wir noch keine lokalen Angaben. Auf dieser Seite stehen die Regeln, die im ganzen {name} gelten. Die Gemeinde kann zusätzliche Regeln haben.",
        "kt_gm_eb": "Gemeinden", "kt_gm_h2": "Lokale Regeln {im}",
        "kt_gm_p": "Fehlt deine Gemeinde, gelten die Regeln auf dieser Seite und die Schilder vor Ort. Weitere Gemeinden kommen laufend dazu.",
        "link_schweiz": "Was zusätzlich in der ganzen Schweiz gilt",
        "link_vergleich": "Mit anderen Kantonen vergleichen",
        "link_suche": "Anderen Ort suchen",
        "kt_titel": "Hunderegeln {im}: Leinenpflicht, Haftpflicht, Hundesteuer | Gassi-Kompass",
        "kt_beschr": "Was für Hunde {im} gilt: Leinenpflicht, Zutrittsverbote, Haftpflicht, Kurse, Hundesteuer und Rassenregeln. Mit amtlicher Quelle zu jeder Angabe.",
        "gm_h1": "Hunderegeln {in_ort}",
        "gm_lede": "Die lokalen Regeln {in_ort} und die Vorschriften {des}, die im ganzen Kanton gelten.",
        "gm_weitere": "Weitere Orte {im}", "gm_uebrige": "Übrige Gemeinden",
        "gm_titel": "Hunderegeln {in_ort}: Leinenpflicht, Hundesteuer, Freilauf | Gassi-Kompass",
        "gm_beschr": "Was für Hunde {in_ort} gilt: lokale Regeln, Leinenpflicht, Hundesteuer und die Vorschriften {des}. Mit amtlicher Quelle zu jeder Angabe.",
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
        "ueb_alt": "La version originale a été modifiée depuis et est plus récente que cette traduction.",
        "monate": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
                   "septembre", "octobre", "novembre", "décembre"],
        "mon3": ["janv", "févr", "mars", "avr", "mai", "juin", "juil", "août", "sept", "oct", "nov", "déc"],
        "wochentage": ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"],
        "start": "Accueil", "pfad": "Fil d'Ariane", "sprachwahl": "Langue",
        "stempel": "Vérifié le {d}",
        "quelle": "Source :", "quellen": "Sources :",
        "fuss_recht": "<strong>Pas un conseil juridique.</strong> Font foi la loi, l'ordonnance et la signalisation sur place. Gassi-Kompass est un projet privé et non une offre d'un canton ou d'une commune.",
        "fuss_fehler": "Une erreur ou un oubli ? Écrivez à {mail}.",
        "betreff": "Remarque sur ",
        "fuss_quellen": "Indications de cette page vérifiées le {d}. Sources :",
        "fussnav": "Navigation de pied de page",
        "nav_suche": "Chercher un lieu", "nav_schweiz": "Toute la Suisse (en allemand)",
        "nav_vergleich": "Les cantons en comparaison", "nav_ueber": "À propos",
        "kanton_kurz": "Canton {kurz}",
        "erfasst": "saisi", "folgt": "à venir",
        "wald_kopf": "Laisse en forêt",
        "wald_band": "Laisse",
        "wald_gross": "Laisse obligatoire en forêt du {von} au {bis}",
        "wald_text": "S'applique chaque année {wo}. En dehors de cette période, votre chien doit tout de même rester sous contrôle, et la signalisation sur place prime.",
        "wald_unter": "En couleur : laisse obligatoire en forêt, du {von} au {bis}",
        "wald_aria": "Barre annuelle : laisse obligatoire en forêt du {von} au {bis}.",
        "wald_ohne_gross": "Pas de période fixe en forêt",
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
        "lokal_h2": "Règles supplémentaires {in_ort}", "freilauf": "Espaces de liberté pour chiens",
        "suche": {
            "lade": "Le répertoire des localités se charge.",
            "leer": "Aucun lieu trouvé. Vérifiez l'orthographe ou saisissez le code postal.",
            "fehler": "La recherche ne peut pas être chargée pour l'instant. Choisissez votre canton ci-dessous.",
            "treffer": "Résultats : {n}",
            "viele": "Les {max} premiers résultats sur {n}. Continuez à taper pour préciser.",
            "kt": "{name} (canton)",
            "gemeinde": "commune : {name}",
            "lokal": "règles locales",
            "kanton": "règles du canton",
            "bund": "canton à venir, règles fédérales (en allemand)",
            "in-de": "en allemand", "in-fr": "en français", "in-it": "en italien",
        },
        "suche_label": "Commune, localité ou code postal",
        "suche_beispiel": "p. ex. Montreux ou 1820",
        "suche_noscript": "La recherche a besoin de JavaScript. Sans JavaScript, choisissez votre canton ci-dessous.",
        "start_h1": "Quelles règles pour votre chien ici ?",
        "start_lede": "Saisissez votre commune ou votre code postal. Vous voyez ce qui s'y applique : les règles de votre canton et, lorsqu'elles existent, les règles locales de votre commune. Chaque indication renvoie à sa source officielle.",
        "start_kt_eb": "Choisir un canton", "start_kt_h2": "Les 26 cantons",
        "start_kt_p": "Choisissez votre canton. Ce qui vaut dans toute la Suisse figure sur la page <a href=\"/schweiz/\" hreflang=\"de-CH\">Ganze Schweiz</a> (en allemand).",
        "start_gm_eb": "Règles locales", "start_gm_h2": "Communes avec leur propre page",
        "start_gm_p": "Pour ces communes, vous trouvez en plus des indications locales, par exemple l'impôt sur les chiens, les lieux où la laisse est obligatoire ou les espaces de liberté.",
        "start_vg_eb": "Déménagement", "start_vg_h2": "Les cantons en comparaison",
        "start_vg_p": "Ce qui change si vous déménagez avec votre chien dans un autre canton.",
        "vg_kanton": "Canton",
        "vg_andere": "Autres cantons, dans une autre langue :",
        "start_titel": "Règles pour les chiens en Suisse par canton et par commune | Gassi-Kompass",
        "start_beschr": "Saisissez une commune ou un code postal et voyez ce qui vaut pour les chiens : laisse obligatoire, assurance responsabilité civile, cours et impôt sur les chiens. Avec la source officielle de chaque indication.",
        "kt_h1": "Règles pour les chiens {im}",
        "kt_lede": "Ces règles valent dans toutes les communes {des}. Les communes peuvent désigner d'autres lieux où la laisse est obligatoire ou les chiens interdits.",
        "kt_hinweis": "Nous n'avons pas encore d'indications locales pour ce lieu. Cette page présente les règles valables partout {im}. La commune peut avoir des règles supplémentaires.",
        "kt_gm_eb": "Communes", "kt_gm_h2": "Règles locales {im}",
        "kt_gm_p": "Si votre commune manque, les règles de cette page et la signalisation sur place s'appliquent. D'autres communes suivent.",
        "link_schweiz": "Ce qui vaut en plus dans toute la Suisse (en allemand)",
        "link_vergleich": "Comparer avec d'autres cantons",
        "link_suche": "Chercher un autre lieu",
        "kt_titel": "Règles pour les chiens {im} : laisse obligatoire, assurance RC, impôt | Gassi-Kompass",
        "kt_beschr": "Ce qui vaut pour les chiens {im} : laisse obligatoire, lieux interdits, assurance responsabilité civile, cours, impôt sur les chiens et races. Avec la source officielle de chaque indication.",
        "gm_h1": "Règles pour les chiens {in_ort}",
        "gm_lede": "Les règles locales {in_ort} et les prescriptions {des}, valables dans tout le canton.",
        "gm_weitere": "Autres lieux {im}", "gm_uebrige": "Autres communes",
        "gm_titel": "Règles pour les chiens {in_ort} : laisse obligatoire, impôt, espaces de liberté | Gassi-Kompass",
        "gm_beschr": "Ce qui vaut pour les chiens {in_ort} : règles locales, laisse obligatoire, impôt sur les chiens et prescriptions {des}. Avec la source officielle de chaque indication.",
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
        "ueb_alt": "La versione originale è stata modificata nel frattempo ed è più recente di questa traduzione.",
        "monate": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
                   "settembre", "ottobre", "novembre", "dicembre"],
        "mon3": ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"],
        "wochentage": ["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"],
        "start": "Inizio", "pfad": "Percorso", "sprachwahl": "Lingua",
        "stempel": "Verificato il {d}",
        "quelle": "Fonte:", "quellen": "Fonti:",
        "fuss_recht": "<strong>Nessuna consulenza legale.</strong> Fanno stato la legge, l'ordinanza e la segnaletica sul posto. Gassi-Kompass è un progetto privato e non un'offerta di un Cantone o di un Comune.",
        "fuss_fehler": "Qualcosa non è corretto o manca? Scrivi a {mail}.",
        "betreff": "Segnalazione su ",
        "fuss_quellen": "Indicazioni di questa pagina verificate il {d}. Fonti:",
        "fussnav": "Navigazione a piè di pagina",
        "nav_suche": "Cerca un luogo", "nav_schweiz": "Tutta la Svizzera (in tedesco)",
        "nav_vergleich": "Cantoni a confronto", "nav_ueber": "Informazioni",
        "kanton_kurz": "Cantone {kurz}",
        "erfasst": "registrato", "folgt": "in arrivo",
        "wald_kopf": "Guinzaglio nel bosco",
        "wald_band": "Guinzaglio",
        "wald_gross": "Obbligo di guinzaglio nel bosco {dal_von} {al_bis}",
        "wald_text": "Vale ogni anno {wo}. Fuori da questo periodo il tuo cane deve comunque restare sotto controllo, e la segnaletica sul posto ha la precedenza.",
        "wald_unter": "Evidenziato: obbligo di guinzaglio nel bosco, {dal_von} {al_bis}",
        "wald_aria": "Barra annuale: obbligo di guinzaglio nel bosco {dal_von} {al_bis}.",
        "wald_ohne_gross": "Nessun periodo fisso nel bosco",
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
        "lokal_h2": "Regole supplementari {in_ort}", "freilauf": "Aree di svago per cani",
        "suche": {
            "lade": "L'elenco delle località è in caricamento.",
            "leer": "Nessun luogo trovato. Controlla l'ortografia o inserisci il numero postale di avviamento.",
            "fehler": "La ricerca non può essere caricata in questo momento. Scegli il tuo Cantone qui sotto.",
            "treffer": "Risultati: {n}",
            "viele": "I primi {max} risultati su {n}. Continua a scrivere per restringere.",
            "kt": "{name} (Cantone)",
            "gemeinde": "Comune di {name}",
            "lokal": "regole locali",
            "kanton": "regole del Cantone",
            "bund": "Cantone in arrivo, regole federali (in tedesco)",
            "in-de": "in tedesco", "in-fr": "in francese", "in-it": "in italiano",
        },
        "suche_label": "Comune, località o numero postale di avviamento",
        "suche_beispiel": "p. es. Mendrisio o 6850",
        "suche_noscript": "La ricerca ha bisogno di JavaScript. Senza JavaScript scegli il tuo Cantone qui sotto.",
        "start_h1": "Cosa vale qui per il tuo cane?",
        "start_lede": "Inserisci il tuo Comune o il numero postale di avviamento. Vedi cosa vale lì: le regole del tuo Cantone e, dove esistono, le regole locali del tuo Comune. Per ogni indicazione trovi la fonte ufficiale.",
        "start_kt_eb": "Scegli il Cantone", "start_kt_h2": "Tutti i 26 Cantoni",
        "start_kt_p": "Scegli il tuo Cantone. Cosa vale in tutta la Svizzera si trova sulla pagina <a href=\"/schweiz/\" hreflang=\"de-CH\">Ganze Schweiz</a> (in tedesco).",
        "start_gm_eb": "Regole locali", "start_gm_h2": "Comuni con una pagina propria",
        "start_gm_p": "Per questi Comuni trovi anche indicazioni locali, per esempio l'imposta sui cani, i luoghi con obbligo di guinzaglio o le aree di svago per cani.",
        "start_vg_eb": "Trasloco", "start_vg_h2": "Cantoni a confronto",
        "start_vg_p": "Cosa cambia se ti trasferisci con il tuo cane in un altro Cantone.",
        "vg_kanton": "Cantone",
        "vg_andere": "Altri Cantoni, in un'altra lingua:",
        "start_titel": "Regole per i cani in Svizzera per Cantone e Comune | Gassi-Kompass",
        "start_beschr": "Inserisci un Comune o un numero postale di avviamento e vedi cosa vale per i cani: obbligo di guinzaglio, responsabilità civile, corsi e imposta sui cani. Con la fonte ufficiale per ogni indicazione.",
        "kt_h1": "Regole per i cani {im}",
        "kt_lede": "Queste regole valgono in tutti i Comuni {des}. I Comuni possono stabilire altri luoghi con obbligo di guinzaglio o divieto per i cani.",
        "kt_hinweis": "Per questo luogo non abbiamo ancora indicazioni locali. Questa pagina riporta le regole che valgono ovunque {im}. Il Comune può avere regole supplementari.",
        "kt_gm_eb": "Comuni", "kt_gm_h2": "Regole locali {im}",
        "kt_gm_p": "Se il tuo Comune manca, valgono le regole di questa pagina e la segnaletica sul posto. Altri Comuni seguiranno.",
        "link_schweiz": "Cosa vale in più in tutta la Svizzera (in tedesco)",
        "link_vergleich": "Confronta con altri Cantoni",
        "link_suche": "Cerca un altro luogo",
        "kt_titel": "Regole per i cani {im}: obbligo di guinzaglio, responsabilità civile, imposta | Gassi-Kompass",
        "kt_beschr": "Cosa vale per i cani {im}: obbligo di guinzaglio, luoghi vietati, responsabilità civile, corsi, imposta sui cani e razze. Con la fonte ufficiale per ogni indicazione.",
        "gm_h1": "Regole per i cani {in_ort}",
        "gm_lede": "Le regole locali {in_ort} e le prescrizioni {des}, che valgono in tutto il Cantone.",
        "gm_weitere": "Altri luoghi {im}", "gm_uebrige": "Altri Comuni",
        "gm_titel": "Regole per i cani {in_ort}: obbligo di guinzaglio, imposta, aree per cani | Gassi-Kompass",
        "gm_beschr": "Cosa vale per i cani {in_ort}: regole locali, obbligo di guinzaglio, imposta sui cani e prescrizioni {des}. Con la fonte ufficiale per ogni indicazione.",
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

LANG = "de"       # Sprache der Seite, die gerade entsteht. Wird mit sprache() gesetzt.
S = TEXTE["de"]   # Texte dieser Sprache
W = {}            # Daten je Sprache: {"de": {"k": [Kantone], "g": [Gemeinden]}, ...}


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
    bund = lies(DATA / "schweiz.json")
    orte = json.loads((DATA / "orte.json").read_text("utf-8"))
    return quellen, welt, bund, orte


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


def k_ziel(kid):
    """Beste Fassung des Kantons für die Sprache der Seite: (Sprache, Adresse) oder None."""
    da = k_sprachen(kid)
    if not da:
        return None
    lang = LANG if LANG in da else da[0]
    return lang, k_pfad(lang, kid)


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
    monate = "".join(f"<span>{m}</span>" for m in S["mon3"])
    # Texte für assets/heute.js: Datum, Markierung «heute» und der Tagesstatus in der Sprache der Seite
    js = {key: S["heute"][key] for key in ("heute", "datum", "punkt", "erster")}
    js["mon"], js["wt"] = S["monate"], S["wochentage"]
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
    else:
        band, attrs = "", ' data-saison="0"'
        gross, text = S["wald_ohne_gross"], w["text"]
        unter = S["wald_ohne_unter"].format(im=k["im"])
        aria = S["wald_ohne_aria"]
    attrs += f' data-texte="{e(json.dumps(js, ensure_ascii=False, separators=(",", ":")))}"'
    note = f'<p class="today-note">{e(hinweis)}</p>' if hinweis else ""
    return (f'<section class="today" data-wald{attrs}>'
            f'<div class="today-head"><span class="eyebrow">{S["wald_kopf"]} · {e(k["name"])}</span>'
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
            f'<h2>{S["regeln_h2"]}</h2></div><div class="split">'
            f'<div class="list-card leash"><h3><span class="chip must">{S["leine_chip"]}</span>{S["leine_h3"]}</h3>'
            f'<ul>{li(k["leine"]["punkte"])}</ul>{qlinks(k["leine"]["quellen"], Q, benutzt)}</div>'
            f'<div class="list-card"><h3><span class="chip none">{S["verbot_chip"]}</span>{S["verbot_h3"]}</h3>'
            f'{lead}<ul>{li(k["verbot"]["punkte"])}</ul>{qlinks(k["verbot"]["quellen"], Q, benutzt)}</div>'
            '</div></section>')


def pflichten(k, Q, benutzt):
    karten = "".join(karte(c, Q, benutzt) for c in k["karten"])
    umzug = ""
    if k.get("umzug"):
        umzug = (f'<div class="callout"><p><strong>{e(S["umzug"].format(name=k["name"], im=k["im"]))}</strong> '
                 f'{e(k["umzug"]["text"])}</p>{qlinks(k["umzug"]["quellen"], Q, benutzt)}</div>')
    return (f'<section class="sec"><div class="sec-head"><span class="eyebrow">{e(k["name"])}</span>'
            f'<h2>{S["pflichten_h2"]}</h2></div><div class="cards">{karten}</div>{umzug}</section>')


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
        zonen = (f'<h3 class="sub">{S["freilauf"]}</h3><div class="zones">{"".join(teile)}</div>'
                 f'{qlinks(g["freilaufzonen_quellen"], Q, benutzt)}')
    karten = "".join(karte(c, Q, benutzt) for c in g["karten"])
    return (f'<section class="sec"><div class="sec-head"><span class="eyebrow">{e(g["name"])}</span>'
            f'<h2>{e(S["lokal_h2"].format(in_ort=g["in_ort"]))}</h2>{intro}</div>{zonen}'
            f'<div class="cards">{karten}</div></section>')


def hinweis_uebersetzung(d, art):
    """Hinweis unter dem Titel einer übersetzten Seite, mit Link zur Originalfassung. art: 'k' oder 'g'."""
    aus = d.get("uebersetzt_aus")
    if not aus:
        return ""
    ziel = k_pfad(aus, d["id"]) if art == "k" else g_pfad(aus, d)
    alt = f' <strong>{S["ueb_alt"]}</strong>' if d.get("_veraltet") else ""
    return (f'<p class="transl" data-uebersetzung>{S["ueb"][aus]}{alt} '
            f'<a href="{ziel}" hreflang="{HTMLLANG[aus]}">{S["ueb_link"][aus]}</a></p>')


def tafel(href, name, unter, aktiv=False, klasse=""):
    cur = ' aria-current="page"' if aktiv else ""
    art = f"dest {klasse}".strip()
    return (f'<a class="{art}" href="{href}"{cur}>'
            f'<span class="dest-name">{e(name)}</span><span class="dest-sub">{e(unter)}</span></a>')


def gemeinde_tafeln(kid, ohne=None):
    """Tafeln zu den Gemeinden eines Kantons: zuerst die Seiten in der Sprache der Seite, dann
    Gemeinden, die es nur in einer anderen Sprache gibt, mit Angabe der Sprache.
    ohne: BFS-Nummer der Gemeinde, auf deren Seite die Tafeln stehen."""
    unter = S["kanton_kurz"].format(kurz=kid.upper())
    teile, da = [], set()
    for lang in [LANG] + [l for l in SPRACHEN if l != LANG]:
        for g in W[lang]["g"]:
            if g["kanton"] != kid or g["bfs"] in da:
                continue
            da.add(g["bfs"])
            if g["bfs"] != ohne:
                teile.append(tafel(g_pfad(lang, g), g["name"],
                                   unter if lang == LANG else f'{unter} · {S["sprache"][lang]}'))
    return "".join(teile)


def suche():
    """Suchfeld für Gemeinde, Ort, Postleitzahl oder Kanton. Ohne Skript bleibt es unsichtbar.
    Alle Texte stehen in TEXTE, assets/suche.js kennt keine Sprache."""
    attrs = "".join(f' data-{k}="{e(v)}"' for k, v in S["suche"].items())
    return (f'<div class="search" data-suche data-lang="{LANG}"{attrs} hidden>'
            f'<label for="ortssuche">{S["suche_label"]}</label>'
            '<input id="ortssuche" type="search" autocomplete="off" enterkeyhint="search" '
            f'placeholder="{S["suche_beispiel"]}" aria-describedby="such-status">'
            '<p class="search-status" id="such-status" role="status"></p>'
            '<div class="plates" id="treffer"></div></div>'
            f'<noscript><p>{S["suche_noscript"]}</p></noscript>')


def kantonsraster():
    """Alle 26 Kantone: erfasste führen zur Kantonsseite (wenn es sie in der Sprache der Seite nicht
    gibt, zur Fassung in der anderen Sprache, mit Angabe der Sprache), die übrigen zu den Regeln des Bundes."""
    namen = KANTONSNAMEN[LANG]
    reihe = KANTONE_ALLE if LANG == "de" else sorted(KANTONE_ALLE, key=lambda x: ohne_akzent(namen[x[0]]))
    teile = []
    for kid, _ in reihe:
        ziel = k_ziel(kid)
        if ziel:
            unter = kid.upper()
            if ziel[0] != LANG:
                unter += f' · {S["sprache"][ziel[0]]}'
            teile.append(tafel(ziel[1], namen[kid], unter, klasse="ok"))
        else:
            teile.append(tafel(f"/schweiz/#kt={kid}", namen[kid], f'{kid.upper()} · {S["folgt"]}', klasse="wait"))
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


def themenleiste(ohne=None):
    """Tafeln zu den Themenseiten. ohne: id der Seite, auf der die Leiste steht."""
    return ('<div class="plates small">'
            + "".join(tafel(f'/thema/{t["id"]}/', t["name"], "alle Kantone") for t in THEMEN if t["id"] != ohne)
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


def vergleich():
    kantone = W[LANG]["k"]
    thema = {t["key"]: t["id"] for t in THEMEN}
    if LANG == "de":  # Themenseiten gibt es vorerst nur auf Deutsch
        kopf = "".join(f'<th scope="col"><a href="/thema/{thema[key]}/">{e(t)}</a></th>' for key, t in VERGLEICH)
    else:
        kopf = "".join(f'<th scope="col">{e(t)}</th>' for t in VERGLEICH_TITEL[LANG])
    zeilen = []
    for k in kantone:
        zellen = "".join(f'<td>{e(k["vergleich"][key])}</td>' for key, _ in VERGLEICH)
        zeilen.append(f'<tr><th scope="row"><a href="{k_pfad(LANG, k["id"])}">{e(k["name"])}</a></th>{zellen}</tr>')
    return (f'<div class="table-wrap"><table class="wide"><thead><tr><th scope="col">{S["vg_kanton"]}</th>'
            f'{kopf}</tr></thead><tbody>{"".join(zeilen)}</tbody></table></div>'
            f'{andere_kantone(S["vg_andere"])}')


def seite(pfad, titel, beschr, inhalt, krumen, stand, benutzt, Q, index=True, alt=None):
    """pfad: Adresse ab Wurzel, z. B. '/zh/zuerich/'. krumen: Liste (Name, Pfad).
    alt: {Sprache: Adresse} aller Sprachfassungen dieser Seite, die eigene eingeschlossen."""
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
        quellen = f'<p>{S["fuss_quellen"].format(d=de_datum(stand))}</p><ol>{punkte}</ol>'
    robots = "" if index else '<meta name="robots" content="noindex">\n'
    mail = f'<a href="mailto:{KONTAKT}?subject={quote(S["betreff"] + pfad)}">{KONTAKT}</a>'
    return f"""<!doctype html>
<html lang="{HTMLLANG[LANG]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschr)}">
{robots}<link rel="canonical" href="{SITE}{pfad}">
{hreflang}<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschr)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{pfad}">
<meta property="og:locale" content="{HTMLLANG[LANG].replace("-", "_")}">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
{ld}
</head>
<body>
<div class="wrap">
<header class="top"><a class="brand" href="{start}">Gassi-Kompass</a>{stempel}</header>
{inhalt.replace("<!--KRUMEN-->", crumbs)}
<footer class="foot">
<p>{S["fuss_recht"]}</p>
<p>{S["fuss_fehler"].format(mail=mail)}</p>
{quellen}
<nav aria-label="{S["fussnav"]}"><a href="{start}">{S["nav_suche"]}</a><a href="/schweiz/">{S["nav_schweiz"]}</a><a href="{start}#vergleich">{S["nav_vergleich"]}</a><a href="{start}ueber/">{S["nav_ueber"]}</a></nav>
</footer>
</div>
<script src="/assets/heute.js" defer></script>
<script src="/assets/suche.js" defer></script>
</body>
</html>
"""


# --------------------------------------------------------------------- Seiten

def startseiten():
    """Adressen der Startseiten: Deutsch immer, die anderen Sprachen ab dem ersten Kanton."""
    return {l: PRAEFIX[l] + "/" for l in SPRACHEN if l == "de" or W[l]["k"]}


def seite_start(Q, bund):
    kantone = W[LANG]["k"]
    start = PRAEFIX[LANG] + "/"
    gruppen = []
    for k in kantone:
        tafeln = gemeinde_tafeln(k["id"])
        if tafeln:
            gruppen.append(f'<div class="group"><h3><a href="{k_pfad(LANG, k["id"])}">{e(k["name"])}</a></h3>'
                           f'<div class="plates">{tafeln}</div></div>')
    for kid in erfasste():  # Kantone, die es nur in einer anderen Sprache gibt
        lang, pfad = k_ziel(kid)
        tafeln = gemeinde_tafeln(kid) if lang != LANG else ""
        if tafeln:
            gruppen.append(f'<div class="group"><h3><a href="{pfad}" hreflang="{HTMLLANG[lang]}">'
                           f'{e(KANTONSNAMEN[LANG][kid])}</a> ({S["sprache"][lang]})</h3>'
                           f'<div class="plates">{tafeln}</div></div>')
    stand = min([k["geprueft"] for k in kantone] + ([bund["geprueft"]] if LANG == "de" else []))
    themen = f'\n<h3 class="sub">Ein Thema, alle Kantone</h3>\n{themenleiste()}' if LANG == "de" else ""
    inhalt = f"""<section class="hero">
<h1>{S["start_h1"]}</h1>
<p class="lede">{S["start_lede"]}</p>
{suche()}
</section>
<section class="sec" id="orte">
<div class="sec-head"><span class="eyebrow">{S["start_kt_eb"]}</span><h2>{S["start_kt_h2"]}</h2><p>{S["start_kt_p"].format(n=len(erfasste()))}</p></div>
{kantonsraster()}
</section>
<section class="sec" id="gemeinden">
<div class="sec-head"><span class="eyebrow">{S["start_gm_eb"]}</span><h2>{S["start_gm_h2"]}</h2><p>{S["start_gm_p"]}</p></div>
{"".join(gruppen)}
</section>
<section class="sec" id="vergleich">
<div class="sec-head"><span class="eyebrow">{S["start_vg_eb"]}</span><h2>{S["start_vg_h2"]}</h2><p>{S["start_vg_p"]}</p></div>
{vergleich()}{themen}
</section>"""
    return seite(start, S["start_titel"], S["start_beschr"], inhalt, None, stand, [], Q, alt=startseiten())


def seite_schweiz(bund, Q):
    benutzt = []
    karten = "".join(karte(c, Q, benutzt) for c in bund["karten"])
    da = erfasste()
    offen = json.dumps({kid: name for kid, name in KANTONE_ALLE if kid not in da}, ensure_ascii=False)
    hinweis = (f'<p class="callout" data-ort-hinweis data-kantone="{e(offen)}" data-text="Der Kanton '
               '{kanton} hat noch keine eigene Seite. Auf dieser Seite steht, was in der ganzen Schweiz gilt. '
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
<div class="sec-head"><span class="eyebrow">Kanton wählen</span><h2>Dazu kommt dein Kanton</h2><p>Leinenpflicht, Haftpflicht, Kurse und Rasselisten regelt dein Kanton. Wähle ihn aus.</p></div>
{kantonsraster()}
<p><a class="text-link" href="/">Gemeinde oder Postleitzahl suchen</a></p>
</section>"""
    return seite("/schweiz/", "Hunderegeln Schweiz: Was in allen Kantonen gilt | Gassi-Kompass",
                 "Was der Bund für alle Hunde in der Schweiz vorschreibt: Mikrochip, AMICUS, Anmeldung, "
                 "Hundesteuer, Haltung und verbotene Hilfsmittel. Mit amtlicher Quelle zu jeder Angabe.",
                 inhalt, [("Start", "/"), ("Ganze Schweiz", "/schweiz/")], bund["geprueft"], benutzt, Q)


def seite_kanton(k, Q):
    benutzt = []
    start = PRAEFIX[LANG] + "/"
    pfad = k_pfad(LANG, k["id"])
    tafeln = gemeinde_tafeln(k["id"])
    orte = (f'<div class="plates">{tafeln}</div>' if tafeln else "")
    f = {"im": k["im"], "des": k["des"], "name": k["name"]}
    themen = """
<section class="sec">
<div class="sec-head"><span class="eyebrow">Vergleich</span><h2>Ein Thema, alle Kantone</h2><p>So regeln es die anderen Kantone.</p></div>
""" + themenleiste() + "\n</section>" if LANG == "de" else ""
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>{e(S["kt_h1"].format(**f))}</h1>
<p class="lede">{e(S["kt_lede"].format(**f))}</p>
{hinweis_uebersetzung(k, "k")}
<p class="callout" data-ort-hinweis data-text="{e(S["kt_hinweis"].format(**f))}" hidden></p>
</section>
{wald(k, Q, benutzt)}
{regeln(k, Q, benutzt)}
{pflichten(k, Q, benutzt)}
<section class="sec">
<div class="sec-head"><span class="eyebrow">{S["kt_gm_eb"]}</span><h2>{e(S["kt_gm_h2"].format(**f))}</h2><p>{S["kt_gm_p"]}</p></div>
{orte}
<p><a class="text-link" href="/schweiz/">{S["link_schweiz"]}</a></p>
<p><a class="text-link" href="{start}#vergleich">{S["link_vergleich"]}</a></p>
<p><a class="text-link" href="{start}">{S["link_suche"]}</a></p>
</section>{themen}"""
    return seite(pfad, S["kt_titel"].format(**f), S["kt_beschr"].format(**f),
                 inhalt, [(S["start"], start), (k["name"], pfad)], k["geprueft"], benutzt, Q,
                 alt={l: k_pfad(l, k["id"]) for l in k_sprachen(k["id"])})


def seite_gemeinde(g, k, Q):
    benutzt = []
    start = PRAEFIX[LANG] + "/"
    andere = gemeinde_tafeln(k["id"], ohne=g["bfs"])
    andere += tafel(k_pfad(LANG, k["id"]), S["gm_uebrige"], k["name"])
    stand = min(g["geprueft"], k["geprueft"])
    f = {"in_ort": g["in_ort"], "im": k["im"], "des": k["des"]}
    inhalt = f"""<section class="hero"><!--KRUMEN-->
<h1>{e(S["gm_h1"].format(**f))}</h1>
<p class="lede">{e(S["gm_lede"].format(**f))}</p>
{hinweis_uebersetzung(g, "g")}
</section>
{wald(k, Q, benutzt, g.get("hinweis_heute"))}
{lokal(g, Q, benutzt)}
{regeln(k, Q, benutzt)}
{pflichten(k, Q, benutzt)}
<section class="sec">
<div class="sec-head"><span class="eyebrow">{e(k["name"])}</span><h2>{e(S["gm_weitere"].format(**f))}</h2></div>
<div class="plates">{andere}</div>
<p><a class="text-link" href="/schweiz/">{S["link_schweiz"]}</a></p>
<p><a class="text-link" href="{start}">{S["link_suche"]}</a></p>
</section>"""
    pfad = g_pfad(LANG, g)
    return seite(pfad, S["gm_titel"].format(**f), S["gm_beschr"].format(**f),
                 inhalt, [(S["start"], start), (k["name"], k_pfad(LANG, k["id"])), (g["name"], pfad)],
                 stand, benutzt, Q, alt=g_sprachen(g["bfs"]))


def seite_thema(t, Q):
    """Vergleich aller Kantone mit deutscher Fassung zu einem Thema. Alle Angaben stammen aus den
    Kantonsdateien, nichts wird übersetzt. Kantone ohne deutsche Fassung stehen in einer Zeile darunter."""
    benutzt = []
    kantone = W["de"]["k"]
    n = len(kantone)
    alle = len(erfasste())

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
            zahl += " Bei den übrigen gelten andere Regeln, zum Beispiel eine Leinenpflicht das ganze Jahr oder Regeln der Gemeinden. Sie stehen beim Kanton."
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
    rest = (f" Die übrigen {26 - alle} folgen." if alle < 25 else " Der letzte folgt." if alle == 25 else "")
    if alle > n:
        rest = f"Diese Seite vergleicht {n} Kantone. Die übrigen findest du weiter unten."
    pfad = f'/thema/{t["id"]}/'
    inhalt = f"""<section class="hero thema"><!--KRUMEN-->
<h1>{e(t["name"])}: alle Kantone im Vergleich</h1>
<p class="lede">{rest} {e(zahl)} Was der Bund für alle Hunde vorschreibt, steht unter <a href="/schweiz/">Ganze Schweiz</a>.</p>
</section>
<section class="sec">
<div class="sec-head"><span class="eyebrow">Überblick</span><h2>{e(t["spalte"])} nach Kanton</h2></div>
<div class="table-wrap"><table><thead><tr><th scope="col">Kanton</th><th scope="col">Kurz</th><th scope="col">{e(t["spalte"])}</th></tr></thead><tbody>{"".join(zeilen)}</tbody></table></div>
{andere_kantone("Weitere Kantone, auf ihrer Seite in der Sprache des Kantons:")}
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
    return seite(f"{start}ueber/", u["titel"], u["beschr"],
                 inhalt, [(S["start"], start), (S["nav_ueber"], f"{start}ueber/")], None, [], Q,
                 alt={l: p + "ueber/" for l, p in startseiten().items()})


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
    ziel = ROOT / rel.lstrip("/")
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, "utf-8")


def baue(Q, bund, orte):
    for ordner in ROOT.iterdir():
        if ordner.is_dir() and (ordner / MARKE).exists():
            shutil.rmtree(ordner)
    urls = []
    for lang in SPRACHEN:
        kantone, gemeinden = W[lang]["k"], W[lang]["g"]
        if lang != "de" and not kantone:
            continue  # Startseite und «Über diese Seite» erst ab dem ersten Kanton in dieser Sprache
        sprache(lang)
        start = PRAEFIX[lang] + "/"
        nach_id = {k["id"]: k for k in kantone}
        urls.append((start, min([k["geprueft"] for k in kantone] + ([bund["geprueft"]] if lang == "de" else []))))
        urls.append((f"{start}ueber/", None))
        schreibe(f"{start}index.html", seite_start(Q, bund))
        schreibe(f"{start}ueber/index.html", seite_ueber(Q))
        if lang == "de":
            urls.append(("/schweiz/", bund["geprueft"]))
            schreibe("404.html", seite_404(Q))
            schreibe(f"ueber/{MARKE}", "")
            schreibe("schweiz/index.html", seite_schweiz(bund, Q))
            schreibe(f"schweiz/{MARKE}", "")
            schreibe(f"thema/{MARKE}", "")
            for t in THEMEN:
                schreibe(f'thema/{t["id"]}/index.html', seite_thema(t, Q))
                urls.append((f'/thema/{t["id"]}/', min(k["geprueft"] for k in kantone)))
        else:
            schreibe(f"{start}{MARKE}", "")  # der ganze Sprachordner wird beim Neubau ersetzt
        for k in kantone:
            schreibe(f'{k_pfad(lang, k["id"])}index.html', seite_kanton(k, Q))
            if lang == "de":
                schreibe(f'{k["id"]}/{MARKE}', "")
            urls.append((k_pfad(lang, k["id"]), k["geprueft"]))
        for g in gemeinden:
            k = nach_id[g["kanton"]]
            schreibe(f"{g_pfad(lang, g)}index.html", seite_gemeinde(g, k, Q))
            urls.append((g_pfad(lang, g), min(g["geprueft"], k["geprueft"])))
    sprache("de")
    schreibe("assets/orte.json", ortsindex(orte))
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
    if "--pruefsumme" in sys.argv:
        dateien = [a for a in sys.argv[1:] if not a.startswith("--")]
        for a in dateien:
            print(pruefsumme(json.loads(Path(a).read_text("utf-8"))), a)
        if not dateien:
            print("Aufruf: python3 build.py --pruefsumme data/kantone/zh.json")
        return 0 if dateien else 1
    quellen, welt, bund, orte = lade()
    fehler = pruefe(quellen, welt, bund, orte)
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

    sammle(welt)
    sammle(bund)
    benutzt.add("ch_swisstopo_orte")  # steht auf der Seite «Über diese Seite»
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
              f"Übersetzungen: {len(offen) - veraltet} fehlen, {veraltet} veraltet.")
        return 0
    anzahl = baue(quellen, bund, orte)
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
