# Gassi-Kompass

Quelltext der Website [gassi-kompass.ch](https://gassi-kompass.ch): Hunderegeln der Schweiz nach Kanton und Gemeinde, mit amtlicher Quelle zu jeder Angabe. Privates Projekt, kein Angebot eines Kantons oder einer Gemeinde.

## Bauen

```
python3 build.py        # Daten prüfen und Seiten erzeugen
node tests/seiten.js    # gebaute Seiten im Browser prüfen (braucht Playwright)
```

Die Daten liegen in `data/`. Wie sie gepflegt werden, steht in `CLAUDE.md`, was als Nächstes ansteht in `BACKLOG.md`, was sich geändert hat in `CHANGELOG.md`.

## Schriften

Archivo (Omnibus-Type) und IBM Plex Mono (IBM), beide unter der SIL Open Font License 1.1. Die Lizenztexte liegen in `assets/fonts/`.
