"""Shared helpers for the coloring pages in this folder.

Every page is 140 x 200 mm (viewBox 560 x 800), black outlines only (#111, stroke 3),
white fills, every shape closed so it can be colored. See STYLE.md.

Usage in a page script:

    from lib import *
    begin("Judul", "Caption dari cerita.")
    ...draw the scene with rect/circle/path/poly/capsule/text/steam/scalloped/rotated...
    end("judul.svg")
"""
import math
import os
import random

W, H = 560, 800
INK, SW = "#111", 3
out = []


def add(s):
    out.append(s)


def style(fill="#fff", sw=SW):
    return f'fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'


def rect(x, y, w, h, r=0, fill="#fff"):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" {style(fill)}/>')


def circle(x, y, r, fill="#fff"):
    add(f'<circle cx="{x}" cy="{y}" r="{r}" {style(fill)}/>')


def path(d, fill="none"):
    add(f'<path d="{d}" {style(fill)}/>')


def line(x1, y1, x2, y2):
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {style("none")}/>')


def poly(pts, fill="#fff"):
    add(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" {style(fill)}/>')


def capsule(x1, y1, x2, y2, w):
    """Outlined thick line: black stroke underneath, white stroke on top."""
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/>')
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="{w - 2 * SW}" stroke-linecap="round"/>')


def text(x, y, s, size, weight="normal", italic=False, outline=False):
    st = ' font-style="italic"' if italic else ""
    if outline:
        add(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Georgia, serif" font-size="{size}" '
            f'font-weight="{weight}"{st} fill="#fff" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round">{s}</text>')
    else:
        add(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Georgia, serif" font-size="{size}" '
            f'font-weight="{weight}"{st} fill="{INK}">{s}</text>')


def steam(x, y, h, amp=6, waves=2):
    pts = []
    for i in range(0, 41):
        t = i / 40
        pts.append(f"{x + amp * math.sin(t * waves * 2 * math.pi):.1f},{y - h * t:.1f}")
    add(f'<polyline points="{" ".join(pts)}" {style("none", 2.5)}/>')


def scalloped(cx, cy, R, n=9, a=0.09):
    pts = []
    for i in range(0, 121):
        t = i / 120 * 2 * math.pi
        r = R * (1 + a * math.sin(n * t))
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    poly(pts)


def rotated(cx, cy, deg, fn):
    add(f'<g transform="rotate({deg} {cx} {cy})">')
    fn()
    add("</g>")




def border(seed=3):
    """Circuit-board border used on every page (two rounded traces with random links)."""
    random.seed(seed)
    for inset in (24, 46):
        rect(inset, inset, W - 2 * inset, H - 2 * inset, r=22, fill="none")

    def link_h(x):
        for y in (24, H - 24):
            yy = y + (22 if y < 100 else -22)
            line(x, y, x, yy)
            circle(x, y, 5)
            circle(x, yy, 5)

    def link_v(y):
        for x in (24, W - 24):
            xx = x + (22 if x < 100 else -22)
            line(x, y, xx, y)
            circle(x, y, 5)
            circle(xx, y, 5)

    for x in range(70, W - 60, 40):
        if random.random() < 0.55:
            link_h(x)
    for y in range(70, H - 60, 40):
        if random.random() < 0.55:
            link_v(y)


def begin(title, caption, seed=3, title_size=54):
    """Start a page: white background, border, outlined title, subtitle. Caption is drawn by end()."""
    out.clear()
    add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="140mm" height="200mm">')
    add(f'<rect width="{W}" height="{H}" fill="#fff"/>')
    border(seed)
    text(W / 2, 124, title, title_size, "bold", outline=True)
    text(W / 2, 150, "Warnai halamannya!", 16, italic=True)
    _state["caption"] = caption


_state = {}


def end(filename):
    """Finish the page with the caption at the bottom and write the SVG next to this file."""
    text(W / 2, 736, _state.get("caption", ""), 16, italic=True)
    add("</svg>")
    path_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(path_out, "w") as f:
        f.write("\n".join(out))
    print("wrote", filename)
