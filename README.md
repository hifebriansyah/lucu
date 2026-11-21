# lucu

Two books of short, funny Indonesian stories, plus a small website to preview and print them.

## Books

| Folder | Title | Stories |
|---|---|---|
| `ai/` | *Kecerdasan Buatan, Kelakuan Asli* | 71, in six parts plus an epilog |
| `politics/` | *Janji Tinggal Janji* (working title) | 100, in five parts |

Each book has one story per file (`1.md`, `2.md`, ...) and a `naskah.md` with the full manuscript. Writing rules are in `CLAUDE.md`; each book's cast and background are in its own `CLAUDE.md`.

## Preview site

Serve the folder with any static server and open `index.html`:

```bash
python3 -m http.server 5210 --directory lucu
```

- `index.html`: the bookshelf, with every book listed in `books.json`.
- `reader.html?book=<id>`: reads `naskah.md` as a paged book with a page-turn animation. Arrow keys or swiping turn pages, and the dropdown jumps to any story.
- `print.html?book=<id>`: lays out the interior with Paged.js at 14 × 21 cm, A5 or 13 × 19 cm, with mirrored margins, page numbers, running heads, and a contents page with real page numbers. Use **Cetak / Simpan PDF** to save a print-ready PDF.

## Covers

Covers are placeholders. To use a real one, save it as `<book>/cover.jpg` (2:3, for example 1400 × 2100 px). The shelf and the reader pick it up automatically. The print PDF is the interior only; send the cover to the printer separately.
