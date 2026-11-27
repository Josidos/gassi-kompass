#!/usr/bin/env python3
"""Änderungswächter: merkt, welche Quelle sich seit dem letzten Abruf geändert hat.

Läuft in der GitHub Action «Quellen auf Änderungen prüfen» (.github/workflows/wandel.yml),
jeden Montag früh. Der Stand liegt nicht auf `main`, sondern auf dem Zweig `wandel` in der
Datei `wandel.json`. Kostet kein Guthaben: kein Modell, nur Abrufe und Prüfsummen.

Aufrufe:
  python3 tools/wandel.py <stand.json>     ruft alle Quellen ab und schreibt den Stand nach <stand.json>
  python3 tools/wandel.py --faellig        für den Lauf: welche Originalfassung ist nachzuprüfen?
  python3 tools/wandel.py --faellig --stand <stand.json>   dasselbe mit einem Stand aus einer Datei

Was eine Prüfsumme ist:
  HTML    der sichtbare Text ohne script, style, nav, header, footer, Formulare (und noscript,
          svg, template), Leerraum zusammengefasst
  sonst   die Bytes der Datei (PDF, Word)
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


def hole(url):
    """Gibt (Bytes, Inhaltsart, Zeichensatz, Zieladresse) zurück oder wirft eine Ausnahme."""
    sauber = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~")
    req = urllib.request.Request(sauber, headers=KOPF)
    with urllib.request.urlopen(req, timeout=ZEIT) as r:
        return r.read(GROESSTE), r.headers.get_content_type(), r.headers.get_content_charset(), r.geturl()


def abruf(url, art):
    """art "inhalt" oder "uebersicht". Gibt {"summe", ...} oder {"fehler"} zurück."""
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
    geaendert = bool(eintrag.get("summe")) and eintrag["summe"] != ergebnis["summe"]
    if geaendert:
        eintrag["geaendert"] = heute
        eintrag["aenderungen"] = (eintrag.get("aenderungen", []) + [heute])[-BEHALTEN:]
    if "summe" not in eintrag:
        eintrag["erster_abruf"] = heute
    eintrag["summe"] = ergebnis["summe"]
    eintrag["abgerufen"] = heute
    for feld in ("art", "zeichen", "bytes"):
        if feld in ergebnis:
            eintrag[feld] = ergebnis[feld]
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
        auftraege.add((q["url"], "inhalt"))
        if "uebersicht" in q:
            auftraege.add((q["uebersicht"], "uebersicht"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        ergebnisse = dict(zip(sorted(auftraege), pool.map(lambda a: abruf(*a), sorted(auftraege))))
    neu = {}
    zahl = {"quellen": len(qs), "erreichbar": 0, "nicht": 0, "erstmals": 0, "geaendert": 0}
    zeilen = []
    for key, q in sorted(qs.items()):
        vorher = alt.get(key) or {}
        erstmals = not (vorher.get("url") == q["url"] and vorher.get("summe"))
        eintrag, geaendert = nachfuehren(alt.get(key), q["url"], ergebnisse[(q["url"], "inhalt")], heute)
        if "fehler" in ergebnisse[(q["url"], "inhalt")]:
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
    ordnung = {"GEÄNDERT": 0, "LEER": 1, "NICHT": 2}
    zeilen.sort(key=lambda z: (ordnung[z.split("\t")[0]], z))
    for z in zeilen:
        print(z)
    schluss = (f"Abgerufen: {zahl['quellen']} Quellen. Erreichbar: {zahl['erreichbar']}, nicht erreichbar: "
               f"{zahl['nicht']}, zum ersten Mal erfasst: {zahl['erstmals']}, geändert: {zahl['geaendert']}.")
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


def main():
    args = sys.argv[1:]
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
