# Parallel-Lauf ne-fr (2026-11-18, Staffel A)

## Protokoll

- Neu: Kanton Neuenburg französisch (`data/fr-ch/kantone/ne.json`), sieben Quellen in `data/quellen/ne-fr.json`. Alle Quellen in diesem Lauf abgerufen. Geprüft über eine vorübergehende Kopie unter `data/kantone/`, Build und Test fehlerfrei.
- `geprueft` steht auf 2026-11-17, wie bei `vd-fr` (der Lauf lief kurz nach Mitternacht Schweizer Zeit).
- Belegt: Leinenpflicht im Wald 15. April bis 30. Juni (LFS Art. 21 Abs. 4, Faltblatt 2024), Beherrschen durch Stimme oder Geste, sonst Leine (LChiens Art. 12, LFS Art. 21 Abs. 3), Hundetaxe höchstens CHF 120 samt CHF 30 Staatsanteil (LChiens Art. 3 und 7), Befreiungen (Art. 4, RELChiens Art. 3), Busse bis zum Doppelten der hinterzogenen Taxe (Art. 8), Kurspflicht für neue Halter (LChiens Art. 19 Abs. 2, Einzelheiten von der Seite des SCAV: 2 Stunden Theorie, 8 Lektionen zu 45 Minuten, Beginn innert 6 Monaten), Massnahmen im Einzelfall (Art. 17), Kot (Art. 14), Busse bis CHF 40 000 nach LFS Art. 72.
- Karte Kurs mit `ton: must`: Die Pflicht gilt für alle, die erstmals einen Hund halten. Karten Haftpflicht und Rassen mit `ton: none`: Die LChiens enthält laut gezielter Abfrage weder die Wörter «assurance» und «responsabilité civile» noch eine Rasseliste.
- Unsicherheit: Die Gesetzestexte wurden über WebFetch gelesen, das lange Artikel nur in Stücken oder zusammengefasst wiedergibt. Art. 4, 5, 7, 8, 14 und 17 LChiens liegen nur als Zusammenfassung vor. Die Quelle `ne_scav` ist eine Adresse auf ne.ch, die auf eine Sammelseite des SCAV führt, nicht auf das Kursreglement selbst. Das Kursreglement des Staatsrats wurde nicht gefunden.
- Weggelassen: Meldefrist (weder LChiens noch SCAV nennen eine, die Frist des Bundesrechts wurde nicht abgerufen), Mindestsumme einer Haftpflicht, Kurspreis (nur Schätzung des SCAV), Höhe der Busse nach LChiens (Art. 20 nennt keinen Betrag), Regeln für Weiden und Waldrand (stehen in keiner Quelle), Feld `umzug`.
- Neu: Ville de Neuchâtel französisch (`data/fr-ch/gemeinden/ne/neuchatel.json`), vier Karten (Laisse, Accès interdit, Annonce, Amendes), zwei Quellen. Das Faltblatt «Mon chien en ville» trägt kein Datum, der Dateiname nennt 2022, das steht als Stand im Text. Das Polizeireglement wurde in einer Fassung mit Änderungen bis 2015 gelesen.
- Weggelassen bei Neuchâtel: Betrag der Hundetaxe (das Reglement vom 17. November 2025 verweist nur auf das kantonale Gesetz, das Faltblatt nennt keinen Betrag), Namen der Freilaufzonen (nur auf einem Plan, Zuordnung unklar), Meldefrist.
- Nicht gelungen: nichts.

## Backlog

- Erledigt: Neuenburg (`ne`), französisch, Abschnitt 2, Daten unter `data/fr-ch/`. Ville de Neuchâtel. Die Seiten entstehen erst nach dem Sonderlauf Mehrsprachigkeit.
- Weitere Gemeinden für Abschnitt 3: La Chaux-de-Fonds, Le Locle, Val-de-Ruz, Val-de-Travers, Milvignes.
- Neue Lücken für Abschnitt 4: Wortlaut der LChiens (Art. 4, 5, 7, 8, 14, 17) und der LFS am PDF gegenprüfen. Kursreglement des Staatsrats und eigene Seite des SCAV zu Hunden suchen. Neuchâtel: Betrag der Hundetaxe, Namen der Freilaufzonen, geltende Fassung des Polizeireglements und Liste der Strände im Faltblatt gegenprüfen.
