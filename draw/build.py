#!/usr/bin/env python3
"""Build naskah.md for the coloring book from the page SVGs in this folder.

Run:  python3 build.py   (after running the page scripts)

Pages follow the order of the stories in book 1 (../ai/). Pages whose SVG
doesn't exist yet are skipped.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PB = '<div style="page-break-after: always;"></div>'
TITLE = "Buku Mewarnai SITI"
SUBTITLE = "Gambar dari Cerita-Cerita Kecerdasan Buatan, Kelakuan Asli"

# (slug, title) in story order from book 1
PAGES = [
    ("bikin-hrd-merinding", "Bikin HRD Merinding"),
    ("gorengan", "Gorengan"),
    ("pelan-pelan", "Pelan-Pelan"),
    ("titip-absen", "Titip Absen"),
    ("strawberry", "Strawberry"),
    ("waktu-layar", "Waktu Layar"),
    ("bangun-sahur", "Bangun Sahur"),
    ("uang-rokok", "Uang Rokok"),
    ("siap", "Siap!"),
    ("balap-karung", "Balap Karung"),
    ("hari-baik", "Hari Baik"),
]

present = [(slug, title) for slug, title in PAGES if os.path.exists(os.path.join(HERE, f"{slug}.svg"))]

parts = [
    f"# {TITLE}\n\n### {SUBTITLE}\n\n&nbsp;\n\n**[Nama Penulis]**",
    f"""**{TITLE}**
{SUBTITLE}

Gambar: dibuat dengan kode, tanpa model gambar.
Cetakan pertama, 2026

Hak cipta dilindungi undang-undang. Boleh difotokopi untuk diwarnai di rumah dan di sekolah.""",
    """## Cara Pakai

Setiap gambar diambil dari satu cerita di buku *Kecerdasan Buatan, Kelakuan Asli*. Pilih gambar, ambil pensil warna, dan warnai sesukamu.

Gambar hanya dicetak di halaman kanan, jadi spidol tidak tembus ke gambar berikutnya.

Kalau kamu bingung harus mewarnai apa dulu, tanya SITI. Dia pasti menjawab dengan percaya diri.""",
]
parts += [f"![{title}](draw/{slug}.svg)" for slug, title in present]

with open(os.path.join(HERE, "naskah.md"), "w") as f:
    f.write(f"\n\n{PB}\n\n".join(parts) + "\n")
print(f"wrote naskah.md with {len(present)} pages")
