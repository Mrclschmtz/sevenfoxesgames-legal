#!/usr/bin/env python3
"""Launch-Tag Bumblossom: schaltet BUMBLOSSOM_LIVE auf True, baut die Seite neu und
committet/pusht auf Wunsch (GitHub Pages liefert danach in ~1–2 Minuten aus).

    python3 site/golive_bumblossom.py          # nur umschalten + bauen (zum Prüfen)
    python3 site/golive_bumblossom.py --push   # umschalten, bauen, committen, pushen
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "site" / "pages.py"

src = PAGES.read_text()
old = 'BUMBLOSSOM_LIVE = False or _os.environ.get("BUMBLOSSOM_LIVE") == "1"'
new = 'BUMBLOSSOM_LIVE = True or _os.environ.get("BUMBLOSSOM_LIVE") == "1"'
if old in src:
    PAGES.write_text(src.replace(old, new, 1))
    print("BUMBLOSSOM_LIVE → True")
elif new in src:
    print("BUMBLOSSOM_LIVE war schon True")
else:
    sys.exit("Schalter in site/pages.py nicht gefunden – bitte von Hand prüfen.")

subprocess.run([sys.executable, str(ROOT / "build.py")], check=True)

if "--push" in sys.argv:
    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(ROOT), "commit", "-m",
                    "Bumblossom ist live: Store-Button"], check=True)
    subprocess.run(["git", "-C", str(ROOT), "push"], check=True)
    print("Gepusht – in 1–2 Minuten auf sevenfoxes.de.")
else:
    print("Nur lokal gebaut. Zum Veröffentlichen: python3 site/golive_bumblossom.py --push")
