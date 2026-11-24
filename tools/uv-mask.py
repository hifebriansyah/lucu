#!/usr/bin/env python3
"""SITI's outline on the front cover, for the spot UV mask: ai/book-cover/web/front-uv-siti.png,
opaque black where SITI is, see-through elsewhere, the same size as ai/book-cover/front.jpeg
(the glowing circle is drawn by the page, from frontRing in books.json).

Two pictures, both on this Mac (nothing is uploaded or generated):
1. ai/book-cover/front-siti-only.png, the cover's SITI on white with everyone else removed,
   gives her rough outline: everything that isn't white, with small white spots inside her
   (her shirt, light lines) filled and big ones (between her legs) left empty, shrunk by RIM
   to drop her glow. It is not an exact copy of the cover (her arm hangs a little apart), so:
2. OpenCV's GrabCut snaps that outline to the real edges in ai/book-cover/front.jpeg, within
   BAND pixels of it: deeper inside is surely her, further out surely not. So the edge, and
   gaps like the one between her hand and her skirt, follow the cover itself.
Then the outline is smoothed and left with a soft (anti-aliased) edge like a drawn shape, and
its fingerprint goes in web/index.json so browsers load the new one.

Usage: python3 tools/uv-mask.py [preview.jpg] [smooth]   (needs opencv-python-headless, numpy)
The optional preview shows the outline in red over the cover, to check it lines up.
"""
import hashlib
import json
import sys
from pathlib import Path

import cv2
import numpy as np

SRC = "ai/book-cover/front-siti-only.png"
COVER = "ai/book-cover/front.jpeg"
OUT = "ai/book-cover/web/front-uv-siti.png"
RIM = 3      # px in the SITI-only picture: her thin cyan glow
HOLE = 500   # px in the SITI-only picture: white spots inside her up to this size are filled
BAND = 24    # px in the cover: how far GrabCut may move the edge
SMOOTH = float(sys.argv[2]) if len(sys.argv) > 2 else 2  # px in the cover: how much the outline is smoothed


def disk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def solid(mask, hole):
    """The biggest piece of mask, with enclosed spots smaller than hole filled."""
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask)
    mask = (lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(1 - mask)
    for i in range(1, n):
        if i != lab[0, 0] and stats[i, cv2.CC_STAT_AREA] < hole:
            mask[lab == i] = 1
    return mask


cover = cv2.imread(COVER)
H, W = cover.shape[:2]
src = cv2.imread(SRC)
scale = W / src.shape[1]

# 1. Rough outline from the SITI-only picture, at the cover's size.
grey = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
sat = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)[..., 1]
rough = solid(((grey < 235) | (sat > 40)).astype(np.uint8), HOLE)
rough = cv2.erode(rough, disk(RIM))
rough = cv2.resize(rough * 255, (W, H), interpolation=cv2.INTER_LINEAR) >= 128

# 2. Snap it to the cover's edges.
m = np.full((H, W), cv2.GC_BGD, np.uint8)
m[cv2.dilate(rough.astype(np.uint8), disk(BAND)) > 0] = cv2.GC_PR_BGD
m[rough] = cv2.GC_PR_FGD
m[cv2.erode(rough.astype(np.uint8), disk(BAND)) > 0] = cv2.GC_FGD
ys, xs = np.nonzero(m != cv2.GC_BGD)
y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
crop = m[y0:y1, x0:x1].copy()
cv2.grabCut(cover[y0:y1, x0:x1].copy(), crop, None, np.zeros((1, 65)), np.zeros((1, 65)), 5, cv2.GC_INIT_WITH_MASK)
fg = np.zeros((H, W), np.uint8)
fg[y0:y1, x0:x1] = np.isin(crop, [cv2.GC_FGD, cv2.GC_PR_FGD])
fg = solid(fg, int(HOLE * scale * scale))

# Up to four times the size, smooth the pixel steps away, cut at the middle, then shrink back
# with averaging: a smooth outline with a soft edge.
big = cv2.resize(fg * 255, (W * 4, H * 4), interpolation=cv2.INTER_LINEAR)
big = np.where(cv2.GaussianBlur(big, (0, 0), SMOOTH * 4) >= 128, 255, 0).astype(np.uint8)
alpha = cv2.resize(big, (W, H), interpolation=cv2.INTER_AREA)

out = np.zeros((H, W, 4), np.uint8)
out[..., 3] = alpha
cv2.imwrite(OUT, out)
print(f"saved {OUT} ({W} x {H})")

# Its fingerprint in web/index.json: the pages add it to the picture's address, so a browser
# never shows an old cached mask.
index_file = Path(OUT).parent / "index.json"
index = json.loads(index_file.read_text(encoding="utf-8")) if index_file.exists() else {}
index[Path(OUT).name] = {"src": hashlib.sha1(Path(OUT).read_bytes()).hexdigest()[:12]}
index_file.write_text(json.dumps(dict(sorted(index.items())), indent=1) + "\n", encoding="utf-8")

if len(sys.argv) > 1:
    a = alpha[..., None] / 255 * 0.5
    red = np.zeros_like(cover)
    red[:] = (60, 0, 255)
    cv2.imwrite(sys.argv[1], (cover * (1 - a) + red * a).astype(np.uint8))
    print(f"preview {sys.argv[1]}")
