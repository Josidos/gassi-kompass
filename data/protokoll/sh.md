# Parallel-Lauf `sh` (Staffel C), 18. November 2026

## Protokoll

Neu:
- `data/kantone/sh.json`: Kanton Schaffhausen, alle Felder belegt. Sechs Quellen in `data/quellen/sh.json`.
- Wald: Leinenpflicht im Wald und in Waldesnähe vom 15. April bis 30. Juni (Merkblatt des Veterinäramts, das Gesetz nennt nur «Setz- und Brutzeit»).
- Haftpflicht mind. CHF 1 Mio., Anmeldung innert 10 Tagen bei der Wohnsitzgemeinde, Hundeabgabe CHF 100 bis 200 je nach Gemeinde, Bewilligungspflicht für Rassentypen mit erhöhtem Gefährdungspotenzial, Busse bis CHF 10 000.
- `data/gemeinden/sh/schaffhausen.json`: Stadt Schaffhausen mit drei lokalen Angaben: Leine in öffentlichen Anlagen (Polizeiverordnung Art. 30, Stand 2016), Hunde auf den Friedhöfen nur mit Bewilligung (Friedhofreglement Art. 20), Busse bis CHF 1000 (Polizeiverordnung Art. 59).

Einschränkung, wichtig für die nächste Prüfung:
- Die geltende Fassung von Hundegesetz (SHR 455.200) und Hundeverordnung (SHR 455.201) liess sich nicht abrufen: rechtsbuch.sh.ch liefert den Text nur per Skript. Gelesen wurden die Fassungen auf lexfind.ch (Gesetz Stand 2010, Verordnung von 2009). Jede Angabe, die nur aus diesen Fassungen stammt, nennt auf der Seite den Stand. Durch das aktuelle Merkblatt des Veterinäramts bestätigt sind: Haftpflichtnachweis, 10-Tage-Frist, AMICUS, Hundeabgabe, Leinenpflicht im Wald mit Daten, Kotaufnahme, Bewilligungspflicht. Der Rahmen CHF 100 bis 200 wird 2023 in einer Kleinen Anfrage im Grossen Stadtrat Schaffhausen genannt.
- Die Seiten «Haltung und Betreuung von Hunden» und «Bewilligungspflichtige Hunde» des Veterinäramts auf sh.ch liefern ebenfalls keinen lesbaren Text.

Weggelassen und warum:
- Zahl der bewilligungspflichtigen Rassentypen: Die Verordnung von 2009 nennt vier, das aktuelle Merkblatt vierzehn und weitere Züchtungen. Die Seite zählt nicht, sondern führt die im Merkblatt genannten Typen auf.
- Kantonsbeitrag an der Hundeabgabe (CHF 20 laut Verordnung von 2009): Stand unklar, für Halterinnen und Halter ohne Belang.
- Kurs: Das Gesetz verweist auf den Ausbildungsnachweis nach Bundesrecht. Ob das heute noch eine Pflicht bedeutet, steht in keiner abgerufenen Schaffhauser Quelle. Die Karte hat deshalb den Ton `note` und behauptet weder Pflicht noch «keine Pflicht».
- Hundeabgabe der Stadt Schaffhausen: Betrag in keiner abrufbaren amtlichen Quelle gefunden (Formular zur Rückerstattung und Verwaltungsbericht 2022 nicht abrufbar). Keine Karte Hundetaxe.

## Backlog

- Erledigt: Abschnitt 1, Schaffhausen (`sh`).
- Erledigt: Stadt Schaffhausen.
- Weitere Gemeinden für Abschnitt 3: Neuhausen am Rheinfall, Thayngen, Beringen, Stein am Rhein.
- Neue Lücken für Abschnitt 4:
  - SH: geltende Fassung von SHR 455.200 und 455.201 abrufen (rechtsbuch.sh.ch braucht einen Browser) und alle Angaben mit «Stand des Gesetzestexts: 2010» abgleichen, danach die Stand-Hinweise entfernen.
  - SH: Karte Kurs klären, sobald die Seite des Veterinäramts lesbar ist.
  - Stadt Schaffhausen: Betrag der Hundeabgabe und Anmeldestelle belegen.
