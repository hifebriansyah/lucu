import { loadBook } from "./book.js";
import { paginate, pageElement } from "./paginate.js";

const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);
const bookId = params.get("book") || "ai";

const { book, sections, missing } = await loadBook(bookId);
document.title = `${book.title} · PDF siap cetak`;
$("readLink").href = `reader.html?book=${book.id}`;
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

$("info").textContent = `${pages.length} halaman · A5 (14,8 × 21 cm)`;
$("printBtn").disabled = false;
$("printBtn").addEventListener("click", () => window.print());
