"""Airbnb lighting layers Reel: 30s flow edit: soft dissolves, slow push in, 96 bpm bed.

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

# Speed ramp edit: each shot drifts in slow motion, then whips fast into the next. Last shot stays slow.
# (source second, seconds on screen, section). Durations are scaled so the Reel is exactly 30s.
XF = 0.12  # tiny blend at the fast peak
SLOW, FAST, RAMP = 0.5, 3.0, 0.3  # slow motion speed, whip speed, share of each shot spent ramping
SHOTS = [
    (2.0, 1.9, 0), (4.3, 1.8, 0),
    (13.8, 2.2, 1), (15.6, 2.4, 1), (29.8, 1.8, 1),
    (24.0, 2.4, 2), (36.0, 1.8, 2), (117.2, 2.2, 2),
    (39.2, 2.2, 3), (50.6, 2.2, 3), (53.0, 2.8, 3),
    (63.0, 1.9, 4), (70.0, 1.9, 4), (75.6, 2.0, 4),
    (59.4, 4.2, 5),
]
_k = (30 + XF * (len(SHOTS) - 1)) / sum(d for _, d, _ in SHOTS)
SHOTS = [(t, d * _k, sec) for t, d, sec in SHOTS]

COPY = [  # (small setup, big line) per section
    ("great airbnbs aren't furnished,", "they're lit"),
    ("aim light at the walls,", "not the floor"),
    ("hide the bulb,", "show the glow"),
    ("one fixture guests", "photograph"),
    ("after sunset,", "light the water"),
    ("your photos are only as good as", "your light"),
]


def text_times():
    starts, t = [], 0.0
    for i, (_, d, sec) in enumerate(SHOTS):
        if not starts or sec != SHOTS[i - 1][2]:
            starts.append(max(0.0, t - (XF / 2 if i else 0)))
        t += d - XF
    ends = starts[1:] + [30.0]
    return [(a, b, *c) for a, b, c in zip(starts, ends, COPY)]


# Grade: tonemap HLG, warm the shadows, glow on the practicals, soft vignette.
TONEMAP = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
GRADE = ("eq=contrast=1.10:saturation=1.15:gamma=0.96,"
         "colorbalance=rs=0.04:gs=0.01:bs=-0.04:rh=0.03:bh=-0.03,"
         "split[a][b];[b]curves=all='0/0 0.62/0 1/1',gblur=sigma=28[g];[a][g]blend=all_mode=screen:all_opacity=0.35,"
         "vignette=PI/5")


def run(cmd):
    subprocess.run(cmd, check=True)


def cut(src, i, t, dur, tmp):
    n = int(round(dur * FPS))
    last = i == len(SHOTS) - 1
    slow_out = dur if last else dur * (1 - RAMP)
    fast_out = 0 if last else dur * RAMP
    s_src, f_src = slow_out * SLOW, fast_out * FAST
    smooth = "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:vsbmc=1"
    if last:
        speed = f"{smooth},setpts={1 / SLOW}*PTS,fps={FPS}"
    else:
        speed = (f"split[a][b];[a]trim=0:{s_src:.3f},setpts=PTS-STARTPTS,{smooth},setpts={1 / SLOW}*PTS,fps={FPS}[sa];"
                 f"[b]trim={s_src:.3f}:{s_src + f_src:.3f},setpts=PTS-STARTPTS,setpts=PTS/{FAST},tmix=frames=4,fps={FPS}[fa];"
                 f"[sa][fa]concat=n=2:v=1")
    r0 = slow_out / dur
    zoom = f"1.02+0.03*t/{dur:.3f}+0.10*pow(max(0\\,t/{dur:.3f}-{r0:.3f})/{max(1 - r0, 0.01):.3f}\\,2)"
    vf = (f"[0:v]{TONEMAP},{speed},setpts=PTS-STARTPTS,"
          f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
          f"scale=w='trunc({W}*({zoom})/2)*2':h='trunc({H}*({zoom})/2)*2':eval=frame,crop={W}:{H},"
          f"unsharp=5:5:0.8,{GRADE},format=yuv420p")
    out = tmp / f"r{i:02d}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-t", f"{s_src + f_src + 0.5:.3f}", "-i", str(src),
         "-filter_complex", vf, "-frames:v", str(n), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", str(out)])
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
        return dict(sf=mf(44), bf=mf(150), bc=bone, sc=bone, upper=True, stroke=8, lh=0.98)
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


def overlay(setup, big, s):
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
        parts = [cut(src, i, t, d, tmp) for i, (t, d, _) in enumerate(SHOTS)]
        inp, fc, last, off = [], "", "0:v", 0.0
        for i, pth in enumerate(parts):
            inp += ["-i", str(pth)]
            if i:
                off += SHOTS[i - 1][1] - XF
                fc += f"[{last}][{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}];"
                last = f"x{i}"
        run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", fc.rstrip(";"), "-map", f"[{last}]", "-t", "30",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", str(base)])
    beat = out / "beat.wav"
    if not beat.exists():
        run(["python3", str(Path(__file__).parent / "make_beat.py"), str(beat), "--bpm", "96", "--seconds", "30", "--mood", "dark"])
    for name in styles:
        s = style(name)
        pngs, inputs, chain, last = [], [], "", "0:v"
        for k, (a, b, setup, big) in enumerate(text_times()):
            p = tmp / f"t{name}{k}.png"
            overlay(setup, big, s).save(p)
            inputs += ["-loop", "1", "-t", "30", "-i", str(p)]
            chain += (f"[{k + 2}:v]format=rgba,fade=in:st={a}:d=0.3:alpha=1[o{k}];"
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
        run(["ffmpeg", "-v", "error", "-y", "-ss", "17.5", "-i", str(base), "-frames:v", "1", str(fr)])
        c = Image.open(fr).convert("RGBA"); c.alpha_composite(Image.open(tmp / f"t{name}0.png"))
        c.convert("RGB").save(out / f"cover-{name}.jpg", quality=92)
        print("built", name)


if __name__ == "__main__":
    st = "A,B,C,D,E"
    if "--styles" in sys.argv:
        st = sys.argv[sys.argv.index("--styles") + 1]
    main(sys.argv[1], sys.argv[2], st.split(","))
