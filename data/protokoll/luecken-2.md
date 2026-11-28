# Parallel-Lauf luecken-2: Kanton Tessin, Lücken (28. November 2026)

## Protokoll

### 1. Legge sui cani im geltenden Wortlaut

- Abgerufen: Raccolta delle leggi del Cantone Ticino, Legge sui cani (LCani, RL 482.300) del 19 febbraio 2008, «stato 15 maggio 2026», konsolidierte Fassung auf m3.ti.ch (`legge-piatta/num/479`). Das PDF «pdfatto/atto/479» auf m3.ti.ch ist eine alte Fassung (Änderungen nur bis 2014, Steuer CHF 50 bis 100, kein Art. 4a und 11a) und wurde nicht verwendet.
- Neue Quelle `ti_lcani_rl` (in `data/quellen/luecken-2.json`). Sie ersetzt `ti_lcani` (LexFind) in allen Feldern der drei Fassungen, die sich auf die LCani stützen: `wald`, `leine`, `verbot`, Karten Responsabilità civile, Corso, Imposta sui cani, A passeggio. `ti_lcani` ist damit unbenutzt (`build.py --check` meldet es als Hinweis) und kann beim Einsammeln aus `data/quellen/ti-it.json` entfernt werden.
- Verglichen und bestätigt: Art. 4 (Tassa für Hunde über 3 Monate, Comune fixiert CHF 75 bis 125 und erhebt sie), Art. 4a (CHF 25 an den Fondo per il soccorso degli animali, CHF 40 an den Staat), Art. 7 cpv. 2 bis 5 (Vorkehrungen gegen Flucht, Flucht sofort der Polizei melden, Leine an Orten mit Publikum oder anderen Tieren, Maulkorb wenn nötig, Hunde nach Art. 14 auf öffentlichen Flächen nur einzeln), Art. 11 (Municipi regeln die Hundehaltung mit Verordnung, können Aree di svago festlegen), Art. 11a (Grundkurs vor dem Erwerb, ausser Hundehaltung in den letzten 10 Jahren, Kosten zulasten der Teilnehmenden), Art. 21 cpv. 1 (Busse bis CHF 20 000). Die Leinenregel kennt keine Saison im Wald.
- Geändert (Karte Responsabilità civile, Art. 5 LCani: «Ogni proprietario di cani è tenuto a stipulare un'assicurazione contro la responsabilità civile, la cui copertura deve essere estesa anche al detentore occasionale.»):
  - alt: «Ogni detentore deve stipulare un'assicurazione di responsabilità civile per i danni causati dal cane, per un importo minimo di tre milioni di franchi.»
  - neu: «Ogni proprietario di cani deve stipulare un'assicurazione di responsabilità civile per i danni causati dal cane, estesa anche al detentore occasionale, per un importo minimo di tre milioni di franchi.»
  - Übersetzungen deutsch und französisch entsprechend nachgeführt, `original` auf `a49dde25a58d`.
- `geprueft` nicht geändert: Abgeglichen wurden nur die Angaben aus der LCani.

### 2. Datum der Kurspflicht

- LCani, Fussnote zu Art. 11a: «in vigore dal 1.9.2026 - BU 2025, 393 e BU 2026, 147». Ein 1. Juni 2026 kommt im Gesetzestext nicht vor.
- Seite des UVC «Corso teorico obbligatorio» (`ti_uvc_corso`): oben und unter «Sanzioni» «Dal 1° settembre 2026», in den historischen Hinweisen noch «Queste basi legali entreranno in vigore il 1° giugno 2026». Der neuere Rechtstext (BU 2026, 147) nennt den 1. September 2026.
- Ergebnis: Die Angabe «Dal 1° settembre 2026» in der Karte Corso stimmt, keine Änderung.

### 3. Feld `vermisst` ergänzt

- Quelle `ti_lcani_rl` (Stand 15. Mai 2026), Wortlaut: Art. 7 cpv. 3 «La fuga di un cane deve essere immediatamente segnalata agli organi di polizia.» Art. 3 cpv. 3 «Se né il proprietario né il detentore sono reperibili, i cani sono consegnati ad una società per la protezione degli animali riconosciuta o ad altri enti con competenze analoghe per un collocamento a spese del Cantone in base alla legislazione cantonale sulla protezione degli animali. In caso di successiva reperibilità del proprietario o del detentore, le spese sono poste a carico del proprietario o, in via subordinata, del detentore.»
- Neu: zwei Punkte zuoberst in `vermisst.punkte` (Flucht sofort der Polizei melden; Übergabe an einen anerkannten Tierschutzverein auf Kosten des Kantons, Kosten später zulasten des Eigentümers, ersatzweise des Halters). `ti_lcani_rl` in `vermisst.quellen` ergänzt. Übersetzungen nachgeführt, `original` auf `66501b82f773`.

### 4. Jagd- und Waldrecht auf Leinenpflicht (zwei Suchanläufe)

- Gefunden: Regolamento sulla caccia e la protezione dei mammiferi e degli uccelli (RL 922.110) del 11 luglio 2006, PDF des Ufficio della caccia e della pesca auf www4.ti.ch («Regolamento_venatorio_2025.pdf», Stand laut Abruf 27. Juni 2025). Laut Abruf: Art. 36 Leinenpflicht in den Bandite (Jagdbanngebiete) ausser mit Sonderbewilligung, Art. 37 cpv. 1 «Durante tutto l'anno non si possono lasciare vagare cani di qualsiasi specie», Art. 37 cpv. 2 unbeaufsichtigte Hunde, die Wild hetzen, dürfen abgeschossen werden, Anhang 1 Bussen CHF 150 (Leine in den Bandite) und CHF 100 (Hunde unbeaufsichtigt laufen lassen). Eine allgemeine Leinenpflicht im Wald enthält das Reglement laut Abruf nicht.
- Nicht übernommen: Der vollständige Wortlaut von Art. 36 und 37 liegt nicht wörtlich vor, und ob das PDF von 2025 die geltende Fassung ist, liess sich in der Raccolta delle leggi nicht bestätigen (zweiter Suchanlauf fand den Erlass dort nicht). Waldrecht: nicht gesucht, Suchanläufe aufgebraucht.

## Backlog

- Kanton Tessin, LCani im geltenden Wortlaut gegenprüfen (Art. 4, 4a, 7, 11a): geschlossen. Quelle `ti_lcani_rl`, Stand 15. Mai 2026.
- Kanton Tessin, Datum der Kurspflicht: geschlossen, 1. September 2026 (LCani Fussnote zu Art. 11a, BU 2026, 147). Hinweis an das UVC wäre möglich: Die Seite nennt in den historischen Hinweisen noch den 1. Juni 2026.
- Quelle `ti_lcani` (LexFind) ist unbenutzt und kann aus `data/quellen/ti-it.json` entfernt werden.
- Kanton Tessin, Abschnitt «Hund vermisst oder gefunden» (LCani Art. 7 Abs. 3, Art. 3 Abs. 3): geschlossen, Quelle `ti_lcani_rl`.
- Tessiner Jagd- und Waldrecht auf Leinenpflicht: teilweise. Jagdrecht: Regolamento venatorio (RL 922.110) Art. 36 und 37 sind ein Kandidat für `leine` (Leine in den Bandite, Hunde nie unbeaufsichtigt laufen lassen). Nächster Schritt: geltende Fassung in der Raccolta delle leggi finden und Art. 36 und 37 wörtlich lesen. Waldrecht (Legge cantonale sulle foreste): offen.
- Lugano (Hundezonen, Barbengo): nicht Teil dieses Auftrags, offen.
