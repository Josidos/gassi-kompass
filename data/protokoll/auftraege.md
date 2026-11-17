# Vergebene Aufträge

Diese Aufträge sind an Parallel-Läufe vergeben. Die Regeln stehen in `CLAUDE.md` unter «Parallel-Läufe». Jede Zeile nennt den Namen des Auftrags, die Uhrzeit der Vergabe und den Inhalt. Wer das Protokoll eines Auftrags einsammelt, löscht seine Zeile. Ein normaler Lauf nimmt nichts, was hier steht, solange der Auftrag jünger als drei Stunden ist.

## Kantone (je samt grösster Gemeinde oder Hauptort)

- `so`, 2026-11-17 22:40: Kanton Solothurn
- `gr`, 2026-11-17 22:40: Kanton Graubünden, deutsche Fassung
- `sz`, 2026-11-17 22:40: Kanton Schwyz
- `zg`, 2026-11-17 22:40: Kanton Zug
- `sh`, 2026-11-17 22:40: Kanton Schaffhausen
- `ar`, 2026-11-17 22:40: Kanton Appenzell Ausserrhoden
- `nw`, 2026-11-17 22:40: Kanton Nidwalden
- `gl`, 2026-11-17 22:40: Kanton Glarus
- `ow`, 2026-11-17 22:40: Kanton Obwalden
- `ur`, 2026-11-17 22:40: Kanton Uri
- `ai`, 2026-11-17 22:40: Kanton Appenzell Innerrhoden

Nicht vergeben und damit Sache des normalen Laufs: Basel-Landschaft (`bl`) und Thurgau (`tg`), danach die Sonderläufe Themenseiten und Mehrsprachigkeit.

## Gemeinden

- `gemeinden-zh-1`, 2026-11-17 22:45: Winterthur, Uster, Dübendorf, Dietikon
- `gemeinden-zh-2`, 2026-11-17 22:45: Wetzikon, Wädenswil, Horgen, Bülach
- `gemeinden-zh-3`, 2026-11-17 22:45: Kloten, Opfikon, Thalwil, Adliswil
- `gemeinden-zh-4`, 2026-11-17 22:45: Regensdorf, Illnau-Effretikon, Schlieren, Volketswil
- `gemeinden-be-1`, 2026-11-17 22:45: Biel/Bienne (deutsche Fassung, Adresse `biel-bienne`), Thun, Köniz, Burgdorf
- `gemeinden-be-2`, 2026-11-17 22:45: Langenthal, Steffisburg, Ostermundigen, Muri bei Bern
- `gemeinden-be-3`, 2026-11-17 22:45: Spiez, Lyss, Münsingen, Worb
- `gemeinden-lu-1`, 2026-11-17 22:45: Emmen, Kriens, Horw, Ebikon
- `gemeinden-lu-2`, 2026-11-17 22:45: Sursee, Hochdorf, Willisau, Ittigen (BE)
- `gemeinden-ag-1`, 2026-11-17 22:45: Wettingen, Baden, Wohlen, Rheinfelden
- `gemeinden-sg-1`, 2026-11-17 22:45: Rapperswil-Jona, Wil, Gossau, Uzwil
- `gemeinden-bs-1`, 2026-11-17 22:45: Riehen, Bettingen, Aarau (AG, zweiter Anlauf)

## Französisch und Italienisch

Dateien unter `data/fr-ch/` und `data/it-ch/`, siehe `CLAUDE.md` unter «Französische und italienische Daten vor dem Umbau».

- `vd`, 2026-11-17 23:05: Kanton Waadt, französisch, samt Lausanne
- `ge`, 2026-11-17 23:05: Kanton Genf, französisch, samt Stadt Genf
- `ne`, 2026-11-17 23:05: Kanton Neuenburg, französisch, samt grösster Gemeinde
- `ju`, 2026-11-17 23:05: Kanton Jura, französisch, samt Delémont
- `ti`, 2026-11-17 23:05: Kanton Tessin, italienisch, samt Lugano
- `vs`, 2026-11-17 23:05: Kanton Wallis, deutsch und französisch, samt Sion (französisch)
- `fr`, 2026-11-17 23:05: Kanton Freiburg, deutsch und französisch, samt Stadt Freiburg (französisch)
- `be-fr`, 2026-11-17 23:05: Kanton Bern, französische Fassung, samt Biel/Bienne französisch

## Lücken und Gegenprüfung

Diese Läufe ändern bestehende Dateien. Bis ihr Protokoll eingesammelt ist, ändert sie sonst niemand.

- `luecken-zh`, 2026-11-17 23:05: `data/gemeinden/zh/zuerich.json`
- `luecken-be`, 2026-11-17 23:05: `data/kantone/be.json`, `data/gemeinden/be/bern.json`
- `luecken-lu`, 2026-11-17 23:05: `data/gemeinden/lu/luzern.json`
- `luecken-ag`, 2026-11-17 23:05: `data/kantone/ag.json`
- `luecken-sg`, 2026-11-17 23:05: `data/kantone/sg.json`, `data/gemeinden/sg/st-gallen.json`
- `luecken-bs`, 2026-11-17 23:05: `data/kantone/bs.json`, `data/gemeinden/bs/basel.json`
- `pruefung-bl`, 2026-11-17 23:05: `data/kantone/bl.json` und die Gemeinde des Kantons
- `pruefung-tg`, 2026-11-17 23:05: `data/kantone/tg.json` und die Gemeinde des Kantons
