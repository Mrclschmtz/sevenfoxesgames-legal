#!/usr/bin/env python3
"""Statischer Generator für sevenfoxes.de – ohne Abhängigkeiten.

    python3 build.py

Liest die Inhalte aus site/ (Texte je Sprache in site/i18n/, Seitenaufbau in
site/pages.py, Rechtstexte als fertiges HTML in site/legal/) und schreibt die
fertigen HTML-Dateien ins Repo-Wurzelverzeichnis, das GitHub Pages ausliefert.
Die generierten Dateien werden mit eingecheckt – Pages baut nichts selbst
(.nojekyll), es gibt also keinen Build-Schritt auf GitHub-Seite.

Sprachen: Deutsch liegt in der Wurzel, Englisch unter /en/, Spanisch unter /es/.
Die Datenschutz-URLs /quizerra/ und /quizerra-kids/ sind in der veröffentlichten
App, in App Store Connect und bei AdMob hinterlegt und dürfen sich NICHT ändern.
"""
import importlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SITE = ROOT / "site"
sys.path.insert(0, str(SITE))

import pages  # noqa: E402  (liegt in site/)

LANGS = ("de", "en", "es")
BASE_URL = "https://sevenfoxes.de"

# Seitenschlüssel → Pfad je Sprache (immer mit abschließendem Slash, "" = Wurzel).
SLUGS = {
    "home":          {"de": "",               "en": "en/",                "es": "es/"},
    "apps":          {"de": "apps/",          "en": "en/apps/",           "es": "es/apps/"},
    "quizerra":      {"de": "apps/quizerra/", "en": "en/apps/quizerra/",  "es": "es/apps/quizerra/"},
    "kids":          {"de": "apps/quizerra-kids/", "en": "en/apps/quizerra-kids/", "es": "es/apps/quizerra-kids/"},
    "contact":       {"de": "kontakt/",       "en": "en/contact/",        "es": "es/contacto/"},
    "imprint":       {"de": "impressum/",     "en": "en/legal-notice/",   "es": "es/aviso-legal/"},
    "privacy":       {"de": "datenschutz/",   "en": "en/privacy/",        "es": "es/privacidad/"},
    # Die App-Rechtstexte sind dreisprachig in EINEM Dokument (Sprachanker #de/#en/#es).
    # Die Kopien unter /en/ und /es/ tragen nur die Navigation in der jeweiligen Sprache;
    # kanonisch bleibt die Wurzel-URL.
    "legal-quizerra": {"de": "quizerra/",      "en": "en/quizerra/",       "es": "es/quizerra/"},
    "legal-kids":     {"de": "quizerra-kids/", "en": "en/quizerra-kids/",  "es": "es/quizerra-kids/"},
}
CANONICAL_LANG = {"legal-quizerra": "de", "legal-kids": "de"}


def url(key, lang):
    return "/" + SLUGS[key][lang]


def load_strings(lang):
    return importlib.import_module(f"i18n.{lang}").T


def nav_html(t, lang, current):
    items = [("apps", t["nav_apps"]), ("contact", t["nav_contact"])]
    out = []
    for key, label in items:
        cls = ' class="is-current"' if key == current or (key == "apps" and current in ("quizerra", "kids")) else ""
        out.append(f'<a href="{url(key, lang)}"{cls}>{label}</a>')
    return "\n      ".join(out)


def langswitch_html(key, lang):
    names = {"de": "DE", "en": "EN", "es": "ES"}
    full = {"de": "Deutsch", "en": "English", "es": "Español"}
    out = []
    for l in LANGS:
        href = url(key, l)
        if key in CANONICAL_LANG:
            href += f"#{l}"  # in den passenden Sprachabschnitt springen
        cur = ' aria-current="true"' if l == lang else ""
        out.append(f'<a href="{href}" hreflang="{l}" lang="{l}" title="{full[l]}"{cur}>{names[l]}</a>')
    return "".join(out)


def alternates_html(key):
    out = []
    for l in LANGS:
        out.append(f'<link rel="alternate" hreflang="{l}" href="{BASE_URL}{url(key, l)}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}{url(key, "de")}">')
    return "\n".join(out)


def footer_html(t, lang):
    legal = [
        ("imprint", t["nav_imprint"]),
        ("privacy", t["nav_privacy_site"]),
        ("legal-quizerra", t["nav_privacy_quizerra"]),
        ("legal-kids", t["nav_privacy_kids"]),
    ]
    links = []
    for key, label in legal:
        href = url(key, lang) + (f"#{lang}" if key in CANONICAL_LANG else "")
        links.append(f'<a href="{href}">{label}</a>')
    return "\n        ".join(links)


def build_page(template, key, lang, t):
    page = pages.render(key, lang, t, url)
    canonical_lang = CANONICAL_LANG.get(key, lang)
    html = template
    repl = {
        "{{lang}}": lang,
        "{{title}}": page["title"],
        "{{description}}": page["description"],
        "{{world}}": page.get("world", "studio"),
        "{{bodyclass}}": page.get("bodyclass", ""),
        "{{canonical}}": BASE_URL + url(key, canonical_lang),
        "{{alternates}}": alternates_html(key),
        "{{nav}}": nav_html(t, lang, key),
        "{{langswitch}}": langswitch_html(key, lang),
        "{{home}}": url("home", lang),
        "{{content}}": page["content"],
        "{{footer}}": footer_html(t, lang),
        "{{footer_claim}}": t["footer_claim"],
        "{{skip}}": t["skip_to_content"],
        "{{brand_alt}}": "SevenFoxes Games",
        "{{og_image}}": BASE_URL + page.get("og_image", "/assets/og-default.png"),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    leftover = [m for m in ("{{",) if m in html]
    if leftover:
        raise SystemExit(f"Unersetzter Platzhalter in {key}/{lang}")
    return html


def write_sitemap(entries):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key in SLUGS:
        for lang in LANGS:
            if key in CANONICAL_LANG and lang != CANONICAL_LANG[key]:
                continue
            lines.append("  <url>")
            lines.append(f"    <loc>{BASE_URL}{url(key, lang)}</loc>")
            for l in LANGS:
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{BASE_URL}{url(key, l)}"/>')
            lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")


def main():
    template = (SITE / "base.html").read_text()
    written = []
    for lang in LANGS:
        t = load_strings(lang)
        for key in SLUGS:
            html = build_page(template, key, lang, t)
            out = ROOT / SLUGS[key][lang] / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html)
            written.append(out.relative_to(ROOT))
    write_sitemap(written)
    for w in written:
        print(f"  {w}")
    print(f"{len(written)} Seiten geschrieben.")


if __name__ == "__main__":
    main()
