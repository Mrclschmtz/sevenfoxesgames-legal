#!/usr/bin/env python3
"""Statischer Generator für sevenfoxes.de – ohne Abhängigkeiten.

    python3 build.py

Liest die Inhalte aus site/ (Texte je Sprache in site/i18n/, Seitenaufbau in
site/pages.py, Rechtstexte als fertiges HTML in site/legal/) und schreibt die
fertigen HTML-Dateien ins Repo-Wurzelverzeichnis, das GitHub Pages ausliefert.
Die generierten Dateien werden mit eingecheckt – Pages baut nichts selbst
(.nojekyll), es gibt also keinen Build-Schritt auf GitHub-Seite.

Sprachen: Deutsch liegt in der Wurzel, Englisch unter /en/, Spanisch unter /es/.
Die Datenschutz-URLs /quizerra/, /quizerra-kids/ und /bumblossom/ sind in der veröffentlichten
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
# Cache-Buster für site.css (GitHub Pages cached Assets 10 Min.) – bei CSS-Änderungen hochzählen.
CSS_VERSION = "20261006b"
BASE_URL = "https://sevenfoxes.de"

# Seitenschlüssel → Pfad je Sprache (immer mit abschließendem Slash, "" = Wurzel).
SLUGS = {
    "home":          {"de": "",               "en": "en/",                "es": "es/"},
    "apps":          {"de": "apps/",          "en": "en/apps/",           "es": "es/apps/"},
    "quizerra":      {"de": "apps/quizerra/", "en": "en/apps/quizerra/",  "es": "es/apps/quizerra/"},
    "kids":          {"de": "apps/quizerra-kids/", "en": "en/apps/quizerra-kids/", "es": "es/apps/quizerra-kids/"},
    "bumblossom":    {"de": "apps/bumblossom/", "en": "en/apps/bumblossom/", "es": "es/apps/bumblossom/"},
    "contact":       {"de": "kontakt/",       "en": "en/contact/",        "es": "es/contacto/"},
    "imprint":       {"de": "impressum/",     "en": "en/legal-notice/",   "es": "es/aviso-legal/"},
    "privacy":       {"de": "datenschutz/",   "en": "en/privacy/",        "es": "es/privacidad/"},
    # Die App-Rechtstexte sind dreisprachig in EINEM Dokument (Sprachanker #de/#en/#es).
    # Die Kopien unter /en/ und /es/ tragen nur die Navigation in der jeweiligen Sprache;
    # kanonisch bleibt die Wurzel-URL.
    "legal-quizerra": {"de": "quizerra/",      "en": "en/quizerra/",       "es": "es/quizerra/"},
    "legal-kids":     {"de": "quizerra-kids/", "en": "en/quizerra-kids/",  "es": "es/quizerra-kids/"},
    "legal-bumblossom": {"de": "bumblossom/",  "en": "en/bumblossom/",     "es": "es/bumblossom/"},
    # Ziel der Duell-Einladung aus der Quizerra-App (DuelInvite.swift, ?c=<Code>) – Pfade nicht ändern.
    "duel":           {"de": "duell/",         "en": "en/duel/",           "es": "es/duelo/"},
}
CANONICAL_LANG = {"legal-quizerra": "de", "legal-kids": "de", "legal-bumblossom": "de"}
# Seiten ohne Launch-Banner und ohne Sitemap-Eintrag (noindex): nur über einen geteilten Link erreichbar.
UNLISTED = {"duel"}
COUNTER_SNIPPET = '<script data-goatcounter="https://sevenfoxes.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n'
NO_COUNTER = {"legal-kids"}


def url(key, lang):
    return "/" + SLUGS[key][lang]


def load_strings(lang):
    return importlib.import_module(f"i18n.{lang}").T


def nav_html(t, lang, current):
    items = [("apps", t["nav_apps"]), ("contact", t["nav_contact"])]
    out = []
    for key, label in items:
        cls = ' class="is-current"' if key == current or (key == "apps" and current in ("quizerra", "kids", "bumblossom")) else ""
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


def banner_html(t, lang, key):
    """Launch-Banner – auf allen Seiten außer den App-Rechtstexten: Bumblossom (01.10.2026) über
    Quizerra Kids (08.10.2026). Jedes blendet sich nach seinem Stichtag selbst aus, falls die Seite
    bis dahin nicht neu gebaut wurde."""
    if key in CANONICAL_LANG or key in UNLISTED:
        return ""
    out = []
    # Bumblossom-Events: alle im HTML, sichtbar nur im eigenen Zeitraum (Skript unten); ohne Skript bleiben sie verborgen
    for k, von, bis in pages.EVENTS:
        out.append(f'''<a class="launch-banner bb ev" href="{url("bumblossom", lang)}#events" data-from="{von}" data-until="{bis}" hidden>
  <span class="wrap">
    <img src="/assets/img/bumblossom/events/icon_{k}.png" alt="" width="40" height="40" loading="lazy">
    <span class="launch-text"><b>{t[f"ev_{k}_title"]}</b> {t[f"banner_ev_{k}"]}</span>
    <span class="launch-cta">{t["btn_more"]} &rarr;</span>
  </span>
</a>''')
    # Bumblossom: vor dem Launch „erscheint am 1. Oktober“, danach zwei Wochen „ist da“
    if pages.BUMBLOSSOM_LIVE:
        href, until, rel = pages.APP_STORE_BUMBLOSSOM, "2026-10-15T07:00:00Z", True
        title, text, cta = t["banner_b_live_title"], t["banner_b_live_text"], t["btn_store"]
    else:
        href, until, rel = url("bumblossom", lang), "2026-10-01T07:00:00Z", False
        title, text, cta = t["banner_b_title"], t["banner_b_text"], t["btn_more"]
    out.append(f'''<a class="launch-banner bb" href="{href}" data-until="{until}"{" rel=\"noopener\"" if rel else ""}>
  <span class="wrap">
    <img src="/assets/img/bumblossom/bee_y.png" alt="" width="40" height="40" loading="lazy">
    <span class="launch-text"><b>{title}</b> {text}</span>
    <span class="launch-cta">{cta} &rarr;</span>
  </span>
</a>''')
    if pages.KIDS_LIVE:
        # Nach dem Launch: zwei Wochen „Jetzt im App Store", dann verschwindet das Banner.
        href, until = pages.APP_STORE_KIDS, "2026-10-22T07:00:00Z"
        title, text, cta = t["banner_live_title"], t["banner_live_text"], t["btn_store"]
    else:
        href, until = url("kids", lang), "2026-10-08T07:00:00Z"
        title, text, cta = t["banner_kids_title"], t["banner_kids_text"], t["btn_more"]
    out.append(f'''<a class="launch-banner" href="{href}" data-until="{until}"{" rel=\"noopener\"" if pages.KIDS_LIVE else ""}>
  <span class="wrap">
    <img src="/assets/img/kids/ella-{"cheer" if pages.KIDS_LIVE else "happy"}.png" alt="" width="40" height="40" loading="lazy">
    <span class="launch-text"><b>{title}</b> {text}</span>
    <span class="launch-cta">{cta} &rarr;</span>
  </span>
</a>''')
    return "\n".join(out) + '''
<script>(function(){var q=new URLSearchParams(location.search).get("jetzt"),n=q?Date.parse(q):Date.now();document.querySelectorAll(".launch-banner").forEach(function(b){
if(n>Date.parse(b.dataset.until)||(b.dataset.from&&n<Date.parse(b.dataset.from)))b.remove();else b.hidden=false;});})();</script>'''


def footer_html(t, lang):
    legal = [
        ("imprint", t["nav_imprint"]),
        ("privacy", t["nav_privacy_site"]),
        ("legal-quizerra", t["nav_privacy_quizerra"]),
        ("legal-kids", t["nav_privacy_kids"]),
        ("legal-bumblossom", t["nav_privacy_bumblossom"]),
    ]
    links = []
    for key, label in legal:
        href = url(key, lang) + (f"#{lang}" if key in CANONICAL_LANG else "")
        links.append(f'<a href="{href}">{label}</a>')
    return "\n        ".join(links)


# Strukturierte Daten (schema.org, JSON-LD) und Apples Smart-App-Banner für Google bzw. Safari.
# Bewusst ohne Bewertungen (aggregateRating): die Sterne stammen aus dem App Store, nicht von dieser Seite.
APPS_META = {
    "quizerra":   {"name": "Quizerra", "id": "6789493203", "icon": "/assets/img/quizerra/icon.png",
                   "genre": "Quiz", "devices": "iPhone, iPad"},
    "kids":       {"name": "Quizerra Kids", "id": "6808029347", "icon": "/assets/img/kids/icon.png",
                   "genre": "Educational", "devices": "iPhone, iPad"},
    "bumblossom": {"name": "Bumblossom", "id": "6815565230", "icon": "/assets/img/bumblossom/icon.png",
                   "genre": "Puzzle", "devices": "iPhone"},
}
ORG = {
    "@type": "Organization",
    "name": "SevenFoxes Games",
    "url": BASE_URL + "/",
    "logo": BASE_URL + "/assets/apple-touch-icon.png",
    "email": "kontakt@sevenfoxes.de",
    "sameAs": ["https://www.instagram.com/sevenfoxes_games/"],
}


def structured_html(key, lang, page):
    import json
    data = None
    banner = ""
    if key == "home":
        data = {"@context": "https://schema.org", **ORG}
    elif key in APPS_META:
        a = APPS_META[key]
        data = {
            "@context": "https://schema.org",
            "@type": "MobileApplication",
            "name": a["name"],
            "description": page["description"],
            "url": BASE_URL + url(key, lang),
            "image": BASE_URL + a["icon"],
            "operatingSystem": "iOS",
            "applicationCategory": "GameApplication",
            "applicationSubCategory": a["genre"],
            "availableOnDevice": a["devices"],
            "installUrl": f"https://apps.apple.com/app/id{a['id']}",
            "inLanguage": lang,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
            "publisher": {"@type": "Organization", "name": ORG["name"], "url": ORG["url"]},
        }
        banner = f'<meta name="apple-itunes-app" content="app-id={a["id"]}">\n'
    if not data:
        return ""
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return banner + f'<script type="application/ld+json">{js}</script>\n'


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
        "{{banner}}": banner_html(t, lang, key),
        "{{cssv}}": CSS_VERSION,
        "{{footer}}": footer_html(t, lang),
        "{{footer_claim}}": t["footer_claim"],
        "{{skip}}": t["skip_to_content"],
        "{{brand_alt}}": "SevenFoxes Games",
        "{{og_image}}": BASE_URL + page.get("og_image", "/assets/og-default.png"),
        "{{robots}}": f'<meta name="robots" content="{page["robots"]}">\n' if page.get("robots") else "",
        # Cookielose Besucherzählung (GoatCounter, Datenschutz Ziffer 4) – nicht auf der Datenschutzseite
        # von Quizerra Kids, die aus der Kinder-App verlinkt ist (Apple Kids-Kategorie: keine Analyse-Dienste).
        "{{counter}}": "" if key in NO_COUNTER else COUNTER_SNIPPET,
        "{{structured}}": structured_html(key, lang, page),
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
        if key in UNLISTED:
            continue
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
