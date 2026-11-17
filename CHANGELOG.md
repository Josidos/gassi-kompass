# Protokoll

Neuster Eintrag zuoberst. Pro Lauf: nachgeprüft, geändert, neu, nicht gelungen.

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
