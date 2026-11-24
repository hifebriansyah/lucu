#!/usr/bin/env python3
"""Update the copies of a book's cover, story and section pictures that the reader and the
print page load. (Hitam putih greys these same copies in the browser, so there are no
separate black-and-white copies.)

Usage:
    python3 tools/covers.py              # book "ai": only new or changed pictures
    python3 tools/covers.py --all        # remake every copy
    python3 tools/covers.py --check      # only report what would change

The reader and the print page load small copies of the pictures, set in books.json:
`storyArt` (for example ai/story-cover/web/{n}.jpg; with `storyArtAt: "end"` the picture
follows the story instead of facing its start, and `storyArtOffset` lets a later volume go on
numbering in a shared folder, as bad/characters does) and `partArt`
(ai/section-cover/web/s{n}.jpg). Originals live one folder up (ai/story-cover/1.jpeg,
ai/section-cover/s1.jpeg) and can be jpg, jpeg, png or webp.

For each original this writes, when the copy is missing or the original's contents changed
(checked by fingerprint, not by file date, since a file copied in from Finder keeps its old date):
- web/<name>.jpg: color, 1200 px tall, loaded by the reader and the print page.
The front cover (books.json `cover`, for example ai/book-cover/web/cover.jpg) is copied from
front.* one folder up (or cover.*, or the only picture there), COVER_HEIGHT px tall. The back
cover (books.json `backCover`, ai/book-cover/web/back.jpg) is copied from back.* the same way,
and the spine background (`sideCover`, web/side.jpg) from side.*.
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

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
EXTS = {".jpg", ".jpeg", ".png", ".webp"}
HEIGHT = 1200
COVER_HEIGHT = 2600  # full size: the reader can save the cover for print (A5 at 300 dpi is 2480 px tall)
QUALITY = 80


def manuscript_counts(book):
    """Number of stories and of parts (sections) in the book's naskah.md."""
    text = (ROOT / book["manuscript"]).read_text(encoding="utf-8")
    stories = len(re.findall(r"^##\s+\d+\.\s", text, re.M))
    parts = len(re.findall(r"^#\s+(?:Bagian\b|Epilog\b)", text, re.M))
    return stories, parts


def save_copy(src, dest):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
    if im.height > HEIGHT:
        im = im.resize((round(im.width * HEIGHT / im.height), HEIGHT), Image.LANCZOS)
    dest.parent.mkdir(exist_ok=True)
    im.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)


def fingerprint(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()[:12]


def sync(label, pattern, expected, rebuild, check):
    """pattern is the books.json value, e.g. ai/section-cover/web/s{n}.jpg."""
    web = ROOT / Path(pattern).parent
    src_dir = web.parent
    prefix, suffix = Path(pattern).name.split("{n}")
    stem_re = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    if not src_dir.is_dir():
        print(f"{label}: no folder {src_dir.relative_to(ROOT)}")
        return 0

    # What each copy was last made from: {copy name: {"src": fingerprint}}.
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
        index[name] = {"src": fp}
        if not dest:
            continue
        made += 1
        print(f"  {'would update' if check else 'update'} {src.relative_to(ROOT)}")
        if not check:
            save_copy(src, dest)

    # Copies whose original was removed or renamed.
    for folder in (web,):
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

    wanted = set(range(1, expected + 1)) if isinstance(expected, int) else set(expected)
    missing = sorted(n for n in wanted if n not in found)
    extra = sorted(n for n in found if n not in wanted)
    if missing:
        print(f"  warning: no picture for {label} {', '.join(map(str, missing))}")
    if extra:
        print(f"  warning: pictures {', '.join(map(str, extra))} have no {label} in naskah.md")
    print(f"{label}: {len(found)} pictures, {made} {'to update' if check else 'updated'}")
    return made


def sync_cover(pattern, names, label, rebuild, check):
    """A cover picture: the first of `names` (front, cover / back) found in the folder above
    web/, or the only picture there, copied to the books.json path at COVER_HEIGHT px tall."""
    web = ROOT / Path(pattern).parent
    src_dir = web.parent
    dest = ROOT / pattern
    pics = [p for p in src_dir.iterdir() if p.is_file() and p.suffix.lower() in EXTS] if src_dir.is_dir() else []
    # the first name that has a picture; if several share it (back.png, back.jpeg), the newest
    named = next((sorted((p for p in pics if p.stem.lower() == n), key=lambda p: p.stat().st_mtime, reverse=True) for n in names if any(p.stem.lower() == n for p in pics)), [])
    src = named[0] if named else (pics[0] if len(pics) == 1 else None)
    if not src:
        print(f"{label}: no {' or '.join(n + '.jpeg' for n in names)} in {src_dir.relative_to(ROOT)}")
        return 0
    index_file = web / "index.json"
    try:
        index = json.loads(index_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        index = {}
    fp = fingerprint(src)
    if not rebuild and index.get(dest.name, {}).get("src") == fp and dest.exists():
        print(f"{label}: up to date")
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
    print(f"{label}: {'to update' if check else 'updated'}")
    return 1


def sync_cutout(art, rebuild, check):
    """The figure on the spine (books.json `spineArt`, {"from": original, "to": web/<name>.png}):
    the original's plain white background, flood-filled from the corners, becomes see-through,
    and the copy is cropped to the figure, HEIGHT px tall, as a PNG."""
    src, dest = ROOT / art["from"], ROOT / art["to"]
    if not src.exists():
        print(f"spine figure: no {art['from']}")
        return 0
    web = dest.parent
    index_file = web / "index.json"
    try:
        index = json.loads(index_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        index = {}
    fp = fingerprint(src)
    if not rebuild and index.get(dest.name, {}).get("src") == fp and dest.exists():
        print("spine figure: up to date")
        return 0
    print(f"  {'would update' if check else 'update'} {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
    if not check:
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
        w, h = im.size
        seed = im.convert("L").point(lambda v: 255 if v > 232 else 0)
        for pt in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
            if seed.getpixel(pt) == 255:
                ImageDraw.floodfill(seed, pt, 128, thresh=0)
        alpha = ImageChops.invert(seed.point(lambda v: 255 if v == 128 else 0)).filter(ImageFilter.GaussianBlur(1.2))
        out = im.convert("RGBA")
        out.putalpha(alpha)
        out = out.crop(alpha.point(lambda v: 255 if v > 20 else 0).getbbox())
        if out.height > HEIGHT:
            out = out.resize((round(out.width * HEIGHT / out.height), HEIGHT), Image.LANCZOS)
        web.mkdir(exist_ok=True)
        out.save(dest, "PNG", optimize=True)
        index[dest.name] = {"src": fp}
        index_file.write_text(json.dumps(dict(sorted(index.items())), indent=1) + "\n", encoding="utf-8")
    print(f"spine figure: {'to update' if check else 'updated'}")
    return 1


def sync_front(art, rebuild, check):
    """Each part's contents page has a picture too (books.json `contentsArt`, for example
ai/section-art/web/{n}.jpg from ai/section-art/1.jpeg, numbered like the parts).
Front-matter pictures (books.json `frontArt`, title -> web/<name>.jpg): each is copied
    from the picture of the same name one folder up (ai/front-art/siti.jpeg -> web/siti.jpg),
    HEIGHT px tall."""
    made = 0
    for title, pattern in art.items():
        dest = ROOT / pattern
        web = dest.parent
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
            save_copy(srcs[0], dest)
            index[dest.name] = {"src": fp}
            index_file.write_text(json.dumps(dict(sorted(index.items())), indent=1) + "\n", encoding="utf-8")
    print(f"front: {len(art)} pictures, {made} {'to update' if check else 'updated'}")
    return made


def main():
    parser = argparse.ArgumentParser(description="Update the color and black-and-white copies of story and section pictures.")
    parser.add_argument("--book", default="ai", help="book id from books.json (default: ai)")
    parser.add_argument("--all", action="store_true", help="remake every copy, not only changed ones")
    parser.add_argument("--check", action="store_true", help="only report what would change")
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
        # Volumes of one book can share a picture folder, numbered on across volumes
        # (storyArtOffset: Jilid 2's story 1 is picture 18). Expect every volume's pictures.
        wanted = set()
        for b in catalog:
            if b.get("storyArt") == book["storyArt"]:
                off = b.get("storyArtOffset", 0)
                wanted |= set(range(off + 1, off + manuscript_counts(b)[0] + 1))
        sync("story", book["storyArt"], wanted, args.all, args.check)
    if book.get("partArt"):
        sync("section", book["partArt"], parts, args.all, args.check)
    if book.get("contentsArt"):
        sync("contents", book["contentsArt"], parts, args.all, args.check)
    if book.get("frontArt"):
        sync_front(book["frontArt"], args.all, args.check)
    if has_cover:
        sync_cover(cover, ("front", "cover"), "cover", args.all, args.check)
    if book.get("backCover"):
        sync_cover(book["backCover"], ("back",), "back cover", args.all, args.check)
    if book.get("sideCover"):
        sync_cover(book["sideCover"], ("side",), "spine", args.all, args.check)
    if book.get("spineArt"):
        sync_cutout(book["spineArt"], args.all, args.check)


if __name__ == "__main__":
    main()
