#!/usr/bin/env python3
"""Coloring page for the story "Uang Rokok" (ai/31.md), drawn with plain geometry.

A week after Dimas set SITI up next to the human counter to learn by listening,
he comes back with a broken KTP, and the kiosk asks him for "uang rokok".
Characters come from siap.py so they match the other pages.

Run:  python3 uang-rokok.py   ->  uang-rokok.svg
"""
from siap import *

begin("Uang Rokok", "Seminggu belajar, SITI ikut minta uang rokok.", title_size=50)

# ---- loket 1: the human clerk SITI learned from, palm already open
rect(76, 296, 196, 150, r=8)
rect(86, 306, 176, 140, r=4)
place(174, 378, 0.56, lambda: person("bald"))
circle(236, 428, 13)                                          # open palm on the counter
for k in range(4):
    capsule(226 + k * 7, 420, 228 + k * 7, 408, 7)

# ---- SITI as the kiosk on loket 2
rect(388, 410, 24, 34)                                        # neck of the stand
rect(316, 286, 168, 128, r=10)
rect(326, 296, 148, 96, r=6)
text(400, 408, "SITI", 13, "bold")
line(400, 286, 400, 262)
circle(400, 256, 7)
rect(350, 322, 24, 18, r=3)                                   # square eyes, half closed
rect(426, 322, 24, 18, r=3)
line(346, 318, 378, 324)
line(454, 318, 422, 324)
path("M360,358 Q400,386 440,358 Q400,370 360,358 Z", fill="#fff")   # sly grin
circle(344, 356, 6, fill="none")
circle(456, 356, 6, fill="none")

# speech bubble with a cigarette-pack icon
bubble(74, 190, 236, 82, 322, 318)
text(162, 224, "Ada uang", 21, "bold")
text(162, 252, "rokoknya, Mas?", 21, "bold")


def pack():
    rect(-16, -20, 32, 46, r=3)                               # pack
    line(-16, -6, 16, -6)                                     # flip-top lid
    for k, h in enumerate((14, 20, 10)):                      # cigarettes sticking out
        rect(-12 + k * 9, -20 - h, 7, h, r=1)
        line(-12 + k * 9, -20 - h + 5, -5 + k * 9, -20 - h + 5)
    circle(0, 10, 7)


place(278, 238, 1, pack, rot=8)

# ---- counter
rect(62, 440, 436, 24, r=4)
rect(70, 464, 420, 100)
rect(124, 474, 100, 26, r=5)
text(174, 493, "LOKET 1", 15, "bold")
line(62, 700, 498, 700)                                       # floor

# ---- queue of residents behind Dimas (far to near)
for x, s, kind in [(96, 0.5, "cap"), (156, 0.54, "hijab"), (222, 0.58, "curly"), (284, 0.6, "kid")]:
    place(x, 700 - 256 * s, s, lambda k=kind: person(k, full=True, mouth="o" if k == "kid" else "smile"))


# ---- Dimas at the front, holding up his cracked KTP
def dimas_ktp():
    capsule(64, 80, 86, 150, 30)                              # arm down
    dimas(eyes="wide", mouth="o", full=True)
    circle(88, 156, 14)
    capsule(-66, 80, -98, 22, 30)                             # arm up with the KTP
    rect(-158, -40, 92, 58, r=5)
    rect(-150, -30, 26, 32, r=3)
    circle(-137, -20, 6)
    path("M-146,2 Q-137,-12 -128,2 Z", fill="#fff")
    line(-116, -24, -76, -24)
    line(-116, -12, -84, -12)
    path("M-104,-40 L-110,-26 L-98,-14 L-106,0 L-100,18")   # the crack
    circle(-100, 22, 14)
    path("M48,-46 Q40,-30 48,-24 Q56,-30 48,-46 Z", fill="#fff")  # sweat drop


place(400, 700 - 270 * 0.8, 0.8, dimas_ktp)

end("uang-rokok.svg")
