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

- [ ] fällig: **«Neu einen Hund»: die Schritte je Kanton, dazu der Sprunglink** (Abschnitt 10, Punkt 5. Vorgabe aus der Sitzung vom 28.11.2026). Wer einen Hund übernimmt, sieht auf der Seite seines Kantons, was der Reihe nach zu tun ist. Tierheime können direkt darauf verlinken. Alles entsteht aus den vorhandenen Angaben: keine Recherche, keine neuen Datenfelder, kein Wort an den Daten ändern. Keine neue Seitenart, keine neue Adresse.
  1. Anker. Die sechs Karten der Kantonsseite bekommen feste `id`, in jeder Sprache dieselben: `haftpflicht`, `kurs`, `anmeldung`, `hundesteuer`, `rassen`, `unterwegs` (nach der Position der Karte, nicht nach ihrem Titel). Der Kasten zur Leine im Wald bekommt `wald`, falls er noch keine `id` hat. Nur auf der Kantonsseite, nicht auf Themenseiten und Gemeindeseiten: Dort stünden sonst dieselben `id` mehrfach. Springt man einen Anker an, darf die Überschrift nicht unter dem Kopf der Seite verschwinden (`scroll-margin-top`, falls nötig).
  2. Abschnitt auf jeder Kantonsseite, nach den Pflichten (samt Kasten zum Umzug) und vor «Hund vermisst oder gefunden», mit `id="neuer-hund"`. Überschrift: «Neu einen Hund {im}: die Schritte». Darunter ein Satz: «Du hast einen Hund übernommen oder holst bald einen zu dir? Hier stehen die Angaben dieser Seite in der Reihenfolge, in der sie für dich wichtig werden. Einzelheiten und Quellen findest du beim jeweiligen Punkt.» Dann eine nummerierte Liste (`<ol>`) mit genau sechs Schritten in dieser Reihenfolge: Rassen (Karte 5, `vergleich.rassen`), Anmeldung (Karte 3, `vergleich.anm`), Haftpflicht (Karte 1, `vergleich.haft`), Kurs (Karte 2, `vergleich.kurs`), Hundesteuer (Karte 4, `vergleich.steuer`), Leine im Wald (`vergleich.wald`). Jeder Schritt zeigt: den Titel der Karte in der Sprache der Seite als Link auf ihren Anker, die Marke der Karte als Chip in ihrem Ton (wie in den Tabellen der Themenseiten) und den Text aus `vergleich`, unverändert. Beim Wald: Titel aus `TEXTE` («Leine im Wald», «Laisse en forêt», «Guinzaglio nel bosco»), Chip und Ton wie in `seite_thema()` für das Thema `leinenpflicht-wald`, Link auf `#wald`. Die festen Texte behaupten nie eine Pflicht: Ob etwas Pflicht ist, sagen nur Chip und Text des Kantons.
  3. Darstellung mit den vorhandenen Bausteinen und Farben (`assets/site.css`, `DESIGN.md`), ruhig und knapp: eine Zeile je Schritt, auf dem Handy untereinander. Keine neuen Farben, keine neue Schrift.
  4. Sprunglink «Zum Inhalt» am Anfang jeder Seite, für Tastatur und Screenreader, in drei Sprachen («Zum Inhalt», «Aller au contenu», «Vai al contenuto»): erstes Element im `body`, sichtbar erst bei Fokus, Ziel ist der Hauptinhalt (`id` am `main` oder am ersten Abschnitt). Kleiner Umbau in `seite()` und `assets/site.css`.
  5. Texte in `TEXTE` für `de`, `fr`, `it`. Französisch und Italienisch nach `handbuch/uebersetzungen.md` (Anrede, Wortwahl). In der Fusszeile oder Themenleiste ändert sich nichts.
  6. Test (`tests/seiten.js`): Jede Kantonsseite in jeder Sprache hat genau einen Abschnitt `#neuer-hund` mit genau sechs Schritten. Jeder Link eines Schritts führt auf eine `id`, die es auf derselben Seite genau einmal gibt. Keine `id` kommt auf einer Seite doppelt vor. Jede Seite hat den Sprunglink, und sein Ziel gibt es.
  7. Ansehen: die Kantonsseiten Zürich (deutsch), Genf (französisch) und Tessin (italienisch) als Bild, einmal breit und einmal mit 390 Pixeln Breite. Erst pushen, wenn der Abschnitt ordentlich aussieht und nichts überläuft.
  8. Handbuch: `handbuch/generator.md` bekommt den Abschnitt «Neu einen Hund und Sprunglink» (wie es gebaut ist, die festen `id`). In `CLAUDE.md` nur ein Satz bei «Datenfelder Kanton», dass die Kantonsseite aus `karten` und `vergleich` den Abschnitt «Neu einen Hund» baut und `vergleich` darum auch dort erscheint. Lehnt die Umgebung die Änderung an `CLAUDE.md` ab: nicht wiederholen, im Protokoll festhalten, der Umbau gilt trotzdem als erledigt.
  9. Danach in Abschnitt 10 den Punkt 5 abhaken. Im Bericht die Adresse nennen, die ein Tierheim verlinken kann: `https://gassi-kompass.ch/<kt>/#neuer-hund`.

- [ ] **Rechtstexte für den Wächter und für den Lauf**: gebaut vom Lauf am 28.11.2026 (Protokoll dieses Tages). Der Wächter liest die 65 Erlasse auf LexWork, clex und tlex über die Schnittstelle der Sammlung, ihr Text liegt auf dem Zweig `wandel`: `python3 tools/wandel.py --text <Schlüssel> [--suche <Wort>]`. Im Handbuch steht das seit dem 28.11.2026 als Hinweis. Offen ist nur der Entscheid von Joss, ob ein solcher Text als «im Lauf abgerufen» zählt (Qualitätsregel 2), wenn sein Abruf höchstens 8 Tage alt ist: Die Umgebung des Laufs hat diese Änderung an `CLAUDE.md` abgelehnt, darum entscheidet er. Wort: «Regel 2 ja». Bis dahin ist der Text ein Hinweis, keine Quelle. Nicht fällig für den Lauf.

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
- [x] Jura 2026-11-28
- [ ] Appenzell Ausserrhoden: zurückgestellt am 2026-11-28. Keine amtliche Quelle nennt eine Meldestelle für entlaufene oder gefundene Hunde. Gelesen: EG zum ZGB (bGS 211.1), Hundeverordnung (bGS 525.11), Broschüre zur Hundehaltung (nur: die Gemeinden sorgen für streunende und herrenlose Hunde), Seite «Hunde» des Veterinäramts, Seite «Fundbüro» der Kantonspolizei (nur ein Link «Findeltiere» auf ein Tierheim, ohne Satz dazu). Die Seiten «Meldungen an das Veterinäramt» und «Tierschutz» auf ar.ch lieferten einen Fehler. Nächster Ansatz: die Seite «Tierschutz» des Veterinäramts (`ar.ch/verwaltung/departement-gesundheit-und-soziales/veterinaeramt/tierschutz/`) in einer Sitzung im Browser von Joss lesen. Ihr Link heisst auf der Seite des Amts «Tierschutzmeldungen und Findeltiere», WebFetch scheiterte am 28.11.2026 dreimal an der Website (Fehler der Seite, nicht gesperrt). Steht dort nichts: Auskunft des Veterinäramts beider Appenzell per Mail, Entwurf von Claude, Joss verschickt.
- [ ] Obwalden
- [ ] Uri
- [ ] Appenzell Innerrhoden: zurückgestellt am 2026-11-28. Auf den Seiten «Fundbüro» und «Melden und Anzeigen» der Kantonspolizei und «Tierhaltung» auf ai.ch steht nichts zu entlaufenen oder gefundenen Tieren, in der Gesetzessammlung fand sich nichts. Nächster Ansatz: zuerst die Seite «Tierschutz» des gemeinsamen Veterinäramts im Browser lesen (siehe Appenzell Ausserrhoden) und nur verwenden, wenn sie ausdrücklich auch für Innerrhoden gilt. Sonst Auskunft des Veterinäramts beider Appenzell per Mail, Entwurf von Claude, Joss verschickt.

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
