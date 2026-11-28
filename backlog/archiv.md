# Ausbauliste, Archiv

Abgehakte Punkte aus `BACKLOG.md` und den Dateien unter `backlog/`. Entsteht mit `python3 tools/archiv.py`. Nicht ganz lesen: mit grep suchen.

## Archiviert am 2026-11-27, von Hand

### BACKLOG.md, Kette

Die «Kette Übersetzungen» (von Joss am 18. November 2026 um 11:55 Uhr freigegeben, höchstens 8 Glieder) ist mit Glied 7 am 18. November 2026 erledigt: Alle 26 Kantone und 45 Gemeinden gibt es auf Deutsch, Französisch und Italienisch, `python3 build.py --fehlend` meldet nichts mehr.

- [x] a) Übersetzungen der Kantone (erledigt mit Glied 4 am 18.11.2026)
- [x] b) Übersetzungen der Gemeinden (erledigt mit Glied 7 am 18.11.2026)

Was die Glieder in Originalfassungen bemerkt haben, steht in `CHANGELOG.md` unter «Aufgefallen» und gehört in die nächste Nachprüfung.

## Archiviert am 2026-11-27

### BACKLOG.md, 1. Deutschsprachige Kantone

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

### BACKLOG.md, 2. Französisch und Italienisch

- [x] Waadt (`vd`), französisch, 2026-11-18, mit Lausanne (`/fr-ch/vd/`)
- [x] Genf (`ge`), französisch, 2026-11-18, mit Ville de Genève (`/fr-ch/ge/`)
- [x] Wallis (`vs`), französisch und deutsch, 2026-11-18, mit Ville de Sion französisch und Brig-Glis deutsch (`/vs/`, `/fr-ch/vs/`)
- [x] Freiburg (`fr`), französisch und deutsch, 2026-11-18, mit Ville de Fribourg französisch (`/fr/`, `/fr-ch/fr/`)
- [x] Tessin (`ti`), italienisch, 2026-11-18, mit Città di Lugano (`/it-ch/ti/`)
- [x] Neuenburg (`ne`), französisch, 2026-11-18, mit Ville de Neuchâtel (`/fr-ch/ne/`)
- [x] Jura (`ju`), französisch, 2026-11-18, ohne Gemeinde (Delémont zurückgestellt) (`/fr-ch/ju/`)
- [x] Bern (`be`), französische Fassung des Kantons, 2026-11-18 (`/fr-ch/be/`). Biel/Bienne französisch steht in Abschnitt 3.
- [x] Graubünden (`gr`), italienische Fassung, 2026-11-18, ohne Gemeinde (`/it-ch/gr/`)

### BACKLOG.md, Tote Links

- [x] `ai_vob` (Kanton Appenzell Innerrhoden), 2026-11-20: ersetzt durch den Anhang 1 der VOB im Stand 31. März 2025 (`ai.clex.ch/api/annex_document_dictionaries/2903`). Beträge unverändert (CHF 50 und CHF 100). Die Adresse ist wieder ein Dateipfad der Gesetzessammlung: Die nächste Link-Prüfung zeigt, ob sie hält.
- [x] `ar_brosch` (Kanton Appenzell Ausserrhoden), 2026-11-19: ersetzt durch die Broschüre Version 02/2025 (`…/Informationsbroschuere_zur_Hundehaltung_AR_250224_.pdf`)
- [x] `be_oce_fr` (Kanton Bern, französische Fassung), 2026-11-27: ersetzt nach drei Läufen ohne Ersatz. Im Browser von Joss auf belex.sites.be.ch im Volltext gelesen: OCE (RSB 916.51, Stand 1. August 2026, Art. 13 und 13a) und Loi sur les chiens (RSB 916.31, Stand 1. April 2021). Neue Adresse `belex.sites.be.ch/app/fr/texts_of_law/916.51`, neue Quelle `be_lchiens_fr` (`…/app/fr/texts_of_law/916.31`). Beide Angaben der Karte «Annonce» und der Karte «Impôt sur les chiens» stimmen. Die Gesetzessammlung entsteht erst im Browser: Das Abrufwerkzeug sieht dort nur einen leeren Rahmen, und die Link-Prüfung merkt nur, ob die Adresse antwortet.
- [x] `ne_laisse` (Kanton Neuenburg), 2026-11-19: Der Flyer war nicht mehr zu finden. Ersetzt durch die Mitteilung des DDTE vom 12. April 2024 (`ne.ch/medias/Pages/Chiens-en-laisse-.aspx`, nachgeführt am 9. März 2026)
- [x] `zg_steinhausen_steuer` (Kanton Zug), 2026-11-20: Merkblatt Hundesteuer 2025 ersetzt durch das Reglement über das Halten von Hunden der Gemeinde Steinhausen (Nr. 52.1, § 11, `…/copy_of_dokumente/regl-halten-von-hunden.pdf/download`). Die Adresse liegt im selben Ordner wie die tote: Die nächste Link-Prüfung zeigt, ob sie hält.
- [x] `zh_winterthur_merkblatt` (Winterthur), 2026-11-21: ersetzt durch die Seite «Hund an- oder abmelden» der Einwohnerkontrolle (neuer Schlüssel `zh_winterthur_anmeldung`). Das neue Merkblatt «Hundewesen Gebühren» (stadt.winterthur.ch/download/media/657/…, Dateiname mit 20250603) war nicht abrufbar und ist ein Dateipfad, darum die Seite.
- [x] `ne_scav` (Kanton Neuenburg), 2026-11-20: Adresse ersetzt durch die Seite «S'occuper d'animaux» des SCAV, auf die die alte Adresse führte (`ne.ch/themes/vie-quotidienne-et-famille/animaux/soccuper-danimaux`).
- [x] `ur_silenen_hhv` (Silenen), 2026-11-21: Der Verdacht vom 20.11.2026 hat sich in zwei Durchgängen (20.11. um 11:30 Uhr, 21.11.) nicht wiederholt. Nichts geändert.

### BACKLOG.md, 5. Umbauten am Generator

- [x] Themenseiten, 2026-11-17
- [x] Mehrsprachigkeit (Französisch und Italienisch), 2026-11-18
- [x] Darstellung überarbeiten: Startseite ohne Vergleichstabelle, Gemeindeverzeichnis, Thementafeln, Karten in zwei Spalten (18.11.2026)
- [x] Übersetzungen im Generator: Kennzeichnung, Prüfsumme, Zahlenvergleich, `--fehlend`. Probe: Kanton und Stadt Zürich auf Französisch und Italienisch (18.11.2026)
- [x] Bund, Themenseiten und Fehlerseite in drei Sprachen (18.11.2026)
- [x] Link-Prüfung: `tools/links.py` und die Action «Quellen-Links prüfen» fragen jede Adresse aus den Quellendateien mit einem echten Abruf ab (18.11.2026). Anlass: Das Veterinäramt Thurgau meldete einen toten Link (Error 404), den WebFetch noch auslieferte. Erster Durchgang: 264 Quellen, 253 in Ordnung, 6 tot, 1 Verdacht, 4 unklar. Die Liste steht in Abschnitt 4.
- [x] 2026-11-27, gebaut im Lauf: **Themenfeld «Hund vermisst oder gefunden»** (Entscheid von Joss vom 27.11.2026: «Kern», neue Themen). Abweichung von Punkt 4: Art. 720a ZGB war nicht lesbar (fedlex.admin.ch liefert dem Abrufwerkzeug nur eine leere Rahmenseite), die Karte des Bundes stützt sich darum nur auf ch.ch, siehe Abschnitt 4. Der Sonderlauf baut nur das Folgende, die Kantone folgen danach nach Abschnitt 9:
  1. Neues wahlweises Feld im Kanton, in jeder Sprachfassung: `vermisst: {"text": "...", "punkte": ["..."], "quellen": [...]}`. `text` sagt in ein bis zwei Sätzen, wo man einen entlaufenen oder einen gefundenen Hund im Kanton meldet. `punkte` ist wahlweise und nennt die Schritte. Übersetzungen führen das Feld wie jedes andere: gleicher Aufbau, gleiche Quellen, gleiche Zahlen.
  2. Kantonsseite: eigener Abschnitt nach dem Abschnitt zum Zuzug, nur wenn das Feld da ist. Überschrift «Hund vermisst oder gefunden {im}», französisch und italienisch entsprechend. Alle festen Texte in `TEXTE` in drei Sprachen. Vorhandene Bausteine und Farben, keine neuen.
  3. Siebte Themenseite unter `/thema/vermisst/`, `/fr-ch/thema/vermisst/` und `/it-ch/thema/vermisst/`: zuoberst, was beim Bund gilt, darunter je Kanton der Text mit seinen Quellen und dem Link zur Kantonsseite. Die Seite zählt keine Kantone. Kantone ohne Feld erscheinen nicht. Sie steht in der Sitemap, auf der Startseite und auf den Kantonsseiten wie die anderen Themen. Bestehende Adressen bleiben.
  4. Bund: in den drei Fassungen von `schweiz.json` eine Karte zum Verlust und Fund eines Tieres. Einstieg: Art. 720a ZGB auf fedlex.admin.ch und die Seiten des BLV in der jeweiligen Sprache. Nur schreiben, was die abgerufene Quelle sagt.
  5. Probe: das Feld für den Kanton Zürich belegen und in beide Sprachen übersetzen. Test erweitern: Die Themenseite führt jeden Kanton mit Feld samt Quelle, eine Kantonsseite ohne Feld zeigt den Abschnitt nicht.
  6. Jede neue Seitenart bei 390 und 1280 Pixeln als Bild ansehen, Handbuch im selben Commit nachführen (Aufbau, Datenfelder Kanton, Themenseiten).

### BACKLOG.md, 9.1 Hund vermisst oder gefunden

- [x] Zürich, 2026-11-27 (Probe im Sonderlauf, deutsch, französisch und italienisch)
- [x] Bern (deutsch und französisch), 2026-11-27 (in der Sitzung, dazu italienisch)
- [x] Waadt, 2026-11-27 (in der Sitzung, französisch, deutsch und italienisch)
- [x] Aargau, 2026-11-27 (in der Sitzung, deutsch, französisch und italienisch)
- [x] St. Gallen, 2026-11-27 (in der Sitzung, deutsch, französisch und italienisch)
- [x] Genf, 2026-11-27 (in der Sitzung, französisch, deutsch und italienisch)
- [x] Luzern, 2026-11-27 (in der Sitzung, deutsch, französisch und italienisch)
- [x] Basel-Landschaft, 2026-11-27 (in der Sitzung, deutsch, französisch und italienisch)
- [x] Thurgau, 2026-11-27 (in der Sitzung, deutsch, französisch und italienisch)
- [x] Schaffhausen, 2026-11-27 (in der Sitzung, deutsch, französisch und italienisch)
- [x] Nidwalden, 2026-11-27 (in der Sitzung, deutsch, französisch und italienisch)
- [x] Glarus, 2026-11-27 (in der Sitzung, deutsch, französisch und italienisch)

### backlog/gemeinden.md, Gemeinden nach Grösse

- [x] Aarau (AG), 2026-11-27 (in der Sitzung, deutsch, französisch und italienisch). Am 17.11.2026 zurückgestellt, weil die geltende Polizeiverordnung nicht lesbar war. Im Browser von Joss gelesen: Polizeiverordnung in der Fassung vom 1. Januar 2023, Bau- und Nutzungsordnung, Badeverordnung, Merkblätter und Online-Schalter der Stadt.
- [x] Wettingen (AG), 2026-11-19
- [x] Baden (AG), 2026-11-19
- [x] Muttenz (BL), 2026-11-19
- [x] Liestal (BL), 2026-11-20
- [x] Kreuzlingen (TG), 2026-11-17
- [x] Arbon (TG), 2026-11-17
- [x] Zuchwil (SO), 2026-11-21
- [x] Einsiedeln (SZ), 2026-11-18
- [x] Schwyz (SZ), 2026-11-17
- [x] Arth (SZ), 2026-11-18
- [x] Davos (GR), 2026-11-18
- [x] Landquart (GR), 2026-11-18
- [x] Domat/Ems (GR), 2026-11-21
- [x] Riehen (BS), 2026-11-21
- [x] Gossau (SG), 2026-11-21
- [x] Winterthur (ZH), 2026-11-18
- [x] Biel/Bienne (BE), 2026-11-27, Adresse `biel-bienne`, deutsch und französisch als Originalfassungen, im Browser von Joss gelesen
- [x] Thun (BE), 2026-11-21
- [x] Köniz (BE), 2026-11-21
- [x] Uster (ZH), 2026-11-18
- [x] Emmen (LU), 2026-11-18
- [x] Dübendorf (ZH), 2026-11-18
- [x] Dietikon (ZH), 2026-11-18
- [x] Wetzikon (ZH), 2026-11-18
- [x] Wädenswil (ZH), 2026-11-18
- [x] Burgdorf (BE), 2026-11-21
- [x] Bülach (ZH), 2026-11-18
- [x] Horw (LU), 2026-11-18
- [x] Ebikon (LU), 2026-11-18
- [x] Steffisburg (BE), 2026-11-21
- [x] Ostermundigen (BE), 2026-11-21
- [x] Opfikon (ZH), 2026-11-18
- [x] Thalwil (ZH), 2026-11-18
- [x] Adliswil (ZH), 2026-11-18
- [x] Sursee (LU), 2026-11-18
- [x] Regensdorf (ZH), 2026-11-18
- [x] Illnau-Effretikon (ZH), 2026-11-18
- [x] Schlieren (ZH), 2026-11-21 (Hundeabgabe, Anmeldung, Hundeverbot auf dem Friedhof)
- [x] Volketswil (ZH), 2026-11-18
- [x] Risch (ZG), 2026-11-25. Hundereglement unter zg.ch/behoerden/gemeinden/risch-rotkreuz/…/101-hundereglement.
- [x] Steinhausen (ZG), 2026-11-25. Nicht übernommen: § 9 des Reglements von 1976 (Leine im Wald, am Waldrand und nachts), weil das kantonale Recht den Wald seit 2024 anders regelt. Reglement über das Halten von Hunden und Merkblatt Hundesteuer 2025 auf zg.ch.
- [x] Glarus (GL), 2026-11-18
- [x] Schaffhausen (SH), 2026-11-18
- [x] Neuhausen am Rheinfall (SH), 2026-11-21
- [x] La Chaux-de-Fonds (NE), französisch, 2026-11-25. Ohne Anmeldestelle: Die Seite «Impôts, taxes, amendes» der Stadt lieferte nur eine Fehlerseite. Das Règlement de police liegt im Stand 1. Juni 2015 vor: bei der nächsten Nachprüfung eine neuere Fassung suchen.
- [x] Sarnen (OW), 2026-11-18
- [x] Silenen (UR), 2026-11-18
- [x] Sion (VS), französisch, 2026-11-18
- [x] Brig-Glis (VS), deutsch, 2026-11-18

### backlog/luecken.md, Offene Lücken

- [x] 2026-11-27: Stadt Zürich, Karte «Hundeabgabe» ergänzt: CHF 130 an die Stadt, dazu der Kantonsbeitrag, den die Vollzugsvorschriften mit CHF 30 nennen, Einschreibegebühr CHF 20, verspätet CHF 40 (Vollzugsvorschriften zum Hundegesetz, in Kraft seit 1. September 2017). Dazu die Frist von 10 Tagen für die Anmeldung.
- [x] 2026-11-27: Stadt Zürich, Hundeabgabe: Ermässigung nach freiwilligem Kurs und Erlass am Volltext der Vollzugsvorschriften gelesen und ergänzt. § 24 des kantonalen Hundegesetzes erlaubt die Ermässigung auch in der Fassung, die seit 1. Juni 2025 gilt.
- [x] 2026-11-27: Kanton Zürich, Karten Hundesteuer und Anmeldung aus dem Volltext des Hundegesetzes ergänzt (LS 554.5, Nachtrag 129, Stand 1. Juli 2025, §§ 21 und 23 bis 26). Neue Quelle `zh_hundeg`: die Seite des Erlasses in der Gesetzessammlung. Ihre Adresse trägt die Nummer des Nachtrags: Bei der nächsten Änderung des Gesetzes bleibt sie erreichbar, zeigt aber die frühere Fassung. Beim Nachprüfen von Zürich nachsehen, ob dort noch «129 (aktuell)» steht. § 15 (die Polizei fängt streunende Hunde ein und meldet sie der Meldestelle für gefundene Tiere nach Art. 720a Abs. 2 ZGB) ist gelesen, aber nicht eingetragen: Das Feld `vermisst` stützt sich auf die Seiten des Veterinäramts.
- [x] 2026-11-27: Stadt Zürich, die 7 Freilaufzonen mit Namen aufgeführt und in der Karte «Zonen» die 69 Flächen mit Leinenpflicht nach Zeit geordnet (Datensatz «Hundezonen», 728 Flächen, Stand der Daten 14.07.2026, im Browser von Joss gelesen).
- [x] 2026-11-27: Stadt Bern, Hundetaxe CHF 150 pro Hund und Jahr für Hunde ab 6 Monaten, Rechnung im August, Befreiung für Assistenz-, Begleit-, Therapie- und Rettungshunde (Seite der Stadt, geändert am 8. Oktober 2026).
- [x] 2026-11-27: Stadt Luzern, Bussen: gestützt auf die Kantonale Ordnungsbussenverordnung (`lu_kobv`, Stand 1. November 2026). Die Broschüre der Stadt nennt dieselben Beträge.
- [x] 2026-11-27: Kanton Bern, «keine Kurspflicht» belegt mit dem Hundegesetz (kennt keinen Pflichtkurs, Kurse nur als Massnahme im Einzelfall, Art. 12) und der Seite «Einen Hund kaufen und halten» des Amts für Veterinärwesen (empfiehlt einen Kurs). Die Quelle der Gemeinde Büren entfällt.
- [x] 2026-11-27: Kanton Aargau, Hundeverordnung (SAR 393.411) in der Fassung vom 1. März 2024 gelesen und eingearbeitet: Deckungssumme CHF 1 Million, Fristen für Kurs und Prüfung, Stichtag der Taxe, Befreiungen. Die halbe Taxe gibt es nicht mehr (§ 21 Abs. 3 bis 5 sind seit 1. März 2024 aufgehoben).
- [x] 2026-11-27: Kanton Aargau, die vier Seiten auf www.ag.ch (Hunde, Listenhunde, Leinenpflicht, Kantonspolizei) im Browser von Joss gegengelesen, nachdem er die Domain freigegeben hat. Die Angaben stimmen. Die Adresse der Quelle `ag_vet` leitete auf eine neue Adresse um, die Quelle zeigt jetzt direkt dorthin.
- [x] 2026-11-27: Kanton Aargau, Ordnungsbusse für Hundekot (CHF 100) bestätigt. Die OBVV (SAR 251.213) gilt unverändert in der Fassung vom 1. Juli 2021, Anhang 1 Ziffer 2.2. Derselbe Anhang nennt CHF 100 für die Leinen- und Führpflicht der Listenhunde und in den Schutzgebieten an der Reuss.
- [x] 2026-11-27: Kanton St. Gallen, Verordnung über die Jagdvorschriften (sGS 853.111, Fassung vom 1. Juni 2024) gelesen: Sie regelt nur Jagdhunde, eine Leinenpflicht im Wald steht nicht darin. Hundegesetz, Hundeverordnung, Jagdgesetz und Jagdverordnung in der Gesetzessammlung des Kantons gegengelesen. Die Quellen zeigen jetzt dorthin (alt: PDF auf sg.lexwork.naz.ch).
- [x] 2026-11-27: Kanton Basel-Landschaft, Seiten des Veterinärwesens und des Amts für Wald und Wild auf baselland.ch im Browser gelesen und mit den Gesetzen verglichen. AMICUS ist ergänzt. «Waldesnähe» erklärt das Amt mit «an Waldrändern und auf angrenzenden Wiesen».
- [x] 2026-11-27: Kanton Thurgau, Hundegesetz (RB 641.2) und Hundeverordnung (RB 641.21) im Rechtsbuch des Kantons gelesen, im Browser von Joss, beide im ganzen Wortlaut und mit Stand 1. Mai 2025. Eine Meldefrist bei der Gemeinde nennt das Gesetz nicht (§ 8 und § 9 verweisen auf das Bundesrecht), eine Übergangsregel beim Kurs steht nicht im geltenden Text, das Merkblatt mit der Gebühr von CHF 500 trägt kein Datum.
- [x] 2026-11-27: Muttenz, Reglement über das Halten von Hunden (Nr. 11.600, Fassung 17. Oktober 2024) und Gebührenordnung (Nr. 11.609, Fassung 8. Mai 2024) im Browser von Joss gelesen. Neu auf der Seite: Gebühr, Orte mit Leinenpflicht, Hundekot, Strafrahmen. Eine Meldefrist nennt die Gemeinde nicht, das Reglement verweist auf die Tierseuchenverordnung.
- [x] 2026-11-27: Kanton Nidwalden, geltende Fassungen im Browser von Joss in der Erlass-Sammlung des Kantons (gesetze.nw.ch) gelesen: Hundegesetz (NG 826.3, Stand 1. Januar 2016), Hundeverordnung (NG 826.31, Stand 1. Januar 2012), Verordnung über die Wildruhegebiete (NG 841.15, Stand 1. Januar 2020), Ordnungsbussenverordnung, Jagdgesetz und Jagdverordnung, Waldgesetz und Waldverordnung. Alle Angaben verglichen, die Hinweise «Fassung von 2005» und «Stand 2019» entfernt. Neu: die 14 Wildruhegebiete mit Namen und Daten der Leinenpflicht, Busse CHF 150, Jagdbanngebiet Huetstock. Waldgesetz und Waldverordnung nennen Hunde nicht.
- [x] 2026-11-27: Kanton Schaffhausen, geltende Fassung von SHR 455.200 (Stand 1. Januar 2010) und SHR 455.201 (Stand 1. Januar 2017) im Browser von Joss auf rechtsbuch.sh.ch gelesen, alle Angaben verglichen, Stand-Hinweise entfernt. Karte Kurs geklärt mit der Seite des Veterinäramts: keine generelle Ausbildungspflicht. Die Kontrollmarke steht nicht mehr in der Verordnung und ist gestrichen.
- [x] 2026-11-27: Stadt Schaffhausen, Betrag der Hundesteuer (Stadtratsbeschluss vom 8. Mai 2018) und Anmeldung bei der Einwohnerkontrolle (Seite «Hundekontrolle») belegt, beides im Browser von Joss gelesen.
- [x] 2026-11-27: Kanton Glarus, im Browser von Joss in der Erlass-Sammlung (gesetze.gl.ch) gelesen: Einführungsgesetz zum Tierschutzgesetz und zum Tierseuchengesetz (GS IV G/3/2, Stand 1. Januar 2026), Veterinärverordnung, Jagdverordnung, Wildruhezonenverordnung, Ordnungsbussenverordnung, EG ZGB. Leinenpflicht im öffentlichen Raum (Art. 31) steht jetzt mit dem Gesetz als Quelle, Deckungssumme («ausreichend», kein Betrag), Bussen (CHF 100 Ordnungsbusse, Busse bis CHF 10 000), Wildruhezonen, Schutzgebiet Hüttenböschen-Seeflechsen. Karte Kurs: `ton` auf `must`, die Pflicht für Ersthundehalter steht in Art. 26a. Eine Pflicht, Hundekot aufzunehmen, nennen Gesetz und Verordnung nicht. Merkblatt (Version 9 vom 12. Februar 2025) gelesen.
- [x] 2026-11-27: Kanton Waadt, LPolC (BLV 133.75) und RLPolC (BLV 133.75.1) in der Base législative vaudoise gegengeprüft: Beide gelten unverändert in der Fassung vom 1. Mai 2014, der Stand von LexFind war der geltende. Die Leinenpflicht im Wald steht seit 1. Juni 2024 in Art. 7b RLFaune (BLV 922.03.1, gelesen in der Fassung vom 1. Januar 2026), nicht mehr in Art. 2a. Das Faltblatt der DGE nennt noch Art. 2a.
- [x] 2026-11-27: Kanton Bern, beide Originalfassungen am geltenden Recht geprüft und ergänzt: Hundegesetz, Verordnung über den Tierschutz und die Hunde, Tierseuchenverordnung, Verordnung über den Wildtierschutz, Ordnungsbussenverordnung, deutsch und französisch auf belex.sites.be.ch im Browser von Joss gelesen, dazu Broschüre und Seite des Amts für Veterinärwesen in beiden Sprachen. Maulkorb, Bussen (CHF 100 Ordnungsbusse, bis CHF 5000 bei hinterzogener Taxe), Regeln im Wald und Feld, Wildschutzgebiete, Rudel-Ausnahmen, Feld `vermisst`. `geprueft` in beiden Fassungen gesetzt.
- [x] 2026-11-27: Ville de Neuchâtel, Namen der Freilauf- und Badezonen belegt. Der «Arrêté concernant les modalités d'accès des chiens aux espaces publics» vom 15. Juni 2020 (Bild-PDF, 9 Seiten) im Browser von Joss Seite für Seite als Bild gelesen: sechs Freilaufzonen und die Badezonen, Flächen aus den Plänen im Anhang. Er gilt laut Art. 94 des Polizeireglements vom 11. Mai 2026 weiter, die Seite der Stadt nennt ihn «l'arrêté communal en vigueur».
- [x] 2026-11-27: Acht Gemeinden vom 21.11.2026 (Thun, Steffisburg, Ostermundigen, Burgdorf, Schlieren, Neuhausen am Rheinfall, Domat/Ems, Gossau) an den Dokumenten gegengelesen, im Browser von Joss: Seiten der Gemeinden und die Erlasse als PDF-Text. Alle acht tragen `geprueft` 2026-11-27. Einzig die Seite «Hunde melden» von Domat/Ems kam über WebFetch, weil www.domat-ems.ch im Chrome von Joss nicht freigegeben ist.
- [x] 2026-11-27: Thun, Verordnung über die Benützung des Seeuferbereichs (733.10, in Kraft seit 1. April 2026) und Situationsplan gelesen. Art. 7: Leine in den speziell markierten Bereichen laut Plan, sonst und auf dem Hundespielplatz frei. Art. 2 Abs. 3: Hundeverbot im Strandbadareal das ganze Jahr. Art. 11: Hundekot. Die Bereiche stehen nur als Zeichnung im Plan, die Seite verlinkt ihn.
- [x] 2026-11-27: Köniz, Betrag der Hundetaxe (CHF 100, Verordnung 916.311 und Reglement 916.31), Friedhöfe, Schwimmbad Weiermatt, Liebefeld Park und Schlosspark belegt, im Browser von Joss als PDF-Text gelesen. Die Übersicht der Erlasse steht unter `koeniz.ch/verwaltung/reglementeverordnungen.page/952`. Dort stehen auch zwei Erlasse, die nicht eingetragen sind, weil sie nur wiederholen, was Kanton und Ortspolizeireglement schon sagen: Areal Villa Bernau (731.42, Leinenpflicht) und Schul- und Sportanlagen (430.61, Leinenpflicht, kein Versäubern, keine Tiere im Lehrschwimmbad).
- [x] 2026-11-27: Steffisburg, Friedhof- und Bestattungsreglement von 2015 gelesen (Hunde auf dem Friedhof an der Leine) und als Quelle eingetragen. Die Verordnung dazu nennt Hunde nicht.
- [x] 2026-11-27: Ostermundigen, Kinderspielplätze geklärt, so weit es die Dokumente erlauben. Das Ortspolizeireglement von 1984 (Art. 49 Abs. 1) verbietet den Zutritt. Das Reglement über die Park- und Grünanlagen (Nr. 230, in Kraft seit 1. Mai 2007) gilt auch für Spielplätze, verbietet dort das freie Laufenlassen (Art. 3 Bst. h) und hebt frühere widersprechende Vorschriften auf (Art. 11 Abs. 2). Seite und Merkblatt der Gemeinde (2020) nennen für öffentliche Spielplätze die Leine. Die Seite zeigt jetzt beides und verweist auf die Tafeln vor Ort. Ob die Leine von 22.00 bis 06.00 Uhr noch durchgesetzt wird, sagt kein Dokument: Der Satz steht weiter als Inhalt des Reglements von 1984.
- [x] 2026-11-27: Burgdorf, Hundereglement (Ausgabe August 2021), Gebührenverordnung (Ausgabe Januar 2026, Ziffer 8.14.2), Anlagenutzungsverordnung (Ausgabe Mai 2026), Gemeindepolizeireglement und Bestattungsreglement gelesen. Das Hundereglement regelt nur die Taxe und die Befreiungen. Eigene Leinenorte, Verbote oder Bussen zu Hunden kennt Burgdorf ausser dem Friedhof nicht: Die Anlagenutzungsverordnung verweist auf das kantonale Hundegesetz (Art. 6 Abs. 6), das Gemeindepolizeireglement behält die Vorschriften über das Halten von Tieren vor.
- [x] 2026-11-27: Schlieren, Betrag von CHF 170 am Gebührentarif SKR 9.11 vom 17. Juni 2026 (in Kraft seit 1. August 2026, § 36) bestätigt. Neu auf der Seite: die Meldegebühren aus demselben Paragrafen.
- [x] 2026-11-27: Neuhausen am Rheinfall, Reglement über die Abgabe für das Halten von Hunden (644.101, in Kraft seit 1. Januar 2018) gelesen: CHF 160 und CHF 200 bestätigt, dazu Pauschale für Zuchten, halbe Abgabe und Erlass. Badeordnung der Rhyfallbadi Otterstall gelesen und eingetragen.
- [x] 2026-11-27: Domat/Ems, Kommunales Polizeigesetz (SRS 5.1-1, Fassung vom 1. November 2025), Steuergesetz (SRS 6.3-1) und Friedhofverordnung (SRS 8.2-1.1) auf domat-ems.tlex.ch gelesen: Leine im besiedelten Gebiet, kein Zutritt zu öffentlichen Gebäuden, Sport- und Kinderspielplätzen und zum Friedhof, Verunreinigungen, Bussen, Meldefrist von 14 Tagen. Der Online-Schalter der Gemeinde nennt weiter CHF 90 und CHF 210.
- [x] 2026-11-27: Domat/Ems, www.domat-ems.ch im Browser von Joss gelesen (ab 16:32 Uhr, in der Seitenleiste von Claude in Chrome, die Joss auf dem Tab der Gemeinde geöffnet hat). Seite «Hunde melden» bestätigt. Ordnungsbussenliste des Gemeinderats gefunden (SRS 5.1-2, Fassung in Kraft seit 1. Januar 2023) und eingetragen: CHF 100 für liegen gelassenen Hundekot, je CHF 50 für die missachtete Aufsichtspflicht und die missachtete Leinenpflicht im Siedlungsgebiet. Neu belegt: Landwirtschaftsgesetz (SRS 9.2-1, Art. 10: Tiere vom 15. März bis 15. November nicht frei über Wiesen und Weiden) und die Mitteilungen der Gemeinde «Hundemeldepflicht» (1. Mai 2026) und «Betreten der Flure» (18. März 2026).
- [x] 2026-11-27: Gossau, Polizeireglement mit beiden Nachträgen gelesen. Es hat keinen Hundeartikel: eingetragen sind Art. 9 (Haustiere dürfen Dritte nicht erheblich stören), die Ruhezeiten, Art. 13 (Verunreinigung öffentlicher Anlagen) und Art. 29 (Busse, ohne Betrag). Befreiungen von der Taxe und das Einwohneramt als zuständiges Amt stehen auf der Seite «Hundekontrolle» und sind eingetragen. Friedhofreglement samt Ausführungsbestimmungen und das Reglement über die Nutzung städtischer Bauten und Anlagen nennen Hunde nicht.
- [x] 2026-11-27: Kanton Bern, französische Fassung an den französischen Texten geprüft: Loi sur les chiens (RSB 916.31), OPAC (RSB 916.812), OCE (RSB 916.51), OPFS (RSB 922.63) und OCAO (RSB 324.111). Befreiungen von der Taxe, Zutrittsverbote der Gemeinden und Bussen stimmen und sind ergänzt. Französische Quelle zum Wald: Art. 7 OPFS.
- [x] 2026-11-27: Kanton Genf, LChiens (M 3 45) und RChiens (M 3 45.01) im Volltext auf silgeneve.ch gelesen, beide «dernières modifications au 17 novembre 2026». Die Änderung vom 17. November 2026 berichtigt nur den Namen der Stelle, die grosse Revision gilt seit 29. April 2023. RChiens Art. 13 Bst. l (Ufer und Wasser, Oktober bis März) ist jetzt in der Liste der Verbote, Art. 14 Bst. d und e stimmen mit der Seite überein, die Liste in Art. 17 nennt dieselben 15 Rassen. Bussenbeträge nennt das Gesetz nicht (Art. 40).
- [x] 2026-11-27: Kanton Thurgau, `data/kantone/tg.json` gegen das geltende Hundegesetz geprüft. Die Busse von CHF 50 steht jetzt in der Liste der Ordnungsbussen. «Betreuen» und der Gentest unter 50 Prozent stehen im Gesetz (§ 3a). Für Auswärtige gilt § 69 Abs. 3 der Verordnung über das Veterinärwesen: keine Bewilligung, aber Leine von höchstens 2,5 m und Maulkorb. Die Karte war falsch und ist berichtigt. Bullmastiff und Alano nennt die Hundeverordnung weiterhin nicht, sie stehen im Merkblatt, Alano auch auf der Seite des Veterinäramts.
- [x] 2026-11-27: Regensdorf, Betrag der Hundesteuer aus dem Gebührenreglement (CHF 100 pro Hund und Jahr, dazu der Kantonsbeitrag) und Polizeiverordnung im Browser von Joss gelesen. Die Polizeiverordnung von 2024 nennt Hunde nicht eigens: keine Orte mit Leinenpflicht oder Hundeverbot, kein eigener Artikel zum Hundekot, keine Bussenbeträge. Offen bleibt die Höhe des Kantonsbeitrags (siehe Lücke Kanton Zürich).
- [x] 2026-11-27: Luzern, Karte Rassen: Die Quelle `srf` ist ersetzt durch das Hundegesetz und die Hundeverordnung im geltenden Text (srl.lu.ch). Beide enthalten keine Rasseliste, der Veterinärdienst ordnet Massnahmen im Einzelfall an (§ 7a HuV). Die Karte sagt jetzt «keine Rasseliste» statt «keine Einschränkungen».
- [x] 2026-11-27 abgehakt, die Datei trägt schon `ganzjaehrig: true` und die Seite titelt «Leinenpflicht im Wald das ganze Jahr»: Glarus, Feld `wald`: `saison` ist `false`, die Leine gilt aber ganzjährig. Die Seite titelt «Keine Saisonregel im Wald». Titel oder Daten so anpassen, dass niemand «keine Pflicht» liest (aufgefallen in der Kette Übersetzungen, 18.11.2026)
- [x] 2026-11-27: Waadt, Genf und Neuenburg französisch, `vergleich.wald`: Schreibweise überall «du 1.4. au 15.7.» (Neuenburg am 2026-11-19, Waadt und Genf am 2026-11-27 beim Nachprüfen)

### backlog/luecken.md, Aufgefallen beim Übersetzen (Kette Übersetzungen, 18.11.2026)

- [x] `data/fr-ch/kantone/ne.json`, Feld `vergleich.wald`: «15.4 au 30.6» ohne Punkt nach dem Monat, wie schon bei VD und GE gemeldet. Die Übersetzungen schreiben «15.4. bis 30.6.» und «dal 15.4. al 30.6.». Erledigt am 2026-11-19.
- [x] 2026-11-27: `data/gemeinden/lu/luzern.json` hat jetzt vier Karten (Hundetaxe, Leine, Anmeldung, Bussen). «CHF 100 bis 150 (Naturschutzgebiete)» ist geklärt: CHF 150 gilt nur für den Leinenzwang in Naturschutzgebieten, sonst CHF 100 (Kantonale Ordnungsbussenverordnung).
- [x] 2026-11-27, in der Sitzung erledigt für ZH, BS, FR (deutsch und französisch), NE, VS (deutsch und französisch) und TI, Übersetzungen nachgeführt. LU: Das Merkblatt des Veterinärdiensts nennt keine Liste, nur «geeignete Kurse» und die Website des NHB, darum kein Zusatz. TG: keine amtliche Liste gefunden, kein Zusatz. Ursprünglicher Eintrag: Kurs-Karte in den acht Kantonen mit Kurspflicht: sagen, wo man die anerkannten Kursanbieter findet, mit der amtlichen Seite als Quelle. Am 27.11.2026 gefunden, im Lauf neu abrufen. ZH: zwei Listen der bewilligten Hundeausbildenden auf zh.ch/hunde, alphabetisch und nach Postleitzahl, Stand 30.10.2026. FR: Liste und Karte auf der Seite «Hundeausbildnerinnen und Hundeausbildner», Liste vom 9.11.2026. NE: Liste des SCAV vom 12.3.2026. BS: Die Seite «Hundekurse» verweist auf den Verband VKAS. VS: «Affaires canines» verlinkt die Liste der NHB-Fachpersonen. TI: «Corso teorico obbligatorio» verweist für Kursliste und Anmeldung auf die Associazione Ticinese Istruttori Cinofili. LU: Das Merkblatt von 2023 nennt keine Liste. TG: keine Liste, das «Merkblatt Ausbildungsstätten für Hundehalter» des Veterinäramts prüfen.

## Archiviert am 2026-11-27

### backlog/spaeter.md, Ideen für später

- [x] 2026-11-27: Handbuch und Backlog verschlankt (Entscheid von Joss um 23:24 Uhr an Claude übertragen). `CLAUDE.md` von 107 auf 46 KB, `BACKLOG.md` von 117 auf 14 KB, `CHANGELOG.md` von 280 auf 24 KB. Nichts gelöscht: Nachschlageteile unter `handbuch/`, lange Listen unter `backlog/`, Archiv mit `tools/archiv.py`.

## Archiviert am 2026-11-27

### BACKLOG.md, 5. Umbauten am Generator

- [x] 2026-11-27 (Sonderlauf, siehe Protokoll): **Änderungswächter für Quellen** (Frage von Joss vom 27.11.2026, 01:59 Uhr: Wie bleiben die Angaben aktuell, bei so vielen Quellen?). Heute prüft der Lauf blind die ältesten Dateien, 4 pro Lauf. Bei 96 Originalfassungen dauert eine Runde mit zwei Läufen pro Woche 12 Wochen, die Schwelle ist aber 60 Tage. Der Wächter sagt stattdessen, welche Quelle sich geändert hat. Er läuft wie die Link-Prüfung als GitHub Action und kostet kein Guthaben.
  1. `tools/wandel.py` ruft jede Adresse aus den Quellendateien ab, mit denselben Kopfzeilen und Zeitgrenzen wie `tools/links.py`. Aus HTML nimmt es den sichtbaren Text ohne `script`, `style`, `nav`, `header`, `footer` und Formulare, fasst Leerraum zusammen und bildet davon eine Prüfsumme. Bei PDF und anderen Dateien bildet es die Prüfsumme der Bytes.
  2. Der Stand liegt nicht auf `main`, sondern auf dem Zweig `wandel` in der Datei `wandel.json`: je Schlüssel die Prüfsumme, das Datum des letzten Abrufs, das Datum der letzten Änderung und die Daten der letzten Änderungen. Eine Änderung zählt nur, wenn es schon eine Prüfsumme gab und die neue anders ist. Antwortet eine Adresse nicht, bleibt der Eintrag stehen.
  3. `.github/workflows/wandel.yml`: jeden Montag früh und auf Befehl (`workflow_dispatch`), mit `permissions: contents: write`. Sie holt den Zweig `wandel` (und legt ihn beim ersten Mal an), lässt das Werkzeug laufen und schreibt den Stand zurück. Sie wird nie rot und fasst `main` nie an.
  4. `python3 tools/wandel.py --faellig` für den Lauf: liest `wandel.json` vom Zweig `wandel` (`git fetch origin wandel`, `git show origin/wandel:wandel.json`) und nennt jede Originalfassung, die eine Quelle zitiert, deren letzte Änderung nach dem `geprueft` der Datei liegt. Quellen mit mehr als drei Änderungen in vier Wochen gelten als unruhig und zählen nicht.
  5. Handbuch, Schritt 2 «Nachprüfen»: Nach den toten Links kommen die Dateien, die der Wächter nennt, dann die ältesten. Die Obergrenze von 4 Dateien bleibt. Die Schwelle für das blinde Nachprüfen steigt von 60 auf 120 Tage, das schafft der Lauf auch mit zwei Tagen pro Woche. Dazu ein Kalender: im März alle Felder `wald`, im Januar alle Karten zu Hundesteuer und Hundetaxe, unabhängig vom Alter der Datei.
  6. Erster Durchgang: Action auslösen und im Protokoll festhalten, wie viele Quellen erreichbar waren. Dieses Handbuch im selben Commit nachführen (Aufbau, neuer Abschnitt «Änderungswächter» nach «Link-Prüfung»).
  7. Grenze, aufgefallen am 27.11.2026 in Neuenburg: Die Stadt hat seit dem 21. Oktober 2026 ein neues Polizeireglement. Das alte PDF blieb unverändert online, die Link-Prüfung zeigte «in Ordnung», und ein Wächter auf dieser Adresse hätte nichts gemerkt. Gefunden wurde es erst über die Übersicht der Reglemente. Darum beobachtet der Wächter bei Quellen, die ein einzelnes Dokument sind (PDF oder Adresse mit der Nummer der Fassung), zusätzlich die Übersichtsseite, die das Dokument verlinkt, wenn der Quelleneintrag eine nennt (neues wahlweises Feld `uebersicht`, `build.py` muss es zulassen). Ändert sich dort die Liste der verlinkten Dokumente, meldet er die Quelle. Erste Einträge: `ne_ville_police` und `ne_ville_taxes` (neuchatelville.ch/votre-commune/reglementation), `zh_hundeg` (die Seite des Erlasses trägt die Nummer des Nachtrags), `sh_stadt_hundesteuer`, `bl_muttenz_hundereglement`. Weitere kommen beim Nachprüfen dazu. Umgesetzt am 27.11.2026 für die ersten vier. `bl_muttenz_hundereglement` ohne Übersicht: Die Suche fand keine Übersichtsseite der Reglemente, und die Quelle ist selbst eine Webseite, deren Text der Wächter ohnehin vergleicht.

## Archiviert am 2026-11-28

### BACKLOG.md, 9.1 Hund vermisst oder gefunden

- [x] Tessin 2026-11-27
- [x] Wallis (deutsch und französisch) 2026-11-27
- [x] Freiburg (deutsch und französisch) 2026-11-27
- [x] Solothurn 2026-11-27

## Archiviert am 2026-11-28

### BACKLOG.md, 9.1 Hund vermisst oder gefunden

- [x] Zug 2026-11-28

### backlog/gemeinden.md, Gemeinden nach Grösse

- [x] Spiez (BE) 2026-11-28
- [x] Lyss (BE) 2026-11-28
- [x] Münsingen (BE) 2026-11-28
- [x] Düdingen (FR) 2026-11-28
- [x] Bulle (FR) 2026-11-28
- [x] Yverdon-les-Bains (VD) 2026-11-28
- [x] Nyon (VD) 2026-11-28
- [x] Vernier (GE) 2026-11-28
- [x] Lancy (GE) 2026-11-28
- [x] Meyrin (GE) 2026-11-28
- [x] Carouge (GE) 2026-11-28
- [x] Visp (VS) 2026-11-28
- [x] Naters (VS) 2026-11-28
- [x] Martigny (VS) 2026-11-28

## Archiviert am 2026-11-28

### BACKLOG.md, 5. Umbauten am Generator

- [x] **«Neu einen Hund»: die Schritte je Kanton, dazu der Sprunglink** (erledigt 28.11.2026, Sonderlauf) (Abschnitt 10, Punkt 5. Vorgabe aus der Sitzung vom 28.11.2026). Wer einen Hund übernimmt, sieht auf der Seite seines Kantons, was der Reihe nach zu tun ist. Tierheime können direkt darauf verlinken. Alles entsteht aus den vorhandenen Angaben: keine Recherche, keine neuen Datenfelder, kein Wort an den Daten ändern. Keine neue Seitenart, keine neue Adresse.
  1. Anker. Die sechs Karten der Kantonsseite bekommen feste `id`, in jeder Sprache dieselben: `haftpflicht`, `kurs`, `anmeldung`, `hundesteuer`, `rassen`, `unterwegs` (nach der Position der Karte, nicht nach ihrem Titel). Der Kasten zur Leine im Wald bekommt `wald`, falls er noch keine `id` hat. Nur auf der Kantonsseite, nicht auf Themenseiten und Gemeindeseiten: Dort stünden sonst dieselben `id` mehrfach. Springt man einen Anker an, darf die Überschrift nicht unter dem Kopf der Seite verschwinden (`scroll-margin-top`, falls nötig).
  2. Abschnitt auf jeder Kantonsseite, nach den Pflichten (samt Kasten zum Umzug) und vor «Hund vermisst oder gefunden», mit `id="neuer-hund"`. Überschrift: «Neu einen Hund {im}: die Schritte». Darunter ein Satz: «Du hast einen Hund übernommen oder holst bald einen zu dir? Hier stehen die Angaben dieser Seite in der Reihenfolge, in der sie für dich wichtig werden. Einzelheiten und Quellen findest du beim jeweiligen Punkt.» Dann eine nummerierte Liste (`<ol>`) mit genau sechs Schritten in dieser Reihenfolge: Rassen (Karte 5, `vergleich.rassen`), Anmeldung (Karte 3, `vergleich.anm`), Haftpflicht (Karte 1, `vergleich.haft`), Kurs (Karte 2, `vergleich.kurs`), Hundesteuer (Karte 4, `vergleich.steuer`), Leine im Wald (`vergleich.wald`). Jeder Schritt zeigt: den Titel der Karte in der Sprache der Seite als Link auf ihren Anker, die Marke der Karte als Chip in ihrem Ton (wie in den Tabellen der Themenseiten) und den Text aus `vergleich`, unverändert. Beim Wald: Titel aus `TEXTE` («Leine im Wald», «Laisse en forêt», «Guinzaglio nel bosco»), Chip und Ton wie in `seite_thema()` für das Thema `leinenpflicht-wald`, Link auf `#wald`. Die festen Texte behaupten nie eine Pflicht: Ob etwas Pflicht ist, sagen nur Chip und Text des Kantons.
  3. Darstellung mit den vorhandenen Bausteinen und Farben (`assets/site.css`, `DESIGN.md`), ruhig und knapp: eine Zeile je Schritt, auf dem Handy untereinander. Keine neuen Farben, keine neue Schrift.
  4. Sprunglink «Zum Inhalt» am Anfang jeder Seite, für Tastatur und Screenreader, in drei Sprachen («Zum Inhalt», «Aller au contenu», «Vai al contenuto»): erstes Element im `body`, sichtbar erst bei Fokus, Ziel ist der Hauptinhalt (`id` am `main` oder am ersten Abschnitt). Kleiner Umbau in `seite()` und `assets/site.css`.
  5. Texte in `TEXTE` für `de`, `fr`, `it`. Französisch und Italienisch nach `handbuch/uebersetzungen.md` (Anrede, Wortwahl). In der Fusszeile oder Themenleiste ändert sich nichts.
  6. Test (`tests/seiten.js`): Jede Kantonsseite in jeder Sprache hat genau einen Abschnitt `#neuer-hund` mit genau sechs Schritten. Jeder Link eines Schritts führt auf eine `id`, die es auf derselben Seite genau einmal gibt. Keine `id` kommt auf einer Seite doppelt vor. Jede Seite hat den Sprunglink, und sein Ziel gibt es.
  7. Ansehen: die Kantonsseiten Zürich (deutsch), Genf (französisch) und Tessin (italienisch) als Bild, einmal breit und einmal mit 390 Pixeln Breite. Erst pushen, wenn der Abschnitt ordentlich aussieht und nichts überläuft.
  8. Handbuch: `handbuch/generator.md` bekommt den Abschnitt «Neu einen Hund und Sprunglink» (wie es gebaut ist, die festen `id`). In `CLAUDE.md` nur ein Satz bei «Datenfelder Kanton», dass die Kantonsseite aus `karten` und `vergleich` den Abschnitt «Neu einen Hund» baut und `vergleich` darum auch dort erscheint. Lehnt die Umgebung die Änderung an `CLAUDE.md` ab: nicht wiederholen, im Protokoll festhalten, der Umbau gilt trotzdem als erledigt.
  9. Danach in Abschnitt 10 den Punkt 5 abhaken. Im Bericht die Adresse nennen, die ein Tierheim verlinken kann: `https://gassi-kompass.ch/<kt>/#neuer-hund`.

## Archiviert am 2026-11-28

### BACKLOG.md, 5. Umbauten am Generator

- [x] **Rechtstexte für den Wächter und für den Lauf** 2026-11-28: gebaut vom Lauf, Handbuch in der Sitzung nachgeführt. Entscheid von Joss vom 28.11.2026, 02:43 Uhr: Ein Erlass vom Zweig `wandel` gilt als im Lauf abgerufen, wenn sein Abruf höchstens 8 Tage alt ist (Qualitätsregel 2, `handbuch/freigaben.md`).

### BACKLOG.md, 9.1 Hund vermisst oder gefunden

- [x] Schwyz 2026-11-28
- [x] Jura 2026-11-28
- [x] Obwalden 2026-11-28
- [x] Uri 2026-11-28

## Archiviert am 2026-11-28

### BACKLOG.md, 9.1 Hund vermisst oder gefunden

- [x] Graubünden (deutsch und italienisch) 2026-11-28
- [x] Neuenburg 2026-11-28
- [x] Basel-Stadt 2026-11-28

### backlog/luecken.md, Offene Lücken

- [x] Riehen: Orte mit Hundeverbot und mit Leinenpflicht aus der Liste «Hundeverbots- und Leinenpflichtzonen» des Gesundheitsdepartements (`bs_zonen`) als Karten «Kein Zutritt» und «Leine» ergänzen. Die Liste nennt für Riehen elf Orte mit Hundeverbot und sieben mit Leinenpflicht (abgerufen am 26.11.2026). Erledigt 2026-11-28 (Auftrag `luecken-1`): elf Orte mit Hundeverbot, sieben mit Leinenpflicht, in der Sitzung an der Liste gegengelesen.
- [x] Kanton Genf: Zuschlagsrappen der Gemeinden zur Hundesteuer nachtragen, auch für die Stadt Genf. Die Liste ist ein PDF (ge.ch/document/impots-chiens-centimes-additionnels, Stand 17. März 2025). Im Browser war sie am 27.11.2026 nicht lesbar (ge.ch lässt das Leseprogramm nicht zu), der Download-Link ist für WebFetch nicht freigegeben. Die Seite verlinkt das Dokument als Quelle. Das PDF «Liste des races» ist nicht gelesen, massgebend ist Art. 17 RChiens. Stand 28.11.2026: WebFetch liest die Tabelle über den Link «télécharger» der Seite (`ge.ch/document/110/telecharger`). Gelesen: Genève-Ville 100, Carouge 100, Lancy 50, Vernier 50, je für 2021 bis 2025. Die Zeile Meyrin hat nur vier Werte. Lancy, Vernier und Carouge nennen ihren Zuschlag schon auf ihrer Seite, Kanton und Stadt Genf noch nicht. Erledigt 2026-11-28 (Auftrag `luecken-1`): Die Stadt Genf hat eine Karte zur Hundesteuer mit 100 centimes additionnels, die Karte des Kantons nennt den Zuschlag schon.
