# Parallel-Lauf pruefung-tg (18. November 2026)

## Protokoll

Gegenprüfung von `data/kantone/tg.json` und der drei Gemeinden Arbon, Frauenfeld und Kreuzlingen. Jede Quelle neu abgerufen.

- **Nicht abrufbar:** `tg_hundeg` (Hundegesetz, lexfind.ch/tol/17744/de). WebFetch gab die Adresse nicht frei, zwei Suchen fanden keinen anderen amtlichen Wortlaut der geltenden Fassung. Erster Fehlversuch für diese Quelle. `geprueft` von `tg.json` bleibt deshalb auf 2026-11-17, an der Datei wurde nichts geändert.
- **Kanton, mit der Hundeverordnung (Stand 1. Mai 2025) und dem Merkblatt des Veterinäramts verglichen, alles stimmt (rund 25 Angaben):** Kurs mindestens 10 Lektionen mit Inhalten und Welpenkurs, Registrierungsstelle AMICUS, befreite Nutzhunde, Liste der 14 Rassen und Typen samt Kreuzungen, Unterlagen für die Bewilligung, Ausweis mitführen, Zuzug 10 Tage und Bewilligung des Herkunftskantons, Ordnungsbussen CHF 200 (unbeaufsichtigt), CHF 150 (Kot), CHF 100 (Mitführverbot), CHF 100 (Wald 1. April bis 31. Juli), CHF 100 (Anordnung der Gemeinde), entlaufene Hunde ausschreiben, Bewilligung CHF 500.
- **Kanton, nicht gegengeprüft, weil nur im Hundegesetz belegt (rund 12 Angaben):** Haftpflicht CHF 3 Millionen, Kursfrist ein Jahr und Nachweis, Steuer CHF 80 und CHF 130, Erhöhung um höchstens 50 Prozent, Zahlung bis Ende April, Befreiung unter fünf Monaten, Orte der Leinenpflicht und des Mitführverbots, Aussehen und Gentest unter 50 Prozent, Volljährigkeit und fester Wohnsitz, Bussenrahmen CHF 50 bis CHF 5'000. Die Informationen der Stadt Frauenfeld nennen ebenfalls CHF 3 Millionen und 10 Lektionen innert eines Jahres, das ersetzt den Gesetzestext aber nicht.
- **Arbon (9 Angaben):** alles stimmt. `geprueft` bleibt 2026-11-17 (das Datum des Generators, der in UTC rechnet).
- **Frauenfeld (17 Angaben):** eine Änderung. Alt: «Hundesäcke gibt es dort kostenlos.» (bezogen auf den Schalter der Einwohnerdienste). Neu: «Hundesäcke gibt es kostenlos am Informationsschalter im Rathaus.», so steht es in der Quelle. `geprueft` bleibt 2026-11-17 (das Datum des Generators, der in UTC rechnet).
- **Kreuzlingen (9 Angaben):** alles stimmt. `geprueft` bleibt 2026-11-17 (das Datum des Generators, der in UTC rechnet).
- Hinweis ohne Änderung: Die Ordnungsbusse für das Nichtanleinen in Park-, Schul-, Spiel- und Sportanlagen und an verkehrsreichen Strassen beträgt CHF 50 (HundeV § 13 Ziff. 3). Die Seite nennt diesen Betrag nicht und sagt nichts Falsches.

## Backlog

- Erledigt: Gegenprüfung der drei Thurgauer Gemeinden.
- Offen für Abschnitt 4: `data/kantone/tg.json` gegen das Hundegesetz (RB 641.2, geltende Fassung) prüfen, sobald der Wortlaut abrufbar ist. Dabei kann die Busse von CHF 50 für das Nichtanleinen in Anlagen und an verkehrsreichen Strassen bei `leine` ergänzt werden.
