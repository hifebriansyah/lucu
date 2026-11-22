# lucu/

Short funny stories written in casual Indonesian (gue/lu for dialogue). Each book lives in its own folder, with one story per file (`1.md`, `2.md`, ...) and its own `naskah.md`:

- `ai/`: book 1, *Kelakuan Pengguna Ai!!*. 62 stories about AI, in six parts plus an epilog.
- `politics/`: book 2. 100 Indonesian political jokes.

`naskah.md` compiles every story of that book into one manuscript (title page, copyright, contents, foreword, the parts, closing). When a story changes or a new one is added, update that book's `naskah.md` and its Daftar Isi in the same change.

## Characters

Every book uses the same names: Pak Bos, Bu HRD, Dimas, Raka, Bang Yudi, Nadia, Pak Satpam, Pak Darmo, Bu Ratna, Bima, Bu Guru, Pak Lurah, and SITI. Whether SITI must appear depends on the book; see its `CLAUDE.md`. Don't add new named characters; unnamed roles (warga, investor, caleg lawan) are fine.

Each character's background (job, habits, relationships) can differ between books. Each book's folder has its own `CLAUDE.md` with that book's cast and background; follow it inside that folder.

## Rules

- **Short.** Readable in under a minute. Cut any detail that isn't a setup, a punchline, or a callback.
- **Punchy.** Short sentences. One joke per beat. The punchline goes at the end of the line.
- **Always end with a plot twist.** It must flip what the reader expected.
- **The twist must be logical.** Plant its cause earlier so the reader thinks "oh, of course", not "wait, how?". Example: the user typed "YA AMPUN" and the AI read it as "Ya". Never use events with no cause, or tech that doesn't work that way (deleting a server over SSH doesn't turn office PCs blue).
- **The last line lands the joke.** Don't explain it afterwards.

## Comedy techniques

Use at least two in every story:

- **Callback**: bring back an earlier detail as the punchline (the line quoted from TikTok returns at the end).
- **Rule of three**: two normal items, then an absurd third.
- **Escalation**: each beat makes things worse than the last.
- **Setup / payoff (Chekhov's gun)**: a harmless early detail ("langsung kirim aja") causes the ending.
- **Misunderstanding**: one side reads words too literally (an AI that is too honest, too obedient, too literal).
- **Irony**: the thing meant to save the character is what ruins them.
- **Understatement**: a calm reaction to a disaster ("Semoga membantu!").
- **Dramatic irony**: the reader knows something the character doesn't.

## Format

- `# <number>. <Title>` heading. **Short title**: one to three words, taken from the story's key word or callback ("Strawberry", "Senior Developer", "Bikin HRD Merinding").
- **Smooth storytelling.** Flowing narrative prose with dialogue woven in, like a story told aloud. No chat transcripts, no tables, no bullet lists, no `---` breaks. Link the beats with transitions ("CV itu bekerja terlalu baik.", "Sayangnya, ...") so each paragraph leads into the next.
- **No emoji or emoticons**, not even inside an AI message.
- Give the human character a name (Raka, Dimas, ...).
- When a story has an AI character, it is always **SITI**, an AI agent with code **M4.KZ-A**. Never explain the code's meaning in a story.
