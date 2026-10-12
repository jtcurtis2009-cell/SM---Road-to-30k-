"""Render a carousel post (slides.json) into 1080x1350 PNGs.

Usage:
    python3 scripts/render_carousel.py content/posts/<slug>

Output goes to exports/<slug>/slide-01.png and so on.
"""
import base64
import html
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PALETTE = json.loads((ROOT / "brand" / "palette.json").read_text())
W, H = 1080, 1350


def esc(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")


def photo_uri(base: Path, rel):
    if not rel:
        return None
    f = (base / rel)
    if not f.exists():
        return None
    mime = "image/png" if f.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()


def monogram(color_text: str) -> str:
    return f"""<div class="mono"><span style="color:{color_text}">JT</span></div>"""


CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:%(W)spx; height:%(H)spx; }
body { font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }
.slide { position:relative; width:%(W)spx; height:%(H)spx; padding:96px 96px 120px; display:flex; flex-direction:column; overflow:hidden; }
.dark { background:%(charcoal)s; color:%(sand)s; }
.light { background:%(sand)s; color:%(charcoal)s; }
.mono { width:84px; height:84px; border:5px solid %(rust)s; border-radius:8px; display:flex; align-items:center; justify-content:center;
        font-family:'Inter Display'; font-weight:800; font-size:38px; letter-spacing:-1px; }
.top { display:flex; justify-content:space-between; align-items:center; }
.kicker { font-weight:700; letter-spacing:6px; font-size:24px; color:%(denim_light)s; }
.light .kicker { color:%(denim)s; }
.foot { position:absolute; left:96px; right:96px; bottom:64px; display:flex; justify-content:space-between; align-items:center;
        font-size:24px; font-weight:600; letter-spacing:1px; opacity:.75; }
.cover h1 { font-family:'Inter Display'; font-weight:800; font-size:118px; line-height:1.0; letter-spacing:-4px; margin-top:auto; }
.cover .accent { font-family:'Inter Display'; font-weight:700; font-size:64px; line-height:1.1; color:%(rust_light)s; margin-top:40px; letter-spacing:-1.5px; }
.cover .bar { width:140px; height:10px; background:%(denim)s; margin-top:56px; margin-bottom:40px; }
.swipe { color:%(rust_light)s; opacity:1; }
.lesson .num { font-family:'Inter Display'; font-weight:800; font-size:260px; line-height:.85; color:%(rust)s; letter-spacing:-10px; margin-top:72px; }
.lesson h2 { font-family:'Inter Display'; font-weight:800; font-size:78px; line-height:1.05; letter-spacing:-1.5px; margin-top:56px; }
.lesson .rule { width:100px; height:8px; background:%(denim)s; margin:48px 0 40px; }
.lesson p { font-size:42px; line-height:1.45; font-weight:400; color:%(charcoal_soft)s; max-width:860px; }
.cta h1 { font-family:'Inter Display'; font-weight:800; font-size:132px; letter-spacing:-5px; line-height:1; margin-top:auto; }
.cta p { font-size:42px; line-height:1.45; margin-top:44px; max-width:880px; opacity:.92; }
.cta .accent { font-family:'Inter Display'; font-weight:700; font-size:50px; color:%(rust_light)s; margin-top:56px; line-height:1.2; letter-spacing:-1px; margin-bottom:40px; }
.story { background:%(charcoal)s; color:%(sand)s; padding:0; }
.story .bg { position:absolute; inset:0; background-size:cover; background-position:center; }
.story .ph { position:absolute; inset:0; background:radial-gradient(120%% 80%% at 70%% 20%%, %(denim)s 0%%, %(charcoal)s 70%%); }
.story .ph span { position:absolute; top:46%%; left:0; right:0; text-align:center; font-size:30px; letter-spacing:6px; opacity:.45; font-weight:600; }
.story .shade { position:absolute; inset:0; background:linear-gradient(180deg, rgba(43,41,38,.15) 0%%, rgba(43,41,38,0) 35%%, rgba(43,41,38,.88) 72%%, rgba(43,41,38,.97) 100%%); }
.story .inner { position:relative; height:100%%; padding:96px 96px 150px; display:flex; flex-direction:column; }
.story h1 { font-family:'Inter Display'; font-weight:800; font-size:100px; line-height:1.02; letter-spacing:-3px; margin-top:auto; }
.story .accent { font-size:44px; line-height:1.3; margin-top:32px; color:%(rust_light)s; font-weight:600; }
.lesson .note { margin-top:40px; padding-left:28px; border-left:6px solid %(rust)s; font-size:34px; line-height:1.4; font-style:italic; color:%(denim)s; max-width:860px; }
.cta .avatar { width:220px; height:220px; border-radius:50%%; background-size:cover; background-position:center; border:6px solid %(rust)s; margin-top:auto; margin-bottom:48px; }
.cta .avatar + h1 { margin-top:0; }
""" % {"W": W, "H": H, **PALETTE}


def slide_html(s: dict, i: int, total: int, handle: str, base: Path) -> str:
    t = s["type"]
    counter = f"{i}/{total}"
    photo = photo_uri(base, s.get("photo"))
    if t == "story_cover":
        bg = f'<div class="bg" style="background-image:url({photo})"></div>' if photo else '<div class="ph"><span>YOUR PHOTO HERE</span></div>'
        body = f"""
        <div class="slide story">
          {bg}<div class="shade"></div>
          <div class="inner">
            <div class="top">{monogram(PALETTE['sand'])}<div class="kicker">{esc(s['kicker'])}</div></div>
            <h1>{esc(s['title'])}</h1>
            <div class="accent">{esc(s['accent'])}</div>
          </div>
          <div class="foot"><span>{handle}</span><span class="swipe">{esc(s.get('footer','Swipe'))} &rarr;</span></div>
        </div>"""
    elif t == "cover":
        body = f"""
        <div class="slide dark cover">
          <div class="top">{monogram(PALETTE['sand'])}<div class="kicker">{esc(s['kicker'])}</div></div>
          <h1>{esc(s['title'])}</h1>
          <div class="accent">{esc(s['accent'])}</div>
          <div class="bar"></div>
          <div class="foot"><span>{handle}</span><span class="swipe">{esc(s['footer'])} &rarr;</span></div>
        </div>"""
    elif t == "lesson":
        body = f"""
        <div class="slide light lesson">
          <div class="top">{monogram(PALETTE['charcoal'])}<div class="kicker">LESSON {esc(s['number'])}</div></div>
          <div class="num">{esc(s['number'])}</div>
          <h2>{esc(s['title'])}</h2>
          <div class="rule"></div>
          <p>{esc(s['body'])}</p>
          {f'<div class="note">{esc(s["note"])}</div>' if s.get("note") else ''}
          <div class="foot"><span>{handle}</span><span>{counter}</span></div>
        </div>"""
    else:
        body = f"""
        <div class="slide dark cta">
          <div class="top">{monogram(PALETTE['sand'])}<div class="kicker">{esc(s['kicker'])}</div></div>
          {f'<div class="avatar" style="background-image:url({photo})"></div>' if photo else ''}
          <h1>{esc(s['title'])}</h1>
          <p>{esc(s['body'])}</p>
          <div class="accent">{esc(s['accent'])}</div>
          <div class="foot"><span>{handle}</span><span>{counter}</span></div>
        </div>"""
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"


def main(post_dir: str) -> None:
    post = Path(post_dir)
    data = json.loads((post / "slides.json").read_text())
    out = ROOT / "exports" / data["slug"]
    out.mkdir(parents=True, exist_ok=True)
    slides = data["slides"]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H})
        for i, s in enumerate(slides, start=1):
            page.set_content(slide_html(s, i, len(slides), data["handle"], post))
            page.wait_for_timeout(150)
            page.screenshot(path=str(out / f"slide-{i:02d}.png"))
        browser.close()
    print(f"Rendered {len(slides)} slides to {out}")


if __name__ == "__main__":
    main(sys.argv[1])
