# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Drei Lesergruppen, alle bestätigt:

- Hundehaltende unterwegs am Telefon, kurz vor oder während dem Spaziergang. Ihre Frage: Muss mein Hund hier an die Leine?
- Wer umzieht oder einen Hund übernimmt. Ihre Fragen: Haftpflicht, Kurs, Anmeldung, Hundesteuer, Rassen, was im neuen Kanton gilt.
- Ämter und Fachleute (Veterinärdienste, Hundeschulen, Medien), die Angaben prüfen oder verlinken. Die Seite muss man einem Amt zeigen können.

## Product Purpose

Gassi-Kompass sagt für jeden Ort der Schweiz, was für Hunde gilt: Regeln des Bundes, des Kantons und, wo amtlich belegt, der Gemeinde. Jede Angabe trägt ihre amtliche Quelle. Erfolg heisst: Wer nach Ort und Thema sucht («Leinenpflicht Aargau», «Hundesteuer Winterthur»), findet über Google die Seite und dort die Antwort in Sekunden.

## Positioning

Alle 26 Kantone und die grösseren Gemeinden an einem Ort, in Deutsch, Französisch und Italienisch, jede Angabe mit Link zur amtlichen Quelle und Prüfdatum. Dazu der Wald-Status für heute (Leinenpflicht im Wald nach Saison) und Vergleichsseiten je Thema über alle Kantone.

## Operating Context

- Statische Website auf GitHub Pages, erzeugt von `build.py` aus JSON-Daten. Ein automatischer Lauf pflegt die Daten. Seitentypen: Startseite mit Ortssuche, Kanton, Gemeinde, Thema (Vergleich aller Kantone), Bund, Über diese Seite, Fehlerseite, je in drei Sprachen.
- Häufig gelesen auf dem Telefon, im Freien, mit schlechtem Netz.

## Capabilities and Constraints

- Adressen, Seitentitel, Inhalte und Funktionen bleiben. Die Seitentitel nennen Ort und Thema (Suchmaschine).
- Zuoberst steht die Antwort auf die häufigste Frage: Muss mein Hund hier an die Leine? Auf dem Telefon sofort sichtbar.
- Keine externen Skripte oder Schriften, kein Tracking, keine Cookies. Schriften liegen selbst gehostet unter `assets/fonts/`.
- Die Seite ist privat und darf nie wie die Seite eines Kantons, einer Gemeinde oder des Bundes wirken (Handbuch, Regel 9).
- Leicht und schnell: keine grossen Bilder, wenig Bewegung.
- Später kommen Anzeigen dazu (noch nicht freigegeben).

## Brand Commitments

- Name «Gassi-Kompass». Logo, Farben und Schriften sind frei (Entscheid vom 23. November 2026).
- Sprache: kurze Sätze, Du-Form (Französisch «vous», Italienisch «tu»), Schweizer Rechtschreibung, keine Werbesprache.
- Nicht verspielt: kein Comic, keine Pfoten- oder Knochen-Deko, kein Werbe-Look.

## Evidence on Hand

- 26 Kantone, 60 Gemeinden, über 300 amtliche Quellen in `data/`.
- Keine Fotos, keine Testimonials, keine Besucherzahlen. Nichts davon erfinden.

## Product Principles

1. Richtigkeit vor Menge: lieber weglassen als unbelegt zeigen.
2. Die Antwort zuerst, die Quelle immer daneben.
3. Gleich gut in drei Sprachen und auf dem Telefon.
4. Glaubwürdig genug für ein Amt, ohne amtlich zu wirken.

## Accessibility & Inclusion

Gute Lesbarkeit draussen bei Tageslicht (Kontrast), Bedienung mit Tastatur, kein Text in Bildern.
