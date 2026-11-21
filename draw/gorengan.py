#!/usr/bin/env python3
"""Coloring page for the story "Gorengan", drawn with plain geometry (no image model).

Page: 140 x 200 mm (viewBox 560 x 800). Every shape is a closed outline so it can be colored.
Math used: rose curve (poster), scalloped circle r(t)=R(1+a*sin(nt)) (bakwan),
sine waves (steam), seeded random walk of traces (circuit border).

Run:  python3 gorengan.py   ->  gorengan.svg
"""
import math
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


# ---------------------------------------------------------------- page
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="140mm" height="200mm">')
add(f'<rect width="{W}" height="{H}" fill="#fff"/>')

# ---- circuit-board border: two rounded traces joined by random links and pads
random.seed(3)
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

# ---- title
text(W / 2, 124, "Gorengan", 54, "bold", outline=True)
text(W / 2, 150, "Warnai halamannya!", 16, italic=True)

# ---- scene (shifted up so the caption fits under the floor)
add('<g transform="translate(0,-30)">')

# floor
line(62, 740, 498, 740)

# wall clock showing 11.07
cx, cy = 115, 255
circle(cx, cy, 38)
circle(cx, cy, 31, fill="none")
for k in range(12):
    a = k * math.pi / 6
    line(cx + 26 * math.sin(a), cy - 26 * math.cos(a), cx + 31 * math.sin(a), cy - 31 * math.cos(a))
h_ang = math.radians((11 + 7 / 60) * 30)
m_ang = math.radians(7 * 6)
line(cx, cy, cx + 17 * math.sin(h_ang), cy - 17 * math.cos(h_ang))
line(cx, cy, cx + 26 * math.sin(m_ang), cy - 26 * math.cos(m_ang))
circle(cx, cy, 3, fill=INK)

# poster: rose curve r = 40 cos(5t)
px, py = 440, 260
rect(px - 52, py - 64, 104, 128, r=6)
circle(px, py, 46, fill="none")
pts = []
for i in range(0, 361):
    t = i / 360 * math.pi
    r = 40 * math.cos(5 * t)
    pts.append((px + r * math.cos(t), py + r * math.sin(t)))
poly(pts)
circle(px, py, 5)

# body (behind table)
path("M150,600 L150,500 Q150,440 230,440 Q310,440 310,500 L310,600 Z", fill="#fff")
rect(215, 420, 30, 30)                                   # neck
poly([(205, 440), (230, 482), (255, 440)])               # shirt collar
poly([(222, 482), (238, 482), (234, 494), (226, 494)])   # tie knot
poly([(226, 494), (234, 494), (241, 516), (230, 530), (219, 516)])  # tie
path("M175,452 L205,440 M285,452 L255,440")              # lapels
circle(197, 540, 4)
circle(263, 540, 4)

# head
circle(170, 372, 12)
circle(290, 372, 12)
circle(230, 370, 60)
path("M178,345 Q190,300 230,308 Q270,300 282,345 Q262,322 230,330 Q198,322 178,345 Z", fill="#fff")  # hair
circle(208, 368, 14)
circle(252, 368, 14)
line(222, 368, 238, 368)
circle(208, 370, 3.5, fill=INK)
circle(252, 370, 3.5, fill=INK)
line(196, 346, 218, 350)
line(264, 346, 242, 350)
path("M230,376 Q223,388 232,390")                        # nose
path("M205,402 Q218,388 230,398 Q242,388 255,402 Q242,408 230,404 Q218,408 205,402 Z", fill="#fff")  # mustache
add(f'<ellipse cx="230" cy="418" rx="9" ry="7" {style()}/>')  # mouth: "oh"
path("M292,318 Q283,334 292,342 Q301,334 292,318 Z", fill="#fff")  # nervous sweat drop

# arm holding a gorengan (left)
capsule(160, 490, 118, 440, 32)
rotated(113, 395, 15, lambda: rect(100, 365, 26, 62, r=13))   # pisang goreng
circle(113, 436, 17)
steam(108, 360, 40)
steam(122, 360, 30, waves=1.5)

# table
rect(70, 590, 420, 28, r=6)
rect(95, 618, 22, 92)
rect(443, 618, 22, 92)

# plate with gorengan
add(f'<ellipse cx="230" cy="590" rx="70" ry="13" {style()}/>')
scalloped(200, 568, 22)
scalloped(262, 568, 22, n=11)
poly([(216, 562), (244, 562), (230, 542)])               # tempe
rotated(230, 585, -8, lambda: rect(204, 573, 56, 20, r=10))

# SITI on the monitor
rect(400, 480, 100, 90, r=8)
rect(408, 488, 84, 74, r=4)
poly([(440, 570), (460, 570), (466, 590), (434, 590)])
line(450, 480, 450, 462)
circle(450, 458, 5)
rect(420, 508, 16, 16, r=3)
rect(464, 508, 16, 16, r=3)
path("M424,545 L433,538 L442,545 L451,538 L460,545 L469,538 L476,545")
circle(418, 534, 5, fill="none")
circle(482, 534, 5, fill="none")

# speech bubble from SITI
path("M404,356 Q404,342 418,342 L488,342 Q502,342 502,356 L502,396 Q502,410 488,410 L462,410 "
     "L452,448 L440,410 L418,410 Q404,410 404,396 Z", fill="#fff")
text(453, 370, "Anda", 15, "bold")
text(453, 390, "kesiangan.", 15, "bold")

# arm holding the phone (right)
capsule(300, 490, 345, 452, 32)
rect(321, 345, 62, 104, r=10)
rect(327, 355, 50, 74, r=4)
text(352, 376, "11.07", 13, "bold")
rect(334, 398, 36, 20, r=8)
text(352, 412, "Hadir", 11)
circle(352, 444, 17)

add("</g>")

# ---- caption
text(W / 2, 736, "Rapat jam sembilan, mulai jam sebelas.", 16, italic=True)

add("</svg>")

with open(__file__.replace("gorengan.py", "gorengan.svg"), "w") as f:
    f.write("\n".join(out))
print("wrote gorengan.svg")
