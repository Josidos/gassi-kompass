#!/usr/bin/env python3
"""Prüft alle Adressen aus den Quellendateien mit einem echten Abruf.

Läuft in der GitHub Action «Quellen-Links prüfen» (.github/workflows/quellen.yml).
Der Lauf selbst kann fremde Seiten nicht direkt abrufen, und WebFetch liefert auch
Adressen aus, die im Browser «Error 404» zeigen (Merkblatt Thurgau, 18.11.2026).

Aufruf:   python3 tools/links.py
Ausgabe:  eine Zeile pro Adresse, die auffällt, am Schluss die Zahlen.

  TOT       Antwort 404 oder 410: Die Adresse gibt es nicht mehr.
  VERDACHT  Antwort 200, aber statt des PDF kommt eine Webseite, die Adresse
            führt auf die Startseite oder die Seite nennt sich selbst Fehlerseite.
  UNKLAR    Alles andere (403, 429, 5xx, Zeitüberschreitung). Viele Ämter weisen
            Abrufe aus dem Ausland oder von Programmen ab. Das heisst nicht,
            dass der Link für Leserinnen und Leser tot ist.

Das Programm endet immer ohne Fehler, damit die Action nie rot wird.
"""
import concurrent.futures
import glob
import json
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT = "Mozilla/5.0 (compatible; gassi-kompass-linkpruefung/1.0; +https://gassi-kompass.ch/ueber/)"
FEHLERTEXTE = (
    "seite nicht gefunden", "seite konnte nicht gefunden werden", "error 404", "fehler 404",
    "404 not found", "page not found", "page introuvable", "page non trouvée",
    "pagina non trovata", "pagina non è stata trovata",
)
_sperren = {}
_sperren_lock = threading.Lock()


def quellen():
    alle = {}
    dateien = [os.path.join(WURZEL, "data", "quellen.json")]
    dateien += sorted(glob.glob(os.path.join(WURZEL, "data", "quellen", "*.json")))
    for datei in dateien:
        with open(datei, encoding="utf-8") as f:
            for key, q in json.load(f).items():
                alle[key] = q["url"]
    return alle


def sperre(host):
    with _sperren_lock:
        return _sperren.setdefault(host, threading.Semaphore(2))


def abruf(url):
    """Gibt (Stand, Zahl oder Fehlername, Bemerkung) zurück."""
    sauber = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~")
    req = urllib.request.Request(sauber, headers={
        "User-Agent": AGENT,
        "Accept": "text/html,application/pdf,*/*;q=0.8",
        "Accept-Language": "de-CH,de;q=0.9,fr;q=0.8,it;q=0.7",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            art = r.headers.get_content_type()
            ziel = r.geturl()
            pfad_alt = urllib.parse.urlsplit(sauber).path.rstrip("/")
            pfad_neu = urllib.parse.urlsplit(ziel).path.rstrip("/")
            if ".pdf" in sauber.lower() and art == "text/html":
                return "VERDACHT", r.status, f"PDF erwartet, Webseite erhalten ({ziel})"
            if pfad_alt and not pfad_neu:
                return "VERDACHT", r.status, f"führt auf die Startseite ({ziel})"
            if art == "text/html":
                text = r.read(60000).decode("utf-8", "ignore").lower()
                kopf = text[:text.find("</h1>") + 5] if "</h1>" in text else text[:4000]
                for wort in FEHLERTEXTE:
                    if wort in kopf:
                        return "VERDACHT", r.status, f"Seite nennt sich Fehlerseite («{wort}»)"
            return "OK", r.status, ""
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return "TOT", e.code, ""
        return "UNKLAR", e.code, ""
    except Exception as e:  # Zeitüberschreitung, DNS, TLS
        return "UNKLAR", type(e).__name__, str(e)[:90]


def pruefe(eintrag):
    key, url = eintrag
    host = urllib.parse.urlsplit(url).netloc
    with sperre(host):
        ergebnis = abruf(url)
        if ergebnis[0] == "UNKLAR" and ergebnis[1] not in (401, 403):
            time.sleep(3)
            ergebnis = abruf(url)
        time.sleep(0.3)
    return key, url, ergebnis


def main():
    alle = sorted(quellen().items())
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        ergebnisse = list(pool.map(pruefe, alle))
    zahl = {"OK": 0, "TOT": 0, "VERDACHT": 0, "UNKLAR": 0}
    zeilen = []
    for key, url, (stand, code, bemerkung) in ergebnisse:
        zahl[stand] += 1
        if stand != "OK":
            zeilen.append(f"{stand}\t{code}\t{key}\t{url}\t{bemerkung}".rstrip())
    ordnung = {"TOT": 0, "VERDACHT": 1, "UNKLAR": 2}
    zeilen.sort(key=lambda z: (ordnung[z.split("\t")[0]], z))
    for z in zeilen:
        print(z)
    schluss = (f"Geprüft: {len(ergebnisse)} Quellen. In Ordnung: {zahl['OK']}, tot: {zahl['TOT']}, "
               f"Verdacht: {zahl['VERDACHT']}, unklar: {zahl['UNKLAR']}.")
    print(schluss)
    bericht = os.environ.get("GITHUB_STEP_SUMMARY")
    if bericht:
        with open(bericht, "a", encoding="utf-8") as f:
            f.write(schluss + "\n\n")
            if zeilen:
                f.write("| Stand | Antwort | Quelle | Adresse | Bemerkung |\n|---|---|---|---|---|\n")
                for z in zeilen:
                    teile = (z.split("\t") + [""] * 5)[:5]
                    f.write("| " + " | ".join(t.replace("|", "\\|") for t in teile) + " |\n")


if __name__ == "__main__":
    main()
