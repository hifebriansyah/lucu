#!/usr/bin/env python3
"""Coloring page for the story "Hari Baik" (ai/40.md), drawn with plain geometry.

Dimas and Nadia on the wedding stage, the tent packed with the whole RT, the
envelope box overflowing, and Pak Darmo smiling at the real source of his
"hari baik": SITI's answer on his phone. Characters come from siap.py.

Math: scalloped tent valance (half circles), rose curves r = R cos(3t) for the
stage flowers.

Run:  python3 hari-baik.py   ->  hari-baik.svg
"""
from siap import *

begin("Hari Baik", "Hari paling baik: tanggal gajian.")

# ---- tent roof and valance
poly([(62, 214), (280, 172), (498, 214)])
n = 10
w = 436 / n
for i in range(n):
    x = 62 + i * w
    path(f"M{x},214 A{w / 2},{w / 2 * 0.8} 0 0 0 {x + w},214 Z", fill="#fff")
rect(66, 214, 10, 486)                                        # poles
rect(484, 214, 10, 486)

# ---- pelaminan: backdrop with arch and flowers
path("M138,430 L138,290 Q138,226 280,226 Q422,226 422,290 L422,430 Z", fill="#fff")
path("M156,430 L156,296 Q156,244 280,244 Q404,244 404,296 L404,430 Z", fill="#fff")
rect(214, 252, 132, 26, r=13)
text(280, 271, "Dimas &amp; Nadia", 14, "bold")


def flower(cx, cy, R=18):
    pts = []
    for i in range(0, 361):
        t = i / 360 * math.pi
        r = R * math.cos(3 * t)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    poly(pts)
    circle(cx, cy, 4)


for cx, cy in [(150, 288), (410, 288), (140, 340), (420, 340)]:
    flower(cx, cy)

place(236, 314, 0.6, lambda: dimas(mouth="smile"))
place(326, 314, 0.6, lambda: nadia())
for sx in (236 - 22, 326 + 20):                               # corsages
    flower(sx, 372, 8)
rect(120, 410, 320, 22, r=4)                                  # stage
rect(130, 432, 300, 16)

# ---- packed tent: two rows of guests
kinds = ["hijab", "cap", "bun", "curly", "bald", "kid", "hijab", "cap", "curly", "bun"]
for i in range(9):
    place(96 + i * 46, 476, 0.36, lambda k=kinds[i % len(kinds)]: person(k))
for i in range(8):
    place(118 + i * 46, 512, 0.4, lambda k=kinds[(i + 3) % len(kinds)]: person(k, mouth="o" if i % 3 == 0 else "smile"))

# ---- the envelope box, overflowing
for x, y, deg in [(372, 548, -18), (400, 540, 10), (432, 546, -6), (452, 556, 20), (346, 562, 25)]:
    def env(x=x, y=y):
        rect(x - 22, y - 14, 44, 28, r=2)
        path(f"M{x - 22},{y - 14} L{x},{y + 2} L{x + 22},{y - 14}")
    rotated(x, y, deg, env)
rect(330, 560, 148, 140, r=6)
rect(372, 572, 64, 10, r=5)                                   # slot
rect(350, 606, 108, 32, r=5)
text(404, 629, "AMPLOP", 18, "bold")
for x, y, deg in [(352, 682, 12), (446, 688, -14)]:
    def env2(x=x, y=y):
        rect(x - 20, y - 12, 40, 24, r=2)
        path(f"M{x - 20},{y - 12} L{x},{y + 2} L{x + 20},{y - 12}")
    rotated(x, y, deg, env2)
line(76, 700, 484, 700)                                       # floor


# ---- Pak Darmo in front, smiling at his phone
def darmo_phone():
    capsule(-62, 80, -84, 150, 30)                            # arm down
    darmo(eyes="happy", full=True)
    circle(-86, 156, 14)
    capsule(64, 80, 92, 136, 30)                              # arm up holding the phone


place(152, 700 - 270 * 0.86, 0.86, darmo_phone)
rect(212, 456, 112, 150, r=12)                                # phone
rect(220, 468, 96, 120, r=4)
circle(268, 597, 4)
text(268, 494, "SITI:", 14, "bold")
text(268, 528, "Tanggal 25.", 15, "bold")
text(268, 556, "Hari gajian.", 15, "bold")
circle(232, 590, 14)                                          # hand on the phone

end("hari-baik.svg")
