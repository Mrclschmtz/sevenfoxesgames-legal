"""Seitenaufbau für sevenfoxes.de.

render(key, lang, t, url) liefert Titel, Beschreibung, Welt und den HTML-Inhalt
einer Seite. Die Texte kommen aus site/i18n/<lang>.py (Dict T), die Rechtstexte
der Apps liegen fertig in site/legal/. Keine Abhängigkeiten außer der Stdlib.
"""
import importlib
import pathlib
import random

HERE = pathlib.Path(__file__).resolve().parent
APP_STORE_QUIZERRA = "https://apps.apple.com/app/id6789493203"
APP_STORE_KIDS = "https://apps.apple.com/app/id6808029347"
APP_STORE_BUMBLOSSOM = "https://apps.apple.com/app/id6815565230"

# Launch-Schalter für Quizerra Kids (Veröffentlichung Do 08.10.2026, 09:00 MESZ).
# False: „Ab 8. Oktober"-Badge + Ankündigungs-Banner. True: Store-Button + „Jetzt im
# App Store"-Banner. Umschalten mit `python3 site/golive_kids.py` (oder KIDS_LIVE=1
# zum Probebauen).
import os as _os
KIDS_LIVE = True or _os.environ.get("KIDS_LIVE") == "1"
# Bumblossom-Launch (01.10.2026): Store-Button statt „Ab 1. Oktober"-Badge. Umschalten: BUMBLOSSOM_LIVE = True, dann build.py
BUMBLOSSOM_LIVE = True or _os.environ.get("BUMBLOSSOM_LIVE") == "1"
MAIL = "kontakt@sevenfoxes.de"

# Impressum-Angaben, die nur Marcel liefern kann. Solange None, wird die Zeile
# NICHT gerendert – lieber eine fehlende Zeile als ein Platzhalter auf der Live-Seite.
PHONE = "+49 1575 6548598"   # Geschaeftsrufnummer SevenFoxes Games (auch im DSA-Datensatz)
PHONE_LINK = "+4915756548598"
VAT_ID = None         # Umsatzsteuer-Identifikationsnummer nach § 27a UStG, falls vorhanden
W_ID = None           # Wirtschafts-Identifikationsnummer nach § 139c AO (BZSt vergibt sie seit 11/2024 stufenweise), falls vorhanden
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


def store_button(t, href=APP_STORE_QUIZERRA, small=None):
    return (f'<a class="btn btn-store" href="{href}" rel="noopener">'
            f'<span class="apple" aria-hidden="true">&#63743;</span>'
            f'<span>{t["btn_store"]}<br><small>{small or t["btn_store_small"]}</small></span></a>')


def soon_badge(t):
    return f'<span class="soon">{t["kids_soon"]}</span>'


def kids_cta(t):
    """Vor dem Launch das Datums-Badge, danach der echte Store-Button."""
    return store_button(t, APP_STORE_KIDS) if KIDS_LIVE else soon_badge(t)


def bumblossom_cta(t):
    """Vor dem Launch das Datums-Badge, danach der Store-Button (nur iPhone)."""
    return store_button(t, APP_STORE_BUMBLOSSOM, t["b_store_small"]) if BUMBLOSSOM_LIVE else f'<span class="soon">{t["b_soon"]}</span>'


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
    <div class="actions">{kids_cta(t)}
      <a class="btn btn-ghost" href="{url("kids", lang)}">{t["btn_more"]}</a></div>
  </div>
  <div class="panel-art">
    <img class="device" src="/assets/img/kids/{lang}/hero-device.jpg" alt="{t["k_shot_alt"]}" width="560" height="1216" loading="lazy">
    <img class="ella" src="/assets/img/kids/ella-happy.png" alt="" loading="lazy">
    <img class="sticker" src="/assets/img/kids/sticker-space-1.png" alt="" style="right:-4%;top:6%;transform:rotate(12deg)" loading="lazy">
  </div>
</article>'''


def panel_bumblossom(t, lang, url):
    return f'''
<article class="world-panel" data-world="garden" aria-labelledby="p-bumblossom">
  <div class="panel-copy">
    <div class="app-name"><img src="/assets/img/bumblossom/icon.png" alt="" width="64" height="64">
      <h3 id="p-bumblossom"><span class="display">BUMB<b>LOSSOM</b></span></h3></div>
    <p class="app-sub">{t["b_subtitle"]}</p>
    <p>{t["b_teaser"]}</p>
    {facts(t["b_facts"])}
    <div class="actions">{bumblossom_cta(t)}
      <a class="btn btn-ghost" href="{url("bumblossom", lang)}">{t["btn_more"]}</a></div>
  </div>
  <div class="panel-art">
    <img class="device" src="/assets/img/bumblossom/hero-device.jpg" alt="{t["b_shot_alt"]}" width="560" height="1127" loading="lazy">
    <img class="bee" src="/assets/img/bumblossom/bee_y.png" alt="" loading="lazy">
    <img class="sticker" src="/assets/img/bumblossom/flower_r.png" alt="" style="right:-2%;top:8%;transform:rotate(14deg)" loading="lazy">
    <img class="sticker" src="/assets/img/bumblossom/flower_b.png" alt="" style="right:6%;bottom:6%;width:16%;transform:rotate(-10deg)" loading="lazy">
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
  {panel_bumblossom(t, lang, url)}
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
  {panel_bumblossom(t, lang, url)}
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
    <div class="actions">{kids_cta(t)}</div>
    {"" if KIDS_LIVE else f'<p class="muted" style="margin-top:12px;font-size:.95rem">{t["k_soon_note"]}</p>'}
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
      <p style="margin:8px 0 0"><a href="{url("guide-kids", lang)}">{t["guide_kids_link"]}</a></p>
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



# Bumblossom-Events: erscheinen per Datum von selbst (data-from/data-until, Skript in build.py) – kein Neubau nötig.
# Zeiten in UTC = Mitternacht deutscher Zeit (MESZ bis 25.10., danach MEZ).
EVENTS = [
    ("halloween", "2026-10-22T22:00:00Z", "2026-11-02T23:00:00Z"),
    ("advent",    "2026-11-27T23:00:00Z", "2026-12-24T23:00:00Z"),
    ("winter",    "2026-12-24T23:00:00Z", "2027-01-06T23:00:00Z"),
]


def events_section(t):
    """„Gerade im Garten“: laufendes Event als „Jetzt“, das nächste als „Bald“, vergangene verschwinden (per Skript)."""
    cards = "".join(f'''
    <article class="ev-card" data-from="{von}" data-until="{bis}" hidden>
      <img src="/assets/img/bumblossom/events/{k}.jpg" alt="" width="960" height="540" loading="lazy">
      <div class="ev-body">
        <p class="ev-state"><span class="ev-now">{t["ev_now"]}</span><span class="ev-soon">{t["ev_soon"]}</span> · {t[f"ev_{k}_date"]}</p>
        <h3>{t[f"ev_{k}_title"]}</h3>
        <p class="muted">{t[f"ev_{k}_text"]}</p>
      </div>
    </article>''' for k, von, bis in EVENTS)
    return f'''
<section class="section wrap ev-section" id="events" hidden>
  <p class="eyebrow">{t["ev_eyebrow"]}</p>
  <h2 style="margin-bottom:22px">{t["ev_title"]}</h2>
  <div class="ev-grid">{cards}
  </div>
</section>
<script>(function(){{var q=new URLSearchParams(location.search).get("jetzt"),n=q?Date.parse(q):Date.now(),s=document.querySelector(".ev-section"),bald=0;
s.querySelectorAll(".ev-card").forEach(function(c){{var v=Date.parse(c.dataset.from),b=Date.parse(c.dataset.until);
if(n>=b){{c.remove();return;}}
if(n>=v){{c.classList.add("is-now");c.hidden=false;}}
else if(bald<1){{bald++;c.classList.add("is-soon");c.hidden=false;}} else c.remove();}});
if(s.querySelector(".ev-card:not([hidden])"))s.hidden=false;}})();</script>'''


def page_bumblossom(t, lang, url):
    stats = "".join(f"<li><b>{b}</b><span>{s}</span></li>" for b, s in t["b_stats"])
    steps = "".join(f"<li>{s}</li>" for s in t["b_how"])
    names = ["01-bloom", "02-bees", "03-gardens", "04-herbarium", "05-pressed", "06-start"]
    content = f'''
<section class="product-hero wrap">
  <div class="panel-copy">
    <div class="app-name"><img src="/assets/img/bumblossom/icon.png" alt="" width="64" height="64">
      <h1><span class="display">BUMB<b>LOSSOM</b></span></h1></div>
    <p class="app-sub">{t["b_subtitle"]}</p>
    <p class="lead">{t["b_lead"]}</p>
    <div class="actions">{bumblossom_cta(t)}</div>
    {"" if BUMBLOSSOM_LIVE else f'<p class="muted" style="margin-top:12px;font-size:.95rem">{t["b_soon_note"]}</p>'}
    <ul class="statrow">{stats}</ul>
  </div>
  <div class="panel-art">
    <img class="device" src="/assets/img/bumblossom/hero-device.jpg" alt="{t["b_shot_alt"]}" width="560" height="1127">
    <img class="bee" src="/assets/img/bumblossom/bee_y.png" alt="">
    <img class="sticker" src="/assets/img/bumblossom/flower_r.png" alt="" style="right:-2%;top:8%;transform:rotate(14deg)" loading="lazy">
    <img class="sticker" src="/assets/img/bumblossom/flower_b.png" alt="" style="right:6%;bottom:6%;width:16%;transform:rotate(-10deg)" loading="lazy">
  </div>
</section>
<div class="wrap">{pixels("b-1")}</div>

<section class="section wrap">
  <div class="two-col">
    <div>
      <p class="eyebrow">{t["b_how_eyebrow"]}</p>
      <h2>{t["b_how_title"]}</h2>
      <ol class="steps" style="margin-top:20px">{steps}</ol>
    </div>
    <div>
      <p class="eyebrow">{t["b_gardens_eyebrow"]}</p>
      <h2>{t["b_gardens_title"]}</h2>
      <p class="muted" style="margin-top:10px">{t["b_gardens_text"]}</p>
      {chips(t["b_gardens"], t["b_gardens_more"])}
    </div>
  </div>
</section>

{events_section(t)}

<section class="section wrap">
  <p class="eyebrow">{t["q_feat_eyebrow"]}</p>
  <h2 style="margin-bottom:22px">{t["b_feat_title"]}</h2>
  {features(t["b_features"])}
</section>

<section class="section wrap">
  <p class="eyebrow">{t["gallery_eyebrow"]}</p>
  <h2 style="margin-bottom:8px">{t["b_gallery_title"]}</h2>
  {gallery("bumblossom", lang, names, t["b_gallery_alts"])}
</section>

<section class="section wrap">
  <div class="two-col">
    <div class="note">
      <p class="eyebrow">{t["privacy_eyebrow"]}</p>
      <p>{t["b_privacy_text"]}</p>
      <p><a href="{url("legal-bumblossom", lang)}#{lang}">{t["b_privacy_full"]}</a></p>
    </div>
    <div class="note">
      <p class="eyebrow">{t["support_eyebrow"]}</p>
      <p>{t["support_text"]}</p>
      <p><a href="mailto:{MAIL}?subject=Bumblossom">{MAIL}</a> · <a href="{url("contact", lang)}">{t["nav_contact"]}</a></p>
    </div>
  </div>
</section>'''
    return dict(title=t["b_page_title"], description=t["b_desc"], world="garden", content=content,
                og_image="/assets/img/bumblossom/icon.png")

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
    # Diensteanbieter ist bei einem Einzelunternehmen die natürliche Person;
    # „SevenFoxes Games" ist nur die Geschäftsbezeichnung (keine Rechtsform-Zeile,
    # kein separater „Inhaber" – das erweckte den Eindruck einer Gesellschaft).
    contact = f'{t["email_label"]}: <a href="mailto:{MAIL}">{MAIL}</a>'
    if PHONE:
        contact += f'<br>{t["imp_phone"]}: <a href="tel:{PHONE_LINK}">{PHONE}</a>'
    rows = [
        (t["imp_provider"], f"Marcel Krause<br>{t['imp_trading_as']} SevenFoxes Games"),
        (t["imp_address"], f"c/o Autorenglück #39534<br>Albert-Einstein-Str. 47<br>02977 Hoyerswerda<br>{t['country']}"),
        (t["imp_contact"], contact),
    ]
    # § 5 Abs. 1 Nr. 6 DDG: USt-IdNr. ODER Wirtschafts-Identifikationsnummer sind
    # Pflicht, sobald vorhanden. Der Kleinunternehmer-Hinweis ist freiwillig.
    if VAT_ID:
        rows.append((t["imp_vat_id"], VAT_ID))
    if W_ID:
        rows.append((t["imp_w_id"], W_ID))
    if SMALL_BUSINESS and not VAT_ID:
        rows.append((t["imp_vat"], t["imp_vat_small"]))
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
    word, title, desc = {
        "quizerra": (quizerra_word(), t["legal_q_title"], t["legal_q_desc"]),
        "quizerra-kids": (kids_word(), t["legal_k_title"], t["legal_k_desc"]),
        "bumblossom": ('<span class="display">BUMBLOSSOM</span>', t["legal_b_title"], t["legal_b_desc"]),
    }[app]
    content = f'''
<section class="section wrap legal">
  <p class="brand-line">{word}</p>
  <p class="lang-switch"><a href="#de" hreflang="de">Deutsch</a> <a href="#en" hreflang="en">English</a> <a href="#es" hreflang="es">Español</a> <a href="#fr" hreflang="fr">Français</a></p>
{body}
</section>'''
    return dict(title=title, description=desc, world="studio", content=content)


def page_duel(t, lang, url):
    """Einladung zum Quizerra-Duell (Link aus der App: /duell/?c=482913). Der Code steht nur in der
    URL; ein kleines Skript zeigt ihn an und baut den Deep Link quizerra://duell?c=… – nichts wird
    gespeichert oder übertragen. Ohne Code bleibt die Seite eine allgemeine Einladung."""
    steps = "".join(f"<li>{s}</li>" for s in t["duel_how"])
    content = f'''
<section class="section wrap narrow duel-invite">
  <div class="app-name"><img src="/assets/img/quizerra/icon.png" alt="" width="64" height="64">
    <span>{quizerra_word()}</span></div>
  <p class="eyebrow" style="margin-top:24px">{t["duel_eyebrow"]}</p>
  <h1>{t["duel_title"]}</h1>
  <p class="lead" style="margin-top:12px">{t["duel_lead"]}</p>
  <div class="contact-card invite-card">
    <div id="invite-code" hidden>
      <p class="eyebrow">{t["duel_code_label"]}</p>
      <p class="invite-code" id="invite-code-value"></p>
    </div>
    <p class="muted" id="invite-nocode">{t["duel_nocode"]}</p>
    <div class="actions">
      {store_button(t)}
      <a class="btn btn-accent btn-open" id="invite-open" href="quizerra://duell" hidden><span>{t["duel_open"]}<br><small>{t["duel_open_small"]}</small></span></a>
    </div>
  </div>
  <h2 style="font-size:1.3rem">{t["duel_how_title"]}</h2>
  <ol class="steps" style="margin-top:16px">{steps}</ol>
  <p class="muted" style="margin-top:28px">{t["duel_privacy"]}</p>
</section>
<script>(function(){{
  var c=(new URLSearchParams(location.search).get("c")||"").replace(/\\D/g,"");
  if(!/^[1-9][0-9]{{5}}$/.test(c))return;
  document.getElementById("invite-code-value").textContent=c.slice(0,3)+"\\u2009"+c.slice(3);
  document.getElementById("invite-code").hidden=false;
  document.getElementById("invite-nocode").hidden=true;
  var o=document.getElementById("invite-open");o.href="quizerra://duell?c="+c;o.hidden=false;
  document.querySelectorAll(".lang a").forEach(function(a){{a.href=a.getAttribute("href")+"?c="+c;}});
}})();</script>'''
    return dict(title=t["duel_page_title"], description=t["duel_desc"], world="noir",
                content=content, robots="noindex", og_image="/assets/img/quizerra/icon.png")


def page_guide_kids(t, lang, url):
    """Ratgeber für Eltern: Woran man eine gute Quiz-App für Kinder erkennt (site/guides.py)."""
    from guides import guide_kids
    g = guide_kids(lang)
    checks = "".join(f"<li><h3>{h}</h3><p>{p}</p></li>" for h, p in g["checks"])
    settings = "".join(f"<li>{x}</li>" for x in g["settings"])
    example = "".join(f"<li>{x}</li>" for x in g["example"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in g["faq"])
    content = f'''
<article class="guide">
<section class="section wrap narrow guide-head">
  <p class="eyebrow">{g["eyebrow"]}</p>
  <h1>{g["title"]}</h1>
  <p class="lead" style="margin-top:14px">{g["lead"]}</p>
  <p class="muted guide-meta">{g["meta"]}</p>
</section>
<div class="wrap narrow">{pixels("g-1")}</div>
<section class="section wrap narrow">
  <h2>{g["check_title"]}</h2>
  <p style="margin-top:10px">{g["check_intro"]}</p>
  <ol class="steps guide-checks">{checks}</ol>
</section>
<section class="section wrap narrow">
  <div class="note">
    <h2 style="font-size:1.25rem;margin-bottom:10px">{g["settings_title"]}</h2>
    <ul class="guide-list">{settings}</ul>
  </div>
</section>
<section class="section wrap narrow">
  <div class="parents guide-example">
    <img class="guide-ella" src="/assets/img/kids/ella-think.png" alt="" width="140" loading="lazy">
    <p class="eyebrow">{g["example_eyebrow"]}</p>
    <h2>{g["example_title"]}</h2>
    <p style="margin-top:10px">{g["example_intro"]}</p>
    <ul>{example}</ul>
    <div class="actions" style="margin-top:18px">{kids_cta(t)}
      <a class="btn btn-ghost" href="{url("kids", lang)}">{g["example_more"]}</a></div>
  </div>
</section>
<section class="section wrap narrow">
  <h2>{g["faq_title"]}</h2>
  <div class="faq" style="margin-top:14px">{faq}</div>
</section>
</article>'''
    return dict(title=g["page_title"], description=g["desc"], world="sky", content=content,
                og_image="/assets/img/kids/icon.png")


def page_notfound(url):
    """404-Seite: EINE Datei für alle Sprachen (GitHub Pages liefert nur /404.html). Alle drei Fassungen
    stehen im HTML; ein kleines Skript blendet die Fassung zum Pfad (/en/…, /es/…) ein, sonst Deutsch."""
    blocks = []
    for lang in ("de", "en", "es", "fr"):
        t = importlib.import_module(f"i18n.{lang}").T
        answers = [("A", t["nf_a"], t["nf_a_sub"], url("home", lang)),
                   ("B", t["nf_b"], t["nf_b_sub"], url("apps", lang)),
                   ("C", t["nf_c"], t["nf_c_sub"], url("contact", lang))]
        rows = "".join(f'''<a class="nf-answer" href="{href}"><span class="nf-letter">{l}</span>
      <span class="nf-text"><b>{a}</b><small>{sub}</small></span></a>''' for l, a, sub, href in answers)
        blocks.append(f'''<section class="section wrap narrow nf" lang="{lang}" data-lang="{lang}"{"" if lang == "de" else " hidden"}>
  <p class="eyebrow">{t["nf_eyebrow"]}</p>
  <p class="nf-code" aria-hidden="true">404</p>
  <h1>{t["nf_title"]}</h1>
  <p class="lead" style="margin-top:12px">{t["nf_lead"]}</p>
  <div class="contact-card nf-card">
    <p class="nf-q">{t["nf_question"]}</p>
    {rows}
    <p class="muted nf-hint">{t["nf_hint"]}</p>
  </div>
</section>''')
    content = f'''
<div class="hero nf-hero wrap" aria-hidden="true">{hero_pixels(seed=404, count=22)}</div>
{"".join(blocks)}
<script>(function(){{var m=location.pathname.match(/^\\/(en|es|fr)(\\/|$)/),l=m?m[1]:"de";
document.querySelectorAll(".nf").forEach(function(s){{s.hidden=s.dataset.lang!==l;}});document.documentElement.lang=l;}})();</script>'''
    t = importlib.import_module("i18n.de").T
    return dict(title=t["nf_page_title"], description=t["nf_desc"], world="studio", content=content, robots="noindex")



PRESS_KIDS_QUESTIONS = 800   # bei Kids 1.3 (Weltreise) auf 880 und die Kategorien auf 11 setzen, zusammen mit dem Store-Update
PRESS_KIDS_CATEGORIES = 10
PRESS_DIR = "/assets/press/quizerra-kids"

PRESS_TEXT = {
    "de": dict(
        title="Presse – Quizerra Kids", desc="Pressematerial, Fakten und Kontakt zu Quizerra Kids, dem werbefreien Quizspiel für Kinder von 6 bis 12 Jahren.",
        eyebrow="Presse", lead="Ein Quizspiel für Kinder von 6 bis 12 Jahren: ohne Werbung, ohne Tracking, ohne Abo.",
        about_h="Kurzbeschreibung",
        about=("Quizerra Kids ist ein Quizspiel für iPhone und iPad. Kinder beantworten in zwei Minuten so viele Fragen wie möglich, "
               "bekommen für richtige Antworten Sticker und kleben sie in ein Stickerheft. Das Spiel hat {q} kindgerecht formulierte Fragen "
               "in {c} Kategorien und zwei Altersstufen (6 bis 8 Jahre mit Vorlesefunktion, 9 bis 12 Jahre), auf Deutsch, Englisch, Spanisch und Französisch. "
               "Vier Kategorien sind dauerhaft kostenlos, weitere gibt es als Einmalkauf, nie als Abo. Die App kommt ohne Werbung, ohne Tracking und ohne Konto aus."),
        facts_h="Fakten auf einen Blick",
        facts=[("Plattform", "iPhone und iPad (iOS 17 oder neuer), läuft komplett offline"),
               ("Preis", "gratis; vier Kategorien dauerhaft kostenlos, weitere je 0,99 € oder alle für 4,99 € (Einmalkäufe, kein Abo)"),
               ("Alter", "Kinder von 6 bis 12 Jahren; Altersfreigabe 4+, Kids-Kategorie im App Store"),
               ("Sprachen", "Deutsch, Englisch, Spanisch, Französisch"),
               ("Inhalt", "{q} Fragen, {c} Kategorien, 2 Altersstufen, Stickerheft, Tages-Challenge, Statistik"),
               ("Datenschutz", "Im App Store: „Es werden keine Daten erfasst“. Keine Werbung, keine Analyse-Dienste, kein Konto"),
               ("Erschienen", "5. Oktober 2026"),
               ("Hersteller", "SevenFoxes Games, Marcel Krause")],
        parents_h="Was Eltern wissen wollen",
        parents=["Keine Werbung, kein Tracking, keine Analyse-Dienste, kein Konto, keine Registrierung",
                 "Alle Käufe und der einzige externe Link liegen hinter einer Elternsicherung (kleine Rechenaufgabe)",
                 "Einmalkäufe statt Abo: Gekauft ist für immer gekauft",
                 "Fehler tun nicht weh: Eule Ella zeigt freundlich die richtige Antwort, es gibt keinen Zeitdruck-Alarm und keine Bestrafung",
                 "Die Vorlesefunktion (Stufe 6 bis 8) läuft auf dem Gerät und hilft Leseanfängern, allein zu spielen"],
        material_h="Pressematerial", material_note="Alle Bilder dürfen im Zusammenhang mit der Berichterstattung über Quizerra Kids frei verwendet werden.",
        zip="Gesamtpaket herunterladen (ZIP, Icon, Eule Ella, Screenshots in Deutsch und Englisch)",
        icon="App-Symbol (1024 × 1024)", ella="Eule Ella (Maskottchen, drei Posen, transparent)", shots="Screenshots (Deutsch)", shots_en="Screenshots (Englisch)",
        test_h="Zum Ausprobieren", test="Für Besprechungen schicken wir auf Anfrage Gutscheincodes, mit denen sich alle Kategorien kostenlos freischalten lassen.",
        contact_h="Pressekontakt", contact="Marcel Krause, SevenFoxes Games. Wir antworten in der Regel innerhalb von zwei Werktagen.",
        links_h="Weiterführende Links", app="Quizerra Kids im App Store", page="Produktseite", privacy="Datenschutzerklärung",
        studio_h="Über SevenFoxes Games", studio="SevenFoxes Games ist ein kleines, unabhängiges Studio. Wir bauen Spiele, die wir selbst gern spielen: schnell zu starten, ohne Anmeldung, ohne Wartezeiten und ohne Tricks, die einen länger festhalten sollen, als man möchte."),
    "en": dict(
        title="Press – Quizerra Kids", desc="Press material, facts and contact for Quizerra Kids, the ad-free quiz game for children aged 6 to 12.",
        eyebrow="Press", lead="A quiz game for children aged 6 to 12: no ads, no tracking, no subscription.",
        about_h="Short description",
        about=("Quizerra Kids is a quiz game for iPhone and iPad. Children answer as many questions as they can in two minutes, earn stickers for correct answers "
               "and stick them into a sticker book. The game has {q} kid-friendly questions in {c} categories and two age levels (ages 6 to 8 with read-aloud, ages 9 to 12), "
               "in German, English, Spanish and French. Four categories are free forever, more can be unlocked with one-time purchases, never with a subscription. "
               "The app has no ads, no tracking and no account."),
        facts_h="Facts at a glance",
        facts=[("Platform", "iPhone and iPad (iOS 17 or later), works completely offline"),
               ("Price", "free; four categories free forever, more at €0.99 each or all for €4.99 (one-time purchases, no subscription)"),
               ("Age", "children aged 6 to 12; age rating 4+, Kids category on the App Store"),
               ("Languages", "German, English, Spanish, French"),
               ("Content", "{q} questions, {c} categories, 2 age levels, sticker book, daily challenge, statistics"),
               ("Privacy", "App Store privacy label: “Data Not Collected”. No ads, no analytics, no account"),
               ("Released", "October 5, 2026"),
               ("Publisher", "SevenFoxes Games, Marcel Krause")],
        parents_h="What parents want to know",
        parents=["No ads, no tracking, no analytics, no account, no sign-up",
                 "All purchases and the only external link sit behind a parental gate (a small multiplication task)",
                 "One-time purchases instead of a subscription: bought is bought for good",
                 "Mistakes do not hurt: Ella the owl kindly shows the right answer, with no time-pressure alarms and no punishment",
                 "The read-aloud feature (ages 6 to 8) runs on the device and helps early readers play on their own"],
        material_h="Press material", material_note="All images may be used freely in connection with coverage of Quizerra Kids.",
        zip="Download everything (ZIP: icon, Ella the owl, screenshots in German and English)",
        icon="App icon (1024 × 1024)", ella="Ella the owl (mascot, three poses, transparent)", shots="Screenshots (German)", shots_en="Screenshots (English)",
        test_h="Try it", test="For reviews we send promo codes on request that unlock all categories for free.",
        contact_h="Press contact", contact="Marcel Krause, SevenFoxes Games. We usually reply within two working days.",
        links_h="Links", app="Quizerra Kids on the App Store", page="Product page", privacy="Privacy policy",
        studio_h="About SevenFoxes Games", studio="SevenFoxes Games is a small, independent studio. We build games we like to play ourselves: quick to start, no sign-up, no waiting, and no tricks designed to keep you hooked longer than you want to be."),
}


def page_press(t, lang, url):
    """Presseseite zu Quizerra Kids (unlisted, noindex). Deutsch und Englisch; es/fr zeigen den englischen Text."""
    P = PRESS_TEXT["de" if lang == "de" else "en"]
    sub = dict(q=PRESS_KIDS_QUESTIONS, c=PRESS_KIDS_CATEGORIES)
    facts_rows = "".join(f"<li><b>{k}:</b> {v.format(**sub)}</li>" for k, v in P["facts"])
    parents = "".join(f"<li>{x}</li>" for x in P["parents"])
    def files(folder, prefix, label):
        names = ["01-menu", "02-ageselect", "03-gameplay", "04-album", "05-results"]
        items = "".join(f'<li><a href="{PRESS_DIR}/{folder}/quizerra-kids-{prefix}-{n}.jpg" download>{n}</a></li>' for n in names)
        return f"<p><b>{label}</b></p><ul class=\"topics\">{items}</ul>"
    ella = "".join(f'<li><a href="{PRESS_DIR}/ella-{n}.png" download>ella-{n}.png</a></li>' for n in ("happy", "cheer", "think"))
    previews = gallery("kids", "de" if lang == "de" else "en", ["01-menu", "03-gameplay", "04-album", "05-results"],
                       [P["shots"]] * 4)
    body = f'''
<section class="section wrap narrow">
  <p class="eyebrow">{P["eyebrow"]}</p>
  <div class="app-name"><img src="/assets/img/kids/icon.png" alt="" width="64" height="64"><h1>{kids_word()}</h1></div>
  <p class="lead" style="margin-top:12px">{P["lead"]}</p>
  <div class="actions" style="margin:18px 0">{store_button(t, APP_STORE_KIDS)}</div>
  {previews}
  <h2 style="font-size:1.3rem">{P["about_h"]}</h2>
  <p>{P["about"].format(**sub)}</p>
  <h2 style="font-size:1.3rem;margin-top:30px">{P["facts_h"]}</h2>
  <ul class="topics">{facts_rows}</ul>
  <h2 style="font-size:1.3rem;margin-top:30px">{P["parents_h"]}</h2>
  <ul class="topics">{parents}</ul>
  <h2 style="font-size:1.3rem;margin-top:30px">{P["material_h"]}</h2>
  <p class="muted">{P["material_note"]}</p>
  <p><a class="btn btn-accent" href="/assets/press/quizerra-kids-pressekit.zip" download>{P["zip"]}</a></p>
  <p><b>{P["icon"]}</b>: <a href="{PRESS_DIR}/quizerra-kids-icon-1024.png" download>quizerra-kids-icon-1024.png</a></p>
  <p><b>{P["ella"]}</b></p><ul class="topics">{ella}</ul>
  {files("screenshots-de", "de", P["shots"])}
  {files("screenshots-en", "en", P["shots_en"])}
  <h2 style="font-size:1.3rem;margin-top:30px">{P["test_h"]}</h2>
  <p>{P["test"]}</p>
  <h2 style="font-size:1.3rem;margin-top:30px">{P["contact_h"]}</h2>
  <p>{P["contact"]}</p>
  {address_box(t)}
  <h2 style="font-size:1.3rem;margin-top:30px">{P["links_h"]}</h2>
  <ul class="topics"><li><a href="{APP_STORE_KIDS}" rel="noopener">{P["app"]}</a></li>
  <li><a href="{url("kids", lang)}">{P["page"]}</a></li>
  <li><a href="{url("legal-kids", lang)}#{lang if lang in ("de","en") else "en"}">{P["privacy"]}</a></li></ul>
  <h2 style="font-size:1.3rem;margin-top:30px">{P["studio_h"]}</h2>
  <p>{P["studio"]}</p>
</section>'''
    if lang in ("es", "fr"):
        body = f'<div lang="en">{body}</div>'
    return dict(title=P["title"], description=P["desc"], world="sky", content=body, robots="noindex",
                og_image="/assets/img/kids/icon.png")


def render(key, lang, t, url):
    if key == "home":
        return page_home(t, lang, url)
    if key == "apps":
        return page_apps(t, lang, url)
    if key == "quizerra":
        return page_quizerra(t, lang, url)
    if key == "kids":
        return page_kids(t, lang, url)
    if key == "bumblossom":
        return page_bumblossom(t, lang, url)
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
    if key == "legal-bumblossom":
        return page_legal("bumblossom", t, lang, url)
    if key == "duel":
        return page_duel(t, lang, url)
    if key == "guide-kids":
        return page_guide_kids(t, lang, url)
    if key == "press":
        return page_press(t, lang, url)
    if key == "notfound":
        return page_notfound(url)
    raise KeyError(key)
