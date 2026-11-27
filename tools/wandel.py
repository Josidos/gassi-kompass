#!/usr/bin/env python3
"""Änderungswächter: merkt, welche Quelle sich seit dem letzten Abruf geändert hat.

Läuft in der GitHub Action «Quellen auf Änderungen prüfen» (.github/workflows/wandel.yml),
jeden Montag früh. Der Stand liegt nicht auf `main`, sondern auf dem Zweig `wandel` in der
Datei `wandel.json`. Kostet kein Guthaben: kein Modell, nur Abrufe und Prüfsummen.

Aufrufe:
  python3 tools/wandel.py <stand.json>     ruft alle Quellen ab und schreibt den Stand nach <stand.json>
  python3 tools/wandel.py --faellig        für den Lauf: welche Originalfassung ist nachzuprüfen?
  python3 tools/wandel.py --faellig --stand <stand.json>   dasselbe mit einem Stand aus einer Datei
  python3 tools/wandel.py --text <Schlüssel>                 druckt den Text eines Erlasses vom Zweig
  python3 tools/wandel.py --text <Schlüssel> --suche <Wort>  nur die Paragrafen mit diesem Wort

Was eine Prüfsumme ist:
  HTML    der sichtbare Text ohne script, style, nav, header, footer, Formulare (und noscript,
          svg, template), Leerraum zusammengefasst
  Erlass  Adressen der Form https://<Server>/app/<Sprache>/texts_of_law/<Nummer> (LexWork, clex,
          tlex): Die Seite selbst ist ein leerer Rahmen. Das Programm holt stattdessen
          /api/<Sprache>/texts_of_law/<Nummer> (JSON) und bildet die Prüfsumme über den Stand
          (version_dates_str) und den sichtbaren Text (xhtml_tol). Den Text legt die Action auf den
          Zweig `wandel` als texte/<Schlüssel>.txt: Titel, Stand, Tag des Abrufs, dann eine Zeile je
          Absatz. Geht das nicht, gilt die Seite wie jede andere, mit der Zeile «OHNE TEXT».
  sonst   die Bytes der Datei (PDF, Word)
  Eine Webseite mit weniger als 200 Zeichen sichtbarem Text heisst «LEER»: Für sie ist der
  Wächter blind.
  Übersicht (Feld `uebersicht` einer Quelle): die sortierte Liste der Adressen, die die Seite
          ausserhalb von Kopf, Fuss und Navigation verlinkt. Ändert sich die Liste, hat das Amt
          wahrscheinlich ein Dokument ersetzt (Neuenburg, 21. Oktober 2026: neues Reglement,
          das alte PDF blieb unverändert online).

Eine Änderung zählt nur, wenn es schon eine Prüfsumme für dieselbe Adresse gab und die neue
anders ist. Antwortet eine Adresse nicht, bleibt der Eintrag, wie er ist. Das Programm endet
beim Abrufen immer ohne Fehler, damit die Action nie rot wird.
"""
import concurrent.futures
import datetime
import glob
import hashlib
import html.parser
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from links import AGENT  # noqa: E402  dieselbe Kennung wie die Link-Prüfung

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KOPF = {
    "User-Agent": AGENT,
    "Accept": "text/html,application/pdf,*/*;q=0.8",
    "Accept-Language": "de-CH,de;q=0.9,fr;q=0.8,it;q=0.7",
}
ZEIT = 30                    # Sekunden je Abruf, wie tools/links.py
GROESSTE = 40 * 1024 * 1024  # mehr Bytes liest das Programm nicht
UNRUHIG = 3                  # mehr Änderungen als das in UNRUHIG_TAGE gilt als unruhig
UNRUHIG_TAGE = 28
MIN_TEXT = 200              # weniger sichtbarer Text: Seite gilt als LEER, der Wächter ist blind
FRISCH_TAGE = 8              # so alt darf ein Text vom Zweig sein, um als im Lauf abgerufen zu gelten
ERLASS = re.compile(r"^(https?://[^/?#]+)/app/([a-z]{2})/texts_of_law/([^/?#]+)")
KOPF_PARAGRAF = re.compile(r"^(§+|Art\.?|Artikel|Article|Articolo)\s*\d+[a-z]*\.?$", re.I)
BEHALTEN = 12                # so viele Daten von Änderungen bleiben je Eintrag stehen
WEG = {"script", "style", "nav", "header", "footer", "form", "noscript", "svg", "template"}
LEER = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param",
        "source", "track", "wbr"}
_sperren = {}
_sperren_lock = threading.Lock()


def quellen():
    """Alle Quellen als {Schlüssel: {"url", "uebersicht"?}}."""
    alle = {}
    dateien = [os.path.join(WURZEL, "data", "quellen.json")]
    dateien += sorted(glob.glob(os.path.join(WURZEL, "data", "quellen", "*.json")))
    for datei in dateien:
        with open(datei, encoding="utf-8") as f:
            for key, q in json.load(f).items():
                alle[key] = {"url": q["url"]}
                if q.get("uebersicht"):
                    alle[key]["uebersicht"] = q["uebersicht"]
    return alle


class Leser(html.parser.HTMLParser):
    """Sammelt den sichtbaren Text und die Links ausserhalb der Teile in WEG."""

    def __init__(self, basis):
        super().__init__(convert_charrefs=True)
        self.basis = basis
        self.stapel = []
        self.text = []
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag in LEER:
            if tag == "br":
                self.text.append(" ")
            return
        self.stapel.append(tag)
        if tag == "a" and not (WEG & set(self.stapel)):
            href = dict(attrs).get("href") or ""
            if href and not href.startswith(("#", "mailto:", "tel:", "javascript:")):
                ziel = urllib.parse.urljoin(self.basis, href.strip())
                self.links.add(urllib.parse.urldefrag(ziel)[0])

    def handle_endtag(self, tag):
        if tag in self.stapel:  # unsauberes HTML: bis zum passenden Tag zurück
            while self.stapel:
                if self.stapel.pop() == tag:
                    break
        self.text.append(" ")

    def handle_data(self, data):
        if not (WEG & set(self.stapel)):
            self.text.append(data)


def lies_html(roh, zeichensatz, basis):
    leser = Leser(basis)
    try:
        leser.feed(roh.decode(zeichensatz or "utf-8", "replace"))
        leser.close()
    except Exception:
        pass
    text = re.sub(r"\s+", " ", "".join(leser.text)).strip()
    return text, sorted(leser.links)


def summe(daten):
    if isinstance(daten, str):
        daten = daten.encode("utf-8")
    return hashlib.sha256(daten).hexdigest()[:20]


def sperre(host):
    with _sperren_lock:
        return _sperren.setdefault(host, threading.Semaphore(2))


def hole(url, accept=None):
    """Gibt (Bytes, Inhaltsart, Zeichensatz, Zieladresse) zurück oder wirft eine Ausnahme."""
    sauber = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~")
    kopf = dict(KOPF, Accept=accept) if accept else KOPF
    req = urllib.request.Request(sauber, headers=kopf)
    with urllib.request.urlopen(req, timeout=ZEIT) as r:
        return r.read(GROESSTE), r.headers.get_content_type(), r.headers.get_content_charset(), r.geturl()


class ErlassLeser(html.parser.HTMLParser):
    """Macht aus xhtml_tol einer Gesetzessammlung Zeilen: eine je Block (Absatz, Titel,
    Paragrafennummer). Fussnotenzeichen und Änderungssterne fallen weg."""

    BLOCK = {"div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "table", "ul", "ol", "dt", "dd"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.zeilen = []
        self.jetzt = []
        self.stapel = []
        self.still = 0

    def neue_zeile(self):
        z = re.sub(r"\s+", " ", "".join(self.jetzt)).strip()
        z = re.sub(r"(?:^|\s)\*(?=\s|$)", "", z).strip()
        if z:
            self.zeilen.append(z)
        self.jetzt = []

    def handle_starttag(self, tag, attrs):
        klasse = dict(attrs).get("class") or ""
        if tag == "br":
            self.neue_zeile()
            return
        if tag in LEER:
            return
        still = tag in ("script", "style") or (tag == "a" and "footnote" in klasse.split())
        self.stapel.append((tag, still, "number" in klasse.split()))
        if still:
            self.still += 1
        if tag in self.BLOCK:
            self.neue_zeile()
        elif tag in ("td", "th"):
            self.jetzt.append(" ")

    def handle_endtag(self, tag):
        if tag in LEER:
            return
        nummer = False
        while self.stapel:
            t, still, nummer = self.stapel.pop()
            if still:
                self.still -= 1
            if t == tag:
                break
        if tag in self.BLOCK:
            self.neue_zeile()
        else:
            self.jetzt.append(" " if tag in ("p", "td", "th") or nummer else "")

    def handle_data(self, data):
        if not self.still:
            self.jetzt.append(data)


def erlass_zeilen(xhtml):
    leser = ErlassLeser()
    leser.feed(xhtml)
    leser.close()
    leser.neue_zeile()
    return leser.zeilen


def abruf_erlass(url):
    """Holt den Text eines Erlasses über die Schnittstelle der Sammlung.
    Gibt {"summe", "art": "erlass", ...} oder {"ohne_text": Grund} zurück."""
    m = ERLASS.match(url)
    api = f"{m.group(1)}/api/{m.group(2)}/texts_of_law/{m.group(3)}"
    host = urllib.parse.urlsplit(url).netloc
    with sperre(host):
        grund = ""
        for versuch in (1, 2):
            try:
                roh, typ, zs, _ = hole(api, "application/json")
                break
            except urllib.error.HTTPError as e:
                grund = f"Schnittstelle {e.code}"
                if e.code in (401, 403, 404, 410):
                    return {"ohne_text": grund}
            except Exception as e:
                grund = f"Schnittstelle {type(e).__name__}"
            if versuch == 1:
                time.sleep(3)
        else:
            return {"ohne_text": grund}
        time.sleep(0.3)
    try:
        tol = json.loads(roh.decode(zs or "utf-8", "replace"))["text_of_law"]
        version = tol["selected_version"]
        xhtml, stand = version["xhtml_tol"], version["version_dates_str"]
        titel = tol.get("title") or version.get("title") or ""
        if not isinstance(xhtml, str) or not isinstance(stand, str) or not xhtml.strip():
            raise ValueError("Feld leer")
        zeilen = erlass_zeilen(xhtml)
    except Exception as e:
        return {"ohne_text": f"Antwort ohne Text ({type(e).__name__})"}
    if not zeilen:
        return {"ohne_text": "Text leer"}
    text = "\n".join(zeilen)
    return {"summe": summe(stand + "\n" + text), "art": "erlass", "zeichen": len(text),
            "erlass_stand": stand, "titel": str(titel), "zeilen": zeilen}


def abruf(url, art):
    """art "inhalt", "erlass" oder "uebersicht". Gibt {"summe", ...} oder {"fehler"} zurück."""
    if art == "erlass":
        erg = abruf_erlass(url)
        if "ohne_text" not in erg:
            return erg
        seite = abruf(url, "inhalt")
        seite["ohne_text"] = erg["ohne_text"]
        return seite
    host = urllib.parse.urlsplit(url).netloc
    with sperre(host):
        for versuch in (1, 2):
            try:
                roh, typ, zs, ziel = hole(url)
                break
            except urllib.error.HTTPError as e:
                fehler = str(e.code)
                if e.code in (401, 403, 404, 410):
                    return {"fehler": fehler}
            except Exception as e:  # Zeitüberschreitung, DNS, TLS
                fehler = type(e).__name__
            if versuch == 1:
                time.sleep(3)
        else:
            return {"fehler": fehler}
        time.sleep(0.3)
    if art == "uebersicht":
        if typ not in ("text/html", "application/xhtml+xml"):
            return {"fehler": f"keine Webseite ({typ})"}
        _, links = lies_html(roh, zs, ziel)
        return {"summe": summe("\n".join(links)), "links": links}
    if typ in ("text/html", "application/xhtml+xml"):
        text, _ = lies_html(roh, zs, ziel)
        return {"summe": summe(text), "art": "text", "zeichen": len(text)}
    return {"summe": summe(roh), "art": "datei", "bytes": len(roh)}


def nachfuehren(alt, url, ergebnis, heute):
    """Neuer Eintrag aus dem alten und dem Abruf. Gibt (Eintrag, geändert?) zurück."""
    eintrag = dict(alt) if alt and alt.get("url") == url else {"url": url}
    if "fehler" in ergebnis:
        eintrag["fehler"] = ergebnis["fehler"]
        eintrag["fehler_am"] = heute
        return eintrag, False
    eintrag.pop("fehler", None)
    eintrag.pop("fehler_am", None)
    # Wechselt die Art (Seite <-> Erlass), ist die alte Prüfsumme nicht vergleichbar: neu erfassen
    gleiche_art = eintrag.get("art", ergebnis.get("art")) == ergebnis.get("art")
    geaendert = bool(eintrag.get("summe")) and gleiche_art and eintrag["summe"] != ergebnis["summe"]
    if geaendert:
        eintrag["geaendert"] = heute
        eintrag["aenderungen"] = (eintrag.get("aenderungen", []) + [heute])[-BEHALTEN:]
    if "summe" not in eintrag or not gleiche_art:
        eintrag["erster_abruf"] = heute
    eintrag["summe"] = ergebnis["summe"]
    eintrag["abgerufen"] = heute
    for feld in ("art", "zeichen", "bytes", "erlass_stand", "titel", "ohne_text"):
        if feld in ergebnis:
            eintrag[feld] = ergebnis[feld]
        elif feld != "art":
            eintrag.pop(feld, None)
    if "links" in ergebnis:
        vorher = set(eintrag.get("links", []))
        if geaendert:
            eintrag["neu"] = sorted(set(ergebnis["links"]) - vorher)
            eintrag["weg"] = sorted(vorher - set(ergebnis["links"]))
        eintrag["links"] = ergebnis["links"]
    return eintrag, geaendert


def lies_stand(pfad):
    try:
        with open(pfad, encoding="utf-8") as f:
            stand = json.load(f)
        if isinstance(stand, dict) and isinstance(stand.get("quellen"), dict):
            return stand
    except (OSError, ValueError):
        pass
    return {"quellen": {}}


def abrufen(pfad):
    heute = datetime.date.today().isoformat()
    stand = lies_stand(pfad)
    alt = stand["quellen"]
    qs = quellen()
    auftraege = set()
    for q in qs.values():
        auftraege.add((q["url"], "erlass" if ERLASS.match(q["url"]) else "inhalt"))
        if "uebersicht" in q:
            auftraege.add((q["uebersicht"], "uebersicht"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        ergebnisse = dict(zip(sorted(auftraege), pool.map(lambda a: abruf(*a), sorted(auftraege))))
    neu = {}
    zahl = {"quellen": len(qs), "erreichbar": 0, "nicht": 0, "erstmals": 0, "geaendert": 0,
            "erlasse": 0, "mit_text": 0, "leer": 0}
    zeilen = []
    ordner = os.path.join(os.path.dirname(os.path.abspath(pfad)), "texte")
    for key, q in sorted(qs.items()):
        vorher = alt.get(key) or {}
        erstmals = not (vorher.get("url") == q["url"] and vorher.get("summe"))
        art = "erlass" if ERLASS.match(q["url"]) else "inhalt"
        erg = ergebnisse[(q["url"], art)]
        eintrag, geaendert = nachfuehren(alt.get(key), q["url"], erg, heute)
        if art == "erlass":
            zahl["erlasse"] += 1
            if erg.get("art") == "erlass":
                zahl["mit_text"] += 1
                os.makedirs(ordner, exist_ok=True)
                with open(os.path.join(ordner, f"{key}.txt"), "w", encoding="utf-8") as f:
                    f.write("\n".join([erg["titel"], erg["erlass_stand"], heute] + erg["zeilen"]) + "\n")
            else:
                zeilen.append(f"OHNE TEXT\t{key}\t{erg.get('ohne_text', '')}\t{q['url']}")
        if erg.get("art") == "text" and erg.get("zeichen", 0) < MIN_TEXT:
            zahl["leer"] += 1
            zeilen.append(f"LEER\t{key}\tnur {erg['zeichen']} Zeichen sichtbarer Text, Wächter blind\t{q['url']}")
        if "fehler" in erg:
            zahl["nicht"] += 1
            zeilen.append(f"NICHT\t{key}\t{eintrag['fehler']}\t{q['url']}")
        else:
            zahl["erreichbar"] += 1
            if erstmals:
                zahl["erstmals"] += 1
        if geaendert:
            zahl["geaendert"] += 1
            zeilen.append(f"GEÄNDERT\t{key}\tInhalt\t{q['url']}")
        if "uebersicht" in q:
            vorher = (alt.get(key) or {}).get("uebersicht")
            u_erg = ergebnisse[(q["uebersicht"], "uebersicht")]
            u, u_geaendert = nachfuehren(vorher, q["uebersicht"], u_erg, heute)
            eintrag["uebersicht"] = u
            if "fehler" in u_erg:
                zeilen.append(f"NICHT\t{key}\tÜbersicht: {u['fehler']}\t{q['uebersicht']}")
            elif not u.get("links"):
                zeilen.append(f"LEER\t{key}\tÜbersicht ohne Links (Seite lädt sie wohl mit Skript)\t{q['uebersicht']}")
            if u_geaendert:
                zeilen.append(f"GEÄNDERT\t{key}\tÜbersicht, neu verlinkt: {len(u.get('neu', []))}, "
                              f"nicht mehr: {len(u.get('weg', []))}\t{q['uebersicht']}")
        else:
            eintrag.pop("uebersicht", None)
        neu[key] = eintrag
    stand = {"stand": heute, "zahlen": zahl, "quellen": neu}
    os.makedirs(os.path.dirname(os.path.abspath(pfad)), exist_ok=True)
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(stand, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    ordnung = {"GEÄNDERT": 0, "OHNE TEXT": 1, "LEER": 2, "NICHT": 3}
    zeilen.sort(key=lambda z: (ordnung[z.split("\t")[0]], z))
    for z in zeilen:
        print(z)
    schluss = (f"Abgerufen: {zahl['quellen']} Quellen. Erreichbar: {zahl['erreichbar']}, nicht erreichbar: "
               f"{zahl['nicht']}, zum ersten Mal erfasst: {zahl['erstmals']}, geändert: {zahl['geaendert']}. "
               f"Erlasse: {zahl['erlasse']}, davon mit Text: {zahl['mit_text']}. "
               f"Leer (Wächter blind): {zahl['leer']}.")
    print(schluss)
    bericht = os.environ.get("GITHUB_STEP_SUMMARY")
    if bericht:
        with open(bericht, "a", encoding="utf-8") as f:
            f.write(schluss + "\n\n")
            if zeilen:
                f.write("| Stand | Quelle | Bemerkung | Adresse |\n|---|---|---|---|\n")
                for z in zeilen:
                    f.write("| " + " | ".join(t.replace("|", "\\|") for t in z.split("\t")) + " |\n")


# ---------------------------------------------------------------- für den Lauf

def stand_vom_zweig():
    try:
        subprocess.run(["git", "-C", WURZEL, "fetch", "-q", "origin", "wandel"], check=True,
                       capture_output=True, timeout=120)
        aus = subprocess.run(["git", "-C", WURZEL, "show", "FETCH_HEAD:wandel.json"], check=True,
                             capture_output=True, timeout=60)
        return json.loads(aus.stdout.decode("utf-8"))
    except Exception as e:
        print(f"Zweig «wandel» nicht lesbar ({type(e).__name__}). Der Wächter hat noch keinen Stand "
              f"oder der Abruf ist gescheitert: nach dem Alter nachprüfen.")
        return None


def originalfassungen():
    """[(Pfad, geprueft, {Schlüssel})] aller Dateien ohne `uebersetzt_aus`."""
    muster = ["kantone/*.json", "gemeinden/*/*.json", "schweiz.json"]
    ordner = ["data", "data/fr-ch", "data/it-ch"]
    aus = []
    for o in ordner:
        for m in muster:
            for pfad in sorted(glob.glob(os.path.join(WURZEL, o, m))):
                with open(pfad, encoding="utf-8") as f:
                    d = json.load(f)
                if d.get("uebersetzt_aus"):
                    continue
                keys = set()

                def sammle(x):
                    if isinstance(x, dict):
                        for k, v in x.items():
                            if k.endswith("quellen") and isinstance(v, list):
                                keys.update(s for s in v if isinstance(s, str))
                            else:
                                sammle(v)
                    elif isinstance(x, list):
                        for v in x:
                            sammle(v)
                sammle(d)
                aus.append((os.path.relpath(pfad, WURZEL), d.get("geprueft", ""), keys))
    return aus


def unruhig(eintrag, heute):
    grenze = (heute - datetime.timedelta(days=UNRUHIG_TAGE)).isoformat()
    return len([d for d in eintrag.get("aenderungen", []) if d >= grenze]) > UNRUHIG


def faellig(stand):
    if not stand:
        return
    heute = datetime.date.today()
    q = stand.get("quellen", {})
    treffer, laut = [], set()
    for pfad, geprueft, keys in originalfassungen():
        gruende = []
        for key in sorted(keys):
            e = q.get(key) or {}
            for teil, name in ((e, "Inhalt"), (e.get("uebersicht") or {}, "Übersicht")):
                if teil.get("geaendert", "") > geprueft:
                    if unruhig(teil, heute):
                        laut.add(f"{key} ({name})")
                    else:
                        gruende.append(f"{key} ({name} geändert am {teil['geaendert']})")
        if gruende:
            treffer.append((geprueft, pfad, gruende))
    print(f"Stand des Wächters: {stand.get('stand', 'unbekannt')}.")
    if not treffer:
        print("Keine Originalfassung zitiert eine Quelle, die sich seit ihrer Prüfung geändert hat.")
    for geprueft, pfad, gruende in sorted(treffer):
        print(f"FÄLLIG\t{pfad}\tgeprüft {geprueft}\t" + "; ".join(gruende))
    if laut:
        print("Unruhig, zählen nicht (mehr als drei Änderungen in vier Wochen): " + ", ".join(sorted(laut)))
    blind = sorted(k for k, e in q.items()
                   if e.get("art") == "text" and e.get("zeichen", MIN_TEXT) < MIN_TEXT)
    if blind:
        print(f"Blind, weniger als {MIN_TEXT} Zeichen Text (nach dem Alter nachprüfen): " + ", ".join(blind))


def text(key, wort=None):
    """Druckt den Text eines Erlasses vom Zweig wandel, mit --suche nur die passenden Paragrafen."""
    try:
        subprocess.run(["git", "-C", WURZEL, "fetch", "-q", "origin", "wandel"], check=True,
                       capture_output=True, timeout=120)
        aus = subprocess.run(["git", "-C", WURZEL, "show", f"FETCH_HEAD:texte/{key}.txt"], check=True,
                             capture_output=True, timeout=60)
    except Exception as e:
        print(f"Kein Text für «{key}» auf dem Zweig «wandel» ({type(e).__name__}). Die Quelle ist kein "
              f"Erlass mit Schnittstelle, oder der Wächter hat sie noch nicht abgerufen.")
        return
    zeilen = aus.stdout.decode("utf-8").splitlines()
    titel, stand, tag, rumpf = (zeilen + ["", "", ""])[0], zeilen[1:2], zeilen[2:3], zeilen[3:]
    stand, tag = (stand or [""])[0], (tag or [""])[0]
    print(f"Titel: {titel}\nStand: {stand}\nAbgerufen: {tag}")
    try:
        alter = (datetime.date.today() - datetime.date.fromisoformat(tag)).days
        if alter > FRISCH_TAGE:
            print(f"ACHTUNG: Der Abruf ist {alter} Tage alt, mehr als {FRISCH_TAGE}. Der Text gilt nicht als "
                  f"im Lauf abgerufen.")
    except ValueError:
        pass
    print()
    if not wort:
        print("\n".join(rumpf))
        return
    teile, jetzt = [], []
    for z in rumpf:
        if KOPF_PARAGRAF.match(z) and jetzt:
            teile.append(jetzt)
            jetzt = []
        jetzt.append(z)
    if jetzt:
        teile.append(jetzt)
    treffer = [t for t in teile if KOPF_PARAGRAF.match(t[0]) and any(wort.lower() in z.lower() for z in t)]
    if not treffer:
        print(f"Kein Paragraf enthält «{wort}».")
    for t in treffer:
        print("\n".join(t) + "\n")


def main():
    args = sys.argv[1:]
    if "--text" in args:
        i = args.index("--text")
        wort = args[args.index("--suche") + 1] if "--suche" in args else None
        text(args[i + 1], wort)
        return
    if "--faellig" in args:
        if "--stand" in args:
            faellig(lies_stand(args[args.index("--stand") + 1]))
        else:
            faellig(stand_vom_zweig())
        return
    if len(args) != 1:
        print(__doc__)
        return
    try:
        abrufen(args[0])
    except Exception as e:  # die Action wird nie rot
        print(f"Abbruch: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
