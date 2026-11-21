# lucu

Two books of short, funny Indonesian stories and a coloring book, plus a small website to preview and print them.

## Books

| Folder | Title | Stories |
|---|---|---|
| `ai/` | *Kecerdasan Buatan, Kelakuan Asli* | 62, in six parts plus an epilog |
| `politics/` | *Janji Tinggal Janji* (working title) | 100, in five parts |
| `draw/` | *Buku Mewarnai SITI* | 11 coloring pages, one per story from book 1 |

The story books have one story per file (`1.md`, `2.md`, ...) and a `naskah.md` with the full manuscript. Writing rules are in `CLAUDE.md`; each book's cast and background are in its own `CLAUDE.md`.

`ai/naskah.docx` is a Word export of book 1 for publishers and the ISBN submission: A5, 11 pt Literata, mirrored margins, parts on right-hand pages, running heads, page numbers and a Daftar Isi with page references (Word asks to update fields on open). It is generated from `naskah.md`, so rebuild it after the manuscript changes. Install Literata on any computer that opens it.

## Preview site

Serve the folder with any static server and open `index.html`:

```bash
python3 -m http.server 5210 --directory lucu
```

- `index.html`: the bookshelf, with every book listed in `books.json`.
- `reader.html?book=<id>`: reads `naskah.md` as a paged book with a page-turn animation. The cover sits alone, then page 1 opens on the right. Arrow keys or swiping turn pages, and the dropdown jumps to any story.
- `print.html?book=<id>`: the print-ready interior, A5 (14,8 × 21 cm). It shows exactly the pages the reader shows: same page breaks, page numbers and contents page numbers. Both use one layout engine (`assets/paginate.js`) and one set of A5 page styles (`assets/pages.css`: 11 pt Literata on about 16 pt leading, Inter for page numbers and running heads, margins 2 cm top and bottom, 2 cm at the spine and 1.6 cm outside); the reader only scales the pages to fit the window. Use **Cetak / Simpan PDF** to save the PDF.

## Covers

Covers are placeholders. To use a real one, save it as `<book>/cover.jpg` (2:3, for example 1400 × 2100 px). The shelf and the reader pick it up automatically. The print PDF is the interior only; send the cover to the printer separately.

## Coloring book

The coloring pages in `draw/` are drawn with code, not an image model: each `<slug>.py` builds `<slug>.svg` from plain geometry using `draw/lib.py`. The look and the character designs are in `draw/STYLE.md`. After adding or changing a page, run `python3 draw/build.py` to rebuild `draw/naskah.md`. In the print PDF, each picture sits on a right-hand page with a blank back, so markers don't bleed through.
