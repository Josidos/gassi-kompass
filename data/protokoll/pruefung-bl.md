# Parallel-Lauf pruefung-bl (Nacht auf den 18. November 2026)

## Protokoll

Gegenprüfung von `data/kantone/bl.json` und `data/gemeinden/bl/allschwil.json`. Alle neun Quellen abgerufen (`bl_hug`, `bl_pgh`, `bl_wjg`, `bl_wjv`, `bl_wald`, `bl_allschwil_hunde`, `bl_allschwil_gebuehren`, `bl_allschwil_pr`, `bl_allschwil_prv`). 61 Angaben verglichen (Kanton 38, Allschwil 23). 59 stimmen, 2 angepasst. `geprueft` bleibt in beiden Dateien 2026-11-17, weil `build.py` nach UTC rechnet und den 18. noch als Zukunft ablehnt.

Geändert:

- Kanton BL, `leine`, vierter Punkt. Alt: «an weiteren Orten, die deine Gemeinde bestimmt, zum Beispiel bei Dunkelheit, an verkehrsreichen Stellen oder in bestimmten Gebieten». Neu: «an weiteren Orten oder zu weiteren Zeiten, die deine Gemeinde bestimmt, zum Beispiel bei Dunkelheit oder an verkehrsreichen Stellen». Grund: § 3 Abs. 2 lit. b Hundegesetz nennt als Beispiele nur Dunkelheit und verkehrsreiche Stellen, «bestimmte Gebiete» war nicht zu belegen.
- Allschwil, Karte Hundetaxe. Alt: «Befreit sind unter anderem Diensthunde, Blindenführhunde sowie Sozial-, Therapie-, Assistenz- und Begleithunde.» Neu: «Befreit sind unter anderem Diensthunde, Blindenführhunde, Assistenz- und Begleithunde sowie Sozial- und Therapiehunde, die unentgeltlich in sozialen Institutionen eingesetzt werden.» Grund: § 13 der Verordnung zum Polizeireglement befreit Sozial- und Therapiehunde nur bei unentgeltlichem Einsatz in sozialen Institutionen.

Bestätigt, unter anderem: Leinenpflicht 1. April bis 31. Juli im Wald und in Waldesnähe (§ 12 WJG), Wildruhegebiete samt begrenzenden Waldstrassen und ausgeschilderten Wanderwegen (§ 3 WJV), Haftpflicht CHF 3 Millionen, Meldefrist 14 Tage, entlaufene Hunde 2 Tage, acht Rassen, weiterer Hund 16 Wochen, Gesuch CHF 250, Zuzug 4 Wochen. Allschwil: CHF 150 und CHF 75, Leinenorte nach § 35, Freilaufwege mit roten Streifen, Wiesland November bis Februar, Bussen CHF 50 und CHF 100, Höchstbusse CHF 5'000.

Hinweise ohne Änderung:

- Die Adresse «Baslerstrasse 111» steht auf der Seite der Einwohnerdienste Allschwil nur in den Angaben zur Seite, nicht im Lauftext. Belassen.
- Das Hundegesetz liegt auf LexFind mit Stand 1. Januar 2008 vor. Eine neuere Fassung ist dort nicht ausgewiesen.
- Die Texte kamen über WebFetch als Auszug mit kurzen Zitaten, nicht als Volltext. Geprüft wurde jede Angabe gezielt gegen diese Auszüge.

## Backlog

- Erledigt: Gegenprüfung BL (Kanton und Allschwil).
- Keine neuen Lücken.
