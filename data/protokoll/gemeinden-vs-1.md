# Parallel-Lauf gemeinden-vs-1 (28. November 2026)

## Protokoll

- Neu: Gemeinde Visp (VS), deutsche Originalfassung `data/gemeinden/vs/visp.json`, Übersetzungen französisch (Viège) und italienisch. Drei lokale Angaben: Hundesteuer CHF 195 (Steuergrundlagen 2025, Fälligkeit 31. März und CHF 175 bei teilweiser Befreiung laut Anzeige 2024), Anmeldung bei der Regionalpolizei Visp, Busse bis zum Dreifachen der Steuer. Neue Quellen: `vs_visp_steuern`, `vs_visp_vaz_hunde`.
- Weggelassen bei Visp: Leinenpflicht und Hundezonen. Die Seite der Regionalpolizei verlinkt einen Hundezonenplan, ein Pflichtenheft und das Reglement über die Erhebung der Hundesteuer, aber WebFetch lieferte unter diesen Adressen (`?action=get_file&id=100…` und `id=201…`) zweimal eine andere Ausgabe der visper allgemeinen zeitung statt des Dokuments. Das Polizeireglement liess sich ebenso nicht lesen.

## Backlog

- Erledigt: Visp (VS).
- Neue Lücke für `backlog/luecken.md`: Visp, Leinenpflicht und Hundezonen aus dem Hundezonenplan und dem Pflichtenheft der Regionalpolizei Visp belegen (im Browser lesen, WebFetch liefert falsche Dateien). Die Anzeige an die Hundebesitzer stammt von 2024, eine neuere Ausgabe (Januar 2025 oder 2026) wäre die bessere Quelle.
