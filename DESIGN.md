---
name: Gassi-Kompass
description: Hunderegeln der Schweiz nach Kanton und Gemeinde, jede Angabe mit amtlicher Quelle.
colors:
  paper: "#F5F7F4"
  sheet: "#FFFFFF"
  sunk: "#E9EDE8"
  rule: "#C9D2CA"
  rule-soft: "#DEE4DE"
  ink: "#16201A"
  ink-2: "#47544B"
  binding: "#1E3B2C"
  binding-2: "#2C5140"
  binding-3: "#3B6450"
  on-binding: "#F1F5EF"
  on-binding-2: "#BFD0C3"
  must: "#A3381C"
  must-bg: "#F6E4DD"
  free: "#2B6537"
  free-bg: "#E1EDE1"
  note: "#2D5476"
  note-bg: "#E2E9F1"
  none: "#56625A"
  none-bg: "#E6EAE5"
  code: "#B8451F"
  on-code: "#FFF8F4"
  focus: "#2D5476"
typography:
  display:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.35rem, 1.35rem + 4.2vw, 3.75rem)"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.005em"
    fontVariation: "\"wdth\" 76"
  status:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.75rem, 1.15rem + 2.5vw, 2.55rem)"
    fontWeight: 800
    lineHeight: 1.02
    fontVariation: "\"wdth\" 76"
  headline:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.5rem, 1.2rem + 1.1vw, 1.9rem)"
    fontWeight: 780
    lineHeight: 1.1
    fontVariation: "\"wdth\" 80"
  title:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.3rem"
    fontWeight: 780
    lineHeight: 1.15
    fontVariation: "\"wdth\" 82"
    fontFeature: "\"tnum\""
  title-sm:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.08rem"
    fontWeight: 760
    lineHeight: 1.2
    fontVariation: "\"wdth\" 88"
  body:
    fontFamily: "Source Serif 4, Charter, Cambria, Georgia, serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
  lede:
    fontFamily: "Source Serif 4, Charter, Cambria, Georgia, serif"
    fontSize: "1.12rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.74rem"
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: "0.02em"
    fontFeature: "\"tnum\""
  meta:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  tag: "2px"
  base: "3px"
  tab: "4px"
spacing:
  inline: "8px"
  gutter: "16px"
  stack: "18px"
  column: "40px"
  section-mobile: "40px"
  section: "48px"
components:
  chip-must:
    backgroundColor: "{colors.must-bg}"
    textColor: "{colors.must}"
    typography: "{typography.label}"
    rounded: "{rounded.tag}"
    padding: "2px 8px"
  chip-free:
    backgroundColor: "{colors.free-bg}"
    textColor: "{colors.free}"
    typography: "{typography.label}"
    rounded: "{rounded.tag}"
    padding: "2px 8px"
  chip-note:
    backgroundColor: "{colors.note-bg}"
    textColor: "{colors.note}"
    typography: "{typography.label}"
    rounded: "{rounded.tag}"
    padding: "2px 8px"
  chip-none:
    backgroundColor: "{colors.none-bg}"
    textColor: "{colors.none}"
    typography: "{typography.label}"
    rounded: "{rounded.tag}"
    padding: "2px 8px"
  register-tab:
    backgroundColor: "{colors.binding-2}"
    textColor: "{colors.on-binding}"
    rounded: "{rounded.tab}"
    padding: "6px 14px"
    height: "38px"
  register-tab-hover:
    backgroundColor: "{colors.binding-3}"
  register-tab-current:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
  code-square:
    backgroundColor: "{colors.code}"
    textColor: "{colors.on-code}"
    rounded: "{rounded.tag}"
    width: "40px"
    height: "34px"
  plate:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.base}"
    padding: "8px 14px"
    height: "44px"
  plate-hover:
    backgroundColor: "{colors.sunk}"
  plate-current:
    backgroundColor: "{colors.binding}"
    textColor: "{colors.on-binding}"
  search-input:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.base}"
    padding: "14px 16px"
  forest-panel:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.base}"
    padding: "20px 22px 22px"
  lang-button:
    backgroundColor: "{colors.binding}"
    textColor: "{colors.on-binding}"
    rounded: "{rounded.tag}"
    padding: "4px 9px"
  lang-button-hover:
    backgroundColor: "{colors.binding-2}"
---

# Design System: Gassi-Kompass

## Overview

**Creative North Star: "Der Feldführer"**

Gassi-Kompass sieht aus wie ein Bestimmungsbuch für Hunderegeln. Jeder Ort ist ein Eintrag mit Kennung, Merkmalen und Beleg. Ein moosgrüner Einband trägt Kopf und Fuss über die ganze Breite, dazwischen liegt kühles Papier. Einträge stehen ohne Kästen auf dem Papier, getrennt durch feine Linien. Zwischen Merkmal und Marke läuft eine punktierte Führungslinie wie im Bestimmungsschlüssel.

Die Seite ist zum Nachlesen gemacht: ruhig, dicht, belegt. Die Antwort steht zuerst (die Tafel «Leine im Wald» mit grossem Status und Monatsleiste), die Quelle immer daneben. Farbe trägt Bedeutung, nicht Stimmung: Rost heisst Pflicht, Blattgrün heisst frei, Schieferblau heisst Hinweis. Bewegung gibt es nur als Farbwechsel bei Hover und Fokus.

Die Seite ist privat und darf nie wie ein Amt wirken. Darum kein Wappen und keine amtlich wirkenden Zeichen. Nicht verspielt: keine Pfoten, keine Knochen, kein Werbe-Look.

**Key Characteristics:**
- Einband in Moosgrün oben und unten, vollbreit; Papier dazwischen.
- Einträge mit Linien statt Karten mit Rahmen.
- Punktierte Führungslinie zwischen Merkmal und Marke.
- Register-Reiter als Pfad am Einband; der aktuelle Reiter hat die Farbe des Papiers.
- Kennungen (ZH, AG) in schmaler, fetter Archivo auf Rost-Quadraten.
- Lesetext in Source Serif 4, alles Bedienbare und alle Überschriften in schmaler Archivo.
- Hell und dunkel, beide aus denselben Variablen.

## Colors

Wenige, gedeckte Naturfarben auf kühlem Papier; die drei Signalfarben stehen für genau drei Bedeutungen.

### Primary
- **Einband-Moosgrün** (binding): Kopf und Fuss über die ganze Breite, gewählte Tafel, Textmarkierung. Die Abstufungen binding-2 (Reiter, Hover auf Sprachknöpfen) und binding-3 (Rahmen auf dem Einband, Hover auf Reitern) bleiben auf dem Einband.
- **Hell auf Einband** (on-binding, on-binding-2): Schrift auf dem Einband, die zweite Stufe für Prüfdatum und Fusstext.

### Secondary
- **Rost** (must): Pflicht und Verbot. Marke «Pflicht», Leinenmonate in der Monatsleiste, Linie über der Leinenliste, Status «Leinenpflicht». Hintergrund dazu must-bg.
- **Kennungs-Rost** (code, on-code): nur die Quadrate der Kantonskennungen und das Zeichen der Wortmarke.

### Tertiary
- **Blattgrün** (free, free-bg): keine Pflicht, Status «Heute keine Leinenpflicht», Freilaufzonen, «Seite vorhanden» in Tafeln.
- **Schieferblau** (note, note-bg): neutrale Hinweise, Hinweiskasten, «Mehr»-Aufklapper. Gleicher Wert wie **focus**, der Fokusrahmen.
- **Stein** (none, none-bg): Marke «keine Pflicht» und neutrale Verbots-Marke.

### Neutral
- **Papier** (paper): Seitengrund.
- **Blatt** (sheet): erhöhte Flächen: Tafel «Leine im Wald», Suchfeld, Tafeln, Übersetzungshinweis.
- **Vertieft** (sunk): Hover auf Tafeln, hervorgehobene Tabellenspalte, schlichte Hinweise.
- **Linie** (rule, rule-soft): Trennlinien und Rahmen; die weiche Stufe zwischen Einträgen derselben Liste.
- **Tinte** (ink, ink-2): Text; ink-2 für Einleitung, Quellen, Beschriftungen. Volle Tinte auch für die 2px-Linie über Listen und Tabellen.

Dunkelmodus: alle Variablen haben eigene Werte unter `prefers-color-scheme: dark` und `[data-theme="dark"]` (Werte im Sidecar). Der Einband wird fast schwarz-grün, die Signalfarben werden heller und die Hintergründe dunkel.

### Named Rules
**The Drei-Signale Rule.** Rost, Blattgrün und Schieferblau bedeuten Pflicht, frei und Hinweis, nichts anderes. Keine Signalfarbe als Schmuck.

**The Einband Rule.** Moosgrün gehört dem Einband und dem gewählten Zustand. Es wird keine Hintergrundfarbe für Abschnitte im Inhalt.

## Typography

**Display Font:** Archivo, variabel mit Breitenachse (Fallback Helvetica Neue, Arial)
**Body Font:** Source Serif 4 (Fallback Charter, Cambria, Georgia)

**Character:** Schmale, fette Archivo gibt Überschriften und Kennungen die Knappheit eines Registers; die Serife trägt den Lesetext ruhig und gut lesbar im Freien. Beide Schriften liegen selbst gehostet unter `assets/fonts/`.

### Hierarchy
- **Display** (800, Breite 76 %, fliessend bis 3.75rem, Zeilenhöhe 1): Seitentitel, höchstens etwa 20 Zeichen breit, ausgeglichen umbrochen.
- **Status** (800, Breite 76 %, fliessend bis 2.55rem): der Status in der Tafel «Leine im Wald», gefärbt in Rost oder Blattgrün.
- **Headline** (780, Breite 80 %, fliessend bis 1.9rem): Abschnittsüberschriften. Der Geltungsbereich steht in der Überschrift («Leine und Zutritt im Kanton Zürich»).
- **Title** (780, Breite 82 %, 1.3rem): Wert eines Merkmals («CHF 120», «Pflicht»), tabellarische Ziffern.
- **Title klein** (750 bis 760, Breite 85 bis 90 %, rund 1rem bis 1.1rem): Listenköpfe, Merkmalsnamen, Kantonsnamen im Register.
- **Body** (400, 17px, 1.55): Lesetext, höchstens 60 bis 68 Zeichen pro Zeile.
- **Lede** (400, 1.12rem, 1.5, ink-2): Einleitung unter dem Titel.
- **Label** (700, 0.74rem, 0.02em): Marken.
- **Meta** (400, 0.78rem): Quellen, Prüfdatum, Monatsnamen, Beschriftungen.

### Named Rules
**The Zwei-Stimmen Rule.** Archivo für alles, was man bedient oder überfliegt (Überschriften, Marken, Tafeln, Tabellen, Kopf und Fuss); Source Serif 4 nur für Fliesstext.

**The Ziffern Rule.** Beträge, Daten, Zahlen und Kennungen stehen in tabellarischen Ziffern.

## Layout

Eine Spalte von höchstens 1000px, seitlicher Rand 16px (mindestens die Safe Area). Abschnitte stehen 48px auseinander, auf dem Telefon 40px; innerhalb eines Abschnitts 18px. Kopf und Fuss reichen über die ganze Fensterbreite, ohne seitliches Überlaufen.

Merkmale stehen in einem automatischen Raster mit Spalten ab 360px und 40px Spaltenabstand, am Bildschirm also zwei Spalten. «Leine» und «Kein Zutritt» stehen ab 720px nebeneinander. Die Tafel «Leine im Wald» teilt sich ab 780px in Status links und Monatsleiste rechts. Das Kantonsregister füllt Spalten ab 210px, das Gemeindeverzeichnis ist ab 860px zweispaltig. Die Zeilen der Themenseiten stellen unter 640px den Kurztext unter Name und Marke. Unter 480px werden Kopf, Reiter, Monatsnamen und die Tafel kompakter.

## Elevation & Depth

Die Seite ist flach. Tiefe entsteht durch Papierstufen (paper, sheet, sunk) und durch den Einband. Genau ein Element hebt sich ab: die Tafel «Leine im Wald», weil sie die Antwort trägt.

### Shadow Vocabulary
- **Tafel-Schatten** (`box-shadow: 0 1px 0 var(--rule-soft), 0 10px 24px -18px rgb(22 32 26 / .35)`): nur die Tafel «Leine im Wald».

### Named Rules
**The Eine-Tafel Rule.** Nur die Antwort auf die häufigste Frage liegt erhöht. Alles andere liegt flach auf dem Papier.

## Shapes

Fast eckig. Marken, Kennungs-Quadrate und Monatsleiste 2px, Tafeln, Felder und Hinweise 3px, die Register-Reiter 4px oben und unten offen, damit der aktuelle Reiter in das Papier übergeht. Linien statt Rahmen: 2px Tinte über Listen, Tabellen und Registern; 3px über den Spalten «Leine» (Rost) und «Kein Zutritt» (Tinte); 1px zwischen Einträgen. Listenpunkte sind kleine Quadrate (8px). Was in dieser Sprache noch fehlt, hat einen gestrichelten Rahmen.

## Components

### Register-Reiter (Pfad)
Der Pfad hängt als Reiter am Einband. Reiter in binding-2 mit heller Schrift, mindestens 38px hoch; Hover binding-3. Der aktuelle Reiter hat die Farbe des Papiers und dunkle Schrift und geht nahtlos in die Seite über.

### Marken
Kleine Stempel in Archivo 700, 0.74rem, Ecken 2px, Farbpaar aus Signalfarbe auf ihrem hellen Grund: Pflicht (Rost), frei (Blattgrün), Hinweis (Schieferblau), keine Pflicht (Stein).

### Merkmal (Eintrag)
Kein Kasten: Linie oben (1px), Name des Merkmals in ink-2, punktierte Führungslinie (2px gepunktet, rule) bis zur Marke, darunter der Wert gross (Title), der Text und die Quellen in Meta. Weitere Punkte hinter einem Aufklapper in Schieferblau. Kurze Einträge wie Rassen stehen dort in zwei Spalten, ganze Sätze in einer Spalte mit höchstens 65 Zeichen Breite (`ul.saetze`, der Generator entscheidet nach der mittleren Länge der Einträge). Kein Eintrag bricht über zwei Spalten.

### Tafel «Leine im Wald»
Die Signatur. Blatt auf Papier mit Rahmen und dem einzigen Schatten. Kopfzeile mit Ort, Führungslinie und Datum. Links der Status gross in Rost oder Blattgrün mit Erklärung und Quelle; rechts die Monatsleiste wie die Blühzeit im Pflanzenbuch: zwölf Felder, die Leinenmonate in Rost gefüllt mit dem Wort «LEINE», ein Strich in Tinte mit der Beschriftung «heute».

### Kantonsregister und Tafeln
Im Register steht jede Kantonskennung in einem Rost-Quadrat (40 × 34px), daneben Name und Zahl der Gemeinden; Linien statt Rahmen, Hover unterstreicht den Namen. Eigenständige Tafeln (Suchtreffer, Gemeinden) sind Blatt mit 1px Rahmen, mindestens 44px hoch; Hover sunk mit Einband-Rahmen; gewählt in Moosgrün. Fehlt eine Sprachfassung: gestrichelter Rahmen, durchsichtig.

### Ortssuche
Grosses Feld (1.18rem, Archivo) auf Blatt mit 2px Rahmen in Tinte, Ecken 3px. Fokus 3px Schieferblau mit 2px Abstand. Darunter eine Statuszeile in Meta.

### Suche auf den Seiten
Seit dem 28. November 2026. Dasselbe Feld findet auch Stichworte. Auf der Startseite steht es direkt unter dem Titel, die Einleitung und die Zahlen danach. Unter der Statuszeile zuerst die Tafeln der Orte (unter 640px in voller Breite untereinander), dann die Gruppe «Auf den Seiten gefunden»: Überschrift in Archivo fett 0.95rem, darunter eine Linienliste wie die Themen der Startseite in einer Spalte (2px Tinte oben, 1px rule-soft zwischen den Zeilen, kein Kasten). Je Treffer der Titel der Seite (Archivo, unterstrichen wie ein Thema), die Überschrift des Abschnitts in Archivo halbfett ink-2 0.88rem und ein Ausschnitt in Lesetext ink-2. Das gefundene Wort steht in `<mark>` auf free-bg mit einer 1px-Linie in free darunter, Schrift in ink, in beiden Farbmodi aus der Palette. Jeder Treffer ist mindestens 44px hoch. Keine neuen Farben, kein neuer Knopf. Steht ein Wort auf einer Themenseite bei mehreren Kantonen, nennt die Zeile unter dem Titel statt eines Abschnitts die Zahl («Steht bei 16 Kantonen»), und der Ausschnitt beginnt mit dem Namen des Kantons, aus dem er stammt. Der Ausschnitt beginnt am Anfang des Abschnitts, wenn das Wort dort steht: So zeigt der Treffer bei einer Karte Marke und Wert («Pflicht · mind. CHF 3 Mio.»).

### Sprachwahl
Kleine Knöpfe auf dem Einband mit 1px Rahmen binding-3, Hover binding-2.

### Tabellen
Wie im Bestimmungsbuch: 2px Tinte oben, 1px Linien zwischen Zeilen, Kopf in Meta-Grösse; die gewählte Spalte in sunk. Seit dem 28. November 2026 gibt es auf der Seite keine `<table>` mehr: Die Themenseiten führen die Kantone als Liste von Zeilen zum Aufklappen (`.kt-liste`, `.kt-zeile`, Baustein `kt_zeile()`). Gleiche Linien wie eine Tabelle (2px Tinte oben, 1px rule unter der Kopfzeile und am Ende, 1px rule-soft zwischen den Zeilen), keine Kästen. Am Bildschirm vier Spalten: Kanton (22 %, Archivo fett), Marke (10rem), Kurztext (ink-2), rechts ein kleiner Winkel aus zwei 2px-Linien, der beim Öffnen nach oben zeigt. Darüber eine Kopfzeile in Meta-Grösse. Unter 640px stehen Name, Marke und Winkel in einer Zeile, der Kurztext darunter, ohne Kopfzeile. Hover (nur mit Maus): Zeile in sunk 60 %, Name unterstrichen. Aufgeklappt: Wert in Archivo 1.15rem, Text in Lesetext bis 70ch, Punkte mit 8px-Quadraten, Quellenzeile, Link zur Kantonsseite. Mit Finger als Zeiger ist jede Zeile mindestens 44px hoch.

### Auf einen Blick
Seit dem 28. November 2026. Linienliste wie die Schritte unter «Neu einen Hund», ohne Nummern: 2px Tinte oben, 1px Linien zwischen den Zeilen, je Zeile ein Titel in Archivo als Link und daneben der Wert. Am Bildschirm zwei Spalten (Titel, Wert in Lesetext), mit Marken drei (Titel, Marke, Kurztext in ink-2). Unter 640px stehen Titel und Marke in einer Zeile und der Text darunter. Mit Finger als Zeiger ist die ganze Zeile antippbar und mindestens 44px hoch. Baustein `blick()` in `build.py`, Klassen `.blick`, `.blick.mit-marke`. Gebraucht unter dem Titel der Gemeindeseite und für den Kanton in Kurzform. Seit dem 28. November 2026 auch als Übersicht vor den Karten: auf der Kantonsseite unter «Pflichten» (mit Marken, Kurztext aus `vergleich`, Link auf die Karte derselben Seite) und auf der Seite des Bundes (ohne Marken, mit dem Wert jeder Karte).

### Quellenverzeichnis
Seit dem 28. November 2026, nur auf `/quellen/`. Unter dem Titel das Suchfeld wie die Ortssuche, darunter die Wahl des Geltungsbereichs als Kennungs-Quadrate in Archivo (Blatt mit 1px Rahmen, gewählt in Kennungs-Rost mit heller Schrift wie die Quadrate des Kantonsregisters, «Alle» etwas breiter), dann «Sortieren» mit zwei Textknöpfen (gewählt mit 2px-Unterstrich in Tinte) und die Statuszeile. Die Quellen stehen als Linienliste (2px Tinte oben, 1px rule-soft zwischen den Einträgen, kein Kasten), mit Zwischenüberschriften je Kanton in Archivo. Je Eintrag: kleines Kennungs-Quadrat (24px hoch) und Kurzname in Archivo fett, Langname als Link in Lesetext 0.94rem, «Zitiert auf» als Quellenzeile, darunter Geltungsbereich und Datum in Meta. Mit Finger als Zeiger sind die Quadrate und Sortierknöpfe 44px hoch, die Links der Quellenzeile wie überall 44px. Klassen `.q-wahl`, `.q-k`, `.q-sort`, `.q-liste`, `.q`. Ohne Wahl und ohne Suchwort steht je Kanton eine Zeile wie auf den Themenseiten: Name in Archivo fett 1.08rem, rechts die Zahl der Quellen in Meta und der Winkel der Kantonszeilen, 1px rule-soft dazwischen, mindestens 48px hoch (`.q-kurz`, `.q-g`). Ist ein Kanton gewählt, bleibt seine Zeile als Überschrift stehen, der Winkel zeigt nach oben.

### Sprungleiste
Seit dem 28. November 2026. Eine Zeile Links auf der Kantonsseite und der Seite des Bundes, sonst nirgends. Beim Bund steht sie unter der Einleitung, beim Kanton nach der Tafel «Leine im Wald», damit deren Status am Telefon im ersten Bildschirm bleibt (so seit der Abnahme vom 28. November 2026, 14 Uhr): `<nav class="sprung">` mit der Beschriftung «Auf dieser Seite» in Archivo ink-2, danach die Abschnitte in Archivo halbfett, je ein bis drei Wörter («Leine und Zutritt», «Pflichten», «Neu einen Hund», «Vermisst», «Gemeinden», «Themen», «Quellen»). Je eine 1px-Linie oben und unten, kein Kasten, keine Farbe. Sie rückt 22px näher an die Einleitung als der übliche Abstand zwischen Abschnitten. Am Telefon bricht sie in mehrere Zeilen um, mit Finger als Zeiger ist jeder Link 44px hoch. Die Ziele halten mit `scroll-margin-top` 16px Abstand zum Bildrand. Baustein `sprungleiste()` in `build.py`, Texte in `TEXTE` unter `sprung`.

### Karte der Hundezonen
Die einzige Seitenart, die man bedient statt liest. Vor dem Laden steht im Kartenfeld (vertieft, 1px Rahmen) nur der Hinweis, was geladen wird, und ein Knopf in Tinte mit Schrift in Papierfarbe: der einzige gefüllte Knopf der Seite. Darüber die Wahl der Flächen als drei Kästchen mit Farbfeld auf Blatt. Auf der Karte gelten feste Farben, weil die Kartenbilder in beiden Farbmodi hell bleiben: Blattgrün für Freilaufzonen, Rost für Leinenpflicht (gestrichelte Linie, wenn sie nur zu bestimmten Zeiten gilt), Tinte für Hundeverbot, Schieferblau für den eigenen Standort. Das folgt den Spalten «Leine» (Rost) und «Kein Zutritt» (Tinte). Die Auskunft zu einer Fläche steht als Blatt am unteren Rand der Karte, ohne Schatten, mit «Schliessen» als Textknopf. Die Knöpfe des Kartenprogramms bekommen Blatt, Linie und 3px Ecken. Als Grund dient die graue swissTLM-Karte von swisstopo mit 60 % Deckkraft. Freilaufzonen tragen aus der Ferne einen grünen Punkt mit hellem Rand. Die Karte bewegt sich nur unter dem Finger, und Kartenbilder blenden nicht ein.

### Telefon und Berührung
Seit dem 28. November 2026. Wo der Zeiger ein Finger ist (`@media (pointer:coarse)`), hat jedes freie Ziel eine Tippfläche von rund 44px Höhe, nie unter 28px. Das Bild mit Maus bleibt unverändert. Listen von Links bekommen höhere Zeilen: Gemeindeverzeichnis und Navigation im Fuss 44px je Zeile, Register-Reiter 44px statt 38px, die Zeilen der Themenseiten mindestens 44px. Jede Zeile einer Quellenzeile und jede Quelle im Fuss ist 44px hoch, ohne dass sich Tippflächen überlappen (Zeilenabstand 23px, Tippfläche 11.5px über und unter dem Text). Wo eine höhere Zeile die Seite nur länger machte, wächst die Tippfläche unsichtbar: Quellenzeile, Wortmarke, «Mehr»-Zeilen und Titel der Merkmale haben Innenabstand mit gleich grossem negativem Aussenabstand, Links im Lauftext nur Innenabstand, die Sprachwahl ein unsichtbares Feld um den Knopf, und die Schritte unter «Neu einen Hund» sind als ganze Zeile antippbar. Jede Hover-Regel steht in `@media (hover:hover) and (pointer:fine)`, damit nach dem Antippen nichts hervorgehoben bleibt. Rückmeldung beim Antippen geben `:active` an Tafeln, Reitern und Sprachwahl und das Aufblitzen in Einbandfarbe (`-webkit-tap-highlight-color`, auf dem Einband in Papierfarbe). Kleine Schrift ist bis 640px Breite eine Stufe grösser: Marken 0.8rem statt 0.74rem; Quellenzeile, Untertitel der Tafeln, Datum und Legende der Tafel «Leine im Wald» seit dem Umbau «Übersicht und Sprungmarken» 0.875rem (14px) statt 0.78rem, 0.76rem und 0.8rem, Monatskürzel bis 480px 0.7rem in schmaler Breite (70 %). Der Zoom bleibt frei, Felder haben mindestens 16px Schrift. Geprüft wird mit `node tests/tippflaechen.js`.

### Druck
Seit dem 28. November 2026. Papier ist immer hell: Schwarz auf Weiss, auch wenn der Bildschirm dunkel ist. Ohne Einband und ohne Bedienung, Titel 20pt, Text 11pt. Kopf: Marke und Prüfdatum, darunter eine feine Linie. Alle Zeilen offen, unter jedem Link auf eine Quelle die Adresse in 8pt. Nur der Jahresbalken druckt seine Farben (`print-color-adjust: exact`), alles andere spricht durch Schrift und Linien.

### Fokus
Überall ein sichtbarer Rahmen in Schieferblau (2px bei Links, 3px bei Feldern und Tafeln); auf dem Einband in on-binding.

## Do's and Don'ts

### Do:
- **Do** Farben und Schriften nur über die Variablen in `:root` ändern, hell und dunkel gemeinsam.
- **Do** Einträge mit Linien trennen (1px rule-soft zwischen Einträgen, 2px ink über einer Liste oder Tabelle).
- **Do** Rost nur für Pflicht und Verbot, Blattgrün nur für frei, Schieferblau nur für Hinweis und Fokus verwenden.
- **Do** Überschriften, Marken und Bedienelemente in Archivo mit schmaler Breite (76 bis 90 %) setzen, Lesetext in Source Serif 4.
- **Do** den Geltungsbereich in die Überschrift schreiben («im Kanton Zürich»), nicht in eine Zeile darüber.
- **Do** jede Quelle direkt beim Merkmal in Meta-Grösse zeigen.
- **Do** jede Hover-Regel in `@media (hover:hover) and (pointer:fine)` setzen und Listen von Links für den Finger 44px hoch machen (`tests/tippflaechen.js`).

### Don't:
- **Don't** Merkmale in gerahmte Karten mit gleich grossen Kästen setzen; das Ratgeber-Raster ist die Gegenwelt.
- **Don't** Kicker oder Grossbuchstaben-Zeilen über Überschriften setzen.
- **Don't** weitere Schatten einführen; nur die Tafel «Leine im Wald» liegt erhöht.
- **Don't** Wappen oder amtlich wirkende Zeichen verwenden; die Seite ist privat.
- **Don't** Pfoten, Knochen, Comic oder Werbe-Look.
- **Don't** Bewegung ausser Farbwechsel bei Hover und Fokus; keine externen Schriften oder Skripte. Einzige Ausnahme ist die Karte der Hundezonen: Sie folgt dem Finger und lädt nach einem Klick Kartenbilder von swisstopo.
