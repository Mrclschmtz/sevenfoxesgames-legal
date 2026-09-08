"""Seitenaufbau für sevenfoxes.de.

render(key, lang, t, url) liefert Titel, Beschreibung, Welt und den HTML-Inhalt
einer Seite. Die Texte kommen aus site/i18n/<lang>.py (Dict T), die Rechtstexte
der Apps liegen fertig in site/legal/. Keine Abhängigkeiten außer der Stdlib.
"""
import pathlib
import random

HERE = pathlib.Path(__file__).resolve().parent
APP_STORE_QUIZERRA = "https://apps.apple.com/app/id6789493203"
MAIL = "kontakt@sevenfoxes.de"

# Impressum-Angaben, die nur Marcel liefern kann. Solange None, wird die Zeile
# NICHT gerendert – lieber eine fehlende Zeile als ein Platzhalter auf der Live-Seite.
PHONE = "+49 1575 6548598"   # Geschaeftsrufnummer SevenFoxes Games (auch im DSA-Datensatz)
PHONE_LINK = "+4915756548598"
VAT_ID = None         # Umsatzsteuer-Identifikationsnummer nach § 27a UStG, falls vorhanden
SMALL_BUSINESS = True # Kleinunternehmer nach § 19 UStG (bestaetigt 2026-09-08), keine USt-IdNr.


# ---------- Bausteine ----------

def pixels(seed, count=26):
    """Pixel-Trenner: verstreute Quadrate wie die Fragmente am Logo-Fuchs.
    Deterministisch je Seed, damit jeder Build dieselbe Datei erzeugt."""
    rnd = random.Random(seed)
    rects = []
    for _ in range(count):
        s = rnd.choice((3, 4, 5, 6, 8, 10, 12))
        x = rnd.uniform(0, 100)
        y = rnd.uniform(0, 26 - s)
        o = rnd.uniform(.18, .9)
        rects.append(f'<rect x="{x:.1f}%" y="{y:.0f}" width="{s}" height="{s}" opacity="{o:.2f}"/>')
    return ('<svg class="pixels" viewBox="0 0 1080 26" preserveAspectRatio="none" aria-hidden="true" '
            'fill="currentColor">' + "".join(rects) + "</svg>")


def hero_pixels(seed=7, count=18):
    rnd = random.Random(seed)
    out = []
    for i in range(count):
        s = rnd.choice((5, 6, 8, 10, 12, 14))
        x = rnd.uniform(-260, 260)
        y = rnd.uniform(-170, 190)
        d = rnd.uniform(0, .5)
        r = rnd.uniform(-40, 40)
        out.append(f'<i style="--s:{s}px;--x:{x:.0f}px;--y:{y:.0f}px;--d:{d:.2f}s;--r:{r:.0f}deg"></i>')
    return '<div class="hero-pixels" aria-hidden="true">' + "".join(out) + "</div>"


def quizerra_word():
    return '<span class="display">QUIZ<b>ERRA</b></span>'


def kids_word():
    return ('<span class="display">QUIZ<b>ERRA</b> '
            '<span class="kids-word"><b>K</b><b>I</b><b>D</b><b>S</b></span></span>')


def store_button(t):
    return (f'<a class="btn btn-store" href="{APP_STORE_QUIZERRA}" rel="noopener">'
            f'<span class="apple" aria-hidden="true">&#63743;</span>'
            f'<span>{t["btn_store"]}<br><small>{t["btn_store_small"]}</small></span></a>')


def soon_badge(t):
    return f'<span class="soon">{t["kids_soon"]}</span>'


def facts(items):
    return "<ul class=\"facts\">" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def panel_quizerra(t, lang, url):
    return f'''
<article class="world-panel" data-world="noir" aria-labelledby="p-quizerra">
  <div class="panel-copy">
    <div class="app-name"><img src="/assets/img/quizerra/icon.png" alt="" width="64" height="64">
      <h3 id="p-quizerra">{quizerra_word()}</h3></div>
    <p class="app-sub">{t["q_subtitle"]}</p>
    <p>{t["q_teaser"]}</p>
    {facts(t["q_facts"])}
    <div class="actions">{store_button(t)}
      <a class="btn btn-ghost" href="{url("quizerra", lang)}">{t["btn_more"]}</a></div>
  </div>
  <div class="panel-art">
    <img class="device" src="/assets/img/quizerra/{lang}/hero-device.jpg" alt="{t["q_shot_alt"]}" width="560" height="1216" loading="lazy">
  </div>
</article>'''


def panel_kids(t, lang, url):
    return f'''
<article class="world-panel" data-world="sky" aria-labelledby="p-kids">
  <div class="panel-copy">
    <div class="app-name"><img src="/assets/img/kids/icon.png" alt="" width="64" height="64">
      <h3 id="p-kids">{kids_word()}</h3></div>
    <p class="app-sub">{t["k_subtitle"]}</p>
    <p>{t["k_teaser"]}</p>
    {facts(t["k_facts"])}
    <div class="actions">{soon_badge(t)}
      <a class="btn btn-ghost" href="{url("kids", lang)}">{t["btn_more"]}</a></div>
  </div>
  <div class="panel-art">
    <img class="device" src="/assets/img/kids/{lang}/hero-device.jpg" alt="{t["k_shot_alt"]}" width="560" height="1216" loading="lazy">
    <img class="ella" src="/assets/img/kids/ella-happy.png" alt="" loading="lazy">
    <img class="sticker" src="/assets/img/kids/sticker-space-1.png" alt="" style="right:-4%;top:6%;transform:rotate(12deg)" loading="lazy">
  </div>
</article>'''


def gallery(app, lang, names, alts):
    imgs = "".join(
        f'<img src="/assets/img/{app}/{lang}/{n}.jpg" alt="{a}" width="230" height="500" loading="lazy">'
        for n, a in zip(names, alts))
    return f'<div class="gallery">{imgs}</div>'


def features(items):
    return "<ul class=\"features\">" + "".join(f"<li><h3>{h}</h3><p>{p}</p></li>" for h, p in items) + "</ul>"


def chips(items, mix=None):
    li = "".join(f"<li>{c}</li>" for c in items)
    if mix:
        li += f'<li class="mix">{mix}</li>'
    return f'<ul class="chips">{li}</ul>'


def address_box(t):
    return (f'<div class="box"><address class="address">SevenFoxes Games<br>'
            f'{t["owner_label"]}: Marcel Krause<br>c/o Autorenglück #39534<br>'
            f'Albert-Einstein-Str. 47<br>02977 Hoyerswerda, {t["country"]}<br>'
            f'{t["email_label"]}: <a href="mailto:{MAIL}">{MAIL}</a></address></div>')


# ---------- Seiten ----------

def page_home(t, lang, url):
    principles = "".join(f'<div class="principle"><h3>{h}</h3><p>{p}</p></div>' for h, p in t["home_principles"])
    content = f'''
<section class="hero wrap">
  {hero_pixels()}
  <img class="logo-full" src="/assets/logo-full.svg" alt="SevenFoxes Games" width="420" height="349">
  <h1>{t["home_claim"]}</h1>
  <p class="lead">{t["home_sub"]}</p>
</section>
<div class="wrap">{pixels("home-1")}</div>

<section class="section wrap" id="apps">
  <div class="section-head">
    <p class="eyebrow">{t["home_apps_eyebrow"]}</p>
    <h2>{t["home_apps_title"]}</h2>
  </div>
  {panel_quizerra(t, lang, url)}
  {panel_kids(t, lang, url)}
</section>
<div class="wrap">{pixels("home-2")}</div>

<section class="section wrap" id="studio">
  <div class="section-head">
    <p class="eyebrow">{t["home_studio_eyebrow"]}</p>
    <h2>{t["home_studio_title"]}</h2>
  </div>
  <div class="narrow">{t["home_studio_text"]}</div>
  <div class="principles">{principles}</div>
</section>'''
    return dict(title=t["home_title"], description=t["home_desc"], world="studio", content=content)


def page_apps(t, lang, url):
    content = f'''
<section class="section wrap">
  <div class="section-head">
    <p class="eyebrow">{t["home_apps_eyebrow"]}</p>
    <h1>{t["apps_title"]}</h1>
    <p class="lead">{t["apps_lead"]}</p>
  </div>
  {panel_quizerra(t, lang, url)}
  {panel_kids(t, lang, url)}
</section>'''
    return dict(title=t["apps_page_title"], description=t["apps_lead"], world="studio", content=content)


def page_quizerra(t, lang, url):
    stats = "".join(f"<li><b>{b}</b><span>{s}</span></li>" for b, s in t["q_stats"])
    steps = "".join(f"<li>{s}</li>" for s in t["q_how"])
    names = ["01-menu", "02-gameplay", "03-results", "04-collection", "05-stats"]
    content = f'''
<section class="product-hero wrap">
  <div class="panel-copy">
    <div class="app-name"><img src="/assets/img/quizerra/icon.png" alt="" width="64" height="64">
      <h1>{quizerra_word()}</h1></div>
    <p class="app-sub">{t["q_subtitle"]}</p>
    <p class="lead">{t["q_lead"]}</p>
    <div class="actions">{store_button(t)}</div>
    <ul class="statrow">{stats}</ul>
  </div>
  <div class="panel-art">
    <img class="device" src="/assets/img/quizerra/{lang}/hero-device.jpg" alt="{t["q_shot_alt"]}" width="560" height="1216">
  </div>
</section>
<div class="wrap">{pixels("q-1")}</div>

<section class="section wrap">
  <div class="two-col">
    <div>
      <p class="eyebrow">{t["q_how_eyebrow"]}</p>
      <h2>{t["q_how_title"]}</h2>
      <ol class="steps" style="margin-top:20px">{steps}</ol>
    </div>
    <div>
      <p class="eyebrow">{t["q_cat_eyebrow"]}</p>
      <h2>{t["q_cat_title"]}</h2>
      <p class="muted" style="margin-top:10px">{t["q_cat_text"]}</p>
      {chips(t["q_categories"], t["q_cat_mix"])}
    </div>
  </div>
</section>

<section class="section wrap">
  <p class="eyebrow">{t["q_feat_eyebrow"]}</p>
  <h2 style="margin-bottom:22px">{t["q_feat_title"]}</h2>
  {features(t["q_features"])}
</section>

<section class="section wrap">
  <p class="eyebrow">{t["gallery_eyebrow"]}</p>
  <h2 style="margin-bottom:8px">{t["q_gallery_title"]}</h2>
  {gallery("quizerra", lang, names, t["q_gallery_alts"])}
</section>

<section class="section wrap">
  <div class="two-col">
    <div class="note">
      <p class="eyebrow">{t["privacy_eyebrow"]}</p>
      <p>{t["q_privacy_text"]}</p>
      <p><a href="{url("legal-quizerra", lang)}#{lang}">{t["q_privacy_link"]}</a></p>
    </div>
    <div class="note">
      <p class="eyebrow">{t["support_eyebrow"]}</p>
      <p>{t["support_text"]}</p>
      <p><a href="mailto:{MAIL}?subject=Quizerra">{MAIL}</a> · <a href="{url("contact", lang)}">{t["nav_contact"]}</a></p>
    </div>
  </div>
</section>'''
    return dict(title=t["q_page_title"], description=t["q_desc"], world="noir", content=content,
                og_image="/assets/img/quizerra/icon.png")


def page_kids(t, lang, url):
    stats = "".join(f"<li><b>{b}</b><span>{s}</span></li>" for b, s in t["k_stats"])
    ages = "".join(f"<li><h3>{h}</h3><p>{p}</p></li>" for h, p in t["k_ages"])
    parents = "".join(f"<li>{p}</li>" for p in t["k_parents"])
    names = ["01-menu", "02-ageselect", "03-gameplay", "04-album", "05-results"]
    content = f'''
<section class="product-hero wrap">
  <div class="panel-copy">
    <div class="app-name"><img src="/assets/img/kids/icon.png" alt="" width="64" height="64">
      <h1>{kids_word()}</h1></div>
    <p class="app-sub">{t["k_subtitle"]}</p>
    <p class="lead">{t["k_lead"]}</p>
    <div class="actions">{soon_badge(t)}</div>
    <p class="muted" style="margin-top:12px;font-size:.95rem">{t["k_soon_note"]}</p>
    <ul class="statrow">{stats}</ul>
  </div>
  <div class="panel-art">
    <img class="device" src="/assets/img/kids/{lang}/hero-device.jpg" alt="{t["k_shot_alt"]}" width="560" height="1216">
    <img class="ella" src="/assets/img/kids/ella-cheer.png" alt="" style="left:-10%;bottom:0">
    <img class="sticker" src="/assets/img/kids/sticker-dinosaurs-1.png" alt="" style="right:-6%;top:4%;transform:rotate(10deg)" loading="lazy">
    <img class="sticker" src="/assets/img/kids/sticker-animals-2.png" alt="" style="right:-2%;bottom:14%;transform:rotate(-8deg)" loading="lazy">
  </div>
</section>
<div class="wrap">{pixels("k-1")}</div>

<section class="section wrap">
  <div class="two-col">
    <div class="parents">
      <p class="eyebrow">{t["k_parents_eyebrow"]}</p>
      <h2>{t["k_parents_title"]}</h2>
      <p style="margin-top:10px">{t["k_parents_intro"]}</p>
      <ul>{parents}</ul>
      <p style="margin:16px 0 0"><a href="{url("legal-kids", lang)}#{lang}">{t["k_privacy_link"]}</a></p>
    </div>
    <div>
      <p class="eyebrow">{t["k_ages_eyebrow"]}</p>
      <h2>{t["k_ages_title"]}</h2>
      <p class="muted" style="margin-top:10px">{t["k_ages_intro"]}</p>
      <ul class="features" style="grid-template-columns:1fr">{ages}</ul>
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="two-col">
    <div>
      <p class="eyebrow">{t["k_album_eyebrow"]}</p>
      <h2>{t["k_album_title"]}</h2>
      <p style="margin-top:12px">{t["k_album_text"]}</p>
      <p class="eyebrow" style="margin-top:28px">{t["q_cat_eyebrow"]}</p>
      {chips(t["k_categories"])}
      <p class="muted" style="margin-top:14px;font-size:.95rem">{t["k_pricing"]}</p>
    </div>
    <div class="album-art">
      <img class="album" src="/assets/img/kids/album-space.jpg" alt="{t["k_album_alt"]}" width="600" height="900" loading="lazy">
      <img class="sticker" src="/assets/img/kids/sticker-space-3.png" alt="" style="left:8%;top:12%;transform:rotate(-9deg)" loading="lazy">
      <img class="sticker" src="/assets/img/kids/sticker-space-1.png" alt="" style="right:10%;top:38%;transform:rotate(7deg)" loading="lazy">
      <img class="sticker" src="/assets/img/kids/sticker-myths-1.png" alt="" style="left:16%;bottom:10%;transform:rotate(4deg)" loading="lazy">
    </div>
  </div>
</section>

<section class="section wrap">
  <p class="eyebrow">{t["q_feat_eyebrow"]}</p>
  <h2 style="margin-bottom:22px">{t["k_feat_title"]}</h2>
  {features(t["k_features"])}
</section>

<section class="section wrap">
  <p class="eyebrow">{t["gallery_eyebrow"]}</p>
  <h2 style="margin-bottom:8px">{t["k_gallery_title"]}</h2>
  {gallery("kids", lang, names, t["k_gallery_alts"])}
</section>

<section class="section wrap">
  <div class="note">
    <p class="eyebrow">{t["support_eyebrow"]}</p>
    <p>{t["support_text"]}</p>
    <p><a href="mailto:{MAIL}?subject=Quizerra%20Kids">{MAIL}</a> · <a href="{url("contact", lang)}">{t["nav_contact"]}</a></p>
  </div>
</section>'''
    return dict(title=t["k_page_title"], description=t["k_desc"], world="sky", content=content,
                og_image="/assets/img/kids/icon.png")


def page_contact(t, lang, url):
    topics = "".join(f"<li>{x}</li>" for x in t["contact_topics"])
    content = f'''
<section class="section wrap narrow">
  <p class="eyebrow">{t["nav_contact"]}</p>
  <h1>{t["contact_title"]}</h1>
  <p class="lead" style="margin-top:12px">{t["contact_lead"]}</p>
  <div class="contact-card">
    <a class="btn btn-accent" href="mailto:{MAIL}">{t["contact_button"]}</a>
    <p style="margin:14px 0 0"><a href="mailto:{MAIL}">{MAIL}</a></p>
  </div>
  <h2 style="font-size:1.3rem">{t["contact_topics_title"]}</h2>
  <ul class="topics">{topics}</ul>
  <h2 style="font-size:1.3rem;margin-top:36px">{t["contact_post_title"]}</h2>
  <p class="muted">{t["contact_post_note"]}</p>
  {address_box(t)}
</section>'''
    return dict(title=t["contact_page_title"], description=t["contact_lead"], world="studio", content=content)


def page_imprint(t, lang, url):
    """Impressum nach § 5 DDG: Pflichtangaben als beschriftete Liste, damit jede
    Angabe eindeutig zuzuordnen ist. Telefon und Umsatzsteuer-Angaben erscheinen
    nur, wenn sie oben in den Konstanten gesetzt sind (keine Platzhalter live)."""
    rows = [
        (t["imp_provider"], "SevenFoxes Games"),
        (t["imp_form"], t["imp_form_value"]),
        (t["imp_owner"], "Marcel Krause"),
        (t["imp_address"], f"c/o Autorenglück #39534<br>Albert-Einstein-Str. 47<br>02977 Hoyerswerda<br>{t['country']}"),
        (t["email_label"], f'<a href="mailto:{MAIL}">{MAIL}</a>'),
    ]
    if PHONE:
        rows.append((t["imp_phone"], f'<a href="tel:{PHONE_LINK}">{PHONE}</a>'))
    if VAT_ID:
        rows.append((t["imp_vat"], VAT_ID))
    elif SMALL_BUSINESS:
        rows.append((t["imp_vat"], t["imp_vat_small"]))
    rows.append((t["imp_responsible"], f"Marcel Krause<br><span class=\"muted\">{t['imp_responsible_note']}</span>"))
    dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
    sections = "".join(f"<h2>{h}</h2>{b}" for h, b in t["imprint_sections"])
    content = f'''
<section class="section wrap legal">
  <p class="eyebrow">{t["nav_imprint"]}</p>
  <h1 style="margin-top:0">{t["imprint_title"]}</h1>
  <p class="muted">{t["imprint_sub"]}</p>
  <dl class="imprint">{dl}</dl>
  {sections}
</section>'''
    return dict(title=t["imprint_page_title"], description=t["imprint_desc"], world="studio", content=content)


def page_privacy(t, lang, url):
    sections = "".join(f"<h2>{h}</h2>{b}" for h, b in t["privacy_sections"])
    content = f'''
<section class="section wrap legal">
  <p class="eyebrow">{t["nav_privacy_site"]}</p>
  <h1 style="margin-top:0">{t["privacy_title"]}</h1>
  <p class="muted">{t["privacy_sub"]}</p>
  {sections}
</section>'''
    return dict(title=t["privacy_page_title"], description=t["privacy_desc"], world="studio", content=content)


def page_legal(app, t, lang, url):
    body = (HERE / "legal" / f"{app}.html").read_text()
    word = quizerra_word() if app == "quizerra" else kids_word()
    title = t["legal_q_title"] if app == "quizerra" else t["legal_k_title"]
    desc = t["legal_q_desc"] if app == "quizerra" else t["legal_k_desc"]
    content = f'''
<section class="section wrap legal">
  <p class="brand-line">{word}</p>
  <p class="lang-switch"><a href="#de" hreflang="de">Deutsch</a> <a href="#en" hreflang="en">English</a> <a href="#es" hreflang="es">Español</a></p>
{body}
</section>'''
    return dict(title=title, description=desc, world="studio", content=content)


def render(key, lang, t, url):
    if key == "home":
        return page_home(t, lang, url)
    if key == "apps":
        return page_apps(t, lang, url)
    if key == "quizerra":
        return page_quizerra(t, lang, url)
    if key == "kids":
        return page_kids(t, lang, url)
    if key == "contact":
        return page_contact(t, lang, url)
    if key == "imprint":
        return page_imprint(t, lang, url)
    if key == "privacy":
        return page_privacy(t, lang, url)
    if key == "legal-quizerra":
        return page_legal("quizerra", t, lang, url)
    if key == "legal-kids":
        return page_legal("quizerra-kids", t, lang, url)
    raise KeyError(key)
