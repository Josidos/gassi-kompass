# Parallel-Lauf fr-fr (Staffel E), 2026-11-17

## Protokoll

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

## Backlog

- Abschnitt 2: Freiburg (`fr`), französisch und deutsch, erfasst. Die deutsche Seite wird sofort gebaut, die französischen Dateien liegen unter `data/fr-ch/` und warten auf den Sonderlauf Mehrsprachigkeit. Mit kopierten Dateien gebaut und getestet.
- Weitere Gemeinden für Abschnitt 3: Bulle (französisch), Villars-sur-Glâne (französisch), Düdingen (deutsch), Murten/Morat (deutsch und französisch), Estavayer (französisch). Hinweis: Viele Freiburger Gemeinden haben ein «Règlement sur la détention et l'imposition des chiens» nach kantonalem Muster, mit Steuerbetrag, Leinenzonen und Bussen.
- Neue Lücken für Abschnitt 4:
  - `fr`: geltende deutsche Fassung des HHR (SGF 725.31, 2024) abrufen und die deutsche Datei damit belegen (Haftpflicht, Fristen).
  - `fr`: Bewilligung für mehr als vier Hunde und Ordnungsbusse für die Leine im Wald (OCAO, FR 107) belegen.
  - `fr/fribourg`: heutigen Betrag der Gemeindesteuer bestätigen. Das Reglement von 1993 nennt CHF 120, eine neuere amtliche Angabe der Stadt wurde nicht gefunden. Anmeldestelle der Stadt und allfällige Freilaufzonen suchen.
