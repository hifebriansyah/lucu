#!/usr/bin/env python3
"""Coloring page for the story "Balap Karung", drawn with lib.py geometry (no image model).

Run:  python3 balap-karung.py   ->  balap-karung.svg
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
def sack(cx, top, bottom, w):
    """Burlap sack: slightly flared body with a tied, frilled top edge."""
    path(f"M{cx-w/2+4},{top} L{cx-w/2},{bottom-8} Q{cx-w/2},{bottom} {cx-w/2+8},{bottom} "
         f"L{cx+w/2-8},{bottom} Q{cx+w/2},{bottom} {cx+w/2},{bottom-8} L{cx+w/2-4},{top} Z", fill="#fff")
    pts = []
    for i in range(0, 13):
        u = i / 12
        pts.append((cx - w / 2 + 2 + u * (w - 4), top - 6 + (5 if i % 2 else 0)))
    pts += [(cx + w / 2 - 2, top + 8), (cx - w / 2 + 2, top + 8)]
    poly(pts)


def racer(x, ground, hop, hair):
    """Small background racer mid-hop: sack, arms up, a head with its own hair."""
    b = ground - hop
    for k in range(3):   # motion lines behind
        line(x - 30 - 6 * k, b - 10 - 10 * k, x - 20 - 6 * k, b - 10 - 10 * k)
    if hop:
        ellipse(x, ground, 14, 3, sw=2)   # shadow on the road
    capsule(x - 10, b - 44, x - 22, b - 66, 9)
    capsule(x + 10, b - 44, x + 22, b - 66, 9)
    rect(x - 12, b - 50, 24, 16, r=5)   # shirt above the sack
    sack(x, b - 36, b, 34)
    if hair == "hood":   # Dimas: hoodie hood behind a messy fringe
        circle(x, b - 62, 15)
    circle(x, b - 62, 11)
    if hair == "spiky":  # Raka: tall spiky hair
        poly([(x - 11, b - 64), (x - 9, b - 84), (x - 3, b - 72), (x + 2, b - 88), (x + 6, b - 72), (x + 12, b - 82), (x + 11, b - 64)])
    elif hair == "hood":
        poly([(x - 10, b - 64), (x - 6, b - 74), (x - 1, b - 67), (x + 4, b - 75), (x + 10, b - 64)])
    circle(x - 4, b - 61, 1.6, fill=INK)
    circle(x + 4, b - 61, 1.6, fill=INK)


def bunting(y0, sag):
    pts = [(62 + i * 436 / 40, y0 + sag * math.sin(math.pi * i / 40)) for i in range(41)]
    add(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" {style("none")}/>')
    for k in range(1, 12):
        t = k / 12
        x = 62 + 436 * t
        y = y0 + sag * math.sin(math.pi * t)
        poly([(x - 14, y), (x + 14, y), (x, y + 26)])


def trophy(cx, top):
    path(f"M{cx-26},{top} L{cx+26},{top} Q{cx+26},{top+44} {cx},{top+50} Q{cx-26},{top+44} {cx-26},{top} Z", fill="#fff")
    path(f"M{cx-24},{top+8} Q{cx-44},{top+10} {cx-38},{top+24} Q{cx-34},{top+32} {cx-20},{top+30} "
         f"L{cx-20},{top+25} Q{cx-30},{top+26} {cx-32},{top+21} Q{cx-34},{top+14} {cx-24},{top+15} Z", fill="#fff")
    path(f"M{cx+24},{top+8} Q{cx+44},{top+10} {cx+38},{top+24} Q{cx+34},{top+32} {cx+20},{top+30} "
         f"L{cx+20},{top+25} Q{cx+30},{top+26} {cx+32},{top+21} Q{cx+34},{top+14} {cx+24},{top+15} Z", fill="#fff")
    text(cx, top + 32, "1", 22, "bold")
    rect(cx - 6, top + 50, 12, 14)
    rect(cx - 20, top + 64, 40, 12, r=3)


begin("Balap Karung", "Juara satu tanpa meninggalkan garis start.")

bunting(180, 30)

# flag on a pole (two bands to color red and white)
rect(280, 232, 8, 252, r=3)
circle(284, 228, 6)
rect(288, 238, 62, 20)
rect(288, 258, 62, 20)

# road and finish line far away
line(62, 484, 498, 484)
rect(442, 330, 8, 154, r=3)
rect(488, 330, 8, 154, r=3)
rect(436, 300, 62, 30, r=4)
text(467, 322, "FINIS", 15, "bold")

# racers mid-hop, small in the background
rotated(318, 466, 80, lambda: sack(318, 448, 486, 32))   # a racer who fell over
circle(352, 472, 11)
circle(354, 468, 1.6, fill=INK)
racer(398, 484, 22, "spiky")   # Raka
racer(469, 484, 30, "hood")    # Dimas, first over the line

# Pak Darmo, still at the start line in his sack, holding the trophy up
darmo(140, 384, face="kind", mo="grin", legs=False)
sack(140, 548, 694, 124)
rect(104, 606, 72, 34, r=4)   # printed label on the sack
text(140, 629, "BERAS", 15, "bold")
arm(88, 446, 76, 528)
arm(192, 446, 226, 364)
trophy(226, 286)
for (x1, y1, x2, y2) in [(176, 300, 166, 290), (276, 300, 286, 290), (226, 272, 226, 260)]:
    line(x1, y1, x2, y2)   # shine marks

# start line and sign
for i in range(12):
    rect(62 + i * 20, 694, 20, 10)
rect(270, 652, 8, 42, r=3)
rect(236, 616, 76, 36, r=6)
text(274, 640, "START", 16, "bold")

# SITI judging on a tripod
line(426, 650, 396, 702)
line(426, 650, 456, 702)
line(426, 650, 426, 702)
rect(380, 590, 92, 64, r=8)
rect(387, 597, 78, 50, r=4)
line(426, 590, 426, 576)
circle(426, 572, 5)
siti_face(426, 622, 78, 50, mo="smile")
bubble(330, 498, 494, 560, 426, 566, ["Juara 1:", "Pak Darmo!"], size=16)

end("balap-karung.svg")
