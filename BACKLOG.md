# Ausbauliste

Erledigtes abhaken und das Datum dahinter schreiben. Was sich nicht belegen lässt, mit Datum und Grund als «zurückgestellt» markieren und weitergehen.

Diese Datei liest jeder Lauf ganz. Darum steht hier nur, was den nächsten Lauf steuert. Die langen Listen liegen unter `backlog/`: `gemeinden.md` (Abschnitt 3), `luecken.md` (Abschnitt 4) und `spaeter.md` (Abschnitte 6 bis 8, 9.2 und 9.3). Abgehaktes verschiebt `python3 tools/archiv.py` nach `backlog/archiv.md`.

## Reihenfolge

Ziel: jede Seite auf Deutsch, Französisch und Italienisch, dazu 60 Gemeinden. Für jeden Lauf gilt die erste Zeile, die zutrifft:

1. **Sonderlauf.** Ist in Abschnitt 5 ein Punkt mit dem Vermerk «fällig» offen, macht der Lauf nur den obersten davon.
2. **Übersetzungen.** Fehlen laut `python3 build.py --fehlend` mehr als 12 Übersetzungen, macht der Lauf nur Übersetzungen, höchstens 12 Dateien.
3. **Neuer Kanton.** Der oberste offene Kanton aus Abschnitt 1. Dazu seine grösste Gemeinde oder sein Hauptort. Ist Abschnitt 1 erledigt und die Mehrsprachigkeit in Abschnitt 5 abgehakt: der oberste offene Eintrag aus Abschnitt 2.
4. **Themenfelder.** Ist kein Kanton offen und in Abschnitt 9 ein Themenfeld offen, dessen Umbau in Abschnitt 5 abgehakt ist: dieses Feld für bis zu 4 Kantone belegen, in der Reihenfolge der Liste dort. Die Übersetzungen der geänderten Dateien entstehen im selben Lauf.
5. **Gemeinden.** Ist nichts davon möglich, bis zu 4 Gemeinden aus `backlog/gemeinden.md`.

In jedem Lauf ausser den Sonderläufen zusätzlich höchstens eine Lücke aus `backlog/luecken.md`: zuerst eine, die Abschnitt 10 nennt, sonst eine zu einem Kanton oder einer Gemeinde, die der Lauf ohnehin bearbeitet. Mit grep nach dem Namen suchen, die Datei nicht ganz lesen. Die «Toten Links» in Abschnitt 4 zählen nicht als Lücke: Sie gehören zum Nachprüfen, höchstens vier pro Lauf.

Bleibt ein Kanton nach einem Lauf unvollständig (Entwurf unter `data/entwurf/`), bekommt er in der Liste den Vermerk «zurückgestellt» mit Datum und dem, was fehlt. Der nächste Lauf nimmt den nächsten offenen Kanton. Zurückgestellte Kantone kommen wieder dran, sobald in ihrem Abschnitt kein anderer mehr offen ist. Scheitert ein Kanton dabei ein zweites Mal, bleibt er zurückgestellt, der Bericht meldet ihn zuoberst, und der Abschnitt gilt für die Reihenfolge als erledigt.

## Kette

keine Kette

## 1. Deutschsprachige Kantone

Ungefähr nach Bevölkerung. Schon erfasst: Zürich, Bern, Luzern, Aargau, St. Gallen, Basel-Stadt, Basel-Landschaft, Thurgau, Solothurn, Schwyz, Appenzell Innerrhoden, Graubünden, Zug, Schaffhausen, Appenzell Ausserrhoden, Nidwalden, Glarus, Uri, Obwalden. Aus Abschnitt 2 schon deutsch erfasst: Freiburg.

## 2. Französisch und Italienisch

Der Generator baut Französisch und Italienisch seit dem 2026-11-18. Bei zweisprachigen Kantonen beide Fassungen im selben Lauf, weil die Quellen dieselben sind.

## 3. Gemeinden

Die Liste steht in `backlog/gemeinden.md`, ungefähr nach Grösse. Neue Kantone tragen dort ihre grössten Gemeinden ein.

## 4. Lücken in bestehenden Seiten

### Tote Links

Zuerst erledigen, höchstens vier pro Lauf. Vorgehen in `CLAUDE.md` unter «Link-Prüfung». Offene Fälle (Antwort 404 beim echten Abruf oder Verdacht) trägt der Lauf hier als Punkte ein. Zurzeit ist keiner offen.

Unklar, nur beobachten. Durchgang vom 18.11.2026: `bl_wald` (baselland.ch, Antwort 403), `zh_wetzikon_hundewesen`, `zh_wetzikon_pvo` und `zh_wetzikon_tarif` (wetzikon.ch, Zeitüberschreitung). Durchgang vom 19.11.2026: `bl_wald` (403, zum zweiten Mal), `tg_vet_rassen` (Zeitüberschreitung, zum ersten Mal). Die drei Quellen von Wetzikon waren in Ordnung. Durchgang vom 20.11.2026: `bl_wald` (403, zum dritten Mal hintereinander, steht im Bericht vom 20.11.2026). `tg_vet_rassen` war in Ordnung. Durchgang vom 21.11.2026: `bl_wald` (403, zum fünften Mal, Joss ist seit dem 20.11.2026 gebeten, die Adresse im Browser anzuklicken), Joss hat die Adresse am 21.11.2026 auf der Seite angeklickt: Sie funktioniert im Browser. `bl_wald` gilt damit als in Ordnung, ein 403 der Link-Prüfung kommt bei dieser Quelle nicht mehr in den Bericht. Dazu zum ersten Mal mit Zeitüberschreitung `lu_stadt`, `ow_leine_2022` und `zh_opfikon_hundeabgabe`. Durchgang vom 25.11.2026: `bl_wald` (403, gilt als in Ordnung), `sz_einsiedeln_formular` (503, zum ersten Mal). Die drei vom 21.11. waren in Ordnung.

Zuletzt ausgewertet: der Durchgang der Link-Prüfung vom 27.11.2026, 12:39 Uhr. Der Lauf führt diese Zeile nach, wenn er einen neueren Durchgang ausgewertet hat.

### Lücken

Die offenen Lücken stehen in `backlog/luecken.md`, jede Zeile beginnt mit dem Kanton oder der Gemeinde. Nicht ganz lesen, sondern suchen: `grep -n "Kanton Thurgau" backlog/luecken.md`. Neue Lücken trägt der Lauf dort ein, unten angefügt.

## 5. Umbauten am Generator

Vorgaben in `CLAUDE.md` unter «Umbauten am Generator».

- [ ] **Rechtstexte für den Wächter und für den Lauf**: Teile 1 bis 4, 6 und 7 erledigt am 28.11.2026 (Lauf). Offen ist nur Teil 5, das Handbuch: Der Lauf durfte `CLAUDE.md` nicht ändern, die Sperre der Umgebung lehnte die Änderung an Qualitätsregel 2 ab. Teil 5 macht Claude in einer Sitzung auf das Wort von Joss, der Vorschlag steht im Protokoll vom 28.11.2026. Nicht mehr fällig für den Lauf. Bis dahin gilt Qualitätsregel 2 unverändert: Ein Text vom Zweig `wandel` ist ein Hinweis, keine im Lauf abgerufene Quelle. (aufgefallen am 28.11.2026 bei der Durchsicht des ersten Durchgangs). Bei den 65 Quellen auf Gesetzessammlungen mit Adressen der Form `https://<Server>/app/<Sprache>/texts_of_law/<Nummer>` (LexWork, clex, tlex: belex.sites.be.ch, gesetzessammlungen.ag.ch, srl.lu.ch, bl.clex.ch, rechtsbuch.tg.ch, biel-bienne.tlex.ch und weitere) sieht der Wächter nur den leeren Rahmen der Seite: 7 Zeichen Text und dieselbe Prüfsumme für alle. Für die wichtigsten Quellen ist er damit blind. Dieselben Texte kann der Lauf mit WebFetch nicht lesen, bisher ging das nur im Browser von Joss.
  1. `tools/wandel.py`: Für solche Adressen ruft es statt der Seite `https://<Server>/api/<Sprache>/texts_of_law/<Nummer>` ab (JSON). Der Text steht in `text_of_law.selected_version.xhtml_tol` (HTML), der Stand in `text_of_law.selected_version.version_dates_str`, der Titel in `text_of_law.title`. Die Prüfsumme geht über Stand und sichtbaren Text, die Art im Stand heisst `erlass`. Antwortet die Schnittstelle nicht oder fehlt ein Feld: Eintrag wie bisher, dazu im Bericht der Action eine Zeile «OHNE TEXT <Schlüssel>».
  2. Der Wächter legt den sichtbaren Text jedes solchen Erlasses auf den Zweig `wandel`, als `texte/<Schlüssel>.txt`: erste Zeile der Titel, zweite der Stand, dritte der Tag des Abrufs, dann der Text mit einer Zeile je Absatz. Überschriften von Paragrafen und Artikeln («§ 3», «Art. 12») stehen auf einer eigenen Zeile. Die Action fügt `texte/` zu ihrem Commit hinzu.
  3. `python3 tools/wandel.py --text <Schlüssel>` holt den Zweig wie `--faellig` und druckt Titel, Stand, Tag des Abrufs und den Text. Mit `--suche <Wort>` druckt es nur die Paragrafen, die das Wort enthalten. So liest der Lauf den geltenden Text ohne Browser.
  4. Allgemein: Liefert eine HTML-Seite weniger als 200 Zeichen sichtbaren Text, zählt sie als «LEER». Der Bericht der Action und `--faellig` nennen diese Quellen in einer eigenen Zeile als blind.
  5. Handbuch: Qualitätsregel 2 ergänzen. Ein Text vom Zweig `wandel` gilt als im Lauf abgerufen, wenn sein Abruf höchstens 8 Tage alt ist. Der Eintrag im Protokoll nennt dann Stand und Tag des Abrufs. Die Abschnitte «Änderungswächter» und «Hinweise zur Recherche» nachführen, in `handbuch/sitzung.md` unter «Quellen im Browser lesen» einen Satz ergänzen, dass diese Erlasse jetzt auch ohne Browser lesbar sind.
  6. Erster Durchgang: Action auslösen wie beim Bau des Wächters und im Protokoll festhalten, wie viele der 65 Erlasse einen Text haben, welche Server die Schnittstelle nicht bedienen und wie viele Quellen «LEER» sind. Probe: `python3 tools/wandel.py --text tg_vetv --suche Maulkorb` muss § 69 zeigen.
  7. Nicht in diesem Sonderlauf: andere Gesetzessammlungen (silgeneve.ch, prestations.vd.ch, zhlex, LexFind). Zeigt der erste Durchgang sie als «LEER», bekommt jede eine Zeile in `backlog/luecken.md`.

- [ ] Sprunglink «Zum Inhalt» am Anfang jeder Seite, für Tastatur und Screenreader, in drei Sprachen (aufgefallen am 2026-11-27 beim Abgleich mit der Prüfliste `web-design-guidelines` von Vercel). Kleiner Umbau in `seite()` und `assets/site.css`, zusammen mit dem nächsten Sonderlauf am Generator. Die übrigen prüfbaren Punkte der Liste sind erfüllt: sichtbarer Fokus überall, Zoomen nicht gesperrt, reduzierte Bewegung beachtet, keine Bilder ohne Masse.

## 6. Ideen für später

Steht in `backlog/spaeter.md`.

## 7. Braucht Zugriff, den der Lauf nicht hat

Steht in `backlog/spaeter.md`.

## 8. Später, nur nach Freigabe von Joss

Steht in `backlog/spaeter.md`. Der automatische Lauf braucht es nicht.

## 9. Neue Themenfelder

Entscheid von Joss vom 27.11.2026: Die Seite bleibt ein Nachschlagewerk mit amtlichen Quellen und bekommt neue Themen. Reihenfolge: 1. Hund vermisst oder gefunden. 2. Hunde als Beruf und Gewerbe: betreuen und ausbilden. 3. Reisen und Einreise mit Hund. 4. Wild und Weide. 5. Hunde mit besonderer Aufgabe und Hundesport (siehe 9.2). Ein Thema nach dem anderen: Zuerst baut ein Sonderlauf das Feld in den Generator (Abschnitt 5), dann belegt jeder Lauf bis zu 4 Kantone. Ist ein Thema in allen Kantonen belegt oder zurückgestellt, meldet der Bericht das zuoberst. Das nächste Thema braucht zuerst eine Vorgabe in Abschnitt 5. Die schreibt Claude in einer Sitzung, der Lauf erfindet keine.

### 9.1 Hund vermisst oder gefunden

Feld `vermisst`, gebaut mit dem Sonderlauf in Abschnitt 5. Je Kanton zu belegen, jede Angabe aus einer amtlichen Quelle, die im Lauf abgerufen wurde:

- wo man einen entlaufenen Hund meldet (Stelle des Kantons, Polizei, Datenbank AMICUS),
- wo man einen gefundenen Hund meldet (die Meldestelle, die der Kanton nach Art. 720a ZGB bezeichnet),
- was die Quelle sonst zum Vorgehen sagt (Fristen, Kosten, Tierheim).

Einstiege: Seite des Veterinärdiensts, Seite der Kantonspolizei, kantonale Gesetzessammlung (Einführungsgesetz zum ZGB, Verordnung über die Meldestelle für Findeltiere). Nennt der Kanton eine private Meldestelle als seine amtliche, ist die Seite oder der Erlass des Kantons die Quelle, nicht die Website der Meldestelle. Findet sich nach zwei Suchversuchen keine amtliche Quelle: Feld weglassen und den Kanton hier als «zurückgestellt» mit Datum und Grund vermerken. Bei zweisprachigen Kantonen kommt das Feld in beide Originalfassungen.

- [ ] Graubünden (deutsch und italienisch)
- [ ] Neuenburg
- [ ] Basel-Stadt
- [ ] Schwyz
- [ ] Zug
- [ ] Jura
- [ ] Appenzell Ausserrhoden
- [ ] Obwalden
- [ ] Uri
- [ ] Appenzell Innerrhoden

### 9.2 und 9.3

Die vorgemerkten Themen und die Themenlandkarte stehen in `backlog/spaeter.md`.

## 10. Ausbau vor der Verbreitung

Entscheid von Joss vom 27.11.2026, 01:50 Uhr: zuerst die Seite so vollständig und gut wie möglich machen, dann die Tierheime und die zweite Runde an Hundeschulen anschreiben. Damit das ein Ende hat, gilt dieses Programm. Stehen die Punkte 1 bis 4, meldet der Bericht zuoberst «bereit für die Verbreitung». Empfänger und Texte liegen bereit (Seiten «Hundeschulen Runde 2» und «Tierheime Runde 1» von Joss). Die Adressen der Hundeschulen stammen aus der Liste vom 20.11.2026 und werden vor dem Versand noch einmal geprüft. Spätestens Ende Februar 2027 gehen die Mails raus, auch wenn nicht alles steht: Am 1. April beginnt in vielen Kantonen die Leinenpflicht im Wald, dann wird am meisten gesucht.

1. [ ] Themenfeld «Hund vermisst oder gefunden»: Sonderlauf (Abschnitt 5), dann alle Kantone (Abschnitt 9.1). Macht der Lauf.
2. [x] Lücke «Kursanbieter finden»: am 27.11.2026 in der Sitzung erledigt für sechs der acht Kantone mit Kurspflicht. Für Luzern und Thurgau gibt es keine amtliche Liste.
3. [ ] Tote Links und Quellen, die dreimal «UNKLAR» waren, bereinigen (Abschnitt 4). Macht der Lauf beim Nachprüfen.
   Dazu der Änderungswächter für Quellen (Abschnitt 5, zweiter Sonderlauf): Er zeigt, welche Quelle sich geändert hat, damit der Lauf nicht blind nachprüft.
4. [ ] Seite «Für Hundeschulen» mit dem Angebot in drei Sprachen und der Baustein für Partner-Einträge samt Ordnung nach Angebot. Macht Claude in einer Sitzung, der Lauf nicht.
5. [ ] «Neu einen Hund»: je Kanton die Schritte nach der Übernahme, zusammengestellt aus den vorhandenen Angaben, ohne neue Recherche. Braucht zuerst eine Vorgabe in Abschnitt 5, die Claude in einer Sitzung schreibt. Wichtig für die Tierheime.
6. [ ] Impressum und Datenschutzerklärung. Braucht den Entscheid von Joss, welche Angaben zu seiner Person erscheinen. Vor dem ersten bezahlten Eintrag nötig. Entscheid von Joss vom 27.11.2026, 12:33 Uhr: «Impressum für später, ja». Vor dem Bau legt Claude ihm den Wortlaut vor, mit genau den Angaben zu seiner Person, die erscheinen würden. In die Datenschutzerklärung gehören die Karte der Hundezonen (Kartenbilder von swisstopo) und GitHub Pages als Hoster.

Solange Punkt 1 offen ist, arbeitet der Lauf täglich (Handbuch, «Der Wochenlauf»).
