// Word export, run in the browser from the print page: turns a book's naskah.md into an A5
// .docx that follows the book layout in pages.css: 11 pt Literata on 16 pt leading, mirrored
// margins (2 cm top/bottom/spine, 1.6 cm outside), parts on right-hand pages, running heads,
// page numbers, and a Daftar Isi with real page numbers (Word asks to update fields on open).
// Text only, no pictures. The docx and fflate libraries load from jsDelivr on first use.
// <w:mirrorMargins/> goes after these settings, which must come first in settings.xml.
const SETTINGS_HEAD = /(<w:settings[^>]*>)((?:\s*<w:(?:writeProtection|view|zoom|removePersonalInformation|removeDateAndTime|doNotDisplayPageBoundaries|displayBackgroundShape|printPostScriptOverText|printFractionalCharacterWidth|printFormsData|embedTrueTypeFonts|embedSystemFonts|saveSubsetFonts|saveFormsData)\b[^>]*\/>)*)/;
const PAGE_BREAK = '<div style="page-break-after: always;"></div>';

export async function exportDocx(book) {
  const md = await (await fetch(book.manuscript, { cache: "no-store" })).text();
  const {
    Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType, PageNumber,
    SectionType, LineRuleType, LevelFormat, Bookmark, PageReference, PositionalTab,
    PositionalTabAlignment, PositionalTabLeader, PositionalTabRelativeTo, BorderStyle,
  } = await import("https://cdn.jsdelivr.net/npm/docx@9.5.1/+esm");
  const { unzipSync, zipSync, strFromU8, strToU8 } = await import("https://cdn.jsdelivr.net/npm/fflate@0.8.2/+esm");

  const MM = 56.6929; // DXA per mm
  const BOOK = "Literata", UI = "Inter";
  const pt = (n) => Math.round(n * 20); // points to twentieths

  /* ---------- Inline markdown: **bold** and *italic* ---------- */
  function runs(text, base = {}) {
    text = text.replace(/&nbsp;/g, " ");
    const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/).filter((p) => p !== "");
    return parts.map((p) => {
      if (p.startsWith("**")) return new TextRun({ ...base, text: p.slice(2, -2), bold: true });
      if (p.startsWith("*") && p.length > 2) return new TextRun({ ...base, text: p.slice(1, -1), italics: !base.italics });
      return new TextRun({ ...base, text: p });
    });
  }
  // Lines inside one paragraph keep their line breaks, as in the reader.
  function lineRuns(lines, base = {}) {
    const out = [];
    lines.forEach((l, i) => {
      if (i > 0) out.push(new TextRun({ ...base, break: 1 }));
      out.push(...runs(l, base));
    });
    return out;
  }

  /* ---------- Blocks ---------- */
  function blocks(text) {
    const lines = text.split("\n");
    const out = [];
    let i = 0;
    while (i < lines.length) {
      const l = lines[i];
      if (!l.trim()) { i++; continue; }
      let m;
      if ((m = l.match(/^(#{1,3})\s+(.*)$/))) { out.push({ t: "h" + m[1].length, text: m[2].trim() }); i++; continue; }
      if (l.startsWith(">")) {
        const inner = [];
        while (i < lines.length && lines[i].startsWith(">")) { inner.push(lines[i].replace(/^>\s?/, "")); i++; }
        out.push({ t: "quote", children: blocks(inner.join("\n")) });
        continue;
      }
      if (/^\s*[*-]\s+/.test(l) || /^\d+\.\s+/.test(l)) {
        const items = [];
        while (i < lines.length && (/^\s*[*-]\s+/.test(lines[i]) || /^\d+\.\s+/.test(lines[i]))) {
          const b = lines[i].match(/^\s*[*-]\s+(.*)$/);
          const n = lines[i].match(/^(\d+)\.\s+(.*)$/);
          items.push(b ? { bullet: true, text: b[1] } : { num: n[1], text: n[2] });
          i++;
        }
        out.push({ t: "list", items });
        continue;
      }
      const para = [];
      while (i < lines.length && lines[i].trim() && !/^(#{1,3}\s|>|\s*[*-]\s+|\d+\.\s+)/.test(lines[i])) { para.push(lines[i]); i++; }
      out.push({ t: "p", lines: para });
    }
    return out;
  }

  /* ---------- Sections (same rules as assets/book.js) ---------- */
  const sections = md.split(PAGE_BREAK).map((s) => s.trim()).filter(Boolean).map((text, index) => {
    const story = text.match(/^##\s+(\d+)\.\s+(.+)$/m);
    const part = text.match(/^#\s+(.+)$/m);
    const heading = text.match(/^##\s+(.+)$/m);
    let type, title = "";
    if (index === 0) { type = "title"; title = part ? part[1] : ""; }
    else if (story && text.startsWith("##")) { type = "story"; title = `${story[1]}. ${story[2].trim()}`; }
    else if (part && text.split("\n").length <= 2) { type = "part"; title = part[1].trim(); }
    else if (heading) { type = heading[1].trim() === "Daftar Isi" ? "toc" : "front"; title = heading[1].trim(); }
    else type = text.split("\n").filter((l) => l.trim()).every((l) => /^\*[^*].*\*$/.test(l.trim())) ? "dedication" : "copyright";
    return { index, type, title, text };
  });
  const bookTitle = sections[0].title;

  // Bookmarks for contents page numbers.
  const bookmarkOf = new Map();
  sections.forEach((s, i) => {
    if (!s.title || s.type === "title") return;
    const id = `sec${i}`;
    s.bookmark = id;
    bookmarkOf.set(s.title, id);
    const m = s.title.match(/^\d+\.\s+(.+)$/);
    if (m) bookmarkOf.set(m[1], id);
  });

  /* ---------- Paragraph builders ---------- */
  const body = { spacing: { after: pt(6.6), line: pt(16), lineRule: LineRuleType.EXACT } };

  function para(lines, opts = {}) {
    return new Paragraph({ ...body, ...opts, children: lineRuns(lines, opts.run || {}) });
  }

  function renderBlocks(bl, s, ctx = {}) {
    const out = [];
    for (const b of bl) {
      if (b.t === "h1" || b.t === "h2" || b.t === "h3") {
        const text = b.text.replace(/\*/g, "");
        const kids = runs(b.text);
        const children = s.bookmark && !ctx.marked ? [new Bookmark({ id: s.bookmark, children: kids })] : kids;
        ctx.marked = true;
        if (s.type === "title") {
          out.push(b.t === "h1"
            ? new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: pt(145), after: pt(10) }, keepNext: true, children: runs(text, { size: 48, bold: true }) })
            : new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: pt(40) }, children: runs(text, { size: 24, italics: true }) }));
        } else if (s.type === "part") {
          out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: pt(193) }, children: [new Bookmark({ id: s.bookmark, children: runs(text, { size: 40, bold: true }) })] }));
        } else if (s.type === "story") {
          out.push(new Paragraph({ spacing: { before: pt(12), after: pt(18) }, keepNext: true, children: [new Bookmark({ id: s.bookmark, children: runs(text, { size: 32, bold: true }) })] }));
        } else {
          out.push(new Paragraph({ spacing: { before: 0, after: pt(16) }, keepNext: true, children: [new Bookmark({ id: s.bookmark || `h${Math.random()}`, children: runs(text, { size: 30, bold: true }) })] }));
        }
      } else if (b.t === "p") {
        if (s.type === "title") out.push(new Paragraph({ alignment: AlignmentType.CENTER, children: lineRuns(b.lines, { size: 24 }) }));
        else if (s.type === "dedication") out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: pt(170), line: pt(16), lineRule: LineRuleType.EXACT }, children: lineRuns(b.lines) }));
        else if (s.type === "copyright") out.push(new Paragraph({ spacing: { after: pt(8), line: pt(12.5), lineRule: LineRuleType.EXACT }, children: lineRuns(b.lines, { size: 18 }) }));
        else out.push(para(b.lines, ctx.quote ? quoteOpts() : {}));
      } else if (b.t === "quote") {
        out.push(...renderBlocks(b.children, s, { ...ctx, quote: true }));
      } else if (b.t === "list") {
        for (const it of b.items) {
          if (it.bullet) {
            out.push(new Paragraph({ ...body, ...(ctx.quote ? quoteOpts() : {}), numbering: { reference: "bullets", level: 0 }, children: runs(it.text) }));
          } else {
            const left = (ctx.quote ? 200 : 0) + 340;
            out.push(new Paragraph({
              ...body, ...(ctx.quote ? { border: quoteBorder() } : {}),
              indent: { left, hanging: 340 },
              children: [new TextRun({ text: `${it.num}.\t` }), ...runs(it.text)],
              tabStops: [{ type: "left", position: left }],
            }));
          }
        }
      }
    }
    return out;
  }
  const quoteBorder = () => ({ left: { style: BorderStyle.SINGLE, size: 12, color: "D8CFBF", space: 8 } });
  const quoteOpts = () => ({ indent: { left: 200 }, border: quoteBorder() });

  // Contents page: every entry gets its real page number, right-aligned with a dot leader.
  function renderToc(s) {
    const out = [new Paragraph({ spacing: { after: pt(14) }, children: [new Bookmark({ id: s.bookmark, children: [new TextRun({ text: "Daftar Isi", size: 30, bold: true })] })] })];
    for (const b of blocks(s.text)) {
      if (b.t === "h2") continue;
      const entries = b.t === "list" ? b.items.map((it) => ({ label: `${it.num}. ${it.text}`, key: it.text, bold: false }))
        : b.t === "p" ? b.lines.map((l) => ({ label: l.replace(/\*\*/g, ""), key: l.replace(/\*\*/g, ""), bold: /^\*\*/.test(l) })) : [];
      for (const e of entries) {
        const id = bookmarkOf.get(e.key);
        out.push(new Paragraph({
          spacing: { before: e.bold ? pt(9) : 0, after: pt(3), line: pt(13.5), lineRule: LineRuleType.EXACT },
          keepNext: e.bold,
          children: [
            new TextRun({ text: e.label, size: 20, bold: e.bold }),
            ...(id ? [
              new TextRun({ size: 20, children: [new PositionalTab({ alignment: PositionalTabAlignment.RIGHT, relativeTo: PositionalTabRelativeTo.MARGIN, leader: PositionalTabLeader.DOT })] }),
              new TextRun({ size: 20, bold: e.bold, children: [new PageReference(id)] }),
            ] : []),
          ],
        }));
      }
    }
    return out;
  }

  /* ---------- Headers and footers ---------- */
  const headRun = (text) => new TextRun({ text: text.toUpperCase(), font: UI, size: 15, color: "777777", characterSpacing: 12 });
  const header = (text) => new Header({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: text ? [headRun(text)] : [] })] });
  const folio = () => new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ font: UI, size: 18, color: "555555", children: [PageNumber.CURRENT] })] })] });
  const emptyFooter = () => new Footer({ children: [new Paragraph({ children: [] })] });

  const page = {
    size: { width: Math.round(148 * MM), height: Math.round(210 * MM) },
    // With mirrored margins Word reads "left" as the spine side and "right" as the outside.
    margin: { top: Math.round(20 * MM), bottom: Math.round(20 * MM), left: Math.round(20 * MM), right: Math.round(16 * MM), header: Math.round(10 * MM), footer: Math.round(10 * MM) },
  };

  const docSections = sections.map((s, i) => {
    const onRight = s.type === "title" || s.type === "part";
    const props = { page, type: i === 0 ? SectionType.NEXT_PAGE : onRight ? SectionType.ODD_PAGE : SectionType.NEXT_PAGE };
    let headers, footers;
    if (s.type === "story") {
      props.titlePage = true;
      headers = { first: header(""), default: header(s.title), even: header(bookTitle) };
      footers = { first: folio(), default: folio(), even: folio() };
    } else if (s.type === "front" || s.type === "toc") {
      headers = { default: header(""), even: header("") };
      footers = { default: folio(), even: folio() };
    } else {
      headers = { default: header(""), even: header("") };
      footers = { default: emptyFooter(), even: emptyFooter() };
    }
    const children = s.type === "toc" ? renderToc(s) : renderBlocks(blocks(s.text), s);
    return { properties: props, headers, footers, children };
  });

  const doc = new Document({
    creator: "lucu",
    title: bookTitle,
    evenAndOddHeaderAndFooters: true,
    features: { updateFields: true },
    styles: { default: { document: { run: { font: BOOK, size: 22, color: "111111" }, paragraph: { spacing: { line: pt(16), lineRule: LineRuleType.EXACT } } } } },
    numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 340, hanging: 220 } } } }] }] },
    sections: docSections,
  });


  // Mirrored margins (Word reads "left" as the spine side), which the library doesn't expose.
  const files = unzipSync(new Uint8Array(await (await Packer.toBlob(doc)).arrayBuffer()));
  files["word/settings.xml"] = strToU8(strFromU8(files["word/settings.xml"]).replace(SETTINGS_HEAD, "$1$2<w:mirrorMargins/>"));
  for (const name of Object.keys(files)) if (name.endsWith("/")) delete files[name]; // folder entries upset Word online
  const blob = new Blob([zipSync(files)], { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });
  const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: `${book.id}-naskah.docx` });
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 10000);
}
