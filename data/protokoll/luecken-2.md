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

## Backlog

- Kanton Tessin, LCani im geltenden Wortlaut gegenprüfen (Art. 4, 4a, 7, 11a): geschlossen. Quelle `ti_lcani_rl`, Stand 15. Mai 2026.
- Kanton Tessin, Datum der Kurspflicht: geschlossen, 1. September 2026 (LCani Fussnote zu Art. 11a, BU 2026, 147). Hinweis an das UVC wäre möglich: Die Seite nennt in den historischen Hinweisen noch den 1. Juni 2026.
- Quelle `ti_lcani` (LexFind) ist unbenutzt und kann aus `data/quellen/ti-it.json` entfernt werden.
- Kanton Tessin, Abschnitt «Hund vermisst oder gefunden» (LCani Art. 7 Abs. 3, Art. 3 Abs. 3): offen, folgt im nächsten Schritt.
- Tessiner Jagd- und Waldrecht auf Leinenpflicht: offen.
- Lugano (Hundezonen, Barbengo): nicht Teil dieses Auftrags, offen.
