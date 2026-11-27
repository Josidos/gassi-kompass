# Parallel-Lauf gemeinden-vs-1 (28. November 2026)

## Protokoll

- Neu: Gemeinde Visp (VS), deutsche Originalfassung `data/gemeinden/vs/visp.json`, Übersetzungen französisch (Viège) und italienisch. Drei lokale Angaben: Hundesteuer CHF 195 (Steuergrundlagen 2025, Fälligkeit 31. März und CHF 175 bei teilweiser Befreiung laut Anzeige 2024), Anmeldung bei der Regionalpolizei Visp, Busse bis zum Dreifachen der Steuer. Neue Quellen: `vs_visp_steuern`, `vs_visp_vaz_hunde`.
- Weggelassen bei Visp: Leinenpflicht und Hundezonen. Die Seite der Regionalpolizei verlinkt einen Hundezonenplan, ein Pflichtenheft und das Reglement über die Erhebung der Hundesteuer, aber WebFetch lieferte unter diesen Adressen (`?action=get_file&id=100…` und `id=201…`) zweimal eine andere Ausgabe der visper allgemeinen zeitung statt des Dokuments. Das Polizeireglement liess sich ebenso nicht lesen.
- Neu: Gemeinde Naters (VS), deutsche Originalfassung `data/gemeinden/vs/naters.json`, Übersetzungen französisch und italienisch. Vier lokale Angaben: Hundesteuer CHF 125, Hundeverbot auf den Spielplätzen der Gemeinde, Nachweise auf der Gemeindekanzlei, Busse bis zum Dreifachen der Steuer. Neue Quellen: `vs_naters_hunde`, `vs_naters_spielplaetze`.
- Weggelassen bei Naters: Leinenpflicht. Das Polizeireglement vom 17.09.2014 ist auf der Seite «Infos+Download» verlinkt, WebFetch gab die Adresse aber nicht frei, und zwei Suchen fanden sie nicht als Treffer. Die Seite «Hundesteuer» der Kanzleidienste antwortete mit einem Fehler.

## Backlog

- Erledigt: Visp (VS), Naters (VS).
- Neue Lücke für `backlog/luecken.md`: Naters, Leinenpflicht aus dem Polizeireglement vom 17.09.2014 belegen (Seite «Infos+Download» der Gemeinde).
- Neue Lücke für `backlog/luecken.md`: Visp, Leinenpflicht und Hundezonen aus dem Hundezonenplan und dem Pflichtenheft der Regionalpolizei Visp belegen (im Browser lesen, WebFetch liefert falsche Dateien). Die Anzeige an die Hundebesitzer stammt von 2024, eine neuere Ausgabe (Januar 2025 oder 2026) wäre die bessere Quelle.
