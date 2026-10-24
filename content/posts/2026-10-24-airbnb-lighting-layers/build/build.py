"""Airbnb lighting layers Reel: 30s, 120 bpm, cuts on the beat.

Usage: python3 build.py <IMG_2319.mov> <out_dir> [--styles A,B,C,D,E]
Raw clip is not committed. Source is iPhone HLG HDR, tonemapped to SDR here.
"""
import subprocess, sys, json, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[4]
FONTS = ROOT / "brand" / "fonts"
P = json.loads((ROOT / "brand" / "palette.json").read_text())
W, H, FPS, BEAT = 1080, 1920, 30, 0.5
HANDLE = "@justinthymecurtis"

# (source second, beats). 60 beats = 30s.
SHOTS = [
    # hook: lock glow
    (2.0, 2), (4.5, 1), (6.2, 1), (7.0, 2),
    # layer 1 wash the walls
    (11.3, 1), (14.2, 1), (15.1, 1), (16.0, 3), (17.3, 2), (28.2, 1), (30.2, 2),
    # layer 2 hide the source
    (24.0, 1), (25.3, 1), (26.2, 2), (36.2, 2), (37.6, 1), (38.5, 1), (42.3, 1), (118.4, 2),
    # layer 3 one statement piece
    (39.5, 1), (40.4, 1), (44.6, 1), (48.4, 1), (50.3, 1), (51.5, 2), (53.0, 3), (55.0, 2), (59.2, 1), (60.3, 1),
    # layer 4 color after dark
    (63.3, 1), (64.2, 1), (70.3, 1), (71.2, 1), (75.4, 1), (76.3, 2), (98.0, 1), (105.3, 1),
    # close: back to the lock so it loops
    (82.2, 1), (0.0, 8),
]
assert sum(b for _, b in SHOTS) == 60

TEXT = [  # (start, end, small setup, big word)
    (0.0, 3.0, "4 lighting layers that", "sell the stay"),
    (3.0, 8.5, "layer 1", "wash the walls"),
    (8.5, 14.0, "layer 2", "hide the source"),
    (14.0, 21.0, "layer 3", "one statement piece"),
    (21.0, 25.5, "layer 4", "color after dark"),
    (25.5, 30.0, "save this for your", "next furnish"),
]

# Grade: tonemap HLG, warm the shadows, glow on the practicals, soft vignette.
TONEMAP = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
GRADE = ("eq=contrast=1.10:saturation=1.15:gamma=0.96,"
         "colorbalance=rs=0.04:gs=0.01:bs=-0.04:rh=0.03:bh=-0.03,"
         "split[a][b];[b]curves=all='0/0 0.62/0 1/1',gblur=sigma=28[g];[a][g]blend=all_mode=screen:all_opacity=0.35,"
         "vignette=PI/5")


def run(cmd):
    subprocess.run(cmd, check=True)


def cut(src, i, t, beats, tmp):
    n = int(round(beats * BEAT * FPS))
    zoom = "1+0.12*max(0\\,1-t/0.25)" if i % 2 else "1.04+0.03*t"  # punch in on alternating cuts, slow push on the rest
    flash = "0.18*max(0\\,1-t/0.12)" if i else "0"  # quick light flash on every cut
    vf = (f"[0:v]{TONEMAP},fps={FPS},setpts=PTS-STARTPTS,"
          f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
          f"scale=w='trunc({W}*({zoom})/2)*2':h='trunc({H}*({zoom})/2)*2':eval=frame,crop={W}:{H},"
          f"unsharp=5:5:0.8,{GRADE},eq=brightness='{flash}':eval=frame,format=yuv420p")
    out = tmp / f"s{i:02d}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(src), "-filter_complex", vf, "-frames:v", str(n),
         "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", str(out)])
    return out


def font(file, size, axes=None):
    f = ImageFont.truetype(str(FONTS / file), size)
    if axes:
        try:
            f.set_variation_by_axes(axes)
        except Exception:
            pass
    return f


def hexc(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


# Five text styles. Each returns (setup_font, big_font, big_color, upper, stroke)
def style(name):
    oak, bone = hexc(P["rust_light"]), (255, 255, 255, 255)
    if name == "A":  # Montserrat Black caps, black outline
        mf = lambda s: font("Montserrat%5Bwght%5D.ttf", s, [900])
        return dict(sf=mf(54), bf=mf(150), bc=bone, sc=bone, upper=True, stroke=8, lh=0.98)
    if name == "B":  # Anton caps, oak big word
        return dict(sf=font("DMSans[opsz,wght].ttf", 54, [14, 700]), bf=font("Anton-Regular.ttf", 190),
                    bc=oak, sc=bone, upper=True, stroke=0, lh=1.0)
    if name == "C":  # house default: DM Sans setup over Fraunces Soft
        return dict(sf=font("DMSans[opsz,wght].ttf", 56, [14, 600]),
                    bf=font("Fraunces[SOFT,WONK,opsz,wght].ttf", 170, [144, 900, 100, 1]),
                    bc=bone, sc=bone, upper=False, stroke=0, lh=0.9)
    if name == "D":  # Instrument Serif italic, oak
        return dict(sf=font("DMSans[opsz,wght].ttf", 58, [14, 600]), bf=font("InstrumentSerif-Italic.ttf", 210),
                    bc=bone, sc=bone, upper=False, stroke=0, lh=0.9)
    if name == "E":  # DM Serif Display italic (luxury)
        return dict(sf=font("DMSans[opsz,wght].ttf", 58, [14, 600]), bf=font("DMSerifDisplay-Italic.ttf", 165),
                    bc=bone, sc=bone, upper=False, stroke=0, lh=0.98)
    raise ValueError(name)


def wrap(text, f, maxw, d):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def overlay(setup, big, s, end=False):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if s["upper"]:
        setup, big = setup.upper(), big.upper()
    lines = wrap(big, s["bf"], W - 140, d)
    a_, d_ = s["bf"].getmetrics()
    asc = a_ + d_ * 0.4
    # soft top shade so text reads over bright walls
    shade = Image.new("L", (1, H))
    for yy in range(H):
        shade.putpixel((0, yy), int(120 * max(0, 1 - yy / 1050)))
    top = Image.new("RGBA", (W, H), (0, 0, 0, 0)); top.putalpha(shade.resize((W, H)))
    y = 330
    d.text((W / 2, y), setup, font=s["sf"], fill=s["sc"], anchor="mt")
    y += s["sf"].size + 24
    for ln in lines:
        d.text((W / 2, y), ln, font=s["bf"], fill=s["bc"], anchor="mt",
               stroke_width=s["stroke"], stroke_fill=(0, 0, 0, 255))
        y += int(asc * s["lh"])
    if end:
        hf = font("DMSans[opsz,wght].ttf", 40, [14, 700])
        tw = d.textlength(HANDLE, font=hf)
        y += 30
        d.rounded_rectangle([W / 2 - tw / 2 - 34, y, W / 2 + tw / 2 + 34, y + 76], 38, fill=hexc(P["rust"]))
        d.text((W / 2, y + 38), HANDLE, font=hf, fill=hexc(P["sand"]), anchor="mm")
    # soft shadow
    txt = img
    a = txt.split()[3].filter(ImageFilter.GaussianBlur(14))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.55)))
    return Image.alpha_composite(Image.alpha_composite(top, sh), txt)


def main(src, out_dir, styles):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_tmp"; tmp.mkdir(exist_ok=True)
    base = out / "base.mp4"
    if not base.exists():
        parts = [cut(src, i, t, b, tmp) for i, (t, b) in enumerate(SHOTS)]
        (tmp / "list.txt").write_text("".join(f"file '{p.name}'\n" for p in parts))
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-c", "copy", str(base)])
    beat = out / "beat.wav"
    if not beat.exists():
        run(["python3", str(Path(__file__).parent / "make_beat.py"), str(beat), "--bpm", "120", "--seconds", "30", "--mood", "bright"])
    for name in styles:
        s = style(name)
        pngs, inputs, chain, last = [], [], "", "0:v"
        for k, (a, b, setup, big) in enumerate(TEXT):
            p = tmp / f"t{name}{k}.png"
            overlay(setup, big, s, end=(k == len(TEXT) - 1)).save(p)
            inputs += ["-loop", "1", "-t", "30", "-i", str(p)]
            chain += (f"[{k + 2}:v]format=rgba,fade=in:st={a}:d=0.12:alpha=1[o{k}];"
                      f"[{last}][o{k}]overlay=0:0:enable='between(t,{a},{b - 0.001})'[v{k}];")
            last = f"v{k}"
        for silent in (False, True):
            f = out / (f"reel-{name}-silent.mp4" if silent else f"reel-{name}.mp4")
            amap = ["-an"] if silent else ["-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
            run(["ffmpeg", "-v", "error", "-y", "-i", str(base), "-i", str(beat), *inputs,
                 "-filter_complex", chain.rstrip(";"), "-map", f"[{last}]", *amap,
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
                 "-movflags", "+faststart", str(f)])
        fr = tmp / "coverframe.png"
        run(["ffmpeg", "-v", "error", "-y", "-ss", "19.2", "-i", str(base), "-frames:v", "1", str(fr)])
        c = Image.open(fr).convert("RGBA"); c.alpha_composite(Image.open(tmp / f"t{name}0.png"))
        c.convert("RGB").save(out / f"cover-{name}.jpg", quality=92)
        print("built", name)


if __name__ == "__main__":
    st = "A,B,C,D,E"
    if "--styles" in sys.argv:
        st = sys.argv[sys.argv.index("--styles") + 1]
    main(sys.argv[1], sys.argv[2], st.split(","))
