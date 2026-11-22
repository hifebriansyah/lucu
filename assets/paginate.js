// One page-breaking engine for both the reader and the print PDF, so what you see
// on screen is exactly what gets printed. Pages are real A5 sheets (pages.css):
// print uses them at full size, the reader scales them to fit the window.
//
// Returns the interior pages (no cover). Page n is pages[n - 1]; odd pages are
// right-hand pages, as in a printed book.

const FONTS = ["400 11pt Literata", "italic 400 11pt Literata", "700 11pt Literata", "700 16pt Literata", "500 9pt Inter", "900 33pt Orbitron", "600 19pt Orbitron"];

export function blankPage(kind) {
  const el = document.createElement("div");
  el.className = `page ${kind}`;
  el.innerHTML = `<div class="head"></div><div class="body"></div><div class="foot"></div>`;
  return el;
}

const NO_FOLIO = new Set(["title", "part", "dedication", "blank", "image"]);

// Builds the element for one interior page: left or right side, running head
// (book title on the left, story title on the right) and page number.
export function pageElement(data) {
  const el = blankPage(data ? data.kind : "blank");
  if (!data) return el;
  el.classList.add(data.number % 2 ? "right" : "left");
  el.querySelector(".body").innerHTML = data.html;
  if (!NO_FOLIO.has(data.kind)) el.querySelector(".foot").textContent = data.number;
  if (data.kind === "story" && !data.first) el.querySelector(".head").textContent = data.number % 2 ? data.story : data.bookTitle;
  return el;
}

const overflows = (body) => body.scrollHeight > body.clientHeight + 1;

// Contents entries get a page-number slot before layout, sized for three digits,
// so filling in the real numbers afterwards cannot change the line breaks.
function addTocSlots(html) {
  const holder = document.createElement("div");
  holder.innerHTML = html;
  const entries = [...holder.querySelectorAll("li")];
  for (const p of holder.querySelectorAll("p")) {
    if (p.childElementCount === 1 && p.firstElementChild.tagName === "STRONG" && p.textContent.trim() === p.firstElementChild.textContent.trim()) entries.push(p);
  }
  for (const e of entries) e.insertAdjacentHTML("afterbegin", `<span class="pg">000</span>`);
  return holder.innerHTML;
}

export async function paginate(sections, measure, { bookTitle = "" } = {}) {
  // Measure with the real book font, or the page breaks drift once it loads.
  await Promise.all(FONTS.map((f) => document.fonts.load(f).catch(() => {})));

  const pages = [];
  const push = (kind, html, story = "") => pages.push({ kind, html, story, bookTitle, number: pages.length + 1 });
  // Start on a right-hand (odd) page.
  const startOnRight = () => { if (pages.length % 2 === 1) push("blank", ""); };
  const startOnLeft = () => { if (pages.length % 2 === 0) push("blank", ""); };

  function flow(kind, html, story) {
    const holder = document.createElement("div");
    holder.innerHTML = html;
    const blocks = [...holder.children];
    let page = blankPage(kind);
    measure.replaceChildren(page);
    let body = page.querySelector(".body");

    const flush = () => {
      if (body.childElementCount) push(kind, body.innerHTML, story);
      page = blankPage(kind);
      measure.replaceChildren(page);
      body = page.querySelector(".body");
    };

    for (const block of blocks) {
      body.append(block);
      if (!overflows(body)) continue;
      block.remove();
      // Lists can continue across pages, so fill the rest of this page first.
      const isList = block.tagName === "OL" || block.tagName === "UL";
      if (body.childElementCount && !isList) {
        flush();
        body.append(block);
        if (!overflows(body)) continue;
        block.remove();
      }
      // A single block taller than a page (a long paragraph, or the contents list):
      // move its pieces one by one into copies of the block, starting a new page
      // whenever the current one is full.
      let shell = block.cloneNode(false);
      body.append(shell);
      const pieces = [...block.childNodes].flatMap((n) =>
        n.nodeType === Node.TEXT_NODE ? n.textContent.split(/(?<=\s)/).map((t) => document.createTextNode(t)) : [n]);
      for (const piece of pieces) {
        shell.append(piece);
        if (!overflows(body)) continue;
        piece.remove();
        if (piece.nodeName === "BR") continue; // a line break at the page end is not needed
        const prev = shell;
        flush();
        shell = block.cloneNode(false);
        if (shell.tagName === "OL") {
          shell.start = (prev.start || 1) + prev.children.length; // keep numbering going
        }
        body.append(shell);
        if (piece.nodeType === Node.TEXT_NODE && !piece.textContent.trim()) continue;
        shell.append(piece);
      }
      // drop a leading line break left at the top of a continued block
      while (shell.firstChild && shell.firstChild.nodeName === "BR") shell.firstChild.remove();
    }
    flush();
  }

  for (const s of sections) {
    if (s.type === "title") { startOnRight(); s.page = pages.length + 1; push("title", s.html); }
    else if (s.type === "part") { startOnRight(); s.page = pages.length + 1; push("part", s.html, s.title); }
    else if (s.type === "dedication") { s.page = pages.length + 1; push("dedication", s.html); }
    // Coloring pages sit on a right-hand page with a blank back, so colors don't bleed through.
    else if (s.type === "image") { startOnRight(); s.page = pages.length + 1; push("image", s.html, s.title); push("blank", ""); }
    else if (s.type === "story" && s.art) {
      // Illustrated story: text starts on a left-hand page, its picture fills the right-hand
      // page facing it. A longer story continues on the next left-hand page.
      startOnLeft();
      s.page = pages.length + 1;
      flow("story", s.html, s.title);
      pages[s.page - 1].first = true;
      pages.splice(s.page, 0, { kind: "art", html: `<img src="${s.art}" alt="">`, story: s.title, bookTitle });
      pages.forEach((p, i) => { p.number = i + 1; });
    }
    else if (s.type === "story") { s.page = pages.length + 1; flow("story", s.html, s.title); pages[s.page - 1].first = true; }
    else if (s.type === "toc") { s.page = pages.length + 1; flow("toc", addTocSlots(s.html), s.title); }
    else { s.page = pages.length + 1; flow("front", s.html, s.title); }
  }
  measure.replaceChildren();

  fillTocNumbers(pages, sections);
  return pages;
}

// Put each section's real page number into its contents entry.
function fillTocNumbers(pages, sections) {
  const where = new Map();
  for (const s of sections) {
    if (!s.title || s.page === undefined) continue;
    where.set(s.title, s.page);
    const m = s.title.match(/^\d+\.\s+(.+)$/);
    if (m) where.set(m[1], s.page);
  }
  for (const page of pages) {
    if (page.kind !== "toc") continue;
    const holder = document.createElement("div");
    holder.innerHTML = page.html;
    for (const slot of holder.querySelectorAll(".pg")) {
      const entry = slot.parentElement;
      const text = entry.textContent.replace(slot.textContent, "").trim();
      const n = where.get(text);
      if (n === undefined) slot.remove();
      else slot.textContent = n;
    }
    page.html = holder.innerHTML;
  }
}
