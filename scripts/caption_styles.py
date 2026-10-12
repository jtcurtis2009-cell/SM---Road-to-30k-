"""Shared Reel caption font styles, picked by letter.

Used by make_reel.py ("font": "G" in reel.json) and caption_fonts.py (the comparison sheet).
Each style: label, setup line CSS, big word CSS, scale (multiplies the big word size so
wide fonts and condensed fonts land at a similar visual size), and the font faces it needs.
"""
import base64
import re
from pathlib import Path

FONTS = Path(__file__).resolve().parent.parent / "brand" / "fonts"

FACES = {
    "Fraunces": ("Fraunces[SOFT,WONK,opsz,wght].ttf", "font-weight:100 900;"),
    "DMSans": ("DMSans[opsz,wght].ttf", "font-weight:100 1000;"),
    "Gloock": ("Gloock-Regular.ttf", ""),
    "DMSerif": ("DMSerifDisplay-Regular.ttf", ""),
    "DMSerifItalic": ("DMSerifDisplay-Italic.ttf", ""),
    "Playfair": ("PlayfairDisplay[wght].ttf", "font-weight:400 900;"),
    "InstrumentItalic": ("InstrumentSerif-Italic.ttf", ""),
    "Bricolage": ("BricolageGrotesque[opsz,wdth,wght].ttf", "font-weight:200 800;"),
    "Anton": ("Anton-Regular.ttf", ""),
    "Bebas": ("BebasNeue-Regular.ttf", ""),
    "ArchivoBlack": ("ArchivoBlack-Regular.ttf", ""),
    "Abril": ("AbrilFatface-Regular.ttf", ""),
    "Montserrat": ("Montserrat[wght].ttf", "font-weight:100 900;"),
    "Oswald": ("Oswald[wght].ttf", "font-weight:200 700;"),
    "Syne": ("Syne[wght].ttf", "font-weight:400 800;"),
    "Unbounded": ("Unbounded[wght].ttf", "font-weight:200 900;"),
    "BigShoulders": ("BigShoulders[opsz,wght].ttf", "font-weight:100 900;"),
    "CormorantItalic": ("CormorantGaramond-Italic[wght].ttf", "font-weight:300 700;"),
    "Bodoni": ("BodoniModa[opsz,wght].ttf", "font-weight:400 900;"),
    "Poppins": ("Poppins-ExtraBold.ttf", "font-weight:800;"),
    "SpaceGrotesk": ("SpaceGrotesk[wght].ttf", "font-weight:300 700;"),
}

DM = "font-family:DMSans;font-weight:600"
CAPS = "text-transform:uppercase;"

STYLES = {
    # Set 1
    "A": ("Fraunces Soft + DM Sans (original default)", DM,
          "font-family:Fraunces;font-weight:900;font-variation-settings:'SOFT' 100,'WONK' 1,'opsz' 144;letter-spacing:-.03em", 1.0),
    "B": ("Gloock + DM Sans", DM, "font-family:Gloock;letter-spacing:-.02em", 1.0),
    "C": ("DM Serif Display + DM Sans", DM, "font-family:DMSerif;letter-spacing:-.02em", 1.0),
    "D": ("Playfair Display Black + DM Sans", DM, "font-family:Playfair;font-weight:900;letter-spacing:-.02em", 1.0),
    "E": ("Abril Fatface + DM Sans", DM, "font-family:Abril;letter-spacing:-.01em", 1.0),
    "F": ("Instrument Serif Italic + Bricolage", "font-family:Bricolage;font-weight:600",
          "font-family:InstrumentItalic;letter-spacing:-.02em;color:#E9C9A6", 1.05),
    "G": ("Anton caps + DM Sans (gym energy)", "font-family:DMSans;font-weight:700;letter-spacing:.08em;" + CAPS,
          "font-family:Anton;letter-spacing:.01em;" + CAPS, 0.95),
    "H": ("Bebas Neue + Montserrat", "font-family:Montserrat;font-weight:600;letter-spacing:.04em",
          "font-family:Bebas;letter-spacing:.02em;" + CAPS, 1.05),
    "I": ("Archivo Black + Instrument italic", "font-family:InstrumentItalic;font-size:1.25em",
          "font-family:ArchivoBlack;letter-spacing:-.04em", 0.9),
    "J": ("Montserrat Black (clean sans)", "font-family:Montserrat;font-weight:500",
          "font-family:Montserrat;font-weight:900;letter-spacing:-.04em", 0.9),
    # Set 2
    "K": ("Oswald Bold caps + DM Sans (athletic)", "font-family:DMSans;font-weight:600;letter-spacing:.04em",
          "font-family:Oswald;font-weight:700;letter-spacing:-.01em;" + CAPS, 0.95),
    "L": ("Unbounded Black (round, modern, bubbly)", "font-family:DMSans;font-weight:600",
          "font-family:Unbounded;font-weight:900;letter-spacing:-.05em", 0.72),
    "M": ("Syne ExtraBold + Space Grotesk (editorial)", "font-family:SpaceGrotesk;font-weight:500",
          "font-family:Syne;font-weight:800;letter-spacing:-.04em", 0.85),
    "N": ("Bodoni Moda Black Italic (luxury)", "font-family:Montserrat;font-weight:600;letter-spacing:.12em;" + CAPS + "font-size:.8em",
          "font-family:Bodoni;font-weight:900;font-style:italic;letter-spacing:-.03em", 1.0),
    "O": ("Cormorant Italic + Montserrat caps (elegant, faith)",
          "font-family:Montserrat;font-weight:600;letter-spacing:.18em;" + CAPS + "font-size:.75em",
          "font-family:CormorantItalic;font-weight:700;letter-spacing:-.02em", 1.15),
    "P": ("Big Shoulders Black caps (stadium)", "font-family:DMSans;font-weight:700;letter-spacing:.1em;" + CAPS,
          "font-family:BigShoulders;font-weight:900;letter-spacing:.01em;" + CAPS, 1.1),
    "Q": ("Poppins ExtraBold + DM Serif italic setup", "font-family:DMSerifItalic;font-size:1.2em",
          "font-family:Poppins;letter-spacing:-.05em", 0.85),
    "R": ("DM Serif Italic in light oak + DM Sans", DM,
          "font-family:DMSerifItalic;letter-spacing:-.02em;color:#C8A982", 1.05),
    "S": ("Anton caps in light oak + Instrument italic", "font-family:InstrumentItalic;font-size:1.25em",
          "font-family:Anton;color:#C8A982;" + CAPS, 0.95),
    "T": ("Fraunces Soft in light oak + DM Sans", DM,
          "font-family:Fraunces;font-weight:900;font-variation-settings:'SOFT' 100,'WONK' 1,'opsz' 144;letter-spacing:-.03em;color:#C8A982", 1.0),
}


def style(letter):
    label, setup_css, big_css, scale = STYLES[letter.upper()]
    return {"label": label, "setup": setup_css, "big": big_css, "scale": scale}


def faces_used(letters):
    css = " ".join(STYLES[l][1] + STYLES[l][2] for l in letters)
    names = set(re.findall(r"font-family:(\w+)", css)) | {"DMSans"}
    return names


def face_css(names=None):
    out = []
    for name, (file, extra) in FACES.items():
        if names is not None and name not in names:
            continue
        b = base64.b64encode((FONTS / file).read_bytes()).decode()
        out.append(f"@font-face{{font-family:'{name}';src:url(data:font/ttf;base64,{b});{extra}}}")
    return "".join(out)
