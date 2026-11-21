#!/usr/bin/env python3
"""Coloring page for the story "Bangun Sahur", drawn with lib.py geometry (no image model).

Run:  python3 bangun-sahur.py   ->  bangun-sahur.svg
"""
import math

from lib import *

# ---------------------------------------------------------------- characters
# Same geometry on every page (strawberry, waktu-layar, bangun-sahur, balap-karung).
# Each function takes the head centre (x, y); the body hangs below it.


def ellipse(cx, cy, rx, ry, fill="#fff", sw=SW):
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" {style(fill, sw)}/>')


def arm(x1, y1, x2, y2, w=26, hand=11):
    """Sleeve as an outlined capsule with a round hand at the end."""
    capsule(x1, y1, x2, y2, w)
    circle(x2, y2, hand)


def mouth(x, y, kind):
    if kind == "smile":
        path(f"M{x-12},{y-3} Q{x},{y+9} {x+12},{y-3}")
    elif kind == "grin":
        path(f"M{x-14},{y-4} Q{x},{y+14} {x+14},{y-4} Z", fill="#fff")
    elif kind == "oh":
        ellipse(x, y + 5, 7, 8)
    elif kind == "flat":
        line(x - 9, y, x + 9, y)
    elif kind == "wave":
        path(f"M{x-12},{y} Q{x-6},{y-5} {x},{y} Q{x+6},{y+5} {x+12},{y}")


def eyes(x, y, dx, kind, r=7):
    for s in (-1, 1):
        ex = x + s * dx
        if kind == "open":
            circle(ex, y, r)
            circle(ex, y + 1, 3, fill=INK)
        elif kind == "wide":
            circle(ex, y, r + 4)
            circle(ex, y, 3.5, fill=INK)
        elif kind == "kind":
            path(f"M{ex-8},{y+2} Q{ex},{y-7} {ex+8},{y+2}")
        elif kind == "closed":
            path(f"M{ex-8},{y-1} Q{ex},{y+6} {ex+8},{y-1}")
        elif kind == "side":   # looking to the right
            circle(ex, y, r)
            circle(ex + 3, y + 1, 3, fill=INK)


def batik(cx, cy):
    """One batik motif: a diamond with a dot inside (two closed regions)."""
    poly([(cx, cy - 9), (cx + 8, cy), (cx, cy + 9), (cx - 8, cy)])
    circle(cx, cy, 2.5)


def darmo_head(x, y, face="open", mo="flat"):
    """Pak Darmo: older man, peci, grey side hair, thin mustache."""
    circle(x - 46, y + 4, 10)
    circle(x + 46, y + 4, 10)
    circle(x, y, 46)
    for s in (-1, 1):   # grey hair under the peci
        path(f"M{x+s*44},{y+6} Q{x+s*52},{y-10} {x+s*42},{y-22} L{x+s*32},{y-20} Q{x+s*38},{y-6} {x+s*44},{y+6} Z", fill="#fff")
    # peci (cap) with its oval top
    path(f"M{x-42},{y-20} L{x-39},{y-56} Q{x},{y-64} {x+39},{y-56} L{x+42},{y-20} Q{x},{y-28} {x-42},{y-20} Z", fill="#fff")
    path(f"M{x-39},{y-56} Q{x},{y-48} {x+39},{y-56}")
    # brows, wrinkles
    path(f"M{x-27},{y-10} Q{x-17},{y-15} {x-8},{y-10}")
    path(f"M{x+27},{y-10} Q{x+17},{y-15} {x+8},{y-10}")
    eyes(x, y + 2, 17, face)
    path(f"M{x},{y+6} Q{x-7},{y+18} {x+3},{y+19}")
    # thin mustache
    path(f"M{x-21},{y+29} Q{x-10},{y+21} {x},{y+25} Q{x+10},{y+21} {x+21},{y+29} "
         f"Q{x+10},{y+27} {x},{y+29} Q{x-10},{y+27} {x-21},{y+29} Z", fill="#fff")
    mouth(x, y + 36, mo)


def darmo_shirt(x, y):
    """Batik shirt, from the neck (head centre y) down to y+178."""
    rect(x - 12, y + 38, 24, 16)
    path(f"M{x-58},{y+178} L{x-58},{y+74} Q{x-58},{y+50} {x-30},{y+50} L{x+30},{y+50} "
         f"Q{x+58},{y+50} {x+58},{y+74} L{x+58},{y+178} Z", fill="#fff")
    poly([(x - 24, y + 50), (x, y + 84), (x - 6, y + 92), (x - 30, y + 60)])   # collar
    poly([(x + 24, y + 50), (x, y + 84), (x + 6, y + 92), (x + 30, y + 60)])
    line(x, y + 84, x, y + 178)
    for by in (108, 136, 162):
        circle(x, y + by, 3)
    for bx in (-41, -20, 20, 41):
        for by in (100, 130, 160):
            if abs(bx) == 20 and by == 100:
                continue
            batik(x + bx, y + by)


def darmo(x, y, face="open", mo="flat", legs=True):
    """Standing Pak Darmo: feet at about y+312. Arms are drawn by the scene.
    legs=False draws only the head and shirt (for when he sits in bed)."""
    if legs:
        ellipse(x - 24, y + 306, 20, 9)
        ellipse(x + 24, y + 306, 20, 9)
        # sarong with a plaid of closed cells
        path(f"M{x-54},{y+176} L{x-50},{y+302} L{x+50},{y+302} L{x+54},{y+176} Z", fill="#fff")
        for vx in (-26, 0, 26):
            line(x + vx, y + 188, x + vx, y + 302)
        for hy in (222, 262):
            line(x - 52, y + hy, x + 52, y + hy)
    darmo_shirt(x, y)
    if legs:
        rect(x - 56, y + 170, 112, 18, r=4)   # sarong fold over the shirt hem
    darmo_head(x, y, face, mo)


def ratna_head(x, y, face="kind", mo="smile"):
    """Bu Ratna: hijab framing a round face. Cape reaches y+104."""
    path(f"M{x-54},{y} A54,54 0 0 1 {x+54},{y} L{x+74},{y+96} Q{x},{y+116} {x-74},{y+96} Z", fill="#fff")
    ellipse(x, y + 8, 36, 42)
    path(f"M{x-36},{y-4} Q{x},{y-44} {x+36},{y-4}")   # hijab edge over the forehead
    eyes(x, y + 8, 14, face, r=6)
    circle(x - 23, y + 24, 5)   # cheeks
    circle(x + 23, y + 24, 5)
    path(f"M{x},{y+12} Q{x-4},{y+22} {x+2},{y+23}")
    mouth(x, y + 34, mo)


def ratna_body(x, y, legs=True):
    """Long blouse and skirt, feet at about y+306."""
    if legs:
        ellipse(x - 20, y + 302, 18, 8)
        ellipse(x + 20, y + 302, 18, 8)
    path(f"M{x-46},{y+238} L{x-42},{y+298} L{x+42},{y+298} L{x+46},{y+238} Z", fill="#fff")
    path(f"M{x-50},{y+80} L{x-64},{y+238} Q{x},{y+250} {x+64},{y+238} L{x+50},{y+80} Z", fill="#fff")
    for by in (128, 160, 192, 222):
        circle(x, y + by, 4)


def ratna(x, y, face="kind", mo="smile", arms=(), legs=True):
    ratna_body(x, y, legs)
    for a in arms:
        arm(*a)
    ratna_head(x, y, face, mo)


def bima_head(x, y, face="open", mo="smile"):
    """Bima: small boy, short spiky fringe, big eyes."""
    circle(x - 36, y + 4, 8)
    circle(x + 36, y + 4, 8)
    circle(x, y, 36)
    pts = []
    for i in range(0, 25):   # hair cap following the top of the head
        a = math.pi + i / 24 * math.pi
        pts.append((x + 38 * math.cos(a), y - 4 + 38 * math.sin(a)))
    for i in range(0, 9):    # spiky fringe back across the forehead
        fx = x + 37 - i * 74 / 8
        pts.append((fx, y - 12 if i % 2 == 0 else y - 24))
    poly(pts)
    for s in (-1, 1):
        ex = x + s * 14
        if face == "closed":
            path(f"M{ex-8},{y+2} Q{ex},{y+9} {ex+8},{y+2}")
        elif face == "down":
            circle(ex, y + 4, 9)
            circle(ex, y + 8, 4, fill=INK)
        else:
            circle(ex, y + 4, 10)
            circle(ex + (2 if face == "side" else 0), y + 5, 4.5, fill=INK)
            circle(ex + (2 if face == "side" else 0) - 2, y + 2, 1.5)
    mouth(x, y + 22, mo)


def bima_shirt(x, y):
    """SD uniform shirt with collar, pocket and small tie, from y+34 to y+112."""
    path(f"M{x-34},{y+112} L{x-34},{y+50} Q{x-34},{y+36} {x-20},{y+36} L{x+20},{y+36} "
         f"Q{x+34},{y+36} {x+34},{y+50} L{x+34},{y+112} Z", fill="#fff")
    poly([(x - 16, y + 36), (x, y + 50), (x - 12, y + 56)])
    poly([(x + 16, y + 36), (x, y + 50), (x + 12, y + 56)])
    poly([(x - 4, y + 50), (x + 4, y + 50), (x + 6, y + 74), (x, y + 80), (x - 6, y + 74)])
    rect(x + 12, y + 68, 14, 14, r=2)


def bima(x, y, face="open", mo="smile", legs=True):
    """Standing Bima: shorts, legs, shoes at about y+196."""
    if legs:
        capsule(x - 14, y + 140, x - 14, y + 184, 18)
        capsule(x + 14, y + 140, x + 14, y + 184, 18)
        ellipse(x - 16, y + 192, 15, 8)
        ellipse(x + 16, y + 192, 15, 8)
    rect(x - 34, y + 106, 68, 40, r=4)   # shorts
    line(x, y + 120, x, y + 146)
    bima_shirt(x, y)
    bima_head(x, y, face, mo)


def siti_face(x, y, w, h, mo="zigzag"):
    """SITI on any screen: square eyes, round cheeks, zigzag or smile mouth."""
    rect(x - 0.3 * w - 8, y - 0.18 * h - 8, 16, 16, r=3)
    rect(x + 0.3 * w - 8, y - 0.18 * h - 8, 16, 16, r=3)
    my = y + 0.2 * h
    if mo == "zigzag":
        pts = " ".join(f"L{x - 26 + i * 52 / 6:.1f},{my + (0 if i % 2 == 0 else -7)}" for i in range(7))
        path("M" + pts[1:])
    else:
        path(f"M{x-18},{my-5} Q{x},{my+9} {x+18},{my-5}")
    circle(x - 0.4 * w, y + 0.05 * h, 5, fill="none")
    circle(x + 0.4 * w, y + 0.05 * h, 5, fill="none")


def bubble(x1, y1, x2, y2, tx, ty, lines, size=15):
    """Rounded speech bubble (one closed path) with a tail pointing to (tx, ty)."""
    r = 14
    mx = min(max(tx, x1 + 30), x2 - 30)
    if ty > y2:
        d = (f"M{x1},{y1+r} Q{x1},{y1} {x1+r},{y1} L{x2-r},{y1} Q{x2},{y1} {x2},{y1+r} L{x2},{y2-r} "
             f"Q{x2},{y2} {x2-r},{y2} L{mx+10},{y2} L{tx},{ty} L{mx-10},{y2} L{x1+r},{y2} Q{x1},{y2} {x1},{y2-r} Z")
    else:
        d = (f"M{x1},{y1+r} Q{x1},{y1} {x1+r},{y1} L{mx-10},{y1} L{tx},{ty} L{mx+10},{y1} L{x2-r},{y1} "
             f"Q{x2},{y1} {x2},{y1+r} L{x2},{y2-r} Q{x2},{y2} {x2-r},{y2} L{x1+r},{y2} Q{x1},{y2} {x1},{y2-r} Z")
    path(d, fill="#fff")
    n = len(lines)
    cy = (y1 + y2) / 2 - (n - 1) * size * 0.6 + size * 0.35
    for i, s in enumerate(lines):
        text((x1 + x2) / 2, cy + i * size * 1.2, s, size, "bold")


# ---------------------------------------------------------------- page
def star(cx, cy, R, r=None):
    r = r or R * 0.45
    poly([(cx + (R if k % 2 == 0 else r) * math.sin(k * math.pi / 5),
           cy - (R if k % 2 == 0 else r) * math.cos(k * math.pi / 5)) for k in range(10)])


def clock(cx, cy, r, h, m):
    circle(cx, cy, r)
    circle(cx, cy, r - 7, fill="none")
    for k in range(12):
        a = k * math.pi / 6
        line(cx + (r - 12) * math.sin(a), cy - (r - 12) * math.cos(a), cx + (r - 7) * math.sin(a), cy - (r - 7) * math.cos(a))
    ha, ma = math.radians((h + m / 60) * 30), math.radians(m * 6)
    line(cx, cy, cx + 0.45 * r * math.sin(ha), cy - 0.45 * r * math.cos(ha))
    line(cx, cy, cx + 0.7 * r * math.sin(ma), cy - 0.7 * r * math.cos(ma))
    circle(cx, cy, 3, fill=INK)


begin("Bangun Sahur", "Panci gagal, notifikasi transfer berhasil.")

line(62, 702, 498, 702)   # floor

# night window: crescent moon and stars
rect(226, 180, 170, 130, r=6)
rect(236, 190, 150, 110, r=3)
line(311, 190, 311, 300)
line(236, 245, 386, 245)
path("M268,200 A26,26 0 1 0 296,236 A20,20 0 1 1 268,200 Z", fill="#fff")
star(352, 214, 11)
star(338, 270, 8)
star(368, 280, 7)
star(256, 276, 7)
clock(450, 238, 36, 3, 0)

# bed: headboard, pillow, Pak Darmo bolt upright, blanket
rect(222, 452, 178, 120, r=18)
for k in range(3):
    circle(262 + k * 49, 476, 9)
ellipse(311, 500, 70, 20)
darmo(311, 410, face="wide", mo="oh", legs=False)
for (x1, y1, x2, y2) in [(311, 334, 311, 318), (282, 340, 272, 326), (340, 340, 350, 326)]:
    line(x1, y1, x2, y2)   # startle marks
arm(260, 472, 250, 556)
path("M214,566 Q262,548 311,562 Q360,548 408,566 L408,640 L214,640 Z", fill="#fff")   # blanket
path("M226,596 Q311,612 396,596")
rect(214, 640, 194, 26, r=4)   # bed frame
rect(222, 666, 16, 36)
rect(384, 666, 16, 36)
arm(362, 472, 432, 532)   # reaching for the phone

# nightstand with the phone
rect(414, 580, 80, 122, r=4)
rect(424, 596, 60, 40, r=4)
circle(454, 616, 4)
rect(434, 506, 44, 74, r=8)
rect(439, 514, 34, 52, r=3)
text(456, 545, "Rp", 12, "bold")
circle(432, 532, 11)
for (x1, y1, x2, y2) in [(422, 498, 414, 488), (456, 494, 456, 482), (490, 498, 498, 488)]:
    line(x1, y1, x2, y2)   # ring marks
bubble(386, 342, 494, 444, 456, 482, ["Ting!", "Transfer", "masuk"], size=16)

# Bu Ratna, amused, still holding the pot that did not work
ratna(136, 380, face="kind", mo="grin")
rotated(150, 512, 20, lambda: rect(144, 482, 12, 50, r=6))   # spoon in the pot
rect(102, 532, 68, 46, r=6)   # pot
rect(96, 524, 80, 12, r=6)
capsule(90, 486, 94, 538, 24)
capsule(182, 486, 178, 538, 24)
circle(94, 540, 11)
circle(178, 540, 11)
bubble(70, 190, 206, 246, 120, 330, ["Ampuh juga..."], size=15)

end("bangun-sahur.svg")
