# Coloring pages: style guide

A coloring book drawn only with code (no image model), one page per story from book 1 (`../ai/`). `gorengan.py` is the reference page; copy its look.

## Page

- Each page is a Python script `<slug>.py` that imports `lib.py` and writes `<slug>.svg`.
- 140 × 200 mm, viewBox 560 × 800. Use `begin(title, caption)` and `end("<slug>.svg")` from `lib.py`. They draw the circuit-board border, the outlined title, "Warnai halamannya!", and the caption at y = 736.
- The scene sits between y ≈ 170 and y ≈ 715, inside x ≈ 62–498.
- Black outlines only: `#111`, stroke width 3 (2–2.5 for small details). Fills are white. Solid black only for tiny things (pupils, a clock centre).
- Every region must be a closed shape that a child can color. No hatching, no grey, no gradients, no shading.
- Shapes are simple and geometric: circles, rounded rectangles, quadratic curves. Use maths for patterns (rose curves, scallops, sine waves, spirals).
- Title: the story title. Caption: one short line from the story that sums up the joke, in Indonesian.
- Text inside the scene (speech bubbles, screens, signs): short, bold, readable.

## Characters

Keep each character recognisable across pages:

- **SITI**: a boxy monitor or robot screen with an antenna and a round tip, square eyes, and a zigzag or smile mouth (as in `gorengan.py`).
- **Pak Bos**: round head, hair only as a band on top, round glasses, thick mustache, shirt and tie (as in `gorengan.py`).
- **Pak Darmo**: older man, peci (black cap, can be left white to color), thin mustache, batik shirt (pattern of simple closed shapes), sarong.
- **Bu Ratna**: hijab framing a round face, long blouse, kind eyes.
- **Bima**: small boy, short spiky fringe, SD uniform (shirt and shorts), big eyes.
- **Raka**: young man, tall spiky hair, oversized blazer.
- **Dimas**: messy hair, hoodie, bags under the eyes.
- **Nadia**: long straight hair, cardigan.
- **Bang Yudi**: rectangular glasses, short beard, plaid shirt.
- **Bu HRD**: hair in a bun, blazer, lanyard ID card.
- **Pak Satpam**: security cap with badge, uniform with shoulder patches.
- **Pak Lurah**: peci and safari suit.

## Checking a page

Render it and look at it before calling it done. Quick Look crops to a square, so wrap the page in a square viewBox and a square size first:

```bash
sed -e 's/viewBox="0 0 560 800"/viewBox="-120 0 800 800"/' -e 's/width="140mm" height="200mm"/width="800" height="800"/' page.svg > /tmp/check.svg
qlmanage -t -s 1000 -o /tmp /tmp/check.svg
```

Then open `/tmp/check.svg.png` and check: nothing overlaps the border, the title, or the caption; every region is closed; the joke reads at a glance.
