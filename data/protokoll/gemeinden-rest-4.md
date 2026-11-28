# Parallel-Lauf gemeinden-rest-4 (28. November 2026, 03:40 bis 04:50 Uhr)

## Protokoll

### Engelberg (OW), neu

- Neu: `data/gemeinden/ow/engelberg.json` (BFS 1402) mit drei lokalen Angaben: Leine in dicht bewohnten Gebieten und kein unbeaufsichtigtes Freilaufen, Hundekot aufnehmen (Busse möglich, ohne Betrag), Hundesteuer mit Rechnung Mitte Jahr anhand der AMICUS-Daten. Übersetzungen fr und it.
- Quelle: `ow_engelberg_hundewesen`, Seite «Hundewesen» der Gemeinde (Finanzverwaltung), abgerufen am 28.11.2026, ohne Datum auf der Seite. Alle Sätze mit wörtlichen Zitaten aus WebFetch abgeglichen.
- Weggelassen: Betrag der Hundesteuer, Zeitraum der Leinenpflicht im Wald, Verbotsorte und Bussenbetrag. Sie stehen im «Reglement über die Hundehaltung und die Hundesteuer» (https://www.gde-engelberg.ch/_doc/968078) und im «Hundesteuer Tarif» (https://www.gde-engelberg.ch/_doc/968079). Beide Adressen und die Publikationsseite (https://www.gde-engelberg.ch/reglemente/16046) lehnte WebFetch ab, weil sie in keinem Suchtreffer erschienen. Vier Suchen mit WebSearch fanden sie nicht. Darum kein `hinweis_heute`.
- Nicht gelungen: Reglement und Tarif lesen (siehe oben).

### Kerns (OW), zurückgestellt

- Keine Datei. Belegt sind nur Angaben zur Hundesteuer und zur Anmeldung, beide aus der Seite «Hundesteuer/Hundekontrolle» (https://www.kerns.ch/dienstleistungen/14199): Anmeldung bei der Finanzverwaltung und in AMICUS, reduzierter Tarif für Landwirtschaftshunde, Steuerpflicht ab 6 Monaten, ganze oder halbe Jahressteuer. Die Seite nennt keinen Betrag. Das ergibt höchstens zwei Karten.
- Das Hundereglement (4.17 Hundereglement EG Kerns vom 27.11.2006, gültig ab 1.1.2007, Stand 18.03.2013) steht auf https://www.kerns.ch/reglemente/16624, das PDF unter https://www.kerns.ch/_doc/5456248. Das PDF lehnte WebFetch ab, weil es in keinem Suchtreffer erschien. Zwei Suchen fanden es nicht. Die Mitteilung zu Herdenschutzhunden (https://www.kerns.ch/aktuellesinformationen/2316577) lieferte einen Fehler der Website.

### Sachseln (OW), neu

- Neu: `data/gemeinden/ow/sachseln.json` (BFS 1406) mit drei lokalen Angaben. Übersetzungen fr und it.
- Hundetaxe (`ow_sachseln_steuer`, Seite «Hundesteuer» der Finanzverwaltung, abgerufen 28.11.2026): CHF 120 für den ersten Hund, CHF 130 für jeden weiteren, landwirtschaftlich gehaltene Hunde CHF 70 für den ersten, CHF 130 für den zweiten und jeden weiteren. Rechnung in der ersten Jahreshälfte, Hälfte nach dem 30. Juni, nichts nach dem 1. November, befreit Schweiss-, Dienst-, Militär- und Blindenhunde. Alles mit wörtlichen Zitaten abgeglichen.
- Anmeldung (`ow_sachseln_steuer`, `ow_sachseln_registrierung`): innert 30 Tagen bei der Finanzverwaltung, neue Halter zuerst bei der Gemeinde registrieren, Mikrochip und Meldung an AMICUS durch die Tierarztpraxis. Wörtlich abgeglichen.
- Kein Zutritt (`ow_sachseln_benuetzung`, Ausführungsbestimmungen zum Benützungsreglement vom 1. Juli 2019, in Kraft seit 12. Dezember 2019, Art. 19 Abs. 2): «Das Mitführen von Hunden in den Innenräumen der Schulanlagen ist untersagt.» Die Übersichtsseite führt nur diese eine Fassung. Stand 2019 auf der Seite genannt.
- Weggelassen: Leine, Leinenpflicht im Wald, Hundekot und Bussen. Sie stehen vermutlich in der «Verordnung über das Halten von Hunden und die Hundesteuer vom 11. November 1991» (https://www.sachseln.ch/reglemente/3506, PDF https://www.sachseln.ch/_doc/3260675). Das PDF lehnte WebFetch ab, weil es in keinem Suchtreffer erschien. Darum kein `hinweis_heute`. Die Definition «landwirtschaftlich gehaltene Hunde» lieferte WebFetch nur gekürzt, sie bleibt weg.

## Backlog

- Erledigt: Engelberg (OW), mit nur drei Angaben aus der Seite «Hundewesen».
- Neue Lücke Engelberg (OW): Reglement über die Hundehaltung und die Hundesteuer (https://www.gde-engelberg.ch/_doc/968078) und Hundesteuer-Tarif (https://www.gde-engelberg.ch/_doc/968079) im Browser lesen. Daraus Betrag der Hundesteuer, Leinenpflicht im Wald mit Zeitraum (für `hinweis_heute`), Verbotsorte, Bussen und Stand des Reglements ergänzen.
- Zurückgestellt (28.11.2026): Kerns (OW), nur zwei Karten belegbar (Hundesteuer ohne Betrag, Anmeldung). Im Browser lesen: Hundereglement https://www.kerns.ch/_doc/5456248 (über https://www.kerns.ch/reglemente/16624) und Mitteilung Herdenschutzhunde https://www.kerns.ch/aktuellesinformationen/2316577.
- Erledigt: Sachseln (OW), drei Angaben.
- Neue Lücke Sachseln (OW): Verordnung über das Halten von Hunden und die Hundesteuer vom 11. November 1991 (https://www.sachseln.ch/_doc/3260675, über https://www.sachseln.ch/reglemente/3506) im Browser lesen. Daraus Leine, Leinenpflicht im Wald mit Zeitraum (für `hinweis_heute`), Verbotsorte, Hundekot und Bussen ergänzen.
