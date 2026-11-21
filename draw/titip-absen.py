#!/usr/bin/env python3
"""Coloring page for the story "Titip Absen" (book 1, story 8).

08.00 in the lobby: Pak Satpam takes the daily attendance selfie with Pak Bos's account.
A zoomed-in phone screen shows the account name, the selfie and "Hadir 08.00".
Math: clock ticks on a circle, scalloped leaves (plant), rotated peace-sign fingers.

Run:  python3 titip-absen.py  ->  titip-absen.svg
"""
import math

from lib import *


def at(dx, dy, s, fn):
    add(f'<g transform="translate({dx},{dy}) scale({s})">')
    fn()
    add("</g>")


# ---------------------------------------------------------------- Pak Satpam (same head as pelan-pelan.py)
def satpam_head(mood="shock"):
    """Pak Satpam: security cap with a badge, thick eyebrows."""
    circle(-48, 8, 10)
    circle(48, 8, 10)
    circle(0, 0, 48)
    path("M-48,-14 Q-52,-74 0,-76 Q52,-74 48,-14 Z", fill="#fff")   # cap crown
    rect(-50, -26, 100, 14, r=4)                                     # band
    path("M-46,-14 Q0,-6 62,-16 Q66,-8 56,-4 Q0,4 -46,-6 Z", fill="#fff")  # brim
    poly([(0, -62), (14, -56), (12, -40), (0, -32), (-12, -40), (-14, -56)])  # badge
    circle(0, -48, 4)
    rect(-30, 3, 22, 5, r=2.5, fill=INK)                             # thick eyebrows
    rect(8, 3, 22, 5, r=2.5, fill=INK)
    if mood == "shock":
        circle(-18, 19, 8)
        circle(18, 19, 8)
        circle(-15, 20, 3, fill=INK)
        circle(21, 20, 3, fill=INK)
        add(f'<ellipse cx="0" cy="38" rx="7" ry="6" {style()}/>')
    else:
        path("M-26,23 Q-18,14 -10,23 M10,23 Q18,14 26,23")            # happy closed eyes
        path("M-24,33 Q0,31 24,33 Q20,50 0,50 Q-20,50 -24,33 Z", fill="#fff")  # big grin
        line(-21, 38, 21, 38)
    path("M-3,22 Q-7,28 1,29")                                        # nose


# ---------------------------------------------------------------- page
begin("Titip Absen", "Pak Bos datang jam sebelas, absennya jam delapan.")

FLOOR = 702
line(62, FLOOR, 498, FLOOR)

# lobby wall clock showing 08.00
cx, cy = 118, 236
circle(cx, cy, 44)
circle(cx, cy, 36, fill="none")
for k in range(12):
    a = k * math.pi / 6
    line(cx + 30 * math.sin(a), cy - 30 * math.cos(a), cx + 36 * math.sin(a), cy - 36 * math.cos(a))
h_ang = math.radians(8 * 30)
line(cx, cy, cx + 19 * math.sin(h_ang), cy - 19 * math.cos(h_ang))
line(cx, cy, cx, cy - 29)
circle(cx, cy, 3.5, fill=INK)
rect(cx - 34, cy + 54, 68, 28, r=6)
text(cx, cy + 75, "08.00", 18, "bold")

# lobby sign
rect(196, 186, 100, 40, r=8)
text(246, 214, "LOBI", 22, "bold")

# potted plant (scalloped leaves)
scalloped(96, 540, 30, n=8, a=0.14)
scalloped(74, 590, 24, n=7, a=0.14)
scalloped(120, 596, 26, n=7, a=0.14)
poly([(70, 620), (126, 620), (118, 698), (78, 698)])
rect(64, 610, 68, 18, r=5)


# ---- Pak Satpam taking the selfie
def satpam():
    # trousers, shoes, belt
    rect(-50, 150, 46, 120, r=4)
    rect(4, 150, 46, 120, r=4)
    add(f'<ellipse cx="-30" cy="272" rx="30" ry="10" {style()}/>')
    add(f'<ellipse cx="30" cy="272" rx="30" ry="10" {style()}/>')
    # uniform shirt
    path("M-72,160 L-70,90 Q-66,56 0,56 Q66,56 70,90 L72,160 Z", fill="#fff")
    rect(-72, 144, 144, 18, r=3)                                     # belt
    rect(-12, 144, 24, 18, r=3)                                      # buckle
    rect(-14, 44, 28, 18)                                            # neck
    poly([(-18, 56), (0, 80), (18, 56)])                             # collar
    line(0, 80, 0, 144)
    for y in (96, 120):
        circle(6, y, 3)
    rect(-58, 62, 36, 12, r=3)                                       # shoulder patches
    rect(22, 62, 36, 12, r=3)
    rect(-54, 92, 32, 28, r=3)                                       # pocket
    line(-54, 100, -22, 100)
    poly([(30, 90), (48, 90), (48, 106), (39, 114), (30, 106)])      # chest badge
    # left arm: peace sign next to the face
    capsule(-64, 80, -96, 30, 32)
    capsule(-96, 30, -76, -24, 32)
    circle(-74, -30, 15)
    rotated(-80, -42, -14, lambda: rect(-86, -76, 11, 38, r=5.5))
    rotated(-68, -42, 12, lambda: rect(-73, -76, 11, 38, r=5.5))
    # right arm: stretched up to hold the phone
    capsule(64, 80, 118, 10, 32)
    capsule(118, 10, 160, -12, 32)
    satpam_head("grin")


at(232, 430, 1, satpam)

# the phone (back side, toward the viewer), held up for the selfie
rect(374, 342, 52, 88, r=9)
circle(388, 356, 6)
rect(404, 352, 12, 8, r=2)
circle(398, 422, 16)
text(316, 362, "Cekrek!", 16, "bold", italic=True)

# zoomed-in screen of the attendance app: Pak Bos's account, Pak Satpam's face
ZX, ZY, ZW, ZH = 326, 168, 170, 164
poly([(400, 342), (384, ZY + ZH - 4), (416, ZY + ZH - 4)])
rect(ZX, ZY, ZW, ZH, r=12)
rect(ZX + 8, ZY + 8, ZW - 16, 26, r=6)
text(ZX + ZW / 2, ZY + 27, "Akun: Pak Bos", 13, "bold")
rect(ZX + 36, ZY + 40, ZW - 72, 82, r=6)
at(ZX + ZW / 2, ZY + 90, 0.5, lambda: satpam_head("grin"))
rect(ZX + 20, ZY + 128, ZW - 40, 28, r=10)
text(ZX + ZW / 2, ZY + 148, "Hadir 08.00", 14, "bold")

end("titip-absen.svg")
