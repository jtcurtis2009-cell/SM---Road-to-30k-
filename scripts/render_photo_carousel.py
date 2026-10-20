import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

CAFE, SUNSET, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
F = sys.argv[4] if len(sys.argv) > 4 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand", "fonts")
F = F.rstrip("/") + "/"
W, H = 1080, 1350  # Instagram 4:5 carousel
INK = (26, 29, 34)
OAK = (168, 131, 95)
LOAK = (200, 169, 130)
BONE = (237, 231, 221)
COGNAC = (138, 90, 59)
WHITE = (255, 255, 255)


def font(name, size, var=None):
    f = ImageFont.truetype(F + name, size)
    if var:
        f.set_variation_by_name(var)
    return f


def fit(path, cy=0.5):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    s = W / im.width
    im = im.resize((W, round(im.height * s)), Image.LANCZOS)
    top = int((im.height - H) * cy)
    return im.crop((0, top, W, top + H))


LH = 1.08  # line height as a multiple of font size, baseline to baseline


def draw_block(img, lines, x, y, align, shadow, blur=12):
    """lines: (text, font, color, gap_after). y is the top of the block. Baseline spacing keeps lines even."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(layer), ImageDraw.Draw(sh)
    y += lines[0][1].size * 0.78
    for i, (text, f, col, gap) in enumerate(lines):
        if i:
            y += f.size * LH
        l, t, r, b = d.textbbox((0, 0), text, font=f, anchor="ls")
        tx = x - r if align == "right" else x - (l + r) / 2
        ds.text((tx, y), text, font=f, fill=shadow, anchor="ls")
        d.text((tx, y), text, font=f, fill=col, anchor="ls")
        y += gap
    out = Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(blur)))
    return Image.alpha_composite(out, layer).convert("RGB")


def block_height(lines):
    h = lines[0][1].size * 0.78
    for i, (text, f, col, gap) in enumerate(lines):
        h += (f.size * LH if i else 0) + gap
    return h + lines[-1][1].size * 0.22


# Each style: fonts for setup line, key line, and the scripture slide
STYLES = {
    "serif": dict(  # Instrument Serif, upright setup + italic oak payoff
        setup=("InstrumentSerif-Regular.ttf", 92, None),
        key=("InstrumentSerif-Italic.ttf", 92, None),
        verse=("InstrumentSerif-Italic.ttf", 76, None),
        ref=("InstrumentSerif-Regular.ttf", 40, None),
        caps=False,
    ),
    "luxury": dict(  # DM Serif Display with italic oak key words
        setup=("DMSerifDisplay-Regular.ttf", 80, None),
        key=("DMSerifDisplay-Italic.ttf", 80, None),
        verse=("DMSerifDisplay-Regular.ttf", 64, None),
        ref=("DMSerifDisplay-Italic.ttf", 38, None),
        caps=False,
    ),
    "bold": dict(  # Anton caps, gym energy
        setup=("Anton-Regular.ttf", 64, None),
        key=("Anton-Regular.ttf", 96, None),
        verse=("Anton-Regular.ttf", 66, None),
        ref=("Montserrat%5Bwght%5D.ttf", 30, "Bold"),
        caps=True,
    ),
}

S1 = ("There is a time", "to be locked in.")
S2 = ("And a time to", "reflect with gratitude.")
S2_KEY = ("reflect with", "gratitude.")
VERSE = ["To every thing", "there is a season,", "and a time to", "every purpose", "under the heaven."]
REF = "Ecclesiastes 3:1"

cafe = fit(CAFE, 0.5)
sunset = fit(SUNSET, 0.62)


def lift(img, shadows=0.55, gamma=0.78, sat=1.08):
    """Brighten shadows and midtones while keeping the bright sky from blowing out."""
    import numpy as np
    a = np.asarray(img).astype(np.float32) / 255.0
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    target = lum ** gamma
    target = target + shadows * (1 - target) * (1 - lum) ** 3 * 0.35
    ratio = np.where(lum > 1e-4, target / np.maximum(lum, 1e-4), 1.0)[..., None]
    out = np.clip(a * ratio, 0, 1)
    g = out.mean(axis=2, keepdims=True)
    out = np.clip(g + (out - g) * sat, 0, 1)
    return Image.fromarray((out * 255).astype("uint8"))


sunset = lift(sunset, shadows=0.35, gamma=0.86, sat=0.96)

for name, st in STYLES.items():
    C = (lambda s: s.upper()) if st["caps"] else (lambda s: s)
    fs = font(*st["setup"])
    fk = font(*st["key"])
    os.makedirs(f"{OUT}/{name}", exist_ok=True)

    # Slide 1, cafe: dark ink on the concrete wall, top right
    # auto size so the widest line stays on the wall, right of the pole
    words = [C("There is a time"), C("to be"), C("locked in.")]
    dd = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    size = 140
    while True:
        f1 = font(st["setup"][0], size, st["setup"][2])
        f1k = font(st["key"][0], size, st["key"][2])
        wmax = max(dd.textlength(t, font=f) for t, f in zip(words, [f1, f1, f1k]))
        if wmax <= W * 0.305:
            break
        size -= 2
    lines = [(words[0], f1, INK, 0), (words[1], f1, INK, 0), (words[2], f1k, COGNAC, 0)]
    s1 = draw_block(cafe, lines, int(W * 0.95), int(H * 0.045), "right", (255, 255, 255, 190), blur=10)
    s1.save(f"{OUT}/{name}/slide-1.jpg", quality=93)

    # Slide 2, sunset: white in the open sky, centered
    lines = [(C(S2[0]), fs, WHITE, 0), (C(S2_KEY[0]), fk, WHITE, 0), (C(S2_KEY[1]), fk, (255, 214, 168), 0)]
    s2 = draw_block(sunset, lines, W // 2, int(H * 0.10), "center", (20, 24, 34, 150), blur=16)
    s2.save(f"{OUT}/{name}/slide-2.jpg", quality=93)

    # Slide 3, scripture: blurred, darkened sunset sky, bone text
    # sky only: from the top of the photo down to just past the horizon, so the slide is a soft sunset gradient
    raw = ImageOps.exif_transpose(Image.open(SUNSET)).convert("RGB")
    sky = raw.crop((int(raw.width * 0.1), 0, int(raw.width * 0.9), int(raw.height * 0.45)))
    bg = sky.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))
    shade = Image.new("RGB", (W, H), INK)
    bg = Image.blend(bg, shade, 0.22)
    fv = font(*st["verse"])
    fr = font(*st["ref"])
    vl = [(C(t), fv, BONE, 0) for t in VERSE]
    vl[-1] = (vl[-1][0], fv, BONE, 30)
    vl.append((C(REF) if st["caps"] else REF, fr, BONE, 0))
    y0 = (H - block_height(vl)) // 2
    s3 = draw_block(bg, vl, W // 2, y0, "center", (10, 14, 24, 150), blur=14)
    d = ImageDraw.Draw(s3)
    d.line((W // 2 - 40, y0 - 60, W // 2 + 40, y0 - 60), fill=LOAK, width=3)
    s3.save(f"{OUT}/{name}/slide-3.jpg", quality=93)

print("done")
