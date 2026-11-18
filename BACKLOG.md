# Ausbauliste

Erledigtes abhaken und das Datum dahinter schreiben. Was sich nicht belegen lässt, mit Datum und Grund als «zurückgestellt» markieren und weitergehen.

## Reihenfolge

Ziel: jede Seite auf Deutsch, Französisch und Italienisch, dazu 60 Gemeinden. Für jeden Lauf gilt die erste Zeile, die zutrifft:

1. **Sonderlauf.** Ist in Abschnitt 5 ein Punkt mit dem Vermerk «fällig» offen, macht der Lauf nur den obersten davon.
2. **Übersetzungen.** Fehlen laut `python3 build.py --fehlend` mehr als 12 Übersetzungen, macht der Lauf nur Übersetzungen, höchstens 12 Dateien.
3. **Neuer Kanton.** Der oberste offene Kanton aus Abschnitt 1. Dazu seine grösste Gemeinde oder sein Hauptort. Ist Abschnitt 1 erledigt und die Mehrsprachigkeit in Abschnitt 5 abgehakt: der oberste offene Eintrag aus Abschnitt 2.
4. **Gemeinden.** Ist kein Kanton möglich, bis zu 4 Gemeinden aus Abschnitt 3.

In jedem Lauf ausser den Sonderläufen zusätzlich höchstens eine Lücke aus Abschnitt 4.

Bleibt ein Kanton nach einem Lauf unvollständig (Entwurf unter `data/entwurf/`), bekommt er in der Liste den Vermerk «zurückgestellt» mit Datum und dem, was fehlt. Der nächste Lauf nimmt den nächsten offenen Kanton. Zurückgestellte Kantone kommen wieder dran, sobald in ihrem Abschnitt kein anderer mehr offen ist. Scheitert ein Kanton dabei ein zweites Mal, bleibt er zurückgestellt, der Bericht meldet ihn zuoberst, und der Abschnitt gilt für die Reihenfolge als erledigt.

## Kette

keine Kette

Die «Kette Übersetzungen» (von Joss am 18. November 2026 um 11:55 Uhr freigegeben, höchstens 8 Glieder) ist mit Glied 7 am 18. November 2026 erledigt: Alle 26 Kantone und 45 Gemeinden gibt es auf Deutsch, Französisch und Italienisch, `python3 build.py --fehlend` meldet nichts mehr.

- [x] a) Übersetzungen der Kantone (erledigt mit Glied 4 am 18.11.2026)
- [x] b) Übersetzungen der Gemeinden (erledigt mit Glied 7 am 18.11.2026)

Was die Glieder in Originalfassungen bemerkt haben, steht in `CHANGELOG.md` unter «Aufgefallen» und gehört in die nächste Nachprüfung.

## 1. Deutschsprachige Kantone

Ungefähr nach Bevölkerung. Schon erfasst: Zürich, Bern, Luzern, Aargau, St. Gallen, Basel-Stadt, Basel-Landschaft, Thurgau, Solothurn, Schwyz, Appenzell Innerrhoden, Graubünden, Zug, Schaffhausen, Appenzell Ausserrhoden, Nidwalden, Glarus, Uri, Obwalden. Aus Abschnitt 2 schon deutsch erfasst: Freiburg.

- [x] Aargau (`ag`), 2026-11-17
- [x] St. Gallen (`sg`), 2026-11-17, mit Stadt St. Gallen
- [x] Basel-Stadt (`bs`), 2026-11-17, mit Stadt Basel
- [x] Basel-Landschaft (`bl`), 2026-11-17, mit Allschwil
- [x] Thurgau (`tg`), 2026-11-17, mit Stadt Frauenfeld
- [x] Solothurn (`so`), 2026-11-17, mit Stadt Olten
- [x] Graubünden (`gr`), 2026-11-18, mit Stadt Chur
- [x] Schwyz (`sz`), 2026-11-17, mit Bezirk Küssnacht
- [x] Zug (`zg`), 2026-11-18, ohne Gemeinde (Stadt Zug zurückgestellt)
- [x] Schaffhausen (`sh`), 2026-11-18, mit Stadt Schaffhausen
- [x] Appenzell Ausserrhoden (`ar`), 2026-11-18, ohne Gemeinde (Herisau zurückgestellt)
- [x] Nidwalden (`nw`), 2026-11-18, ohne Gemeinde (Stans zurückgestellt)
- [x] Glarus (`gl`), 2026-11-18, mit Gemeinde Glarus
- [x] Obwalden (`ow`), 2026-11-18, mit Gemeinde Sarnen. Haftpflicht steht weder im Hundegesetz (GDB 818.3, Stand 2007) noch im Veterinärgesetz. Der Nachtrag zum Veterinärgesetz (Art. 26, Massnahmen bei Hunden) ist seit 1. Dezember 2024 in Kraft.
- [x] Uri (`ur`), 2026-11-18, mit Gemeinde Silenen (Altdorf zurückgestellt)
- [x] Appenzell Innerrhoden (`ai`), 2026-11-17, ohne Gemeinde (Bezirk Appenzell zurückgestellt)

## 2. Französisch und Italienisch

Der Generator baut Französisch und Italienisch seit dem 2026-11-18. Bei zweisprachigen Kantonen beide Fassungen im selben Lauf, weil die Quellen dieselben sind.

- [x] Waadt (`vd`), französisch, 2026-11-18, mit Lausanne (`/fr-ch/vd/`)
- [x] Genf (`ge`), französisch, 2026-11-18, mit Ville de Genève (`/fr-ch/ge/`)
- [x] Wallis (`vs`), französisch und deutsch, 2026-11-18, mit Ville de Sion französisch und Brig-Glis deutsch (`/vs/`, `/fr-ch/vs/`)
- [x] Freiburg (`fr`), französisch und deutsch, 2026-11-18, mit Ville de Fribourg französisch (`/fr/`, `/fr-ch/fr/`)
- [x] Tessin (`ti`), italienisch, 2026-11-18, mit Città di Lugano (`/it-ch/ti/`)
- [x] Neuenburg (`ne`), französisch, 2026-11-18, mit Ville de Neuchâtel (`/fr-ch/ne/`)
- [x] Jura (`ju`), französisch, 2026-11-18, ohne Gemeinde (Delémont zurückgestellt) (`/fr-ch/ju/`)
- [x] Bern (`be`), französische Fassung des Kantons, 2026-11-18 (`/fr-ch/be/`). Biel/Bienne französisch steht in Abschnitt 3.
- [x] Graubünden (`gr`), italienische Fassung, 2026-11-18, ohne Gemeinde (`/it-ch/gr/`)

## 3. Gemeinden

Ungefähr nach Grösse. Neue Kantone tragen hier ihre grössten Gemeinden ein.

- [ ] Aarau (AG): zurückgestellt am 2026-11-17. Nur zwei lokale Angaben belegt (Hundetaxe CHF 120, Anmeldung beim Stadtbüro). Für die dritte fehlt die geltende Polizeiverordnung (SRS 5.1-1, aarau.tlex.ch): Der Lauf konnte nur die Fassung von 2010 lesen. Dort stand eine Leinenpflicht auf Strassen und Plätzen im überbauten Gebiet. Neu ansetzen mit der geltenden Fassung oder dem Bestattungs- und Friedhofreglement von 2023.
- [ ] Wettingen (AG)
- [ ] Baden (AG)
- [ ] Wohlen (AG)
- [ ] Rheinfelden (AG)
- [ ] Reinach (BL)
- [ ] Muttenz (BL)
- [ ] Pratteln (BL)
- [ ] Binningen (BL)
- [ ] Liestal (BL)
- [x] Kreuzlingen (TG), 2026-11-17
- [x] Arbon (TG), 2026-11-17
- [ ] Amriswil (TG): zurückgestellt am 2026-11-17. Nur die Meldestelle belegt (Hundekontrollstelle der Einwohnerdienste). Die Seite der Stadt nennt weder Steuerbetrag noch Orte, die Mitteilung zu den Hundesteuer-Rechnungen war nicht abrufbar.
- [ ] Weinfelden (TG): zurückgestellt am 2026-11-17. weinfelden.ch lässt den Abruf nicht zu (robots), keine andere amtliche Quelle gefunden.
- [ ] Romanshorn (TG): zurückgestellt am 2026-11-17. Das Merkblatt Hundehaltung der Stadt trägt kein Datum und ist beim Kurs veraltet (Stand vor April 2024). Es nennt Steuer CHF 100 und CHF 162.50, Leinenpflicht im Seepark, auf Schlosswiese und Surfwiese, Hundezone im Seepark, Verbot in der Holzensteiner Badi. Die aktuellen Seiten (Hundekontrolle, Hundewiese) lassen den Abruf nicht zu. Neu ansetzen, sobald eine datierte Quelle lesbar ist.
- [ ] Solothurn (SO)
- [ ] Grenchen (SO)
- [ ] Zuchwil (SO)
- [ ] Biberist (SO)
- [ ] Freienbach (SZ): zurückgestellt am 2026-11-17. Das Merkblatt Hundehaltung der Gemeinde ist ein PDF ohne lesbaren Text, die Seite dazu war nicht abrufbar.
- [x] Einsiedeln (SZ), 2026-11-18
- [x] Schwyz (SZ), 2026-11-17
- [x] Arth (SZ), 2026-11-18
- [ ] Bezirk Appenzell (AI): zurückgestellt am 2026-11-17. Die Seite «Hundekontrolle / Vollzug HuG» des Bezirks nennt nur die kantonalen Steuerbeträge und die Meldestelle. Eigene Leinenzonen, hundefreie Zonen oder Bussen waren nach zwei Suchen nicht zu finden.
- [ ] Schwende-Rüte (AI). Hinweis für alle Innerrhoder Bezirke: Die Hundesteuer ist kantonal festgelegt, lokale Angaben gibt es nur, wenn ein Bezirk Leinenzonen oder hundefreie Zonen nach Art. 6 HuG angeordnet hat.
- [ ] Oberegg (AI)
- [ ] Gonten (AI)
- [ ] Schlatt-Haslen (AI)
- [x] Davos (GR), 2026-11-18
- [x] Landquart (GR), 2026-11-18
- [ ] Domat/Ems (GR)
- [ ] St. Moritz (GR)
- [ ] Ilanz/Glion (GR)
- [ ] Riehen (BS)
- [ ] Bettingen (BS)
- [ ] Rapperswil-Jona (SG)
- [ ] Wil (SG)
- [ ] Gossau (SG)
- [ ] Uzwil (SG)
- [x] Winterthur (ZH), 2026-11-18
- [ ] Biel/Bienne (BE), Adresse `biel-bienne`, deutsch und französisch. Französisch zurückgestellt am 2026-11-18: keine amtliche Quelle gefunden.
- [ ] Thun (BE)
- [ ] Köniz (BE)
- [x] Uster (ZH), 2026-11-18
- [x] Emmen (LU), 2026-11-18
- [x] Dübendorf (ZH), 2026-11-18
- [ ] Kriens (LU): zurückgestellt am 2026-11-18. Die Website der Stadt ist für das Abrufwerkzeug gesperrt (robots). Nächster Versuch: Rechtssammlung der Stadt als PDF oder amtliche Dokumente unter stadt-kriens.ch/public/upload/.
- [x] Dietikon (ZH), 2026-11-18
- [x] Wetzikon (ZH), 2026-11-18
- [x] Wädenswil (ZH), 2026-11-18
- [ ] Burgdorf (BE)
- [ ] Langenthal (BE)
- [ ] Horgen (ZH): zurückgestellt am 2026-11-18. Nur zwei lokale Angaben belegt (Gebührentarif ab 2022: Ersthunde CHF 130, verspätetes Anmelden CHF 40). Die Seiten «Hunde» und «Hundekontrolle: Anmeldung» gaben zweimal einen Serverfehler, von der Polizeiverordnung war nur das Inhaltsverzeichnis lesbar (Art. 11 Tierhaltung).
- [x] Bülach (ZH), 2026-11-18
- [ ] Kloten (ZH): zurückgestellt am 2026-11-18. Nur zwei belegte Angaben, der Flyer für Hundebesitzer war nicht abrufbar. Nächster Versuch: Flyer und Polizeiverordnung abrufen.
- [x] Horw (LU), 2026-11-18
- [x] Ebikon (LU), 2026-11-18
- [ ] Steffisburg (BE)
- [ ] Ostermundigen (BE)
- [x] Opfikon (ZH), 2026-11-18
- [x] Thalwil (ZH), 2026-11-18
- [x] Adliswil (ZH), 2026-11-18
- [x] Sursee (LU), 2026-11-18
- [ ] Muri bei Bern (BE)
- [x] Regensdorf (ZH), 2026-11-18
- [x] Illnau-Effretikon (ZH), 2026-11-18
- [ ] Schlieren (ZH): zurückgestellt am 2026-11-18. Nur zwei belegte lokale Angaben. Nächster Versuch: Polizeiverordnung in der Sammlung Kommunales Recht (schlieren.ch/gesetzeskapitel) und Gebührenverordnung SKR 9.10.
- [x] Volketswil (ZH), 2026-11-18
- [ ] Spiez (BE)
- [ ] Lyss (BE)
- [ ] Münsingen (BE)
- [ ] Worb (BE)
- [ ] Ittigen (BE)
- [ ] Hochdorf (LU): zurückgestellt am 2026-11-18. Nur zwei belegte lokale Angaben. Nächster Versuch: Seite «Hundesteuer» der Gemeinde erneut abrufen (Betrag), dazu «Reglemente und Verordnungen».
- [ ] Willisau (LU): zurückgestellt am 2026-11-18. Zu wenig belegte lokale Angaben. Nächster Versuch: Rechtssammlung (willisau.ch/verwaltung-politik/verwaltung/rechtssammlung/) nach Hundesteuer-Betrag, Friedhofreglement und Polizeireglement durchsuchen.
- [ ] Herisau (AR): zurückgestellt am 2026-11-18. Zwei Suchen auf herisau.ch ergaben keine Seite mit lokalen Angaben. Hundesteuer und Anmeldung sind kantonal.
- [ ] Teufen (AR). Hinweis für alle Ausserrhoder Gemeinden: Steuer und Anmeldung sind kantonal. Lokale Angaben gibt es nur, wenn die Gemeinde Leinenorte (Art. 8 Abs. 2 HuG) oder Zutrittsverbote (Art. 9 HuG) bezeichnet hat. Bei Urnäsch und Hundwil zählt die Wildruhezone.
- [ ] Heiden (AR)
- [ ] Speicher (AR)
- [ ] Urnäsch (AR)
- [ ] Hundwil (AR)
- [ ] Zug (ZG): zurückgestellt am 2026-11-18. stadtzug.ch und lesesaal.stadtzug.ch (Stadtratsbeschluss Nr. 20.19 vom 15. Januar 2019 zur Leinenpflicht) waren nicht abrufbar, keine lokale Angabe belegt.
- [ ] Baar (ZG)
- [ ] Cham (ZG)
- [ ] Risch (ZG). Hundereglement unter zg.ch/behoerden/gemeinden/risch-rotkreuz/…/101-hundereglement.
- [ ] Steinhausen (ZG). Reglement über das Halten von Hunden und Merkblatt Hundesteuer 2025 auf zg.ch.
- [ ] Stans (NW): zurückgestellt am 2026-11-18. Hundesteuer und Hundekontrolle sind in Nidwalden kantonal, auf stans.ch keine lokale Angabe zu Hunden gefunden.
- [ ] Hergiswil (NW). Hinweis für alle Nidwaldner Gemeinden: vorher prüfen, ob es überhaupt Gemeinderegeln zu Hunden gibt. Sonst alle zurückstellen.
- [ ] Buochs (NW)
- [ ] Ennetbürgen (NW)
- [ ] Stansstad (NW)
- [x] Glarus (GL), 2026-11-18
- [ ] Glarus Nord (GL)
- [ ] Glarus Süd (GL)
- [x] Schaffhausen (SH), 2026-11-18
- [ ] Neuhausen am Rheinfall (SH)
- [ ] Thayngen (SH)
- [ ] Beringen (SH)
- [ ] Stein am Rhein (SH)
- [ ] Düdingen (FR), deutsch
- [ ] Murten/Morat (FR), deutsch und französisch
- [ ] Bulle (FR), französisch. Hinweis: Viele Freiburger Gemeinden haben ein «Règlement sur la détention et l'imposition des chiens» nach kantonalem Muster, mit Steuerbetrag, Leinenzonen und Bussen. Französische Gemeinden liegen unter `data/fr-ch/gemeinden/`.
- [ ] Villars-sur-Glâne (FR), französisch
- [ ] Estavayer (FR), französisch
- [ ] Yverdon-les-Bains (VD), französisch
- [ ] Montreux (VD), französisch
- [ ] Nyon (VD), französisch
- [ ] Renens (VD), französisch
- [ ] Vevey (VD), französisch
- [ ] La Chaux-de-Fonds (NE), französisch
- [ ] Le Locle (NE), französisch
- [ ] Val-de-Ruz (NE), französisch
- [ ] Val-de-Travers (NE), französisch
- [ ] Milvignes (NE), französisch
- [x] Sarnen (OW), 2026-11-18
- [ ] Kerns (OW). Hinweis für alle Obwaldner Gemeinden: Die Leinenpflicht im Wald steht in den Hundeverordnungen der Gemeinden, Alpnach hat laut Kanton keine.
- [ ] Alpnach (OW)
- [ ] Sachseln (OW)
- [ ] Engelberg (OW)
- [ ] Altdorf (UR): zurückgestellt am 2026-11-18. Nur zwei lokale Angaben belegt (Hundesteuer CHF 80, An- und Abmeldung bei der Einwohnerkontrolle innert 30 Tagen). Die «Verordnung über das Halten von Hunden» (30.31, vom 1. August 2017) steht im Rechtsbuch der Gemeinde, das Abrufwerkzeug liess das PDF zweimal nicht zu (altdorf.ch/uploads/organisation/politik/rechtssammlung/30_oeffentliche_ordnung_und_sicherheit/30.31.pdf). Neu ansetzen, sobald das PDF lesbar ist.
- [x] Silenen (UR), 2026-11-18
- [ ] Andermatt (UR). Verordnung über das Halten von Hunden von 2007 ist gelesen (Taxe CHF 110, Leine im Dorf, Verbotsorte, Busse bis CHF 500). Vor dem Anlegen prüfen, ob sie unverändert gilt. Hinweis für alle Urner Gemeinden: Der Kanton hat kein Hundegesetz, jede Gemeinde hat eine eigene Hundehalteverordnung (meist Nummer 30.31 im Rechtsbuch der Gemeinde).
- [ ] Schattdorf (UR)
- [ ] Bürglen (UR)
- [ ] Erstfeld (UR)
- [ ] Flüelen (UR). Hundehalteverordnung von 2006 unter flueelen.ch, am 2026-11-18 nicht abrufbar.
- [ ] Saint-Imier (BE), französisch
- [ ] Tramelan (BE), französisch
- [ ] La Neuveville (BE), französisch
- [ ] Valbirse (BE), französisch
- [ ] Vernier (GE), französisch
- [ ] Lancy (GE), französisch
- [ ] Meyrin (GE), französisch
- [ ] Carouge (GE), französisch
- [ ] Onex (GE), französisch
- [x] Sion (VS), französisch, 2026-11-18
- [x] Brig-Glis (VS), deutsch, 2026-11-18
- [ ] Visp (VS), deutsch
- [ ] Naters (VS), deutsch
- [ ] Martigny (VS), französisch
- [ ] Monthey (VS), französisch
- [ ] Sierre (VS), französisch. Hinweis für alle Walliser Gemeinden: Die Gemeinde legt die Hundesteuer fest (CHF 100 bis 250) und kann Leinenzonen und Verbotsorte bestimmen. Viele veröffentlichen jedes Jahr einen Anschlag «Hundesteuer» oder «Avis aux propriétaires de chiens».
- [ ] Delémont (JU), französisch: zurückgestellt am 2026-11-18. Nur zwei lokale Angaben belegt (Grundtaxe CHF 130 laut Budget 2026, Anmeldung beim Secrétariat de la police administrative). Das «Règlement communal sur la garde et la taxe des chiens» (delemont.ch/Htdocs/Files/v/26541.pdf) ist ein PDF ohne lesbaren Text, die Rechtssammlung delemont.tlex.ch liefert dem Abrufwerkzeug keinen Inhalt.
- [ ] Porrentruy (JU), französisch. Règlement concernant la garde et la taxe des chiens unter porrentruy.ch/_docn/5559397/… (am 2026-11-18 Serverfehler). Hinweis für alle jurassischen Gemeinden: Die Gemeinde legt die Taxe mit dem Budget fest und regelt Leine, Verbotsorte und Bussen in einem eigenen Reglement über Haltung und Taxe der Hunde.
- [ ] Saignelégier (JU), französisch. Règlement concernant la garde et la taxe des chiens vom 17. Juni 2003 unter saignelegier.ch/FileDownload/Download/30 (lesbar: Leine auf öffentlichen Strassen und Plätzen, Verbot auf Spielplätzen, Friedhöfen und Schulanlagen, Bussen CHF 50 bis 1000). Der Betrag der Taxe fehlt noch.
- [ ] Haute-Sorne (JU), französisch
- [ ] Develier (JU), französisch. Seite «Chiens» unter develier.ch.
- [ ] Bellinzona (TI), italienisch
- [ ] Locarno (TI), italienisch
- [ ] Mendrisio (TI), italienisch
- [ ] Chiasso (TI), italienisch

## 4. Lücken in bestehenden Seiten

- [ ] Stadt Zürich: Betrag der Hundeabgabe belegen und als Karte «Hundeabgabe» ergänzen
- [ ] Stadt Zürich: Freilaufzonen aus dem städtischen Datensatz «Hundezonen» namentlich aufführen
- [ ] Stadt Bern: Betrag der Hundetaxe belegen
- [ ] Stadt Bern: Quelle «Gemeinderat Bern 2019» (Tierpark, Kinderzoo) durch eine aktuelle amtliche Quelle ersetzen
- [ ] Stadt Luzern: Bussen mit einer Quelle nach 2022 belegen
- [ ] Kanton Bern: «kein Kursobligatorium» mit einer Quelle des Kantons statt der Gemeinde Büren belegen
- [ ] Kanton Bern: Entscheid des Grossen Rats von 2023 zur Wald-Leinenpflicht mit einer amtlichen Quelle (Ratsprotokoll) belegen

- [ ] Kanton Aargau: Hundeverordnung (HuV, SAR 393.411) in der geltenden Fassung lesen. Der Lauf vom 2026-11-17 erreichte nur die Fassungen von 2014 und 2016. Danach ergänzen, falls unverändert: Deckungssumme der Haftpflicht für Listenhunde, Fristen für Kurs und Prüfung, halbe Taxe.
- [ ] Kanton Aargau: Ordnungsbusse für Hundekot (CHF 100) mit einer Fassung der OBVV nach 2021 bestätigen

- [ ] Stadt St. Gallen: Leinenpflicht und Hundeverbote direkt mit dem Polizeireglement belegen (bisher nur über die Seite der Stadtpolizei), Bussen ergänzen
- [ ] Kanton St. Gallen: Verordnung über die Jagdvorschriften (sGS 853.111) auf eine Leinenpflicht im Wald prüfen. Am 2026-11-17 war der Text nicht lesbar. Bis dahin sagt die Seite nur, was in Hundegesetz, Jagdgesetz und Jagdverordnung steht.
- [ ] Kanton Basel-Stadt: Gebiete ohne Wald-Leinenpflicht (rechte Wieseseite, Vorländer und Dammwege laut Veterinäramt) mit dem Beschluss des Regierungsrats nach § 8 Abs. 3 WJG belegen und auf der Seite ergänzen
- [ ] Kanton Basel-Stadt: Busse CHF 100 mit der Ordnungsbussenverordnung belegen (bisher Seite des Veterinäramts)
- [ ] Kanton Basel-Stadt: Das Hundegesetz wird revidiert (Entwurf in Vernehmlassung). Beim Nachprüfen den Stand von SG 365.100 beachten.
- [ ] Stadt Basel: Hundefreilaufzonen aus der Karte geo.bs.ch/hundesignalisation namentlich aufführen
- [ ] Kanton Basel-Landschaft: Die Seiten des Veterinärdienstes und des Amts für Wald auf baselland.ch waren am 2026-11-17 nicht abrufbar. Beim Nachprüfen die Angaben aus den Gesetzen damit vergleichen und AMICUS, «Waldesnähe» und die Busse bei der Leinenpflicht ergänzen, falls dort belegt.
- [ ] Allschwil: Freilaufwege aus dem Plan in Anhang I des Polizeireglements namentlich aufführen
- [ ] Kanton Thurgau: Hundegesetz und Hundeverordnung im Rechtsbuch des Kantons (rechtsbuch.tg.ch) statt auf LexFind lesen und die Seite «Hunde» des Veterinäramts abgleichen. Danach ergänzen, falls belegt: Meldefrist bei der Gemeinde, Übergangsregel beim Kurs für kleine Hunde, Datum des Merkblatts mit der Gebühr von CHF 500.
- [ ] Kreuzlingen: Orte mit Leinenpflicht, Hundeverbot oder Freilauf belegen (Seeufer, Seeburgpark). Broschüre und Website nennen keine. Die Seite steht bisher auf Steuer, Anmeldung und Kotsäcken.
- [ ] Kreuzlingen und Arbon: Meldefrist bei der Stadt klären (Quellen der Stadt widersprechen sich: 10 und 30 Tage, 10 und 14 Tage)
- [ ] Arbon: Stand der Broschüre und der Steuerbeträge mit einer datierten Quelle belegen
- [ ] Stadt Frauenfeld: Hundeverbote und Bussen der Stadt suchen (Polizeireglement), die Informationen für Hundehaltende nennen keine
- [ ] Kanton Solothurn: Hundegesetz und Hundeverordnung im vollen Wortlaut lesen (das Abrufwerkzeug lieferte Zusammenfassungen mit kurzen Zitaten). Danach ergänzen, falls belegt: Gebühr der Haltebewilligung (Merkblatt des Veterinärdienstes, Gebührentarif), Bussen, was die Änderung vom 18. Mai 2025 gebracht hat. Klären, ob die Leinenpflicht vom 1. April bis 31. Juli auch am Waldrand gilt (Verordnung: «im Wald», Seite «Mein Hund und ich»: «Wald und Waldränder»).
- [ ] Stadt Olten: prüfen, ob das Polizeireglement von 2016 (Art. 19, Leine im Siedlungsgebiet) nach der Teilrevision von 2019 unverändert gilt. Hundeverbote (Friedhof, Badi, Schulanlagen) und Freilaufflächen suchen, das Reglement nennt keine.
- [ ] Kanton Schwyz: Veterinärgesetz (SRSZ 312.420, sz.ch/public/upload/assets/6711/312_420.pdf, gelesen mit Stand 2015) und Veterinärverordnung (SRSZ 312.421, lexfind.ch/tol/16642/de, gelesen mit Stand 2016) in der geltenden Fassung lesen und ergänzen, falls belegt: AMICUS als Datenbank des Kantons, Kontrolle durch die Gemeinden, Massnahmen des Kantonstierarztes im Einzelfall (Leine, Maulkorb, Wesenstest, Erziehungskurs). Meldung von Beissvorfällen: Seite «Tierschutz» des Kantonstierarztes der Urkantone (laburk.ch).
- [ ] Kanton Schwyz: Jagd- und Wildschutzgesetz (SRSZ 761.100) lesen. Die am 2026-11-17 abgerufene Fassung trug den Stand «1.2.2027» und wurde nicht verwendet. Danach ergänzen, falls belegt: wildernde Hunde, Leinenpflicht in den kantonalen Schutzgebieten (Frauenwinkel, Lauerzersee, Rothenthurm, Ibergeregg und weitere) mit Ordnungsbusse CHF 100.
- [ ] Gemeinde Schwyz: Orte mit Leinenpflicht, Hundeverbot oder Freilauf suchen (Friedhof, Badi, Schulanlagen). Die Seite steht bisher auf Steuer, Anmeldung und Meldungen. Die Schutzverordnung von 1999 enthält nichts zu Hunden.
- [ ] Bezirk Küssnacht: Eine Mitteilung des Bezirks vom 3. September 2020 beschreibt eine eingezäunte Hundewiese beim Sportzentrum Luterbach. Eine spätere Mitteilung («IG übernimmt Hundewiese») war nicht abrufbar. Mit aktueller Quelle ergänzen.
- [ ] Kanton Schwyz: Die Teilrevision des Hundegesetzes war am 16. September 2026 im Kantonsrat. Ergebnis und Inkrafttreten waren am 2026-11-17 amtlich nicht auffindbar. Bei jedem Nachprüfen den Stand von SRSZ 546.100 prüfen. Die Revision bringt laut Medienmitteilung vom 25. August 2026: Kurspflicht innert 18 Monaten, Jahressteuer mit Sätzen des Gemeinderats, Freilaufzonen, keine Hundemarke mehr. Danach Kanton und Küssnacht anpassen.
- [ ] Bezirk Küssnacht: Die Seite stützt sich auf die Broschüre von April 2019. Die aktuellen Seiten (Dienstleistung Hunde, Hundewiese, Ausnahme im Luterbach) lassen den Abruf nicht zu (robots). Mit einer neueren Quelle bestätigen, Hundewiese ergänzen.
- [ ] Kanton Appenzell Innerrhoden: Jagdgesetz (GS 922.000) und Wildruhegebiete auf Regeln für Hunde prüfen. Danach den Wald-Text anpassen.
- [ ] Kanton Appenzell Innerrhoden: Seite «Leinenpflicht in beiden Appenzell» (ar.ch, Veterinäramt) abrufen und mit `leine` abgleichen.
- [ ] Kanton Appenzell Innerrhoden: Daten der Alpzeit und betroffene Alpen (Alpgesetz, Art. 1 der Verordnung) belegen.
- [ ] Kanton Graubünden: geltende Fassung des Veterinärgesetzes (BR 914.000) auf gr-lex.gr.ch gegenprüfen. Gelesen wurde der Stand 1. Januar 2016.
- [ ] Kanton Graubünden: Regeln zu Hunden in Wildruhezonen und Wildschutzgebieten suchen. Hundesteuer: Gesetz über die Gemeinde- und Kirchensteuern (BR 720.200) erneut abrufen.
- [ ] Kanton Graubünden italienisch: eine italienischsprachige Gemeinde anlegen (Poschiavo, Roveredo oder Mesocco), wenn drei lokale Angaben belegt sind. Die Karte «Imposta sui cani» nennt noch kein Beispiel einer Gemeinde. Die Legge sulla veterinaria (CSC 914.000) wurde wie die deutsche Fassung im Stand 1. Januar 2016 gelesen: geltende Fassung gegenprüfen.
- [ ] Stadt Chur: Polizeigesetz der Stadt (RB 411) im Wortlaut suchen (Leine, Kot, Flurordnung, Bussen).
- [ ] Bezirk Einsiedeln: Die Seite stützt sich auf eine Broschüre ohne Datum (Steuersätze ab 2012) und das Anmeldeformular. Mit einer datierten Quelle bestätigen, Orte mit Leinenpflicht oder Hundeverbot suchen (Friedhof, Klosterplatz, Sihlsee).
- [ ] Gemeinde Arth: «Hinweise-Hundehalter.pdf» (arth.ch/_doc/3664036) und die Robidog-Pläne waren am 2026-11-18 nicht abrufbar. Lesen und ergänzen. Prüfen, ob das Friedhofreglement von 2016 unverändert gilt (Genehmigung durch den Regierungsrat, spätere Änderungen).
- [ ] Gemeinde Davos: Betrag der Ordnungsbussen (Gemeindegesetz über öffentliche Ruhe und Ordnung), Gebührentarif (DRB 22.1) und Friedhofsgesetz (DRB 17) lesen und ergänzen.
- [ ] Gemeinde Landquart: Polizeigesetz, Steuergesetz, Friedhofordnung und Benützungsreglement für Flur- und Waldwege im Wortlaut lesen (landquart.ch/gesetze/gesetzesgrundlagen, am 2026-11-18 nicht abrufbar). Bisher ist Art. 50 Polizeigesetz nur über die Mitteilung des Gemeindepolizeiamts belegt. Meldefrist, Leinenpflicht, Verbote und Bussen ergänzen.

- [ ] Kanton Appenzell Ausserrhoden: Seite des Veterinäramts (ar.ch/hunde) abrufen: heutige Meldestelle und Meldeweg, Abgleich mit `leine`.
- [ ] Kanton Appenzell Ausserrhoden: geltenden Stand und Perimeter der Wildruhezone «südliches Appenzeller Hinterland» belegen, weitere Wildruhezonen oder Naturschutzgebiete mit Regeln für Hunde suchen.
- [ ] Kanton Appenzell Ausserrhoden: Sömmerungsvorschriften und Alpen auf Regeln für Hunde prüfen. Bussenbeträge (Ordnungsbussen) für Leine und Kot belegen.
- [ ] Kanton Zug: «Infoblatt Hundereglemente der Gemeinden im Kanton Zug» des Veterinärdienstes auswerten (cdn.zg.ch war nicht abrufbar). Damit die Karten Haftpflicht, Kurs, Rassen und Hundesteuer schärfen (heute nur Verweis auf die Gemeinde). Paragraf und Busse der Leinenpflicht im Einführungsgesetz zum Waldgesetz nachtragen, Meterangabe zum Waldrand, falls das Gesetz eine nennt.
- [ ] Kanton Nidwalden: geltende Fassung des Hundegesetzes (NG 826.3) und der Hundeverordnung aus gesetze.nw.ch gegenprüfen (braucht einen Browser) und die Hinweise «Fassung von 2005» entfernen oder die Angaben korrigieren. Verordnung über die Wildruhegebiete (NG 841.15) im Volltext: Gebiete und Daten der Leinenpflicht nachtragen. Kantonales Waldgesetz auf Leinenpflicht prüfen.
- [ ] Kanton Schaffhausen: geltende Fassung von SHR 455.200 und 455.201 abrufen (rechtsbuch.sh.ch braucht einen Browser) und alle Angaben mit «Stand des Gesetzestexts: 2010» abgleichen, danach die Stand-Hinweise entfernen. Karte Kurs klären, sobald die Seite des Veterinäramts lesbar ist.
- [ ] Stadt Schaffhausen: Betrag der Hundeabgabe und Anmeldestelle belegen.
- [ ] Kanton Glarus: Einführungsgesetz GS IV G/3/2 abrufen (gesetze.gl.ch braucht einen Browser) und daraus Leinenpflicht im öffentlichen Raum (Art. 31), Deckungssumme, Kotaufnahme und Bussen ergänzen. Die Leinenorte stehen bisher nur über die Seite der Gemeinde Glarus auf der Kantonsseite. Danach Karte Kurs und `ton` prüfen. Merkblatt bewilligungspflichtige Hundehaltung erneut abrufen.
- [ ] Gemeinde Glarus: lokale Leinen- oder Verbotsorte und Bussen belegen (Polizeireglement nicht gefunden).
- [ ] Kanton Freiburg: geltende deutsche Fassung des HHR (SGF 725.31, 2024) abrufen und die deutsche Datei damit belegen (Haftpflicht, Fristen). Bewilligung für mehr als vier Hunde und Ordnungsbusse für die Leine im Wald (OCAO, FR 107) belegen.
- [ ] Ville de Fribourg: heutigen Betrag der Gemeindesteuer bestätigen (Reglement von 1993: CHF 120). Anmeldestelle der Stadt und allfällige Freilaufzonen suchen.
- [ ] Kanton Waadt: geltende Fassung von LPolC (BLV 133.75) und RLPolC auf der Gesetzessammlung des Kantons gegenprüfen (gelesen: Stand 2014). Wortlaut von Art. 2a RLFaune abrufen. Regeln für Besuch und Zuzug mit bewilligungspflichtigen Hunden suchen.
- [ ] Ville de Lausanne: Règlement général de police (Leine, Verbotsorte, Kot, Bussen) und Namen der Freilaufzonen suchen.
- [ ] Kanton Neuenburg: Wortlaut der LChiens (Art. 4, 5, 7, 8, 14, 17) und der LFS am PDF gegenprüfen. Kursreglement des Staatsrats und eigene Seite des SCAV zu Hunden suchen.
- [ ] Ville de Neuchâtel: Betrag der Hundetaxe, Namen der Freilaufzonen, geltende Fassung des Polizeireglements und Liste der Strände im Faltblatt gegenprüfen.
- [ ] Winterthur: Allgemeine Polizeiverordnung und Nutzungsordnungen der Parks (Leine, Verbote, Bussen) nachtragen. Datum des Merkblatts Hundewesen klären.
- [ ] Uster: Ordnungsbussen der Stadt zu Hunden suchen.
- [ ] Dübendorf: klären, ob die Hundesteuer den Kantonsbeitrag enthält. Geltende Fassung der Polizeiverordnung prüfen.
- [ ] Dietikon: Polizeiverordnung 510.1 abrufen (dietikon.ch/_doc/7194661): Leine, Verbote, Kot, Bussen.
- [ ] Wetzikon: Art. 22 und 23 der Polizeiverordnung am Volltext gegenprüfen (auch die Aussage «keine eigene Leinenpflicht»), Ordnungsbussen und Hundewiese nachtragen.
- [ ] Wädenswil: Kantonsbeitrag klären, Polizeiverordnung (Leine, Verbote, Kot, Bussen) nachtragen.
- [ ] Bülach: Gebührenreglement (verspätete Meldung, Gebühr ab 1. April) und Polizeiverordnung nachtragen, Kantonsbeitrag klären.
- [ ] Kanton Obwalden: Zeitraum der Leinenpflicht im Wald je Gemeinde (Sarnen ist erfasst: Mitte Dezember bis Ende Juni, ohne Abstand in Metern). Nummern und Namen der Wildruhezonen 1 bis 7. Aktuelle Liste der Naturschutzzonen mit Leinenpflicht. Höhe der Bussen in Sarnen (die Verordnung nennt keinen Betrag).
- [ ] Kanton Bern, französische Fassung: Loi sur les chiens (RSB 916.31) französisch im Wortlaut lesen und `data/fr-ch/kantone/be.json` daran gegenprüfen, vor allem Befreiungen von der Taxe, Zutrittsverbote der Gemeinden und Bussen. Geltende Fassung der OCAO für die Bussenbeträge. Französische amtliche Quelle zur Leinenpflicht im Wald.
- [ ] Kanton Genf: LChiens und RChiens im Volltext gegenprüfen, besonders RChiens Art. 13 Bst. l (Ufer, Oktober bis März) und Art. 14 Bst. d und e sowie die Änderungen vom 17. November 2026. Gemeindezuschläge zur Hundesteuer (ge.ch/node/110), auch für die Stadt Genf. Bussenbeträge. PDF «Liste des races de chiens considérées comme potentiellement dangereuses» mit RChiens Art. 17 abgleichen.
- [ ] Kanton Tessin: geltende Fassung der LCani auf der Gesetzessammlung des Kantons (www3.ti.ch) im Wortlaut gegenprüfen, besonders Art. 4, 4a, 7 und 11a. Datum der Kurspflicht klären (1. Juni oder 1. September 2026). Tessiner Jagd- und Waldrecht auf Leinenpflicht prüfen. Lugano: italienische Seite der Hundezonen suchen und Barbengo bestätigen.
- [ ] Kanton Thurgau: `data/kantone/tg.json` gegen das Hundegesetz (RB 641.2, geltende Fassung) prüfen, sobald der Wortlaut abrufbar ist. Dabei kann die Busse von CHF 50 für das Nichtanleinen in Anlagen und an verkehrsreichen Strassen bei `leine` ergänzt werden. Am 18.11.2026 zum zweiten Mal nicht abrufbar. Beim nächsten Mal zuerst eine andere amtliche Quelle suchen und in der Karte Rassen den Gentest unter 50 Prozent (§ 3a Abs. 4 HundeG), «Betreuen» und die Geltung für Auswärtige (bisher nur im Merkblatt) mit dem Gesetz abgleichen. Zugleich schauen, ob die Hundeverordnung (§ 7b Abs. 3) Bullmastiff und Alano inzwischen nennt: Bisher stehen sie nur im Merkblatt des Veterinäramts.
- [ ] Emmen, Horw, Ebikon: Wortlaut der Quellen gegenprüfen. Bussen, weitere Orte mit Leinenpflicht oder Hundeverbot, Robidog.
- [ ] Emmen: Ausgang des Postulats Hundefreilaufzonen (Einwohnerrat, 12. Mai 2026). Junghunde-Tarif.
- [ ] Horw: geltende Rechtsgrundlage und aktueller Stand der Leinenpflicht im Naturschutzgebiet Widenbachdelta (Quelle von 2015).
- [ ] Ebikon: Bedingungen der Tarife CHF 60 und CHF 0, Rechtsgrundlage der Leinenregel im Waldreservat im Riedholz.
- [ ] Sursee: Bussen, Friedhofreglement, Robidog und Hundekot, Wortlaut der Seite Hundekontrolle gegenprüfen.
- [ ] Opfikon: Ordnungsbussen Hundehalter und Polizeiverordnung (Leine, Verbote, Kot) nachtragen, Angaben am Volltext gegenprüfen.
- [ ] Thalwil: Herkunft der Leinenpflicht auf Strassen, Plätzen und Schularealen klären (Polizeiverordnung), Bussen nachtragen.
- [ ] Adliswil: Polizeiverordnung (Leine, Verbote, Kot, Bussen) nachtragen.
- [ ] Regensdorf: Betrag der Hundesteuer und Polizeiverordnung (Leine, Verbote, Kot, Bussen) nachtragen.
- [ ] Volketswil: Anmeldestelle, Meldegebühr und Ordnungsbussenliste des Gemeinderats nachtragen.
- [ ] Illnau-Effretikon: geltende Fassung des Gebührenreglements suchen und die Beträge von 2019 bestätigen oder ersetzen (vordringlich). Anmeldestelle und Polizeiverordnung nachtragen.
- [ ] Kanton Uri: Verfassung des Kantons (RB 1.1101, Art. 110 Abs. 1 Bst. a) als Grundlage der Gemeindeverordnungen direkt belegen. Merkblatt «Verhaltensregeln für Hundehalter» des Veterinärdienstes der Urkantone lesen (laburk.ch, am 2026-11-18 nicht abrufbar). Busse für die Leinenpflicht im Wald belegen (Art. 44 KJSV nennt keinen Betrag, Ordnungsbussenrecht prüfen). Prüfen, ob die Verordnung von Andermatt von 2007 unverändert gilt, sonst die Beispiele auf der Kantonsseite ersetzen.
- [ ] Silenen: Wortlaut der Hundehalteverordnung am PDF gegenprüfen (gelesen als Zusammenfassung des Abrufwerkzeugs), «definierte Gebiete» mit Leinenpflicht und Anmeldestelle auf der Website der Gemeinde suchen.
- [ ] Kanton Wallis: französischen Wortlaut der LALPA (RS/VS 455.1) lesen. lex.vs.ch war am 2026-11-18 nicht abrufbar, die französische Fassung stützt sich auf die Seiten des Service cantonal. Danach ergänzen, falls belegt: Verbotsorte der Gemeinden (Art. 33), Material für den Kot (Art. 32), Bussen. Deutsche Fassung: geltenden Stand des AGTSchG prüfen (gelesen: Stand 1.1.2020) und die Bussenbeträge klären (Art. 53 und 54, die Ausbildungsverordnung verweist für die Busse des Veterinäramts auf Art. 54).
- [ ] Kanton Wallis: deutsche Fassung des Steuergesetzes (SGS 642.1, Art. 182) in der geltenden Fassung lesen. Der Rahmen CHF 100 bis 250 ist in der deutschen Datei mit dem französischen Gesetzestext belegt (Stand 1.1.2026).
- [ ] Kanton Wallis: Jagd- und Naturschutzrecht auf eine Leinenpflicht im Wald oder in Wildruhezonen prüfen. Die Richtlinien für Gemeinden zu verbotenen Hunden (PDF auf vs.ch) liessen den Abruf nicht zu. Der Kanton hat 2026 ein neues kantonales Hundegesetz in die Vernehmlassung gegeben: beim Nachprüfen den Stand beachten.
- [ ] Kanton Jura: Wortlaut der Loi concernant la taxe des chiens (RSJU 645.1, Stand 1.1.2020) aus amtlicher Quelle lesen und Rahmen der Taxe, Stichtag, Befreiungen und Strafsteuer ergänzen. Am 2026-11-18 lieferte rsju.jura.ch nur die Rahmenseite, die PDF auf jura.ch und delemont.ch liess das Abrufwerkzeug nicht zu. Die Karte nennt deshalb nur, dass die Taxe kommunal ist, und Delémont als Beispiel.
- [ ] Kanton Jura: geltende Fassung der Ordonnance sur la chasse (RSJU 922.111, Art. 40) lesen. Abrufbar war nur der Stand 2012, die Seite nennt ihn. Danach auch Bussen ergänzen (Loi sur la chasse, RSJU 922.11, Art. 71: nur im Stand 2013 gelesen, weggelassen).
- [ ] Ville de Sion: geltende Fassung des Règlement communal de police prüfen (gelesen: Fassung von 1996, homologiert 1997). Freilaufzonen und Verbotsorte suchen.
- [ ] Brig-Glis: Datum des Merkblatts «Freilauf-Zonen / Leinenpflicht» klären, Merkblatt Robidogs lesen.
- [ ] Luzern, Karte Rassen: Die einzige Quelle ist ein Medium (`srf`). Amtliche Quelle suchen, sonst die Angabe kürzen (aufgefallen in der Kette Übersetzungen, 18.11.2026)
- [ ] Wallis deutsch, Karte Rassen: die Rassenamen «Neapolitanischer Mastiff» und «Spanischer Mastiff» mit der Quelle vergleichen (aufgefallen 18.11.2026)
- [ ] Tessin, Karte Rassen, Liste: «Pastori belga» mit der Quelle vergleichen (aufgefallen 18.11.2026)
- [ ] Glarus, Feld `wald`: `saison` ist `false`, die Leine gilt aber ganzjährig. Die Seite titelt «Keine Saisonregel im Wald». Titel oder Daten so anpassen, dass niemand «keine Pflicht» liest (aufgefallen in der Kette Übersetzungen, 18.11.2026)
- [ ] Uri, Karte Unterwegs: «unschädlich machen» mit der Jagdverordnung vergleichen und klarer fassen (aufgefallen 18.11.2026)
- [ ] Waadt, Genf und Neuenburg französisch, `vergleich.wald`: Schreibweise «1.4 au 15.7» an «du 1.4. au 15.7.» angleichen. Danach sind die Übersetzungen veraltet und im selben Lauf nachzuführen (aufgefallen 18.11.2026)

### Aufgefallen beim Übersetzen (Kette Übersetzungen, 18.11.2026)

Die Glieder der Kette haben jede Originalfassung Satz für Satz gelesen und notiert, was unklar oder uneinheitlich ist. Nichts davon ist ein belegter Fehler. Beim Nachprüfen der jeweiligen Datei mit der Quelle klären. Ändert sich dabei die Originalfassung, sind ihre Übersetzungen veraltet und im selben Lauf nachzuführen.

- [ ] `data/fr-ch/kantone/ne.json`, Feld `vergleich.wald`: «15.4 au 30.6» ohne Punkt nach dem Monat, wie schon bei VD und GE gemeldet. Die Übersetzungen schreiben «15.4. bis 30.6.» und «dal 15.4. al 30.6.».
- [ ] `data/fr-ch/kantone/ne.json`, Karte Annonce: «vous annoncez votre arrivée à votre commune de domicile» ist unklar (wessen Ankunft?). Übersetzt als «meldest du dich bei deiner Wohngemeinde». Beim Nachprüfen mit der Quelle vergleichen.
- [ ] `data/kantone/bl.json`, Karte Hundesteuer: «landwirtschaftlicher Nebenhof» ist ein Begriff aus dem Gesetz ohne Erklärung. In den Übersetzungen steht er deutsch in Klammern hinter «ferme annexe» und «fattoria annessa».
- [ ] `data/kantone/sz.json`, Karte Anmeldung: Marke «Pflicht» mit `ton: note`, bei BL, SO und TG steht dieselbe Marke mit `ton: must`.
- [ ] `data/kantone/tg.json` und `data/kantone/gr.json`: Tausender verschieden geschrieben («CHF 5'000» und «CHF 20 000»).
- [ ] `data/kantone/gl.json`, Karte Haftpflicht: im `wert` «innert 1 Monat» mit Ziffer, im Text «innert eines Monats» als Wort. Die Übersetzungen folgen dem Original.
- [ ] `data/kantone/nw.json`, Karte Anmeldung: «spätestens drei Monate nach der Geburt» gilt wörtlich nur für Welpen. Für später übernommene Hunde nennt die Karte keine Frist.
- [ ] `data/kantone/ur.json`, Karte Unterwegs: «unschädlich machen» ist unklar (erlegen?). Übersetzt als «mis hors d'état de nuire» und «resi inoffensivi». Beim Nachprüfen mit der Jagdverordnung vergleichen.
- [ ] `data/kantone/zg.json`, Karten Haftpflicht, Kurs und Rassen: derselbe erste Satz steht dreimal auf der Seite.
- [ ] `data/kantone/ai.json`, Feld `leine`, erster Punkt, und `wald`: «Alpzeit» ohne Daten. Wer die Seite liest, erfährt nicht, wann die Leinenpflicht auf den Alpen gilt. Der Satz dazu steht nur im Feld `leine`.
- [ ] `data/kantone/ai.json`, Karte Anmeldung: Die Karte nennt keine Frist für die Meldung an den Bezirk und nennt die Hundedatenbank nicht beim Namen (andere Kantone: AMICUS).
- [ ] `data/gemeinden/zh/adliswil.json`, Karte Gebühren: «erhebt die Stadt», die Einleitung nennt aber die Polizei Adliswil - Langnau am Albis als zuständig. Karte Anmeldung: `wert` mit «10», `text` mit «zehn».
- [ ] `data/gemeinden/zh/buelach.json`, Karte Hundetaxe: «Danach wird die Gebühr höher, ausser der Hund ist neu» nennt keinen Betrag und sagt nicht, was «neu» heisst.
- [ ] `data/gemeinden/zh/dietikon.json` und `data/gemeinden/zh/illnau-effretikon.json`, Karte «Entlaufener Hund»: «Vermittlung eines entlaufenen Hundes» ist unklar (Rückgabe an die Halterin oder Weitervermittlung?). Übersetzt als «restitution» und «riconsegna», also Rückgabe. Bei der nächsten Nachprüfung am Tarif klären.
- [ ] `data/gemeinden/zh/illnau-effretikon.json`: alle drei Karten stammen aus derselben Quelle mit Stand 2019.
- [ ] `data/gemeinden/zh/regensdorf.json` und `data/gemeinden/be/bern.json`, Karte Hundetaxe: kein Betrag. Bei Bern steht nur der Stichtag.
- [ ] `data/fr-ch/gemeinden/fr/fribourg.json`, Karte «Laisse»: `wert` nennt «manifestations», der Text nicht.
- [ ] `data/fr-ch/gemeinden/ge/geneve.json`, `freilaufzonen`: «promenade des Crêts» und «parc Bertrand» stehen in beiden Listen (eingezäunt und nicht eingezäunt). Der parc Liotard steht bei den Freilaufzonen und bei den Verboten, die Karte «Accès interdit» sagt das selbst. Mit der Quelle vergleichen.
- [ ] `data/fr-ch/gemeinden/vs/sion.json`, Karte «Annonce»: «le passeport de l'animal avec son numéro AMICUS» lässt offen, ob die Nummer im Pass stehen muss oder zusätzlich vorzulegen ist.
- [ ] `data/gemeinden/bl/allschwil.json`: Karte Hundetaxe spricht von «Hundegebühr». Karte Bussen schreibt «CHF 5'000», die anderen Dateien «CHF 5000».
- [ ] `data/gemeinden/lu/luzern.json`: nur eine Karte (Bussen). Dort ist «CHF 100 bis 150 (Naturschutzgebiete)» unklar: Gilt der ganze Rahmen oder nur der obere Betrag für Naturschutzgebiete?
- [ ] `data/gemeinden/tg/arbon.json`, Karte Anmeldung: Die Stadt nennt 10 und 14 Tage, die Karte sagt das offen. Bei der Nachprüfung klären.
- [ ] `data/gemeinden/vs/brig-glis.json`, Karte Hundetaxe: `wert` «CHF 125 pro Jahr» ohne «pro Hund». Karte Leine: `wert` nennt «Brig, Glis, Gamsen und Brigerbad», der Text «Brig-Glis und Gamsen».
- [ ] `data/it-ch/gemeinden/ti/lugano.json`: Karte «Imposta sui cani» spricht im Text von «tassa». Die Datei nennt die Freilaufzonen «aree per cani», die Wortliste des Handbuchs «area di svago per cani», und in der Karte «Guinzaglio» ist die «area di svago di Pian Casoro» ein Ort mit Leinenpflicht. Das kann man verwechseln.
- [ ] `data/fr-ch/gemeinden/ne/neuchatel.json`: Die Karte «Annonce» spricht von «taxe», eine Karte zum Betrag fehlt. «Amicus» steht dort in Kleinbuchstaben, sonst überall «AMICUS».
- [ ] `data/gemeinden/gl/glarus.json`, Karte Leine: Wald und Waldränder stehen ohne Jahreszeit. Mit `wald` in `data/kantone/gl.json` vergleichen.
- [ ] `data/gemeinden/gr/chur.json`, Karte Leine: «in Gastwirtschaftsbetrieben» steht als Ort mit Leinenpflicht zwischen Anlagen der Stadt. Karte «Kein Zutritt»: Das Betretverbot für Wiesland steht ohne den Hinweis, ob es für Hunde oder für alle gilt.
- [ ] `data/gemeinden/gr/landquart.json`, Karte Hundetaxe: «höchstens CHF 600, also für fünf Hunde». Der Zusatz ist eine eigene Rechnung, mit der Quelle vergleichen.
- [ ] `data/gemeinden/ow/sarnen.json`, Karte Anmeldung: `wert` nennt die «Bevölkerungsdienste», der Text die «Einwohnerdienste». Karte Hundetaxe: «ab CHF 120 pro Hund» sagt nicht, wovon der höhere Betrag abhängt.
- [ ] `data/gemeinden/sz/einsiedeln.json`: Die Steuersätze stammen aus einer Broschüre ohne Datum mit Sätzen ab 2012. Die Karte sagt das, die Zahl ist trotzdem alt.
- [ ] `data/gemeinden/sz/kuessnacht.json`, Karte Hundetaxe: «Jeder weitere Hund kostet CHF 100 mehr als die Grundsteuer» lässt offen, ob das auch für Nutzhunde gilt (CHF 140) und ob es pro Hund weiter steigt. Arth, Einsiedeln und Schwyz nennen CHF 200.
- [ ] `data/gemeinden/sz/schwyz.json`, Karte «Änderungen melden»: `wert` schreibt «10 Tagen», der Text «zehn Tagen». Einsiedeln schreibt «zehn», Küssnacht «10».
- [ ] `data/gemeinden/tg/kreuzlingen.json`, Karte Anmeldung: Broschüre 10 Tage, Website 30 Tage. Die Karte sagt das offen. Bei der Nachprüfung klären.
- [ ] Schreibweisen in allen Originalfassungen vereinheitlichen: Tausender («CHF 5'000», «CHF 20 000», «CHF 5000»), «mind.» und «mindestens», «Mio.» und «Millionen», Ziffer oder Zahlwort im selben Feld. In den Tabellen der Themenseiten stehen die Kantone untereinander, dort fällt es auf.

## 5. Umbauten am Generator

Vorgaben in `CLAUDE.md` unter «Umbauten am Generator».

- [x] Themenseiten, 2026-11-17
- [x] Mehrsprachigkeit (Französisch und Italienisch), 2026-11-18
- [x] Darstellung überarbeiten: Startseite ohne Vergleichstabelle, Gemeindeverzeichnis, Thementafeln, Karten in zwei Spalten (18.11.2026)
- [x] Übersetzungen im Generator: Kennzeichnung, Prüfsumme, Zahlenvergleich, `--fehlend`. Probe: Kanton und Stadt Zürich auf Französisch und Italienisch (18.11.2026)
- [x] Bund, Themenseiten und Fehlerseite in drei Sprachen (18.11.2026)
- [ ] Link-Prüfung: alle Adressen aus den Quellendateien mit einem echten Abruf prüfen (HTTP-Status), nicht mit WebFetch. Anlass: Am 18.11.2026 meldete das Veterinäramt Thurgau einen toten Link (Error 404), den WebFetch noch auslieferte. Der Lauf erkennt tote Links also nicht. Kein Sonderlauf: Claude baut das in einer Sitzung mit Joss.

## 6. Ideen für später

Aus dem Vergleich mit anderen Seiten. Erst angehen, wenn alle Kantone erfasst sind, jeweils als Sonderlauf.

- Rassen-Check: Rasse wählen und sehen, in welchen Kantonen sie verboten oder bewilligungspflichtig ist. Braucht die Rasselisten als eigene Datenfelder.
- Kantone direkt vergleichen: zwei Kantone wählen und nur die Unterschiede sehen (für den Umzug).
- Checkliste «Neu mit Hund» pro Kanton zum Abhaken und Drucken, erzeugt aus den Karten.
- «Standort verwenden» in der Ortssuche. Die Koordinaten stehen im Ortschaftenverzeichnis.
- Fragen als Überschriften («Braucht es im Kanton Zürich einen Hundekurs?»), sobald die Suchdaten zeigen, wie gefragt wird.

## 7. Braucht Zugriff, den der Lauf nicht hat

- Ortsverzeichnis `data/orte.json` auf den aktuellen Stand bringen. Es braucht die aktuelle CSV-Datei «Amtliches Ortschaftenverzeichnis» von swisstopo, dann `python3 tools/orte.py DATEI "Stand"`. Der Lauf kann die Datei nicht abrufen. Offen, bis Joss sie liefert oder Claude sie in einer Sitzung mit Browser holt.
- Suchdaten aus der Google Search Console auswerten: macht Claude in einer Sitzung über den Browser von Joss.
- Postfach kontakt@gassi-kompass.ch lesen und beantworten: macht Joss, oder Claude in einer Sitzung über den Browser von Joss. Der Lauf hat keinen Zugriff darauf.

## 8. Später, nur nach Freigabe von Joss

- Englisch und weitere Sprachen
- Anzeigen und Affiliate-Links
- Impressum und Datenschutzerklärung
- Anschreiben an Behörden, Vereine und Medien. Erste Runde am 18.11.2026 von Joss verschickt: Veterinärdienste SO, TG, BL, JU, TI. Antwort TG am 18.11.2026, eingearbeitet (siehe `CHANGELOG.md`). Für die nächste Runde: zuerst je Kanton klären, wer zuständig ist (im Thurgau die Gemeinden, das Veterinäramt nur für die Bewilligungen), und die Links der Kantonsseite mit einem echten Abruf prüfen.
