import { loadBook } from "./book.js";
import { exportDocx } from "./docx.js";
import { paginate, pageElement } from "./paginate.js";
import { DEFAULT_PAPER, savedPaper, applyPaper, savedBorder, applyBorder, savedFrame, applyFrame, savedBw, saveBw, applyBw } from "./paper.js";

const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);
const bookId = params.get("book") || "ai";

const { book, sections, missing } = await loadBook(bookId);
document.title = `${book.title} · PDF siap cetak`;
$("readLink").href = `reader.html?book=${book.id}`;
// The paper color saved in the reader prints too (print.css keeps the colors exact).
const paper = savedPaper(book.id);
applyPaper(paper);
const border = savedBorder(book.id); // and the picture border color
applyBorder(border);
applyFrame(savedFrame(book.id)); // and the shape of the part pictures' facing pictures
// Hitam putih, the same switch as in the reader (and saved for it too).
const bwBtn = $("bwBtn");
applyBw(savedBw(), bwBtn);
lucide.createIcons();

if (missing) {
  $("info").textContent = "Naskah buku ini belum tersedia.";
  throw new Error("missing manuscript");
}

// The same A5 pages the reader shows, from the same engine, printed at full size.
const pages = await paginate(sections, $("measure"), { bookTitle: book.title });

const frag = document.createDocumentFragment();
for (const data of pages) frag.append(pageElement(data));
$("pages").replaceChildren(frag);

const showInfo = () => {
  const bw = document.body.classList.contains("bw") ? " · hitam putih" : "";
  $("info").textContent = `${pages.length} halaman · A5 (14,8 × 21 cm) · kertas ${paper || DEFAULT_PAPER}${border ? ` · bingkai ${border}` : ""}${bw}`;
};
showInfo();
bwBtn.addEventListener("click", () => { const on = !document.body.classList.contains("bw"); applyBw(on, bwBtn); saveBw(on); showInfo(); });
$("printBtn").disabled = false;

// Word: the same manuscript as an A5 .docx, built in the browser (assets/docx.js).
const docxBtn = $("docxBtn"), docxLabel = docxBtn.querySelector("span");
docxBtn.disabled = false;
docxBtn.addEventListener("click", async () => {
  docxBtn.disabled = true; docxLabel.textContent = "Membuat…";
  try { await exportDocx(book, sections); docxLabel.textContent = "Word"; }
  catch (e) { console.error(e); docxLabel.textContent = "Gagal, coba lagi"; }
  finally { docxBtn.disabled = false; }
});
$("printBtn").addEventListener("click", () => window.print());
