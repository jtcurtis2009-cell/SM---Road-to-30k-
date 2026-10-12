"""Cut a branded Reel from raw footage using a reel.json spec.

Usage:
    python3 scripts/make_reel.py content/posts/<slug>

reel.json fields:
    source:    path to the raw clip (absolute, or relative to the post folder)
    segments:  [{"start": s, "end": s, "speed": 1.0}]  pieces kept, in order
    overlays:  [{"text": "...", "accent": "...", "start": s, "end": s, "style": "hook" | "end"}]
               times are on the FINISHED reel timeline

Output: exports/<slug>/reel.mp4 (1080x1920, 30fps, no audio so trending audio
can be added in Instagram) and cover.jpg
"""
import base64
import html
import json
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
P = json.loads((ROOT / "brand" / "palette.json").read_text())
W, H = 1080, 1920
FONTS = ROOT / "brand" / "fonts"


def _ff(name, file, extra=""):
    b = base64.b64encode((FONTS / file).read_bytes()).decode()
    return f"@font-face{{font-family:'{name}';src:url(data:font/ttf;base64,{b});{extra}}}"


FONT_CSS = (_ff("Fraunces", "Fraunces[SOFT,WONK,opsz,wght].ttf", "font-weight:100 900;")
            + _ff("DMSans", "DMSans[opsz,wght].ttf", "font-weight:100 1000;"))

CSS = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; background:transparent; font-family:'Inter'; -webkit-font-smoothing:antialiased; }}
.hook {{ position:absolute; left:72px; right:72px; top:300px; }}
.card {{ display:inline-block; background:rgba(43,41,38,.84); border-left:12px solid {P['rust']}; border-radius:18px;
         padding:30px 40px 34px; color:{P['sand']}; }}
.card h1 {{ font-family:'Inter Display'; font-weight:800; font-size:76px; line-height:1.06; letter-spacing:-2px; }}
.card p {{ font-size:40px; line-height:1.3; font-weight:600; color:{P['rust_light']}; margin-top:16px; }}
.shade {{ position:absolute; inset:0; background:radial-gradient(70% 30% at 50% 48%, rgba(43,41,38,.62), rgba(43,41,38,0)); }}
.end {{ position:absolute; left:0; right:0; top:760px; text-align:center; color:{P['sand']}; }}
.end .k {{ font-weight:700; letter-spacing:10px; font-size:34px; color:{P['denim_light']}; }}
.end h1 {{ font-family:'Inter Display'; font-weight:800; font-size:110px; letter-spacing:-4px; margin-top:18px;
           text-shadow:0 6px 30px rgba(0,0,0,.45); }}
.pop {{ position:absolute; left:40px; right:40px; text-align:center; color:#fff; text-shadow:0 4px 26px rgba(0,0,0,.42); }}
.pop .s {{ font-family:'DMSans'; font-weight:600; font-size:58px; letter-spacing:-.5px; }}
.pop .b {{ font-family:'Fraunces'; font-weight:900; font-variation-settings:'SOFT' 100,'WONK' 1,'opsz' 144;
          line-height:.86; letter-spacing:-8px; margin-top:8px; }}
.pop .a {{ font-family:'DMSans'; font-weight:700; font-size:40px; letter-spacing:8px; margin-top:26px; color:{P['sand']}; }}
.pop .h {{ display:inline-block; margin-top:30px; background:{P['rust']}; color:{P['sand']}; font-family:'DMSans'; font-weight:700;
           font-size:40px; padding:14px 34px; border-radius:999px; text-shadow:none; }}
.end .h {{ display:inline-block; margin-top:28px; background:{P['rust']}; color:{P['sand']}; font-weight:700; font-size:40px;
           padding:16px 34px; border-radius:999px; }}
"""


# Color grades. Set "grade" in reel.json to a name below, or to a raw ffmpeg filter string.
GRADES = {
    "default": "eq=contrast=1.04:saturation=1.06",
    # Dark indoor footage: lifts shadows and midtones, keeps blacks moody, light denoise for lifted grain.
    "lift_dark": ("hqdn3d=2:1.5:4:3,curves=master='0/0 0.18/0.34 0.5/0.68 1/1',"
                  "eq=gamma=1.1:contrast=1.04:saturation=1.1"),
    "lift_light": "curves=master='0/0 0.25/0.34 0.6/0.7 1/1',eq=gamma=1.05:contrast=1.03:saturation=1.06",
}


def esc(t):
    return html.escape(t).replace("\n", "<br>")


def overlay_html(o, handle):
    if o.get("style") in ("pop", "pop_end"):
        size = o.get("size", 250)
        top = o.get("top", 380)
        setup = f'<div class="s">{esc(o["setup"])}</div>' if o.get("setup") else ""
        tail = ""
        if o["style"] == "pop_end":
            tail = (f'<div class="a">{esc(o.get("accent", ""))}</div>' if o.get("accent") else "") + f'<div class="h">{handle}</div>'
        body = (f'<div class="pop" style="top:{top}px">{setup}'
                f'<div class="b" style="font-size:{size}px">{esc(o["text"])}</div>{tail}</div>')
        return f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{CSS}</style></head><body>{body}</body></html>"
    if o.get("style") == "end":
        body = f"""<div class="shade"></div><div class="end"><div class="k">{esc(o.get('accent', 'JUSTIN THYME'))}</div>
        <h1>{esc(o['text'])}</h1><div class="h">{handle}</div></div>"""
    else:
        acc = f"<p>{esc(o['accent'])}</p>" if o.get("accent") else ""
        body = f'<div class="hook"><div class="card"><h1>{esc(o["text"])}</h1>{acc}</div></div>'
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"


def render_overlays(overlays, handle, out_dir):
    paths = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": W, "height": H})
        for i, o in enumerate(overlays):
            page.set_content(overlay_html(o, handle))
            page.wait_for_timeout(120)
            f = out_dir / f"overlay-{i:02d}.png"
            page.screenshot(path=str(f), omit_background=True)
            paths.append(f)
        b.close()
    return paths


def main(post_dir):
    post = Path(post_dir)
    spec = json.loads((post / "reel.json").read_text())
    src = Path(spec["source"])
    if not src.is_absolute():
        src = post / src
    slug = spec["slug"]
    out = ROOT / "exports" / slug
    work = out / "_work"
    work.mkdir(parents=True, exist_ok=True)

    segs = spec["segments"]
    total = sum((s["end"] - s["start"]) / s.get("speed", 1.0) for s in segs)
    pngs = render_overlays(spec["overlays"], spec.get("handle", "@justinthymecurtis"), work)

    fc = []
    for i, s in enumerate(segs):
        sp = s.get("speed", 1.0)
        fc.append(f"[0:v]trim=start={s['start']}:end={s['end']},setpts=(PTS-STARTPTS)/{sp},"
                  f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30[v{i}]")
    grade = GRADES.get(spec.get("grade", "default"), spec.get("grade"))
    fc.append("".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0,"
              f"{grade}[base]")
    last = "base"
    inputs = ["-i", str(src)]
    for i, (o, png) in enumerate(zip(spec["overlays"], pngs)):
        inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(png)]
        st, en = o["start"], min(o["end"], total)
        fc.append(f"[{i+1}:v]format=rgba,fade=in:st={st}:d=0.25:alpha=1,fade=out:st={max(st, en-0.25)}:d=0.25:alpha=1[o{i}]")
        fc.append(f"[{last}][o{i}]overlay=0:0:enable='between(t,{st},{en})'[c{i}]")
        last = f"c{i}"

    reel = out / "reel.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", f"[{last}]",
           "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-an", str(reel)]
    subprocess.run(cmd, check=True)

    cover_t = spec.get("cover_at", 0.5)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(cover_t), "-i", str(reel), "-frames:v", "1",
                    "-q:v", "2", str(out / "cover.jpg")], check=True)
    print(f"Reel: {reel} ({total:.1f}s)")


if __name__ == "__main__":
    main(sys.argv[1])
