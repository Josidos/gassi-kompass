# Ausbauliste

Erledigtes abhaken und das Datum dahinter schreiben. Was sich nicht belegen lässt, mit Datum und Grund als «zurückgestellt» markieren und weitergehen.

## Reihenfolge

Ziel: alle 26 Kantone, jeder in seinen Amtssprachen. Für jeden Lauf gilt die erste Zeile, die zutrifft:

1. **Sonderlauf Themenseiten.** Sind 10 Kantone erfasst und ist der Punkt in Abschnitt 5 offen, macht der Lauf nur das.
2. **Sonderlauf Mehrsprachigkeit.** Ist Abschnitt 1 erledigt und ist der Punkt in Abschnitt 5 offen, macht der Lauf nur das.
3. **Neuer Kanton.** Der oberste offene Kanton aus Abschnitt 1. Dazu seine grösste Gemeinde oder sein Hauptort. Ist Abschnitt 1 erledigt und die Mehrsprachigkeit in Abschnitt 5 abgehakt: der oberste offene Eintrag aus Abschnitt 2.
4. **Gemeinden.** Ist kein Kanton möglich, bis zu 4 Gemeinden aus Abschnitt 3.

In jedem Lauf ausser den Sonderläufen zusätzlich höchstens eine Lücke aus Abschnitt 4.

## 1. Deutschsprachige Kantone

Ungefähr nach Bevölkerung. Schon erfasst: Zürich, Bern, Luzern.

- [ ] Aargau (`ag`)
- [ ] St. Gallen (`sg`)
- [ ] Basel-Stadt (`bs`)
- [ ] Basel-Landschaft (`bl`)
- [ ] Thurgau (`tg`)
- [ ] Solothurn (`so`)
- [ ] Graubünden (`gr`)
- [ ] Schwyz (`sz`)
- [ ] Zug (`zg`)
- [ ] Schaffhausen (`sh`)
- [ ] Appenzell Ausserrhoden (`ar`)
- [ ] Nidwalden (`nw`)
- [ ] Glarus (`gl`)
- [ ] Obwalden (`ow`)
- [ ] Uri (`ur`)
- [ ] Appenzell Innerrhoden (`ai`)

## 2. Französisch und Italienisch

Erst nach dem Sonderlauf Mehrsprachigkeit. Bei zweisprachigen Kantonen beide Fassungen im selben Lauf, weil die Quellen dieselben sind.

- [ ] Waadt (`vd`), französisch
- [ ] Genf (`ge`), französisch
- [ ] Wallis (`vs`), französisch und deutsch
- [ ] Freiburg (`fr`), französisch und deutsch
- [ ] Tessin (`ti`), italienisch
- [ ] Neuenburg (`ne`), französisch
- [ ] Jura (`ju`), französisch
- [ ] Bern (`be`), französische Fassung des Kantons und von Biel/Bienne
- [ ] Graubünden (`gr`), italienische Fassung

## 3. Gemeinden

Ungefähr nach Grösse. Neue Kantone tragen hier ihre grössten Gemeinden ein.

- [ ] Winterthur (ZH)
- [ ] Biel/Bienne (BE), Adresse `biel-bienne`
- [ ] Thun (BE)
- [ ] Köniz (BE)
- [ ] Uster (ZH)
- [ ] Emmen (LU)
- [ ] Dübendorf (ZH)
- [ ] Kriens (LU)
- [ ] Dietikon (ZH)
- [ ] Wetzikon (ZH)
- [ ] Wädenswil (ZH)
- [ ] Burgdorf (BE)
- [ ] Langenthal (BE)
- [ ] Horgen (ZH)
- [ ] Bülach (ZH)
- [ ] Kloten (ZH)
- [ ] Horw (LU)
- [ ] Ebikon (LU)
- [ ] Steffisburg (BE)
- [ ] Ostermundigen (BE)
- [ ] Opfikon (ZH)
- [ ] Thalwil (ZH)
- [ ] Adliswil (ZH)
- [ ] Sursee (LU)
- [ ] Muri bei Bern (BE)
- [ ] Regensdorf (ZH)
- [ ] Illnau-Effretikon (ZH)
- [ ] Schlieren (ZH)
- [ ] Volketswil (ZH)
- [ ] Spiez (BE)
- [ ] Lyss (BE)
- [ ] Münsingen (BE)
- [ ] Worb (BE)
- [ ] Ittigen (BE)
- [ ] Hochdorf (LU)
- [ ] Willisau (LU)

## 4. Lücken in bestehenden Seiten

- [ ] Stadt Zürich: Betrag der Hundeabgabe belegen und als Karte «Hundeabgabe» ergänzen
- [ ] Stadt Zürich: Freilaufzonen aus dem städtischen Datensatz «Hundezonen» namentlich aufführen
- [ ] Stadt Bern: Betrag der Hundetaxe belegen
- [ ] Stadt Bern: Quelle «Gemeinderat Bern 2019» (Tierpark, Kinderzoo) durch eine aktuelle amtliche Quelle ersetzen
- [ ] Stadt Luzern: Bussen mit einer Quelle nach 2022 belegen
- [ ] Kanton Bern: «kein Kursobligatorium» mit einer Quelle des Kantons statt der Gemeinde Büren belegen
- [ ] Kanton Bern: Entscheid des Grossen Rats von 2023 zur Wald-Leinenpflicht mit einer amtlichen Quelle (Ratsprotokoll) belegen

## 5. Umbauten am Generator

Vorgaben in `CLAUDE.md` unter «Umbauten am Generator».

- [ ] Themenseiten
- [ ] Mehrsprachigkeit (Französisch und Italienisch)

## 6. Ideen für später

Aus dem Vergleich mit anderen Seiten. Erst angehen, wenn alle Kantone erfasst sind, jeweils als Sonderlauf.

- Rassen-Check: Rasse wählen und sehen, in welchen Kantonen sie verboten oder bewilligungspflichtig ist. Braucht die Rasselisten als eigene Datenfelder.
- Kantone direkt vergleichen: zwei Kantone wählen und nur die Unterschiede sehen (für den Umzug).
- Checkliste «Neu mit Hund» pro Kanton zum Abhaken und Drucken, erzeugt aus den Karten.
- «Standort verwenden» in der Ortssuche. Die Koordinaten stehen im Ortschaftenverzeichnis.
- Fragen als Überschriften («Braucht es im Kanton Zürich einen Hundekurs?»), sobald die Suchdaten zeigen, wie gefragt wird.

## 7. Braucht Zugriff, den der Lauf nicht hat

- Ortsverzeichnis `data/orte.json` auf den aktuellen Stand bringen. Es braucht die aktuelle CSV-Datei «Amtliches Ortschaftenverzeichnis» von swisstopo, dann `python3 tools/orte.py DATEI "Stand"`. Der Lauf kann die Datei nicht abrufen. Offen, bis Joss sie liefert oder Claude sie in einer Sitzung mit Browser holt.
- Suchdaten aus der Google Search Console auswerten: macht Claude in einer Sitzung über den Browser von Joss.
- «Fehler melden» auf jeder Seite: braucht eine Kontaktadresse, die Joss freigibt.

## 8. Später, nur nach Freigabe von Joss

- Übersetzungen in Sprachen, die am Ort nicht Amtssprache sind, auch Englisch
- Anzeigen und Affiliate-Links
- Impressum und Datenschutzerklärung
- Anschreiben an Behörden, Vereine und Medien
