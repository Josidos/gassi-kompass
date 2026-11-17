# Parallel-Lauf ge-fr (2026-11-18, Staffel B)

## Protokoll

- Neu: Kanton Genf französisch (`data/fr-ch/kantone/ge.json`), elf Quellen in `data/quellen/ge-fr.json`. Alle Quellen in diesem Lauf abgerufen. Geprüft über eine vorübergehende Kopie unter `data/kantone/` und `data/gemeinden/ge/`, Build und Test fehlerfrei.
- `geprueft` steht auf 2026-11-17, wie bei `vd-fr` (der Build lehnt das Datum 2026-11-18 kurz nach Mitternacht ab).
- Belegt: Leinenpflicht im Wald 1. April bis 15. Juli (RChiens Art. 14 Bst. f, Seite des Kantons), Leinenpflicht in Ortschaften, Parks, Flughafen, Campings (Art. 14), Verbotsorte (Art. 13 Abs. 1), Haftpflicht für alle ohne Mindestsumme (LChiens Art. 16 Abs. 3), keine Kurspflicht, TMC für Hunde über 25 kg und 56 cm (LChiens Art. 22 und 27, Seite des Kantons), Eintrag in AMICUS innert 10 Tagen (LChiens Art. 17 Abs. 2, RChiens Art. 23), Kontrollmarke ab 6 Monaten bis 1. April (RChiens Art. 9), Kantonssteuer CHF 50 / 70 / 100 plus Gemeindezuschlag, CHF 1 Versicherung und CHF 4 Tierseuchenfonds, 15 verbotene Rassen samt Kreuzungen (LChiens Art. 23, RChiens Art. 17 Abs. 2), Kot aufnehmen (LChiens Art. 21 Abs. 2), Bewilligung ab mehr als drei anvertrauten Hunden (Art. 18 Abs. 3).
- Karte Kurs mit `ton: note`: keine allgemeine Kurspflicht, Test nur für grosse Hunde. Karte Rassen mit `ton: must`: Liste mit Verbot.
- Unsicherheit: Gesetz und Reglement wurden über eine Zusammenfassung des Abrufwerkzeugs mit Zitaten gelesen, nicht Artikel für Artikel im Volltext. Bei RChiens Art. 14 kamen nur die Buchstaben a, b, c, f und g zurück. Die Buchstaben d und e (vermutlich Moulin-de-Vert und Vogelreservat) stammen deshalb von der Seite des Kantons (Stand 2023). SILGeneve nennt für beide Erlasse eine Änderung oder Berichtigung vom 17. November 2026 (bei der LChiens zu Art. 3 Abs. 1). Was genau sich geändert hat, ist nicht geprüft. Die Seiten des Kantons zu Hunden sind von 2023, der Stand steht in den Karten Kurs und Annonce.
- Weggelassen: Mindestsumme der Haftpflicht (in keiner Quelle), Bussenbeträge (weder Gesetz noch Reglement nennen welche), Leinenverbot an Ufern und im Wasser von Oktober bis März (Art. 13 Bst. l, Geltungsbereich im Abruf abgeschnitten), Gemeindezuschläge zur Hundesteuer je Gemeinde (eigene Seite ge.ch/node/110, nicht abgerufen), Chip-Frist für Welpen, Regeln für Besuch mit Listenhunden (nicht gefunden).
- Neu: Ville de Genève französisch (`data/fr-ch/gemeinden/ge/geneve.json`, BFS 6621), vier Karten (Laisse, Accès interdit mit 12 namentlich genannten Parks, Annonce bei der Police municipale, Amendes ohne Beträge) und zwei Gruppen von Freilaufzonen mit Namen, zwei weitere Quellen der Stadt. Der Parc Liotard steht auf der Seite der Stadt sowohl bei den eingezäunten Freilaufzonen als auch bei den verbotenen Parks, die Karte sagt das so. Der Parc Geisendorf ist seit 1. Juni 2026 geschlossen und nicht als Zone aufgeführt.
- Weggelassen bei Genf: Hundesteuer der Stadt (Zuschlag nicht abgerufen), Bussenbeträge (nicht veröffentlicht).
- Nicht gelungen: nichts.

## Backlog

- Erledigt: Genf (`ge`), französisch, Abschnitt 2, Daten unter `data/fr-ch/`. Ville de Genève. Die Seiten entstehen erst nach dem Sonderlauf Mehrsprachigkeit.
- Weitere Gemeinden für Abschnitt 3: Vernier, Lancy, Meyrin, Carouge, Onex.
- Neue Lücken für Abschnitt 4: LChiens und RChiens im Volltext gegenprüfen, besonders RChiens Art. 13 Bst. l (Ufer, Oktober bis März) und Art. 14 Bst. d und e sowie die Änderungen vom 17. November 2026. Gemeindezuschläge zur Hundesteuer (ge.ch/node/110), auch für die Stadt Genf. Bussenbeträge (Ordnungsbussen des Kantons). PDF «Liste des races de chiens considérées comme potentiellement dangereuses» mit RChiens Art. 17 abgleichen.
