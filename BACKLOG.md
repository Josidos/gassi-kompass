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

Reihenfolge seit dem 28.11.2026, 04:40 Uhr: zuerst der Umbau für bessere Benutzerfreundlichkeit in drei Teilen (Auftrag von Joss um 04:18 Uhr, Befund der Durchsicht gegen vier Regelsammlungen), dann Suche und Quellenverzeichnis, dann das Themenfeld. Steht bei einem Punkt eine Datei `backlog/vorgabe-….md`, liest der Sonderlauf sie zuerst ganz.

- [ ] **Bedienung, Rest** (nicht fällig, in einer Sitzung). Erledigt am 28.11.2026: Tippflächen, Hover nur mit Maus, kleine Schrift, Test `tests/tippflaechen.js`, dazu (c) und (d) unten. Der Umbau des Aufbaus steht oben als drei fällige Punkte. Offen: (a) Rückmeldung von einem echten Telefon: Tastatur über den Treffern der Startseite, Lesbarkeit im Sonnenlicht, Treffsicherheit der Quellen-Links. (b) Aus der Rückmeldung vom 28.11.2026 in `backlog/spaeter.md`: «Standort verwenden», Favoriten. (c) Erledigt am 28.11.2026: Karte der Hundezonen mit «© swisstopo» im Kartenbild, Name und `role="region"` am Kartenblatt. (d) Erledigt am 28.11.2026: Druckansicht (`handbuch/generator.md`, «Druckansicht»). (e) Lesen ohne Netz braucht einen Service Worker: neuer Baustein, nur nach einem Entscheid von Joss.

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

- [ ] Appenzell Ausserrhoden: zurückgestellt am 2026-11-28. Keine amtliche Quelle nennt eine Meldestelle für entlaufene oder gefundene Hunde. Gelesen: EG zum ZGB (bGS 211.1), Hundeverordnung (bGS 525.11), Broschüre zur Hundehaltung (nur: die Gemeinden sorgen für streunende und herrenlose Hunde), Seite «Hunde» des Veterinäramts, Seite «Fundbüro» der Kantonspolizei (nur ein Link «Findeltiere» auf ein Tierheim, ohne Satz dazu). Die Seiten «Meldungen an das Veterinäramt» und «Tierschutz» auf ar.ch lieferten einen Fehler. Nächster Ansatz: die Seite «Tierschutz» des Veterinäramts (`ar.ch/verwaltung/departement-gesundheit-und-soziales/veterinaeramt/tierschutz/`) in einer Sitzung im Browser von Joss lesen. Ihr Link heisst auf der Seite des Amts «Tierschutzmeldungen und Findeltiere», WebFetch scheiterte am 28.11.2026 dreimal an der Website (Fehler der Seite, nicht gesperrt). Steht dort nichts: Auskunft des Veterinäramts beider Appenzell per Mail, Entwurf von Claude, Joss verschickt.
- [ ] Appenzell Innerrhoden: zurückgestellt am 2026-11-28. Auf den Seiten «Fundbüro» und «Melden und Anzeigen» der Kantonspolizei und «Tierhaltung» auf ai.ch steht nichts zu entlaufenen oder gefundenen Tieren, in der Gesetzessammlung fand sich nichts. Nächster Ansatz: zuerst die Seite «Tierschutz» des gemeinsamen Veterinäramts im Browser lesen (siehe Appenzell Ausserrhoden) und nur verwenden, wenn sie ausdrücklich auch für Innerrhoden gilt. Sonst Auskunft des Veterinäramts beider Appenzell per Mail, Entwurf von Claude, Joss verschickt.

### 9.4 Thema 2: Hunde betreuen und ausbilden als Beruf

Feld `gewerbe`, gebaut mit dem Sonderlauf vom 28.11.2026 (Abschnitt 5). Der Lauf belegt die Kantone, bis zu 4 pro Lauf, in dieser Reihenfolge (nach Einwohnerzahl). Je Kanton zu belegen, jede Angabe aus einer amtlichen Quelle des Kantons, die im Lauf abgerufen wurde:

- Betreuen gegen Entgelt (Pension, Tagesstätte, Hundesitting): bei welcher Stelle des Kantons man die Bewilligung beantragt, ab wann sie nötig ist und was die Seite des Amts zu Ausbildung, Gesuch und Gebühr sagt.
- Fremde Hunde ausführen: Bewilligung für Hundeausführdienste und Höchstzahl gleichzeitig geführter Hunde, wenn der Kanton das regelt.
- Ausbilden: Bewilligung, Anerkennung oder Meldepflicht für Hundeschulen und Kursleitende, auch für die obligatorischen Kurse des Kantons. Genau sagen, wofür sie gilt: nur für die obligatorischen Kurse des Kantons oder für jede Hundeausbildung. Zürich (Abnahme vom 28.11.2026): Die Bewilligung gilt nur für die obligatorischen Kurse, der Lauf hatte «wer Hunde ausbildet» geschrieben. Eine Liste nur so nennen, wie die Seite des Amts sie nennt.
- Weitere Pflichten für diese Tätigkeiten (zum Beispiel Haftpflicht oder Meldung an die Gemeinde), nur wenn sie in einem Erlass oder auf der Seite des Amts stehen.

Die Karte des Bundes (`schweiz.json`, `"id": "gewerbe"`) nennt schon die Regeln der Tierschutzverordnung (Bewilligung ab mehr als 5 fremden Tieren pro Tag, Ausbildung nach Zahl der Plätze, Zucht ab mehr als 20 Hunden oder mehr als drei Würfen pro Jahr): im Feld des Kantons nicht wiederholen, ausser die Seite des Kantons sagt es selbst. Handel ist auf der Karte des Bundes noch nicht belegt (Fachinformation 12.1 des BLV nicht gelesen), Hundeschulen regelt der Bund dort nicht. Nicht dazu gehören Empfehlungen, Regeln von Verbänden, Preise und einzelne Anbieter. Zucht und Handel nur, wenn der Kanton über das Bundesrecht hinausgeht. Sagt der Kanton nur, dass das Bundesrecht gilt, und nennt die Stelle für das Gesuch: genau das schreiben. Steht eine Angabe schon in einer Karte des Kantons (zum Beispiel die Höchstzahl geführter Hunde unter «Unterwegs»): im Feld wiederholen, mit derselben Quelle, nichts Neues daraus ableiten. Einstiege: Seite des Veterinärdiensts unter «Bewilligungen», «Tierschutz» oder «Tierhaltung», das Hundegesetz des Kantons (`python3 tools/wandel.py --text <Schlüssel> --suche Bewilligung`), Merkblätter und Gesuchsformulare des Amts. Findet sich nach zwei Suchanläufen keine amtliche Quelle des Kantons: Feld weglassen und den Kanton hier als «zurückgestellt» mit Datum und Grund vermerken. Bei zweisprachigen Kantonen kommt das Feld in beide Originalfassungen.

- [ ] Wallis (deutsch und französisch)
- [ ] Freiburg (deutsch und französisch)
- [ ] Basel-Landschaft
- [ ] Thurgau
- [ ] Solothurn
- [ ] Graubünden (deutsch und italienisch)
- [ ] Basel-Stadt
- [ ] Neuenburg
- [ ] Schwyz
- [ ] Zug
- [ ] Schaffhausen
- [ ] Jura
- [ ] Appenzell Ausserrhoden
- [ ] Nidwalden
- [ ] Glarus
- [ ] Obwalden
- [ ] Uri
- [ ] Appenzell Innerrhoden

### 9.2 und 9.3

Die vorgemerkten Themen und die Themenlandkarte stehen in `backlog/spaeter.md`.

## 10. Ausbau vor der Verbreitung

Entscheid von Joss vom 27.11.2026, 01:50 Uhr: zuerst die Seite so vollständig und gut wie möglich machen, dann die Tierheime und die zweite Runde an Hundeschulen anschreiben. Damit das ein Ende hat, gilt dieses Programm. Stehen die Punkte 1 bis 4, meldet der Bericht zuoberst «bereit für die Verbreitung». Empfänger und Texte liegen bereit (Seiten «Hundeschulen Runde 2» und «Tierheime Runde 1» von Joss). Die Adressen der Hundeschulen stammen aus der Liste vom 20.11.2026 und werden vor dem Versand noch einmal geprüft. Spätestens Ende Februar 2027 gehen die Mails raus, auch wenn nicht alles steht: Am 1. April beginnt in vielen Kantonen die Leinenpflicht im Wald, dann wird am meisten gesucht.

1. [x] Themenfeld «Hund vermisst oder gefunden»: Sonderlauf (Abschnitt 5), dann alle Kantone (Abschnitt 9.1). Macht der Lauf. Stand 2026-11-28: 24 von 26 Kantonen belegt, Appenzell Ausserrhoden und Appenzell Innerrhoden zurückgestellt (Abschnitt 9.1).
2. [x] Lücke «Kursanbieter finden»: am 27.11.2026 in der Sitzung erledigt für sechs der acht Kantone mit Kurspflicht. Für Luzern und Thurgau gibt es keine amtliche Liste.
3. [ ] Tote Links und Quellen, die dreimal «UNKLAR» waren, bereinigen (Abschnitt 4). Macht der Lauf beim Nachprüfen.
   Dazu der Änderungswächter für Quellen (Abschnitt 5, zweiter Sonderlauf): Er zeigt, welche Quelle sich geändert hat, damit der Lauf nicht blind nachprüft.
4. [ ] Seite «Für Hundeschulen» mit dem Angebot in drei Sprachen und der Baustein für Partner-Einträge samt Ordnung nach Angebot. Macht Claude in einer Sitzung, der Lauf nicht. Stand 28.11.2026: Die Seite mit dem Angebot wartet auf das Impressum (Punkt 6), weil sie einen Preis nennt. Der Baustein für Partner-Einträge hängt nicht daran: Er entsteht, sobald die erste Hundeschule zusagt.
5. [x] (erledigt 28.11.2026, Sonderlauf: `https://gassi-kompass.ch/<kt>/#neuer-hund`) «Neu einen Hund»: je Kanton die Schritte nach der Übernahme, zusammengestellt aus den vorhandenen Angaben, ohne neue Recherche. Braucht zuerst eine Vorgabe in Abschnitt 5, die Claude in einer Sitzung schreibt. Wichtig für die Tierheime.
6. [ ] Impressum und Datenschutzerklärung. Braucht den Entscheid von Joss, welche Angaben zu seiner Person erscheinen. Vor dem ersten bezahlten Eintrag nötig. Entscheid von Joss vom 27.11.2026, 12:33 Uhr: «Impressum für später, ja». Vor dem Bau legt Claude ihm den Wortlaut vor, mit genau den Angaben zu seiner Person, die erscheinen würden. In die Datenschutzerklärung gehören die Karte der Hundezonen (Kartenbilder von swisstopo) und GitHub Pages als Hoster. Stand 28.11.2026: Der Wortlaut von Impressum und Datenschutzerklärung liegt Joss vor (private Seite «Impressum-Entwurf»). Sein Entscheid von 03:00 Uhr: «Ich will noch kein Impressum.» Nichts veröffentlichen, nicht nachfragen, bis er es wieder aufnimmt.

Solange Punkt 1 offen ist, arbeitet der Lauf täglich (Handbuch, «Der Wochenlauf»).
