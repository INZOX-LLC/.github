"""Shared brand system for the INZOX GitHub profile artwork.

Every asset is a self-contained SVG: fonts are subset and embedded as
base64 WOFF2, there are no external references, and all motion is CSS
keyframes or SMIL, both of which survive GitHub's <img> sandbox.
"""

import base64
import functools
import io
import os
import random
import re

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(ROOT, "fonts")

# Palette: INZOX web blues (#1684FF / #52A4F6 / #87C3FF on #000022) fused
# with the ZOX product cyans (#2EB8EA / #4FD2FF on #04070D).
C = dict(
    void="#030614",
    deep="#060D24",
    panel="#0A1430",
    panel2="#0D1A3D",
    line="#1A2B55",
    grid="#12204A",
    blue="#1684FF",
    sky="#52A4F6",
    ice="#87C3FF",
    cyan="#2EB8EA",
    aqua="#4FD2FF",
    violet="#9747FF",
    lilac="#B98BFF",
    mint="#22E3A6",
    amber="#FFB547",
    rose="#FF5C7A",
    text="#E8F1FF",
    soft="#B4C3E0",
    muted="#7A8CB0",
    dim="#3A4A70",
)

FONTS = {
    # css family: (file, weight)
    "IZ Display": ("SpaceGrotesk[wght].ttf", 700),
    "IZ Body": ("SpaceGrotesk[wght].ttf", 500),
    "IZ Mono": ("JetBrainsMono[wght].ttf", 500),
    "IZ MonoBold": ("JetBrainsMono[wght].ttf", 700),
}
CLASS_FONT = {"d": "IZ Display", "b": "IZ Body", "m": "IZ Mono", "mb": "IZ MonoBold"}
FALLBACK = {
    "IZ Display": "'Segoe UI',Helvetica,Arial,sans-serif",
    "IZ Body": "'Segoe UI',Helvetica,Arial,sans-serif",
    "IZ Mono": "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace",
    "IZ MonoBold": "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace",
}


@functools.lru_cache(maxsize=None)
def _instance(family):
    file, wght = FONTS[family]
    font = TTFont(os.path.join(FONT_DIR, file))
    return instancer.instantiateVariableFont(font, {"wght": wght})


def measure(text, family, size, spacing=0.0):
    """Advance width of `text` in user units (no kerning)."""
    font = _instance(family)
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    upm = font["head"].unitsPerEm
    total = 0
    for ch in text:
        g = cmap.get(ord(ch))
        total += hmtx[g][0] if g else upm * 0.6
    return total * size / upm + spacing * max(len(text) - 1, 0)


def _font_face(family, chars):
    font = _instance(family)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    clone = TTFont(buf)
    sub.subset(clone)
    clone.flavor = "woff2"
    out = io.BytesIO()
    clone.save(out)
    data = base64.b64encode(out.getvalue()).decode()
    return (
        f"@font-face{{font-family:'{family}';"
        f"src:url(data:font/woff2;base64,{data}) format('woff2');}}"
    )


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _text_chars(body):
    chars = set()
    for chunk in re.findall(r">([^<]+)<", body):
        chunk = (
            chunk.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        )
        chars.update(chunk)
    chars.update(" .,")
    return "".join(sorted(chars))


BASE_CSS = """
.d{font-family:'IZ Display',@d;font-weight:700}
.b{font-family:'IZ Body',@b;font-weight:500}
.m{font-family:'IZ Mono',@m;font-weight:500}
.mb{font-family:'IZ MonoBold',@mb;font-weight:700}
.spin{animation:spin 40s linear infinite}
.spinr{animation:spin 60s linear infinite reverse}
.blink{animation:blink 1.1s steps(1) infinite}
.pulse{animation:pulse 2.4s ease-in-out infinite}
.twinkle{animation:twinkle 4s ease-in-out infinite}
.march{stroke-dasharray:6 8;animation:march 1.2s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes blink{50%{opacity:0}}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
@keyframes twinkle{0%,100%{opacity:.15}50%{opacity:.9}}
@keyframes march{to{stroke-dashoffset:-28}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""
for _k in ("mb", "d", "b", "m"):
    BASE_CSS = BASE_CSS.replace("@" + _k + ";", FALLBACK[CLASS_FONT[_k]] + ";")


def svg(w, h, body, title, desc, css="", defs="", panel=True, radius=22):
    """Wrap `body` into a complete standalone SVG document."""
    used = {CLASS_FONT[c] for c in CLASS_FONT if re.search(r'class="[^"]*\b%s\b' % c, body)}
    chars = _text_chars(body)
    faces = "".join(_font_face(f, chars) for f in sorted(used))
    bg = ""
    clip_open = clip_close = ""
    if panel:
        bg = (
            f'<rect width="{w}" height="{h}" rx="{radius}" fill="url(#panelbg)"/>'
            f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{radius - .75}" '
            f'fill="none" stroke="{C["line"]}" stroke-width="1.5"/>'
        )
        clip_open = '<g clip-path="url(#frame)">'
        clip_close = "</g>"
        defs = (
            f'<clipPath id="frame"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath>'
            f'<radialGradient id="panelbg" cx="70%" cy="20%" r="95%">'
            f'<stop offset="0" stop-color="#0B1C46"/><stop offset=".55" stop-color="{C["deep"]}"/>'
            f'<stop offset="1" stop-color="{C["void"]}"/></radialGradient>'
        ) + defs
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" fill="none">'
        f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
        f"<style>{faces}{BASE_CSS}{css}</style>"
        f"<defs>{defs}</defs>"
        f"{clip_open}{bg}{body}{clip_close}</svg>"
    )


def text(x, y, s, cls="b", size=16, fill=None, anchor="start", extra=""):
    fill = fill or C["text"]
    a = "" if anchor == "start" else f' text-anchor="{anchor}"'
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size}" '
        f'fill="{fill}"{a} {extra}>{esc(s)}</text>'
    )


def chip(x, y, label, color, size=12, pad=12, h=26, dot=True, fill=None, cls="m"):
    """Pill-shaped tag. Returns (svg, width)."""
    fam = CLASS_FONT[cls]
    tw = measure(label, fam, size, 0.6)
    w = tw + pad * 2 + (14 if dot else 0)
    fill = fill or C["panel2"]
    out = (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" '
        f'fill="{fill}" stroke="{color}" stroke-opacity=".55"/>'
    )
    tx = x + pad
    if dot:
        out += f'<circle cx="{x + pad + 3:.1f}" cy="{y + h / 2:.1f}" r="3.2" fill="{color}"/>'
        tx += 14
    out += text(tx, y + h / 2 + size * 0.36, label, cls, size, C["soft"], extra='letter-spacing=".6"')
    return out, w


def stars(w, h, n, seed=7, color=None, ymax=None):
    rnd = random.Random(seed)
    color = color or C["ice"]
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, ymax or h)
        r = rnd.choice([0.6, 0.8, 1.0, 1.3])
        d = rnd.uniform(0, 4)
        out.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{color}" class="twinkle" '
            f'style="animation-delay:-{d:.1f}s"/>'
        )
    return "".join(out)
