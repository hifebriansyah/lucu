# lucu

Two books of short, funny Indonesian stories, plus a small website to preview and print them (a coloring book is in progress locally).

## Books

| Folder | Title | Stories |
|---|---|---|
| `ai/` | *Kelakuan Pengguna Ai!!* | 62, in six parts plus an epilog |
| `politics/` | *Janji Tinggal Janji* (working title) | 100, in five parts |

Book 1's author is Febri, S.Kom., PSM, PSPO; the manuscript ends with a Tentang Penulis page (page 149). The imprint page still has placeholders for the editor, cover designer, ISBN and publisher.

The story books have one story per file (`1.md`, `2.md`, ...) and a `naskah.md` with the full manuscript. Writing rules are in `CLAUDE.md`; each book's cast and background are in its own `CLAUDE.md`.

`ai/naskah.docx` is a Word export of book 1 for publishers and the ISBN submission: A5, 11 pt Literata, mirrored margins, parts on right-hand pages, running heads, page numbers and a Daftar Isi with page references (Word asks to update fields on open). It is generated from `naskah.md`, so rebuild it after the manuscript changes. Install Literata on any computer that opens it.

## Preview site

Serve the folder with any static server and open `index.html`:

```bash
python3 -m http.server 5210 --directory lucu
```

- `index.html`: the bookshelf, with every book listed in `books.json`.
- `reader.html?book=<id>`: reads `naskah.md` as a paged book with a page-turn animation. The cover sits alone, then page 1 opens on the right. Arrow keys or swiping turn pages, and the dropdown jumps to any story. Buttons around the page number in the bar go to the previous or next page (‹ ›) and to the previous or next part (« »); « goes to the start of the current part first. On phones they sit on a second row.
- **Hitam putih** in the reader bar turns every interior page black and white (pictures, toska frames and rules, chat bubble, part-title glow), for a grayscale print. The print page has the same button, and the choice is shared, so turning it on in either place prints the PDF in black and white (the info line says "hitam putih"). Each color swaps for a grey of the same brightness (`--siti-grey`, worked out from the chosen border color in `assets/paper.js`) instead of a grayscale filter over the page, because Chrome prints filtered text as a picture. The paper keeps its color and the cover stays in color. The browser remembers the choice.
- **Sampul** in the reader bar saves the cover as the reader shows it, title included, as a PNG at A5 300 dpi (1748 × 2480 px, `<book>-sampul.png`). It lays the cover out off screen and draws it with html-to-image, loaded from jsDelivr only when the button is used. The cover copy in `ai/book-cover/web/` is kept at full size (up to 2600 px tall) so the saved file stays sharp. A printer may want bleed around it; ask them for the exact size.
- **Kertas** in the reader bar sets the paper color of the pages: pick one of five book papers (Gading, the default, Krem, Putih, Novel, Abu) or any color from **Warna lain**, see it on the pages right away, then **Simpan** to keep it (closing without saving goes back to the saved color; **Default** returns to Gading). It is saved per book in this browser (`assets/paper.js`), and the print page uses it too, so the PDF comes out on that paper color, Gading unless another is saved. The same panel has **Bingkai gambar**, the color of the line around the story pictures: Toska (the default), Hitam, Abu, Emas, Merah or any color. **Simpan** keeps both colors, **Default** resets both, and the PDF uses the saved border color too. The button's dot shows the paper color with a ring in the border color. Its last section, **Bentuk gambar bagian**, picks the shape of the picture on the page facing each part picture: Hexagon (the default), 41-gon, Lingkaran, Persegi, Segitiga or 16:9 (Hexagon, Persegi and 16:9 get rounded corners of about 41px; the hexagon is drawn with a rounded-hexagon SVG mask, since `clip-path` can't round a polygon). Each button shows a small preview of its shape. It is saved with the colors and the PDF uses it too (`data-frame` on the page root, shapes in `assets/pages.css`).
- `print.html?book=<id>`: the print-ready interior, A5 (14,8 × 21 cm). It shows exactly the pages the reader shows: same page breaks, page numbers and contents page numbers. Both use one layout engine (`assets/paginate.js`) and one set of A5 page styles (`assets/pages.css`: 11 pt Literata on about 16 pt leading, Inter for page numbers and running heads, every page heading (story titles, Kata Pengantar, Kenalan dengan SITI, Daftar Isi and the part contents pages) in Orbitron like the part titles, centered with wide letter spacing, margins 2 cm top and bottom, 2 cm at the spine and 1.6 cm outside); the reader only scales the pages to fit the window. Use **Cetak / Simpan PDF** to save the PDF.

## Covers

Book 1 has a picture for every story, in both the reader and the print PDF. Every story starts on a left-hand page, and its picture fills the right-hand page facing it, inside the normal page margins (so it lines up with the text on the facing page), with 41px rounded corners, a 3 pt white gap, then a 1.5 pt toska border (`--siti` in `assets/pages.css`, changeable in the reader) and the page number below it. A story that runs over its page by fewer than 20 lines (Bawa Pantunnya, Gorengan, Draf, Strawberry) ends at the top of its picture page instead, and the picture shrinks to fill the rest, 7 mm below the last line (`SPILL_MAX` in `assets/paginate.js`). A story 20 or more lines over would continue on the next left-hand page, with a blank page facing it; no story does now. The book is 149 pages. The originals are `ai/story-cover/<n>.jpeg` (3:4, named by story number); the pages load the smaller copies in `ai/story-cover/web/<n>.jpg` (1200 px tall), set by `storyArt` in `books.json`. After adding, replacing or renaming any story or section picture, run `tools/covers.py` (see below).

Each part page is a full-page picture on a right-hand page, edge to edge, with a thin white line inside its edge (41px rounded corners, like the story pictures) and a poster-style title on top: the part name big (BAGIAN SATU, EPILOG) and its subtitle under it (JAM KERJA; the Epilog has none), in white Orbitron (a free Google font) with a cyan glow. The glow is a CSS `drop-shadow` filter rather than `text-shadow`, because Chrome prints a blurred text-shadow on outlined text as a solid box in the PDF. The pictures are `ai/section-cover/s1.jpeg` to `s7.jpeg`, in part order (s1 is Bagian Satu, s7 is the Epilog), with copies in `ai/section-cover/web/` set by `partArt`. If a story is renumbered, rename its picture too. The left-hand page before each part, which would otherwise be blank, shows a fan-service picture of SITI in a frame, a hexagon unless another shape is picked in the Kertas panel (a line in the picture-border color, a white gap, then the picture), facing the part's picture on the right (`partArtPage` in `assets/paginate.js`); Bagian Satu's is pages 10 and 11. The originals are `ai/section-art/1.jpeg` to `7`, in part order like the part pictures, with copies in `ai/section-art/web/` set by `contentsArt` in `books.json` and made by `tools/covers.py`. Under each picture is a line of trivia about Nadia, labeled TRIVIA in small Orbitron, from `contentsTrivia` in `books.json` (one line per part, in part order). The Word export doesn't include the pictures yet.

Front-matter pages can have a picture too, set by `frontArt` in `books.json` (section heading → copy): "Kenalan dengan SITI" (page 8) faces a full picture of SITI on page 9, framed like a story picture. Page 8 is set in the middle of the page: its Nama / Jenis / Kode / Keahlian / Kelemahan lines become a profile card in toska (labels in small Orbitron), with the paragraph centered under it. Any front-matter paragraph made only of `**Label:** value` lines becomes such a card (`profileCards` in `assets/book.js`). The title page (page 1) sets the title like the cover, from `coverTitle`: KELAKUAN big and PENGGUNA Ai!! smaller, in Orbitron with plain dark ink so it prints cleanly, a short toska rule, the subtitle in italic Literata and the author in small Inter. Page 2, the imprint (any front section mentioning ISBN or Hak cipta), is set like a printed book's: small left-aligned type at the foot of the page, the book's name in Orbitron and a thin rule before the rights notice. Page 3, the dedication, is a short italic verse in the upper middle of the page; its closing question ("Yakin?") shows as a sent chat message under it, in a toska bubble marked Terkirim (`chatBubble` in `assets/book.js`; `naskah.md` is unchanged). Its original is `ai/front-art/siti.jpeg`, a link to `ai/characterV3/siti-cover.jpeg`, and `tools/covers.py` copies it to `ai/front-art/web/siti.jpg` and `bw/`, so after updating that picture just run the script.

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

Book 1 has a real cover: the picture in `ai/book-cover/` (any name; `cover.jpeg` wins if there are several), copied by `tools/covers.py` to `ai/book-cover/web/cover.jpg` (full size, up to 2600 px tall), which `cover` in `books.json` points to. The picture has no lettering, so with `coverText: true` the pages set the title over it in the part pages' Orbitron poster style: the kicker (SITI · M4.KZ-A) on top, KELAKUAN big with PENGGUNA Ai!! smaller under it (`coverTitle` in `books.json`, written exactly as it should show), and the subtitle at the bottom, over dark fades. After replacing the cover, run `python3 tools/covers.py`. The other books' covers are placeholders; to use a real one, save it as `<book>/cover.jpg` (2:3, for example 1400 × 2100 px). The print PDF is the interior only; send the cover to the printer separately.

## Coloring book

The coloring book in `draw/` is a local work in progress: the folder is in `.gitignore`, so it is not in git or on the site, and it is not in `books.json` until it is ready.

## Deploy

Every push to `main` publishes the site to GitHub Pages with `.github/workflows/pages.yml` (plain static files, no build step). Only the picture copies in `web/` and `bw/` are in git; the originals stay local, so run `tools/covers.py` on this machine and commit the copies it writes.
