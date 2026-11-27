#!/usr/bin/env python3
"""Hundezonen der Stadt Zürich für die Karte unter /zh/zuerich/karte/.

Quelle ist der amtliche Datensatz «Hundezonen» von Open Data Zürich (Grün Stadt Zürich, Lizenz CC0):
https://data.stadt-zuerich.ch/dataset/geo_hundezonen

Der Arbeitsplatz des Laufs erreicht die Server der Stadt nicht, und auch Artefakte einer Action kann er
nicht laden. Darum holt eine GitHub Action die Daten (.github/workflows/hundezonen.yml), bereitet sie mit
diesem Skript auf und legt drei Dateien auf den Zweig `geodaten`: roh.json (Antwort der Stadt), paket.json
(Angaben zum Datensatz) und zh-zuerich.json (die aufbereitete Fassung). Der Zweig `main` bleibt unberührt.

    gh api -X POST repos/Josidos/gassi-kompass/actions/workflows/hundezonen.yml/dispatches -f ref=main
    gh run list -R Josidos/gassi-kompass --workflow hundezonen.yml --limit 1     # muss «completed success» zeigen
    git fetch origin geodaten
    git show FETCH_HEAD:geodaten/zh-zuerich.json > data/geo/zh-zuerich.json
    python3 build.py && node tests/seiten.js

Zum Nachrechnen am Arbeitsplatz: roh.json und paket.json genauso aus dem Zweig holen, dann
`python3 tools/hundezonen.py roh.json paket.json`. Das schreibt data/geo/zh-zuerich.json neu.

Was das Skript tut: Es behält jede Fläche mit Zone, Namen und Bemerkung der Stadt, vereinfacht die Umrisse
(Douglas-Peucker, höchstens 1 Meter, bei schmalen Streifen weniger) und rundet auf fünf Stellen (rund 1 Meter). Koordinaten stehen als ganze
Zahlen (Grad mal 100000), der erste Punkt eines Rings ganz, alle weiteren als Unterschied zum Punkt davor.
Der Ring ist geschlossen, der Schlusspunkt fehlt.
"""
import json
import math
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIEL = ROOT / "data" / "geo" / "zh-zuerich.json"
WFS = ("https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Hundezonen?service=WFS&version=1.1.0&request=GetFeature"
       "&typename=hundezone&outputFormat=application%2Fvnd.geo%2Bjson&srsName=EPSG%3A4326")
PAKET = "https://data.stadt-zuerich.ch/api/3/action/package_show?id=geo_hundezonen"
ZONEN = {1, 3, 7, 8, 9, 12}   # Bedeutung laut Datensatz, siehe ZONEN in build.py
TOLERANZ = 1.0                # Meter
BREITE = math.radians(47.38)  # für die Umrechnung von Grad in Meter
MX = 111320.0 * math.cos(BREITE)
MY = 110540.0


def hole(url, ziel):
    anfrage = urllib.request.Request(url, headers={"User-Agent": "gassi-kompass.ch (Hundezonen, kontakt@gassi-kompass.ch)"})
    with urllib.request.urlopen(anfrage, timeout=120) as antwort:
        daten = antwort.read()
    Path(ziel).write_bytes(daten)
    print(f"{ziel}: {len(daten)} Bytes")


def abstand(p, a, b):
    """Abstand des Punktes p von der Strecke a-b in Metern."""
    px, py = (p[0] - a[0]) * MX, (p[1] - a[1]) * MY
    bx, by = (b[0] - a[0]) * MX, (b[1] - a[1]) * MY
    laenge = bx * bx + by * by
    if laenge == 0:
        return math.hypot(px, py)
    t = max(0.0, min(1.0, (px * bx + py * by) / laenge))
    return math.hypot(px - t * bx, py - t * by)


def vereinfache(punkte, toleranz):
    """Douglas-Peucker ohne Rekursion. Erster und letzter Punkt bleiben."""
    if len(punkte) < 3:
        return list(punkte)
    behalten = [False] * len(punkte)
    behalten[0] = behalten[-1] = True
    stapel = [(0, len(punkte) - 1)]
    while stapel:
        a, b = stapel.pop()
        weit, wo = 0.0, None
        for i in range(a + 1, b):
            d = abstand(punkte[i], punkte[a], punkte[b])
            if d > weit:
                weit, wo = d, i
        if wo is not None and weit > toleranz:
            behalten[wo] = True
            stapel.append((a, wo))
            stapel.append((wo, b))
    return [p for p, ja in zip(punkte, behalten) if ja]


def breite(punkte):
    """Mittlere Breite eines Rings in Metern: zweimal die Fläche durch den Umfang."""
    flaeche = umfang = 0.0
    for (ax, ay), (bx, by) in zip(punkte, punkte[1:] + punkte[:1]):
        flaeche += (ax * by - bx * ay) * MX * MY
        umfang += math.hypot((bx - ax) * MX, (by - ay) * MY)
    return abs(flaeche) / umfang if umfang else 0.0


def runde(punkte):
    ganz = []
    for x, y in punkte:
        p = (round(x * 100000), round(y * 100000))
        if not ganz or ganz[-1] != p:
            ganz.append(p)
    if len(ganz) > 1 and ganz[0] == ganz[-1]:
        ganz.pop()
    return ganz


def ring(koordinaten):
    """Ein Ring als flache Liste ganzer Zahlen oder None, wenn er kleiner ist als die Auflösung von rund 1 Meter.
    Schmale Streifen behalten ihre Form: Die Toleranz ist höchstens ein Viertel der mittleren Breite."""
    punkte = [(float(x), float(y)) for x, y in (k[:2] for k in koordinaten)]
    if len(punkte) > 1 and punkte[0] == punkte[-1]:
        punkte = punkte[:-1]
    if len(punkte) < 3:
        return None
    toleranz = max(0.05, min(TOLERANZ, breite(punkte) / 4))
    # Den Ring an seinem entferntesten Punkt teilen, damit Douglas-Peucker zwei offene Linien bekommt.
    fern = max(range(len(punkte)), key=lambda i: ((punkte[i][0] - punkte[0][0]) * MX) ** 2 + ((punkte[i][1] - punkte[0][1]) * MY) ** 2)
    kurz = vereinfache(punkte[: fern + 1], toleranz)[:-1] + vereinfache(punkte[fern:] + [punkte[0]], toleranz)[:-1]
    ganz = runde(kurz)
    if len(ganz) < 3:
        ganz = runde(punkte)  # zu klein für die Vereinfachung: alle Punkte der Stadt nehmen
    if len(ganz) < 3:
        return None
    flach = [ganz[0][0], ganz[0][1]]
    for (ax, ay), (bx, by) in zip(ganz, ganz[1:]):
        flach += [bx - ax, by - ay]
    return flach


def punkt(koordinaten):
    """Ersatz für eine Fläche unter 1 Meter: ein kleines Dreieck um ihren Mittelpunkt, damit sie sichtbar bleibt."""
    xs = [float(k[0]) for k in koordinaten]
    ys = [float(k[1]) for k in koordinaten]
    x, y = round(sum(xs) / len(xs) * 100000), round(sum(ys) / len(ys) * 100000)
    return [x - 1, y - 1, 2, 0, -1, 2]


def verarbeite(roh, paket=None):
    merkmale = roh["features"]
    zonen, vorher, nachher, verloren, winzig = [], 0, 0, 0, 0
    for m in merkmale:
        e = m["properties"]
        zone = int(e["zone"])
        if zone not in ZONEN:
            sys.exit(f"Unbekannte Zone {zone} bei {e.get('zonenname')}: Bedeutung im Datensatz nachlesen und in build.py ergänzen.")
        geo = m["geometry"]
        if not geo:
            sys.exit(f"Fläche ohne Geometrie: {e.get('zonenname')}")
        vielecke = geo["coordinates"] if geo["type"] == "MultiPolygon" else [geo["coordinates"]]
        teile = []
        for vieleck in vielecke:
            vorher += sum(len(r) for r in vieleck)
            ringe = [ring(r) for r in vieleck]
            if ringe[0] is None:  # der äussere Ring ist kleiner als 1 Meter, dann zählt auch kein Loch
                winzig += 1
                continue
            ringe = [r for r in ringe if r]
            nachher += sum(len(r) // 2 for r in ringe)
            teile.append(ringe)
        if not teile:  # die ganze Fläche ist kleiner als 1 Meter: als Punkt behalten
            teile = [[punkt(vielecke[0][0])]]
            nachher += 3
            verloren += 1
        eintrag = {"z": zone, "n": " ".join(str(e.get("zonenname") or "").split())}
        bemerkung = " ".join(str(e.get("bemerkungen") or "").split())
        if bemerkung:
            eintrag["b"] = bemerkung
        eintrag["g"] = teile
        zonen.append(eintrag)
    zonen.sort(key=lambda z: (z["z"] != 7, z["z"] == 1, z["n"].lower(), z["g"][0][0][:2]))
    stand = ""
    if paket:
        stand = str(paket.get("result", paket).get("dateLastUpdated") or "")
    return {
        "quelle": "zh_zonen",
        "stand": stand,
        "abgerufen": date.today().isoformat(),
        "zonen": zonen,
    }, (len(merkmale), vorher, nachher, verloren, winzig)


def main():
    arg = sys.argv[1:]
    if arg and arg[0] == "--holen":
        ordner = Path(arg[1] if len(arg) > 1 else ".")
        ordner.mkdir(parents=True, exist_ok=True)
        hole(WFS, ordner / "roh.json")
        hole(PAKET, ordner / "paket.json")
        roh = json.loads((ordner / "roh.json").read_text("utf-8"))
        print(f"Flächen: {len(roh['features'])}")
        return
    if not arg:
        sys.exit(__doc__)
    roh = json.loads(Path(arg[0]).read_text("utf-8"))
    paket = json.loads(Path(arg[1]).read_text("utf-8")) if len(arg) > 1 else None
    daten, (flaechen, vorher, nachher, verloren, winzig) = verarbeite(roh, paket)
    if len(daten["zonen"]) != flaechen:
        sys.exit(f"Es fehlen Flächen: {len(daten['zonen'])} von {flaechen}")
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(daten, ensure_ascii=False, separators=(",", ":")) + "\n"
    ZIEL.write_text(text, "utf-8")
    je = {}
    for z in daten["zonen"]:
        je[z["z"]] = je.get(z["z"], 0) + 1
    print(f"{ZIEL.relative_to(ROOT)}: {len(daten['zonen'])} von {flaechen} Flächen, {verloren} davon als Punkt, {winzig} Teilflächen unter 1 Meter weggelassen, "
          f"Punkte {vorher} -> {nachher}, {len(text.encode('utf-8'))} Bytes, Stand {daten['stand'] or 'unbekannt'}, je Zone {dict(sorted(je.items()))}")


if __name__ == "__main__":
    main()
