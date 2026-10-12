"""Render a side by side sheet of Reel caption font options over a real frame.

Usage:
    python3 scripts/caption_fonts.py <frame.jpg> "<setup line>" "<big word>" [out.jpg]

Example:
    python3 scripts/caption_fonts.py exports/my-reel/cover.jpg "discipline is a" "habit."

Output defaults to brand/caption-font-options.jpg. Each tile is labeled with a letter
and the font pair, so Justin can just say "use F".
"""
import base64
import html
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "brand" / "fonts"

FACES = {
    "Fraunces": ("Fraunces[SOFT,WONK,opsz,wght].ttf", "font-weight:100 900;"),
    "DMSans": ("DMSans[opsz,wght].ttf", "font-weight:100 1000;"),
    "Gloock": ("Gloock-Regular.ttf", ""),
    "DMSerif": ("DMSerifDisplay-Regular.ttf", ""),
    "Playfair": ("PlayfairDisplay[wght].ttf", "font-weight:400 900;"),
    "InstrumentItalic": ("InstrumentSerif-Italic.ttf", ""),
    "Bricolage": ("BricolageGrotesque[opsz,wdth,wght].ttf", "font-weight:200 800;"),
    "Anton": ("Anton-Regular.ttf", ""),
    "Bebas": ("BebasNeue-Regular.ttf", ""),
    "ArchivoBlack": ("ArchivoBlack-Regular.ttf", ""),
    "Abril": ("AbrilFatface-Regular.ttf", ""),
    "Montserrat": ("Montserrat[wght].ttf", "font-weight:100 900;"),
}

# (letter, label, setup css, big css, uppercase big?)
OPTIONS = [
    ("A", "Fraunces Soft + DM Sans (current default)", "font-family:DMSans;font-weight:600",
     "font-family:Fraunces;font-weight:900;font-variation-settings:'SOFT' 100,'WONK' 1,'opsz' 144;letter-spacing:-.03em", False),
    ("B", "Gloock + DM Sans", "font-family:DMSans;font-weight:600", "font-family:Gloock;letter-spacing:-.02em", False),
    ("C", "DM Serif Display + DM Sans", "font-family:DMSans;font-weight:600", "font-family:DMSerif;letter-spacing:-.02em", False),
    ("D", "Playfair Display Black + DM Sans", "font-family:DMSans;font-weight:600",
     "font-family:Playfair;font-weight:900;letter-spacing:-.02em", False),
    ("E", "Abril Fatface + DM Sans", "font-family:DMSans;font-weight:600", "font-family:Abril;letter-spacing:-.01em", False),
    ("F", "Instrument Serif Italic + Bricolage", "font-family:Bricolage;font-weight:600",
     "font-family:InstrumentItalic;letter-spacing:-.02em;color:#E9C9A6", False),
    ("G", "Anton caps + DM Sans (gym energy)", "font-family:DMSans;font-weight:700;text-transform:uppercase;letter-spacing:.08em",
     "font-family:Anton;letter-spacing:.01em", True),
    ("H", "Bebas Neue + Montserrat", "font-family:Montserrat;font-weight:600;letter-spacing:.04em",
     "font-family:Bebas;letter-spacing:.02em", True),
    ("I", "Archivo Black + Instrument italic", "font-family:InstrumentItalic;font-size:1.25em",
     "font-family:ArchivoBlack;letter-spacing:-.04em", False),
    ("J", "Montserrat Black (clean sans, best for running captions)", "font-family:Montserrat;font-weight:500",
     "font-family:Montserrat;font-weight:900;letter-spacing:-.04em", False),
]


def face_css():
    out = []
    for name, (file, extra) in FACES.items():
        b = base64.b64encode((FONTS / file).read_bytes()).decode()
        out.append(f"@font-face{{font-family:'{name}';src:url(data:font/ttf;base64,{b});{extra}}}")
    return "".join(out)


def main(frame, setup, big, out=None):
    out = Path(out or ROOT / "brand" / "caption-font-options.jpg")
    bg = base64.b64encode(Path(frame).read_bytes()).decode()
    tw, th, cols = 432, 768, 5
    tiles = []
    for letter, label, scss, bcss, upper in OPTIONS:
        word = html.escape(big.upper() if upper else big)
        tiles.append(f"""<div class="t"><div class="cap"><div class="s" style="{scss}">{html.escape(setup)}</div>
        <div class="b" style="{bcss}">{word}</div></div><div class="lab"><b>{letter}</b> {html.escape(label)}</div></div>""")
    rows = -(-len(OPTIONS) // cols)
    W, H = tw * cols, th * rows
    page_html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{face_css()}
    *{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;display:grid;
    grid-template-columns:repeat({cols},{tw}px);background:#1A1D22}}
    .t{{position:relative;width:{tw}px;height:{th}px;background:url(data:image/jpeg;base64,{bg}) center/cover;
       border:2px solid #1A1D22;overflow:hidden}}
    .cap{{position:absolute;left:16px;right:16px;top:95px;text-align:center;color:#fff;text-shadow:0 3px 18px rgba(0,0,0,.5)}}
    .s{{font-size:23px}} .b{{font-size:98px;line-height:.92;margin-top:4px}}
    .lab{{position:absolute;left:0;right:0;bottom:0;padding:14px 16px;background:rgba(26,29,34,.88);color:#EDE7DD;
       font-family:DMSans;font-size:19px;font-weight:500}} .lab b{{color:#C8A982;font-size:26px;margin-right:6px}}
    </style></head><body>{''.join(tiles)}</body></html>"""
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(page_html)
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(out), type="jpeg", quality=90)
        b.close()
    print(f"Font sheet: {out}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
