#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Generates the falkOSS brand kit: master SVGs, PNG exports, favicon.ico and the website's icons.

The mark: a falcon seen from below, all straight edges, over the lake as two flat waveforms (Falkensee – Falcon
Lake) – amber like an amber-phosphor terminal on near-black. The wordmark is drawn from angular, chamfered strokes
(no font needed): "falk" in light, "OSS" in amber.

Needs rsvg-convert (Homebrew: librsvg). Run from anywhere:
    python3 generate.py
Edit this file, not the exports.
"""
import os, shutil, struct, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SVG, PNG = os.path.join(HERE, "svg"), os.path.join(HERE, "png")
SITE = os.path.join(os.path.dirname(HERE), "assets")

NIGHT = "#0B0D10"        # near-black – backgrounds
FALCON = "#FFB000"       # amber, like an amber-phosphor terminal – the falcon, OSS, accents
LAKE = "#5B7083"         # steel – the lake, lines, secondary
MIST = "#E6EDF3"         # light text on dark
INK = "#0B0D10"          # text on light
REED = "#7D8590"         # muted text
FALCON_DARK = "#B87800"  # amber on light backgrounds
LAKE_DARK = "#4A5D70"    # steel on light backgrounds


def svg(view_box, body, size=None):
    dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}"{dims}>\n{body}\n</svg>\n'


# --- mark ------------------------------------------------------------------------------------------------------------

def falcon(color):
    """Falcon from below in a 1024 box, all straight edges: wings bent at the wrist and swept back to a point,
    a faceted body and a squared tail – an insignia, not an illustration."""
    def wing(sign):
        pts = [(506, 380), (340, 344), (270, 382), (104, 540), (292, 482), (506, 492)]
        return "M" + " L".join(f"{a if sign < 0 else 1024 - a},{b}" for a, b in pts) + " Z"
    body = "M512,292 L548,322 L546,410 L532,566 L492,566 L478,410 L476,322 Z"
    tail = "M492,552 L532,552 L566,690 L512,712 L458,690 Z"
    return (f'<g fill="{color}"><path d="{wing(-1)}"/><path d="{wing(1)}"/><path d="{body}"/>'
            f'<path d="{tail}"/></g>')


def lake(color, width=28):
    """The lake as two flat waveforms (straight segments)."""
    w = ('<polyline points="200,806 328,806 376,778 472,834 568,778 664,834 712,806 824,806"/>'
         '<polyline points="312,902 712,902"/>')
    return f'<g fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="square" stroke-linejoin="miter">{w}</g>'


def mark(bird=FALCON, water=LAKE):
    return falcon(bird) + lake(water)


def icon(bg=NIGHT, rounded=True):
    """App/avatar icon: the mark on night, rounded square (macOS-like radius) or full bleed."""
    r = 160 if rounded else 0
    return svg("0 0 1024 1024", f'<rect width="1024" height="1024" rx="{r}" fill="{bg}"/>'
               f'<g transform="translate(512 540) scale(0.86) translate(-512 -600)">{mark()}</g>')


def small_icon(bg=NIGHT):
    """16–48 px: the falcon a little larger, one heavy line for the lake."""
    return svg("0 0 1024 1024", f'<rect width="1024" height="1024" rx="160" fill="{bg}"/>'
               f'<g transform="translate(512 500) scale(1.02) translate(-512 -560)">{falcon(FALCON)}'
               f'<line x1="232" y1="830" x2="792" y2="830" stroke="{LAKE}" stroke-width="70"/></g>')


# --- wordmark (strokes on a 100-unit cap height, baseline y=100) -----------------------------------------------------

GLYPHS = {
    # (advance width, path) – angular, chamfered terminal letters; x-height 40..100, ascender 8, caps 12..100
    "f": (40, "M14,100 V24 L28,10 H38 M2,44 H32"),
    "a": (56, "M48,44 V100 M48,58 L36,44 H16 L6,54 V90 L16,100 H36 L48,88"),
    "l": (22, "M10,8 V100"),
    "k": (52, "M10,8 V100 M46,44 L10,78 M26,64 L48,100"),
    "O": (80, "M20,12 H60 L74,26 V86 L60,100 H20 L6,86 V26 Z"),
    "S": (64, "M58,12 H18 L6,24 V44 L18,56 H46 L58,68 V88 L46,100 H4"),
}


def wordmark_body(light=MIST, accent=FALCON, stroke=13):
    x, parts = 0, []
    for ch in "falkOSS":
        adv, d = GLYPHS[ch]
        color = accent if ch.isupper() else light
        parts.append(f'<path d="{d}" transform="translate({x} 0)" stroke="{color}"/>')
        x += adv + 6
    width = x - 6
    body = (f'<g fill="none" stroke-width="{stroke}" stroke-linecap="square" stroke-linejoin="miter">'
            + "".join(parts) + "</g>")
    return body, width


def wordmark(light=MIST, accent=FALCON):
    body, width = wordmark_body(light, accent)
    return svg(f"-8 0 {width + 16} 112", body)


def lockup(light=MIST, accent=FALCON, bg=None, bird=FALCON, water=LAKE):
    """Mark left, wordmark right – headers, documents."""
    body, width = wordmark_body(light, accent)
    w = 150 + width * 1.0 + 24
    back = f'<rect x="-24" y="-24" width="{w + 48}" height="208" rx="24" fill="{bg}"/>' if bg else ""
    return svg(f"-24 -24 {w + 48} 208", back
               + f'<g transform="translate(-30 -40) scale(0.2)">{mark(bird, water)}</g>'
               + f'<g transform="translate(184 26) scale(1.0)">{body}</g>')


def social():
    """1280×640: GitHub social preview, link previews – terminal style."""
    body, width = wordmark_body()
    mono = 'font-family="SF Mono, Menlo, Consolas, monospace"'
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="640" stroke="#151A20"/>' for x in range(0, 1281, 64)) + \
           "".join(f'<line x1="0" y1="{y}" x2="1280" y2="{y}" stroke="#151A20"/>' for y in range(0, 641, 64))
    return svg("0 0 1280 640", f'<rect width="1280" height="640" fill="{NIGHT}"/>{grid}'
               f'<g transform="translate(96 96) scale(0.44)">{mark()}</g>'
               f'<text x="560" y="196" {mono} font-size="26" fill="{REED}">$ whoami</text>'
               f'<g transform="translate(560 226) scale(1.3)">{body}</g>'
               f'<text x="562" y="420" {mono} font-size="28" fill="{MIST}">Falcon Lake Open Source Software</text>'
               f'<text x="562" y="466" {mono} font-size="24" fill="{REED}">// free software from Falkensee</text>'
               f'<rect x="562" y="492" width="16" height="30" fill="{FALCON}"/>')


def favicon_svg():
    """Transparent mark for browsers; follows light/dark mode."""
    style = (f'<style>.b{{fill:{FALCON}}}.w{{stroke:{LAKE}}}'
             f'@media (prefers-color-scheme: light){{.b{{fill:{FALCON_DARK}}}.w{{stroke:{LAKE_DARK}}}}}</style>')
    return svg("120 260 784 680", style
               + falcon(FALCON).replace(f'fill="{FALCON}"', 'class="b"')
               + f'<line class="w" x1="232" y1="830" x2="792" y2="830" stroke-width="70"/>')


# --- output ----------------------------------------------------------------------------------------------------------

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def render(src, dst, w, h=None):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    args = ["rsvg-convert", "-w", str(w)] + (["-h", str(h)] if h else []) + ["-o", dst, src]
    subprocess.run(args, check=True)


def ico(dst, pngs):
    """favicon.ico with PNG entries (16, 32, 48)."""
    data = [open(p, "rb").read() for p in pngs]
    sizes = [16, 32, 48]
    out = struct.pack("<HHH", 0, 1, len(data))
    offset = 6 + 16 * len(data)
    for s, d in zip(sizes, data):
        out += struct.pack("<BBBBHHII", s, s, 0, 0, 1, 32, len(d), offset)
        offset += len(d)
    with open(dst, "wb") as f:
        f.write(out + b"".join(data))


def main():
    for d in (SVG, PNG):
        if os.path.isdir(d):
            shutil.rmtree(d)   # generated output only
    files = {
        "falkoss-icon.svg": icon(),
        "falkoss-icon-square.svg": icon(rounded=False),
        "falkoss-icon-small.svg": small_icon(),
        "falkoss-mark-on-dark.svg": svg("120 260 784 680", mark()),
        "falkoss-mark-on-light.svg": svg("120 260 784 680", mark(FALCON_DARK, LAKE_DARK)),
        "falkoss-mark-black.svg": svg("120 260 784 680", mark("#000000", "#000000")),
        "falkoss-mark-white.svg": svg("120 260 784 680", mark("#FFFFFF", "#FFFFFF")),
        "falkoss-wordmark-on-dark.svg": wordmark(),
        "falkoss-wordmark-on-light.svg": wordmark(INK, FALCON_DARK),
        "falkoss-lockup-on-dark.svg": lockup(),
        "falkoss-lockup-on-light.svg": lockup(INK, FALCON_DARK, bird=FALCON_DARK, water=LAKE_DARK),
        "falkoss-social-1280x640.svg": social(),
        "favicon.svg": favicon_svg(),
    }
    for name, content in files.items():
        write(os.path.join(SVG, name), content)
    s = lambda n: os.path.join(SVG, n)
    for size in (64, 128, 256, 512, 1024):
        render(s("falkoss-icon.svg"), os.path.join(PNG, "icon", f"falkoss-icon-{size}.png"), size)
        render(s("falkoss-icon-square.svg"), os.path.join(PNG, "icon-square", f"falkoss-icon-square-{size}.png"), size)
    for size in (16, 32, 48):
        render(s("falkoss-icon-small.svg"), os.path.join(PNG, "icon-small", f"falkoss-icon-small-{size}.png"), size)
    for size in (256, 512, 1024):
        for v in ("on-dark", "on-light", "black", "white"):
            render(s(f"falkoss-mark-{v}.svg"), os.path.join(PNG, "mark", f"falkoss-mark-{v}-{size}.png"), size)
    for v in ("on-dark", "on-light"):
        render(s(f"falkoss-wordmark-{v}.svg"), os.path.join(PNG, "wordmark", f"falkoss-wordmark-{v}-1200.png"), 1200)
        render(s(f"falkoss-lockup-{v}.svg"), os.path.join(PNG, "lockup", f"falkoss-lockup-{v}-1200.png"), 1200)
    render(s("falkoss-icon-square.svg"), os.path.join(PNG, "social", "github-avatar-500.png"), 500)
    render(s("falkoss-social-1280x640.svg"), os.path.join(PNG, "social", "falkoss-social-1280x640.png"), 1280, 640)

    # Website head assets
    os.makedirs(SITE, exist_ok=True)
    shutil.copy(s("favicon.svg"), os.path.join(SITE, "favicon.svg"))
    shutil.copy(s("falkoss-lockup-on-dark.svg"), os.path.join(SITE, "falkoss-lockup-on-dark.svg"))
    shutil.copy(s("falkoss-mark-on-dark.svg"), os.path.join(SITE, "falkoss-mark.svg"))
    render(s("falkoss-icon-square.svg"), os.path.join(SITE, "apple-touch-icon.png"), 180)
    render(s("falkoss-icon.svg"), os.path.join(SITE, "icon-192.png"), 192)
    render(s("falkoss-icon.svg"), os.path.join(SITE, "icon-512.png"), 512)
    shutil.copy(os.path.join(PNG, "social", "falkoss-social-1280x640.png"), os.path.join(SITE, "social.png"))
    ico(os.path.join(SITE, "favicon.ico"),
        [os.path.join(PNG, "icon-small", f"falkoss-icon-small-{n}.png") for n in (16, 32, 48)])
    write(os.path.join(SITE, "site.webmanifest"),
          '{\n  "name": "falkOSS",\n  "short_name": "falkOSS",\n  "icons": [\n'
          '    {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},\n'
          '    {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}\n  ],\n'
          f'  "theme_color": "{NIGHT}",\n  "background_color": "{NIGHT}",\n  "display": "standalone"\n}}\n')
    print("brand kit written to", HERE, "and", SITE)


if __name__ == "__main__":
    main()
