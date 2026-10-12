"""Render a side by side sheet of Reel caption font options over a real frame.

Usage:
    python3 scripts/caption_fonts.py <frame.jpg> "<setup line>" "<big word>" [out.jpg] [letters]

Examples:
    python3 scripts/caption_fonts.py exports/my-reel/cover.jpg "discipline is a" "habit."
    python3 scripts/caption_fonts.py frame.jpg "discipline is a" "habit." sheet.jpg KLMNOPQRST

Styles live in scripts/caption_styles.py. Each tile is labeled with its letter so Justin
can just say "use G", then set "font": "G" in reel.json.
"""
import base64
import html
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from caption_styles import STYLES, face_css, faces_used

ROOT = Path(__file__).resolve().parent.parent


def main(frame, setup, big, out=None, letters=None):
    out = Path(out or ROOT / "brand" / "caption-font-options.jpg")
    letters = list(letters.upper()) if letters else list(STYLES)
    bg = base64.b64encode(Path(frame).read_bytes()).decode()
    tw, th, cols = 432, 768, 5
    tiles = []
    for l in letters:
        label, scss, bcss, scale = STYLES[l]
        tiles.append(f"""<div class="t"><div class="cap"><div class="s" style="{scss}">{html.escape(setup)}</div>
        <div class="b" style="{bcss};font-size:{98 * scale:.0f}px">{html.escape(big)}</div></div>
        <div class="lab"><b>{l}</b> {html.escape(label)}</div></div>""")
    rows = -(-len(letters) // cols)
    W, H = tw * cols, th * rows
    page_html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{face_css(faces_used(letters))}
    *{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{H}px;display:grid;
    grid-template-columns:repeat({cols},{tw}px);background:#1A1D22}}
    .t{{position:relative;width:{tw}px;height:{th}px;background:url(data:image/jpeg;base64,{bg}) center/cover;
       border:2px solid #1A1D22;overflow:hidden}}
    .cap{{position:absolute;left:16px;right:16px;top:95px;font-size:23px;text-align:center;color:#fff;text-shadow:0 3px 18px rgba(0,0,0,.5)}}
    .s{{font-size:23px}} .b{{line-height:.92;margin-top:4px}}
    .lab{{position:absolute;left:0;right:0;bottom:0;padding:14px 16px;background:rgba(26,29,34,.88);color:#EDE7DD;
       font-family:DMSans;font-size:19px;font-weight:500}} .lab b{{color:#C8A982;font-size:26px;margin-right:6px}}
    </style></head><body>{''.join(tiles)}</body></html>"""
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(page_html)
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(out), type="jpeg", quality=90)
        b.close()
    print(f"Font sheet: {out}")


if __name__ == "__main__":
    main(*sys.argv[1:6])
