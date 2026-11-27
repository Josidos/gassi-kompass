#!/usr/bin/env python3
"""Baut den Wissensgraphen des Projekts mit Graphify nach graphify-out/.

    python3 tools/graph.py            baut graph.json und GRAPH_REPORT.md neu
    python3 tools/graph.py --pruefe   baut nur im Speicher und meldet Fehler in tools/graph_wissen.txt

Der Graph hat drei Schichten:

1. Code und Dokumente. Graphify liest build.py, tests/, tools/, assets/*.js, die Workflows und die
   Überschriften der Markdown-Dateien selbst. Das läuft lokal und ohne KI.
2. Daten. Kantone, Gemeinden, Quellen und ihre Server aus data/, geladen mit lade() aus build.py,
   damit der Graph dasselbe sieht wie der Generator.
3. Wissen. tools/graph_wissen.txt verbindet Abschnitte des Handbuchs mit Code und Daten und nennt
   Regeln, die sonst nur im Fliesstext stehen. Diese Datei wird von Hand gepflegt.

Der Graph ist ein Wegweiser und keine Quelle. Für Hunderegeln gelten allein die amtlichen Quellen,
für den Stand des Projekts die Dateien selbst.

Graphify muss installiert sein (pip install graphifyy). Fehlt es, endet das Skript mit einem Hinweis
und Code 0, damit ein Lauf deswegen nie scheitert.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
AUS = ROOT / "graphify-out"
WISSEN = ROOT / "tools" / "graph_wissen.txt"
DOKUMENTE = ["CLAUDE.md", "BACKLOG.md", "CHANGELOG.md", "DESIGN.md", "PRODUCT.md", "README.md"]
SPRACHEN = {"de": "Deutsch", "fr": "Französisch", "it": "Italienisch"}
# Begriffe der Datenschicht: Kennung -> Bezeichnung
BEGRIFFE = {
    "daten_kantone": "Kantonsdateien (data/kantone/ und die Sprachordner)",
    "daten_gemeinden": "Gemeindedateien (data/gemeinden/ und die Sprachordner)",
    "daten_quellen": "Quellenverzeichnis (data/quellen.json und data/quellen/*.json)",
    "feld_vermisst": "Feld vermisst: Hund vermisst oder gefunden",
    "feld_durchsicht": "Feld durchsicht: vom Amt durchgesehen",
    "feld_umzug": "Feld umzug: Zuzug in den Kanton",
    "feld_wald_feste_leinenzeit": "Leinenpflicht im Wald zu festen Daten (wald.saison)",
    "feld_wald_ganzjaehrig": "Leinenpflicht im Wald das ganze Jahr (wald.ganzjaehrig)",
    "feld_wald_keine_feste_zeit": "Keine feste Leinenzeit im Wald",
    "pflicht_haftpflicht": "Haftpflichtversicherung Pflicht für alle Hunde (Karte Haftpflicht, ton must)",
    "pflicht_kurs": "Kurspflicht (Karte Kurs, ton must)",
    "rasseliste": "Rasseliste mit Bewilligung oder Verbot (Karte Rassen, ton must)",
    "feld_freilaufzonen": "Freilaufzonen einer Gemeinde (freilaufzonen)",
    "feld_hinweis_heute": "Gemeinde strenger als der Kanton im Wald (hinweis_heute)",
    "karte_hundezonen": "Karte der Hundezonen (data/geo/)",
}


def kennung(text):
    """Kennung eines Knotens: Kleinbuchstaben, Ziffern und Unterstrich."""
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


class Schicht:
    """Sammelt Knoten und Kanten in der Form, die Graphify erwartet."""

    def __init__(self):
        self.nodes, self.edges, self.ids = [], [], set()

    def knoten(self, nid, label, typ, datei, **mehr):
        if nid in self.ids:
            return
        self.ids.add(nid)
        self.nodes.append({"id": nid, "label": label, "file_type": typ, "source_file": datei,
                           "source_location": None, "_origin": "semantic", **mehr})

    def kante(self, von, relation, nach, datei, sicher="EXTRACTED", wert=1.0):
        self.edges.append({"source": von, "target": nach, "relation": relation, "confidence": sicher,
                           "confidence_score": wert, "source_file": datei, "source_location": None,
                           "weight": 1.0, "_origin": "semantic"})


def schicht_code():
    """Schicht 1: Code und Überschriften der Dokumente, von Graphify selbst gelesen."""
    from graphify.detect import detect
    from graphify.extract import extract
    erkannt = detect(ROOT)
    dateien = [Path(f) for f in erkannt["files"]["code"] if not f.endswith(".json")]
    dateien += [ROOT / d for d in DOKUMENTE if (ROOT / d).is_file()]
    return erkannt, extract(sorted(set(dateien)), cache_root=ROOT, root=ROOT)


def quellen_in(daten):
    """Alle Quellenschlüssel, die eine Datendatei nennt."""
    gefunden = []

    def geh(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in ("quellen", "freilaufzonen_quellen") and isinstance(v, list):
                    gefunden.extend(q for q in v if isinstance(q, str))
                else:
                    geh(v)
        elif isinstance(x, list):
            for v in x:
                geh(v)

    geh(daten)
    return sorted(set(gefunden))


def schicht_daten():
    """Schicht 2: Kantone, Gemeinden, Quellen und ihre Server."""
    sys.path.insert(0, str(ROOT))
    sys.dont_write_bytecode = True  # kein __pycache__ im Wurzelordner, der veröffentlicht wird
    import build
    quellen, welt, _bund, _orte = build.lade()
    s = Schicht()
    for nid, label in BEGRIFFE.items():
        s.knoten(nid, label, "concept", "CLAUDE.md")
    for lang, name in SPRACHEN.items():
        s.knoten(f"sprache_{lang}", f"Originalfassung auf {name}", "concept", "CLAUDE.md")

    # Quellen und Server
    qdatei = {}
    for pfad in [ROOT / "data" / "quellen.json"] + sorted((ROOT / "data" / "quellen").glob("*.json")):
        for key in json.loads(pfad.read_text("utf-8")):
            qdatei.setdefault(key, str(pfad.relative_to(ROOT)))
    for key in sorted(quellen):
        q = quellen[key]
        datei = qdatei.get(key, "data/quellen.json")
        s.knoten(f"quelle_{kennung(key)}", f"{q.get('kurz', key)} [{key}]", "document", datei,
                 source_url=q.get("url"))
        s.kante("daten_quellen", "contains", f"quelle_{kennung(key)}", datei)
        host = urlsplit(q.get("url", "")).hostname
        if host:
            s.knoten(f"server_{kennung(host)}", f"Server {host}", "concept", datei)
            s.kante(f"quelle_{kennung(key)}", "hosted_on", f"server_{kennung(host)}", datei)

    namen = dict(build.KANTONE_ALLE)

    def stand(nid, d, datei):
        if d.get("geprueft"):
            s.knoten(f"stand_{kennung(d['geprueft'])}", f"Geprüft am {d['geprueft']}", "concept", "CLAUDE.md")
            s.kante(nid, "checked_on", f"stand_{kennung(d['geprueft'])}", datei)

    def zitiert(nid, d, datei):
        for key in quellen_in(d):
            if key in quellen:
                s.kante(nid, "cites", f"quelle_{kennung(key)}", datei)

    # Kantone: ein Knoten je Kanton, belegt durch die Originalfassung (bei zweien die deutsche)
    je_kanton = {}
    for lang in SPRACHEN:
        for d in welt[lang]["k"]:
            if "uebersetzt_aus" not in d:
                je_kanton.setdefault(d["id"], []).append((lang, d))
    for kid in sorted(je_kanton):
        fassungen = je_kanton[kid]
        lang, d = fassungen[0]
        datei, nid = d["_datei"], f"kanton_{kid}"
        s.knoten(nid, f"Kanton {namen.get(kid, kid)} ({kid.upper()})", "document", datei)
        s.kante("daten_kantone", "contains", nid, datei)
        for l, _ in fassungen:
            s.kante(nid, "original_in", f"sprache_{l}", datei)
        stand(nid, d, datei)
        zitiert(nid, d, datei)
        wald = d.get("wald", {})
        feld = ("feld_wald_feste_leinenzeit" if wald.get("saison") else
                "feld_wald_ganzjaehrig" if wald.get("ganzjaehrig") else "feld_wald_keine_feste_zeit")
        s.kante(nid, "has_field", feld, datei)
        for feld in ("vermisst", "umzug", "durchsicht"):
            if feld in d:
                s.kante(nid, "has_field", f"feld_{feld}", datei)
        karten = d.get("karten", [])
        for pos, begriff in ((0, "pflicht_haftpflicht"), (1, "pflicht_kurs"), (4, "rasseliste")):
            if len(karten) > pos and karten[pos].get("ton") == "must":
                s.kante(nid, "has_field", begriff, datei)

    # Gemeinden
    orte_de = {(g.get("kanton"), g.get("id")): g.get("ort") for g in welt["de"]["g"]}
    je_gemeinde = {}
    for lang in SPRACHEN:
        for g in welt[lang]["g"]:
            if "uebersetzt_aus" not in g:
                je_gemeinde.setdefault((g["kanton"], g["id"]), []).append((lang, g))
    for key in sorted(je_gemeinde):
        fassungen = je_gemeinde[key]
        lang, g = fassungen[0]
        kid, gid = key
        datei, nid = g["_datei"], f"gemeinde_{kid}_{kennung(gid)}"
        s.knoten(nid, f"{orte_de.get(key) or g.get('ort', gid)} (Gemeinde, {kid.upper()})", "document", datei)
        s.kante("daten_gemeinden", "contains", nid, datei)
        s.kante(nid, "part_of", f"kanton_{kid}", datei)
        for l, _ in fassungen:
            s.kante(nid, "original_in", f"sprache_{l}", datei)
        stand(nid, g, datei)
        zitiert(nid, g, datei)
        if g.get("freilaufzonen"):
            s.kante(nid, "has_field", "feld_freilaufzonen", datei)
        if g.get("hinweis_heute"):
            s.kante(nid, "has_field", "feld_hinweis_heute", datei)
        if (ROOT / "data" / "geo" / f"{kid}-{gid}.json").is_file():
            s.kante(nid, "has_field", "karte_hundezonen", datei)

    # Bund: drei Originalfassungen
    for lang in SPRACHEN:
        b = welt[lang].get("b")
        if not b:
            continue
        s.knoten("bund_schweiz", "Regeln des Bundes (Schweiz)", "document", b["_datei"])
        s.kante("bund_schweiz", "original_in", f"sprache_{lang}", b["_datei"])
        stand("bund_schweiz", b, b["_datei"])
        zitiert("bund_schweiz", b, b["_datei"])
    return s


def schicht_wissen(bekannt):
    """Schicht 3: tools/graph_wissen.txt. Gibt die Schicht und die Liste der Fehler zurück."""
    s, fehler = Schicht(), []
    kanten = []
    for nr, zeile in enumerate(WISSEN.read_text("utf-8").splitlines(), 1):
        zeile = zeile.split(" #")[0].strip() if not zeile.lstrip().startswith("#") else ""
        if not zeile:
            continue
        teile = [t.strip() for t in zeile.split("|")]
        if teile[0] == "K" and len(teile) == 4:
            _, nid, label, datei = teile
            if nid != kennung(nid) or not nid.startswith("wissen_"):
                fehler.append(f"Zeile {nr}: Kennung '{nid}' muss mit wissen_ beginnen und klein geschrieben sein")
            elif nid in bekannt or nid in s.ids:
                fehler.append(f"Zeile {nr}: Kennung '{nid}' gibt es schon")
            elif not (ROOT / datei).is_file():
                fehler.append(f"Zeile {nr}: Datei '{datei}' gibt es nicht")
            else:
                s.knoten(nid, label, "rationale", datei)
        elif teile[0] == "E" and len(teile) == 4:
            kanten.append((nr, teile[1], teile[2], teile[3]))
        else:
            fehler.append(f"Zeile {nr}: weder «K | Kennung | Text | Datei» noch «E | von | Relation | nach»")
    alle = bekannt | s.ids
    for nr, von, relation, nach in kanten:
        fehlt = [x for x in (von, nach) if x not in alle]
        if fehlt:
            fehler.append(f"Zeile {nr}: Knoten {', '.join(fehlt)} gibt es nicht (Tippfehler oder umbenannt?)")
        else:
            s.kante(von, relation, nach, "tools/graph_wissen.txt", "INFERRED", 0.95)
    return s, fehler


def namen_der_gruppen(G, gruppen):
    """Benennt jede Gruppe nach ihren zwei am stärksten verbundenen Knoten. Kommt ohne KI aus."""
    namen = {}
    for cid, knoten in gruppen.items():
        oben = sorted(knoten, key=lambda n: (-G.degree(n), n))[:2]
        text = " / ".join(str(G.nodes[n].get("label", n)) for n in oben)
        namen[cid] = text if len(text) <= 70 else text[:67] + "..."
    return namen


def main():
    try:
        from graphify.analyze import god_nodes, suggest_questions, surprising_connections
        from graphify.build import build_from_json
        from graphify.cluster import cluster, score_all
        from graphify.export import to_json
        from graphify.report import generate
    except ImportError:
        print("Graphify ist nicht installiert (pip install graphifyy). Der Graph bleibt, wie er ist.")
        return 0
    nur_pruefen = "--pruefe" in sys.argv

    erkannt, code = schicht_code()
    daten = schicht_daten()
    bekannt = {n["id"] for n in code["nodes"]} | daten.ids
    wissen, fehler = schicht_wissen(bekannt)
    if fehler:
        print("Fehler in tools/graph_wissen.txt:")
        for f in fehler:
            print("  " + f)
        return 1

    auszug = {"nodes": code["nodes"] + daten.nodes + wissen.nodes,
              "edges": code["edges"] + daten.edges + wissen.edges,
              "hyperedges": [], "input_tokens": 0, "output_tokens": 0}
    G = build_from_json(auszug, root=str(ROOT), directed=False)
    if G.number_of_nodes() == 0:
        print("Fehler: Der Graph ist leer.")
        return 1
    zeile = (f"{G.number_of_nodes()} Knoten, {G.number_of_edges()} Kanten "
             f"(Code und Dokumente {len(code['nodes'])}, Daten {len(daten.nodes)}, Wissen {len(wissen.nodes)})")
    if nur_pruefen:
        print("Graph in Ordnung: " + zeile)
        return 0

    gruppen = cluster(G)
    zusammenhalt = score_all(G, gruppen)
    namen = namen_der_gruppen(G, gruppen)
    zentral = god_nodes(G)
    ueberraschend = surprising_connections(G, gruppen)
    fragen = suggest_questions(G, gruppen, namen)
    AUS.mkdir(exist_ok=True)
    if not to_json(G, gruppen, str(AUS / "graph.json"), force=True, community_labels=namen):
        print("Fehler: graph.json wurde nicht geschrieben.")
        return 1
    bericht = generate(G, gruppen, zusammenhalt, namen, zentral, ueberraschend, erkannt,
                       {"input": 0, "output": 0}, str(ROOT), suggested_questions=fragen)
    (AUS / "GRAPH_REPORT.md").write_text(bericht, encoding="utf-8")
    (AUS / ".graphify_labels.json").write_text(
        json.dumps({str(k): v for k, v in namen.items()}, ensure_ascii=False), encoding="utf-8")
    print(f"Graph gebaut: {zeile}, {len(gruppen)} Gruppen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
