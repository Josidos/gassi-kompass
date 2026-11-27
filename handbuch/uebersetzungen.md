# Handbuch: Übersetzungen und Sprachfassungen

Teil des Arbeitshandbuchs `CLAUDE.md` und genauso verbindlich. Lies diese Datei ganz, bevor du eine Datei übersetzt oder eine französische oder italienische Originalfassung schreibst. Nennt ein Verweis einen Abschnitt ohne Datei, steht er in `CLAUDE.md` oder in einer anderen Datei unter `handbuch/`: Die Tabelle «Weitere Teile des Handbuchs» in `CLAUDE.md` sagt, was wo steht.

## Alle Sprachen überall

Entscheid von Joss vom 18. November 2026: Wer in der Schweiz wohnt, soll die Regeln seines Ortes in seiner Sprache lesen können, egal welche Amtssprache am Ort gilt. Jede Seite gibt es deshalb auf Deutsch, Französisch und Italienisch: Kantone, Gemeinden, Bund, Themenseiten, Startseite und «Über diese Seite». Dieser Abschnitt geht älteren Sätzen im Handbuch vor, die Übersetzungen ausschliessen.

### Originalfassung und Übersetzung

- **Originalfassung:** die Datei in einer Amtssprache des Ortes, ohne das Feld `uebersetzt_aus`. Ihre Texte stammen aus den amtlichen Quellen in dieser Sprache. Zweisprachige Kantone haben zwei Originalfassungen (BE, FR und VS deutsch und französisch, GR deutsch und italienisch). Für den Bund gibt es drei: `data/schweiz.json`, `data/fr-ch/schweiz.json` und `data/it-ch/schweiz.json`, jede aus den Seiten des Bundes in ihrer Sprache.
- **Übersetzung:** die Datei in einer Sprache, die am Ort nicht Amtssprache ist. Sie liegt dort, wo auch eine Originalfassung dieser Sprache läge (`data/fr-ch/kantone/zh.json`, `data/it-ch/gemeinden/zh/zuerich.json`, `data/kantone/vd.json`). Sie trägt `uebersetzt_aus` (Sprache der Originalfassung: `de`, `fr` oder `it`) und `original` (Prüfsumme der Originalfassung zum Zeitpunkt der Übersetzung). Gibt es zwei Originalfassungen, wird aus der deutschen übersetzt.
- **Gleicher Aufbau.** Eine Übersetzung hat dieselben Felder wie ihre Originalfassung, in jeder Liste gleich viele Einträge in derselben Reihenfolge und dieselben Werte in `id`, `kanton`, `kurz`, `bfs`, `ton`, `saison`, `von`, `bis` und in allen Quellenlisten. Sie braucht keine eigene Recherche und keine neuen Quellen.
- **Was die Übersetzung nicht enthält:** `geprueft` (der Generator nimmt das Prüfdatum der Originalfassung) und bei Kantonen `name`, `im`, `des` (der Generator setzt sie aus `kantonsformen()` in `build.py` ein: «Canton de Zurich», «dans le canton de Zurich», «du canton de Zurich», «Cantone di Zurigo», «Kanton Waadt»).
- **Zahlen bleiben Ziffern.** Jeder Betrag, jedes Datum, jede Frist, jeder Abstand und jede Artikelnummer steht in der Übersetzung mit denselben Ziffern wie im Original, im Format der Zielsprache («1er avril», «1° aprile», «CHF 120»). `build.py` vergleicht die Zahlen Feld für Feld und meldet jede Abweichung als Fehler. Darum: Steht im Original eine Ziffer, steht sie auch in der Übersetzung («1 Jahr» wird «1 an», nicht «un an»). Steht im Original ein Zahlwort, bleibt es ein Zahlwort. Ein Datum in Ziffern bleibt in Ziffern («1.4. bis 31.7.» wird «du 1.4. au 31.7.» oder «dal 1.4. al 31.7.»).
- **Eigennamen.** Namen von Gesetzen, Verordnungen, Reglementen, Ämtern und amtlichen Listen bleiben in der Originalsprache. Beim ersten Vorkommen darf eine kurze Übersetzung in Klammern folgen: «selon le Hundegesetz (loi sur les chiens)», «Stadtpolizei Zürich (police municipale)». Namen von Hunderassen bleiben, wie sie sind. Kantone heissen wie in `KANTONSNAMEN`. Orte behalten den amtlichen Namen, ausser die Zielsprache hat einen gebräuchlichen eigenen (Zurich, Zurigo, Bâle, Basilea, Lucerne, Lucerna, Saint-Gall, San Gallo, Coire, Coira, Berne, Berna, Genf, Ginevra, Neuenburg, Freiburg, Friburgo, Sitten, Soleure, Soletta, Schaffhouse, Sciaffusa, Winterthour). Heisst eine Gemeinde wie ihr Kanton, heisst sie wie in `KANTONSNAMEN` (Glaris, Glarona, Schwytz, Svitto, Zoug, Zugo). Im Zweifel der amtliche Name.
- **Gemeinden:** `name`, `ort` und `in_ort` stehen in der Zielsprache, so wie die Originalfassungen dieser Sprache sie schreiben: «Ville de Zurich», «Zurich», «à Zurich». «Città di Zurigo», «Zurigo», «a Zurigo». «Stadt Lausanne», «Lausanne», «in Lausanne». Die Kartentitel folgen den üblichen Titeln der Zielsprache (siehe «Französische und italienische Daten»), bei Kantonen den sechs festen Titeln.
- **Sprache.** Übersetze den Sinn Satz für Satz, ohne etwas wegzulassen, zu ergänzen oder zu verschärfen. Aus «kann» wird nie «muss». Französisch mit «vous», Italienisch mit «tu», Deutsch mit «du» und Schweizer Rechtschreibung. Kurze Sätze wie im Original. `wald.wo` muss in die festen Sätze der Zielsprache passen: «Gilt jedes Jahr {wo}», «S'applique chaque année {wo}», «Vale ogni anno {wo}».
- **Wortwahl**, damit alle Seiten gleich klingen:

  | Deutsch | Français | Italiano |
  |---|---|---|
  | Leinenpflicht | laisse obligatoire | obbligo di guinzaglio |
  | Hundehaltende | détenteurs de chiens | chi detiene un cane, detentori di cani |
  | Haftpflichtversicherung | assurance responsabilité civile | assicurazione di responsabilità civile |
  | Hundesteuer, Hundetaxe | impôt sur les chiens | imposta sui cani |
  | Anmeldung, anmelden | annonce, annoncer | notifica, annunciare |
  | Übernahme des Hundes | prise en charge du chien | presa a carico del cane |
  | Wohngemeinde | commune de domicile | Comune di domicilio |
  | Zuzug in den Kanton | arrivée dans le canton | trasferimento nel Cantone |
  | Waldrand | lisière | margine del bosco |
  | Freilaufzone | espace de liberté pour chiens | area di svago per cani |
  | Zutrittsverbot | accès interdit | divieto di accesso |
  | Maulkorb | muselière | museruola |
  | Bewilligung | autorisation | autorizzazione |
  | Rasseliste | liste de races | elenco delle razze |
  | Kot | crottes | escrementi |
  | Schilder vor Ort | signalisation sur place | segnaletica sul posto |
  | Busse | amende | multa |
  | Pflicht, keine Pflicht (Marke) | Obligatoire, Pas d'obligation | Obbligo, Nessun obbligo |
  | Gemeinde, Kanton, Bund | commune, canton, Confédération | Comune, Cantone, Confederazione |
  | Listenhunde | chiens de la liste | cani dell'elenco |
  | potenziell gefährliche Hunde | chiens potentiellement dangereux | cani potenzialmente pericolosi |
  | bewilligungspflichtig | soumis à autorisation | soggetto ad autorizzazione |
  | Halteberechtigung | autorisation de détention | autorizzazione di detenzione |
  | Ordnungsbusse | amende d'ordre | multa disciplinare |
  | Wesenstest, Wesensprüfung | test de comportement | test caratteriale |
  | Sachkundenachweis | attestation de compétences | attestato di competenza |
  | Wildruhezone, Wildruhegebiet | zone de tranquillité pour la faune | zona di tranquillità per la selvaggina |
  | Jagdbanngebiet | district franc fédéral | bandita federale di caccia |
  | Nutzhund, Hofhund | chien d'utilité, chien de ferme | cane da utilità, cane da fattoria |
  | Gebühr | émolument | tassa |
  | Merkblatt | notice | promemoria |
  | Ersthaltende | personnes qui détiennent un chien pour la première fois | chi detiene un cane per la prima volta |

  Weitere Entscheide zur Wortwahl stehen in den Einträgen der «Kette Übersetzungen» vom 18. November 2026 im Archiv des Protokolls. Wer unsicher ist, sucht dort: `grep -n "Wortwahl" changelog/2026-11.md`.

- **Muster:** `data/fr-ch/kantone/zh.json`, `data/it-ch/kantone/zh.json`, `data/fr-ch/gemeinden/zh/zuerich.json` und `data/it-ch/gemeinden/zh/zuerich.json`, jeweils neben der Originalfassung unter `data/kantone/` und `data/gemeinden/` zu lesen. Für die Wortwahl im Französischen und Italienischen zusätzlich eine Originalfassung dieser Sprache (`data/fr-ch/kantone/vd.json`, `data/it-ch/kantone/ti.json`).
- **Kennzeichnung.** Der Generator setzt unter den Titel jeder übersetzten Seite den Hinweis, dass sie eine Übersetzung ist und in welcher Sprache die amtlichen Quellen sind, mit Link zur Originalfassung. Die Namen der Quellen bleiben in der Originalsprache.
- **Veraltet.** Ändert sich die Originalfassung, stimmt die Prüfsumme nicht mehr. Der Generator zeigt dann auf der übersetzten Seite den Hinweis, dass die Originalfassung neuer ist. Eine veraltete Übersetzung wird nicht mehr mit dem Original verglichen, bis sie nachgeführt ist.

### So entsteht eine Übersetzung

1. `python3 build.py --fehlend` nennt pro Zeile: Stand (`veraltet` oder `fehlt`), Zielsprache, Zieldatei, Sprache und Datei der Originalfassung und deren Prüfsumme. Die Liste ist schon geordnet: veraltete zuerst, Kantone vor Gemeinden, grosse Kantone zuerst. Eine Gemeinde braucht die Kantonsdatei in derselben Sprache, darum zuerst die Kantone.
2. Die Originalfassung lesen. Die Zieldatei mit demselben Aufbau anlegen: `uebersetzt_aus` und `original` (die Prüfsumme aus der Liste) ergänzen, `geprueft` und bei Kantonen `name`, `im`, `des` weglassen, alle Texte übersetzen.
3. `python3 build.py --check`. Jede Meldung nennt Datei, Feld und was abweicht. Beheben, bis keine Meldung mehr kommt. Nie eine Zahl im Original ändern, um eine Meldung loszuwerden.
4. Veraltete Übersetzung: Originalfassung und Übersetzung nebeneinander lesen, die geänderten Stellen nachführen, `original` auf die neue Prüfsumme setzen.

### Im Lauf

- Jeder Lauf führt nach dem Ausbauen die Übersetzungen nach: zuerst veraltete, dann fehlende, höchstens 12 Dateien pro Lauf. Wer eine Originalfassung anlegt oder ändert, übersetzt sie im selben Lauf in die beiden anderen Sprachen.
- Nachgeprüft (Schritt 2 des Laufs) werden nur Originalfassungen. Ändert sich dabei eine Angabe, wird die Übersetzung im selben Lauf nachgeführt.
- Vor dem Übersetzen die Muster lesen und Wortwahl und Aufbau übernehmen.
- Nach dem Übersetzen: `python3 build.py` und `node tests/seiten.js`. Der Test prüft, dass jede übersetzte Seite den Hinweis trägt.

## Französische und italienische Daten

Seit dem Umbau vom 18. November 2026 baut der Generator die Dateien unter `data/fr-ch/` und `data/it-ch/` wie die deutschen. Für sie gilt, zusätzlich zum Abschnitt «Französisch und Italienisch» in `handbuch/generator.md`:

- Ablage: `data/fr-ch/kantone/<kt>.json` und `data/fr-ch/gemeinden/<kt>/<gemeinde>.json`, italienisch unter `data/it-ch/`. Gleiche Felder und gleiche `id` wie in den deutschen Mustern.
- Alle Texte stehen in der Sprache der Seite. In einer Amtssprache des Ortes stammen sie aus den amtlichen Quellen in dieser Sprache (Originalfassung). In den anderen Sprachen sind sie eine gekennzeichnete Übersetzung der Originalfassung, siehe «Alle Sprachen überall». `name`, `im` und `des` in der Sprache der Seite («Canton de Vaud», «dans le canton de Vaud», «du canton de Vaud»; «Cantone Ticino», «nel Cantone Ticino», «del Cantone Ticino»), bei Gemeinden `in_ort` («à Lausanne», «a Lugano»).
- Die Schlüssel der Felder (`wald`, `leine`, `verbot`, `karten`, `vergleich`, `ton` und so weiter) bleiben deutsch. Nur die Werte sind französisch oder italienisch.
- Sechs Karten in der Reihenfolge des deutschen Musters. Titel französisch: Responsabilité civile, Cours, Annonce, Impôt sur les chiens, Races, En promenade. Titel italienisch: Responsabilità civile, Corso, Notifica, Imposta sui cani, Razze, A passeggio. Übliche Titel bei Gemeinden französisch: Impôt sur les chiens, Laisse, Accès interdit, Annonce, Amendes. Italienisch: Imposta sui cani, Guinzaglio, Accesso vietato, Notifica, Multe.
- Prüfen wie bei deutschen Dateien: `python3 build.py`, dann `node tests/seiten.js`. `build.py` verlangt je Sprache die Kartentitel dieser Sprache. Eine Gemeinde braucht die Kantonsdatei in derselben Sprache.
- Bei einem zweisprachigen Kanton (BE, FR, VS) liegt die deutsche Fassung wie üblich unter `data/kantone/`. Eine Gemeinde hat Originalfassungen nur in ihren eigenen Amtssprachen, die übrigen Fassungen sind Übersetzungen. Dieselbe Gemeinde hat in jeder Sprache dieselbe `id` und dieselbe `bfs`: Darüber verbindet der Generator die Sprachfassungen.
