#!/usr/bin/env python3
"""Erzeugt data/orte.json aus dem Amtlichen Ortschaftenverzeichnis von swisstopo.

    python3 tools/orte.py PFAD/ZUR/DATEI.csv "Stand der Datei"

Die CSV-Datei (Trennzeichen Strichpunkt) hat die Spalten Ortschaftsname, PLZ, Zusatzziffer,
Gemeindename, BFS-Nr, Kantonskürzel, E, N, Sprache. Herausgeber ist das Bundesamt für
Landestopografie swisstopo, die Nutzung ist frei mit Quellenangabe. Zeilen ohne Kanton
(Liechtenstein) fallen weg.

Die Ortssuche braucht aus dieser Datei nur: Ortsname, Postleitzahl, Gemeinde und Kanton.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Kantonswechsel, die in der verwendeten Ausgabe des Verzeichnisses noch fehlen.
# BFS-Nummer der Gemeinde -> (neuer Kanton, Beleg). Leeren, sobald die Ausgabe sie enthält.
KANTONSWECHSEL = {
    700: ("ju", "Moutier gehört seit dem 1. Januar 2026 zum Kanton Jura "
                "(Bundesamt für Justiz, https://www.bj.admin.ch/de/loesung-der-jurafrage)"),
}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    pfad, stand = sys.argv[1], sys.argv[2]
    gemeinden, orte, nachgefuehrt = {}, set(), []
    with open(pfad, encoding="utf-8-sig", newline="") as f:
        for z in csv.DictReader(f, delimiter=";"):
            kt = z["Kantonskürzel"].strip().lower()
            if not kt:
                continue
            bfs = int(z["BFS-Nr"])
            if bfs in KANTONSWECHSEL and kt != KANTONSWECHSEL[bfs][0]:
                kt = KANTONSWECHSEL[bfs][0]
                if KANTONSWECHSEL[bfs][1] not in nachgefuehrt:
                    nachgefuehrt.append(KANTONSWECHSEL[bfs][1])
            gemeinden[bfs] = [bfs, z["Gemeindename"].strip(), kt]
            orte.add((z["Ortschaftsname"].strip(), z["PLZ"].strip(), bfs))
    g = [gemeinden[b] for b in sorted(gemeinden)]
    o = [list(x) for x in sorted(orte, key=lambda x: (x[1], x[0], x[2]))]
    zeilen = ["{",
              '"quelle": "Amtliches Ortschaftenverzeichnis, Bundesamt für Landestopografie swisstopo",',
              f'"stand": {json.dumps(stand, ensure_ascii=False)},',
              f'"nachgefuehrt": {json.dumps(nachgefuehrt, ensure_ascii=False)},',
              '"gemeinden": [',
              ",\n".join(json.dumps(x, ensure_ascii=False) for x in g),
              "],",
              '"orte": [',
              ",\n".join(json.dumps(x, ensure_ascii=False) for x in o),
              "]",
              "}"]
    (ROOT / "data" / "orte.json").write_text("\n".join(zeilen) + "\n", "utf-8")
    kantone = sorted({x[2] for x in g})
    print(f"data/orte.json: {len(g)} Gemeinden, {len(o)} Orte mit Postleitzahl, {len(kantone)} Kantone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
