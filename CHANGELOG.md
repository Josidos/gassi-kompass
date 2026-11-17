# Protokoll

Neuster Eintrag zuoberst. Pro Lauf: nachgeprüft, geändert, neu, nicht gelungen.

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
