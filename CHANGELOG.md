# Protokoll

Neuster Eintrag zuoberst. Pro Lauf: nachgeprüft, geändert, neu, nicht gelungen.

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
