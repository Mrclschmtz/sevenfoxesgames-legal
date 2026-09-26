# sevenfoxes.de

Website von SevenFoxes Games – Studio-Seite, Produktseiten für Quizerra und
Quizerra Kids, Kontakt, Impressum und die Datenschutzerklärungen. Ausgeliefert
über GitHub Pages (Custom Domain `sevenfoxes.de`, siehe `CNAME`).

## Aufbau

```
build.py            Generator (Python 3, keine Abhängigkeiten)
site/base.html      Seitengerüst mit Header, Navigation, Sprachumschalter, Footer
site/pages.py       Aufbau der einzelnen Seiten
site/i18n/{de,en,es}.py   alle Texte je Sprache
site/legal/*.html   Datenschutzerklärungen der Apps (dreisprachig in EINER Datei)
assets/             Stylesheet, Schriften (selbst gehostet, OFL), Bilder, Logo
```

Alle `index.html` im Repo-Wurzelverzeichnis und unter `en/`, `es/`, `apps/` usw.
sind **generiert** und werden mit eingecheckt. Nach jeder Änderung an `site/`:

```bash
python3 build.py
```

Lokale Vorschau: `python3 -m http.server 8787` im Repo-Ordner, dann
http://localhost:8787/ – die Pfade sind absolut (`/assets/...`), deshalb
muss der Server im Repo-Wurzelverzeichnis laufen.

## Nicht ändern

- `/quizerra/` und `/quizerra-kids/` sind die Datenschutz-URLs, die in der
  veröffentlichten App, in App Store Connect und in der AdMob-Nachricht stehen.
- `CNAME` (Custom Domain) und `.nojekyll` (verhindert, dass GitHub die
  `{{…}}`-Platzhalter in `site/base.html` als Liquid interpretiert).
- Die Quizerra-Datenschutzerklärung liegt zusätzlich als eigenständige Kopie in
  `quizerra/Legal/index.html` im App-Repo; inhaltliche Änderungen dort nachziehen.

## Impressum

Die Pflichtangaben stehen in `site/pages.py` (`page_imprint`) und
`site/i18n/*.py`. Telefonnummer und Umsatzsteuer-Angaben werden nur gerendert,
wenn die Konstanten `PHONE`, `VAT_ID`, `W_ID` bzw. `SMALL_BUSINESS` oben in
`site/pages.py` gesetzt sind.

## Launch-Tag Quizerra Kids (08.10.2026)

Der Schalter `KIDS_LIVE` in `site/pages.py` steuert Store-Button (statt „Ab 8. Oktober"-Badge),
den Hinweistext auf der Kids-Seite und das Banner („Quizerra Kids ist da!", verschwindet am 22.10.
von selbst). Umschalten und veröffentlichen mit einem Befehl:

    python3 site/golive_kids.py --push

Vorher probebauen ohne Umschalten: `KIDS_LIVE=1 python3 build.py`.
