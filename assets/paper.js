// Paper color of a book's pages, chosen in the reader and used by the print PDF too.
// Saved per book in this browser (localStorage), so the print page, which opens from
// the same site, picks up the same color.

export const DEFAULT_PAPER = "#fffdf8";

// A few book papers to start from; any other color comes from the color picker.
export const PAPERS = [
  { name: "Krem", color: "#fffdf8" },
  { name: "Putih", color: "#ffffff" },
  { name: "Gading", color: "#fbf5e6" },
  { name: "Novel", color: "#f5ecd7" },
  { name: "Abu", color: "#f1f1ee" },
];

const key = (bookId) => `lucu-paper-${bookId}`;

export function savedPaper(bookId) {
  try { return localStorage.getItem(key(bookId)) || null; } catch { return null; }
}

export function savePaper(bookId, color) {
  try {
    if (!color || color.toLowerCase() === DEFAULT_PAPER) localStorage.removeItem(key(bookId));
    else localStorage.setItem(key(bookId), color);
  } catch {}
}

// Sets the color on the pages; null goes back to the default.
export function applyPaper(color) {
  if (color) document.documentElement.style.setProperty("--paper", color);
  else document.documentElement.style.removeProperty("--paper");
}

// Border color of the story pictures (the line around each picture page), saved the same way.
export const DEFAULT_BORDER = "#4aa8e0"; // SITI blue, --siti in pages.css

export const BORDERS = [
  { name: "Biru SITI", color: "#4aa8e0" },
  { name: "Hitam", color: "#222222" },
  { name: "Abu", color: "#9a9a9a" },
  { name: "Emas", color: "#c9a227" },
  { name: "Merah", color: "#d04a4a" },
  { name: "Toska", color: "#3fb8a8" },
];

const borderKey = (bookId) => `lucu-border-${bookId}`;

export function savedBorder(bookId) {
  try { return localStorage.getItem(borderKey(bookId)) || null; } catch { return null; }
}

export function saveBorder(bookId, color) {
  try {
    if (!color || color.toLowerCase() === DEFAULT_BORDER) localStorage.removeItem(borderKey(bookId));
    else localStorage.setItem(borderKey(bookId), color);
  } catch {}
}

export function applyBorder(color) {
  if (color) document.documentElement.style.setProperty("--siti", color);
  else document.documentElement.style.removeProperty("--siti");
}

// Shape of the picture on the page facing each part picture (pages.css, data-frame).
export const DEFAULT_FRAME = "hexagon";

export const FRAMES = [
  { name: "Hexagon", value: "hexagon" },
  { name: "41-gon", value: "gon41" },
  { name: "Lingkaran", value: "circle" },
  { name: "Persegi", value: "square" },
  { name: "Segitiga", value: "triangle" },
  { name: "16:9", value: "wide" },
];

const frameKey = (bookId) => `lucu-frame-${bookId}`;

export function savedFrame(bookId) {
  try { return localStorage.getItem(frameKey(bookId)) || null; } catch { return null; }
}

export function saveFrame(bookId, frame) {
  try {
    if (!frame || frame === DEFAULT_FRAME) localStorage.removeItem(frameKey(bookId));
    else localStorage.setItem(frameKey(bookId), frame);
  } catch {}
}

export function applyFrame(frame) {
  if (frame && frame !== DEFAULT_FRAME) document.documentElement.dataset.frame = frame;
  else delete document.documentElement.dataset.frame;
}
