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
- **Hitam putih** in the reader bar shows the interior pictures in black and white, to preview a grayscale print (the cover stays in color). The browser remembers the choice.
- **Kertas** in the reader bar sets the paper color of the pages: pick one of five book papers (Krem, the default, Putih, Gading, Novel, Abu) or any color from **Warna lain**, see it on the pages right away, then **Simpan** to keep it (closing without saving goes back to the saved color; **Default** returns to Krem). It is saved per book in this browser (`assets/paper.js`), and the print page uses it too, so the PDF comes out on that paper color; without a saved color the PDF pages are white.
- `print.html?book=<id>`: the print-ready interior, A5 (14,8 × 21 cm). It shows exactly the pages the reader shows: same page breaks, page numbers and contents page numbers. Both use one layout engine (`assets/paginate.js`) and one set of A5 page styles (`assets/pages.css`: 11 pt Literata on about 16 pt leading, Inter for page numbers and running heads, story titles in Orbitron like the part titles, centered with wide letter spacing, margins 2 cm top and bottom, 2 cm at the spine and 1.6 cm outside); the reader only scales the pages to fit the window. Use **Cetak / Simpan PDF** to save the PDF.

## Covers

Book 1 has a picture for every story, in both the reader and the print PDF. Every story starts on a left-hand page, and its picture fills the right-hand page facing it, inside the normal page margins (so it lines up with the text on the facing page), with 41px rounded corners, a 3 pt white gap, then a 1.5 pt SITI-blue border (`--siti` in `assets/pages.css`) and the page number below it. Seven stories run to a second page; their text continues on the next left-hand page, with a blank page facing it. The originals are `ai/story-cover/<n>.jpeg` (3:4, named by story number); the pages load the smaller copies in `ai/story-cover/web/<n>.jpg` (1200 px tall), set by `storyArt` in `books.json`. After adding, replacing or renaming any story or section picture, run `tools/covers.py` (see below).

Each part page is a full-page picture, edge to edge, with a thin white line inside its edge and a poster-style title on top: the part name big (BAGIAN SATU, EPILOG) and its subtitle under it (JAM KERJA; the Epilog has none), in white Orbitron (a free Google font) with a cyan glow. The pictures are `ai/section-cover/s1.jpeg` to `s7.jpeg`, in part order (s1 is Bagian Satu, s7 is the Epilog), with copies in `ai/section-cover/web/` set by `partArt`. If a story is renumbered, rename its picture too. The Word export doesn't include the pictures yet.

`tools/covers.py` (needs Pillow) updates every copy in one go: the color copies in `web/` that the pages load, and black-and-white copies in `bw/` for a grayscale print. The black and white has its tones stretched so it doesn't print muddy. By default it only redoes pictures that are new or changed, checked by their contents rather than file dates (a file copied in from Finder keeps its old date). It writes `web/index.json` with each picture's fingerprint, and the pages add it to the picture's address, so the browser never shows an old cached picture. It also deletes copies whose original is gone, and warns about a misnamed file (like `a4.jpeg`) or a story or section with no picture. Originals are never changed:

```bash
python3 tools/covers.py
```

```bash
python3 tools/covers.py --check
```

```bash
python3 tools/covers.py --all --contrast 1.2
```

Book 1 has a real cover: the picture in `ai/book-cover/` (any name; `cover.jpeg` wins if there are several), copied by `tools/covers.py` to `ai/book-cover/web/cover.jpg` (1800 px tall), which `cover` in `books.json` points to. The picture has no lettering, so with `coverText: true` the pages set the title over it in the part pages' Orbitron poster style: the kicker (SITI · M4.KZ-A) on top, KECERDASAN BUATAN, with KELAKUAN ASLI big under it, and the subtitle at the bottom, over dark fades. After replacing the cover, run `python3 tools/covers.py`. The other books' covers are placeholders; to use a real one, save it as `<book>/cover.jpg` (2:3, for example 1400 × 2100 px). The print PDF is the interior only; send the cover to the printer separately.

## Coloring book

The coloring pages in `draw/` are drawn with code, not an image model: each `<slug>.py` builds `<slug>.svg` from plain geometry using `draw/lib.py`. The look and the character designs are in `draw/STYLE.md`. After adding or changing a page, run `python3 draw/build.py` to rebuild `draw/naskah.md`. In the print PDF, each picture sits on a right-hand page with a blank back, so markers don't bleed through.

## Deploy

Every push to `main` publishes the site to GitHub Pages with `.github/workflows/pages.yml` (plain static files, no build step). Only the picture copies in `web/` and `bw/` are in git; the originals stay local, so run `tools/covers.py` on this machine and commit the copies it writes.
