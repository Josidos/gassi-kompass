# Protokoll

Neuster Eintrag zuoberst. Pro Lauf: nachgeprüft, geändert, neu, nicht gelungen.

## 2026-11-18, Kette, Glied 1: Sonderlauf Mehrsprachigkeit

- Start: `build.py --check` fehlerfrei, nichts einzusammeln. Das Werkzeug `add_repo` stand nicht zur Verfügung, das Repository war geklont und auf dem Stand von `main`. Angemeldet in `auftraege.md` um 10:06 Uhr, am Schluss wieder gelöscht.
- Umbau: `build.py` baut jetzt Deutsch an der Wurzel, Französisch unter `/fr-ch/` und Italienisch unter `/it-ch/`. Alle festen Texte stehen in der Tabelle `TEXTE` je Sprache. `assets/heute.js` und `assets/suche.js` kennen keine Sprache mehr, ihre Texte kommen aus `build.py`. Jede Seite trägt `lang`, Seiten mit mehreren Sprachfassungen tragen `hreflang` und einen Sprachwechsel im Kopf.
- Neu, aus den vorhandenen Daten unter `data/fr-ch/` und `data/it-ch/` (keine neue Recherche, keine Angabe geändert): Kantone Waadt, Genf, Neuenburg, Freiburg und Bern französisch (`/fr-ch/vd/`, `/fr-ch/ge/`, `/fr-ch/ne/`, `/fr-ch/fr/`, `/fr-ch/be/`), Kanton Tessin italienisch (`/it-ch/ti/`), Gemeinden Lausanne, Genève, Neuchâtel, Fribourg (französisch) und Lugano (italienisch), dazu je Sprache Startseite und «Über diese Seite» (`/fr-ch/`, `/fr-ch/ueber/`, `/it-ch/`, `/it-ch/ueber/`).
- Deutsche Seiten: Aussehen unverändert. Neu sind nur der Sprachwechsel (Startseite, «Über diese Seite», Bern, Freiburg), die Links auf die neuen Seiten (Kantonsraster, Gemeindeliste, Zeile unter dem Vergleich und auf den Themenseiten) und die Zahl der erfassten Kantone (23 statt 19). Geprüft durch Vergleich aller deutschen Seiten vor und nach dem Umbau.
- Entscheide: (1) Die Seite `/schweiz/`, die Themenseiten und `404.html` bleiben deutsch. Französische und italienische Seiten verlinken `/schweiz/` mit dem Zusatz der Sprache. (2) Die Startseiten jeder Sprache führen auch Kantone und Gemeinden auf, die es nur in einer anderen Sprache gibt, mit Angabe der Sprache. (3) Die Ortssuche findet Kantone unter dem deutschen, französischen und italienischen Namen. (4) `build.py` verlangt neu, dass `kurz` das Kürzel in Grossbuchstaben ist, und prüft die Kartentitel je Sprache. (5) Die Themenseiten zählen alle erfassten Kantone und sagen, dass sie die Kantone mit deutscher Fassung vergleichen.
- Test: `tests/seiten.js` prüft neu `lang`, `hreflang` in beide Richtungen und die Suche der französischen und italienischen Startseite. Als Bild angesehen: `/fr-ch/vd/`, `/it-ch/ti/`, `/fr-ch/vd/lausanne/`, `/it-ch/ti/lugano/`, `/fr-ch/`, `/it-ch/`, `/`, `/be/` und die Trefferliste der Suche auf Deutsch und Französisch.
- Backlog: Abschnitt 2 abgehakt für Waadt, Genf, Freiburg, Tessin, Neuenburg und Bern französisch. Offen bleiben dort Wallis, Jura und Graubünden italienisch. Abschnitt 5: Mehrsprachigkeit abgehakt. `CLAUDE.md` nachgeführt (Aufbau, Datenfelder, Abschnitt «Französische und italienische Daten», Zählweise der Gemeinden).
- Nicht gemacht: kein Nachprüfen, keine neuen Daten (Sonderlauf). Französische und italienische Themenseiten bleiben ein späterer Umbau.
- Stand: 23 von 26 Kantonen mit Seite (19 deutsch, 5 französisch, 1 italienisch), 42 Gemeinden, 80 Seiten in der Sitemap. Es fehlen Wallis, Jura und Obwalden.

## 2026-11-18, automatischer Lauf: Kanton Uri und Gemeinde Silenen

- Start: `build.py --check` fehlerfrei. Unter `data/protokoll/` lag nichts zum Einsammeln, in `auftraege.md` ist nichts vergeben. Das Werkzeug `add_repo` stand dem Lauf nicht zur Verfügung, das Repository war schon geklont und auf dem Stand von `main`.
- Nachgeprüft: nichts. Keine Datei ist älter als 60 Tage (ältestes `geprueft`: 2026-11-16).
- Neu: Kanton Uri (`/ur/`). Der Kanton hat kein Hundegesetz. Belegt aus der Jagdverordnung (RB 40.3111, Stand 1. Januar 2026): Leinenpflicht im Wald und in einem Streifen von 50 m ab Waldrand vom 1. April bis 31. Juli, Arbeitshunde ausgenommen. Aus Veterinärverordnung (RB 60.2111) und Veterinärreglement (RB 60.2113): Registrierung in AMICUS, Massnahmen im Einzelfall, keine Bestimmung zu Haftpflicht, Kurspflicht, Rassen oder Hundesteuer. Hundesteuer, Meldung, Leinenorte und Verbote regeln die Gemeinden. Die Kantonsseite nennt dafür Beispiele aus Altdorf, Silenen und Andermatt, bei Andermatt mit dem Hinweis «Stand der Verordnung: 2008».
- Neu: Gemeinde Silenen (`/ur/silenen/`), fünf lokale Angaben aus der Hundehalteverordnung vom 21. Mai 2025 (in Kraft seit 1. Januar 2026): Hundesteuer CHF 80, Meldung innert 30 Tagen, Leinenpflicht in gemeindeeigenen Anlagen, Hundekot, Busse bis CHF 1000.
- Entscheid: Silenen statt Altdorf als Gemeinde zum Kanton. Für den Hauptort Altdorf sind nur zwei lokale Angaben belegt. Silenen ist die Urner Gemeinde, deren geltende Verordnung der Lauf lesen konnte.
- Zurückgestellt: Altdorf. Das PDF der Verordnung über das Halten von Hunden (30.31) liess das Abrufwerkzeug zweimal nicht zu.
- Weggelassen: Bussenbetrag für die Leinenpflicht im Wald (Art. 44 KJSV nennt keinen). Die Hundegebühr von CHF 110 in der Jagdverordnung betrifft nur Jagdhunde und steht nicht auf der Seite.
- Nicht gelungen: Merkblatt «Verhaltensregeln für Hundehalter» des Veterinärdienstes der Urkantone und die Hundehalteverordnung Flüelen (beide nicht abrufbar). Keine Lücke aus Abschnitt 4 bearbeitet.
- Stand: 19 Kantone mit deutscher Seite, 37 Gemeinden, 65 Seiten in der Sitemap. In Abschnitt 1 ist nur noch Obwalden offen (zurückgestellt, Entwurf). Der nächste Lauf nimmt Obwalden wieder auf.

## 2026-11-18, Hauptsitzung: Schlusskontrolle der Nacht

- Verlauf: Am 17. November um 23:02 Uhr und in der Nacht um etwa 00:33 Uhr erreichte das Konto die Nutzungsgrenze. Beide Male brachen alle Läufe in der Cloud mitten in der Arbeit ab. Die Parallel-Läufe von 22:52 bis 23:02 Uhr lieferten nichts. Von 23:52 bis 00:33 Uhr arbeiteten bis zu acht Staffeln und die Nachtkette. Seit 00:33 Uhr hat kein Lauf mehr veröffentlicht, die Kette endete mit Glied 8.
- Stand: 18 Kantone mit deutscher Seite, 36 Gemeinden, 6 Themenseiten, 63 Seiten in der Sitemap. Daten ohne Seite, bis der Sonderlauf Mehrsprachigkeit gebaut ist: Waadt, Genf, Neuenburg, Tessin, die französischen Fassungen von Bern und Freiburg sowie Lausanne, Genève, Neuchâtel, Fribourg und Lugano.
- Offen bei den Kantonen: Obwalden (Entwurf), Uri, Wallis, Jura.
- Nicht geliefert und im Backlog wieder offen: Uri, Wallis, Jura, die Berner Gemeinden, die Gemeinden der Aufträge `ag-1`, `sg-1`, `bl-1` und `bs-1`, die Gegenprüfung Solothurn und die Lücken aus Abschnitt 4 zu AG, SG, BS, ZH, BE und LU.
- Eingesammelt: neun Protokolle, siehe die folgenden Einträge. In `data/protokoll/auftraege.md` ist nichts mehr vergeben.
- Stichproben gegen die amtlichen Quellen, je vier Angaben, alle bestätigt. Kanton Solothurn: Leinenpflicht im Wald vom 1. April bis 31. Juli, Hundesteuer CHF 35 für den Kanton und CHF 50 bis 200 für die Gemeinde, Haftpflicht ohne Mindestsumme, Meldung ab drei Monaten. Kanton Glarus: Hundetaxe CHF 55 ab dem sechsten Lebensmonat, Police innert eines Monats ans Einwohneramt, zehn Rassen mit Bewilligung, Gesuch spätestens 14 Tage nach der Übernahme. Kanton Schaffhausen: Haftpflicht mindestens CHF 1 Mio., Hundeabgabe CHF 100 bis 200, Leinenpflicht vom 15. April bis 30. Juni, Bewilligung vor der Anschaffung.
- Geändert, `build.py`: `geprueft` wird neu mit dem Schweizer Datum verglichen. Bisher lehnte der Build zwischen Mitternacht und 01:00 Uhr das neue Datum als Zukunft ab, weil die Läufe in UTC rechnen.
- Die Nachtkette ist abgeschaltet. Es läuft nur noch der tägliche Lauf um 08:23 Uhr.
- Nicht gelungen: nichts.

## 2026-11-18, Parallel-Lauf `ow`, eingesammelt in der Hauptsitzung

- Abschnitt 3, weitere Gemeinden, sobald der Kanton steht: Sarnen, Kerns, Alpnach, Sachseln, Engelberg. Die Leinenpflicht im Wald steht in den Hundeverordnungen der Gemeinden, Alpnach hat laut Kanton keine.
- Abschnitt 4, Lücken OW: Zeitraum und Abstand der Leinenpflicht im Wald je Gemeinde. Nummern und Namen der Wildruhezonen 1 bis 7. Aktuelle Liste der Naturschutzzonen mit Leinenpflicht.

## 2026-11-18, Parallel-Lauf `be-fr`, eingesammelt in der Hauptsitzung

- Der Lauf startete zuerst ohne Zusatznachricht und endete. Die Nachricht traf danach ein, die Arbeit begann um 00:25 Uhr, Schluss war 00:45 Uhr. Deshalb nur die Kantonsdatei.
- Neu: Kanton Bern französisch (`data/fr-ch/kantone/be.json`), zwei Quellen in `data/quellen/be-fr.json`, beide in diesem Lauf abgerufen. Die deutsche Datei `data/kantone/be.json` ist unverändert. Geprüft über eine vorübergehende Kopie unter `data/kantone/`.
- `geprueft` steht auf 2026-11-17 wie bei `vd-fr` und `ne-fr`.
- Belegt aus der französischen Broschüre des Veterinärdienstes (Juli 2022): Haftpflicht CHF 3 Mio., Orte mit Leinenpflicht, höchstens drei Hunde über vier Monate, Aufsicht, Kot, AMICUS, keine Rasseliste, kein Kursobligatorium. Aus der Änderung der OCE vom 17. Mai 2017 (Art. 13, 13a): Wohngemeinde als Registrierstelle, Hundetaxe wird von den Gemeinden erhoben.
- Unsicherheit: WebFetch gab die Broschüre nur zusammengefasst wieder, nicht im Wortlaut. Die OCE wurde nur als Änderungserlass von 2017 gelesen, nicht in der geltenden Fassung.
- Weggelassen: der Entscheid des Grossen Rates von 2023 zur Leinenpflicht im Wald (keine französische Quelle abgerufen), Befreiungen von der Hundetaxe (die französische Fassung der Loi sur les chiens, RSB 916.31, liess sich nicht abrufen: be.lexwork.naz.ch/fr wurde von WebFetch abgelehnt), Bussenbeträge (gefunden nur in der OCAO mit Stand 1. Januar 2018, lexfind.ch/tolv/119581/fr: Leine CHF 100, Kot CHF 150, zu alt für eine Angabe), Feld `umzug`.
- Nicht gelungen: Biel/Bienne französisch. Zwei Suchen auf biel-bienne.ch brachten nur Budgets und Rechnungen, keine Seite zu Hunden. Keine Datei angelegt.

## 2026-11-18, Parallel-Lauf `ge-fr`, eingesammelt in der Hauptsitzung

- Neu: Kanton Genf französisch (`data/fr-ch/kantone/ge.json`), elf Quellen in `data/quellen/ge-fr.json`. Alle Quellen in diesem Lauf abgerufen. Geprüft über eine vorübergehende Kopie unter `data/kantone/` und `data/gemeinden/ge/`, Build und Test fehlerfrei.
- `geprueft` steht auf 2026-11-17, wie bei `vd-fr` (der Build lehnt das Datum 2026-11-18 kurz nach Mitternacht ab).
- Belegt: Leinenpflicht im Wald 1. April bis 15. Juli (RChiens Art. 14 Bst. f, Seite des Kantons), Leinenpflicht in Ortschaften, Parks, Flughafen, Campings (Art. 14), Verbotsorte (Art. 13 Abs. 1), Haftpflicht für alle ohne Mindestsumme (LChiens Art. 16 Abs. 3), keine Kurspflicht, TMC für Hunde über 25 kg und 56 cm (LChiens Art. 22 und 27, Seite des Kantons), Eintrag in AMICUS innert 10 Tagen (LChiens Art. 17 Abs. 2, RChiens Art. 23), Kontrollmarke ab 6 Monaten bis 1. April (RChiens Art. 9), Kantonssteuer CHF 50 / 70 / 100 plus Gemeindezuschlag, CHF 1 Versicherung und CHF 4 Tierseuchenfonds, 15 verbotene Rassen samt Kreuzungen (LChiens Art. 23, RChiens Art. 17 Abs. 2), Kot aufnehmen (LChiens Art. 21 Abs. 2), Bewilligung ab mehr als drei anvertrauten Hunden (Art. 18 Abs. 3).
- Karte Kurs mit `ton: note`: keine allgemeine Kurspflicht, Test nur für grosse Hunde. Karte Rassen mit `ton: must`: Liste mit Verbot.
- Unsicherheit: Gesetz und Reglement wurden über eine Zusammenfassung des Abrufwerkzeugs mit Zitaten gelesen, nicht Artikel für Artikel im Volltext. Bei RChiens Art. 14 kamen nur die Buchstaben a, b, c, f und g zurück. Die Buchstaben d und e (vermutlich Moulin-de-Vert und Vogelreservat) stammen deshalb von der Seite des Kantons (Stand 2023). SILGeneve nennt für beide Erlasse eine Änderung oder Berichtigung vom 17. November 2026 (bei der LChiens zu Art. 3 Abs. 1). Was genau sich geändert hat, ist nicht geprüft. Die Seiten des Kantons zu Hunden sind von 2023, der Stand steht in den Karten Kurs und Annonce.
- Weggelassen: Mindestsumme der Haftpflicht (in keiner Quelle), Bussenbeträge (weder Gesetz noch Reglement nennen welche), Leinenverbot an Ufern und im Wasser von Oktober bis März (Art. 13 Bst. l, Geltungsbereich im Abruf abgeschnitten), Gemeindezuschläge zur Hundesteuer je Gemeinde (eigene Seite ge.ch/node/110, nicht abgerufen), Chip-Frist für Welpen, Regeln für Besuch mit Listenhunden (nicht gefunden).
- Neu: Ville de Genève französisch (`data/fr-ch/gemeinden/ge/geneve.json`, BFS 6621), vier Karten (Laisse, Accès interdit mit 12 namentlich genannten Parks, Annonce bei der Police municipale, Amendes ohne Beträge) und zwei Gruppen von Freilaufzonen mit Namen, zwei weitere Quellen der Stadt. Der Parc Liotard steht auf der Seite der Stadt sowohl bei den eingezäunten Freilaufzonen als auch bei den verbotenen Parks, die Karte sagt das so. Der Parc Geisendorf ist seit 1. Juni 2026 geschlossen und nicht als Zone aufgeführt.
- Weggelassen bei Genf: Hundesteuer der Stadt (Zuschlag nicht abgerufen), Bussenbeträge (nicht veröffentlicht).
- Nicht gelungen: nichts.

## 2026-11-18, Parallel-Lauf `ti-it`, eingesammelt in der Hauptsitzung

- Neu: Kanton Tessin italienisch (`data/it-ch/kantone/ti.json`), Quellen in `data/quellen/ti-it.json`. Alle Quellen in diesem Lauf abgerufen. Geprüft über eine vorübergehende Kopie unter `data/kantone/`, Build und Test fehlerfrei.
- `geprueft` steht auf 2026-11-17, weil `build.py` das Datum 2026-11-18 (kurz nach Mitternacht) als «in der Zukunft» ablehnt.
- Belegt: Leine an Orten mit Publikum oder anderen Tieren (LCani Art. 7 Abs. 4), Haftpflicht mindestens CHF 3 Mio. (RCani Art. 6), Grundkurs 6 Stunden für Ersthaltende seit 1. September 2026 (LCani Art. 11a, RCani Art. 9 bis 12, Seite des UVC, CHF 120), Hundetaxe CHF 75 bis 125 (LCani Art. 4 und 4a), Rasseliste mit Bewilligung CHF 350 und zwei Tests (RCani Art. 14 bis 20, Seite des UVC), Ordnungsbussen aus dem Anhang des RCani, Busse bis CHF 20 000 (LCani Art. 21).
- Unsicherheit: Die Legge sui cani wurde über LexFind gelesen (Stand 15. Mai 2026). Das PDF der kantonalen Sammlung (m3.ti.ch, atto 479) zeigte eine ältere Fassung (Taxe CHF 50 bis 100) und wurde nicht verwendet. Beginn der Kurspflicht: Das RCani nennt für Art. 9 bis 12 den 1. Juni 2026, Gesetz und Seite des UVC den 1. September 2026. Übernommen ist der 1. September. WebFetch gibt Gesetzestexte nur zusammengefasst wieder, der Wortlaut einzelner Absätze wurde nicht Wort für Wort gelesen.
- Weggelassen: Leinenpflicht im Wald oder Jagdrecht (in LCani und RCani nichts gefunden, Jagdrecht nicht abgerufen, `wald` ohne Saison), kantonale Verbotsorte (das Gesetz nennt keine), Frist in Tagen für die Anmeldung (in keiner Quelle), Befreiungen von der Taxe für Diensthunde im Einzelnen.
- Neu: Città di Lugano italienisch (`data/it-ch/gemeinden/ti/lugano.json`): fünf Karten (Taxe CHF 115, Leine, Zutrittsverbot, Meldung, Bussen) und drei Hundezonen mit Öffnungszeiten. Quelle für Zonen und Öffnungszeiten ist die deutsche Fassung der städtischen Seite, die italienische Seite wurde nicht gefunden. Die Zone Barbengo steht dort nur in der Liste der Öffnungszeiten.
- Nicht gelungen: nichts.

## 2026-11-18, Parallel-Lauf `pruefung-tg`, eingesammelt in der Hauptsitzung

Gegenprüfung von `data/kantone/tg.json` und der drei Gemeinden Arbon, Frauenfeld und Kreuzlingen. Jede Quelle neu abgerufen.

- **Nicht abrufbar:** `tg_hundeg` (Hundegesetz, lexfind.ch/tol/17744/de). WebFetch gab die Adresse nicht frei, zwei Suchen fanden keinen anderen amtlichen Wortlaut der geltenden Fassung. Erster Fehlversuch für diese Quelle. `geprueft` von `tg.json` bleibt deshalb auf 2026-11-17, an der Datei wurde nichts geändert.
- **Kanton, mit der Hundeverordnung (Stand 1. Mai 2025) und dem Merkblatt des Veterinäramts verglichen, alles stimmt (rund 25 Angaben):** Kurs mindestens 10 Lektionen mit Inhalten und Welpenkurs, Registrierungsstelle AMICUS, befreite Nutzhunde, Liste der 14 Rassen und Typen samt Kreuzungen, Unterlagen für die Bewilligung, Ausweis mitführen, Zuzug 10 Tage und Bewilligung des Herkunftskantons, Ordnungsbussen CHF 200 (unbeaufsichtigt), CHF 150 (Kot), CHF 100 (Mitführverbot), CHF 100 (Wald 1. April bis 31. Juli), CHF 100 (Anordnung der Gemeinde), entlaufene Hunde ausschreiben, Bewilligung CHF 500.
- **Kanton, nicht gegengeprüft, weil nur im Hundegesetz belegt (rund 12 Angaben):** Haftpflicht CHF 3 Millionen, Kursfrist ein Jahr und Nachweis, Steuer CHF 80 und CHF 130, Erhöhung um höchstens 50 Prozent, Zahlung bis Ende April, Befreiung unter fünf Monaten, Orte der Leinenpflicht und des Mitführverbots, Aussehen und Gentest unter 50 Prozent, Volljährigkeit und fester Wohnsitz, Bussenrahmen CHF 50 bis CHF 5'000. Die Informationen der Stadt Frauenfeld nennen ebenfalls CHF 3 Millionen und 10 Lektionen innert eines Jahres, das ersetzt den Gesetzestext aber nicht.
- **Arbon (9 Angaben):** alles stimmt. `geprueft` bleibt 2026-11-17 (das Datum des Generators, der in UTC rechnet).
- **Frauenfeld (17 Angaben):** eine Änderung. Alt: «Hundesäcke gibt es dort kostenlos.» (bezogen auf den Schalter der Einwohnerdienste). Neu: «Hundesäcke gibt es kostenlos am Informationsschalter im Rathaus.», so steht es in der Quelle. `geprueft` bleibt 2026-11-17 (das Datum des Generators, der in UTC rechnet).
- **Kreuzlingen (9 Angaben):** alles stimmt. `geprueft` bleibt 2026-11-17 (das Datum des Generators, der in UTC rechnet).
- Hinweis ohne Änderung: Die Ordnungsbusse für das Nichtanleinen in Park-, Schul-, Spiel- und Sportanlagen und an verkehrsreichen Strassen beträgt CHF 50 (HundeV § 13 Ziff. 3). Die Seite nennt diesen Betrag nicht und sagt nichts Falsches.

## 2026-11-18, Parallel-Lauf `gemeinden-lu-1`, eingesammelt in der Hauptsitzung

Der Lauf startete ohne Zusatznachricht und endete zuerst ohne Änderung. Die Zusatznachricht (Staffel H) kam danach als zweite Auslösung um 00:29 Uhr, 16 Minuten vor Schluss. Weil vorher nichts erledigt war, wurde der Auftrag dann bearbeitet. Die Recherche ist entsprechend knapp. Alle Quellen am 18. November 2026 abgerufen. Die Angaben stammen aus der Zusammenfassung des Abrufwerkzeugs mit kurzen wörtlichen Zitaten, nicht aus dem vollen Wortlaut: bei der nächsten Gegenprüfung den Wortlaut vergleichen.

Neu:

- **Emmen** (`data/gemeinden/lu/emmen.json`): Hundesteuer CHF 120, Hofhunde CHF 40, ab sechs Monaten (Seite Sondersteuern). Anmeldung bei der Einwohnerkontrolle, Meldungen über das Online-Formular, Zuzug innert zehn Tagen. Friedhof: Mitbringen oder Laufenlassen von Tieren verboten (Friedhofreglement Art. 15 Abs. 3).
- **Horw** (`data/gemeinden/lu/horw.json`): Hundesteuer CHF 120, Hofhunde CHF 40, Bereich Finanzen. Erfassung in AMICUS durch die Einwohnerdienste vor der Anschaffung. Leinenpflicht im Naturschutzgebiet zwischen Ennethorw und Hergiswil (Mitteilung vom 29. Juni 2015, Stand genannt) sowie auf Terrasse und im Park der Villa Krämerstein, im Innern keine Hunde (Benutzungsverordnung Nr. 550, Anhang 10, verbindlich für Veranstaltende).
- **Ebikon** (`data/gemeinden/lu/ebikon.json`): Hundesteuer CHF 120, Hof- und Jagdhunde CHF 40, Junghunde unter Bedingungen CHF 60. Anmeldung über das Formular «Hundesteuer», Personen-ID über das Formular «AMICUS Personen-ID». Hunde im Waldreservat im Riedholz auf dem Hundsrüggen an der Leine (Mitteilung vom 23. November 2023, Stand genannt).

Weggelassen:

- Emmen: Betrag CHF 60 für Junghunde, weil die Bedingung aus dem Abruf nicht eindeutig hervorging. Hundefreilaufzonen: Der Gemeinderat lehnte am 16. April 2026 ein Postulat ab, der Einwohnerrat entschied am 12. Mai 2026, der Ausgang wurde nicht abgerufen.
- Ebikon: Ermässigung CHF 60 «nach §10» und CHF 0 für Schweisshunde, weil die Bedingungen nicht gelesen wurden. Rechtsgrundlage und Geltungszeit der Leinenregel im Waldreservat nennt die Mitteilung nicht.
- Horw: Rechtsgrundlage der Leinenpflicht im Widenbachdelta nennt die Mitteilung nicht.

Zurückgestellt:

- **Kriens**: Die Seiten der Stadt (stadt-kriens.ch/dienstleistungen/hundehaltung/…: Hundesteuer, Hundehaltung, Hund anmelden) liessen sich nicht abrufen (robots_disallowed, einmal Serverfehler). Keine Angabe belegt, keine Datei angelegt.

Nicht gelungen: nichts weiter.

## 2026-11-18, Parallel-Lauf `gemeinden-lu-2`, eingesammelt in der Hauptsitzung

Der Lauf startete ohne Zusatznachricht und endete zuerst ohne Änderung. Die Zusatznachricht kam danach als zweite Auslösung um 00:25 Uhr, 20 Minuten vor Schluss der Staffel. Weil vorher nichts erledigt war, wurde der Auftrag dann bearbeitet. Die Recherche ist entsprechend knapp. Alle Quellen am 18. November 2026 abgerufen.

Neu:

- **Sursee** (`data/gemeinden/lu/sursee.json`): Hundesteuer CHF 120 pro Hund und Kalenderjahr, Rechnung Mitte Jahr durch die Abteilung Öffentliche Sicherheit. Anmeldung bei der Stadtverwaltung (Erfassung in AMICUS, Sachbereich Sicherheit und Ordnung). Bitte der Stadt, Schul- und Sportwiesen nicht als Hundewiesen zu nutzen (Schulhaus Neufeld, Rasenfläche zwischen Neu und Alt St. Georg, Fussballfelder Allmend). Die Angaben stammen aus der Zusammenfassung des Abrufwerkzeugs, nicht aus dem vollen Wortlaut der Seite: bei der nächsten Gegenprüfung den Wortlaut vergleichen.

Weggelassen:

- Sursee: Friedhofreglement (sursee.ch/_docn/954685/308Friedhofreglement.pdf) liess sich nicht abrufen. Bussenbeträge nennt die Seite Hundekontrolle nicht. Rechtssammlung (sursee.ch/rechtssammlung) nicht durchsucht (Zeit).

Zurückgestellt:

- **Hochdorf**: nur zwei lokale Angaben belegt. Registrierung neuer Hundehalter bei der Einwohnerkontrolle oder über den Online-Schalter (hochdorf.ch/verwaltung/dienstleistungen.html/358/egov_service/376). Leinenpflicht für Hunde in der Gartenanlage Moosbünte, Nutzungsverordnung vom 16. September 2021, Art. 15 Abs. 4. Die Seite «Hundesteuer» (hochdorf.ch/verwaltung/dienstleistungen.html/358/egov_service/488) und der Online-Schalter (…/online-schalter.html/335/product/81) antworteten mit Serverfehler. Keine Datei angelegt.
- **Willisau**: nur eine bis zwei lokale Angaben belegt. Sportzentrum Schlossfeld: Hunde an der Leine, in Turn- und Sporthallen und Spezialräumen nicht erlaubt (Sportanlagen-Benützungsverordnung Nr. 341 vom 27. März 2025, Art. 11 Abs. 5). Das Finanzamt stellt die Hundesteuer in Rechnung (willisau.ch/verwaltung-politik/verwaltung/finanzamt/), ein Betrag steht dort nicht. WillisauInfo April 2025 gibt nur kantonales Recht wieder. Keine Datei angelegt.

Nicht gelungen: nichts weiter.

## 2026-11-18, Parallel-Lauf `gemeinden-zh-3`, eingesammelt in der Hauptsitzung

Der Lauf begann erst um 00:23 Uhr (Schluss 00:45 Uhr), weil die Zusatznachricht der Staffel nach dem Start eintraf. Je Gemeinde wurde deshalb nur die Hundeseite der Gemeinde abgerufen. `geprueft` steht auf 2026-11-17, weil `build.py` nach der Systemuhr (UTC) rechnet.

Neu: drei Gemeinden im Kanton Zürich, Quellen am 18. November 2026 kurz nach Mitternacht abgerufen.

- **Opfikon** (`data/gemeinden/zh/opfikon.json`): Abgabe CHF 180 inklusive Kantonsbeitrag, Rechnung Ende Februar, zahlbar bis Ende März, halbe Abgabe nach dem 30. Juni, halbe Rückerstattung bei Verlust vor dem 30. Juni, Anmeldung bei der Stadtverwaltung/Allgemeine Dienste innert 10 Tagen, Einschreibegebühr CHF 20, verspätete Meldung CHF 40, Amicus-Mutation nach Aufwand bis CHF 150, Verfügungen CHF 50 und CHF 100 (Art. 23 Gebührentarif Bevölkerungsdienste, so auf der Seite der Stadt wiedergegeben).
- **Thalwil** (`thalwil.json`): Abgabe CHF 170 zuzüglich CHF 30 Kantonsbeitrag, Rechnung im Februar, halbe Abgabe und halbe Rückerstattung (Stichtag 30. Juni), reduzierte Abgabe für Diensthunde auf Gesuch an die Sicherheitskommission, Anmeldung bei der Einwohnerkontrolle innert zehn Tagen, Abmeldung über den Online-Schalter.
- **Adliswil** (`adliswil.json`): Hundesteuer CHF 180 inklusive Kantonsbeitrag, einmalige Anmeldegebühr CHF 20, Anmeldung bei der Polizei Adliswil - Langnau am Albis innert zehn Tagen.

Zurückgestellt:

- **Kloten**: nur zwei lokale Angaben belegt (Jahresgebühr CHF 200 pro Hund, Anmeldung innert 10 Tagen bei der Abteilung Sicherheit; https://www.kloten.ch/dienstleistungen/23865). Der «Flyer für Hundebesitzer» (https://www.kloten.ch/_doc/1293491) liess sich nicht abrufen. Keine Datei angelegt.

Weggelassen:

- Alle Angaben beruhen auf der Wiedergabe des Abrufwerkzeugs mit wörtlichen Zitaten, nicht auf dem selbst gelesenen Volltext. Bei der Gegenprüfung am Volltext bestätigen.
- Thalwil: Der Satz «Allgemeine Leinenpflicht auf öffentlichen Strassen, Plätzen und Schularealen» steht auf der Seite unter den Vorschriften «im Kanton Zürich», ohne Rechtsgrundlage. Unklar, ob das eine Thalwiler Regel ist. Nicht übernommen. Polizeiverordnung nicht gesucht (Schluss-Zeit).
- Opfikon: Das Dokument «Ordnungsbussen Hundehalter» (https://www.opfikon.ch/_doc/5561251) und die Broschüre Hundehaltung 2025 (https://www.opfikon.ch/_doc/5875948) liessen sich nicht abrufen. Keine Bussen übernommen. Polizeiverordnung nicht gesucht.
- Adliswil: Die Seite nennt weder Leinenpflicht noch Verbote, Bussen oder Kotaufnahme. Polizeiverordnung nicht gesucht.

Nicht gelungen: Kloten, siehe oben.

## 2026-11-18, Parallel-Lauf `gemeinden-zh-4`, eingesammelt in der Hauptsitzung

Neu: drei Gemeinden im Kanton Zürich, alle Quellen am 18. November 2026 abgerufen. Der Lauf hatte bis zum Schluss der Staffel rund 20 Minuten, die Recherche ist entsprechend knapp.

- **Regensdorf** (`data/gemeinden/zh/regensdorf.json`): Anmeldung online oder per E-Mail bei den Einwohnerdiensten innert 10 Tagen, Meldegebühr CHF 20, Unterlagen, Rechnung der Hundesteuer im Februar oder März.
- **Volketswil** (`volketswil.json`): Hundeabgabe CHF 180 inklusive CHF 30 Kanton, halbe Abgabe nach dem 30. Juni, Polizeiverordnung 2024 Art. 5 (Tierhaltung) und Art. 25 (Busse ohne Betrag).
- **Illnau-Effretikon** (`illnau-effretikon.json`): Hundeabgabe CHF 150 oder CHF 75 nach dem 30. Juni, Meldung gratis oder verspätet CHF 20, Vermittlung entlaufener Hunde CHF 20. Alles aus dem Gebührenreglement mit Stand 1. Januar 2019, der Stand steht in jeder Karte.

Weggelassen:

- Regensdorf: Den Betrag der Hundesteuer nennt keine der drei abgerufenen Seiten. Polizeiverordnung nicht gesucht (Zeit).
- Volketswil: Anmeldestelle und Meldegebühr fehlen, die Seite «An- und Abmeldungen» liess sich nicht abrufen (robots). Der Beschluss zur Hundeabgabe von 2017 wurde nicht selbst gelesen, der Betrag stammt von der Seite der Sicherheitsabteilung. Die Polizeiverordnung nennt keine Leinenpflicht, keine Hundeverbote und keine Kotaufnahmepflicht.
- Illnau-Effretikon: Kursermässigung CHF 50 und Registrierung bei AMICUS durch die Gemeinde (bis CHF 150) stehen im Reglement von 2019, wurden aber nicht übernommen, weil sie auf dem Hundegesetz vor der Revision vom 1. Juni 2025 beruhen. Das Anmeldeformular (ilef.ch/formular/hunde-anmeldung/) liess sich nicht abrufen. Polizeiverordnung nicht gesucht (Zeit).

Zurückgestellt:

- **Schlieren**: nur zwei lokale Angaben belegt (Hundeabgabe CHF 170 pro Hund und Jahr, Anmeldung für Ersthundehaltende bei den Einwohnerdiensten, beides https://www.schlieren.ch/dienstleistungen/123752). Die Ordnungsbussenverordnung SKR 6.12 (Stand 2013) verweist für Hunde nur auf das kantonale Recht. Keine Datei angelegt.

Nicht gelungen: nichts.

## 2026-11-18, Parallel-Lauf `ar`, eingesammelt von Glied 8

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

## 2026-11-18, Parallel-Lauf `zg`, eingesammelt von Glied 8

- Neu: `data/kantone/zg.json` (Kanton Zug) mit sieben Quellen in `data/quellen/zg.json`.
- Belegt: Leinenpflicht im Wald und am Waldrand vom 1. April bis 31. Juli (Seite «Freizeit und Erholung im Wald» und Medienmitteilung vom 27. März 2025, Grundlage Einführungsgesetz zum Waldgesetz, in Kraft seit 1. Januar 2025). Eine Meterangabe zum Waldrand nennt keine der Quellen, deshalb steht keine auf der Seite.
- Der Kanton Zug hat laut Veterinärdienst kein eigenes Hunderecht: «Für das Halten von Hunden ist die eidg. Tierschutzverordnung und die Gesetze und Reglemente der Zuger Gemeinden massgebend.» Die Karten Haftpflicht, Kurs und Rassen sagen deshalb nur das (Ton `note`) und verweisen auf das Reglement der Gemeinde. Sie behaupten nicht «keine Pflicht».
- Die Leinen-Orte ausserhalb des Waldes sind auf der Seite des Kantons Empfehlungen und als solche gekennzeichnet. Die Orte ohne Hunde stehen mit Einleitung, dass die Regeln der Gemeinde verbindlich sind.
- Hundesteuer: kantonal nur belegt, dass die Hundedaten für die Erhebung der Hundesteuer dienen (VV Tierseuchengesetz § 18a). Als Beispiel Steinhausen CHF 70 (Merkblatt 2025), ausdrücklich als Beispiel.
- Quelle `zg_vorfaelle`: abgerufen wurde die Adresse unter `/it/…`, der Inhalt ist derselbe deutsche Text. Die deutsche Adresse liess sich im Lauf nicht direkt abrufen.
- Weggelassen: Paragraf des Einführungsgesetzes zum Waldgesetz, Bussenhöhe, Kotaufnahmepflicht (kantonal nicht belegt).
- Nicht gelungen: Das «Infoblatt Hundereglemente der Gemeinden im Kanton Zug» des Veterinärdienstes (cdn.zg.ch, Ausgaben März 2025 und Oktober 2026) war nicht abrufbar (Abruf nicht freigegeben, publiclogin2.zg.ch verlangt Cookies).
- Nicht gelungen: Stadt Zug. Die Seiten von stadtzug.ch (Dienstleistungen 1727 und 1965) und der Stadtratsbeschluss Nr. 20.19 vom 15. Januar 2019 zur Leinenpflicht (lesesaal.stadtzug.ch) lieferten Fehler. Keine einzige lokale Angabe belegt, keine Datei angelegt.

## 2026-11-18, Parallel-Lauf `nw`, eingesammelt von Glied 8

- Neu: `data/kantone/nw.json` (Kanton Nidwalden) mit sieben Quellen in `data/quellen/nw.json`.
- Belegt aus aktuellen amtlichen Quellen: Hundesteuer CHF 120 pro Kalenderjahr, Anmeldung beim Amt für Justiz spätestens drei Monate nach der Geburt, Mutationen innert 10 Tagen (nw.ch, Hundekontrolle). Ordnungsbussen CHF 100 und CHF 300 (kOBV, Stand 1. September 2026). Meldestelle Kantonstierarzt (nw.ch, Gefährliche Hunde).
- Vorbehalt Hundegesetz: Die amtliche Sammlung gesetze.nw.ch liefert im Lauf nur eine leere Skript-Seite. Gelesen wurde die Fassung auf LexFind (tolv/63743), die nur das Inkrafttreten am 1. Januar 2005 nennt. Angaben, die allein daraus stammen (Verbot auf Friedhöfen, Spielplätzen, in Strandbädern; Leine auf Sportplätzen und in Schulhausanlagen; keine Haftpflicht, kein Pflichtkurs, keine Rasseliste), tragen im Text den Hinweis «Fassung von 2005». Die kOBV von 2026 verweist weiterhin auf Art. 19 Ziff. 1 bis 7 des Hundegesetzes, die Struktur gilt also noch. Haftpflicht, Kurs und Rassen stehen deshalb mit Ton `note`, nicht `none`.
- Wald: keine feste Leinenzeit in Hundegesetz und Jagdverordnung gefunden (`saison: false`). Die Verordnung über die Wildruhegebiete (NG 841.15) nennt in § 3 Abs. 2 eine Leinenpflicht für Hunde. Abgerufen wurde nur die Inhaltsübersicht (lexaris.de, Stand 31. Dezember 2019). Gebiete und Daten sind deshalb weggelassen.
- Weggelassen: Daten der Leinenpflicht in den Wildruhegebieten (nur bei tierimrecht.org gefunden, nicht amtlich), Strafrahmen des Hundegesetzes («Haft oder Busse», veraltet), Steuerbefreiung bei Zahlung in einem anderen Kanton (nur Fassung von 2005).
- Nicht gelungen: gesetze.nw.ch (alle Erlasse, nur Skript-Seite), laburk.ch (Abruf nicht freigegeben).
- Nicht gelungen: Stans. Die Hundesteuer und die Hundekontrolle sind in Nidwalden kantonal. Auf stans.ch keine lokale Angabe zu Hunden gefunden (Strassenreglement: nichts zu Hunden). Null belegte lokale Angaben, keine Datei.

## 2026-11-18, Parallel-Lauf `sh`, eingesammelt von Glied 8

Neu:
- `data/kantone/sh.json`: Kanton Schaffhausen, alle Felder belegt. Sechs Quellen in `data/quellen/sh.json`.
- Wald: Leinenpflicht im Wald und in Waldesnähe vom 15. April bis 30. Juni (Merkblatt des Veterinäramts, das Gesetz nennt nur «Setz- und Brutzeit»).
- Haftpflicht mind. CHF 1 Mio., Anmeldung innert 10 Tagen bei der Wohnsitzgemeinde, Hundeabgabe CHF 100 bis 200 je nach Gemeinde, Bewilligungspflicht für Rassentypen mit erhöhtem Gefährdungspotenzial, Busse bis CHF 10 000.
- `data/gemeinden/sh/schaffhausen.json`: Stadt Schaffhausen mit drei lokalen Angaben: Leine in öffentlichen Anlagen (Polizeiverordnung Art. 30, Stand 2016), Hunde auf den Friedhöfen nur mit Bewilligung (Friedhofreglement Art. 20), Busse bis CHF 1000 (Polizeiverordnung Art. 59).

Einschränkung, wichtig für die nächste Prüfung:
- Die geltende Fassung von Hundegesetz (SHR 455.200) und Hundeverordnung (SHR 455.201) liess sich nicht abrufen: rechtsbuch.sh.ch liefert den Text nur per Skript. Gelesen wurden die Fassungen auf lexfind.ch (Gesetz Stand 2010, Verordnung von 2009). Jede Angabe, die nur aus diesen Fassungen stammt, nennt auf der Seite den Stand. Durch das aktuelle Merkblatt des Veterinäramts bestätigt sind: Haftpflichtnachweis, 10-Tage-Frist, AMICUS, Hundeabgabe, Leinenpflicht im Wald mit Daten, Kotaufnahme, Bewilligungspflicht. Der Rahmen CHF 100 bis 200 wird 2023 in einer Kleinen Anfrage im Grossen Stadtrat Schaffhausen genannt.
- Die Seiten «Haltung und Betreuung von Hunden» und «Bewilligungspflichtige Hunde» des Veterinäramts auf sh.ch liefern ebenfalls keinen lesbaren Text.

Weggelassen und warum:
- Zahl der bewilligungspflichtigen Rassentypen: Die Verordnung von 2009 nennt vier, das aktuelle Merkblatt vierzehn und weitere Züchtungen. Die Seite zählt nicht, sondern führt die im Merkblatt genannten Typen auf.
- Kantonsbeitrag an der Hundeabgabe (CHF 20 laut Verordnung von 2009): Stand unklar, für Halterinnen und Halter ohne Belang.
- Kurs: Das Gesetz verweist auf den Ausbildungsnachweis nach Bundesrecht. Ob das heute noch eine Pflicht bedeutet, steht in keiner abgerufenen Schaffhauser Quelle. Die Karte hat deshalb den Ton `note` und behauptet weder Pflicht noch «keine Pflicht».
- Hundeabgabe der Stadt Schaffhausen: Betrag in keiner abrufbaren amtlichen Quelle gefunden (Formular zur Rückerstattung und Verwaltungsbericht 2022 nicht abrufbar). Keine Karte Hundetaxe.

## 2026-11-18, Parallel-Lauf `gl`, eingesammelt von Glied 8

Neu:
- `data/kantone/gl.json`: Kanton Glarus, alle Felder belegt. Fünf Quellen in `data/quellen/gl.json`.
- Wald: Leinenpflicht ganzjährig im Wald und den Waldrändern entlang (Jagdverordnung Art. 30 Abs. 1, Stand 1. Januar 2026). Keine Saison, deshalb `saison: false`.
- Versicherungspflicht mit Kopie der Police ans Einwohneramt innert eines Monats (Veterinärverordnung Art. 28), kantonale Hundetaxe CHF 55 plus Gemeindezuschlag (Art. 31), Bewilligungspflicht für 10 Rassen und Mischlinge (Art. 19 bis 25, Stand 1. Januar 2024, Hovawart und Rhodesian Ridgeback sind seit 2024 gestrichen), Leinenpflicht in den eidgenössischen Jagdbanngebieten (Vollzugsregelung von 2015, mit Stand genannt).
- Leinenpflicht in Gebäuden, an stark befahrenen Strassen, im öffentlichen Verkehr, auf Pausen-, Spiel- und Sportplätzen und an signalisierten Orten: Die Seite der Gemeinde Glarus führt diese Liste unter dem Titel des kantonalen Tierschutz- und Tierseuchengesetzes. Beim Kanton mit dieser Quelle aufgenommen, am Gesetzestext noch nicht abgeglichen.
- `data/gemeinden/gl/glarus.json`: Gemeinde Glarus mit drei lokalen Angaben: Hundetaxe CHF 190 (CHF 135 Gemeinde, CHF 55 Kanton, seit 1. Januar 2019), Anmeldestelle Einwohnerdienste mit Fristen, Kotaufnahme auf dem ganzen Gemeindegebiet. Dazu eine Karte Leine, die das kantonale Recht wiedergibt und nicht als lokale Angabe zählt.

Einschränkung, wichtig für die nächste Prüfung:
- Das Einführungsgesetz zum Tierschutzgesetz und zum Tierseuchengesetz (GS IV G/3/2) liess sich in zwei Versuchen nicht abrufen: gesetze.gl.ch liefert den Text nur per Skript, auf lexfind.ch nicht gefunden. Alle Angaben stammen aus der Veterinärverordnung, der Jagdverordnung, der Seite der Fachstelle Hundewesen und der Seite der Gemeinde Glarus.
- Das Merkblatt zur bewilligungspflichtigen Hundehaltung (gr.ch) war nicht abrufbar (Fehler des Servers). Die Rasseliste steht übereinstimmend in der Veterinärverordnung und auf der Seite Hundewesen.

Weggelassen und warum:
- Deckungssumme der Haftpflicht, Bussenbeträge, Kotaufnahmepflicht auf Kantonsebene: in keiner abgerufenen kantonalen Quelle.
- Orte mit Hundeverbot: Die gelesenen Verordnungen nennen keine. Der Abschnitt «Verbot» sagt das und nennt die zwei belegten Verbote (Haltung ohne Bewilligung, frei laufen lassen im Wald).
- Karte Kurs hat den Ton `note`: Die Nachweispflicht gilt für Ersthundehalter und für Hunde der Rasseliste, nicht allgemein.
- AMICUS-Frist von 10 Tagen: steht nur auf der Seite der Gemeinde Glarus, deshalb dort.

## 2026-11-18, Parallel-Lauf `fr-fr`, eingesammelt von Glied 8

**Neu:** Kanton Freiburg deutsch (`data/kantone/fr.json`) und französisch (`data/fr-ch/kantone/fr.json`), Ville de Fribourg französisch (`data/fr-ch/gemeinden/fr/fribourg.json`), 16 Quellen in `data/quellen/fr-fr.json`. Alle Quellen in der Nacht vom 17. auf den 18. November 2026 abgerufen. `geprueft` steht auf 2026-11-17, weil `build.py` das Datum vom 18. noch als Zukunft ablehnte.

- LDCh / HHG (RSF/SGF 725.3, Fassung seit 1. Januar 2024, französisch und deutsch gelesen): Haftpflicht (Art. 39), Theoriekurs und Beurteilung der Führbarkeit (Art. 28a, 12 Abs. 3), Verbot Typ Pitbull und Kreuzungen mit Aufenthalt bis 90 Tage an Leine und mit Maulkorb (Art. 20), Leinen- und Verbotszonen der Gemeinden, nicht für das ganze Gemeindegebiet (Art. 30), Kot (Art. 37), Gemeindesteuer höchstens CHF 200 (Art. 50). Art. 19 (Bewilligung) ist aufgehoben.
- RDCh (RSF 725.31 vom 13. Juni 2023, Fassung seit 1. Januar 2024, nur französisch gelesen): Haftpflicht mindestens CHF 1 Million pro Ereignis (Art. 27), Theoriekurs mindestens fünf Stunden (Art. 11, 12), Beurteilung innert 18 Monaten ab Eintrag in AMICUS (Art. 13, 14), Meldung von Adressänderung und Tod innert fünfzehn Tagen (Art. 4), kantonale Steuer CHF 100 (Art. 30), Leine im Wald 1. April bis 15. Juli (Art. 26).
- Seiten von fr.ch in beiden Sprachen: neue Hundehaltende (Kurs, AMICUS innert 10 Tagen), verbotene Hunde, Hundegebühr (CHF 100 plus CHF 5, Oberämter), Verhalten im Wald (Leine 1. April bis 15. Juli, Biotope, Rückruf).
- OCAO (RSF 33.11, Fassung seit 1. Juli 2024): FR 104, CHF 100, Hund nicht unter Kontrolle. Nur in der französischen Datei.
- Ville de Fribourg: Règlement concernant l'impôt communal sur les chiens von 1993 (CHF 120, Befreiungen, Busse CHF 30 bis 100), Règlement général de police vom 4. Juli 2023 (Art. 48 bis 50, 54: Leinenorte, Kot, Streunen, Busse CHF 20 bis 1000), Règlement du cimetière communal 2024 (Art. 4 Abs. 3: Leine).

**Entscheide:**

- Die Stadt Freiburg bekommt nur eine französische Seite. Ihre Amtssprache ist Französisch. Eine deutsche Gemeinde-Datei gibt es nicht.
- Die deutsche Kantonsdatei belegt die Mindestdeckung von CHF 1 Million mit dem französischen RDCh von 2024. Die geltende deutsche Fassung des HHR war nicht abrufbar (bdlf.fr.ch liefert auf Deutsch nur die Fassung von 2019, die denselben Betrag in Art. 50 nennt). Aus der Fassung von 2019 ist nichts übernommen.
- Die Frist «innert fünfzehn Tagen» für Adressänderung und Tod steht nur in der französischen Datei, die deutsche Seite von fr.ch nennt sie nicht.
- Der französische Wortlaut des Polizeireglements stammt aus der Bekanntmachung des Generalratsbeschlusses, das Datum des Inkrafttretens (1. Januar 2025) aus der deutschen konsolidierten Fassung der Stadt. Beide sind als Quelle angegeben.
- Das Polizeireglement von 1990 (Stand 2018) steht noch auf der Website der Stadt, ist aber durch Art. 57 des neuen Reglements aufgehoben. Nicht verwendet.

**Weggelassen:**

- Ordnungsbusse für die Leine im Wald: Die Zuordnung von FR 107 (CHF 150) zu Art. 49 Abs. 1 stand nur im Reglement von 2019. Die OCAO von 2024 wurde nur zusammengefasst gelesen. Keine Angabe.
- Art. 20 Abs. 1 Bst. c LDCh erscheint im Text als «…». Keine Angabe.
- Übergangsfrist für bestehende Hunde (Art. 56a HHG): Wortlaut nicht eindeutig gelesen. Keine Angabe.
- Bewilligung für mehr als vier Hunde: steht in der Fassung 2024 des Gesetzes nicht mehr dort, wo sie 2022 stand. Die Seite von fr.ch dazu wurde nicht abgerufen. Keine Angabe.
- Meter ab Waldrand: Weder Reglement noch Seite nennen einen Abstand. `wo` ist «im Wald» / «en forêt».

**Nicht gelungen:** nichts.

## 2026-11-18, Parallel-Lauf `vd-fr`, eingesammelt von Glied 8

- Neu: Kanton Waadt französisch (`data/fr-ch/kantone/vd.json`), fünf Quellen in `data/quellen/vd-fr.json`. Alle Quellen in diesem Lauf abgerufen. Geprüft über eine vorübergehende Kopie unter `data/kantone/`, Build und Test fehlerfrei.
- `geprueft` steht auf 2026-11-17, weil `build.py` das Datum 2026-11-18 (Schweizer Zeit, kurz nach Mitternacht) als «in der Zukunft» ablehnt.
- Belegt: Leinenpflicht 1. April bis 15. Juli im Wald, an seinen Rändern und auf angrenzenden Wiesen (Faltblatt der DGE, Art. 2a RLFaune), Haftpflicht für alle (LPolC Art. 15, ohne Mindestsumme), Meldung innert zwei Wochen (Art. 9), Bewilligung für Amstaff, American Pit Bull Terrier, Rottweiler und Kreuzungen (RLPolC Art. 2, Gebühr CHF 800), 72 Stunden Kurs nur für diese Hunde (RLPolC Art. 11), Kantonssteuer CHF 100, Busse bis CHF 20 000 (LPolC Art. 34).
- Karte Kurs mit `ton: note`: keine allgemeine Kurspflicht im Gesetz, nur für potenziell gefährliche Hunde.
- Unsicherheit: Die LPolC wurde in der Fassung «in Kraft seit 1. Mai 2014» gelesen (LexFind, dort als aktuell bezeichnet, Dokument erzeugt 2019), das RLPolC als PDF von 2014. Ob es seither Änderungen gab, ist nicht geprüft. Der Stand steht im Langnamen und in der Karte Kurs. Das Faltblatt zur Leinenpflicht trägt kein Datum. Der Wortlaut von Art. 2a RLFaune selbst wurde nicht abgerufen.
- Weggelassen: Mindestsumme der Haftpflicht (steht in keiner Quelle), AMICUS beim Kanton (das Gesetz sagt nur «banque de données»), Regeln für Besuch mit Listenhunden aus anderen Kantonen (nicht gefunden), Pflicht zum Aufnehmen von Kot (nicht in der LPolC), Jahr des Steuerbetrags (die Seite nennt keines).
- Neu: Ville de Lausanne französisch (`data/fr-ch/gemeinden/vd/lausanne.json`), drei Karten (Impôt sur les chiens CHF 190, davon CHF 90 Gemeinde; Annonce innert 15 Tagen; Laisse), drei weitere Quellen. Weggelassen: Namen der Freilaufzonen (stehen nur auf einer Karte, nicht im Text der Seite), Verbotsorte und Bussen (Règlement général de police der Stadt nach einem Suchversuch nicht gefunden, Schluss-Zeit nahe).
- Nicht gelungen: nichts.

## 2026-11-18, Parallel-Lauf `ne-fr`, eingesammelt von Glied 8

- Neu: Kanton Neuenburg französisch (`data/fr-ch/kantone/ne.json`), sieben Quellen in `data/quellen/ne-fr.json`. Alle Quellen in diesem Lauf abgerufen. Geprüft über eine vorübergehende Kopie unter `data/kantone/`, Build und Test fehlerfrei.
- `geprueft` steht auf 2026-11-17, wie bei `vd-fr` (der Lauf lief kurz nach Mitternacht Schweizer Zeit).
- Belegt: Leinenpflicht im Wald 15. April bis 30. Juni (LFS Art. 21 Abs. 4, Faltblatt 2024), Beherrschen durch Stimme oder Geste, sonst Leine (LChiens Art. 12, LFS Art. 21 Abs. 3), Hundetaxe höchstens CHF 120 samt CHF 30 Staatsanteil (LChiens Art. 3 und 7), Befreiungen (Art. 4, RELChiens Art. 3), Busse bis zum Doppelten der hinterzogenen Taxe (Art. 8), Kurspflicht für neue Halter (LChiens Art. 19 Abs. 2, Einzelheiten von der Seite des SCAV: 2 Stunden Theorie, 8 Lektionen zu 45 Minuten, Beginn innert 6 Monaten), Massnahmen im Einzelfall (Art. 17), Kot (Art. 14), Busse bis CHF 40 000 nach LFS Art. 72.
- Karte Kurs mit `ton: must`: Die Pflicht gilt für alle, die erstmals einen Hund halten. Karten Haftpflicht und Rassen mit `ton: none`: Die LChiens enthält laut gezielter Abfrage weder die Wörter «assurance» und «responsabilité civile» noch eine Rasseliste.
- Unsicherheit: Die Gesetzestexte wurden über WebFetch gelesen, das lange Artikel nur in Stücken oder zusammengefasst wiedergibt. Art. 4, 5, 7, 8, 14 und 17 LChiens liegen nur als Zusammenfassung vor. Die Quelle `ne_scav` ist eine Adresse auf ne.ch, die auf eine Sammelseite des SCAV führt, nicht auf das Kursreglement selbst. Das Kursreglement des Staatsrats wurde nicht gefunden.
- Weggelassen: Meldefrist (weder LChiens noch SCAV nennen eine, die Frist des Bundesrechts wurde nicht abgerufen), Mindestsumme einer Haftpflicht, Kurspreis (nur Schätzung des SCAV), Höhe der Busse nach LChiens (Art. 20 nennt keinen Betrag), Regeln für Weiden und Waldrand (stehen in keiner Quelle), Feld `umzug`.
- Neu: Ville de Neuchâtel französisch (`data/fr-ch/gemeinden/ne/neuchatel.json`), vier Karten (Laisse, Accès interdit, Annonce, Amendes), zwei Quellen. Das Faltblatt «Mon chien en ville» trägt kein Datum, der Dateiname nennt 2022, das steht als Stand im Text. Das Polizeireglement wurde in einer Fassung mit Änderungen bis 2015 gelesen.
- Weggelassen bei Neuchâtel: Betrag der Hundetaxe (das Reglement vom 17. November 2025 verweist nur auf das kantonale Gesetz, das Faltblatt nennt keinen Betrag), Namen der Freilaufzonen (nur auf einem Plan, Zuordnung unklar), Meldefrist.
- Nicht gelungen: nichts.

## 2026-11-18, Parallel-Lauf `gemeinden-zh-1`, eingesammelt von Glied 8

Neu: vier Gemeinden im Kanton Zürich, alle Quellen am 18. November 2026 abgerufen.

- **Winterthur** (`data/gemeinden/zh/winterthur.json`): Hundeabgabe CHF 160 plus Kantonsbeitrag CHF 30, Meldegebühr CHF 20, Anmeldung bei der Einwohnerkontrolle, kurze Leine im Wildpark Bruderhaus.
- **Uster** (`uster.json`): Hundeabgabe CHF 200 (inklusive CHF 30 Kanton), Anmeldung CHF 10 bei den Einwohnerdiensten, Kotaufnahmepflicht in der ganzen Stadt, Übersichtsplan Wald und Waldrand (Stand 2023), Hinweis Greifensee.
- **Dübendorf** (`duebendorf.json`): Hundesteuer CHF 150, jeder weitere Hund CHF 170, Anmeldung bei den Einwohnerdiensten, Kotaufnahmepflicht auf dem ganzen Gemeindegebiet und Busse bis CHF 500 (Polizeiverordnung, gültig ab 2014).
- **Dietikon** (`dietikon.json`): Hundeabgabe CHF 160, Meldegebühr CHF 20 oder verspätet CHF 40, Anmeldestelle, Vermittlung entlaufener Hunde CHF 50.

Weggelassen:

- Winterthur: Der Stadtratsbeschluss vom 23. Juni 2021 zur Hundeabgabe liess sich nicht abrufen (Adresse zu lang für WebFetch). Der Betrag stammt aus dem Merkblatt Hundewesen, das kein Datum trägt. Die Nutzungsordnung Eulachpark war nicht abrufbar (Fehler der Website). Lokale Leinenpflicht, Hundeverbote und Bussen: auf den abgerufenen Seiten nichts gefunden.
- Uster: Die «Verhaltensempfehlungen Stadtpark» der Stadtpolizei (keine generelle Leinenpflicht im Stadtpark) tragen kein Datum und sind eine Empfehlung, deshalb nicht übernommen. Die Polizeiverordnung (Ausgabe 2010) nennt Hunde nicht eigens. Bussenbeträge nicht gefunden.
- Dübendorf: Ob die CHF 150 den Kantonsbeitrag enthalten, sagt die Seite nicht, deshalb steht dazu nichts. Die Polizeiverordnung kennt keine lokale Leinenpflicht und keine Hundeverbote. Die Datei der Verordnung heisst «vom 24. April 2015», im Text steht «gültig ab 3. November 2014».
- Dietikon: Die Polizeiverordnung (Nr. 510.1, in Kraft seit 1. März 2023, https://www.dietikon.ch/_doc/7194661) liess sich nicht abrufen. Leine, Verbote, Kot und Bussen fehlen deshalb.

Nicht gelungen: nichts.

## 2026-11-18, Parallel-Lauf `gemeinden-zh-2`, eingesammelt von Glied 8

Neu: drei Gemeinden im Kanton Zürich, alle Quellen am 18. November 2026 kurz nach Mitternacht abgerufen. `geprueft` steht auf 2026-11-17, weil `build.py` nach der Systemuhr (UTC) rechnet und den 18. als Zukunft ablehnt.

- **Wetzikon** (`data/gemeinden/zh/wetzikon.json`): Hundesteuer CHF 180 inklusive CHF 30 Kanton, CHF 90 bei Übernahme nach dem 30. Juni, Anmeldung bei den Einwohnerdiensten, CHF 30 für die Amicus-Meldung durch die Stadt bei Nichtanmeldung (Gebührentarif Ziff. 7.2, Stand 8. Juli 2026), Hundekot nach Art. 22 der Polizeiverordnung vom 9. März 2026 (in Kraft seit 1. August 2026). Die Polizeiverordnung kennt keine eigene Leinenpflicht und keine Hundeverbote für Orte, das steht so auf der Karte «Leine».
- **Wädenswil** (`waedenswil.json`): Hundesteuer CHF 150, Anmeldegebühr CHF 20, verspätet CHF 40, Online-Dienst, Stabstelle Gesellschaft bei Ersthunden, Robidog-Säcke gratis bei den Einwohnerdiensten.
- **Bülach** (`buelach.json`): Jahresgebühr CHF 170, zahlbar bis 31. März, danach höher (Betrag nicht genannt), 50 Prozent Reduktion im Abschlussjahr des Hundehalter-Brevets, Teilrückerstattung bei Tod des Hundes vor dem 30. Juni, Anmeldung bei der Stadtpolizei.

Zurückgestellt:

- **Horgen**: nur zwei lokale Angaben belegt (Gebührentarif gültig ab 1. Januar 2022, Art. 50: «Ersthunde, jährlich Fr. 130.00», verspätetes Anmelden CHF 40). Die Seiten «Hunde» und «Hundekontrolle: Anmeldung» von horgen.ch gaben zweimal einen Serverfehler. Von der Allgemeinen Polizeiverordnung (https://www.horgen.ch/public/upload/assets/445/2012_Polizeiverordnung.pdf?fp=3) liess sich nur Inhalts- und Stichwortverzeichnis lesen. Es nennt bei Art. 11 Tierhaltung die Stichworte Leinenpflicht und Hundekot, der Wortlaut fehlte. Keine Datei angelegt.

Weggelassen:

- Wetzikon: Die Wiedergabe von Art. 22 und 23 der Polizeiverordnung beruht auf einer Zusammenfassung des Abrufwerkzeugs, nicht auf dem vollen Wortlaut. Bei der Gegenprüfung den Wortlaut und die Aussage «keine eigene Leinenpflicht» am Volltext bestätigen. Ordnungsbussen legt der Stadtrat fest, Beträge nicht gefunden. Stadtratsbeschluss zur eingezäunten Hundewiese (20. September 2023) nicht gelesen.
- Wädenswil: Ob die CHF 150 den Kantonsbeitrag enthalten, sagt die Seite nicht. Die Seite des Online-Schalters war nicht abrufbar. Polizeiverordnung nicht gesucht (Schluss-Zeit).
- Bülach: Ob die CHF 170 den Kantonsbeitrag enthalten, sagt die Seite nicht. Betrag der Gebühr für verspätete Meldungen und der erhöhten Gebühr ab 1. April steht im Gebührenreglement, das nicht gefunden wurde. Polizeiverordnung nicht gefunden.

Nicht gelungen: Horgen, siehe oben.

## 2026-11-18, Parallel-Lauf `pruefung-bl`, eingesammelt von Glied 8

Gegenprüfung von `data/kantone/bl.json` und `data/gemeinden/bl/allschwil.json`. Alle neun Quellen abgerufen (`bl_hug`, `bl_pgh`, `bl_wjg`, `bl_wjv`, `bl_wald`, `bl_allschwil_hunde`, `bl_allschwil_gebuehren`, `bl_allschwil_pr`, `bl_allschwil_prv`). 61 Angaben verglichen (Kanton 38, Allschwil 23). 59 stimmen, 2 angepasst. `geprueft` bleibt in beiden Dateien 2026-11-17, weil `build.py` nach UTC rechnet und den 18. noch als Zukunft ablehnt.

Geändert:

- Kanton BL, `leine`, vierter Punkt. Alt: «an weiteren Orten, die deine Gemeinde bestimmt, zum Beispiel bei Dunkelheit, an verkehrsreichen Stellen oder in bestimmten Gebieten». Neu: «an weiteren Orten oder zu weiteren Zeiten, die deine Gemeinde bestimmt, zum Beispiel bei Dunkelheit oder an verkehrsreichen Stellen». Grund: § 3 Abs. 2 lit. b Hundegesetz nennt als Beispiele nur Dunkelheit und verkehrsreiche Stellen, «bestimmte Gebiete» war nicht zu belegen.
- Allschwil, Karte Hundetaxe. Alt: «Befreit sind unter anderem Diensthunde, Blindenführhunde sowie Sozial-, Therapie-, Assistenz- und Begleithunde.» Neu: «Befreit sind unter anderem Diensthunde, Blindenführhunde, Assistenz- und Begleithunde sowie Sozial- und Therapiehunde, die unentgeltlich in sozialen Institutionen eingesetzt werden.» Grund: § 13 der Verordnung zum Polizeireglement befreit Sozial- und Therapiehunde nur bei unentgeltlichem Einsatz in sozialen Institutionen.

Bestätigt, unter anderem: Leinenpflicht 1. April bis 31. Juli im Wald und in Waldesnähe (§ 12 WJG), Wildruhegebiete samt begrenzenden Waldstrassen und ausgeschilderten Wanderwegen (§ 3 WJV), Haftpflicht CHF 3 Millionen, Meldefrist 14 Tage, entlaufene Hunde 2 Tage, acht Rassen, weiterer Hund 16 Wochen, Gesuch CHF 250, Zuzug 4 Wochen. Allschwil: CHF 150 und CHF 75, Leinenorte nach § 35, Freilaufwege mit roten Streifen, Wiesland November bis Februar, Bussen CHF 50 und CHF 100, Höchstbusse CHF 5'000.

Hinweise ohne Änderung:

- Die Adresse «Baslerstrasse 111» steht auf der Seite der Einwohnerdienste Allschwil nur in den Angaben zur Seite, nicht im Lauftext. Belassen.
- Das Hundegesetz liegt auf LexFind mit Stand 1. Januar 2008 vor. Eine neuere Fassung ist dort nicht ausgewiesen.
- Die Texte kamen über WebFetch als Auszug mit kurzen Zitaten, nicht als Volltext. Geprüft wurde jede Angabe gezielt gegen diese Auszüge.

## 2026-11-18, Nachtkette, Glied 7

- Nachgeprüft: nichts, keine Datei ist älter als 60 Tage. Eingesammelt: Parallel-Lauf `gr` (eigener Eintrag unten). Alle offenen Kantone sind an Parallel-Läufe vergeben (Staffeln von 23:55 Uhr), deshalb vier Gemeinden aus Abschnitt 3, die nicht vergeben sind.
- Neu: Bezirk Einsiedeln (`/sz/einsiedeln/`), Gemeinde Arth (`/sz/arth/`), Gemeinde Davos (`/gr/davos/`), Gemeinde Landquart (`/gr/landquart/`). 12 von 26 Kantonen, 17 Gemeinden, Sitemap 38 Seiten. Alle Quellen am 18. November 2026 (Schweizer Zeit) abgerufen. `geprueft` steht auf 2026-11-17, weil `build.py` mit der Systemzeit (UTC) rechnet.
- Einsiedeln: Anmeldeformular des Bezirks (CHF 100, weiterer Hund CHF 200, Nutzhund CHF 40, ab vier Monaten, verlangt Haftpflicht mit Policennummer) und Broschüre ohne Datum (Steuersätze ab 2012: Bezirkskasse, Rechnung im Februar, Gratis-Säcke). Der Stand steht auf der Seite. Eigene Leinenorte oder Verbote nennt der Bezirk nicht.
- Arth: Dienstleistung Hundesteuer (CHF 100, weiterer CHF 200, Nutzhund CHF 40, Zucht CHF 500, Kassieramt, AMICUS). Leine auf den Friedhöfen Arth und Goldau: Art. 18 des Friedhofreglements vom 26. August 2016, angenommen am 21. Mai 2017 (80,19 % Ja). Gelesen wurde die Fassung der Abstimmungsvorlage. Die Genehmigung durch den Regierungsrat ist nicht belegt, als Lücke im Backlog.
- Davos: Gemeindegesetz über das Halten von Hunden (DRB 32, Stand 1. Juni 2023), Verordnung vom 25. Februar 2020 (DRB 32.1), Dienstleistung Hunde. Taxe CHF 120 und CHF 240, Leine in Parkanlagen, auf Spielplätzen, in Wildasylen und im Waldgebiet (ohne Jahreszeit), Verbot in Schulen, Amtslokalen, auf Skipisten und Loipen, Anmeldung innert 14 Tagen, Busse bis CHF 20 000. `hinweis_heute` gesetzt.
- Landquart: Seite Steuern (CHF 120 pro Hund, höchstens CHF 600 pro Haushalt, Befreiungen, Gesuch bis 31. März), Online-Schalter Hundekontrolle, Mitteilung des Gemeindepolizeiamts vom 11. Juli 2025 (Art. 50 Polizeigesetz, Robidog, Beutel), Seite Mastrilser Rheinauen (Bitte um Leine, als Bitte wiedergegeben).
- Weggelassen: Arth «Hinweise-Hundehalter.pdf» und Robidog-Pläne (nicht abrufbar). Landquart: Polizeigesetz, Steuergesetz, Friedhofordnung im Wortlaut (nicht abrufbar), daher keine Angabe zu Leinenpflicht, Verboten, Bussen und Meldefrist. Davos: Beträge der Ordnungsbussen, Verwaltungs- und Umschreibegebühr (stehen im Gebührentarif, nicht gelesen). Einsiedeln: Leinenregeln der Broschüre sind kantonales Recht und stehen auf der Kantonsseite.
- `add_repo` und `register_repo_root` standen nicht zur Verfügung, das Repository lag mit Push-Zugriff im Arbeitsordner. Die Zusatznachricht mit der Nummer fehlte, laut Protokoll ist dies Glied 7.
- Nicht gelungen: nichts.

## 2026-11-18, Parallel-Lauf `gr` (Staffel A), eingesammelt von Glied 7

- Neu: Kanton Graubünden (`data/kantone/gr.json`) und Stadt Chur (`data/gemeinden/gr/chur.json`), sechs Quellen in `data/quellen/gr.json`. Alle Quellen in diesem Lauf abgerufen.
- Graubünden hat kein Hundegesetz. Belegt sind: keine allgemeine Pflicht zu Haftpflicht, Kurs oder Leine und keine Rasseliste im Veterinärgesetz (Art. 64 bis 66, 76a, 77), Registrierung durch die Gemeinden, wildernde Hunde (Jagdverordnung Art. 32), Meldepflicht für Vorfälle (Seite Hundewesen). `wald` ohne Saison: Jagdgesetz, Jagdverordnung und Veterinärgesetz nennen keine Leinenpflicht im Wald.
- Unsicherheit: Vom Veterinärgesetz war nur die Fassung «Stand 1. Januar 2016» abrufbar (gr.lexwork.naz.ch). gr-lex.gr.ch liess sich im Lauf nicht abrufen. Ob es eine neuere Fassung gibt, ist nicht geprüft. Der Stand steht im Langnamen der Quelle.
- Weggelassen: Rasseliste und Bewilligungspflicht von der Seite Hundewesen, weil sie nur Glarus betreffen. Kantonale Hundesteuer: Das Gesetz über die Gemeinde- und Kirchensteuern wurde in diesem Lauf nicht abgerufen, die Karte stützt sich nur auf das Veterinärgesetz und das Beispiel Chur. Wildruhezonen des Kantons: keine amtliche Quelle zu Hunden abgerufen.
- Chur: fünf Karten (Hundetaxe CHF 155, Leine, Kein Zutritt, Anmeldung, Bussen) aus der Seite Hundewesen der Stadtpolizei und dem Merkblatt «Wichtige Regeln für Hundehalter» (ohne Datum). Die Seite nennt kein Jahr zur Taxe von CHF 155. Weggelassen: Wortlaut des Polizeigesetzes der Stadt (RB 411), nicht gefunden. Das Merkblatt nennt Art. 23 Abs. 4 und Art. 30 «PG», ohne die Abkürzung zu erklären, deshalb steht der Gesetzesname nicht auf der Seite.
- Nicht gelungen: nichts.

## 2026-11-17, Nachtkette, Glied 6 (Sonderlauf Themenseiten)

- Sonderlauf: nur der Umbau, kein neuer Kanton, keine Gemeinde. Nachgeprüft: nichts. Eingesammelt: beim Start nichts, vor dem Push der Parallel-Lauf `ai` (eigener Eintrag unten).
- Neu: sechs Themenseiten, erzeugt aus den Kantonsdateien, ohne neue Angaben: `/thema/leinenpflicht-wald/`, `/thema/haftpflicht/`, `/thema/hundekurs/`, `/thema/rassen/`, `/thema/hundesteuer/`, `/thema/anmeldung/`. Jede hat Titel «… alle Kantone im Vergleich», einen Absatz, der zählt, eine Tabelle mit Link zu jedem Kanton und je Kanton die Karte mit Quellen. Sitemap: 32 Seiten.
- Startseite: Die Spaltenköpfe der Vergleichstabelle führen auf die Themenseiten, darunter stehen sechs Tafeln. Jede Kantonsseite hat am Schluss den Abschnitt «Ein Thema, alle Kantone». Bestehende Adressen und das Aussehen der übrigen Teile sind unverändert.
- Abweichung von der Vorgabe: Hundesteuer und Anmeldung zählen keine «Pflicht» nach `ton`. Die Karten Hundesteuer haben überall `note`, die Karten Anmeldung teils `must`, teils `note`, obwohl die Anmeldung überall Pflicht ist. Eine Zahl daraus wäre falsch. Dort steht ein neutraler Satz.
- Leinenpflicht im Wald zählt `wald.saison` (7 von 10, überall 1. April bis 31. Juli). Für die übrigen heisst es «keine feste Leinenzeit erfasst», nicht «keine Leinenpflicht».
- `build.py`: prüft neu, dass jeder Kanton genau die sechs Karten in der festen Reihenfolge hat (deutsche, französische oder italienische Titel), weil die Themenseiten über die Position zugreifen. `assets/site.css`: drei Zeilen (Worttrennung der Hauptüberschrift auf Themenseiten, Links im Kartentitel und Tabellenkopf). `tests/seiten.js`: jede Themenseite muss jeden erfassten Kanton mit Quelle aufführen.
- Als Bild angesehen: `/thema/haftpflicht/` (390 px), `/thema/leinenpflicht-wald/` (1280 px). Die Überschrift «Haftpflichtversicherung» lief bei 390 px zuerst über, behoben mit Worttrennung.
- Handbuch nachgeführt: Aufbau, erzeugte Ordner, Datenfelder (`karten`, `ton`), Abschnitt Themenseiten.
- Dem Auftrag fehlte die Zusatznachricht mit der Nummer. Laut Protokoll ist dies Glied 6. `add_repo` und `register_repo_root` standen nicht zur Verfügung, das Repository lag mit Push-Zugriff im Arbeitsordner.
- Fehler dieses Laufs, behoben: Beim Push kam ein Konflikt in `CHANGELOG.md` (ein zweiter Lauf hatte die Gemeinde Schwyz veröffentlicht). Der erste Push um 00:00 Uhr enthielt deshalb für wenige Minuten Konfliktzeichen in `CHANGELOG.md`. Die Seiten selbst waren neu erzeugt und getestet und nicht betroffen. Der Folge-Commit hat das Protokoll bereinigt.
- Nicht gelungen: nichts.

## 2026-11-17, Parallel-Lauf `ai` (Staffel E), eingesammelt von Glied 6

**Neu:** Kanton Appenzell Innerrhoden (`data/kantone/ai.json`), 6 Quellen in `data/quellen/ai.json`. Alle Quellen am 17. November 2026 abgerufen.

- Hundegesetz (GS 560.100, Stand 1. Januar 2011): Haftpflicht ohne Mindestsumme (Art. 17), Leinenzwang und Betretungsverbot (Art. 6), Kot (Art. 7), Massnahmen und Zuzug (Art. 10), Meldepflicht (Art. 12).
- Verordnung zum Hundegesetz (GS 560.110, Stand 1. Januar 2025): Hundesteuer kantonal einheitlich CHF 80, Hofhund CHF 50, weiterer Hund im Haushalt CHF 160, Zuchten und Tierheime CHF 600 (Art. 1), Befreiungen (Art. 3), Meldungen an den Bezirk (Art. 6, 8a).
- Verordnung zum Alpgesetz (GS 916.510, Stand 1. Dezember 2014), Art. 5: Leine während der Alpzeit, ausgenommen Hunde der Bewirtschafter.
- Verordnung zum Jagdgesetz (GS 922.010, Stand 1. Januar 2025), Art. 41: wildernde Hunde. Keine Leinenpflicht im Wald.
- Verordnung über die Ordnungsbussen (GS 311.010, Stand 1. August 2023), Anhang 1 Ziff. 6: CHF 50 für Leinenzwang oder Betretungsverbot, CHF 100 für nicht beseitigten Kot.
- Seite «Hundehalterausbildung» des Kantons: keine Kurspflicht seit 1. Januar 2017, Anordnung im Einzelfall.

**Entscheide:**

- `wald.saison` ist `false`: Die drei gelesenen Erlasse nennen keine Leinenzeit im Wald. Der Text nennt genau diese Erlasse und die Leinenpflicht während der Alpzeit.
- Kurs: Die Seite des Kantons nennt das Veterinäramt als anordnende Stelle, das Hundegesetz (Art. 10) den Bezirk. Beides steht mit Quelle im Text.
- Art. 12 HuG («bei der nächsten Hundelösung melden») ist nicht als Frist übernommen, die Verordnung von 2025 regelt die Meldung ohne diesen Zusatz.

**Weggelassen:**

- Die Seite «Leinenpflicht in beiden Appenzell» des Veterinäramts (ar.ch) war zweimal nicht abrufbar (client_error). Nichts daraus verwendet.
- Jagdgesetz (GS 922.000) und Vorschriften zu Wildruhe- und Naturschutzgebieten: Text nicht abrufbar (ai.clex.ch liefert WebFetch nur eine leere Hülle, auf lexfind.ch nicht gefunden). Keine Angabe daraus.
- Daten der Alpzeit und genaue Liste der Alpen: Die Alpverordnung nennt keine Daten. Der Geltungsbereich (Art. 1) ist nur als «Alpen, für die das Alpgesetz gilt» wiedergegeben.
- Polizeimeldung «Alpstein: polizeiliche Kontrollen» (ai.ch) erwähnt eine Leinenpflicht im Alpstein ohne Rechtsgrundlage und Datum. Nicht verwendet.

**Nicht gelungen:** Bezirk Appenzell (BFS 3101) als Gemeinde, siehe Backlog.

## 2026-11-17, Nachtkette, zweite Auslösung als Glied 5

- Dieser Lauf wurde ohne Nummer ausgelöst und zählte sich nach dem Protokoll als Glied 5. Während er den Kanton Schwyz erfasste, veröffentlichte ein anderer Lauf als Glied 5 denselben Kanton mit dem Bezirk Küssnacht. Es liefen also wieder zwei Auslösungen nebeneinander. Die eigene Kantonsdatei wurde verworfen, die Datei auf `main` blieb unverändert. Damit keine zweite Kette entsteht, löst dieser Lauf kein weiteres Glied aus.
- Nachgeprüft: nichts. Eingesammelt: nichts. Die Aufträge der fünf Staffeln von 23:55 Uhr blieben unberührt.
- Neu: Gemeinde Schwyz (`/sz/schwyz/`), 12 Gemeinden. Quelle, am 17. November 2026 abgerufen: Dienstleistung Hundekontrolle der Gemeinde (ohne Datum). Belegt sind Steuer (CHF 100, weiterer Hund CHF 200, Nutzhund CHF 40, Rechnung im Januar), Anmeldung zuerst bei der Gemeinde (Bereich Finanzen) und Meldung von Änderungen innert zehn Tagen. Orte mit Leinenpflicht oder Verbot nennt die Gemeinde nicht.
- Nach der Reihenfolge wäre der Sonderlauf Themenseiten dran gewesen. Die Recherche zur Gemeinde war beim Wechsel schon abgeschlossen, deshalb wurde nur diese eine Datei veröffentlicht. Der Sonderlauf bleibt Sache der Kette.
- Aus der eigenen Recherche zum Kanton als Lücken ins Backlog: Veterinärgesetz und Veterinärverordnung (AMICUS, Massnahmen im Einzelfall), Jagd- und Wildschutzgesetz (Fassung mit unklarem Stand «1.2.2027», nicht verwendet), Hundewiese Küssnacht.
- `add_repo` und `register_repo_root` standen nicht zur Verfügung. Das Repository lag mit Push-Zugriff im Arbeitsordner.

- Nicht gelungen: nichts.

## 2026-11-17, Nachtkette, Glied 5

- Nachgeprüft: nichts. Keine Datei ist älter als 60 Tage. Eingesammelt: nichts. Graubünden ist an die Hauptsitzung vergeben und wurde übersprungen.
- Neu: Kanton Schwyz (`/sz/`) und Bezirk Küssnacht (`/sz/kuessnacht/`), 10 von 26 Kantonen, 11 Gemeinden. Meilenstein: 10 Kantone erfasst, der nächste Lauf ist der Sonderlauf Themenseiten.
- Quellen, alle am 17. November 2026 abgerufen: Hundegesetz (SRSZ 546.100, Stand 1. Februar 2024), Bericht des Regierungsrats zur Teilrevision (RRB 485/2026 vom 23. Juni 2026), Medienmitteilung vom 25. August 2026, Antwort des Regierungsrats zur Leinenpflicht (RRB 38/2024). Küssnacht: Broschüre des Einwohneramts, Ausgabe April 2019.
- Das Abrufwerkzeug lieferte Zusammenfassungen mit kurzen Zitaten, nicht den vollen Wortlaut.
- Teilrevision: Das Hundegesetz war am 16. September 2026 im Kantonsrat. Ergebnis und Inkrafttreten waren amtlich nicht auffindbar. Erfasst ist das Gesetz in der Fassung der Gesetzessammlung. Die Karten Kurs und Rassen nennen die Revision als geplant.
- Wald: Das Gesetz kennt keine Leinenzeit im Wald, dafür ganzjährig Leine in öffentlichen Anlagen, auf öffentlichen Wegen und im Strassenverkehr.
- Weggelassen: Meldepflicht bei der Gemeinde (kommt laut Bericht erst mit der Revision), Bussenbeträge (das Gesetz nennt keine).
- Bezirk Küssnacht statt Freienbach: Das Merkblatt von Freienbach ist ein PDF ohne lesbaren Text. Küssnacht hat vier belegte lokale Angaben (Steuer, Leine im Areal Luterbach und auf der Finnenbahn, Gratis-Säcklein, Einwohneramt), alle mit Stand April 2019. Die aktuellen Seiten des Bezirks lassen den Abruf nicht zu.
- Zurückgestellt: Freienbach (Merkblatt nicht lesbar).
- Nicht gelungen: nichts.
- Backlog: Einsiedeln, Schwyz und Arth eingetragen, zwei neue Lücken.

## 2026-11-17, Nachtkette, Glied 4

- Dem Auftrag fehlte die Zusatznachricht mit der Nummer. Laut Protokoll sind die Glieder 1 bis 3 gelaufen, ein Glied 4 wurde ausgelöst, hat aber nichts geliefert (Nutzungsgrenze um 23:02 Uhr). Dieser Lauf zählt als Glied 4.
- Nachgeprüft: nichts. Keine Datei ist älter als 60 Tage. Eingesammelt: nichts, unter `data/protokoll/` lag nur `auftraege.md`. Graubünden ist dort an die Hauptsitzung vergeben und blieb unberührt.
- Neu: Kanton Solothurn (`/so/`) und Stadt Olten (`/so/olten/`), 9 von 26 Kantonen, 10 Gemeinden. Quellen, alle am 17. November 2026 abgerufen: Hundegesetz (BGS 614.71, Stand 1. Januar 2026), Hundeverordnung (BGS 614.72, Stand 1. Juni 2026, über LexFind), Seiten «Leinenpflicht», «Bewilligungspflichtige Hunde» und «Mein Hund und ich» des Amts für Landwirtschaft (ohne Datum). Olten: Dienstleistung Hundesteuer, Übersicht AMICUS (beide ohne Datum), Reglement über die gemeindepolizeilichen Aufgaben vom 29. September 2016.
- Das Abrufwerkzeug lieferte Zusammenfassungen mit kurzen Zitaten, nicht den vollen Wortlaut. Das Hundegesetz wurde zweimal gelesen (bgs.so.ch und LexFind), die Angaben stimmen überein.
- Leine im Wald: Die Verordnung sagt «im Wald», die Seite «Mein Hund und ich» des Amts «Wald und Waldränder». Erfasst ist der Rechtstext, die Seite nennt den Hinweis des Amts.
- Weggelassen: Betrag der Gebühr für die Haltebewilligung (das Merkblatt wurde nicht gelesen), Bussenbeträge (weder Gesetz noch Verordnung nennen welche), Meldefrist (das Gesetz nennt keine).
- Stadt Olten: drei lokale Angaben belegt (Steuer CHF 130 plus CHF 35 Kanton, Leine im Siedlungsgebiet, Anmeldung bei der Einwohnerkontrolle). Ein Stadtratsbeschluss von 2007 nennt noch CHF 90, erfasst ist der Betrag der aktuellen Seite. Hundeverbote nennt das Reglement nicht.
- `add_repo` und `register_repo_root` standen nicht zur Verfügung. Das Repository lag mit Push-Zugriff im Arbeitsordner.
- Nicht gelungen: nichts.
- Backlog: Solothurn, Grenchen, Zuchwil und Biberist eingetragen, zwei neue Lücken.

## 2026-11-17, Nachtkette, zweite Auslösung als Glied 3

- Dieser Lauf wurde mit der Zusatznachricht «Glied 3» ausgelöst, kurz nachdem ein Lauf ohne Nummer als Glied 3 den Kanton Thurgau veröffentlicht und Glied 4 ausgelöst hatte. Es laufen damit zwei Auslösungen nebeneinander. Damit keine zweite Kette entsteht, löst dieser Lauf kein weiteres Glied aus.
- Nachgeprüft: nichts. Eingesammelt: nichts, kein Parallel-Lauf hat bisher geliefert.
- Alle offenen Kantone sind an Parallel-Läufe vergeben, also Gemeinden. Um dem schon ausgelösten Glied 4 nicht in die Quere zu kommen, nahm der Lauf die Thurgauer Gemeinden statt der obersten Einträge (Basel-Landschaft).
- Neu: Stadt Arbon (`/tg/arbon/`) und Stadt Kreuzlingen (`/tg/kreuzlingen/`), 9 Gemeinden. Quellen, am 17. November 2026 abgerufen: Arbon Dienstleistung Hundewesen und Informationsbroschüre (beide ohne Datum), Kreuzlingen Broschüre (Stand Juni 2025) und Seite «Informationen zur Hundehaltung».
- Kreuzlingen ist knapp: belegt sind Steuer, Anmeldestelle und Gratis-Kotsäcke. Orte mit Leinenpflicht oder Verbot nennen die Quellen nicht.
- Meldefrist: Die Quellen der Städte widersprechen sich (Kreuzlingen 10 und 30 Tage, Arbon 10 und 14 Tage). Die Seiten nennen beide Angaben und raten zu 10 Tagen.
- Zurückgestellt: Amriswil (nur eine Angabe belegt), Weinfelden (Website nicht abrufbar), Romanshorn (Merkblatt ohne Datum und teils veraltet, aktuelle Seiten nicht abrufbar).
- Nicht gelungen: nichts.

## 2026-11-17, Nachtkette, Glied 3

- Nachgeprüft: nichts. Keine Datei ist älter als 60 Tage.
- Eingesammelt: nichts. Unter `data/protokoll/` lag nur `auftraege.md`, alle Aufträge sind jünger als drei Stunden.
- Neu: Kanton Thurgau (`/tg/`) und Stadt Frauenfeld (`/tg/frauenfeld/`), 8 von 26 Kantonen erfasst. Quellen, alle am 17. November 2026 abgerufen: Hundegesetz (RB 641.2, Stand 1. Mai 2025), Hundeverordnung (RB 641.21, Stand 1. Mai 2025), Merkblatt des Veterinäramts für bewilligungspflichtige Hunderassen (ohne Datum). Frauenfeld: Informationen für Hundehaltende der Einwohnerdienste (Stand 2026), Merkblatt Leinenpflicht vom 15. März 2024.
- Die Gesetzestexte wurden über LexFind gelesen. Das Rechtsbuch des Kantons (rechtsbuch.tg.ch) lieferte nur die Verordnung in der Fassung von 2008, die geltende Adresse des Gesetzes war nicht abrufbar. Das Abrufwerkzeug lieferte Zusammenfassungen mit kurzen Zitaten, nicht den vollen Wortlaut. Die Ordnungsbussen stimmen in zwei Fassungen der Verordnung (2023 und 2025) überein.
- Hundesteuer: Das Gesetz in der Fassung von 2024 nannte einen Zuschlag der Gemeinde von höchstens 25 Prozent, die geltende Fassung nennt 50 Prozent. Erfasst ist die geltende Fassung. Dazu passen die Beträge von Frauenfeld (CHF 120 und CHF 195) und eine Mitteilung der Gemeinde Aadorf vom 9. Mai 2025.
- Weggelassen: Meldefrist bei der Gemeinde auf der Kantonsseite (das Gesetz verweist seit 2025 auf das Bundesrecht und nennt keine Frist), die Übergangsregel beim Kurs für Hunde unter 15 kg (nur in einem Merkblatt des Verbands Thurgauer Gemeinden gefunden, keine Quelle des Kantons), Pauschalsteuer für Zuchten.
- Stadt Frauenfeld: drei lokale Angaben belegt (Steuer, ganzjährige Leinenpflicht in namentlich genannten Wäldern und Schutzgebieten, Anmeldung). Hundeverbote und Bussen der Stadt nennen die Quellen nicht.
- Dem Auftrag fehlte die Zusatznachricht mit der Nummer. Laut Protokoll sind Glied 1 und 2 schon gelaufen, dieser Lauf zählt als Glied 3.
- `add_repo` und `register_repo_root` standen dem Lauf nicht zur Verfügung. Das Repository lag schon mit Push-Zugriff im Arbeitsordner.
- Nicht gelungen: nichts.
- Backlog: Kreuzlingen, Arbon, Amriswil, Weinfelden und Romanshorn eingetragen, zwei neue Lücken.

## 2026-11-17, Nachtkette, Glied 2

- Nachgeprüft: nichts. Keine Datei ist älter als 60 Tage.
- Neu: Kanton Basel-Landschaft (`/bl/`) und Allschwil (`/bl/allschwil/`), 7 von 26 Kantonen erfasst. Quellen, alle am 17. November 2026 abgerufen: Hundegesetz (SGS 342, Stand 1. Januar 2008), Verordnung über das Halten potenziell gefährlicher Hunde (SGS 342.12, Stand 1. Februar 2013), Wildtier- und Jagdgesetz (SGS 520, Stand 1. Januar 2022), Wildtier- und Jagdverordnung (SGS 520.11, Stand 1. November 2026), Medienmitteilung des Kantons zur Leinenpflicht 2025. Allschwil: Seite der Einwohnerdienste, Gebührenordnung Hundegebühren (Stand 1. Januar 2024), Polizeireglement (Teilrevision 2024) und Verordnung dazu.
- Die Gesetzestexte wurden über LexFind gelesen, weil der Lauf die Gesetzessammlung des Kantons (bl.clex.ch) nicht direkt fand. Das Abrufwerkzeug lieferte Zusammenfassungen mit kurzen Zitaten, nicht den vollen Wortlaut. Haftpflicht, Kurspflicht, Meldefrist und Rasseliste wurden gezielt je Paragraph abgefragt.
- Nicht abrufbar (zwei Versuche): die Seite «Hunde» des Veterinärdienstes und die Seite «Leinenpflicht» des Amts für Wald auf baselland.ch. Deshalb weggelassen: AMICUS auf der Kantonsseite, eine Erklärung von «Waldesnähe» in Metern, Bussenbeträge des Kantons. Das Gesetz nennt keine Meterzahl.
- Kurs: Die Kurspflicht steht im Hundegesetz nur als Voraussetzung der Bewilligung für potenziell gefährliche Hunde. Die Seite sagt deshalb «keine Pflicht» für alle anderen Hunde.
- Allschwil: Das Hundereglement von 1996 steht noch auf der Website der Gemeinde, ist aber durch das Polizeireglement von 2017 ersetzt (§ 51). Erfasst ist das Polizeireglement. Es ist strenger als der Kanton: Leine im Wald das ganze Jahr, ausser auf den Freilaufwegen ausserhalb der Zeit vom 1. April bis 31. Juli. Der Plan der Freilaufwege war nicht lesbar, die Wege sind nicht namentlich aufgeführt.
- Dem Auftrag fehlte die Zusatznachricht mit der Nummer. Weil Glied 1 laut Protokoll und Commit `d8d8300` schon gelaufen ist und dieser Lauf zwei Minuten danach ausgelöst wurde, zählt er als Glied 2.
- `add_repo` und `register_repo_root` standen dem Lauf nicht zur Verfügung. Das Repository lag schon mit Push-Zugriff im Arbeitsordner.
- Nicht gelungen: nichts.
- Backlog: Reinach, Muttenz, Pratteln, Binningen und Liestal eingetragen, zwei neue Lücken.

## 2026-11-17, Nachtkette, Glied 1

- Nachgeprüft: nichts. Keine Datei ist älter als 60 Tage.
- Neu: Kanton Basel-Stadt (`/bs/`) und Stadt Basel (`/bs/basel/`), 6 von 26 Kantonen erfasst. Quellen, alle am 17. November 2026 abgerufen: Veterinäramt (Hundehaltende, Hund anmelden, Hundekurse, bewilligungspflichtige Rassen, Merkblatt Hundesteuer 2026/27, Liste der Hundeverbots- und Leinenpflichtzonen), Hundegesetz und Hundeverordnung (Stand 1. April 2025), Wildtier- und Jagdgesetz (Stand 1. April 2024).
- Wald: Leinenpflicht vom 1. April bis 31. Juli nach § 8 WJG «im Wald, am Waldrand und angrenzender Wiese». Das Veterinäramt nennt Ausnahmen an der Wiese (rechte Wieseseite, Vorländer, Dammwege). Weggelassen, weil der Beschluss dazu nicht gelesen wurde. Die Seite ist damit eher zu streng als zu locker.
- Die Gesetzestexte hat das Abrufwerkzeug nur zusammengefasst und mit kurzen Zitaten geliefert, nicht im vollen Wortlaut. Beträge, Fristen und Listen wurden gezielt je Paragraph abgefragt und mit den Seiten des Veterinäramts verglichen. Kein Widerspruch gefunden.
- Weggelassen: verbotene Rassen (das Gesetz erlaubt Verbote, eine Liste war nicht auffindbar), Kosten der Haltebewilligung, Folgen eines versäumten Basiskurses.
- Stadt Basel: Der Kanton besorgt die Aufgaben der Stadt. Lokale Angaben sind der Steuerbetrag der Stadt und die namentlich aufgeführten Anlagen mit Hundeverbot und Leinenpflicht. Die Liste des Kantons trägt kein Datum.
- Hinweis: Im Kanton läuft eine Revision des Hundegesetzes (Entwurf in Vernehmlassung gefunden). Erfasst ist das geltende Recht.
- `add_repo` und `register_repo_root` standen dem Lauf nicht zur Verfügung. Das Repository lag schon mit Push-Zugriff im Arbeitsordner.
- Nicht gelungen: nichts.
- Backlog: Riehen und Bettingen eingetragen, vier neue Lücken zu Basel-Stadt.

## 2026-11-17, Sitzung mit Joss

- Neu: Kontaktadresse kontakt@gassi-kompass.ch (Postfach bei Infomaniak, DNS-Einträge für Mail geprüft). Sie steht im Fuss jeder Seite und auf «Über diese Seite».
- Entscheid von Joss: Der Lauf arbeitet täglich, bis alle 26 Kantone erfasst sind, danach mittwochs und samstags.
- Stichprobe Kanton Aargau: Hundetaxe, Anmeldefrist und Leinenpflicht im Wald mit den Seiten des Kantons verglichen, alles stimmt.
- Geändert, Kanton St. Gallen, Vergleichstabelle «Leine im Wald»: alt «keine Saisonregel, Leine ohne wirksame Kontrolle», neu «keine feste Leinenzeit im Hunde- und Jagdgesetz, Leine ohne wirksame Kontrolle». Grund: Die Verordnung über die Jagdvorschriften (sGS 853.111) war nicht lesbar und ist noch nicht geprüft.

## 2026-11-17, zweiter Lauf (von Hand ausgelöst)

- Nachgeprüft: nichts. Keine Datei ist älter als 60 Tage.
- Neu: Kanton St. Gallen (`/sg/`) und Stadt St. Gallen (`/sg/st-gallen/`), 5 von 26 Kantonen erfasst. Quellen, alle am 17. November 2026 abgerufen: Amt für Verbraucherschutz und Veterinärwesen, Hundegesetz von 2019, Jagdgesetz, Jagdverordnung, Seite der Stadtpolizei St. Gallen.
- Wald: Im Hundegesetz, im Jagdgesetz und in der Jagdverordnung steht keine Leinenpflicht zu festen Daten. Die Seite sagt genau das und nicht mehr. Nicht geprüft: Jagdvorschriften des Departements, Schutzverordnungen einzelner Gebiete.
- LexFind lieferte unter der Adresse des Hundegesetzes die Fassung von 1985 (aufgehoben). Verwendet wurde der Text von `sg.lexwork.naz.ch` mit Stand 1. Januar 2020, auf den auch der Kanton verweist.
- Weggelassen: Frist für die Anmeldung bei der Gemeinde (steht weder im Hundegesetz noch auf den Seiten von Kanton und Stadt).
- Nicht gelungen: nichts.
- Nicht angegangen: Lücke aus Abschnitt 4, um Abrufe zu sparen.
- Backlog: vier St. Galler Gemeinden eingetragen, eine neue Lücke zur Stadt St. Gallen.

## 2026-11-17, automatischer Lauf

- Nachgeprüft: nichts. Keine Datei ist älter als 60 Tage.
- Neu: Kanton Aargau (`/ag/`), 4 von 26 Kantonen erfasst. Quellen, alle am 17. November 2026 abgerufen: Veterinärdienst (Hunde, Listenhunde), Abteilung Wald (Leinenpflicht), Hundegesetz, Jagdverordnung § 21, Ordnungsbussenverordnung.
- Die Gesetzestexte wurden über LexFind und über PDF-Fassungen der Aargauer Gesetzessammlung gelesen. Die Adressen `gesetzessammlungen.ag.ch/data/...` konnte der Lauf nicht abrufen. Hundegesetz: gelesen wurde der Wortlaut von 2012. Laut LexFind gilt die Fassung vom 1. Juli 2024, geändert wurde nur § 7 Abs. 3 (auf der Seite nicht verwendet).
- Weggelassen, weil nur in den Fassungen 2014 und 2016 der Hundeverordnung gelesen: Deckungssumme der Haftpflicht für Listenhunde, Fristen für Kurs und Prüfung, halbe Taxe, Maulkorb für bissige Hunde. Die Rasseliste stammt von der Seite des Veterinärdienstes, nicht aus der Verordnung.
- Widerspruch zwischen Quellen: Hundeverordnung Stand 2014 nennt CHF 115 Hundetaxe, Stand 2016 und die heutige Seite des Veterinärdienstes CHF 120. Übernommen: CHF 120. Die Seite der Abteilung Wald nennt im Text den 31. Juli, in der Seitenbeschreibung den 30. Juli. Übernommen: 31. Juli, wie in § 21 der Jagdverordnung.
- Ordnungsbusse Hundekot CHF 100: Quelle mit Stand 1. Juli 2021, auf der Seite mit Stand genannt.
- Nicht gelungen: Stadt Aarau. Nur zwei lokale Angaben belegt, die geltende Polizeiverordnung war nicht lesbar (zwei Versuche). Keine Seite angelegt, im Backlog zurückgestellt.
- Nicht angegangen: Lücke aus Abschnitt 4, um Abrufe zu sparen.
- Backlog: vier weitere Aargauer Gemeinden eingetragen, zwei neue Lücken zum Kanton Aargau.

## 2026-11-17

- Umbau vom Piloten mit einer Seite auf eigene Seiten pro Kanton und Gemeinde: 8 Seiten.
- Daten nach `data/` ausgelagert, Generator `build.py` mit Datenprüfung, Browser-Test `tests/seiten.js`.
- Schriften lokal eingebunden. Die Seite ruft keine fremden Server mehr ab.
- Neu: Seite «Über diese Seite», 404-Seite, Sitemap mit allen Seiten, Ortsfilter auf der Startseite.
- Arbeitshandbuch `CLAUDE.md` und Ausbauliste `BACKLOG.md` angelegt.
- «Enforce HTTPS» eingeschaltet. Die Seite läuft nur noch über https.
- Google Search Console: Property `https://gassi-kompass.ch/` über die Datei `google49e2be530ce3822a.html` bestätigt, Sitemap eingereicht, 8 Seiten erkannt.
- `build.py --check` meldet neu einen Fehler, wenn `CNAME`, `.nojekyll` oder die Bestätigungsdatei fehlen.
- Automatischer Lauf eingerichtet: mittwochs und samstags um 04:23 Uhr.
- Neue Strategie im Auftrag von Joss: alle 26 Kantone in ihren Amtssprachen, Themenseiten, danach Gemeinden. Reihenfolge in `BACKLOG.md`, Vorgaben in `CLAUDE.md`.
- `tests/seiten.js` bricht neu ab, wenn eine veröffentlichte Adresse verschwindet.
- Neu: Ortssuche für die ganze Schweiz (2137 Gemeinden, 5677 Orte mit Postleitzahl, Quelle swisstopo). Sie führt auf die Gemeinde, sonst auf den Kanton, sonst auf die Regeln des Bundes.
- Neu: Seite `/schweiz/` mit den Regeln des Bundes (Quellen: BLV und ch.ch, abgerufen am 17. November 2026).
- Neu: Übersicht aller 26 Kantone mit Stand «erfasst» oder «folgt».
- Der Browser-Test prüft jede Seite neu in zwei Breiten und dazu die Ortssuche.
- Nicht gelungen: nichts.

## 2026-11-16

- Pilot: Regeln der Kantone Zürich, Luzern und Bern sowie der Städte Zürich, Luzern und Bern aus amtlichen Quellen zusammengetragen und geprüft.
- Offen geblieben: Betrag der Hundeabgabe in Zürich und Bern, Namen der Zürcher Freilaufzonen. Siehe `BACKLOG.md`.
