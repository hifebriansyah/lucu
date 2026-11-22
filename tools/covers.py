#!/usr/bin/env python3
"""Update the copies of a book's cover, story and section pictures: color for the reader,
and black and white for a grayscale print.

Usage:
    python3 tools/covers.py              # book "ai": only new or changed pictures
    python3 tools/covers.py --all        # remake every copy
    python3 tools/covers.py --check      # only report what would change
    python3 tools/covers.py --contrast 1.2   # punchier black and white (use with --all)

The reader and the print page load small copies of the pictures, set in books.json:
`storyArt` (for example ai/story-cover/web/{n}.jpg) and `partArt`
(ai/section-cover/web/s{n}.jpg). Originals live one folder up (ai/story-cover/1.jpeg,
ai/section-cover/s1.jpeg) and can be jpg, jpeg, png or webp.

For each original this writes, when the copy is missing or the original's contents changed
(checked by fingerprint, not by file date, since a file copied in from Finder keeps its old date):
- web/<name>.jpg: color, 1200 px tall, loaded by the reader and the print page;
- bw/<name>.jpg: black and white at the same size, with the tones stretched so the darkest
  part prints black and the lightest white (plain grayscale often prints flat and muddy).
The cover (books.json `cover`, for example ai/book-cover/web/cover.jpg) is copied from the
picture one folder up, whatever its name (cover.jpeg wins if there are several), 1800 px tall.
Each part's contents page has a picture too (books.json `contentsArt`, for example
ai/section-art/web/{n}.jpg from ai/section-art/1.jpeg, numbered like the parts).
Front-matter pictures (books.json `frontArt`, for example "Kenalan dengan SITI" ->
ai/front-art/web/siti.jpg) are copied from the picture of the same name one folder up.
It also writes web/index.json with each picture's fingerprint; the pages add it to the
picture's address, so the browser never shows an old cached copy. It deletes copies whose
original is gone, and warns about
originals whose name doesn't fit the pattern (like a4.jpeg instead of s4.jpeg) or
stories and sections that have no picture. Originals are never changed.

Needs Pillow: pip install pillow
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
EXTS = {".jpg", ".jpeg", ".png", ".webp"}
HEIGHT = 1200
COVER_HEIGHT = 1800  # the cover shows larger, so it gets a bigger copy
QUALITY = 80


def manuscript_counts(book):
    """Number of stories and of parts (sections) in the book's naskah.md."""
    text = (ROOT / book["manuscript"]).read_text(encoding="utf-8")
    stories = len(re.findall(r"^##\s+\d+\.\s", text, re.M))
    parts = len(re.findall(r"^#\s+(?:Bagian\b|Epilog\b)", text, re.M))
    return stories, parts


def save_copies(src, dest, bw_dest, contrast):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
    if im.height > HEIGHT:
        im = im.resize((round(im.width * HEIGHT / im.height), HEIGHT), Image.LANCZOS)
    if dest:
        dest.parent.mkdir(exist_ok=True)
        im.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    if bw_dest:
        gray = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=0.5)
        if contrast != 1:
            gray = ImageEnhance.Contrast(gray).enhance(contrast)
        bw_dest.parent.mkdir(exist_ok=True)
        gray.save(bw_dest, "JPEG", quality=85, optimize=True, progressive=True)


def fingerprint(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()[:12]


def sync(label, pattern, expected, rebuild, check, contrast):
    """pattern is the books.json value, e.g. ai/section-cover/web/s{n}.jpg."""
    web = ROOT / Path(pattern).parent
    src_dir = web.parent
    bw = src_dir / "bw"
    prefix, suffix = Path(pattern).name.split("{n}")
    stem_re = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    if not src_dir.is_dir():
        print(f"{label}: no folder {src_dir.relative_to(ROOT)}")
        return 0

    # What each copy was last made from: {copy name: {"src": fingerprint, "contrast": n}}.
    index_file = web / "index.json"
    try:
        index = json.loads(index_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        index = {}

    made = 0
    found = set()
    for src in sorted(src_dir.iterdir(), key=lambda p: (len(p.stem), p.stem)):
        if not src.is_file() or src.suffix.lower() not in EXTS:
            continue
        m = stem_re.match(src.stem)
        if not m:
            print(f"  warning: {src.relative_to(ROOT)} doesn't match {prefix}<number>, skipped")
            continue
        n = int(m.group(1))
        found.add(n)
        name = f"{prefix}{n}{suffix}"
        fp = fingerprint(src)
        old = index.get(name, {})
        changed = rebuild or old.get("src") != fp
        dest = web / name if changed or not (web / name).exists() else None
        bw_dest = bw / name if changed or not (bw / name).exists() or old.get("contrast") != contrast else None
        index[name] = {"src": fp, "contrast": contrast}
        if not dest and not bw_dest:
            continue
        made += 1
        what = " + ".join(x for x, d in (("color", dest), ("bw", bw_dest)) if d)
        print(f"  {'would update' if check else 'update'} {src.relative_to(ROOT)} ({what})")
        if not check:
            save_copies(src, dest, bw_dest, contrast)

    # Copies whose original was removed or renamed.
    for folder in (web, bw):
        if not folder.is_dir():
            continue
        for copy in folder.iterdir():
            m = stem_re.match(copy.stem)
            if copy.is_file() and m and int(m.group(1)) not in found:
                print(f"  {'would delete' if check else 'delete'} {copy.relative_to(ROOT)} (no original)")
                if not check:
                    copy.unlink()
                index.pop(copy.name, None)
    if not check:
        web.mkdir(exist_ok=True)
        index_file.write_text(json.dumps(dict(sorted(index.items())), indent=1) + "\n", encoding="utf-8")

    missing = [n for n in range(1, expected + 1) if n not in found]
    extra = sorted(n for n in found if n > expected)
    if missing:
        print(f"  warning: no picture for {label} {', '.join(map(str, missing))}")
    if extra:
        print(f"  warning: pictures {', '.join(map(str, extra))} have no {label} in naskah.md")
    print(f"{label}: {len(found)} pictures, {made} {'to update' if check else 'updated'}")
    return made


def sync_cover(pattern, rebuild, check):
    """The book cover: any picture in the folder above web/ (cover.jpeg is preferred when
    there are several), copied to web/cover.jpg at COVER_HEIGHT px tall."""
    web = ROOT / Path(pattern).parent
    src_dir = web.parent
    dest = ROOT / pattern
    pics = [p for p in src_dir.iterdir() if p.is_file() and p.suffix.lower() in EXTS] if src_dir.is_dir() else []
    if not pics:
        print(f"cover: no picture in {src_dir.relative_to(ROOT)}")
        return 0
    named = [p for p in pics if p.stem.lower() == "cover"]
    src = named[0] if named else max(pics, key=lambda p: p.stat().st_mtime)
    if len(pics) > 1:
        print(f"  warning: {len(pics)} pictures in {src_dir.relative_to(ROOT)}, using {src.name}"
              + ("" if named else " (the newest; name the one you want cover.jpeg)"))
    index_file = web / "index.json"
    try:
        index = json.loads(index_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        index = {}
    fp = fingerprint(src)
    if not rebuild and index.get(dest.name, {}).get("src") == fp and dest.exists():
        print("cover: up to date")
        return 0
    print(f"  {'would update' if check else 'update'} {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
    if not check:
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
        if im.height > COVER_HEIGHT:
            im = im.resize((round(im.width * COVER_HEIGHT / im.height), COVER_HEIGHT), Image.LANCZOS)
        web.mkdir(exist_ok=True)
        im.save(dest, "JPEG", quality=85, optimize=True, progressive=True)
        index[dest.name] = {"src": fp}
        index_file.write_text(json.dumps(dict(sorted(index.items())), indent=1) + "\n", encoding="utf-8")
    print(f"cover: {'to update' if check else 'updated'}")
    return 1


def sync_front(art, rebuild, check):
    """Each part's contents page has a picture too (books.json `contentsArt`, for example
ai/section-art/web/{n}.jpg from ai/section-art/1.jpeg, numbered like the parts).
Front-matter pictures (books.json `frontArt`, title -> web/<name>.jpg): each is copied
    from the picture of the same name one folder up (ai/front-art/siti.jpeg -> web/siti.jpg),
    HEIGHT px tall, with a black-and-white copy in bw/."""
    made = 0
    for title, pattern in art.items():
        dest = ROOT / pattern
        web, bw = dest.parent, dest.parent.parent / "bw"
        srcs = [p for p in web.parent.glob(dest.stem + ".*") if p.suffix.lower() in EXTS]
        if not srcs:
            print(f"  warning: no picture for {title} ({web.parent.relative_to(ROOT)}/{dest.stem}.jpeg)")
            continue
        index_file = web / "index.json"
        try:
            index = json.loads(index_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            index = {}
        fp = fingerprint(srcs[0])
        if not rebuild and index.get(dest.name, {}).get("src") == fp and dest.exists():
            continue
        print(f"  {'would update' if check else 'update'} {srcs[0].relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
        made += 1
        if not check:
            web.mkdir(parents=True, exist_ok=True)
            bw.mkdir(exist_ok=True)
            save_copies(srcs[0], dest, bw / dest.name, 1.0)
            index[dest.name] = {"src": fp}
            index_file.write_text(json.dumps(dict(sorted(index.items())), indent=1) + "\n", encoding="utf-8")
    print(f"front: {len(art)} pictures, {made} {'to update' if check else 'updated'}")
    return made


def main():
    parser = argparse.ArgumentParser(description="Update the color and black-and-white copies of story and section pictures.")
    parser.add_argument("--book", default="ai", help="book id from books.json (default: ai)")
    parser.add_argument("--all", action="store_true", help="remake every copy, not only changed ones")
    parser.add_argument("--check", action="store_true", help="only report what would change")
    parser.add_argument("--contrast", type=float, default=1.0, help="extra black-and-white contrast, 1 = none (try 1.1 to 1.3)")
    args = parser.parse_args()

    catalog = json.loads((ROOT / "books.json").read_text(encoding="utf-8"))
    book = next((b for b in catalog if b["id"] == args.book), None)
    if not book:
        sys.exit(f"no book '{args.book}' in books.json")
    cover = book.get("cover", "")
    has_cover = "/web/" in cover  # a cover kept as a copy of an original one folder up
    if not book.get("storyArt") and not book.get("partArt") and not book.get("frontArt") and not book.get("contentsArt") and not has_cover:
        sys.exit(f"book '{args.book}' has no storyArt, partArt or cover copy in books.json")

    stories, parts = manuscript_counts(book)
    if book.get("storyArt"):
        sync("story", book["storyArt"], stories, args.all, args.check, args.contrast)
    if book.get("partArt"):
        sync("section", book["partArt"], parts, args.all, args.check, args.contrast)
    if book.get("contentsArt"):
        sync("contents", book["contentsArt"], parts, args.all, args.check, args.contrast)
    if book.get("frontArt"):
        sync_front(book["frontArt"], args.all, args.check)
    if has_cover:
        sync_cover(cover, args.all, args.check)


if __name__ == "__main__":
    main()
