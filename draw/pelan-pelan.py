#!/usr/bin/env python3
"""Coloring page for the story "Pelan-Pelan" (book 1, story 6).

Friday night: Bu HRD and Pak Satpam peek over the cubicle wall, expecting a secret date.
Bang Yudi is alone with his laptop, a pivot table on screen and SITI's voice in the speaker.
Math: grid of a pivot table, plaid shirt as a clipped grid, sine sound waves, star polygons.

Run:  python3 pelan-pelan.py  ->  pelan-pelan.svg
"""
import math

from lib import *


def at(dx, dy, s, fn):
    add(f'<g transform="translate({dx},{dy}) scale({s})">')
    fn()
    add("</g>")


def star(cx, cy, R, r, n=5):
    pts = []
    for i in range(2 * n):
        a = -math.pi / 2 + i * math.pi / n
        rr = R if i % 2 == 0 else r
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    poly(pts)


# ---------------------------------------------------------------- characters (origin = head centre)
def hrd_head(shock=True):
    """Bu HRD: hair in a bun, round face."""
    circle(0, -60, 20)                                            # bun
    circle(-44, 6, 9)
    circle(44, 6, 9)
    circle(0, 0, 46)
    path("M-46,4 Q-50,-48 0,-48 Q50,-48 46,4 Q40,-20 22,-24 Q6,-14 0,-30 "
         "Q-6,-14 -22,-24 Q-40,-20 -46,4 Z", fill="#fff")      # hair, middle parting
    circle(-16, 4, 9)
    circle(16, 4, 9)
    circle(-13, 5, 3, fill=INK)
    circle(19, 5, 3, fill=INK)
    path("M-26,-14 Q-16,-22 -6,-16 M26,-14 Q16,-22 6,-16")
    if shock:
        add(f'<ellipse cx="0" cy="28" rx="7" ry="9" {style()}/>')
    circle(-44, 20, 4)                                            # earrings
    circle(44, 20, 4)


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
        path("M-26,20 Q-18,12 -10,20 M10,20 Q18,12 26,20")            # happy closed eyes
        path("M-24,33 Q0,31 24,33 Q20,50 0,50 Q-20,50 -24,33 Z", fill="#fff")  # big grin
        line(-21, 38, 21, 38)
    path("M-3,22 Q-7,28 1,29")                                        # nose


def yudi_head():
    """Bang Yudi: rectangular glasses, short beard, short hair."""
    circle(-44, 4, 10)
    circle(44, 4, 10)
    circle(0, 0, 44)
    path("M-44,-2 Q-46,-46 0,-46 Q46,-46 44,-2 L38,-18 L26,-22 L14,-16 L0,-24 L-14,-16 "
         "L-26,-22 L-38,-18 Z", fill="#fff")                           # short hair
    path("M-42,12 Q-40,46 0,48 Q40,46 42,12 Q34,26 18,30 Q0,22 -18,30 Q-34,26 -42,12 Z",
         fill="#fff")                                                   # short beard
    path("M-10,36 Q0,40 10,36")                                         # small smile
    rect(-32, -6, 26, 18, r=3)                                          # rectangular glasses
    rect(6, -6, 26, 18, r=3)
    line(-6, 2, 6, 2)
    # looking right, at the laptop
    circle(-14, 3, 3, fill=INK)
    circle(24, 3, 3, fill=INK)
    path("M0,10 Q-4,18 4,19")


# ---------------------------------------------------------------- page
begin("Pelan-Pelan", "Suara mesra itu cuma SITI ngajarin pivot table.")

FLOOR = 700
line(62, FLOOR, 498, FLOOR)

# window with a Friday-night moon and stars
rect(220, 176, 140, 96, r=6)
line(290, 176, 290, 272)
path("M256,196 Q234,210 242,234 Q252,254 276,246 Q250,240 248,222 Q246,204 256,196 Z", fill="#fff")
star(318, 204, 10, 4.5)
star(340, 238, 7, 3)
star(306, 252, 6, 2.6)

# ---- Bang Yudi's side: chair, Yudi, desk, laptop
# chair back
rect(278, 430, 112, 150, r=14)
# Yudi's body: plaid shirt (clipped grid)
body = "M268,600 L268,536 Q268,492 334,492 Q400,492 400,536 L400,600 Z"
add(f'<clipPath id="plaid"><path d="{body}"/></clipPath>')
path(body, fill="#fff")
add('<g clip-path="url(#plaid)">')
for x in range(284, 400, 22):
    line(x, 480, x, 610)
for y in range(514, 600, 22):
    line(256, y, 412, y)
add("</g>")
rect(320, 472, 28, 26)                                          # neck
path(body)
poly([(312, 492), (334, 516), (356, 492)])                      # collar
# arm reaching to the laptop trackpad
capsule(392, 530, 420, 574, 30)
at(334, 440, 1, yudi_head)

# desk
rect(250, 582, 248, 24, r=6)
rect(266, 606, 20, 94)
rect(462, 606, 20, 94)

# laptop with the pivot table, turned toward the viewer
rect(388, 470, 108, 82, r=6)
rect(396, 478, 92, 66, r=2)
cols, rows = 3, 4
cw, rh = 92 / cols, 66 / rows
for c in range(1, cols):
    line(396 + c * cw, 478, 396 + c * cw, 544)
for r_ in range(1, rows):
    line(396, 478 + r_ * rh, 488, 478 + r_ * rh)
text(396 + cw / 2, 478 + rh - 4, "Bln", 10, "bold")
text(396 + 1.5 * cw, 478 + rh - 4, "Jual", 10, "bold")
text(396 + 2.5 * cw, 478 + rh - 4, "Σ", 11, "bold")
poly([(382, 552), (502, 552), (494, 582), (390, 582)])          # keyboard base
add(f'<ellipse cx="420" cy="574" rx="14" ry="6" {style()}/>')    # hand on the trackpad
# speaker sound waves
for k in range(3):
    r = 12 + k * 10
    a0, a1 = math.radians(-60), math.radians(60)
    path(f"M{442 + r * math.sin(a0):.1f},{466 - r * math.cos(a0):.1f} "
         f"A{r},{r} 0 0 1 {442 + r * math.sin(a1):.1f},{466 - r * math.cos(a1):.1f}")

# SITI's voice bubble from the speaker
path("M380,300 Q380,286 394,286 L484,286 Q498,286 498,300 L498,382 Q498,396 484,396 L452,396 "
     "L442,432 L430,396 L394,396 Q380,396 380,382 Z", fill="#fff")
text(439, 314, "SITI:", 13, "bold", italic=True)
text(439, 336, "Pintar,", 15, "bold")
text(439, 356, "sayang...", 15, "bold")
text(439, 380, "Pivot jadi!", 13, "bold")

# ---- the cubicle wall with Bu HRD and Pak Satpam peeking over it
WALL_TOP = 466


def hrd():
    # shoulders: blazer and lanyard
    path("M-62,120 L-58,80 Q-54,50 0,50 Q54,50 58,80 L62,120 Z", fill="#fff")
    poly([(-16, 50), (0, 76), (16, 50)])
    path("M-16,50 L-26,88 M16,50 L26,88")
    hrd_head()


def satpam_body():
    path("M-66,120 L-62,82 Q-58,52 0,52 Q58,52 62,82 L66,120 Z", fill="#fff")
    rect(-62, 62, 32, 12, r=3)                                   # shoulder patches
    rect(30, 62, 32, 12, r=3)
    poly([(-14, 52), (0, 70), (14, 52)])
    satpam_head("shock")


at(112, 392, 0.85, hrd)
at(202, 390, 0.85, satpam_body)

# wall (covers their bodies)
rect(62, WALL_TOP, 200, FLOOR - WALL_TOP, r=4)
rect(62, WALL_TOP, 200, 16, r=4)
for x in (110, 155, 200):
    circle(x, 610, 4)
# lanyard card hanging over the wall
line(112, 482, 112, 500)
rect(96, 500, 32, 40, r=4)
circle(112, 514, 7)
line(102, 530, 122, 530)
# fingers gripping the top of the wall
for hx in (84, 142, 172, 240):
    rect(hx - 12, WALL_TOP - 8, 24, 18, r=8)

# "YUDI!" shout
scalloped(116, 226, 44, n=12, a=0.12)
text(116, 234, "YUDI!", 20, "bold")
poly([(102, 266), (118, 266), (104, 300)])

end("pelan-pelan.svg")
