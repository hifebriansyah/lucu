import { loadBook, coverMarkup, backCoverMarkup, spineMarkup, uvMarkup, spineUvMarkup, backUvMarkup } from "./book.js";
import { paginate, pageElement, blankPage } from "./paginate.js";
import { PAPERS, DEFAULT_PAPER, savedPaper, savePaper, applyPaper, BORDERS, DEFAULT_BORDER, savedBorder, saveBorder, applyBorder, FRAMES, DEFAULT_FRAME, savedFrame, saveFrame, applyFrame, savedBw, saveBw, applyBw } from "./paper.js";

const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);
const bookId = params.get("book") || "ai";

const { book, sections, missing } = await loadBook(bookId);
document.title = `${book.title} · Pembaca`;
$("printLink").href = `print.html?book=${book.id}`;

// Hitam putih: interior pages in black and white, for a grayscale print. Remembered per browser.
const bwBtn = $("bwBtn");
applyBw(savedBw(), bwBtn);
bwBtn.addEventListener("click", () => { const on = !document.body.classList.contains("bw"); applyBw(on, bwBtn); saveBw(on); });

// Paper and picture-border colors and the part-picture shape: try them live, Simpan keeps all (for this book, and
// for the PDF); closing the panel without saving goes back to the saved colors.
const paperBtn = $("paperBtn"), paperPanel = $("paperPanel");
function picker({ list, def, saved, save, apply, swatches, input, onTry }) {
  let kept = saved(book.id) || def, now = kept;
  const set = (color) => {
    now = color.toLowerCase();
    apply(now === def ? null : now);
    $(input).value = now;
    for (const b of $(swatches).children) b.setAttribute("aria-pressed", b.dataset.color === now);
    onTry(now);
  };
  for (const p of list) {
    const b = Object.assign(document.createElement("button"), { type: "button", title: p.name, className: "swatch-btn" });
    b.dataset.color = p.color;
    b.innerHTML = `<span class="swatch" style="background:${p.color}"></span>${p.name}`;
    b.addEventListener("click", () => set(p.color));
    $(swatches).append(b);
  }
  $(input).addEventListener("input", () => set($(input).value));
  set(kept);
  return { reset: () => set(def), revert: () => set(kept), keep: () => { kept = now; save(book.id, kept); } };
}
const paperPick = picker({ list: PAPERS, def: DEFAULT_PAPER, saved: savedPaper, save: savePaper, apply: applyPaper,
  swatches: "paperSwatches", input: "paperInput", onTry: (c) => { $("paperDot").style.background = c; } });
const borderPick = picker({ list: BORDERS, def: DEFAULT_BORDER, saved: savedBorder, save: saveBorder, apply: applyBorder,
  swatches: "borderSwatches", input: "borderInput", onTry: (c) => { $("paperDot").style.boxShadow = `inset 0 0 0 1px rgba(0, 0, 0, .25), 0 0 0 2px ${c}`; } });
// Shape of the picture facing each part picture: one of a few shapes, no custom value.
const framePick = (() => {
  let kept = savedFrame(book.id) || DEFAULT_FRAME, now = kept;
  const set = (v) => {
    now = v;
    applyFrame(v);
    for (const b of $("frameButtons").children) b.setAttribute("aria-pressed", b.dataset.value === v);
  };
  for (const f of FRAMES) {
    const b = Object.assign(document.createElement("button"), { type: "button", title: f.name, className: "swatch-btn" });
    b.dataset.value = f.value;
    b.innerHTML = `<span class="shape-dot" data-shape="${f.value}"></span>${f.name}`;
    b.addEventListener("click", () => set(f.value));
    $("frameButtons").append(b);
  }
  set(kept);
  return { reset: () => set(DEFAULT_FRAME), revert: () => set(kept), keep: () => { kept = now; saveFrame(book.id, kept); } };
})();
function openPaper(open) {
  paperPanel.hidden = !open;
  paperBtn.setAttribute("aria-expanded", open);
  if (!open) { paperPick.revert(); borderPick.revert(); framePick.revert(); } // drop an unsaved try
}
paperBtn.addEventListener("click", () => openPaper(paperPanel.hidden));
$("paperReset").addEventListener("click", () => { paperPick.reset(); borderPick.reset(); framePick.reset(); });
$("paperSave").addEventListener("click", () => { paperPick.keep(); borderPick.keep(); framePick.keep(); openPaper(false); });
document.addEventListener("click", (e) => { if (!paperPanel.hidden && !e.target.closest(".paper-pick")) openPaper(false); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !paperPanel.hidden) openPaper(false); });

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
// The back cover ends the book alone on the left, like the front cover starts it alone on
// the right: a blank page to even out the interior if needed, the inside of the back
// cover, then the back cover.
const hasBack = book.backCover && await fetch(book.backCover, { method: "HEAD" }).then((r) => r.ok).catch(() => false);
let backAt = -1; // screen index of the back cover
if (hasBack) {
  if (pages.length % 2 === 1) pages.push({ kind: "blank", html: "" });
  pages.push({ kind: "blank", html: "" }, { kind: "cover-page", html: backCoverMarkup(book) });
  backAt = pages.length - 1;
  // The spine, right of the back cover as on the closed book seen from behind: a strip from
  // the middle of the spine picture (assets/reader.css .spine-page).
  if (book.sideCover) pages.push({ kind: "cover-page spine-page", html: spineMarkup(book) });
} else if (pages.length % 2 === 0) pages.push({ kind: "blank", html: "" }); // even out the last spread
// The spot UV masks, last, laid out like the covers: the back's mask with the spine's to its
// right, then the front's on its own. Black is coated with UV, white is left plain.
let uvAt = -1, uvBackAt = -1;
if (book.uvArt) {
  if (pages.length % 2 === 0) pages.push({ kind: "blank", html: "" }); // the back's mask opens a spread on the left
  if (hasBack) {
    pages.push({ kind: "cover-page uv-page", html: backUvMarkup(book) });
    uvBackAt = pages.length - 1;
    pages.push(book.sideCover ? { kind: "cover-page spine-page uv-page", html: spineUvMarkup(book) } : { kind: "blank", html: "" });
  }
  pages.push({ kind: "cover-page uv-page", html: uvMarkup(book) });
  uvAt = pages.length - 1;
}

/* ---------- Rendering ---------- */

function buildPage(i) {
  const data = pages[i];
  if (data && data.kind.startsWith("cover-page")) {
    const el = blankPage(data.kind);
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
  $("prev").disabled = $("prevPage").disabled = atStart;
  $("next").disabled = $("nextPage").disabled = atEnd;
  const [first, last] = shown();
  $("prevSec").disabled = !partPages.some((p) => p < first);
  $("nextSec").disabled = !partPages.some((p) => p > last);
  $("folio").textContent = pos < 2 ? "Sampul"
    : uvAt >= 0 && pos === uvAt ? "UV depan"
    : uvBackAt >= 0 && pos === uvBackAt ? "UV belakang"
    : uvBackAt >= 0 && pos === uvBackAt + 1 ? "UV punggung"
    : hasBack && pos > backAt ? "Punggung"
    : hasBack && pos - 1 > interior.length ? "Sampul belakang"
    : `${pos - 1} / ${interior.length}`;
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

// Screen indexes of the pages now in view (one page, or the two of a spread).
function shown() {
  if (single) return [pos, pos];
  const sp = spreadOf(pos);
  return [Math.max(0, 2 * sp - 1), 2 * sp];
}

// Section opening pages, in screen indexes: every part and every titled page outside the
// stories (Daftar Isi, Kata Pengantar, Kenalan dengan SITI, Penutup, Tentang Penulis), then
// the back cover. » goes to the next one after the pages in view, « to the start of the
// current section, or the one before if already at its start.
const partPages = sections
  .filter((s) => s.page !== undefined && (s.type === "part" || ((s.type === "front" || s.type === "toc") && s.title)))
  .map((s) => s.page)
  .concat(hasBack ? [backAt] : [])
  .sort((a, b) => a - b);
function jumpSection(dir) {
  const [first, last] = shown();
  const target = dir > 0 ? partPages.find((p) => p > last) : partPages.filter((p) => p < first).pop();
  if (target !== undefined) jump(target);
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
  if (hasBack) toc.append(opt("Sampul belakang", backAt));
  if (book.sideCover && backAt >= 0) toc.append(opt("Punggung", backAt + 1));
  if (uvBackAt >= 0) toc.append(opt("UV spot (sampul belakang)", uvBackAt));
  if (uvBackAt >= 0 && book.sideCover) toc.append(opt("UV spot (punggung)", uvBackAt + 1));
  if (uvAt >= 0) toc.append(opt("UV spot (sampul depan)", uvAt));
}
function syncToc() {
  let best = 0;
  for (const o of toc.options) if (+o.value <= pos) best = Math.max(best, +o.value);
  toc.value = String(best);
}
toc.addEventListener("change", () => jump(+toc.value));

/* ---------- Save the cover ---------- */

// Saves the cover as the reader shows it, title included, as a PNG at A5 300 dpi
// (1748 x 2480 px): the cover is laid out off screen at 874 x 1240 CSS px and drawn at
// twice that by html-to-image (loaded only when the button is used).
const COVER_W = 874, COVER_H = 1240, COVER_SCALE = 2;
function loadScript(src) {
  return new Promise((ok, fail) => {
    const el = Object.assign(document.createElement("script"), { src, onload: ok, onerror: fail });
    document.head.append(el);
  });
}
// Marks a PNG as `dpi` dots per inch (a pHYs chunk right after IHDR), so 1748 x 2480 px opens
// as A5 in print and layout apps instead of 72 dpi (about 62 x 87 cm).
function withDpi(png, dpi) {
  const ppm = Math.round(dpi / 0.0254);
  const chunk = new Uint8Array(21);
  const v = new DataView(chunk.buffer);
  v.setUint32(0, 9);
  chunk.set([0x70, 0x48, 0x59, 0x73], 4); // "pHYs"
  v.setUint32(8, ppm);
  v.setUint32(12, ppm);
  chunk[16] = 1; // unit: metre
  let c = ~0;
  for (const b of chunk.subarray(4, 17)) {
    c ^= b;
    for (let k = 0; k < 8; k++) c = (c >>> 1) ^ (0xedb88320 & -(c & 1));
  }
  v.setUint32(17, ~c >>> 0);
  const at = 8 + 25; // signature + IHDR chunk
  const out = new Uint8Array(png.length + chunk.length);
  out.set(png.subarray(0, at));
  out.set(chunk, at);
  out.set(png.subarray(at), at + chunk.length);
  return out;
}
// Draws one cover's markup off screen as a PNG and returns its bytes.
async function coverPng(markup) {
  const holder = document.createElement("div");
  holder.style.cssText = `position:fixed;left:-10000px;top:0;width:${COVER_W}px;height:${COVER_H}px;`;
  holder.innerHTML = markup;
  document.body.append(holder);
  try {
    const img = holder.querySelector(".cover-img");
    if (img && !img.complete) await new Promise((r) => { img.onload = img.onerror = r; });
    await document.fonts.ready;
    const url = await window.htmlToImage.toPng(holder.firstElementChild, { width: COVER_W, height: COVER_H, pixelRatio: COVER_SCALE, cacheBust: false });
    return withDpi(new Uint8Array(await (await fetch(url)).arrayBuffer()), 300);
  } finally {
    holder.remove();
  }
}
function download(bytes, name, type) {
  const url = URL.createObjectURL(new Blob([bytes], { type }));
  const a = Object.assign(document.createElement("a"), { href: url, download: name });
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}
// Each button saves one cover with its text: one download per click, so the browser never
// blocks it.
async function saveCover(btn, markup, name) {
  btn.disabled = true;
  try {
    if (!window.htmlToImage) await loadScript("https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js");
    download(await coverPng(markup()), name, "image/png");
  } catch (err) {
    console.error(err);
    alert("Sampul belum bisa disimpan. Coba lagi.");
  } finally {
    btn.disabled = false;
  }
}
$("coverBtn").addEventListener("click", () => saveCover($("coverBtn"), () => coverMarkup(book, { withImage: true }), `${book.id}-sampul-depan.png`));
$("backCoverBtn").hidden = !hasBack;
$("backCoverBtn").addEventListener("click", () => saveCover($("backCoverBtn"), () => backCoverMarkup(book), `${book.id}-sampul-belakang.png`));
$("spineBtn").hidden = !book.sideCover;
$("spineBtn").addEventListener("click", () => saveCover($("spineBtn"), () => spineMarkup(book), `${book.id}-punggung.png`));
$("uvBtn").hidden = !book.uvArt;
$("uvBtn").addEventListener("click", () => saveCover($("uvBtn"), () => uvMarkup(book), `${book.id}-sampul-depan-uv.png`));
$("uvBackBtn").hidden = !(book.uvArt && hasBack);
$("uvBackBtn").addEventListener("click", () => saveCover($("uvBackBtn"), () => backUvMarkup(book), `${book.id}-sampul-belakang-uv.png`));
$("uvSpineBtn").hidden = !(book.uvArt && book.sideCover);
$("uvSpineBtn").addEventListener("click", () => saveCover($("uvSpineBtn"), () => spineUvMarkup(book), `${book.id}-punggung-uv.png`));

/* ---------- Input ---------- */

$("next").addEventListener("click", () => turn(1));
$("nextPage").addEventListener("click", () => turn(1));
$("prevPage").addEventListener("click", () => turn(-1));
$("nextSec").addEventListener("click", () => jumpSection(1));
$("prevSec").addEventListener("click", () => jumpSection(-1));
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
