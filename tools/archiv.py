#!/usr/bin/env python3
"""Hält Protokoll und Ausbauliste kurz, ohne etwas zu löschen. Kein Modell nötig.

    python3 tools/archiv.py            verschiebt und meldet, was verschoben wurde
    python3 tools/archiv.py --pruefe   meldet nur, was verschoben würde

1. CHANGELOG.md: Es bleiben die neuesten Einträge (BLEIBEN). Ältere wandern nach changelog/JJJJ-MM.md,
   nach dem Datum in ihrer Überschrift, der neuste zuoberst.
2. BACKLOG.md und backlog/*.md (ohne archiv.md): Abgehakte Punkte («- [x]») wandern samt ihren
   eingerückten Folgezeilen nach backlog/archiv.md, unter die Überschrift ihres Abschnitts.
   Nummerierte Punkte («2. [x]») bleiben stehen: Sie gehören zu einem Programm, dessen Nummern zählen.

Läuft eine Kette (BACKLOG.md, Abschnitt «Kette», erste Zeile nicht «keine Kette»), bleibt CHANGELOG.md,
wie es ist: Die Glieder zählen dort ihre Einträge.
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLEIBEN = 8
PROTOKOLL = ROOT / "CHANGELOG.md"
LISTE = ROOT / "BACKLOG.md"
ORDNER_LISTE = ROOT / "backlog"
ORDNER_PROTOKOLL = ROOT / "changelog"
ARCHIV = ORDNER_LISTE / "archiv.md"
KOPF_ARCHIV = ("# Ausbauliste, Archiv\n\nAbgehakte Punkte aus `BACKLOG.md` und den Dateien unter `backlog/`. "
               "Entsteht mit `python3 tools/archiv.py`. Nicht ganz lesen: mit grep suchen.\n")
KOPF_MONAT = ("# Protokoll, Archiv {monat}\n\nÄltere Einträge aus `CHANGELOG.md`, der neuste zuoberst. "
              "Entsteht mit `python3 tools/archiv.py`. Nicht ganz lesen: mit grep suchen.\n\n")


def kette_laeuft():
    if not LISTE.is_file():
        return False
    m = re.search(r"(?m)^## Kette\s*\n+(.+)$", LISTE.read_text("utf-8"))
    return bool(m) and m.group(1).strip() != "keine Kette"


def protokoll(schreiben):
    """Verschiebt alle Einträge bis auf die neuesten. Gibt die Zahl der verschobenen zurück."""
    if not PROTOKOLL.is_file() or kette_laeuft():
        return 0
    text = PROTOKOLL.read_text("utf-8")
    teile = re.split(r"(?m)^(?=## )", text)
    kopf, eintraege = teile[0], teile[1:]
    if len(eintraege) <= BLEIBEN:
        return 0
    bleiben, gehen = eintraege[:BLEIBEN], eintraege[BLEIBEN:]
    je_monat, ohne_datum = {}, []
    for e in gehen:
        m = re.match(r"## (\d{4})-(\d{2})-\d{2}", e)
        if m:
            je_monat.setdefault(f"{m.group(1)}-{m.group(2)}", []).append(e)
        else:
            ohne_datum.append(e)  # ohne Datum in der Überschrift: bleibt im Protokoll
    verschoben = sum(len(v) for v in je_monat.values())
    if schreiben and verschoben:
        ORDNER_PROTOKOLL.mkdir(exist_ok=True)
        for monat, neu in je_monat.items():
            datei = ORDNER_PROTOKOLL / f"{monat}.md"
            kopf_m = KOPF_MONAT.format(monat=monat)
            alt = datei.read_text("utf-8") if datei.is_file() else kopf_m
            i = alt.find("\n## ")
            vorn, hinten = (alt, "") if i < 0 else (alt[: i + 1], alt[i + 1:])
            datei.write_text(vorn + "".join(x if x.endswith("\n\n") else x.rstrip("\n") + "\n\n" for x in neu) + hinten, "utf-8")
        PROTOKOLL.write_text(kopf + "".join(bleiben) + "".join(ohne_datum), "utf-8")
    return verschoben


def erledigte(datei, schreiben):
    """Nimmt abgehakte Punkte aus einer Datei. Gibt [(Abschnitt, Text des Punkts)] zurück."""
    zeilen = datei.read_text("utf-8").split("\n")
    bleibt, weg, abschnitt, i = [], [], "", 0
    while i < len(zeilen):
        z = zeilen[i]
        if re.match(r"#{1,3} ", z):
            abschnitt = z.lstrip("# ").strip()
        if z.startswith("- [x] "):
            block = [z]
            i += 1
            while i < len(zeilen) and zeilen[i].startswith("  ") and zeilen[i].strip():
                block.append(zeilen[i])
                i += 1
            weg.append((abschnitt, "\n".join(block)))
            continue
        bleibt.append(z)
        i += 1
    if schreiben and weg:
        text = re.sub(r"\n{3,}", "\n\n", "\n".join(bleibt))
        datei.write_text(text, "utf-8")
    return weg


def liste(schreiben):
    dateien = [LISTE] if LISTE.is_file() else []
    if ORDNER_LISTE.is_dir():
        dateien += sorted(p for p in ORDNER_LISTE.glob("*.md") if p != ARCHIV)
    neu, zahl = [], 0
    for datei in dateien:
        weg = erledigte(datei, schreiben)
        zahl += len(weg)
        je_abschnitt = {}
        for abschnitt, punkt in weg:
            je_abschnitt.setdefault(abschnitt, []).append(punkt)
        for abschnitt, punkte in je_abschnitt.items():
            neu.append(f"\n### {datei.relative_to(ROOT).as_posix()}, {abschnitt}\n\n" + "\n".join(punkte) + "\n")
    if schreiben and neu:
        ORDNER_LISTE.mkdir(exist_ok=True)
        alt = ARCHIV.read_text("utf-8") if ARCHIV.is_file() else KOPF_ARCHIV
        ARCHIV.write_text(alt.rstrip("\n") + f"\n\n## Archiviert am {date.today().isoformat()}\n" + "".join(neu), "utf-8")
    return zahl


def main():
    schreiben = "--pruefe" not in sys.argv
    n_protokoll, n_liste = protokoll(schreiben), liste(schreiben)
    wort = "verschoben" if schreiben else "zu verschieben"
    if kette_laeuft():
        print("Archiv: Eine Kette läuft, CHANGELOG.md bleibt, wie es ist.")
    print(f"Archiv: {n_protokoll} Einträge aus CHANGELOG.md, {n_liste} erledigte Punkte der Ausbauliste {wort}.")


if __name__ == "__main__":
    main()
