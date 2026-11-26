# Ausbauliste

Erledigtes abhaken und das Datum dahinter schreiben. Was sich nicht belegen lässt, mit Datum und Grund als «zurückgestellt» markieren und weitergehen.

## Reihenfolge

Ziel: jede Seite auf Deutsch, Französisch und Italienisch, dazu 60 Gemeinden. Für jeden Lauf gilt die erste Zeile, die zutrifft:

1. **Sonderlauf.** Ist in Abschnitt 5 ein Punkt mit dem Vermerk «fällig» offen, macht der Lauf nur den obersten davon.
2. **Übersetzungen.** Fehlen laut `python3 build.py --fehlend` mehr als 12 Übersetzungen, macht der Lauf nur Übersetzungen, höchstens 12 Dateien.
3. **Neuer Kanton.** Der oberste offene Kanton aus Abschnitt 1. Dazu seine grösste Gemeinde oder sein Hauptort. Ist Abschnitt 1 erledigt und die Mehrsprachigkeit in Abschnitt 5 abgehakt: der oberste offene Eintrag aus Abschnitt 2.
4. **Gemeinden.** Ist kein Kanton möglich, bis zu 4 Gemeinden aus Abschnitt 3.

In jedem Lauf ausser den Sonderläufen zusätzlich höchstens eine Lücke aus Abschnitt 4. Die «Toten Links» dort zählen nicht als Lücke: Sie gehören zum Nachprüfen, höchstens vier pro Lauf.

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
- [x] Wettingen (AG), 2026-11-19
- [x] Baden (AG), 2026-11-19
- [ ] Wohlen (AG): zurückgestellt am 2026-11-19. Nur zwei lokale Angaben sicher belegt (Anmeldung bei der Regionalpolizei Wohlen ab 3 Monaten, Hundetaxe im Mai fällig). Die Leinenpflicht auf den Wegen beidseitig entlang der Bünz ist laut Mitteilung der Gemeinde vom 18. Juni 2025 rechtskräftig beschlossen, die Mitteilung nennt aber weder Abschnitt noch Beginn. Nächster Versuch: PDF der Mitteilung (wohlen.ch/aktuellesinformationen/2489401) und Polizeireglement von 2016 (wohlen.ch/_doc/1231864, am 19.11.2026 nicht abrufbar).
- [ ] Rheinfelden (AG): zurückgestellt am 2026-11-19. Nur zwei lokale Angaben belegt (Anmeldung beim Stadtbüro innert 10 Tagen mit Kopie des Heimtierausweises, Rechnung der Hundetaxe im Mai durch die Finanzverwaltung). Ein Polizeireglement mit Leinenorten oder Verboten war in zwei Suchen nicht zu finden. Nächster Versuch: Rechtssammlung rheinfelden.tlex.ch (braucht einen Browser) und Regionalpolizei Unteres Fricktal.
- [ ] Reinach (BL): zurückgestellt am 2026-11-19. Lesbar war nur eine Fassung des Polizeireglements vom 23. November 2015 ohne Datum der Genehmigung und des Inkrafttretens (§ 39 bis 46 zu Hunden, Bussenliste). Ob sie heute gilt, ist offen. Die Seite «Hund anmelden oder abmelden» lieferte keinen Inhalt. Nächster Versuch: geltende Fassung auf reinach-bl.tlex.ch (braucht einen Browser), Hundegebühr in der Polizeiverordnung.
- [x] Muttenz (BL), 2026-11-19
- [ ] Pratteln (BL): zurückgestellt am 2026-11-20. Belegt sind nur Anmeldung (Schalter der Einwohnerdienste, innert 14 Tagen, Hunde ab 4 Monaten, Unterlagen laut Merkblatt) und eine Gebühr von CHF 120 aus dem Merkblatt der Gemeindepolizei vom 17. September 2022. Die Gebührenverordnung (2.4.1) wurde seither mehrmals neu gefasst, die nächste Fassung gilt ab 1. Januar 2027: Der Betrag ist deshalb nicht sicher. Das Reglement über die Hundehaltung (4.1.3, in Kraft seit 1. April 2006, pratteln.ch/_rte/information/2071360) mit Leinenorten und Zutrittsverboten und das PDF der Gebührenverordnung (pratteln.ch/_doc/7164151) gab das Abrufwerkzeug nicht frei. Das Polizeireglement 4.1.1 gilt seit 1. Juli 2026 (pratteln.ch/_rte/information/2893861, nicht gelesen), die Fassung unter _docn/1330941 ist nur der Entwurf.
- [ ] Binningen (BL): zurückgestellt am 2026-11-20. Keine lokale Angabe sicher belegt. Lesbar waren das Polizeireglement vom 29. Juni 2015 (Fassung 1. August 2022, nur § 9 mit Verweis auf das Hundereglement vom 26. Mai 1997) und ein interner Bussenkatalog von 2016. Die Seite «Hunde» ist für das Abrufwerkzeug gesperrt (robots), das Hundehaltungsreglement (binningen.ch/public/upload/assets/5962/Hundehaltungsreglement.pdf) und die Ordnungsbussenliste (assets/9443) gab es nicht frei.
- [x] Liestal (BL), 2026-11-20
- [x] Kreuzlingen (TG), 2026-11-17
- [x] Arbon (TG), 2026-11-17
- [ ] Amriswil (TG): zurückgestellt am 2026-11-17. Nur die Meldestelle belegt (Hundekontrollstelle der Einwohnerdienste). Die Seite der Stadt nennt weder Steuerbetrag noch Orte, die Mitteilung zu den Hundesteuer-Rechnungen war nicht abrufbar.
- [ ] Weinfelden (TG): zurückgestellt am 2026-11-17. weinfelden.ch lässt den Abruf nicht zu (robots), keine andere amtliche Quelle gefunden.
- [ ] Romanshorn (TG): zurückgestellt am 2026-11-17. Das Merkblatt Hundehaltung der Stadt trägt kein Datum und ist beim Kurs veraltet (Stand vor April 2024). Es nennt Steuer CHF 100 und CHF 162.50, Leinenpflicht im Seepark, auf Schlosswiese und Surfwiese, Hundezone im Seepark, Verbot in der Holzensteiner Badi. Die aktuellen Seiten (Hundekontrolle, Hundewiese) lassen den Abruf nicht zu. Neu ansetzen, sobald eine datierte Quelle lesbar ist.
- [ ] Solothurn (SO): zurückgestellt am 2026-11-20. Belegt ist nur die Anmeldung bei der Stadtpolizei (Formular, Kopie des Impfausweises, per E-Mail). Der Online-Schalter nennt «CHF 135.00», ohne zu sagen, wofür. Die Polizeiordnung vom 30. Juni 1992 (Fassung 1. September 2024) enthält nichts zu Hunden. Die Rechtssammlung (stadt-solothurn.ch/gzpolizei/kapitel/15) war nicht abrufbar. Nächster Versuch: Gebührentarif und Friedhofreglement.
- [ ] Grenchen (SO): zurückgestellt am 2026-11-21. Belegt ist nur die Anmeldung (Formular «Registrierung neue Hundehalter/in» an die Einwohnerkontrolle, Bahnhofstrasse 23, oder per E-Mail). Die Leinenpflicht in der Witi-Schutzzone mit der Ausnahme im Gebiet Breitholz steht in den kantonalen Zonenvorschriften (RRB von 1994 und 2005) und zählt nicht als lokale Angabe. Das «612 Reglement Hundesteuer» (grenchen.ch/_rtr/publikation_11966), der Onlinedienst «Hundekontrolle / Hundehalter» (_rtr/onlinedienst_36623) und die Lebenslage Hundesteuer (_rtr/thema_5041) gab das Abrufwerkzeug nicht frei. Nächster Versuch: diese drei Adressen über eine Suche erreichen.
- [x] Zuchwil (SO), 2026-11-21
- [ ] Biberist (SO): zurückgestellt am 2026-11-21. Sicher belegt ist nur die Seite «Hundesteuer» (ohne Datum): CHF 135 pro Jahr, Hundejahr 1. April bis 31. März, Mahngebühr CHF 50, Befreiungen. Ältere amtliche Angaben weichen ab (Gebührentarif vom 1. September 2020: CHF 100 ohne Marke, Mitteilung vom 31. März 2022: CHF 140). Das Hundeverbot auf dem Friedhof (§ 15 Abs. 4, Reglement R 512 vom 5. Dezember 2024, in Kraft ab 1. Januar 2025) steht nur in der Vorlage für die Gemeindeversammlung, das Datum der Genehmigung ist dort leer. Formular «An- und Abmeldung von Hunden» und «Informationen_ePetCard_2026.pdf» gab das Abrufwerkzeug nicht frei. Nächster Versuch: genehmigte Fassung von R 512 im Verzeichnis biberist.ch/de/verwaltung/dokumente/index.php, dazu das Formular.
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
- [x] Domat/Ems (GR), 2026-11-21
- [ ] St. Moritz (GR): zurückgestellt am 2026-11-21. Lesbar war nur die Fassung des Polizeigesetzes von 2017 (Art. 14: Leine in Verwaltungsgebäuden, auf Schul- und Kindergartenarealen, Kinderspielplätzen, Sportanlagen, Friedhöfen und in Parkanlagen, Kot, Meldung innert 14 Tagen bei der Gemeindepolizei, Busse Fr. 50 bis 5000, Hundesteuer CHF 150 im Anhang). Die Gesetzessammlung verlinkt eine Teilrevision vom 26. November 2025, in Kraft seit 1. Februar 2026, die nicht abrufbar war. Ohne die geltende Fassung nichts veröffentlicht.
- [ ] Ilanz/Glion (GR)
- [x] Riehen (BS), 2026-11-21
- [ ] Bettingen (BS): zurückgestellt am 2026-11-26. Nur zwei lokale Angaben belegt (Hundesteuer CHF 120, Leinenpflicht am Mattenwegli samt Vorplatz des Schwimmbadeingangs laut Reglement SG 365.150 § 5). Die Liste der Hundeverbote für Bettingen ist seit 2024 aufgehoben, auf der Website der Gemeinde war nichts zu Hunden zu finden. Beide Angaben stehen auf der Kantonsseite.
- [ ] Rapperswil-Jona (SG): zurückgestellt am 2026-11-21. Nur zwei lokale Angaben belegt (Hundesteuer Fr. 140 pro Hund, fällig zu Beginn des Kalenderjahres, Meldung bei der Stadt). Der Stadtrat plante laut Mitteilung vom 24. Oktober 2025 eine Leinenpflicht im Wald und am Waldrand vom 1. April bis 31. Juli per Nachtrag zum Polizeireglement, Inkrafttreten geplant auf 1. April 2026: Ob er gilt, ist nicht belegt. Nächster Versuch: Inkrafttreten belegen, Polizeireglement auf rapperswil-jona.tlex.ch (PDF-Adressen der Form /api/de/versions/<Nr>/pdf_file).
- [ ] Wil (SG): zurückgestellt am 2026-11-21. Belegt ist nur eine Mitteilung vom 24. Mai 2019: Betretungsverbot für Hunde auf Spielplätzen und Friedhöfen ab 3. Juni 2019 und Leinenzwang in öffentlichen Grün- und Parkanlagen, das Urteil des Bundesgerichts stand damals aus. Betrag der Hundesteuer und geltendes Polizeireglement nicht abrufbar. Nächster Versuch: stadtwil.ch/gkfinanzen/kapitel/147 und das Polizeireglement.
- [x] Gossau (SG), 2026-11-21
- [ ] Uzwil (SG): zurückgestellt am 2026-11-21. Belegt sind nur die Taxe (120 Franken pro Hund ab 2020) und die Meldung bei der Réception mit Chip-Nummer. Die Erlasse liegen auf publikationen.sg.ch, das den Abruf sperrt (robots).
- [x] Winterthur (ZH), 2026-11-18
- [ ] Biel/Bienne (BE), Adresse `biel-bienne`, deutsch und französisch. Französisch zurückgestellt am 2026-11-18: keine amtliche Quelle gefunden.
- [x] Thun (BE), 2026-11-21
- [x] Köniz (BE), 2026-11-21
- [x] Uster (ZH), 2026-11-18
- [x] Emmen (LU), 2026-11-18
- [x] Dübendorf (ZH), 2026-11-18
- [ ] Kriens (LU): zurückgestellt am 2026-11-18. Die Website der Stadt ist für das Abrufwerkzeug gesperrt (robots). Nächster Versuch: Rechtssammlung der Stadt als PDF oder amtliche Dokumente unter stadt-kriens.ch/public/upload/.
- [x] Dietikon (ZH), 2026-11-18
- [x] Wetzikon (ZH), 2026-11-18
- [x] Wädenswil (ZH), 2026-11-18
- [x] Burgdorf (BE), 2026-11-21
- [ ] Langenthal (BE): zurückgestellt am 2026-11-21. Taxe (Fr. 120, Stichtag 1. August, älter als sechs Monate) und Anmeldung beim Polizeiinspektorat lagen nur als Zusammenfassung des Abrufwerkzeugs vor, kein Wortlaut. Die Verordnung über die Hundetaxe (4.6.1 V, langenthal.ch/_doc/2211641), die Themenseite «Hunde» (langenthal.ch/bewilligungengastgewerbe/49928), Ortspolizei-Reglement und Friedhofreglement waren nicht abrufbar.
- [ ] Horgen (ZH): zurückgestellt am 2026-11-18. Nur zwei lokale Angaben belegt (Gebührentarif ab 2022: Ersthunde CHF 130, verspätetes Anmelden CHF 40). Die Seiten «Hunde» und «Hundekontrolle: Anmeldung» gaben zweimal einen Serverfehler, von der Polizeiverordnung war nur das Inhaltsverzeichnis lesbar (Art. 11 Tierhaltung).
- [x] Bülach (ZH), 2026-11-18
- [ ] Kloten (ZH): zurückgestellt am 2026-11-18. Nur zwei belegte Angaben, der Flyer für Hundebesitzer war nicht abrufbar. Nächster Versuch: Flyer und Polizeiverordnung abrufen. Versuch vom 2026-11-21: weiterhin nur zwei sichere Angaben (Hundeabgabe CHF 200 pro Hund, An- und Abmeldung bei der Abteilung Sicherheit, Mutationen innert 10 Tagen). Die Polizeiverordnung von 2004 (Leine in Wäldern, Anlagen, Lokalen und an verkehrsreichen Strassen) wird laut Gemeinderatsbeschluss vom 2. April 2024 aufgehoben, das Inkrafttreten der neuen ist nicht belegt (Stadtratsbeschluss 319-2024, kloten.ch/_doc/5437963).
- [x] Horw (LU), 2026-11-18
- [x] Ebikon (LU), 2026-11-18
- [x] Steffisburg (BE), 2026-11-21
- [x] Ostermundigen (BE), 2026-11-21
- [x] Opfikon (ZH), 2026-11-18
- [x] Thalwil (ZH), 2026-11-18
- [x] Adliswil (ZH), 2026-11-18
- [x] Sursee (LU), 2026-11-18
- [ ] Muri bei Bern (BE)
- [x] Regensdorf (ZH), 2026-11-18
- [x] Illnau-Effretikon (ZH), 2026-11-18
- [x] Schlieren (ZH), 2026-11-21 (Hundeabgabe, Anmeldung, Hundeverbot auf dem Friedhof)
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
- [ ] Baar (ZG): zurückgestellt am 2026-11-21. Nur zwei lokale Angaben belegt (Hundesteuer CHF 120 pro kontrollpflichtigen Hund, CHF 40 für Wachhunde auf Landwirtschaftsbetrieben, Meldung bei den Einwohnerdiensten). Hundereglement von 1980 (baar.ch/_doc/2139605) und Merkblatt zur Hundehaltung (baar.ch/_doc/5047555) nicht abrufbar, baar.tlex.ch liefert keinen Text.
- [ ] Cham (ZG): zurückgestellt am 2026-11-21. Sicher belegt ist nur die Erstregistrierung bei den Einwohnerdiensten im Mandelhof. Betrag (CHF 100) und Leinenregeln stehen nur als Satzteile im Protokoll der Gemeindeversammlung vom 4. Dezember 2017. Nächster Versuch: Merkblatt Hunde vom 9. Oktober 2026 (cham.ch/_doc/7278211) und Hundereglement auf cham.tlex.ch.
- [x] Risch (ZG), 2026-11-25. Hundereglement unter zg.ch/behoerden/gemeinden/risch-rotkreuz/…/101-hundereglement.
- [x] Steinhausen (ZG), 2026-11-25. Nicht übernommen: § 9 des Reglements von 1976 (Leine im Wald, am Waldrand und nachts), weil das kantonale Recht den Wald seit 2024 anders regelt. Reglement über das Halten von Hunden und Merkblatt Hundesteuer 2025 auf zg.ch.
- [ ] Stans (NW): zurückgestellt am 2026-11-18. Hundesteuer und Hundekontrolle sind in Nidwalden kantonal, auf stans.ch keine lokale Angabe zu Hunden gefunden.
- [ ] Hergiswil (NW). Hinweis für alle Nidwaldner Gemeinden: vorher prüfen, ob es überhaupt Gemeinderegeln zu Hunden gibt. Sonst alle zurückstellen.
- [ ] Buochs (NW)
- [ ] Ennetbürgen (NW)
- [ ] Stansstad (NW)
- [x] Glarus (GL), 2026-11-18
- [ ] Glarus Nord (GL): zurückgestellt am 2026-11-21. Alle Abrufe auf glarus-nord.ch gaben einen Serverfehler. Nächster Versuch: Seite Hundewesen (glarus-nord.ch/online-schalter/einwohner-und-bestattungsamt/hundewesen.html/2603).
- [ ] Glarus Süd (GL)
- [x] Schaffhausen (SH), 2026-11-18
- [x] Neuhausen am Rheinfall (SH), 2026-11-21
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
- [x] La Chaux-de-Fonds (NE), französisch, 2026-11-25. Ohne Anmeldestelle: Die Seite «Impôts, taxes, amendes» der Stadt lieferte nur eine Fehlerseite. Das Règlement de police liegt im Stand 1. Juni 2015 vor: bei der nächsten Nachprüfung eine neuere Fassung suchen.
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
- [ ] Bellinzona (TI), italienisch: zurückgestellt am 2026-11-25. Nur zwei lokale Angaben belegt (Meldung innert 10 Tagen an die Polizia comunale, vicolo Muggiasca 1a, Formular Ausgabe September 2026. Tierverbot auf den Friedhöfen, Regolamento dei cimiteri Art. 11, vom Kanton genehmigt am 28. Oktober 2025). Die «Ordinanza municipale sulla custodia dei cani» ist auf bellinzona.ch erwähnt, aber nicht verlinkt, zwei Suchen fanden sie nicht. Betrag der Taxe und Dog Parks nicht belegt. Die Seite «Campagna cani» war nicht abrufbar.
- [ ] Locarno (TI), italienisch
- [ ] Mendrisio (TI), italienisch
- [ ] Chiasso (TI), italienisch

## 4. Lücken in bestehenden Seiten

### Tote Links (Link-Prüfung vom 18.11.2026, zuletzt 20.11.2026)

Zuerst erledigen, höchstens vier pro Lauf. Vorgehen in `CLAUDE.md` unter «Link-Prüfung». Antwort 404 beim echten Abruf:

- [x] `ai_vob` (Kanton Appenzell Innerrhoden), 2026-11-20: ersetzt durch den Anhang 1 der VOB im Stand 31. März 2025 (`ai.clex.ch/api/annex_document_dictionaries/2903`). Beträge unverändert (CHF 50 und CHF 100). Die Adresse ist wieder ein Dateipfad der Gesetzessammlung: Die nächste Link-Prüfung zeigt, ob sie hält.
- [x] `ar_brosch` (Kanton Appenzell Ausserrhoden), 2026-11-19: ersetzt durch die Broschüre Version 02/2025 (`…/Informationsbroschuere_zur_Hundehaltung_AR_250224_.pdf`)
- [ ] `be_oce_fr` (Kanton Bern, französische Fassung): `belex.sites.be.ch/frontend/change_document_file_dictionaries/3016` Lauf vom 19.11.2026: erster Lauf ohne Ersatz (am 20.11.2026 nicht bearbeitet, Obergrenze vier pro Lauf, weiterhin 404). Lauf vom 21.11.2026: zweiter Lauf ohne Ersatz. belex.sites.be.ch liefert dem Abrufwerkzeug nur eine leere Rahmenseite (texts_of_law/916.51/versions/1290), die Seite «Loi du canton de Berne sur les chiens» des Veterinäramts (Stand 17. März 2025) nennt weder AMICUS noch die Taxe. Sie verlinkt die Loi sur les chiens unter belex.sites.be.ch/data/916.31/fr und die OPAC unter belex.sites.be.ch/data/916.812/fr: beim nächsten Mal diese beiden abrufen. Nach dem dritten Lauf ohne Ersatz kommt die Quelle in den Bericht. Die Suche fand nur die alte Adresse. Die Broschüre «Loi sur les chiens» des Veterinäramts (weu.be.ch, Juli 2022) belegt AMICUS, importierte Hunde und die Registrierung der Haltenden durch die Gemeinde, aber nicht die Hundetaxe der Gemeinden. Nächster Versuch: RSB 916.51 auf belex.sites.be.ch (texts_of_law/916.51) oder die Loi sur les chiens (RSB 916.31) für die Taxe. Lauf vom 25.11.2026: dritter Lauf ohne Ersatz, steht im Bericht. belex.sites.be.ch/data/916.31/fr gab das Abrufwerkzeug nicht frei, belex.sites.be.ch/frontend/versions/2199?locale=fr liefert nur eine leere Rahmenseite, mm.directories.be.ch/files/6325/17056.pdf ist der Vernehmlassungsentwurf von 2011 und taugt nicht als Quelle. Joss ist gebeten, die geltende Adresse im Browser zu öffnen.
- [x] `ne_laisse` (Kanton Neuenburg), 2026-11-19: Der Flyer war nicht mehr zu finden. Ersetzt durch die Mitteilung des DDTE vom 12. April 2024 (`ne.ch/medias/Pages/Chiens-en-laisse-.aspx`, nachgeführt am 9. März 2026)
- [x] `zg_steinhausen_steuer` (Kanton Zug), 2026-11-20: Merkblatt Hundesteuer 2025 ersetzt durch das Reglement über das Halten von Hunden der Gemeinde Steinhausen (Nr. 52.1, § 11, `…/copy_of_dokumente/regl-halten-von-hunden.pdf/download`). Die Adresse liegt im selben Ordner wie die tote: Die nächste Link-Prüfung zeigt, ob sie hält.
- [x] `zh_winterthur_merkblatt` (Winterthur), 2026-11-21: ersetzt durch die Seite «Hund an- oder abmelden» der Einwohnerkontrolle (neuer Schlüssel `zh_winterthur_anmeldung`). Das neue Merkblatt «Hundewesen Gebühren» (stadt.winterthur.ch/download/media/657/…, Dateiname mit 20250603) war nicht abrufbar und ist ein Dateipfad, darum die Seite.
- [x] `ne_scav` (Kanton Neuenburg), 2026-11-20: Adresse ersetzt durch die Seite «S'occuper d'animaux» des SCAV, auf die die alte Adresse führte (`ne.ch/themes/vie-quotidienne-et-famille/animaux/soccuper-danimaux`).
- [x] `ur_silenen_hhv` (Silenen), 2026-11-21: Der Verdacht vom 20.11.2026 hat sich in zwei Durchgängen (20.11. um 11:30 Uhr, 21.11.) nicht wiederholt. Nichts geändert.

Unklar, nur beobachten. Durchgang vom 18.11.2026: `bl_wald` (baselland.ch, Antwort 403), `zh_wetzikon_hundewesen`, `zh_wetzikon_pvo` und `zh_wetzikon_tarif` (wetzikon.ch, Zeitüberschreitung). Durchgang vom 19.11.2026: `bl_wald` (403, zum zweiten Mal), `tg_vet_rassen` (Zeitüberschreitung, zum ersten Mal). Die drei Quellen von Wetzikon waren in Ordnung. Durchgang vom 20.11.2026: `bl_wald` (403, zum dritten Mal hintereinander, steht im Bericht vom 20.11.2026). `tg_vet_rassen` war in Ordnung. Durchgang vom 21.11.2026: `bl_wald` (403, zum fünften Mal, Joss ist seit dem 20.11.2026 gebeten, die Adresse im Browser anzuklicken), Joss hat die Adresse am 21.11.2026 auf der Seite angeklickt: Sie funktioniert im Browser. `bl_wald` gilt damit als in Ordnung, ein 403 der Link-Prüfung kommt bei dieser Quelle nicht mehr in den Bericht. Dazu zum ersten Mal mit Zeitüberschreitung `lu_stadt`, `ow_leine_2022` und `zh_opfikon_hundeabgabe`. Durchgang vom 25.11.2026: `bl_wald` (403, gilt als in Ordnung), `sz_einsiedeln_formular` (503, zum ersten Mal). Die drei vom 21.11. waren in Ordnung.

### Lücken

- [ ] Stadt Zürich: Betrag der Hundeabgabe belegen und als Karte «Hundeabgabe» ergänzen
- [ ] Stadt Zürich: Freilaufzonen aus dem städtischen Datensatz «Hundezonen» namentlich aufführen
- [ ] Stadt Bern: Betrag der Hundetaxe belegen
- [ ] Stadt Bern: Quelle «Gemeinderat Bern 2019» (Tierpark, Kinderzoo) durch eine aktuelle amtliche Quelle ersetzen
- [ ] Stadt Luzern: Bussen mit einer Quelle nach 2022 belegen
- [ ] Kanton Bern: «kein Kursobligatorium» mit einer Quelle des Kantons statt der Gemeinde Büren belegen
- [ ] Kanton Bern: Entscheid des Grossen Rats von 2023 zur Wald-Leinenpflicht mit einer amtlichen Quelle (Ratsprotokoll) belegen
- [ ] Kanton Zürich, vordringlich: Einzelheiten der Theorieprüfung (Zahl der Fragen, Dauer, Grenze zum Bestehen, Wiederholung) aus dem Prüfungsreglement und den Seiten des Veterinäramts belegen und in der Karte «Kurs» ergänzen. Anstoss: eine Zuschrift vom 26.11.2026 (keine Quelle). Laut Suchdaten vom 26.11.2026 wird nach dem obligatorischen Hundekurs in Zürich gesucht, und die Themenseite Kurs wird schon angeklickt.
- [ ] Bund: Leinenpflicht in den eidgenössischen Jagdbanngebieten auf `/schweiz/` in allen drei Originalfassungen ergänzen (Seiten des Bundesamts für Umwelt in der jeweiligen Sprache, Quellen `ch_bafu_jagdbann` und `ch_bafu_districts`, die italienische kommt neu dazu). Wenn möglich die Verordnung (VEJ, SR 922.31) in der geltenden Fassung lesen: fedlex war am 26.11.2026 nicht abrufbar. Danach die Kantone mit solchen Gebieten nachziehen. Bisher steht es bei GL und VS.
- [ ] Kanton Wallis: Regeln zu Hunden aus dem Bereich der Dienststelle für Jagd, Fischerei und Wildtiere (kantonale Banngebiete, Wildruhezonen) und der Naturpärke belegen. Hinweis des Veterinäramts vom 26.11.2026. Das Ausführungsreglement zum Jagdgesetz (SGS 922.100) enthält nichts dazu, das Jagdgesetz (SGS 922.1) war nicht lesbar.
- [ ] Kanton Freiburg: Das Amt schreibt am 26.11.2026, die Haltung eines Hundes des Typs Pitbull könne bewilligt werden, wenn er nachweislich Umzugsgut ist. In Gesetz, Reglement und auf den Seiten des Amts steht das nicht. Die Seite verweist darum für den Zuzug an das Amt. Ergänzen, sobald eine veröffentlichte Grundlage vorliegt. Die Rückfrage an das Amt geht nur nach dem Ja von Joss raus.
- [ ] Riehen: Orte mit Hundeverbot (§ 4 Abs. 1 lit. b) und mit Leinenpflicht (§ 5 Abs. 1 lit. b) aus dem Reglement betreffend das Halten von Hunden (SG 365.150, Quelle `bs_regl`) als Karten «Kein Zutritt» und «Leine» ergänzen.
- [ ] Stadt Basel: Die Karten «Kein Zutritt» und «Leine» stützen sich auf die Liste des Gesundheitsdepartements (`bs_zonen`). Beim Nachprüfen mit § 4 und § 5 des Reglements (`bs_regl`, Stand 21. März 2024) abgleichen.
- [ ] Kanton Genf: Die Seiten von ge.ch nennen die Stelle noch «SCAV». Beim Nachprüfen Namen (laut ROAC seit Oktober 2026 Direction de la sécurité sanitaire et de la santé environnementale) und Adresse für das Ausnahmegesuch abgleichen und den Zusatz «anciennement SCAV» streichen, sobald ge.ch umgestellt ist.

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

- [ ] Kanton Appenzell Ausserrhoden: Seite des Veterinäramts (ar.ch/hunde) abrufen: heutige Meldestelle und Meldeweg, Abgleich mit `leine`. Dazu aus der Broschüre 02/2025 (gelesen am 19.11.2026): Sie nennt für Änderungen eine Meldefrist von 10 Tagen, die Seite nennt nach dem Hundegesetz 14 Tage. Am Wortlaut von Gesetz und Broschüre klären. Die Broschüre empfiehlt zudem, sich vor dem ersten Hund «idealerweise 1 Woche im Voraus» beim Veterinäramt zu melden (telefonisch, schriftlich oder online).
- [ ] Wettingen: Anmeldestelle der Gemeinde für Hunde belegen. Das Polizeireglement 2026 liegt als Quelle auf der Website von Neuenhof: Adresse auf wettingen.ch suchen und ersetzen (dort stand am 19.11.2026 noch die Fassung von 2013).
- [ ] Stadt Baden: Anmeldestelle und Rechnung der Hundetaxe belegen, Freilaufflächen suchen.
- [ ] Muttenz: Reglement über das Halten von Hunden (Nr. 11.600 vom 29. Oktober 1996, muttenz.ch/_doc/5627326) und Hundegebührenverordnung (muttenz.ch/reglemente/5795) lesen, am 19.11.2026 nicht abrufbar. Danach Orte mit Leinenpflicht und Zutrittsverbot, Betrag der Hundegebühr und Meldefrist ergänzen.
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
- [ ] Kanton Neuenburg, Karte Annonce: Der Satz «Les frais d'identification et d'enregistrement sont à votre charge» steht nicht auf der Seite «S'occuper d'animaux» des SCAV (gelesen am 20.11.2026 als Zusammenfassung des Abrufwerkzeugs). Mit der LChiens belegen, sonst weglassen. Die LChiens gab das Abrufwerkzeug am 20.11.2026 nicht frei. Die Seite nennt zudem die Kosten des Kurses (vom Anbieter frei festgelegt, Schätzung CHF 300 bis 400): nach wörtlicher Lektüre ergänzen.
- [ ] Kanton Appenzell Innerrhoden: Der Anhang 1 der VOB (Stand 31. März 2025) nennt neu CHF 150 für einen Verstoss gegen die Leinenpflicht für Hunde nach Art. 5 Abs. 1 der Wildruheverordnung (WRV, GS 922.012). Die WRV lesen und die Leinenpflicht in Wildruhegebieten samt Busse bei `wald` oder `leine` ergänzen.
- [ ] Liestal: Ordnungsbussen aus dem Anhang des Polizeireglements wörtlich lesen (laut Zusammenfassung des Abrufwerkzeugs CHF 100 für Leine, Zutrittsverbot und Kot, nicht übernommen). Das Formular nennt ein «Reglement über die Hundeanmeldung (ESL 324.1)» und «Hofhund (gebührenfrei)»: klären. Vom Stadtrat signalisierte Leinenorte und Zutrittsverbote sowie Hundewiesen suchen.
- [ ] Kanton Neuenburg: Wortlaut der LChiens (Art. 4, 5, 7, 8, 14, 17) und der LFS am PDF gegenprüfen. Kursreglement des Staatsrats und eigene Seite des SCAV zu Hunden suchen.
- [ ] Ville de Neuchâtel: Betrag der Hundetaxe, Namen der Freilaufzonen, geltende Fassung des Polizeireglements und Liste der Strände im Faltblatt gegenprüfen.
- [ ] Neun Gemeinden vom 2026-11-21 (Thun, Köniz, Steffisburg, Ostermundigen, Burgdorf, Schlieren, Neuhausen am Rheinfall, Domat/Ems, Gossau): Alle Angaben stammen aus Zitaten des Abrufwerkzeugs, nicht aus dem Rohtext. Beim Nachprüfen am Dokument gegenlesen.
- [ ] Thun: Verordnung über die Benützung des Seeuferbereichs (733.10, in Kraft seit 1. April 2026) und Situationsplan lesen, Leinenorte genau fassen. Anmeldestelle (Polizeiinspektorat, Hofstettenstrasse 14) im Wortlaut belegen. Die Themenseite nennt für die Taxe noch «Art. 25b», das geltende Reglement Art. 42.
- [ ] Köniz: Betrag der Hundetaxe (Reglement 916.31 und Verordnung 916.311), Friedhof, Schwimmbad Weiermatt, Liebefeld Park und Schlosspark belegen. Die Quellen liegen unter /public/upload/assets/, solche Adressen sterben oft.
- [ ] Steffisburg: Verordnung zum Gebührenreglement (156.01.01) als Grundlage für CHF 100 und CHF 20 lesen, Friedhofreglement und Verordnung über Schulareale und Sportplätze prüfen.
- [ ] Ostermundigen: Das Ortspolizeireglement von 1984 verbietet Hunden den Zutritt zu Kinderspielplätzen, die Seite der Gemeinde nennt für öffentliche Spielplätze die Leine. Die Seite zeigt das Verbot. Am Merkblatt für Hundehaltende (2020) und am Parkreglement (Nr. 230) klären, auch ob die Leinenpflicht von 22.00 bis 06.00 Uhr noch angewendet wird.
- [ ] Burgdorf: Hundereglement (burgdorf.ch/de/verwaltung/dokumente/dokumente/Hundereglement_01.pdf) und Anlagenutzungsverordnung lesen: Leinenorte, Verbote, Kot, Bussen, Befreiungen.
- [ ] Schlieren: Betrag von Fr. 170 am Gebührentarif SKR 9.11 (in Kraft seit 1. August 2026, schlieren.ch/_doc/7138921) bestätigen.
- [ ] Neuhausen am Rheinfall: Reglement über die Abgabe für das Halten von Hunden (644.101) lesen und die Beträge «ab 1. Januar 2015» bestätigen, Anmeldestelle belegen, Badeordnung und Robidog-Faltblatt lesen.
- [ ] Domat/Ems: Kommunales Polizeigesetz (SRS 5.1-1) als PDF suchen: Leine, Kot, Verbote, Bussen. Prüfen, ob der Gemeindevorstand die Ansätze von Fr. 90 und Fr. 210 der Teuerung angepasst hat.
- [ ] Gossau: Polizeireglement (stadtgossau.ch/_doc/1105087) mit Nachträgen lesen: Hundeartikel, Verbote, Bussen. Befreiungen und Anmeldestelle (Einwohneramt) im Wortlaut belegen.
- [ ] Riehen: Reglement Wildtierschutz Riehen (Gemeinderat, 27. Februar 2024) und den Hundeplan des Landschaftsparks Wiese (landschaftsparkwiese.info) im Wortlaut lesen. Danach ergänzen, falls belegt: was «tagsüber» heisst, Bussen, Wegegebot in den Naturschutzgebieten Autal und Weilmatten (die Seite der Gemeinde nennt sie neben Entenweiher und Eisweiher, wörtlich gelesen sind nur diese zwei).
- [ ] Zuchwil: Rechtsgrundlage und Stand der Hundesteuer von CHF 65 (die Seite trägt kein Datum, das Steuerreglement regelt die Hundesteuer nicht), Meldealter, Frist und Anmeldestelle belegen. Polizeireglement auf Leinenorte und Verbote prüfen.
- [ ] Winterthur: Die Seite der Stadt nennt nur noch CHF 190 Hundesteuer im Jahr, ohne Aufteilung in Gemeindeabgabe und Kantonsbeitrag. Aufteilung am Merkblatt «Hundewesen Gebühren» belegen, falls sie wieder auf die Seite soll. Meldegebühr bei Halterwechsel klären (die Seite nennt nur die «erstmalige Meldegebühr pro Hund»).
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
- [ ] Waadt und Genf (Neuenburg erledigt am 2026-11-19: «du 15.4. au 30.6.»), ursprünglich Waadt, Genf und Neuenburg französisch, `vergleich.wald`: Schreibweise «1.4 au 15.7» an «du 1.4. au 15.7.» angleichen. Danach sind die Übersetzungen veraltet und im selben Lauf nachzuführen (aufgefallen 18.11.2026)

### Aufgefallen beim Übersetzen (Kette Übersetzungen, 18.11.2026)

Die Glieder der Kette haben jede Originalfassung Satz für Satz gelesen und notiert, was unklar oder uneinheitlich ist. Nichts davon ist ein belegter Fehler. Beim Nachprüfen der jeweiligen Datei mit der Quelle klären. Ändert sich dabei die Originalfassung, sind ihre Übersetzungen veraltet und im selben Lauf nachzuführen.

- [x] `data/fr-ch/kantone/ne.json`, Feld `vergleich.wald`: «15.4 au 30.6» ohne Punkt nach dem Monat, wie schon bei VD und GE gemeldet. Die Übersetzungen schreiben «15.4. bis 30.6.» und «dal 15.4. al 30.6.». Erledigt am 2026-11-19.
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
- [x] Link-Prüfung: `tools/links.py` und die Action «Quellen-Links prüfen» fragen jede Adresse aus den Quellendateien mit einem echten Abruf ab (18.11.2026). Anlass: Das Veterinäramt Thurgau meldete einen toten Link (Error 404), den WebFetch noch auslieferte. Erster Durchgang: 264 Quellen, 253 in Ordnung, 6 tot, 1 Verdacht, 4 unklar. Die Liste steht in Abschnitt 4.

## 6. Ideen für später

Aus dem Vergleich mit anderen Seiten. Erst angehen, wenn alle Kantone erfasst sind, jeweils als Sonderlauf.

- Rassen-Check: Rasse wählen und sehen, in welchen Kantonen sie verboten oder bewilligungspflichtig ist. Braucht die Rasselisten als eigene Datenfelder.
- Kantone direkt vergleichen: zwei Kantone wählen und nur die Unterschiede sehen (für den Umzug).
- Checkliste «Neu mit Hund» pro Kanton zum Abhaken und Drucken, erzeugt aus den Karten.
- «Standort verwenden» in der Ortssuche. Die Koordinaten stehen im Ortschaftenverzeichnis.
- Fragen als Überschriften («Braucht es im Kanton Zürich einen Hundekurs?»), sobald die Suchdaten zeigen, wie gefragt wird. Stand 26.11.2026: Gesucht wird in Stichworten (Thema und Ort), nicht in ganzen Fragen. Vorerst nicht nötig.
- Themenseite «Reisen und Einreise mit Hund» (Heimtierpass, Mikrochip, Tollwutimpfung) in drei Sprachen, aus den Seiten des BLV. Anlass: Laut Suchdaten vom 26.11.2026 landen französische Suchanfragen zu Pass und Impfungen auf der Seite des Bundes, die das nur in einer Karte behandelt.

## 7. Braucht Zugriff, den der Lauf nicht hat

- Ortsverzeichnis `data/orte.json` auf den aktuellen Stand bringen. Es braucht die aktuelle CSV-Datei «Amtliches Ortschaftenverzeichnis» von swisstopo, dann `python3 tools/orte.py DATEI "Stand"`. Der Lauf kann die Datei nicht abrufen. Offen, bis Joss sie liefert oder Claude sie in einer Sitzung mit Browser holt.
- Suchdaten aus der Google Search Console auswerten: macht Claude in einer Sitzung über den Browser von Joss. Erste Auslesung am 26.11.2026, nächste am 15.12.2026.
- Bing Webmaster Tools: Die Seite dort eintragen (Import aus der Search Console), damit auch die Suchdaten von Bing sichtbar werden. Braucht ein Microsoft-Konto von Joss. Nicht dringend: IndexNow meldet die Seiten schon an Bing.
- Postfach kontakt@gassi-kompass.ch lesen und beantworten: macht Joss, oder Claude in einer Sitzung über den Browser von Joss. Der Lauf hat keinen Zugriff darauf.

## 8. Später, nur nach Freigabe von Joss

- Englisch und weitere Sprachen
- Anzeigen und Affiliate-Links
- Impressum und Datenschutzerklärung
- Hinweis «vom Veterinärdienst durchgesehen» auf Kantonsseiten, deren Amt die Angaben bestätigt hat. Nur mit dem Einverständnis des Amts und so formuliert, dass die Seite nicht amtlich wirkt. Die Frage danach kann mit dem Dank an die Ämter rausgehen, wenn Joss zustimmt.
- Anschreiben an Behörden, Vereine und Medien. Erste Runde am 18.11.2026 von Joss verschickt: Veterinärdienste SO, TG, BL, JU, TI. Antwort TG am 18.11.2026, eingearbeitet (siehe `CHANGELOG.md`). Antworten TI (Angaben korrekt, keine Änderung) und SO (Angaben korrekt, zwei Vorschläge eingearbeitet) am 21.11.2026. Offen: BL und JU. Für die nächste Runde: zuerst je Kanton klären, wer zuständig ist (im Thurgau die Gemeinden, das Veterinäramt nur für die Bewilligungen), und die Links der Kantonsseite mit einem echten Abruf prüfen. Zweite Runde am 26.11.2026 verschickt: 16 Mails an die Veterinärdienste der 21 übrigen Kantone, von Claude über das Postfach im Browser von Joss. Antworten am selben Tag: BE, AR mit AI, LU und ZG bestätigen (LU mit einem Hinweis, eingearbeitet), BS, FR und VS antworten mit Hinweisen (mit den Quellen verglichen und eingearbeitet, siehe `CHANGELOG.md`), SG prüft keine privaten Seiten. Offen: AG, GR mit GL, UR mit SZ, OW und NW, SH, ZH, GE, NE, VD. Aus der ersten Runde offen: BL und JU. Dank an die Ämter erst nach dem Ja von Joss. Zug: Für die Leinenpflicht im Wald ist das Amt für Wald und Wild zuständig, eine Prüfbitte dorthin braucht eine eigene Freigabe. Danach die 63 Gemeinden mit eigener Seite. Die französische Berner Seite erst verlinken, wenn `be_oce_fr` ersetzt ist.
