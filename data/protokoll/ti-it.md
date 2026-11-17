# Parallel-Lauf ti-it (2026-11-18, Staffel C)

## Protokoll

- Neu: Kanton Tessin italienisch (`data/it-ch/kantone/ti.json`), Quellen in `data/quellen/ti-it.json`. Alle Quellen in diesem Lauf abgerufen. Geprüft über eine vorübergehende Kopie unter `data/kantone/`, Build und Test fehlerfrei.
- `geprueft` steht auf 2026-11-17, weil `build.py` das Datum 2026-11-18 (kurz nach Mitternacht) als «in der Zukunft» ablehnt.
- Belegt: Leine an Orten mit Publikum oder anderen Tieren (LCani Art. 7 Abs. 4), Haftpflicht mindestens CHF 3 Mio. (RCani Art. 6), Grundkurs 6 Stunden für Ersthaltende seit 1. September 2026 (LCani Art. 11a, RCani Art. 9 bis 12, Seite des UVC, CHF 120), Hundetaxe CHF 75 bis 125 (LCani Art. 4 und 4a), Rasseliste mit Bewilligung CHF 350 und zwei Tests (RCani Art. 14 bis 20, Seite des UVC), Ordnungsbussen aus dem Anhang des RCani, Busse bis CHF 20 000 (LCani Art. 21).
- Unsicherheit: Die Legge sui cani wurde über LexFind gelesen (Stand 15. Mai 2026). Das PDF der kantonalen Sammlung (m3.ti.ch, atto 479) zeigte eine ältere Fassung (Taxe CHF 50 bis 100) und wurde nicht verwendet. Beginn der Kurspflicht: Das RCani nennt für Art. 9 bis 12 den 1. Juni 2026, Gesetz und Seite des UVC den 1. September 2026. Übernommen ist der 1. September. WebFetch gibt Gesetzestexte nur zusammengefasst wieder, der Wortlaut einzelner Absätze wurde nicht Wort für Wort gelesen.
- Weggelassen: Leinenpflicht im Wald oder Jagdrecht (in LCani und RCani nichts gefunden, Jagdrecht nicht abgerufen, `wald` ohne Saison), kantonale Verbotsorte (das Gesetz nennt keine), Frist in Tagen für die Anmeldung (in keiner Quelle), Befreiungen von der Taxe für Diensthunde im Einzelnen.
- Neu: Città di Lugano italienisch (`data/it-ch/gemeinden/ti/lugano.json`): fünf Karten (Taxe CHF 115, Leine, Zutrittsverbot, Meldung, Bussen) und drei Hundezonen mit Öffnungszeiten. Quelle für Zonen und Öffnungszeiten ist die deutsche Fassung der städtischen Seite, die italienische Seite wurde nicht gefunden. Die Zone Barbengo steht dort nur in der Liste der Öffnungszeiten.
- Nicht gelungen: nichts.

## Backlog

- Erledigt: Tessin (`ti`), italienisch, Abschnitt 2, Daten unter `data/it-ch/`. Città di Lugano. Die Seiten entstehen erst nach dem Sonderlauf Mehrsprachigkeit.
- Weitere Gemeinden für Abschnitt 3: Bellinzona, Locarno, Mendrisio, Chiasso.
- Neue Lücken für Abschnitt 4: geltende Fassung der LCani auf der Gesetzessammlung des Kantons (www3.ti.ch) im Wortlaut gegenprüfen, besonders Art. 4, 4a, 7 und 11a. Datum der Kurspflicht klären (1. Juni oder 1. September 2026). Tessiner Jagd- und Waldrecht auf Leinenpflicht prüfen. Lugano: italienische Seite der Hundezonen suchen und Barbengo bestätigen.
