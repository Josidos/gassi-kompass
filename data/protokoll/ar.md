# Parallel-Lauf ar (Staffel A), 2026-11-18

## Protokoll

**Neu:** Kanton Appenzell Ausserrhoden (`data/kantone/ar.json`), 6 Quellen in `data/quellen/ar.json`. Alle Quellen in der Nacht auf den 18. November 2026 zwischen 00:00 und 00:15 Uhr abgerufen. `geprueft` steht auf 2026-11-17, weil `build.py` nach Weltzeit rechnet und den 18. als Zukunft ablehnt.

- Hundegesetz (bGS 525.1, Stand 1. Januar 2016): Pflichten und Kot (Art. 6), Leinen- und Maulkorbpflicht (Art. 8), Zutrittsverbote der Gemeinden (Art. 9), Haftpflicht (Art. 11), Kennzeichnung und Meldung innert 14 Tagen (Art. 13, 14), Massnahmen und Geltung ausserkantonaler Massnahmen (Art. 15), Hundesteuer höchstens CHF 200, weiterer Hund doppelt (Art. 19, 20), Busse ohne Betrag (Art. 22).
- Hundeverordnung (bGS 525.11, Stand 1. Januar 2025): Veterinäramt zuständig (Art. 1), Meldung von Vorfällen (Art. 2), Mindestdeckung CHF 5 Millionen (Art. 6), Steuer CHF 120 pro Kalenderjahr (Art. 10), Befreiungen mit Nachweis bis 31. Januar (Art. 11), Nachsteuer CHF 180 (Art. 12).
- Jagdgesetz (bGS 526.2, Stand 1. Juni 2023): keine Bestimmung über Hunde. Jagdverordnung (bGS 526.21, Stand 1. April 2024): Art. 33 wildernde Hunde, keine Leinenpflicht.
- Schutzverordnung Wildruhezone «südliches Appenzeller Hinterland» (2009, genehmigt 2011), Art. 10: Leinenzwang jederzeit, Ausnahmen.
- Informationsbroschüre zur Hundehaltung (Version 07/2019): Anmeldung beim Veterinäramt in Herisau, Empfehlung von Kursen.

**Entscheide:**

- `wald.saison` ist `false`: Die vier Erlasse nennen keine Leinenzeit im Wald.
- Hundesteuer: Die Broschüre von 2019 nennt CHF 100 und CHF 200. Es gilt die Hundeverordnung, Stand 1. Januar 2025: CHF 120. Der Betrag für weitere Hunde ist nur als «doppelte Steuer» wiedergegeben, wie im Gesetz.
- Meldefrist: Die Broschüre von 2019 nennt 10 Tage, das Hundegesetz (Art. 14) 14 Tage. Übernommen ist der Rechtstext.
- Kurs: `ton` ist `none`. Art. 14 HuG nennt die Meldung «erforderlicher Sachkundenachweise», eine kantonale Kurspflicht steht in keinem der beiden Erlasse.

**Weggelassen:**

- Alle Rechtstexte wurden über WebFetch gelesen, das den Wortlaut zusammenfasst. Beträge, Fristen und Artikel wurden mit einer zweiten, gezielten Abfrage bestätigt. Nicht bestätigte Einzelheiten (zum Beispiel die Liste aller Massnahmen in Art. 15, Regeln für Minderjährige und Chip-Frist aus der Broschüre) sind nicht oder nur als Beispiel übernommen.
- Ob die Schutzverordnung der Wildruhezone seit 2011 geändert wurde, war nicht zu klären. Der Text nennt deshalb den Stand.
- Seite ar.ch/hunde und «Leinenpflicht in beiden Appenzell»: in der Suche nicht gefunden, nicht abgerufen.
- Sömmerungsvorschriften AR 2025 (Alpen): nicht abgerufen.

**Nicht gelungen:** Herisau (BFS 3001) als Gemeinde, siehe Backlog.

## Backlog

- Abschnitt 1: Appenzell Ausserrhoden (`ar`) erledigt.
- Zurückgestellt (2026-11-18): Herisau. Zwei Suchen auf herisau.ch nach Hunden, Leinenpflicht, Hundeverbot und Reglement ergaben keine Seite der Gemeinde mit lokalen Angaben. Die Hundesteuer ist kantonal, die Anmeldung läuft über das Veterinäramt. Das sind weniger als drei lokale Angaben.
- Weitere Gemeinden für Abschnitt 3: Teufen (AR), Heiden, Speicher, Urnäsch, Hundwil. Hinweis: Steuer und Anmeldung sind kantonal. Lokale Angaben gibt es nur, wenn die Gemeinde Leinenorte (Art. 8 Abs. 2 HuG) oder Zutrittsverbote (Art. 9 HuG) bezeichnet hat. Bei Urnäsch und Hundwil zählt die Wildruhezone.
- Neue Lücken für Abschnitt 4:
  - `ar`: Seite des Veterinäramts (ar.ch/hunde) abrufen: heutige Meldestelle und Meldeweg, Abgleich mit `leine`.
  - `ar`: geltenden Stand und Perimeter der Wildruhezone «südliches Appenzeller Hinterland» belegen, weitere Wildruhezonen oder Naturschutzgebiete mit Regeln für Hunde suchen.
  - `ar`: Sömmerungsvorschriften und Alpen auf Regeln für Hunde prüfen.
  - `ar`: Bussenbeträge (Ordnungsbussen) für Leine und Kot belegen.
