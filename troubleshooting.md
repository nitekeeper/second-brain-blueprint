# Troubleshooting

Real issues encountered during the original setup, with fixes.

---

## Obsidian shows tag errors on wiki pages

**Symptom:** Obsidian flags YAML frontmatter tags as invalid. Pages show a warning icon.

**Cause:** Tags were written with a `#` prefix in frontmatter — e.g. `tags: [#concept, #llm]`. Obsidian only accepts the `#` prefix for inline body tags, not YAML frontmatter.

**Fix:** Tags in frontmatter must be plain words without `#`:
```yaml
# ✅ Correct
tags: [concept, llm, tool]

# ❌ Wrong
tags: [#concept, #llm, #tool]
```

If this happened across many pages, fix with Python (see Bulk Edits section below). Never use `sed -i` for bulk edits.

---

## Strange `XX*` files appeared in wiki/pages subfolders

**Symptom:** Files named `XX5dT39o`, `XXabcdef`, etc. appear in your pages folders. Obsidian cannot open them.

**Cause:** `sed -i` was used for bulk file edits. On some systems, `sed -i` creates temporary backup files with `XX` prefixes. If the command fails or the flag is wrong, these files are left behind.

**Fix:** Delete the `XX*` files. In terminal:
```bash
find Library/wiki/pages -name "XX*" -delete
```

**Prevention:** Always use Python for bulk edits across multiple pages — never `sed -i`:
```python
import re, pathlib
for f in pathlib.Path("wiki/pages").rglob("*.md"):
    text = f.read_text()
    text = re.sub(r"old-pattern", "new-value", text)
    f.write_text(text)
```

---

## Obsidian created stray `.md` files at the vault root

**Symptom:** Files like `LLM Wiki.md` or `RAG vs Wiki Compilation.md` appear at the root of your Library folder — not inside `wiki/pages/`.

**Cause:** Obsidian auto-creates a note when you click an unresolved `[[wiki link]]`, and it places it in the default new note location (which defaults to vault root).

**Fix:**
1. Delete the stray files from the vault root
2. Go to **Obsidian Settings → Files and links → Default location for new notes**
3. Set it to `wiki/pages` (or a subfolder like `wiki/pages/concepts/`)

This prevents Obsidian from creating notes in the wrong location in future.

---

## Phantom `[[Page Title]]` node in Obsidian graph

**Symptom:** A node called "Page Title" appears in the Obsidian graph view with no real page behind it.

**Cause:** The `CLAUDE.md` schema file contained a literal `[[Page Title]]` in an example code block, which Obsidian rendered as a real wiki link.

**Fix:** Escape the brackets in example code so Obsidian ignores them:
```
\[\[Page Title\]\]
```

Or wrap the example in a fenced code block so Obsidian doesn't parse it as a link.

---

## Agent reads the full log.md on startup, consuming too many tokens

**Symptom:** Sessions feel expensive even for simple queries. Token estimates are high before any real work is done.

**Cause:** The agent is reading the full `log.md` at startup instead of just the tail.

**Fix:** Check `CLAUDE.md` — the startup section should say to read only `hot.md` at startup, and defer `log.md` to when it's actually needed. The log should only ever be read with `tail -5` unless doing a full audit.

---

## Agent forgot to read the ops file before an operation and made mistakes

**Symptom:** Agent skipped a step, formatted a page wrong, or forgot to update index.md or log.md.

**Cause:** The agent started an operation without reading the matching ops file from `scheduled-tasks/ops/`.

**Fix:** Remind the agent: `Before you proceed, read scheduled-tasks/ops/[operation].md`. The ops file reminder table in `CLAUDE.md` should prevent this — if it keeps happening, check that the table is still present in the schema.

---

## Stale `wiki/raw/` folder appeared inside the wiki vault

**Symptom:** A `raw/` folder exists inside `wiki/` alongside `pages/`, containing duplicate source files. Obsidian indexes these raw markdown files as wiki pages.

**Cause:** Early schema versions (v1.0) placed raw files at `wiki/raw/`. This was corrected in v1.1 — the canonical raw archive is `raw/` at the working folder root (outside the Obsidian vault). A stale `wiki/raw/` folder is a leftover from that earlier layout.

**Fix:** Delete `wiki/raw/` and all files inside it. The originals are already in `raw/`. In the Cowork session, tell Claude:
> "Delete wiki/raw/ — it's a stale duplicate."

Claude will request file deletion permission via the Cowork allow-delete prompt, then remove the folder.

**Prevention:** Always open `wiki/` (not the parent working folder) as your Obsidian vault. Raw source files live in `raw/` which is outside the vault and never visible to Obsidian. Clipped articles go to `wiki/inbox/` and are moved to `raw/` by Claude after ingesting.

---

## Session ended before `!! wrap` completed

**Symptom:** You tried to save a session summary but the session closed or timed out before the agent finished writing `memory.md`. The file is empty or incomplete next session.

**Cause:** `!! wrap` requires the agent to write a file — if the session ends mid-write, `memory.md` may be blank or contain only partial content.

**Fix:** At the start of the next session, say `!! ready` anyway — the agent will check `memory.md` and if it's empty, it will simply announce readiness normally. No harm done. Then reconstruct what you remember from the previous session manually if needed.

**Prevention:** Say `!! wrap` with enough time left in a session — don't leave it to the very last message.

---

## `!! ready` was triggered mid-session and wiped memory unexpectedly

**Symptom:** You said something like "I'm ready" or typed `!! ready` during a session (not at the start), and the agent read and wiped `memory.md`, destroying the saved summary before you intended.

**Cause:** `!! ready` is designed as a session-start command but is not restricted to it — it will fire any time you say it, even mid-session.

**Fix:** The summary is gone and cannot be recovered. Going forward, only say `!! ready` as the very first message in a new session.

**Prevention:** Be deliberate with `!! ready` — treat it as a session-opening command only, not something to say casually mid-conversation.

---

## Bulk Edits Reference

Always use Python for any edit touching more than one file:

```python
import re, pathlib

# Example: fix tag format across all pages
for f in pathlib.Path("wiki/pages").rglob("*.md"):
    text = f.read_text()
    # Remove # prefix from tags in frontmatter
    text = re.sub(r"tags: \[#(\w)", r"tags: [\1", text)
    text = re.sub(r", #(\w)", r", \1", text)
    f.write_text(text)
```

Run via the agent's shell sandbox or in your own terminal.
