# Parallel-Lauf `gl` (Staffel C), 18. November 2026

## Protokoll

Neu:
- `data/kantone/gl.json`: Kanton Glarus, alle Felder belegt. Fünf Quellen in `data/quellen/gl.json`.
- Wald: Leinenpflicht ganzjährig im Wald und den Waldrändern entlang (Jagdverordnung Art. 30 Abs. 1, Stand 1. Januar 2026). Keine Saison, deshalb `saison: false`.
- Versicherungspflicht mit Kopie der Police ans Einwohneramt innert eines Monats (Veterinärverordnung Art. 28), kantonale Hundetaxe CHF 55 plus Gemeindezuschlag (Art. 31), Bewilligungspflicht für 10 Rassen und Mischlinge (Art. 19 bis 25, Stand 1. Januar 2024, Hovawart und Rhodesian Ridgeback sind seit 2024 gestrichen), Leinenpflicht in den eidgenössischen Jagdbanngebieten (Vollzugsregelung von 2015, mit Stand genannt).
- Leinenpflicht in Gebäuden, an stark befahrenen Strassen, im öffentlichen Verkehr, auf Pausen-, Spiel- und Sportplätzen und an signalisierten Orten: Die Seite der Gemeinde Glarus führt diese Liste unter dem Titel des kantonalen Tierschutz- und Tierseuchengesetzes. Beim Kanton mit dieser Quelle aufgenommen, am Gesetzestext noch nicht abgeglichen.
- `data/gemeinden/gl/glarus.json`: Gemeinde Glarus mit drei lokalen Angaben: Hundetaxe CHF 190 (CHF 135 Gemeinde, CHF 55 Kanton, seit 1. Januar 2019), Anmeldestelle Einwohnerdienste mit Fristen, Kotaufnahme auf dem ganzen Gemeindegebiet. Dazu eine Karte Leine, die das kantonale Recht wiedergibt und nicht als lokale Angabe zählt.

Einschränkung, wichtig für die nächste Prüfung:
- Das Einführungsgesetz zum Tierschutzgesetz und zum Tierseuchengesetz (GS IV G/3/2) liess sich in zwei Versuchen nicht abrufen: gesetze.gl.ch liefert den Text nur per Skript, auf lexfind.ch nicht gefunden. Alle Angaben stammen aus der Veterinärverordnung, der Jagdverordnung, der Seite der Fachstelle Hundewesen und der Seite der Gemeinde Glarus.
- Das Merkblatt zur bewilligungspflichtigen Hundehaltung (gr.ch) war nicht abrufbar (Fehler des Servers). Die Rasseliste steht übereinstimmend in der Veterinärverordnung und auf der Seite Hundewesen.

Weggelassen und warum:
- Deckungssumme der Haftpflicht, Bussenbeträge, Kotaufnahmepflicht auf Kantonsebene: in keiner abgerufenen kantonalen Quelle.
- Orte mit Hundeverbot: Die gelesenen Verordnungen nennen keine. Der Abschnitt «Verbot» sagt das und nennt die zwei belegten Verbote (Haltung ohne Bewilligung, frei laufen lassen im Wald).
- Karte Kurs hat den Ton `note`: Die Nachweispflicht gilt für Ersthundehalter und für Hunde der Rasseliste, nicht allgemein.
- AMICUS-Frist von 10 Tagen: steht nur auf der Seite der Gemeinde Glarus, deshalb dort.

## Backlog

- Erledigt: Abschnitt 1, Glarus (`gl`).
- Erledigt: Gemeinde Glarus.
- Weitere Gemeinden für Abschnitt 3: Glarus Nord, Glarus Süd (der Kanton hat nur drei Gemeinden).
- Neue Lücken für Abschnitt 4:
  - GL: Einführungsgesetz GS IV G/3/2 abrufen (gesetze.gl.ch braucht einen Browser) und daraus Leinenpflicht im öffentlichen Raum (Art. 31), Deckungssumme, Kotaufnahme und Bussen ergänzen. Danach Karte Kurs und `ton` prüfen.
  - Gemeinde Glarus: lokale Leinen- oder Verbotsorte und Bussen belegen (Polizeireglement nicht gefunden).
  - GL: Merkblatt bewilligungspflichtige Hundehaltung erneut abrufen.
