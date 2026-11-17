# Parallel-Lauf nw (Staffel B), 2026-11-18

## Protokoll

- Neu: `data/kantone/nw.json` (Kanton Nidwalden) mit sieben Quellen in `data/quellen/nw.json`.
- Belegt aus aktuellen amtlichen Quellen: Hundesteuer CHF 120 pro Kalenderjahr, Anmeldung beim Amt für Justiz spätestens drei Monate nach der Geburt, Mutationen innert 10 Tagen (nw.ch, Hundekontrolle). Ordnungsbussen CHF 100 und CHF 300 (kOBV, Stand 1. September 2026). Meldestelle Kantonstierarzt (nw.ch, Gefährliche Hunde).
- Vorbehalt Hundegesetz: Die amtliche Sammlung gesetze.nw.ch liefert im Lauf nur eine leere Skript-Seite. Gelesen wurde die Fassung auf LexFind (tolv/63743), die nur das Inkrafttreten am 1. Januar 2005 nennt. Angaben, die allein daraus stammen (Verbot auf Friedhöfen, Spielplätzen, in Strandbädern; Leine auf Sportplätzen und in Schulhausanlagen; keine Haftpflicht, kein Pflichtkurs, keine Rasseliste), tragen im Text den Hinweis «Fassung von 2005». Die kOBV von 2026 verweist weiterhin auf Art. 19 Ziff. 1 bis 7 des Hundegesetzes, die Struktur gilt also noch. Haftpflicht, Kurs und Rassen stehen deshalb mit Ton `note`, nicht `none`.
- Wald: keine feste Leinenzeit in Hundegesetz und Jagdverordnung gefunden (`saison: false`). Die Verordnung über die Wildruhegebiete (NG 841.15) nennt in § 3 Abs. 2 eine Leinenpflicht für Hunde. Abgerufen wurde nur die Inhaltsübersicht (lexaris.de, Stand 31. Dezember 2019). Gebiete und Daten sind deshalb weggelassen.
- Weggelassen: Daten der Leinenpflicht in den Wildruhegebieten (nur bei tierimrecht.org gefunden, nicht amtlich), Strafrahmen des Hundegesetzes («Haft oder Busse», veraltet), Steuerbefreiung bei Zahlung in einem anderen Kanton (nur Fassung von 2005).
- Nicht gelungen: gesetze.nw.ch (alle Erlasse, nur Skript-Seite), laburk.ch (Abruf nicht freigegeben).
- Nicht gelungen: Stans. Die Hundesteuer und die Hundekontrolle sind in Nidwalden kantonal. Auf stans.ch keine lokale Angabe zu Hunden gefunden (Strassenreglement: nichts zu Hunden). Null belegte lokale Angaben, keine Datei.

## Backlog

- Abschnitt 1: Kanton Nidwalden erledigt (`data/kantone/nw.json`).
- Zurückgestellt (2026-11-18): Stans (BFS 1509). Grund: keine belegte lokale Angabe, Steuer und Anmeldung sind kantonal.
- Abschnitt 3, weitere Gemeinden: Stans (zweiter Anlauf), Hergiswil, Buochs, Ennetbürgen, Stansstad. Vorher prüfen, ob es in Nidwalden überhaupt Gemeinderegeln zu Hunden gibt. Sonst alle zurückstellen.
- Abschnitt 4, Lücken NW: geltende Fassung des Hundegesetzes (NG 826.3) und der Hundeverordnung aus gesetze.nw.ch gegenprüfen und die Hinweise «Fassung von 2005» entfernen oder die Angaben korrigieren. Verordnung über die Wildruhegebiete (NG 841.15) im Volltext: Gebiete und Daten der Leinenpflicht nachtragen. Kantonales Waldgesetz auf Leinenpflicht prüfen (im Lauf nicht abgerufen).
