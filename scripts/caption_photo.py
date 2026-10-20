import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

SRC = sys.argv[1]
OUT = sys.argv[2]
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand", "fonts") + "/"

base = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
W, H = base.size
RIGHT = int(W * 0.955)   # right edge of text block, over the plain concrete wall
TOP = int(H * 0.075)
INK = (28, 28, 28)
OAK = (150, 108, 64)


def font(name, size, var=None):
    f = ImageFont.truetype(F + name, size)
    if var:
        f.set_variation_by_name(var)
    return f


def shadow_text(img, lines, color, blur=10, shadow=(255, 255, 255, 120)):
    """lines: list of (text, font, gap_after). Right aligned at RIGHT."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(layer), ImageDraw.Draw(sh)
    y = TOP
    for text, f, gap, col in lines:
        l, t, r, b = d.textbbox((0, 0), text, font=f)
        x = RIGHT - r
        ds.text((x, y - t), text, font=f, fill=shadow)
        d.text((x, y - t), text, font=f, fill=col or color)
        y += (b - t) + gap
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = Image.alpha_composite(img.convert("RGBA"), sh)
    return Image.alpha_composite(out, layer).convert("RGB")


def save(img, tag):
    img.save(f"{OUT}/caption-{tag}.jpg", quality=94)


# A: Anton caps, gym energy
img = shadow_text(base, [
    ("8 MONTHS", font("Anton-Regular.ttf", int(W * 0.082)), int(W * 0.008), None),
    ("25 UNITS CLOSED", font("Anton-Regular.ttf", int(W * 0.0395)), 0, OAK),
], INK)
save(img, "A")

# B: Instrument Serif, upright setup + italic payoff
img = shadow_text(base, [
    ("8 months.", font("InstrumentSerif-Regular.ttf", int(W * 0.09)), int(W * 0.004), None),
    ("25 units", font("InstrumentSerif-Italic.ttf", int(W * 0.09)), int(W * 0.004), OAK),
    ("closed.", font("InstrumentSerif-Italic.ttf", int(W * 0.09)), 0, OAK),
], INK)
save(img, "B")

# D: DM Serif Display, luxury, italic oak key words
img = shadow_text(base, [
    ("8 months", font("DMSerifDisplay-Regular.ttf", int(W * 0.076)), int(W * 0.004), None),
    ("25 units", font("DMSerifDisplay-Italic.ttf", int(W * 0.076)), int(W * 0.004), OAK),
    ("closed.", font("DMSerifDisplay-Regular.ttf", int(W * 0.076)), 0, None),
], INK)
save(img, "D")

# C: Montserrat Black caps on a black stats card
img = base.convert("RGBA")
big = font("Montserrat%5Bwght%5D.ttf", int(W * 0.05), "Black")
small = font("Montserrat%5Bwght%5D.ttf", int(W * 0.0222), "Black")
pad = int(W * 0.026)
d = ImageDraw.Draw(img)
b1 = d.textbbox((0, 0), "8 MONTHS", font=big)
b2 = d.textbbox((0, 0), "25 UNITS CLOSED", font=small)
bw = max(b1[2] - b1[0], b2[2] - b2[0]) + pad * 2
gap = int(W * 0.012)
bh = (b1[3] - b1[1]) + (b2[3] - b2[1]) + gap + pad * 2
x0, y0 = RIGHT - bw, TOP
card = Image.new("RGBA", img.size, (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle((x0 + 10, y0 + 14, x0 + bw + 10, y0 + bh + 14), radius=int(W * 0.03), fill=(0, 0, 0, 90))
card = card.filter(ImageFilter.GaussianBlur(14))
img = Image.alpha_composite(img, card)
d = ImageDraw.Draw(img)
d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=int(W * 0.03), fill=(16, 16, 16, 240))
cx = x0 + bw / 2
d.text((cx - (b1[2] + b1[0]) / 2, y0 + pad - b1[1]), "8 MONTHS", font=big, fill=(255, 255, 255))
y2 = y0 + pad + (b1[3] - b1[1]) + gap
d.text((cx - (b2[2] + b2[0]) / 2, y2 - b2[1]), "25 UNITS CLOSED", font=small, fill=(214, 178, 132))
save(img.convert("RGB"), "C")
print("done", W, H)
