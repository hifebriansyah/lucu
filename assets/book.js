// Shared loader: reads books.json and turns a book's naskah.md into typed sections.
// A section is the text between two page-break markers in naskah.md.

import { triadLevels, triadSvg } from "./triad.js";

const PAGE_BREAK = /<div style="page-break-after: always;"><\/div>/g;

export async function loadCatalog() {
  const res = await fetch("books.json", { cache: "no-store" });
  const books = await res.json();
  // A cover made by tools/covers.py (in a web/ folder) gets its fingerprint, so a new cover shows at once.
  await Promise.all(books.map(async (b) => {
    if (b.cover?.includes("/web/")) b.cover = (await versioned(b.cover))();
    if (b.backCover) b.backCover = (await versioned(b.backCover))();
    if (b.sideCover) b.sideCover = (await versioned(b.sideCover))();
    if (b.uvArt) b.uvArt = (await versioned(b.uvArt))();
    if (b.spineArt) b.spineArt = (await versioned(b.spineArt.to))();
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
  // The title page sets the title like the cover: coverTitle's small and big lines.
  const titlePage = sections.find((s) => s.type === "title");
  if (titlePage && book.coverTitle) {
    const [lead, main] = book.coverTitle;
    titlePage.html = titlePage.html.replace(/<h1[^>]*>[\s\S]*?<\/h1>/, `<h1 class="poster-title"><span class="lead">${lead}</span><span class="main">${main}</span></h1>`);
  }
  // Book 3: each story's profile page (name, Dark Triad chart, biodata, quote) facing its picture.
  if (book.triadChart) for (const s of sections) if (s.type === "story") addProfile(s);
  if (book.storyArt) addStoryArt(sections, await versioned(book.storyArt), book);
  if (book.partArt) addPartArt(sections, await versioned(book.partArt));
  if (book.contentsArt) {
    const art = await versioned(book.contentsArt);
    sections.filter((s) => s.type === "part").forEach((s, i) => {
      s.contentsArt = art(i + 1);
      s.contentsTrivia = (book.contentsTrivia || [])[i] || ""; // a line of trivia under the picture
    });
  }
  for (const [title, src] of Object.entries(book.frontArt || {})) {
    const s = sections.find((x) => x.type === "front" && x.title === title);
    if (s) s.art = (await versioned(src))();
  }
  return { book, sections, missing: false };
}

// tools/covers.py writes index.json next to the picture copies with a fingerprint per
// picture. Adding it to the address means a replaced picture is never shown from cache.
async function versioned(pattern) {
  const dir = pattern.slice(0, pattern.lastIndexOf("/") + 1);
  let index = {};
  try { index = await (await fetch(`${dir}index.json`, { cache: "no-store" })).json(); } catch {}
  const art = (n) => {
    const src = pattern.replace("{n}", n);
    const v = index[src.slice(dir.length)]?.src;
    return v ? `${src}?v=${v}` : src;
  };
  // Whether the copy exists: index.json lists every copy; without one, assume it does.
  art.has = (n) => !Object.keys(index).length || !!index[pattern.replace("{n}", n).slice(dir.length)];
  return art;
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

// frontArt (books.json) gives a front-matter section, by its heading, a picture page facing it,
// laid out like a story's.

// Book 3: a story's closing "### Profil" section (**Nama:**, **Lahir:**, **Wafat:**,
// **Jenis kelamin:**, **Negara:** lines, then a > quote) becomes its own page, s.profile: the name,
// the triangle chart of the Dark Triad levels from the analysis, the biodata card and the quote.
// paginate.js puts it on a left-hand page, facing the story's picture. A story with no Profil
// section keeps the chart at its end.
function addProfile(s) {
  const levels = triadLevels(s.text);
  const chart = levels ? `<figure class="triad">${triadSvg(levels)}</figure>` : "";
  const m = s.html.match(/<h3[^>]*>Profil<\/h3>/);
  if (!m) { s.html += chart; return; }
  const holder = document.createElement("div");
  holder.innerHTML = profileCards(s.html.slice(m.index + m[0].length));
  let name = s.title.replace(/^\d+\.\s*/, "");
  const dl = holder.querySelector("dl.profile");
  const nama = dl && [...dl.querySelectorAll("dt")].find((dt) => dt.textContent.trim() === "Nama");
  if (nama) { name = nama.nextElementSibling.innerHTML; nama.nextElementSibling.remove(); nama.remove(); }
  // The quote's "— source" line becomes its own small line under the quote.
  for (const p of holder.querySelectorAll("blockquote p")) {
    const [quote, ...cite] = p.innerHTML.split(/<br\s*\/?>\s*(?=—)/);
    if (cite.length) p.outerHTML = `<p>${quote}</p><p class="cite">${cite.join("")}</p>`;
  }
  s.html = s.html.slice(0, m.index);
  s.profile = `<h2 class="profile-name">${name}</h2>${chart}${holder.innerHTML}`;
}

// A picture for each story. paginate.js puts it on the right-hand page facing the story, or,
// with storyArtAt "end", on the page after the story's last one. storyArtOffset continues the
// numbering of a shared picture folder in a later volume. A story with no picture gets none.
function addStoryArt(sections, pattern, book = {}) {
  const offset = book.storyArtOffset || 0;
  for (const s of sections) {
    if (s.type !== "story") continue;
    const n = Number(s.title.match(/^\d+/)[0]) + offset;
    if (!pattern.has(n)) continue;
    s.art = pattern(n);
    if (book.storyArtAt === "end") s.artEnd = true;
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
    } else if (/ISBN|Hak cipta/i.test(text)) {
      type = "copyright"; // the imprint page: publisher, ISBN, rights
    } else {
      type = "dedication";
    }
    const shaped = type === "front" ? profileCards(html) : type === "dedication" ? chatBubble(html) : html;
    return { index, type, title, html: shaped, text };
  });
}

// A dedication that ends on a quoted question ("Yakin?") shows the question as a sent chat
// message under the verse, and any chat lines after it as more bubbles (pages.css .bubble).
function chatBubble(html) {
  const q = '(?:"|&quot;|&#34;|\u201c|\u201d)';
  const holder = document.createElement("div");
  holder.innerHTML = html;
  const paras = [...holder.querySelectorAll(":scope > p")];
  // The verse's closing quoted question becomes the first sent message.
  const verse = paras[0];
  if (verse) verse.outerHTML = verse.outerHTML.replace(new RegExp(`,?\\s*${q}([^"<&\u201d]+)${q}\\s*</em>\\s*</p>\\s*$`), ',</em></p><p class="bubble">$1</p>');
  // Then a chat: *SITI: "..."* is SITI's reply, a lone *"..."* is the reader's next message.
  for (const p of paras.slice(1)) {
    const m = p.textContent.trim().match(new RegExp(`^(SITI:\\s*)?["\u201c](.+?)["\u201d]$`));
    if (m) p.outerHTML = `<p class="bubble${m[1] ? " in" : ""}">${m[2]}</p>`;
  }
  return holder.innerHTML;
}

// A front-matter paragraph made only of "**Label:** value" lines (Kenalan dengan SITI) becomes a
// profile card: a two-column list of labels and values (pages.css .profile).
function profileCards(html) {
  const holder = document.createElement("div");
  holder.innerHTML = html;
  for (const p of holder.querySelectorAll("p")) {
    const lines = p.innerHTML.split(/<br\s*\/?>\s*/i).map((l) => l.trim()).filter(Boolean);
    const rows = lines.map((l) => l.match(/^<strong>([^<]+?):?<\/strong>:?\s*(.*)$/s));
    if (lines.length < 2 || rows.some((r) => !r)) continue;
    const dl = document.createElement("dl");
    dl.className = "profile";
    dl.innerHTML = rows.map((r) => `<dt>${r[1]}</dt><dd>${r[2]}</dd>`).join("");
    p.replaceWith(dl);
  }
  return holder.innerHTML;
}

// The back cover: the picture alone, edge to edge.
// backText (books.json) sets text over it: the blurb paragraphs in the middle of the glowing
// circle in the picture (its center is at backCircle, in % of the picture), and the
// kicker at the foot.
export function backCoverMarkup(book) {
  const t = book.backText;
  const [x, y] = book.backCircle || [50, 47];
  const over = t
    ? `<div class="cover-over back-over">`
      + `<div class="orb-text" style="left:${x}%;top:${y}%">${(t.blurb || []).map((p) => `<p>${p}</p>`).join("")}</div>`
      + `<div class="back-foot"><span class="kicker">${book.kicker || ""}</span>`
      + (t.foot ? `<span class="genre">${t.foot}</span>` : "") + `</div></div>`
    : "";
  return `<div class="cover" style="--cover:${book.color}"><img class="cover-img" src="${book.backCover}" alt="">${over}</div>`;
}

// The spine: its width depends on the page count and paper, so this is a full A5 picture
// with the title running top to bottom along its exact center line (spineArt adds a
// head-and-shoulders portrait at the bottom); the printer crops a strip of the
// spine's width around that line.
// The kicker stacked upright, two letters a line, a gap between words: "SITI · M4.KZ-A"
// becomes SI / TI, then M4 / KZ / -A (dots dropped).
function spineKicker(kicker) {
  // One cell per letter in a two-column grid, so the first letters (S T M K _) and the
  // second letters (I I 4 Z A) each line up in a column.
  return kicker.split(/\s*·\s*/)
    .map((w) => w.replace(/\./g, "").match(/.{1,2}/g).map((p) => [...p.padEnd(2)].map((ch) => `<span>${ch.trim()}</span>`).join("")).join(""))
    .join(`<span class="gap"></span>`);
}

export function spineMarkup(book) {
  const title = (book.coverTitle || [book.title]).join(" ");
  return `<div class="cover" style="--cover:${book.color}"><img class="cover-img" src="${book.sideCover}" alt="">`
    + (book.spineArt ? `<div class="spine-figure"><img src="${book.spineArt}" alt=""></div>` : "")
    + (book.kicker ? `<div class="spine-kicker">${spineKicker(book.kicker)}</div>` : "")
    + `<div class="spine-text"><span class="spine-title">${title}</span>`
    + `</div></div>`;
}

// Spot UV mask for the front cover: the same layout, white, with every piece of text, the
// circle (frontRing) and SITI's outline (uvArt, made by tools/uv-mask.py, the size of the cover picture so it lines
// up) in solid black. The printer puts the UV coating where it is black.
export function uvMarkup(book) {
  return coverMarkup(book, { withImage: true })
    .replace('class="cover"', 'class="cover uv-mask"')
    .replace(/<img class="cover-img" src="[^"]*"/, `${ring(book.frontRing)}<img class="cover-img" src="${book.uvArt}"`);
}

// Spot UV mask for the spine: the same layout, white, with the kicker, the title and SITI's
// portrait in solid black.
export function spineUvMarkup(book) {
  return spineMarkup(book).replace('class="cover"', 'class="cover uv-mask"').replace(/<img class="cover-img"[^>]*>/, "");
}

// Spot UV mask for the back cover: the blurb and the kicker in solid black, plus the glowing
// circle as a black ellipse (backRing: center x, center y, width, height, in % of the cover).
// A glowing circle as a black ellipse: [center x, center y, width, height] in % of the cover.
function ring(r) {
  if (!r) return "";
  const [x, y, w, h] = r;
  return `<div class="uv-ring" style="left:${x}%;top:${y}%;width:${w}%;height:${h}%"></div>`;
}

export function backUvMarkup(book) {
  return backCoverMarkup(book).replace('class="cover"', 'class="cover uv-mask"').replace(/<img class="cover-img"[^>]*>/, ring(book.backRing));
}

export function coverMarkup(book, { withImage = true } = {}) {
  // coverText: the cover picture has no lettering, so the title is set over it, in the
  // same Orbitron poster style as the part pages ("A, B" puts B on its own, bigger line).
  // coverTitle ([small line, big line]) overrides the title on the cover only.
  const [lead, rest] = book.coverTitle || (book.title.includes(",") ? book.title.split(/,\s*/).map((t, i) => i ? t : t + ",") : ["", book.title]);
  const over = book.coverText
    ? `<div class="cover-over"><span class="kicker">${book.kicker || ""}</span>`
      + `<h1 class="title">${lead ? `<span class="lead">${lead}</span>` : ""}<span class="main">${rest}</span></h1>`
      + `<p class="sub">${book.subtitle}</p>`
      + (book.author ? `<p class="cover-author">${book.author}</p>` : "") + `</div>`
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
