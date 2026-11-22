// Shared loader: reads books.json and turns a book's naskah.md into typed sections.
// A section is the text between two page-break markers in naskah.md.

const PAGE_BREAK = /<div style="page-break-after: always;"><\/div>/g;

export async function loadCatalog() {
  const res = await fetch("books.json", { cache: "no-store" });
  const books = await res.json();
  // A cover made by tools/covers.py (in a web/ folder) gets its fingerprint, so a new cover shows at once.
  await Promise.all(books.map(async (b) => {
    if (b.cover?.includes("/web/")) b.cover = (await versioned(b.cover))();
  }));
  return books;
}

export async function loadBook(id) {
  const catalog = await loadCatalog();
  const book = catalog.find((b) => b.id === id) || catalog[0];
  const res = await fetch(book.manuscript, { cache: "no-store" });
  if (!res.ok) {
    return { book, sections: [], missing: true };
  }
  const md = await res.text();
  const sections = parseSections(md);
  if (book.storyArt) addStoryArt(sections, await versioned(book.storyArt));
  if (book.partArt) addPartArt(sections, await versioned(book.partArt));
  return { book, sections, missing: false };
}

// tools/covers.py writes index.json next to the picture copies with a fingerprint per
// picture. Adding it to the address means a replaced picture is never shown from cache.
async function versioned(pattern) {
  const dir = pattern.slice(0, pattern.lastIndexOf("/") + 1);
  let index = {};
  try { index = await (await fetch(`${dir}index.json`, { cache: "no-store" })).json(); } catch {}
  return (n) => {
    const src = pattern.replace("{n}", n);
    const v = index[src.slice(dir.length)]?.src;
    return v ? `${src}?v=${v}` : src;
  };
}

// A picture on each part page, numbered by the part's order (s1 = Bagian Satu, ..., the last = Epilog).
// The title becomes a poster-style heading on the picture: "Bagian Satu: Jam Kerja" shows
// BAGIAN SATU big with JAM KERJA under it. A part with no subtitle (the Epilog) shows its name only.
function addPartArt(sections, pattern) {
  let n = 0;
  sections.forEach((s) => {
    if (s.type !== "part") return;
    const src = pattern(++n);
    const [main, sub = ""] = s.title.split(/:\s*/);
    const size = main.length <= 8 ? "big" : "";
    s.html = `<h1 class="poster ${size}"><span class="main">${main}</span>${sub ? `<span class="sub">${sub}</span>` : ""}</h1>`
      + `<figure class="part-art"><img src="${src}" alt="" onerror="this.parentElement.remove()"></figure>`;
  });
}

// A picture for each story. paginate.js puts it on the right-hand page facing the story.
function addStoryArt(sections, pattern) {
  for (const s of sections) {
    if (s.type === "story") s.art = pattern(s.title.match(/^\d+/)[0]);
  }
}

export function parseSections(md) {
  const raw = md.split(PAGE_BREAK).map((s) => s.trim()).filter(Boolean);
  return raw.map((text, index) => {
    const html = window.marked.parse(text, { breaks: true });
    let type = "front";
    let title = "";
    const story = text.match(/^##\s+(\d+)\.\s+(.+)$/m);
    const part = text.match(/^#\s+(.+)$/m);
    const heading = text.match(/^##\s+(.+)$/m);
    const image = text.match(/^!\[[^\]]*\]\(([^)]+)\)$/);
    if (image) {
      type = "image";
      title = (text.match(/^!\[([^\]]*)\]/) || [])[1] || "";
    } else if (index === 0) {
      type = "title";
      title = part ? part[1] : "";
    } else if (story && text.trim().startsWith("##")) {
      type = "story";
      title = `${story[1]}. ${story[2].trim()}`;
    } else if (part && text.trim().split("\n").length <= 2) {
      type = "part";
      title = part[1].trim();
    } else if (heading) {
      type = heading[1].trim() === "Daftar Isi" ? "toc" : "front";
      title = heading[1].trim();
    } else {
      type = "dedication";
    }
    return { index, type, title, html, text };
  });
}

export function coverMarkup(book, { withImage = true } = {}) {
  // coverText: the cover picture has no lettering, so the title is set over it, in the
  // same Orbitron poster style as the part pages ("A, B" puts B on its own, bigger line).
  const [lead, rest] = book.title.includes(",") ? book.title.split(/,\s*/) : ["", book.title];
  const over = book.coverText
    ? `<div class="cover-over"><span class="kicker">${book.kicker || ""}</span>`
      + `<h1 class="title">${lead ? `<span class="lead">${lead},</span>` : ""}<span class="main">${rest}</span></h1>`
      + `<p class="sub">${book.subtitle}</p></div>`
    : "";
  const img = withImage
    ? `<img class="cover-img" src="${book.cover}" alt="" onerror="this.remove()">${over}`
    : "";
  return `
    <div class="cover" style="--cover:${book.color}">
      <div class="cover-art">
        <span class="cover-kicker">${book.kicker || ""}</span>
        <h1 class="cover-title">${book.title}</h1>
        <p class="cover-sub">${book.subtitle}</p>
        <span class="cover-note">Sampul sementara</span>
      </div>
      ${img}
    </div>`;
}
