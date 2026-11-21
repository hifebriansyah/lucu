#!/usr/bin/env python3
"""Coloring page for the story "Bikin HRD Merinding" (book 1, story 1).

Raka, the fake "senior IT expert", panics at the server rack after typing a command
from a TikTok video; the office goes dark and Pak Bos shouts from the doorway.

Run:  python3 bikin-hrd-merinding.py  ->  bikin-hrd-merinding.svg
"""
import math

from lib import *


def at(dx, dy, s, fn):
    add(f'<g transform="translate({dx},{dy}) scale({s})">')
    fn()
    add("</g>")


# ---------------------------------------------------------------- Pak Bos (geometry from gorengan.py)
def bos_head():
    circle(170, 372, 12)
    circle(290, 372, 12)
    circle(230, 370, 60)
    path("M178,345 Q190,300 230,308 Q270,300 282,345 Q262,322 230,330 Q198,322 178,345 Z", fill="#fff")
    circle(208, 368, 14)
    circle(252, 368, 14)
    line(222, 368, 238, 368)
    circle(208, 370, 3.5, fill=INK)
    circle(252, 370, 3.5, fill=INK)
    line(196, 346, 218, 350)
    line(264, 346, 242, 350)
    path("M230,376 Q223,388 232,390")
    path("M205,402 Q218,388 230,398 Q242,388 255,402 Q242,408 230,404 Q218,408 205,402 Z", fill="#fff")
    add(f'<ellipse cx="230" cy="418" rx="9" ry="7" {style()}/>')
    path("M292,318 Q283,334 292,342 Q301,334 292,318 Z", fill="#fff")


def bos_body():
    path("M150,600 L150,500 Q150,440 230,440 Q310,440 310,500 L310,600 Z", fill="#fff")
    rect(215, 420, 30, 30)
    poly([(205, 440), (230, 482), (255, 440)])
    poly([(222, 482), (238, 482), (234, 494), (226, 494)])
    poly([(226, 494), (234, 494), (241, 516), (230, 530), (219, 516)])
    path("M175,452 L205,440 M285,452 L255,440")
    circle(197, 540, 4)
    circle(263, 540, 4)


def bos_full():
    # trousers and shoes below the gorengan body
    rect(160, 596, 66, 150, r=4)
    rect(234, 596, 66, 150, r=4)
    add(f'<ellipse cx="186" cy="752" rx="38" ry="14" {style()}/>')
    add(f'<ellipse cx="274" cy="752" rx="38" ry="14" {style()}/>')
    bos_body()
    # one hand on the door frame, one hand up at the cheek in shock
    capsule(296, 470, 330, 540, 34)
    capsule(164, 470, 132, 420, 34)
    bos_head()
    circle(132, 414, 18)


# ---------------------------------------------------------------- scene
begin("Bikin HRD Merinding", "Satu perintah dari TikTok, satu kantor ikut mati.", title_size=36)

FLOOR = 702
line(62, FLOOR, 498, FLOOR)

# doorway with Pak Bos (scaled gorengan geometry)
rect(66, 262, 128, FLOOR - 262, r=4)
rect(74, 270, 112, FLOOR - 270, r=2, fill="none")
s = 0.6
at(128 - 230 * s, FLOOR - 4 - 766 * s, s, bos_full)

# speech bubble from Pak Bos
path("M72,180 Q72,168 84,168 L224,168 Q236,168 236,180 L236,214 Q236,226 224,226 L150,226 "
     "L130,400 L118,226 L84,226 Q72,226 72,214 Z", fill="#fff")
text(154, 194, "Lho, kok", 16, "bold")
text(154, 215, "semua mati?!", 16, "bold")

# hanging lamp, switched off: "PET!"
line(444, 162, 444, 192)
path("M414,222 L428,192 L460,192 L474,222 Z", fill="#fff")
path("M432,222 Q432,240 444,240 Q456,240 456,222 Z", fill="#fff")
text(384, 214, "PET!", 16, "bold")

# server rack
RX, RY, RW = 404, 262, 88
rect(RX, RY, RW, FLOOR - RY - 8, r=6)
rect(RX + 10, FLOOR - 8, 18, 8)
rect(RX + RW - 28, FLOOR - 8, 18, 8)
# console screen with the TikTok command
rect(RX + 10, RY + 12, RW - 20, 74, r=4)
rect(RX + 16, RY + 18, RW - 32, 62, r=2)
text(RX + RW / 2, RY + 42, "$ sudo", 13, "bold")
text(RX + RW / 2, RY + 62, "reboot", 13, "bold")
# server units, all lights off
for i in range(6):
    y = RY + 100 + i * 54
    rect(RX + 10, y, RW - 20, 44, r=4)
    for k in range(2):
        circle(RX + 25 + k * 15, y + 22, 5)
    for k in range(3):
        line(RX + 56 + k * 8, y + 13, RX + 56 + k * 8, y + 31)
# unplugged cable with a spark-free plug


# ---------------------------------------------------------------- Raka
def raka():
    cx, cy = 268, 352
    # legs and shoes
    rect(cx - 36, 600, 32, 92, r=4)
    rect(cx + 4, 600, 32, 92, r=4)
    add(f'<ellipse cx="{cx - 24}" cy="{FLOOR - 8}" rx="26" ry="9" {style()}/>')
    add(f'<ellipse cx="{cx + 24}" cy="{FLOOR - 8}" rx="26" ry="9" {style()}/>')
    # neck
    rect(cx - 13, cy + 34, 26, 30)
    # oversized blazer: wide shoulders, long body
    path(f"M{cx - 78},620 L{cx - 70},452 Q{cx - 66},414 {cx - 22},410 L{cx + 22},410 "
         f"Q{cx + 66},414 {cx + 70},452 L{cx + 78},620 Z", fill="#fff")
    poly([(cx - 22, 410), (cx, 470), (cx + 22, 410)])                  # shirt
    path(f"M{cx - 22},410 L{cx - 34},452 L{cx - 18},446 L{cx},520 L{cx + 18},446 "
         f"L{cx + 34},452 L{cx + 22},410")                               # lapels
    circle(cx, 540, 5)
    circle(cx, 570, 5)
    rect(cx - 58, 540, 30, 8, r=2)                                      # pocket
    # left arm: hand on the cheek (panic)
    capsule(cx - 62, 436, cx - 84, 486, 38)
    capsule(cx - 84, 486, cx - 50, 392, 38)
    # right arm: holding the phone with the TikTok video up
    capsule(cx + 62, 436, cx + 92, 486, 38)
    capsule(cx + 92, 486, cx + 94, 424, 38)
    # head
    circle(cx - 44, cy + 4, 10)
    circle(cx + 44, cy + 4, 10)
    # tall spiky hair
    spikes = [(cx - 44, cy - 6)]
    n = 5
    for i in range(n):
        x0 = cx - 46 + i * 92 / n
        spikes.append((x0 + 46 / n + (i - 2) * 4, cy - 100 + 12 * abs(i - 2)))
        spikes.append((x0 + 92 / n, cy - 44))
    spikes[-1] = (cx + 44, cy - 6)
    poly(spikes)
    circle(cx, cy, 44)
    path(f"M{cx - 44},{cy - 6} Q{cx - 40},{cy - 46} {cx},{cy - 46} Q{cx + 40},{cy - 46} {cx + 44},{cy - 6} "
         f"Q{cx + 30},{cy - 26} {cx + 14},{cy - 22} L{cx + 4},{cy - 32} L{cx - 6},{cy - 22} "
         f"Q{cx - 26},{cy - 26} {cx - 44},{cy - 6} Z", fill="#fff")
    # wide panicked eyes
    circle(cx - 16, cy + 2, 10)
    circle(cx + 16, cy + 2, 10)
    circle(cx - 16, cy + 4, 3, fill=INK)
    circle(cx + 16, cy + 4, 3, fill=INK)
    line(cx - 28, cy - 10, cx - 8, cy - 18)
    line(cx + 28, cy - 10, cx + 8, cy - 18)
    circle(cx - 46, cy + 22, 16)            # hand on the cheek
    # wobbly open mouth
    path(f"M{cx - 13},{cy + 26} Q{cx - 7},{cy + 20} {cx},{cy + 24} Q{cx + 7},{cy + 20} {cx + 13},{cy + 26} "
         f"Q{cx + 12},{cy + 38} {cx},{cy + 38} Q{cx - 12},{cy + 38} {cx - 13},{cy + 26} Z", fill="#fff")
    # sweat drops
    for x, y in ((cx + 52, cy - 30), (cx - 58, cy - 20)):
        path(f"M{x},{y} Q{x - 8},{y + 14} {x},{y + 20} Q{x + 8},{y + 14} {x},{y} Z", fill="#fff")


raka()

# phone with the TikTok video, in Raka's right hand
PX, PY = 332, 318
rect(PX, PY, 66, 104, r=10)
rect(PX + 5, PY + 10, 56, 76, r=4)
poly([(PX + 26, PY + 22), (PX + 26, PY + 44), (PX + 44, PY + 33)])
text(PX + 33, PY + 62, "SERVER", 9, "bold")
text(PX + 33, PY + 77, "NGEBUT!", 9, "bold")
circle(PX + 33, PY + 95, 4)
circle(PX + 33, PY + 104, 17)

end("bikin-hrd-merinding.svg")
