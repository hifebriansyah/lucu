# bad/: Jahat Tapi Legal

Book 3, *Jahat Tapi Legal: Dark Triad di Balik Orang-Orang yang Kaya di Celah Hukum*. The theme is the Dark Triad (narcissism, Machiavellianism, psychopathy). **Not a humor book**, so the comedy rules in `../CLAUDE.md` (punchlines, plot twists, the shared cast, gue/lu) don't apply here. Keep the format rules: one story per file, `naskah.md` and its Daftar Isi updated in the same change, no emoji.

## Shape

Each story is a true story about one real person (or company) who got rich in a way that was legal at the time but hurt others: loopholes, fine print, unwritten promises, markets with no choice. The last part, Melewati Batas Legal, is the exception: people who crossed the line into crime (eFishery among them). It shows where "jahat tapi legal" ends.

Each story is 5–7 A5 pages (roughly 1,000–1,500 words) and has, in this order:

1. An italic one-line kicker: place, year, field, and the move in a few words.
2. `### Kisah`: the story, told plainly in standard, readable Indonesian.
3. `### Harga`: the price paid: what happened to the person, to the victims, and to the rules.
4. `### Hasil`: what they gained (money, power, a title or a win).
5. `### Pelajaran`: what the reader can learn, for both sides of the table.
6. `### Analisa Dark Triad`: one bold-labeled paragraph per trait with a level (**Narsisisme: kuat.**, sedang, lemah, tidak terlihat/tidak jelas), the reported behavior behind it, then a **Kesimpulan**. Strongest trait first. It reads public behavior, never diagnoses; when a trait doesn't fit, say so (EpiPen and eFishery point to the system or Cressey's fraud triangle instead). Then `### Profil` (see below).
7. `### Profil`: `**Nama:**`, `**Lahir:**`, `**Wafat:**` (or "Masih hidup"), `**Jenis kelamin:**`, `**Negara:**`, one per line, then a real quote by the person as `> “...”` and `> — where and when`. No quote if none can be sourced; never invent or paraphrase one. The reader sets it as a left-hand page with the Dark Triad chart, facing the character's picture.

## Accuracy

These are real people, so:

- Use only facts from public reporting, books or court records, and round the figures ("sekitar").
- Say "menurut laporan" or "diduga" for anything not proven in court, and give the person's denial where they made one.
- Write disputed anecdotes as disputed ("konon", "menurut keluarga").
- Keep each story's sources in `SOURCES.md` (last full fact-check: 24 November 2026). Before printing, check every story against its sources again. The Indonesian story (eFishery) needs the most care: name only people a court has convicted, and keep the case status current (an appeal may change it).

## Two volumes

The book comes in two volumes, each its own book on the shelf: Jilid 1 (`naskah.md`, book id `bad`, 17 stories) and Jilid 2 (`naskah-2.md`, book id `bad2`, 16 stories). Each volume has the same three sections, and numbers its own stories from 1:

- **Zaman Dulu**: stories from before about 1990, including the Nusantara ones (Raden Wijaya, Coen, Daendels, Raffles, Van den Bosch, Oei Tiong Ham, Liem Sioe Liong).
- **Zaman Sekarang**: from about 1990 on (BPPC is the Indonesian one).
- **Melewati Batas Legal**: people who crossed into crime, every one convicted (Gibran Huzaifah of eFishery and Eddy Tansil are the Indonesian ones). Gibran Huzaifah ends Jilid 1.

Within a section, stories run in date order, except that Jilid 1 opens with Rockefeller (the book's clearest "jahat tapi legal" case) before Raden Wijaya. Each volume has its own Kata Pengantar and Penutup (in the script); Mengenal Dark Triad is the same in both.

## Profile spread

Every story takes an even number of pages, starting on a left-hand page. It ends with one spread: the profile page on the left (name, Dark Triad chart, biodata, quote) and the character's picture on the right, with a blank page first when the story ends on a left-hand page. The chart (`assets/triad.js`, `triadChart` in `books.json`) is read from the analysis's bold labels: keep each as `**Trait: level.**` with the trait spelled Narsisisme, Machiavellianisme or Psikopati and a level from lemah, sedang, kuat, sangat kuat ("X sampai Y" is allowed), or tidak jelas / tidak terlihat. A story missing one of the three labels gets no chart. The profile's dates and quote need sources in `SOURCES.md` like everything else.

## Character pictures

Each story ends with a picture of its person, on the page after the story (`storyArtAt: "end"` in `books.json`). The originals are `characters/bad-<n>.jpeg`, numbered across both volumes in the order of `VOLUMES` (Jilid 1 is 1–17, Jilid 2 is 18–33; `storyArtOffset: 17`). If a story moves, rename its picture to match. After adding or replacing one, run `python3 tools/covers.py --book bad` and commit only the copies in `characters/web/`.

## Building the manuscripts

Each story lives in `stories/<slug>.md`, starting with `# <Title>` (no number). `VOLUMES` in `tools/naskah-bad.py` lists which slugs go in which volume and section, in order; `python3 tools/naskah-bad.py` builds both manuscripts and numbers the stories. To move a story, move its slug in `VOLUMES`; edit the story files or the script, never the `naskah` files directly. A story that mentions another should name the volume or section if they're not in the same one.
