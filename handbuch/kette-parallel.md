# Handbuch: Kette und Parallel-Läufe

Teil des Arbeitshandbuchs `CLAUDE.md` und genauso verbindlich. Lies diese Datei, wenn du als Glied einer Kette oder als Parallel-Lauf ausgelöst wurdest, wenn in `BACKLOG.md` unter «Kette» etwas anderes steht als «keine Kette», oder wenn unter `data/protokoll/` etwas einzusammeln ist. Nennt ein Verweis einen Abschnitt ohne Datei, steht er in `CLAUDE.md` oder in einer anderen Datei unter `handbuch/`: Die Tabelle «Weitere Teile des Handbuchs» in `CLAUDE.md` sagt, was wo steht.

## Kette

Eine Kette sind mehrere Läufe hintereinander, von denen jeder am Schluss den nächsten auslöst. Sie läuft nur nach einem Entscheid von Joss. Ihr Name, ihr Programm, die Höchstzahl der Glieder und die Schluss-Zeit stehen in `BACKLOG.md` unter «Kette». Steht dort «keine Kette», endet ein Lauf, der als Glied ausgelöst wurde, sofort. Für die Arbeit selbst gilt dieses Handbuch, die «Reihenfolge» im Backlog gilt für ein Glied nicht.

Ein Glied arbeitet so:

1. **Nummer.** N ist die Zahl der Einträge in `CHANGELOG.md`, deren Überschrift den Namen der Kette und «Glied» enthält, plus eins. Die Zusatznachricht («Glied N») trifft oft erst ein, wenn der Lauf schon arbeitet oder fertig ist. Sie ändert nichts und ist nie ein zweiter Auftrag: Trifft sie nach dem Bericht ein, ist die Antwort nur «erledigt». In der Nacht auf den 18. November 2026 sind so mehrere Läufe doppelt gelaufen.
2. **Anmelden.** In `data/protokoll/auftraege.md` die Zeile «- <Name der Kette>, Glied N, gestartet HH:MM Uhr» anhängen, nur diese Datei committen und sofort pushen. Lehnt GitHub ab, oder steht nach `git pull --rebase origin main` schon eine Zeile für Glied N da, läuft ein Doppel: sofort enden, nichts ändern, nichts auslösen.
3. **Ein Schritt.** Den ersten Schritt des Programms erledigen, der offen ist. Ein Schritt mit mehreren Portionen (zum Beispiel Übersetzungen) bleibt offen, bis nichts mehr fehlt. Dann macht das Glied eine Portion.
4. **Abschliessen.** `python3 build.py` und `node tests/seiten.js` müssen fehlerfrei sein. In `BACKLOG.md` erledigte Schritte des Programms abhaken. In `CHANGELOG.md` zuoberst ein Eintrag mit der Überschrift «## <Datum>, <Name der Kette>, Glied N: <Schritt>». Die Zeile in `auftraege.md` löschen. Ein Glied ändert nie `build.py`, `assets/`, `tests/` oder dieses Handbuch: Daran kann gleichzeitig Claude in der Sitzung mit Joss arbeiten. Darum in zwei Commits veröffentlichen, zuerst Daten und Protokoll, dann die neu gebauten Seiten:

   ```
   git add data/ BACKLOG.md CHANGELOG.md backlog/ changelog/ && git commit -m "<Name der Kette>, Glied N: <was neu ist>"
   git checkout -- . && git clean -fdq
   git pull --rebase origin main && python3 build.py && node tests/seiten.js
   git add -A && git commit -m "Seiten neu gebaut nach Glied N" && git push origin HEAD:main
   ```

   Lehnt GitHub den Push ab: `git reset --hard HEAD~1` (nur den Commit mit den Seiten verwerfen), dann die letzten zwei Zeilen wiederholen, höchstens fünfmal. Meldet der Bau nach dem Pull einen Fehler in einer eigenen Datei: beheben, als weiteren Daten-Commit festhalten, wiederholen. Ein Konflikt in `BACKLOG.md` oder `CHANGELOG.md`: beide Fassungen behalten.
5. **Weitergeben.** Das nächste Glied auslösen: genau ein Aufruf des Werkzeugs `fire_trigger` mit der Aufgabe aus dem Auftrag des Laufs und dem Text «Glied N+1». Nicht auslösen, wenn N die Höchstzahl erreicht hat, das Programm erledigt ist, die Schluss-Zeit vorbei ist, der Push nicht gelungen ist, Build oder Test am Schluss Fehler hatten, `gh run list -R Josidos/gassi-kompass --workflow pages-build-deployment --limit 3` beim neuesten abgeschlossenen Lauf «failure» zeigt, oder schon das Glied davor denselben Schritt versucht hat, ohne etwas zu veröffentlichen.
6. **Ende.** Ist das Programm erledigt, trägt das letzte Glied in `BACKLOG.md` unter «Kette» wieder «keine Kette» ein und nennt im Bericht den Stand.

## Parallel-Läufe

Soll viel auf einmal entstehen, arbeiten mehrere Läufe gleichzeitig. Jeder hat genau einen Auftrag: einen Kanton samt seiner grössten Gemeinde, bis zu vier Gemeinden, Lücken einer bestehenden Seite oder eine Gegenprüfung. Der Auftrag steht in der Nachricht, die den Lauf auslöst, und hat einen Namen wie `so`, `gemeinden-zh-1` oder `pruefung-so`. Die Qualitätsregeln gelten unverändert. Damit sich zwei Läufe nie dieselbe Datei teilen, gilt:

Parallel-Läufe startet nur Claude in einer Sitzung mit Joss und nur nach seinem Entscheid, weil sie deutlich mehr Guthaben kosten. Der automatische Lauf startet nie welche. Erfahrung aus der Nacht auf den 18. November 2026: Das Konto hat eine Nutzungsgrenze. Ist sie erreicht, brechen alle Läufe mitten in der Arbeit ab, und was nicht veröffentlicht ist, geht verloren. Darum hat jede Staffel eine Schluss-Zeit, und jedes fertige Stück wird sofort veröffentlicht. Erfahrung aus der Nacht auf den 28. November 2026: Fünf Unteragenten auf Opus und ein Lauf verbrauchten die Hälfte der 5-Stunden-Grenze in rund 20 Minuten und brachen um 00:42 Uhr ab. Verloren ging nichts, weil jede Gemeinde einzeln veröffentlicht war und das Angefangene in den Arbeitskopien lag. Seither gilt: höchstens zwei Parallel-Läufe gleichzeitig (bis 28. November 2026: fünf), nie neben einem laufenden automatischen Lauf, und vorher fragt Claude nach dem Stand der Nutzung in den Einstellungen von Joss. Zeigt die 5-Stunden-Anzeige weniger als die Hälfte frei, startet er keine. Eine Gemeinde auf Opus kostet rund 50'000 bis 60'000 Token, die Gegenprobe mit dem `quellenleser` rund 10'000 bis 15'000 je Gemeinde.

### Für den Parallel-Lauf

- Nur den Auftrag erledigen. Kein Nachprüfen, kein Einsammeln, nichts Weiteres aus dem Backlog.
- Alles, was du anlegst oder änderst, liegt unter `data/`: die Datendateien, die der Auftrag nennt, neue Quellen in `data/quellen/<auftragsname>.json` (Schlüssel wie üblich `<kt>_<stichwort>`, keiner darf schon in einer anderen Quellendatei stehen) und das Protokoll `data/protokoll/<auftragsname>.md`.
- Nie ändern: `BACKLOG.md`, `CHANGELOG.md`, `data/quellen.json`, `data/protokoll/auftraege.md`, Datendateien anderer Aufträge, `build.py`, `assets/`, `tests/`, dieses Handbuch.
- Das Protokoll hat zwei Teile. «Protokoll»: was sonst in `CHANGELOG.md` stünde (neu, geändert mit alt und neu, weggelassen und warum, nicht gelungen). «Backlog»: was sonst in `BACKLOG.md` stünde (erledigt, zurückgestellt mit Grund, bei einem neuen Kanton drei bis fünf weitere Gemeinden für `backlog/gemeinden.md`, neue Lücken für `backlog/luecken.md`).
- Kanton unvollständig: Stand als `data/entwurf/<kt>.json` sichern und im Protokoll festhalten, was fehlt. Gemeinde unter drei belegten Angaben: keine Datei, im Protokoll als zurückgestellt mit Grund.
- Vor dem Commit müssen `python3 build.py` und `node tests/seiten.js` fehlerfrei sein. Die erzeugten Seiten gehören aber nicht in den Commit, sie entstehen beim Einsammeln. `git status --short data/` darf nur eigene Dateien zeigen. Dann genau so veröffentlichen:

  ```
  git add data/ && git commit -m "Parallel-Lauf <auftragsname>: <was neu ist>"
  git checkout -- . && git clean -fdq
  git pull --rebase origin main && python3 build.py --check && git push origin HEAD:main
  ```

  Lehnt GitHub den Push ab, die letzte Zeile wiederholen, höchstens fünfmal. Meldet `build.py --check` nach dem Pull einen Fehler in deinen Dateien (zum Beispiel einen doppelten Quellenschlüssel): beheben, neu committen, wiederholen. Nie pushen, solange `--check` einen Fehler meldet.
- Liegt die Zieldatei des Auftrags schon auf `main`, weil ein anderer Lauf schneller war: eigene Arbeit verwerfen und enden.
- Nennt der Auftrag eine Uhrzeit als Schluss: mit `TZ=Europe/Zurich date` prüfen. Danach keine neue Recherche beginnen, sondern veröffentlichen, was belegt ist, und enden.
- Die Veröffentlichung auf GitHub Pages musst du nicht abwarten.

### Für jeden anderen Lauf

- **Vergebene Aufträge.** `data/protokoll/auftraege.md` nennt, welche Kantone, Gemeinden und Dateien an Parallel-Läufe vergeben sind, mit Uhrzeit. Was dort steht, lässt du aus und änderst du nicht, solange der Auftrag jünger als drei Stunden ist. Ist er älter und hat nichts geliefert, ist der Parallel-Lauf gescheitert: Zeile löschen, der Eintrag im Backlog ist wieder offen.
- **Einsammeln**, gleich nach dem Start: Für jedes Protokoll unter `data/protokoll/` (ausser `auftraege.md`), dessen Auftrag fertig ist, den Teil «Protokoll» als eigenen Eintrag in `CHANGELOG.md` übernehmen, den Teil «Backlog» in `BACKLOG.md` nachführen (Kanton oder Gemeinde abhaken, Zurückgestelltes vermerken, Neues eintragen), dann das Protokoll und die Zeile in `auftraege.md` löschen. Die Seiten entstehen beim Bauen am Schluss des Laufs. Fertig ist ein Auftrag, wenn `auftraege.md` für ihn keine Schluss-Zeit nennt oder diese vorbei ist. Vorher bleibt sein Protokoll liegen (Regel seit 28. November 2026): Ein Parallel-Lauf, der nach jedem Stück veröffentlicht, schreibt bis zum Schluss an seinem Protokoll weiter. Wird es vorher gelöscht, läuft sein nächster Push in einen Konflikt, und die Zeile in `auftraege.md` fehlt, obwohl er noch arbeitet.
- Meldet `python3 build.py --check` einen Fehler in einer Datei aus einem Parallel-Lauf, den du in zwei Versuchen nicht beheben kannst: Kantonsdatei nach `data/entwurf/` verschieben, Gemeindedatei löschen, im Backlog «zurückgestellt» mit Grund.
- Für die Reihenfolge im Backlog zählt ein Kanton als erfasst, sobald seine Datei unter `data/kantone/`, `data/fr-ch/kantone/` oder `data/it-ch/kantone/` liegt. Ein zweisprachiger Kanton ist erst mit beiden Fassungen erledigt.
