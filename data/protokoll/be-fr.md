# Parallel-Lauf be-fr (2026-11-18, Staffel C)

## Protokoll

- Der Lauf startete zuerst ohne Zusatznachricht und endete. Die Nachricht traf danach ein, die Arbeit begann um 00:25 Uhr, Schluss war 00:45 Uhr. Deshalb nur die Kantonsdatei.
- Neu: Kanton Bern französisch (`data/fr-ch/kantone/be.json`), zwei Quellen in `data/quellen/be-fr.json`, beide in diesem Lauf abgerufen. Die deutsche Datei `data/kantone/be.json` ist unverändert. Geprüft über eine vorübergehende Kopie unter `data/kantone/`.
- `geprueft` steht auf 2026-11-17 wie bei `vd-fr` und `ne-fr`.
- Belegt aus der französischen Broschüre des Veterinärdienstes (Juli 2022): Haftpflicht CHF 3 Mio., Orte mit Leinenpflicht, höchstens drei Hunde über vier Monate, Aufsicht, Kot, AMICUS, keine Rasseliste, kein Kursobligatorium. Aus der Änderung der OCE vom 17. Mai 2017 (Art. 13, 13a): Wohngemeinde als Registrierstelle, Hundetaxe wird von den Gemeinden erhoben.
- Unsicherheit: WebFetch gab die Broschüre nur zusammengefasst wieder, nicht im Wortlaut. Die OCE wurde nur als Änderungserlass von 2017 gelesen, nicht in der geltenden Fassung.
- Weggelassen: der Entscheid des Grossen Rates von 2023 zur Leinenpflicht im Wald (keine französische Quelle abgerufen), Befreiungen von der Hundetaxe (die französische Fassung der Loi sur les chiens, RSB 916.31, liess sich nicht abrufen: be.lexwork.naz.ch/fr wurde von WebFetch abgelehnt), Bussenbeträge (gefunden nur in der OCAO mit Stand 1. Januar 2018, lexfind.ch/tolv/119581/fr: Leine CHF 100, Kot CHF 150, zu alt für eine Angabe), Feld `umzug`.
- Nicht gelungen: Biel/Bienne französisch. Zwei Suchen auf biel-bienne.ch brachten nur Budgets und Rechnungen, keine Seite zu Hunden. Keine Datei angelegt.

## Backlog

- Erledigt: Bern (`be`), französische Fassung, Abschnitt 2, Daten unter `data/fr-ch/`. Die Seite entsteht erst nach dem Sonderlauf Mehrsprachigkeit.
- Zurückgestellt (2026-11-18): Biel/Bienne französisch, keine amtliche Quelle gefunden, Schluss-Zeit erreicht.
- Weitere Gemeinden für Abschnitt 3 (französisch): Biel/Bienne, Moutier ist nicht mehr bernisch, daher Saint-Imier, Tramelan, La Neuveville, Valbirse.
- Neue Lücken für Abschnitt 4: Loi sur les chiens (RSB 916.31) französisch im Wortlaut lesen und `be.json` (fr) daran gegenprüfen, vor allem Befreiungen von der Taxe, Zutrittsverbote der Gemeinden und Bussen. Geltende Fassung der OCAO für die Bussenbeträge. Französische amtliche Quelle zur Leinenpflicht im Wald.
