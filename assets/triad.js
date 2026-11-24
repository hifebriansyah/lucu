// The Dark Triad chart for book 3 (books.json `triadChart`): a triangle radar with one axis
// per trait, drawn from the story's own bold labels ("**Narsisisme: sedang sampai kuat.**").
// Levels: lemah 1, sedang 2, kuat 3, sangat kuat 4 (rings from the center out, unlabeled);
// "X sampai Y" sits between the two. A trait the story calls tidak jelas / tidak terlihat /
// tidak dapat dibaca stays at the center. No dots: rings and shape have rounded corners.

const TRAITS = [
  { key: "Narsisisme", angle: -90 },
  { key: "Machiavellianisme", angle: 30 },
  { key: "Psikopati", angle: 150 },
];
const LEVELS = [["sangat kuat", 4], ["kuat", 3], ["sedang", 2], ["lemah", 1]];
const UNCLEAR = /tidak (jelas|terlihat|dapat dibaca)/;
const MAX = 4;

// One trait's level from its label text (after the colon): { value, label }.
function readLevel(phrase) {
  let rest = phrase.toLowerCase();
  const found = [];
  for (const [word, n] of LEVELS) {
    if (rest.includes(word)) { found.push([word, n]); rest = rest.split(word).join(" "); }
  }
  found.sort((a, b) => a[1] - b[1]);
  const unclear = phrase.toLowerCase().match(UNCLEAR);
  if (!found.length) return { value: 0, label: unclear && unclear[1] === "terlihat" ? "tidak terlihat" : "tidak jelas" };
  const value = found.reduce((t, [, n]) => t + n, 0) / found.length;
  const label = found.map(([w]) => w).join("–") + (unclear ? ` / ${unclear[0]}` : "");
  return { value, label };
}

// The three levels from a story's markdown, or null when it has no Dark Triad analysis.
export function triadLevels(text) {
  const out = [];
  for (const t of TRAITS) {
    const m = text.match(new RegExp(`\\*\\*${t.key}:\\s*([^*]+?)\\.?\\*\\*`));
    if (!m) return null;
    out.push({ ...t, ...readLevel(m[1]) });
  }
  return out;
}

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");

// The chart as an SVG string. Colors are written out (no CSS variables) so the same SVG can
// be drawn on a canvas for the Word export.
export function triadSvg(levels, { width = 300 } = {}) {
  const cx = 150, cy = 108, R = 78;
  const at = (angle, r) => {
    const a = (angle * Math.PI) / 180;
    return [cx + r * Math.cos(a), cy + r * Math.sin(a)].map((v) => +v.toFixed(1));
  };
  // A closed path through the points with rounded corners (radius `round`, smaller on short sides).
  const rounded = (pts, round) => {
    const n = pts.length, d = [];
    for (let i = 0; i < n; i++) {
      const [px, py] = pts[(i + n - 1) % n], [x, y] = pts[i], [nx, ny] = pts[(i + 1) % n];
      const toward = (ax, ay) => {
        const len = Math.hypot(ax - x, ay - y);
        const k = len ? Math.min(round, len / 2) / len : 0;
        return [x + (ax - x) * k, y + (ay - y) * k].map((v) => +v.toFixed(1));
      };
      const [ix, iy] = toward(px, py), [ox, oy] = toward(nx, ny);
      d.push(`${i ? "L" : "M"}${ix},${iy} Q${x},${y} ${ox},${oy}`);
    }
    return d.join(" ") + " Z";
  };
  const tri = (r) => rounded(TRAITS.map((t) => at(t.angle, r)), r / 6);
  const ink = "#2a2a2e", faint = "#c9c4ba", accent = "#a3202b";
  const font = `font-family="Inter, Helvetica, Arial, sans-serif"`;
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 190" width="${width}" height="${Math.round(width * 190 / 300)}" role="img" aria-label="Grafik Dark Triad: ${levels.map((l) => `${l.key} ${l.label}`).join(", ")}">`;
  // rings (lemah, sedang, kuat, sangat kuat) and axes
  for (let n = 1; n <= MAX; n++) s += `<path d="${tri((R * n) / MAX)}" fill="none" stroke="${faint}" stroke-width="${n === MAX ? 1.2 : 0.8}"/>`;
  for (const t of TRAITS) { const [x, y] = at(t.angle, R); s += `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="${faint}" stroke-width="0.8"/>`; }
  // the person's shape
  const pts = levels.map((l) => at(l.angle, (R * l.value) / MAX));
  s += `<path d="${rounded(pts, 9)}" fill="${accent}" fill-opacity="0.22" stroke="${accent}" stroke-width="1.8" stroke-linejoin="round"/>`;
  // trait names at the corners (the levels are in the text above, so the chart shows none)
  levels.forEach((l) => {
    const [x, y] = at(l.angle, R);
    const ty = l.angle === -90 ? y - 9 : y + 18;
    s += `<text x="${x}" y="${ty}" text-anchor="middle" ${font} font-size="10.5" font-weight="700" fill="${ink}">${esc(l.key)}</text>`;
  });
  return s + "</svg>";
}

// The chart's figure, after the analysis text, which ends the story (the character's
// picture follows on the next page).
export function addTriadChart(html, text) {
  const levels = triadLevels(text);
  if (!levels) return html;
  return `${html}<figure class="triad">${triadSvg(levels)}</figure>`;
}

// The chart as a PNG on a canvas, for the Word export: { data, w, h } at `scale` times its size.
export async function triadPng(levels, { scale = 4, grey = false } = {}) {
  const svg = triadSvg(levels);
  const img = new Image();
  img.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
  await img.decode();
  const c = Object.assign(document.createElement("canvas"), { width: 300 * scale, height: 190 * scale });
  const g = c.getContext("2d");
  g.fillStyle = "#fff";
  g.fillRect(0, 0, c.width, c.height);
  if (grey) g.filter = "grayscale(1)";
  g.drawImage(img, 0, 0, c.width, c.height);
  const blob = await new Promise((r) => c.toBlob(r, "image/png"));
  return { data: new Uint8Array(await blob.arrayBuffer()), w: c.width, h: c.height };
}
