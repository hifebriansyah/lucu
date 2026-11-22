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
