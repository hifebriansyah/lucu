// Shared loader: reads books.json and turns a book's naskah.md into typed sections.
// A section is the text between two page-break markers in naskah.md.

const PAGE_BREAK = /<div style="page-break-after: always;"><\/div>/g;

export async function loadCatalog() {
  const res = await fetch("books.json", { cache: "no-store" });
  return res.json();
}

export async function loadBook(id) {
  const catalog = await loadCatalog();
  const book = catalog.find((b) => b.id === id) || catalog[0];
  const res = await fetch(book.manuscript, { cache: "no-store" });
  if (!res.ok) {
    return { book, sections: [], missing: true };
  }
  const md = await res.text();
  return { book, sections: parseSections(md), missing: false };
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
    if (index === 0) {
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
  const img = withImage
    ? `<img class="cover-img" src="${book.cover}" alt="" onerror="this.remove()">`
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
