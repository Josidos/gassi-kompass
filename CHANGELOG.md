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
- Wöchentlicher automatischer Lauf eingerichtet: mittwochs um 04:23 Uhr.
- Nicht gelungen: nichts.

## 2026-11-16

- Pilot: Regeln der Kantone Zürich, Luzern und Bern sowie der Städte Zürich, Luzern und Bern aus amtlichen Quellen zusammengetragen und geprüft.
- Offen geblieben: Betrag der Hundeabgabe in Zürich und Bern, Namen der Zürcher Freilaufzonen. Siehe `BACKLOG.md`.
