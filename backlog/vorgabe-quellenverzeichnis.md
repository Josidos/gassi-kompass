# Vorgabe für den Sonderlauf «Quellenverzeichnis»

Wunsch von Joss vom 28.11.2026 (03:22 und 04:08 Uhr): eine Seite mit allen Quellen der Website, in der man filtern, sortieren und suchen kann.

Es gelten «Umbauten am Generator» in `CLAUDE.md`, `handbuch/generator.md` (vorher «Darstellung» und «Telefon und Berührung» lesen) und `DESIGN.md`. Keine fremden Skripte. Im Zweifel die schlichtere Lösung.

1. **Seite.** `/quellen/`, `/fr-ch/quellen/`, `/it-ch/quellen/`, in der Sitemap und im Fuss jeder Seite verlinkt. Sie führt jede Quelle, die eine Seite dieser Sprache zitiert: Kurzname, Langname als Link zur amtlichen Adresse, Geltungsbereich (Bund, Kanton, Gemeinde) und «zitiert auf» mit Links zu den Seiten. Alles entsteht aus `data/quellen.json`, `data/quellen/*.json` und den Datendateien, nichts von Hand.
2. **Geltungsbereich** aus dem Schlüssel der Quelle (`ch_`, Kürzel des Kantons) und aus den Dateien, die sie zitieren: Zitiert sie nur die Datei einer Gemeinde, gehört sie zu dieser Gemeinde. Eine «Art» der Quelle (Erlass, Merkblatt, Seite eines Amts) nennt die Seite nicht: Die Daten haben dafür kein Feld, und geraten wird nicht.
3. **Abgeglichen am.** Je Quelle das jüngste `geprueft` der Dateien, die sie zitieren, als «zuletzt abgeglichen am». Mehr behauptet die Seite nicht.
4. **Filtern, Sortieren, Suchen** im Browser: ein Suchfeld (durchsucht Kurzname, Langname, Kanton und Gemeinde, Akzente und Gross- und Kleinschreibung zählen nicht), die Wahl des Geltungsbereichs (Bund und die Kantone als Kennungs-Quadrate) und die Sortierung nach Kanton (Standard) oder nach Name. Eine Statuszeile sagt, wie viele Quellen gerade sichtbar sind (`aria-live`). Ohne Skript steht die ganze Liste da, nach Kanton geordnet mit Zwischenüberschriften.
5. **Darstellung.** Linienliste oder Tabelle mit den Mitteln aus `DESIGN.md`, auf dem Telefon ein Block je Quelle (`table.stack`). Mit Finger als Zeiger sind Links und Quadrate mindestens 44px hoch. Hover-Regeln in `@media (hover:hover) and (pointer:fine)`.
6. **Texte** in `TEXTE` für `de`, `fr`, `it`. Der Titel der Seite nennt, wonach gesucht wird: amtliche Quellen zu Hunderegeln in der Schweiz, Hundegesetze der Kantone. Kein Satz spricht über den Stand des Projekts.
7. **Suche über die ganze Website.** Gibt es sie schon (`assets/suche-<sprache>.json`), nimmt sie `/quellen/` als eine Seite auf, nicht jede Quelle einzeln.
8. **Tests.** `tests/seiten.js`: Die Seite gibt es in drei Sprachen. Sie führt genau die Quellen, die Seiten dieser Sprache zitieren. Jeder Link unter «zitiert auf» führt auf eine Seite, die es gibt. Die Wahl «ZH» zeigt nur Quellen des Kantons Zürich und seiner Gemeinden. Die Suche nach «Hundegesetz» findet mindestens eine Quelle. Die Seite ruft nichts Fremdes ab. `tests/tippflaechen.js` prüft `/quellen/` mit.
9. **Ansehen**, 390 und 1280 Pixel, in drei Sprachen.
10. **Handbuch.** `handbuch/generator.md` (neuer Abschnitt), `DESIGN.md`, wenn ein Baustein dazukommt. In `BACKLOG.md`, Abschnitt 5, diesen Punkt abhaken. Diese Datei danach löschen.
