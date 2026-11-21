import { loadBook } from "./book.js";

const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);
const bookId = params.get("book") || "ai";
const sizeKey = params.get("size") || "14x21";

// Trim sizes in mm: [width, height]. Margins mirror for left and right pages.
const SIZES = { "14x21": [140, 210], a5: [148, 210], "13x19": [130, 190] };
const [w, h] = SIZES[sizeKey] || SIZES["14x21"];

$("size").value = sizeKey in SIZES ? sizeKey : "14x21";
$("size").addEventListener("change", (e) => {
  params.set("size", e.target.value);
  location.search = params.toString();
});

const { book, sections, missing } = await loadBook(bookId);
document.title = `${book.title} · PDF siap cetak`;
$("readLink").href = `reader.html?book=${book.id}`;
lucide.createIcons();

if (missing) {
  $("info").textContent = "Naskah buku ini belum tersedia.";
  throw new Error("missing manuscript");
}

/* Build the interior as one flow; Paged.js breaks it into real pages. */
const root = document.createElement("div");
root.className = "book-root";
root.innerHTML = `<span class="booktitle-marker">${book.title}</span>`;

const stories = [];
for (const s of sections) {
  const el = document.createElement("section");
  if (s.type === "title") el.className = "title-page";
  else if (s.type === "dedication") el.className = "dedication";
  else if (s.type === "part") el.className = "part";
  else if (s.type === "story") el.className = "story";
  else if (s.type === "toc") el.className = "toc-page";
  else if (s.type === "image") el.className = "image-page";
  else el.className = "front";
  el.innerHTML = s.html;
  if (s.type === "story" || s.type === "part") {
    const id = `s-${s.index}`;
    el.querySelector("h1, h2")?.setAttribute("id", id);
    stories.push({ id, title: s.title, part: s.type === "part" });
  }
  root.append(el);
}

// Replace the manuscript's plain list with a contents page that has real page numbers.
const tocEl = root.querySelector(".toc-page");
if (tocEl) {
  tocEl.innerHTML = `<h2>Daftar Isi</h2><ol>${stories
    .map((s) => `<li class="${s.part ? "toc-part" : ""}"><a href="#${s.id}"><span class="t">${s.title}</span></a></li>`)
    .join("")}</ol>`;
}

const pageCss = `
@page { size: ${w}mm ${h}mm; margin: 18mm 14mm 20mm 20mm; }
@page :left { margin: 18mm 20mm 20mm 14mm; }
@page :right { margin: 18mm 14mm 20mm 20mm; }
`;

await document.fonts.ready;
const previewer = new Paged.Previewer();
const flow = await previewer.preview(root, ["assets/print.css", { "page-size.css": pageCss }], $("pages"));

$("info").textContent = `${flow.total} halaman · ${w / 10} × ${h / 10} cm`;
$("printBtn").disabled = false;
$("printBtn").addEventListener("click", () => window.print());
