# Parallel-Lauf zg (Staffel B), 2026-11-17/18

## Protokoll

- Neu: `data/kantone/zg.json` (Kanton Zug) mit sieben Quellen in `data/quellen/zg.json`.
- Belegt: Leinenpflicht im Wald und am Waldrand vom 1. April bis 31. Juli (Seite «Freizeit und Erholung im Wald» und Medienmitteilung vom 27. März 2025, Grundlage Einführungsgesetz zum Waldgesetz, in Kraft seit 1. Januar 2025). Eine Meterangabe zum Waldrand nennt keine der Quellen, deshalb steht keine auf der Seite.
- Der Kanton Zug hat laut Veterinärdienst kein eigenes Hunderecht: «Für das Halten von Hunden ist die eidg. Tierschutzverordnung und die Gesetze und Reglemente der Zuger Gemeinden massgebend.» Die Karten Haftpflicht, Kurs und Rassen sagen deshalb nur das (Ton `note`) und verweisen auf das Reglement der Gemeinde. Sie behaupten nicht «keine Pflicht».
- Die Leinen-Orte ausserhalb des Waldes sind auf der Seite des Kantons Empfehlungen und als solche gekennzeichnet. Die Orte ohne Hunde stehen mit Einleitung, dass die Regeln der Gemeinde verbindlich sind.
- Hundesteuer: kantonal nur belegt, dass die Hundedaten für die Erhebung der Hundesteuer dienen (VV Tierseuchengesetz § 18a). Als Beispiel Steinhausen CHF 70 (Merkblatt 2025), ausdrücklich als Beispiel.
- Quelle `zg_vorfaelle`: abgerufen wurde die Adresse unter `/it/…`, der Inhalt ist derselbe deutsche Text. Die deutsche Adresse liess sich im Lauf nicht direkt abrufen.
- Weggelassen: Paragraf des Einführungsgesetzes zum Waldgesetz, Bussenhöhe, Kotaufnahmepflicht (kantonal nicht belegt).
- Nicht gelungen: Das «Infoblatt Hundereglemente der Gemeinden im Kanton Zug» des Veterinärdienstes (cdn.zg.ch, Ausgaben März 2025 und Oktober 2026) war nicht abrufbar (Abruf nicht freigegeben, publiclogin2.zg.ch verlangt Cookies).
- Nicht gelungen: Stadt Zug. Die Seiten von stadtzug.ch (Dienstleistungen 1727 und 1965) und der Stadtratsbeschluss Nr. 20.19 vom 15. Januar 2019 zur Leinenpflicht (lesesaal.stadtzug.ch) lieferten Fehler. Keine einzige lokale Angabe belegt, keine Datei angelegt.

## Backlog

- Abschnitt 1: Kanton Zug erledigt (`data/kantone/zg.json`).
- Zurückgestellt (2026-11-18): Stadt Zug (BFS 1711). Grund: stadtzug.ch und lesesaal.stadtzug.ch im Lauf nicht abrufbar, null belegte lokale Angaben.
- Abschnitt 3, weitere Gemeinden: Zug (1711, zweiter Anlauf), Baar (1701), Cham (1702), Risch (1707, Hundereglement unter zg.ch/behoerden/gemeinden/risch-rotkreuz/…/101-hundereglement), Steinhausen (1708, Reglement über das Halten von Hunden und Merkblatt Hundesteuer 2025 auf zg.ch).
- Abschnitt 4, Lücken ZG: Infoblatt Hundereglemente der Gemeinden (Veterinärdienst) auswerten. Damit die Karten Haftpflicht, Kurs, Rassen und Hundesteuer schärfen (heute nur Verweis auf die Gemeinde). Paragraf und Busse der Leinenpflicht im Einführungsgesetz zum Waldgesetz (BGS) nachtragen. Meterangabe zum Waldrand, falls das Gesetz eine nennt.
