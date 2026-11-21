import { loadBook, coverMarkup } from "./book.js";
import { paginate, pageElement, blankPage } from "./paginate.js";

const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);
const bookId = params.get("book") || "ai";

const { book, sections, missing } = await loadBook(bookId);
document.title = `${book.title} · Pembaca`;
$("printLink").href = `print.html?book=${book.id}`;

if (missing) {
  $("loading").textContent = "Naskah buku ini belum tersedia.";
  throw new Error("missing manuscript");
}

/* ---------- Pagination ---------- */

// The same engine lays out the print PDF, so every page here is a page of the book.
const interior = await paginate(sections, $("measure"), { bookTitle: book.title });

// Screen order: the cover on its own, then the inside of the cover, so page 1 opens
// on the right as in the printed book. Interior page n sits at index n + 1.
const hasCover = await fetch(book.cover, { method: "HEAD" }).then((r) => r.ok).catch(() => false);
if (hasCover) await new Promise((r) => { const img = new Image(); img.onload = img.onerror = r; img.src = book.cover; });
const pages = [
  { kind: "cover-page", html: coverMarkup(book, { withImage: hasCover }) },
  { kind: "blank", html: "" },
  ...interior,
];
for (const s of sections) if (s.page !== undefined) s.page += 1;
if (pages.length % 2 === 0) pages.push({ kind: "blank", html: "" }); // even out the last spread

/* ---------- Rendering ---------- */

function buildPage(i) {
  const data = pages[i];
  if (data && data.kind === "cover-page") {
    const el = blankPage("cover-page");
    el.innerHTML = `<div class="body">${data.html}</div>`;
    return el;
  }
  return pageElement(data);
}

const cache = pages.map((_, i) => buildPage(i));
const blankEl = blankPage("blank");
const pageEl = (i) => (cache[i] || blankEl).cloneNode(true);

const left = $("left"), right = $("right"), bookEl = $("book"), frame = $("frame"), stage = $("stage");
let single = false;
let pos = Math.min(parseInt((location.hash.match(/p=(\d+)/) || [])[1] || "0", 10), pages.length - 1);
let busy = false;

const spreadOf = (p) => Math.floor((p + 1) / 2);
const lastSpread = () => spreadOf(pages.length - 1);

function fill(slot, i) {
  if (slot.dataset.idx === String(i)) return;
  slot.dataset.idx = String(i);
  slot.replaceChildren();
  slot.classList.toggle("empty", i < 0 || i >= pages.length);
  if (i >= 0 && i < pages.length) slot.append(pageEl(i));
}

function render() {
  if (single) {
    fill(right, pos);
  } else {
    const s = spreadOf(pos);
    fill(left, 2 * s - 1);
    fill(right, 2 * s);
  }
  const atStart = single ? pos === 0 : spreadOf(pos) === 0;
  const atEnd = single ? pos === pages.length - 1 : spreadOf(pos) === lastSpread();
  $("prev").disabled = atStart;
  $("next").disabled = atEnd;
  $("folio").textContent = pos < 2 ? "Sampul" : `${pos - 1} / ${interior.length}`;
  history.replaceState(null, "", `#p=${pos}`);
  syncToc();
}

function layout() {
  single = window.innerWidth < 900;
  document.body.classList.toggle("single", single);
  const mm = 96 / 25.4, pw = 148 * mm, ph = 210 * mm, bw = single ? pw : pw * 2; // A5, as printed
  const pad = window.innerWidth < 600 ? 24 : 120;
  const scale = Math.min((stage.clientWidth - pad) / bw, (stage.clientHeight - 32) / ph, 1.25);
  bookEl.style.transform = `scale(${scale})`;
  frame.style.width = `${bw * scale}px`;
  frame.style.height = `${ph * scale}px`;
  render();
}

/* ---------- Page turn ---------- */

function turn(dir) {
  if (busy) return;
  const s = spreadOf(pos);
  if (single ? (dir > 0 ? pos >= pages.length - 1 : pos <= 0) : (dir > 0 ? s >= lastSpread() : s <= 0)) return;
  busy = true;

  const leaf = document.createElement("div");
  const front = document.createElement("div");
  const back = document.createElement("div");
  front.className = "face front";
  back.className = "face back";
  leaf.append(front, back);

  let target, angle;
  if (single) {
    target = pos + dir;
    leaf.className = "leaf from-right";
    if (dir > 0) {
      front.append(pageEl(pos));
      back.append(blankPage("blank"));
      fill(right, target);
      angle = -180;
    } else {
      front.append(pageEl(target));
      back.append(blankPage("blank"));
      leaf.style.transition = "none";
      leaf.style.transform = "rotateY(-180deg)";
      angle = 0;
    }
  } else if (dir > 0) {
    target = 2 * (s + 1) - 1;
    leaf.className = "leaf from-right";
    front.append(pageEl(2 * s));
    back.append(pageEl(2 * (s + 1) - 1));
    fill(right, 2 * (s + 1));
    angle = -180;
  } else {
    target = 2 * (s - 1);
    leaf.className = "leaf from-left";
    front.append(pageEl(2 * s - 1));
    back.append(pageEl(2 * (s - 1)));
    fill(left, 2 * (s - 1) - 1);
    angle = 180;
  }

  const cast = document.createElement("div");
  cast.className = `cast ${!single && dir < 0 ? "on-left" : "on-right"}`;
  bookEl.append(cast, leaf);
  requestAnimationFrame(() => requestAnimationFrame(() => {
    leaf.style.transition = "";
    cast.classList.add("turning");
    leaf.classList.add("turning");
    leaf.style.transform = `rotateY(${angle}deg)`;
  }));

  let finished = false;
  const done = () => {
    if (finished) return;
    finished = true;
    pos = Math.max(0, Math.min(target, pages.length - 1));
    render(); // fills the slot the leaf now covers, while the leaf is still on top
    requestAnimationFrame(() => { leaf.remove(); cast.remove(); busy = false; });
  };
  leaf.addEventListener("transitionend", (e) => {
    if (e.target === leaf && e.propertyName === "transform") done();
  });
  setTimeout(done, 1100);
}

function jump(p) {
  pos = Math.max(0, Math.min(p, pages.length - 1));
  render();
}

/* ---------- Table of contents ---------- */

const toc = $("toc");
function buildToc() {
  const opt = (label, value) => Object.assign(document.createElement("option"), { textContent: label, value });
  toc.append(opt("Sampul", 0));
  let group = null;
  for (const s of sections) {
    if (s.page === undefined) continue;
    if (s.type === "part") {
      group = Object.assign(document.createElement("optgroup"), { label: s.title });
      toc.append(group);
      group.append(opt(s.title, s.page));
    } else {
      (s.type === "story" && group ? group : toc).append(opt(s.title, s.page));
    }
  }
}
function syncToc() {
  let best = 0;
  for (const o of toc.options) if (+o.value <= pos) best = Math.max(best, +o.value);
  toc.value = String(best);
}
toc.addEventListener("change", () => jump(+toc.value));

/* ---------- Input ---------- */

$("next").addEventListener("click", () => turn(1));
$("prev").addEventListener("click", () => turn(-1));
document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") { e.preventDefault(); turn(1); }
  if (e.key === "ArrowLeft" || e.key === "PageUp") { e.preventDefault(); turn(-1); }
});
let touchX = null;
stage.addEventListener("touchstart", (e) => (touchX = e.touches[0].clientX), { passive: true });
stage.addEventListener("touchend", (e) => {
  if (touchX === null) return;
  const dx = e.changedTouches[0].clientX - touchX;
  if (Math.abs(dx) > 40) turn(dx < 0 ? 1 : -1);
  touchX = null;
});
window.addEventListener("resize", layout);

buildToc();
layout();
lucide.createIcons();
$("loading").classList.add("done");
