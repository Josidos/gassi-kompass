# Parallel-Lauf ai (Staffel E), 2026-11-17

## Protokoll

**Neu:** Kanton Appenzell Innerrhoden (`data/kantone/ai.json`), 6 Quellen in `data/quellen/ai.json`. Alle Quellen am 17. November 2026 abgerufen.

- Hundegesetz (GS 560.100, Stand 1. Januar 2011): Haftpflicht ohne Mindestsumme (Art. 17), Leinenzwang und Betretungsverbot (Art. 6), Kot (Art. 7), Massnahmen und Zuzug (Art. 10), Meldepflicht (Art. 12).
- Verordnung zum Hundegesetz (GS 560.110, Stand 1. Januar 2025): Hundesteuer kantonal einheitlich CHF 80, Hofhund CHF 50, weiterer Hund im Haushalt CHF 160, Zuchten und Tierheime CHF 600 (Art. 1), Befreiungen (Art. 3), Meldungen an den Bezirk (Art. 6, 8a).
- Verordnung zum Alpgesetz (GS 916.510, Stand 1. Dezember 2014), Art. 5: Leine während der Alpzeit, ausgenommen Hunde der Bewirtschafter.
- Verordnung zum Jagdgesetz (GS 922.010, Stand 1. Januar 2025), Art. 41: wildernde Hunde. Keine Leinenpflicht im Wald.
- Verordnung über die Ordnungsbussen (GS 311.010, Stand 1. August 2023), Anhang 1 Ziff. 6: CHF 50 für Leinenzwang oder Betretungsverbot, CHF 100 für nicht beseitigten Kot.
- Seite «Hundehalterausbildung» des Kantons: keine Kurspflicht seit 1. Januar 2017, Anordnung im Einzelfall.

**Entscheide:**

- `wald.saison` ist `false`: Die drei gelesenen Erlasse nennen keine Leinenzeit im Wald. Der Text nennt genau diese Erlasse und die Leinenpflicht während der Alpzeit.
- Kurs: Die Seite des Kantons nennt das Veterinäramt als anordnende Stelle, das Hundegesetz (Art. 10) den Bezirk. Beides steht mit Quelle im Text.
- Art. 12 HuG («bei der nächsten Hundelösung melden») ist nicht als Frist übernommen, die Verordnung von 2025 regelt die Meldung ohne diesen Zusatz.

**Weggelassen:**

- Die Seite «Leinenpflicht in beiden Appenzell» des Veterinäramts (ar.ch) war zweimal nicht abrufbar (client_error). Nichts daraus verwendet.
- Jagdgesetz (GS 922.000) und Vorschriften zu Wildruhe- und Naturschutzgebieten: Text nicht abrufbar (ai.clex.ch liefert WebFetch nur eine leere Hülle, auf lexfind.ch nicht gefunden). Keine Angabe daraus.
- Daten der Alpzeit und genaue Liste der Alpen: Die Alpverordnung nennt keine Daten. Der Geltungsbereich (Art. 1) ist nur als «Alpen, für die das Alpgesetz gilt» wiedergegeben.
- Polizeimeldung «Alpstein: polizeiliche Kontrollen» (ai.ch) erwähnt eine Leinenpflicht im Alpstein ohne Rechtsgrundlage und Datum. Nicht verwendet.

**Nicht gelungen:** Bezirk Appenzell (BFS 3101) als Gemeinde, siehe Backlog.

## Backlog

- Abschnitt 1: Appenzell Innerrhoden (`ai`) erledigt.
- Zurückgestellt (2026-11-17): Bezirk Appenzell. Die Seite «Hundekontrolle / Vollzug HuG» des Bezirks (appenzell.org, dienst_id=23575) nennt nur die kantonalen Steuerbeträge und die Meldestelle (Bezirksverwaltung, Kronengarten 8). Eigene Leinenzonen, hundefreie Zonen oder Bussen des Bezirks waren nach zwei Suchen nicht zu finden. Das sind weniger als drei lokale Angaben.
- Weitere Gemeinden für Abschnitt 3: Schwende-Rüte, Oberegg, Gonten, Schlatt-Haslen. Hinweis: Die Hundesteuer ist kantonal festgelegt, lokale Angaben gibt es nur, wenn ein Bezirk Leinenzonen oder hundefreie Zonen nach Art. 6 HuG angeordnet hat.
- Neue Lücken für Abschnitt 4:
  - `ai`: Jagdgesetz (GS 922.000) und Wildruhegebiete auf Regeln für Hunde prüfen. Danach den Wald-Text anpassen.
  - `ai`: Seite «Leinenpflicht in beiden Appenzell» (ar.ch, Veterinäramt) abrufen und mit `leine` abgleichen.
  - `ai`: Daten der Alpzeit und betroffene Alpen (Alpgesetz, Art. 1 der Verordnung) belegen.
