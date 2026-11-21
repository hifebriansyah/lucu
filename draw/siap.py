#!/usr/bin/env python3
"""Coloring page for the story "Siap!" (ai/33.md), drawn with plain geometry.

Dimas sleeps after lembur, his phone on the pillow keeps answering "Siap!" in the
RT WhatsApp group, and through the window Nadia, her parents and the whole RT are
already at the door.

This file also holds the shared character geometry (Dimas, Nadia, Pak Darmo,
generic neighbours) and small helpers, so uang-rokok.py and hari-baik.py import
them from here and every page draws the characters the same way.

Run:  python3 siap.py   ->  siap.svg
"""
import math

from lib import *

# ================================================================ shared helpers


def place(x, y, s, fn, rot=0):
    """Draw fn() in local coordinates, moved to (x, y), rotated, scaled by s."""
    add(f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">')
    fn()
    add("</g>")


def ellipse(cx, cy, rx, ry, rot=0, fill="#fff", sw=SW):
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" {style(fill, sw)}/>')


def bubble(x, y, w, h, tx, ty, r=14):
    """Rounded speech bubble with a tail from its bottom edge to the tip (tx, ty)."""
    bx = min(max(tx, x + r + 10), x + w - r - 10)
    if ty < y:  # tail on the top edge
        path(f"M{x + r},{y} L{bx - 8},{y} L{tx},{ty} L{bx + 8},{y} L{x + w - r},{y} Q{x + w},{y} {x + w},{y + r} "
             f"L{x + w},{y + h - r} Q{x + w},{y + h} {x + w - r},{y + h} L{x + r},{y + h} "
             f"Q{x},{y + h} {x},{y + h - r} L{x},{y + r} Q{x},{y} {x + r},{y} Z", fill="#fff")
    else:
        path(f"M{x + r},{y} L{x + w - r},{y} Q{x + w},{y} {x + w},{y + r} L{x + w},{y + h - r} "
             f"Q{x + w},{y + h} {x + w - r},{y + h} L{bx + 8},{y + h} L{tx},{ty} L{bx - 8},{y + h} "
             f"L{x + r},{y + h} Q{x},{y + h} {x},{y + h - r} L{x},{y + r} Q{x},{y} {x + r},{y} Z", fill="#fff")


def torso(half=78, top=52, bottom=160):
    path(f"M{-half},{bottom} L{-half},{top + 44} Q{-half},{top} 0,{top} Q{half},{top} {half},{top + 44} "
         f"L{half},{bottom} Z", fill="#fff")


def eye(x, y, kind="open"):
    if kind == "open":
        circle(x, y, 7)
        circle(x, y + 1, 3, fill=INK)
    elif kind == "wide":
        circle(x, y, 9)
        circle(x, y, 2.5, fill=INK)
    elif kind == "shut":
        path(f"M{x - 8},{y} Q{x},{y + 6} {x + 8},{y}")
    elif kind == "happy":
        path(f"M{x - 8},{y + 2} Q{x},{y - 7} {x + 8},{y + 2}")


# ================================================================ characters
# All characters use local coordinates with the head centre at (0, 0);
# the body goes down to y = 160 (bust) or the feet at y ~ 270 (full).


def dimas_hair():
    pts = []
    n = 12
    for i in range(n + 1):
        a = math.radians(188 - i * 196 / n)
        r = 60 if i % 2 else 46
        pts.append((r * math.cos(a), -r * math.sin(a)))
    for i in range(9):                                     # ragged fringe, right to left
        pts.append((42 - i * 84 / 8, -12 if i % 2 else -24))
    poly(pts)


def dimas_head(eyes="open", mouth="flat"):
    circle(-44, 6, 9)
    circle(44, 6, 9)
    circle(0, 0, 44)
    dimas_hair()
    eye(-17, 4, eyes)
    eye(17, 4, eyes)
    for sx in (-1, 1):                                     # bags under the eyes
        path(f"M{sx * 27},{16} Q{sx * 17},{23} {sx * 7},{16}")
    path("M0,10 Q-6,20 3,21")
    if mouth == "flat":
        path("M-10,31 Q0,34 10,31")
    elif mouth == "o":
        ellipse(0, 32, 7, 8)
    elif mouth == "sleep":
        ellipse(4, 32, 5, 4)
    elif mouth == "smile":
        path("M-14,27 Q0,42 14,27 Z", fill="#fff")


def dimas(eyes="open", mouth="flat", full=False):
    """Messy spiky hair, hoodie with hood and drawstrings, bags under the eyes."""
    if full:
        rect(-52, 150, 46, 108, r=6)                       # jeans
        rect(6, 150, 46, 108, r=6)
        ellipse(-32, 262, 28, 10)                          # sneakers
        ellipse(32, 262, 28, 10)
    torso(80)
    path("M-44,160 L-36,122 L36,122 L44,160", fill="#fff")    # kangaroo pocket
    path("M-54,20 Q-72,74 -20,72 L20,72 Q72,74 54,20 Z", fill="#fff")  # hood
    dimas_head(eyes, mouth)
    for sx in (-1, 1):                                     # drawstrings
        line(sx * 12, 72, sx * 14, 104)
        circle(sx * 14, 108, 4)


def nadia(eyes="open", mouth="smile", full=False):
    """Long straight hair, cardigan over a plain top."""
    path("M-50,0 Q-56,-60 0,-58 Q56,-60 50,0 L58,92 L-58,92 Z", fill="#fff")  # hair behind
    if full:
        poly([(-56, 150), (56, 150), (66, 252), (-66, 252)])   # skirt
        ellipse(-24, 258, 20, 8)
        ellipse(24, 258, 20, 8)
    torso(72)
    poly([(-22, 54), (22, 54), (14, 160), (-14, 160)])     # top under the open cardigan
    circle(-26, 100, 3.5)
    circle(-24, 132, 3.5)
    rect(32, 120, 22, 20, r=3)                             # cardigan pocket
    rect(-12, 30, 24, 26)                                  # neck
    circle(0, 0, 40)
    for sx in (-1, 1):                                     # straight strands over the shoulders
        poly([(sx * 47, -8), (sx * 35, -4), (sx * 31, 96), (sx * 51, 96)])
    path("M-42,-6 Q-44,-50 0,-50 Q44,-50 42,-6 Q34,-26 10,-22 Q-20,-30 -42,-6 Z", fill="#fff")  # fringe
    eye(-15, 4, eyes)
    eye(15, 4, eyes)
    if eyes in ("open", "wide"):
        for sx in (-1, 1):
            line(sx * 21, -2, sx * 25, -6)
    ellipse(-25, 21, 4.5, 2.8, sw=2)
    ellipse(25, 21, 4.5, 2.8, sw=2)
    path("M0,10 Q-4,17 2,18")
    if mouth == "smile":
        path("M-11,25 Q0,36 11,25 Z", fill="#fff")
    elif mouth == "o":
        ellipse(0, 28, 5, 6)


def kawung(cx, cy, d=7):
    for k in range(4):
        a = math.radians(45 + 90 * k)
        ellipse(cx + d * math.cos(a), cy + d * math.sin(a), 6.5, 3.6, rot=45 + 90 * k, sw=2)
    circle(cx, cy, 1.8, fill=INK)


def darmo(eyes="happy", mouth="smile", full=False):
    """Older man: peci, thin mustache, batik (kawung) shirt, checked sarong."""
    if full:
        path("M-64,150 L-72,262 L72,262 L64,150 Z", fill="#fff")    # sarong
        for y in (196, 214):                                   # checked band
            xe = 64 + 8 * (y - 150) / 112
            line(-xe, y, xe, y)
        for x in (-24, 24):
            line(x, 150, x * 1.05, 262)
        ellipse(-28, 268, 24, 8)                               # sandals
        ellipse(28, 268, 24, 8)
    torso(76)
    poly([(-22, 52), (0, 76), (22, 52)])                       # collar
    line(0, 76, 0, 160)
    circle(-8, 104, 3)
    circle(-8, 134, 3)
    for cx, cy in ((-46, 104), (-30, 140), (44, 104), (30, 140)):
        kawung(cx, cy)
    rect(-12, 30, 24, 24)                                      # neck
    circle(-42, 6, 8)
    circle(42, 6, 8)
    ellipse(-38, -12, 7, 10)                                   # grey tufts under the peci
    ellipse(38, -12, 7, 10)
    circle(0, 0, 42)
    path("M-38,-24 L-34,-62 Q0,-70 34,-62 L38,-24 Q0,-32 -38,-24 Z", fill="#fff")   # peci
    path("M-14,-17 Q0,-21 14,-17")                             # forehead line
    eye(-16, 2, eyes)
    eye(16, 2, eyes)
    line(-24, -8, -9, -10)
    line(24, -8, 9, -10)
    path("M0,6 Q-7,17 3,18")
    path("M-20,25 Q-10,18 0,22 Q10,18 20,25 Q10,23 0,26 Q-10,23 -20,25 Z", fill="#fff")  # thin mustache
    if mouth == "smile":
        path("M-12,31 Q0,41 12,31")
    path("M-30,18 Q-27,26 -22,30")                             # smile lines
    path("M30,18 Q27,26 22,30")


def person(kind="hijab", full=False, mouth="smile"):
    """Generic neighbour. kind: hijab, bald, bun, cap, kid, curly."""
    if full:
        rect(-44, 150, 40, 100, r=6)
        rect(4, 150, 40, 100, r=6)
        ellipse(-26, 254, 24, 8)
        ellipse(26, 254, 24, 8)
    torso(64, top=54)
    if kind == "hijab":
        path("M-48,4 Q-52,-54 0,-54 Q52,-54 48,4 Q54,54 28,70 L-28,70 Q-54,54 -48,4 Z", fill="#fff")
        circle(0, 0, 32)
    else:
        rect(-11, 30, 22, 26)
        if kind != "cap":
            circle(-36, 6, 7)
            circle(36, 6, 7)
        circle(0, 0, 37)
    if kind == "bald":
        ellipse(-31, -16, 7, 12)
        ellipse(31, -16, 7, 12)
        circle(-14, 2, 10)
        circle(14, 2, 10)
        line(-4, 2, 4, 2)
        path("M-14,22 Q0,15 14,22 Q0,26 -14,22 Z", fill="#fff")
    elif kind == "bun":
        circle(0, -50, 14)
        path("M-37,0 Q-40,-40 0,-40 Q40,-40 37,0 Q28,-22 0,-24 Q-28,-22 -37,0 Z", fill="#fff")
    elif kind == "cap":
        path("M-36,-6 Q-38,-48 0,-48 Q38,-48 36,-6 Z", fill="#fff")
        path("M-36,-6 L-56,-2 Q-58,-12 -36,-14 Z", fill="#fff")
    elif kind == "kid":
        pts = [(-38, -2)]
        for i in range(9):
            pts.append((-36 + i * 9, -44 if i % 2 else -30))
        pts += [(38, -2), (30, -20), (-30, -20)]
        poly(pts)
    elif kind == "curly":
        for k in range(9):
            a = math.radians(180 + k * 22.5)
            circle(34 * math.cos(a), -6 + 34 * math.sin(a), 11)
    ex, ey = (12, 4) if kind == "hijab" else (14, 6)
    if kind != "bald":
        circle(-ex, ey, 3.5, fill=INK)
        circle(ex, ey, 3.5, fill=INK)
    if mouth == "smile":
        path(f"M-10,{ey + 14} Q0,{ey + 22} 10,{ey + 14}")
    elif mouth == "o":
        ellipse(0, ey + 18, 5, 6)


# ================================================================ page
if __name__ == "__main__":
    begin("Siap!", "Kalau bingung, bilang aja “Siap!”")

    # ---- window with Nadia, her parents and the RT outside
    WX, WY, WW, WH = 310, 192, 176, 232
    rect(WX - 10, WY - 10, WW + 20, WH + 24, r=8)
    add(f'<clipPath id="win"><rect x="{WX}" y="{WY}" width="{WW}" height="{WH}"/></clipPath>')
    add('<g clip-path="url(#win)">')
    rect(WX, WY, WW, WH, fill="#fff")
    for i, (kind, x) in enumerate([("cap", 322), ("curly", 350), ("bun", 384), ("bald", 446), ("kid", 474)]):
        place(x, 310 - (i % 2) * 6, 0.36, lambda k=kind: person(k))
    place(415, 304, 0.36, lambda: darmo())
    place(338, 352, 0.5, lambda: person("hijab"))               # Ibu
    place(452, 350, 0.5, lambda: person("bald"))                # Bapak
    place(395, 348, 0.52, lambda: nadia())
    add("</g>")
    rect(WX, WY, WW, WH, fill="none")
    rect(WX - 16, WY + WH + 4, WW + 32, 14, r=4)                # sill
    bubble(WX + 8, WY + 8, WW - 16, 56, 392, 312)
    text(WX + WW / 2, WY + 30, "Aku udah di depan!", 12.5, "bold")
    text(WX + WW / 2, WY + 50, "Udah siap-siap, kan?", 12.5, "bold")

    # ---- "Siap!" bubbles rising from the phone
    for (bx, by, tx) in [(78, 192, 110), (156, 252, 170), (82, 312, 110), (150, 372, 150)]:
        bubble(bx, by, 112, 44, tx, by + 60)
        text(bx + 56, by + 30, "Siap!", 22, "bold")

    # ---- bed
    rect(64, 470, 22, 232, r=6)                                 # headboard
    circle(75, 470, 11)
    rect(476, 540, 22, 162, r=6)                                # footboard
    circle(487, 540, 11)
    rect(96, 672, 14, 30, r=3)
    rect(452, 672, 14, 30, r=3)
    rect(86, 652, 390, 22, r=4)                                 # bed base
    rect(86, 608, 390, 46, r=10)                                # mattress
    rect(92, 574, 190, 46, r=22)                                # pillow

    # Dimas lying on his back, head on the pillow, the rest under the blanket
    def dimas_lying():
        path("M-54,20 Q-72,74 -20,72 L20,72 Q72,74 54,20 Z", fill="#fff")   # hood (as in dimas())
        dimas_head(eyes="shut", mouth="sleep")
    place(204, 536, 1, dimas_lying, rot=-28)
    path("M268,652 L268,500 Q268,466 304,466 L330,466 Q384,466 402,520 Q420,558 470,558 L470,652 Z", fill="#fff")
    path("M268,620 L470,620")                                   # blanket hem
    for cx, cy in [(296, 500), (340, 494), (300, 556), (350, 540), (296, 600), (350, 596),
                   (400, 590), (440, 590), (384, 552)]:
        poly([(cx, cy - 9), (cx + 9, cy), (cx, cy + 9), (cx - 9, cy)])
    for x in range(284, 470, 26):
        circle(x, 636, 4)

    # the phone on the pillow, still answering
    def phone():
        rect(-24, -42, 48, 84, r=8)
        rect(-18, -32, 36, 60, r=3)
        rect(-14, -26, 22, 10, r=4)
        rect(-8, -12, 22, 10, r=4)
        rect(-14, 2, 22, 10, r=4)
        circle(0, 35, 3)
    place(118, 536, 1, phone, rot=-10)
    circle(140, 498, 14)
    text(140, 503, "312", 11, "bold")

    # zzz
    text(244, 476, "z", 16, "bold")
    text(262, 456, "z", 20, "bold")

    end("siap.svg")
