#!/usr/bin/env python3
"""Meldet Adressen an IndexNow: Bing und weitere Suchmaschinen holen die Seiten dann rasch ab.

Google nimmt IndexNow nicht an. Dort läuft es über die Sitemap in der Search Console.
Der Schlüssel ist der Name der Datei <32 Zeichen>.txt an der Wurzel. Sie ist öffentlich, das gehört so.

Aufruf:
  python3 tools/indexnow.py --alle            alle Adressen aus sitemap.xml
  python3 tools/indexnow.py --seit <Commit>   nur Seiten, die sich seit diesem Commit geändert haben

Läuft in der Action «IndexNow» (.github/workflows/indexnow.yml) nach jedem Push auf main.
Das Programm endet immer ohne Fehler, damit die Action nie rot wird.
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://gassi-kompass.ch"
# Jede Stelle gibt die Meldung an die anderen weiter. Die zweite ist nur der Ersatz, falls die erste ablehnt.
ZIELE = ["https://api.indexnow.org/indexnow", "https://www.bing.com/indexnow"]
AGENT = "Mozilla/5.0 (compatible; gassi-kompass-indexnow/1.0; +https://gassi-kompass.ch/ueber/)"


def schluessel():
    for name in sorted(os.listdir(WURZEL)):
        if re.fullmatch(r"[0-9a-f]{32}\.txt", name):
            with open(os.path.join(WURZEL, name), encoding="utf-8") as f:
                if f.read().strip() == name[:-4]:
                    return name[:-4]
    return None


def sitemap():
    with open(os.path.join(WURZEL, "sitemap.xml"), encoding="utf-8") as f:
        return re.findall(r"<loc>([^<]+)</loc>", f.read())


def geaendert(seit):
    """Adressen der Seiten, deren index.html sich seit dem Commit geändert hat. None: nicht feststellbar."""
    if not seit or set(seit) == {"0"}:
        return None
    try:
        aus = subprocess.run(["git", "diff", "--name-only", seit, "HEAD"], cwd=WURZEL,
                             capture_output=True, text=True, check=True).stdout.split("\n")
    except Exception:
        return None
    alle = set(sitemap())
    adressen = []
    for pfad in aus:
        if pfad == "index.html":
            adresse = SITE + "/"
        elif pfad.endswith("/index.html"):
            adresse = SITE + "/" + pfad[: -len("index.html")]
        else:
            continue
        if adresse in alle:
            adressen.append(adresse)
    return adressen


def main():
    key = schluessel()
    if not key:
        print("IndexNow: keine Schlüsseldatei an der Wurzel gefunden, nichts gemeldet.")
        return
    adressen = None
    if "--seit" in sys.argv:
        adressen = geaendert(sys.argv[sys.argv.index("--seit") + 1] if len(sys.argv) > sys.argv.index("--seit") + 1 else "")
    if adressen is None:
        adressen = sitemap()
    if not adressen:
        print("IndexNow: keine geänderten Seiten, nichts gemeldet.")
        return
    # Erst prüfen, ob die Schlüsseldatei schon veröffentlicht ist. Sonst lehnt IndexNow mit 403 ab.
    try:
        with urllib.request.urlopen(urllib.request.Request(f"{SITE}/{key}.txt", headers={"User-Agent": AGENT}), timeout=30) as r:
            inhalt = r.read(200).decode("utf-8", "ignore").strip()
            print(f"Schlüsseldatei: Antwort {r.status}, Inhalt {'stimmt' if inhalt == key else 'stimmt nicht'}.")
            if inhalt != key:
                return
    except Exception as e:
        print(f"Schlüsseldatei nicht abrufbar ({getattr(e, 'code', type(e).__name__)}). Nichts gemeldet, der nächste Push meldet neu.")
        return
    daten = json.dumps({"host": "gassi-kompass.ch", "key": key, "keyLocation": f"{SITE}/{key}.txt",
                        "urlList": adressen}).encode("utf-8")
    for ziel in ZIELE:
        req = urllib.request.Request(ziel, data=daten, method="POST",
                                     headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": AGENT})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"IndexNow ({ziel}): {len(adressen)} Adressen gemeldet, Antwort {r.status}.")
                return
        except urllib.error.HTTPError as e:
            text = e.read(300).decode("utf-8", "ignore").replace("\n", " ")
            print(f"IndexNow ({ziel}): {len(adressen)} Adressen gesendet, Antwort {e.code} ({e.reason}). {text}")
        except Exception as e:  # Netz, Zeitüberschreitung
            print(f"IndexNow ({ziel}): nicht erreichbar ({type(e).__name__}).")
    print("IndexNow: keine Stelle hat angenommen. Nichts weiter nötig, der nächste Push meldet neu.")


if __name__ == "__main__":
    main()
