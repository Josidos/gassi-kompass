# Parallel-Lauf luecken-1 (28. November 2026)

## Protokoll

- Riehen (BS), Orte mit Hundeverbot und Leinenpflicht: geschlossen. Quelle `bs_zonen` (Liste «Hundeverbots- und Leinenpflichtzonen» des Gesundheitsdepartements, ohne Datum) am 28.11.2026 über die Seite «Hundehaltende» des Veterinäramts abgerufen, Riehen vollständig lesbar. Neu: Karte «Kein Zutritt» mit elf Orten mit Hundeverbot (mit den Ausnahmen an der Leine im Wenkenhofpark und in der Wettsteinanlage). Geändert: Karte «Leine», Wert alt «Wald und Lange Erlen: 1. April bis 31. Juli», neu «… dazu sieben Orte», Text um die sieben Orte mit Leinenpflicht ergänzt, Quelle `bs_zonen` dazu. Übersetzungen fr und it nachgeführt.
- Hinweis: Die Liste des Kantons führt den Eisweiher unter Hundeverbot, die Seite der Gemeinde (`bs_riehen_schutz`) nennt dort ein Wegegebot. Beides steht so auf der Seite, je mit seiner Quelle. Beim nächsten Nachprüfen klären.
- Riehen, Reglement Wildtierschutz und Hundeplan Landschaftspark Wiese: offen. Die Seite der Gemeinde «Schutzmassnahmen für Flora und Fauna» verlinkt das Reglement in der Gesetzessammlung (change_documents/1559). WebFetch liess die Adresse nicht zu, eine Suche in gesetzessammlung.bs.ch fand das Reglement nicht (zwei Suchanläufe). Bussen nennt die Seite der Gemeinde nicht. Der Hundeplan liegt nur auf landschaftsparkwiese.info (keine amtliche Quelle).

- Stadt Genf, Zuschlag der Gemeinde zur Hundesteuer: geschlossen. Quelle `ge_impot_centimes`: Seite ge.ch (publiziert 17. März 2025) und das verlinkte PDF «télécharger» am 28.11.2026 abgerufen. Kopfzeile «COMMUNES 2021 2022 2023 2024 2025», Zeile GENEVE-VILLE: 100 in allen fünf Jahren. Neu in `data/fr-ch/gemeinden/ge/geneve.json`: Karte «Impôt sur les chiens» (100 centimes additionnels, für einen ersten Hund CHF 50 mehr; Kantonsbetrag CHF 50 steht in der Kantonsdatei und auf der Seite von ge.ch). Die Datei hatte vorher keine Karte zur Hundesteuer. Übersetzungen de und it nachgeführt.
- Kanton Genf: nicht geändert. Die Karte «Impôt sur les chiens» in `data/fr-ch/kantone/ge.json` sagt schon, dass die Gemeinden centimes additionnels in Prozent der kantonalen Steuer erheben, und verweist auf die Liste der Steuerverwaltung. Vollständige Zeilen im PDF (Werte 2021 bis 2025) zum Beispiel: Carouge 100, Lancy 50, Vernier 50, Onex 100, Thônex 100, Versoix 100. Meyrin hat nur vier Werte.

## Backlog

- [x] Riehen: Orte mit Hundeverbot und mit Leinenpflicht (`bs_zonen`), erledigt 28.11.2026 (luecken-1).
- [ ] Riehen: Reglement Wildtierschutz Riehen bleibt offen. Neu bekannt: Die Gemeinde verlinkt es unter gesetzessammlung.bs.ch/app/de/change_documents/1559 (für WebFetch nicht freigegeben). In einer Sitzung im Browser lesen oder über die Schnittstelle der Sammlung, falls der Wächter es führt.
- [x] Kanton Genf: Zuschlagsrappen der Gemeinden, erledigt 28.11.2026 (luecken-1): Stadt Genf ergänzt, Kantonskarte nennt den Zuschlag schon.
- [ ] Riehen: Eisweiher klären (Liste des Kantons: Hundeverbot, Seite der Gemeinde: Wegegebot).
