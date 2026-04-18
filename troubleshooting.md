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

**Cause:** `sed -i` was used for bulk file edits. GNU and BSD `sed -i` disagree on arguments — BSD/macOS `sed -i` requires an explicit suffix argument, and a misuse ends up treating a subsequent argument as the suffix or a file name. Depending on the exact invocation (and interplay with shell globbing and temp-file naming used by some sed implementations, editor swap files, or cleanup tools), you can end up with stray `XX*`-prefixed files that Obsidian cannot open. The root cause is always the same: `sed -i` is non-portable and easy to misuse across files.

**Fix:** Delete the `XX*` files. In terminal:
```bash
find Library/wiki/pages -name "XX*" -delete
```

**Prevention:** Always use Python for bulk edits across multiple pages — never `sed -i`. Anchor to an absolute root and handle encoding/read errors so a silent zero-match doesn't look like success:
```python
import os, re, pathlib
ROOT = pathlib.Path(os.environ.get("WIKI_ROOT", ".")).resolve()
pages = ROOT / "wiki" / "pages"
assert pages.is_dir(), f"pages dir not found at {pages}"

edited = 0
for f in pages.rglob("*.md"):
    try:
        text = f.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        print(f"skip {f}: {e}")
        continue
    new = re.sub(r"old-pattern", "new-value", text)
    if new != text:
        f.write_text(new, encoding="utf-8")
        edited += 1
print(f"edited {edited} files under {pages}")
```
A count of 0 means the pattern matched nothing — investigate before assuming success.

---

## Obsidian created stray `.md` files at the vault root

**Symptom:** Files like `LLM Wiki.md` or `RAG vs Wiki Compilation.md` appear at the root of your Library folder — not inside `wiki/pages/`.

**Cause:** Obsidian auto-creates a note when you click an unresolved `[[wiki link]]`, and it places it in the default new note location (which defaults to vault root).

**Fix:**
1. Delete the stray files from the vault root
2. Go to **Obsidian Settings → Files and links → Default location for new notes**
3. Set it to `pages` (or a subfolder like `pages/concepts/`) — this is vault-relative, and the Obsidian vault root is `wiki/`

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

**Cause:** Older schema versions (≤1.9) did not gate `!! ready` by session position. In schema v1.10+, the agent requires `!! ready confirm` if invoked mid-session.

**Fix:** The summary is gone and cannot be recovered.

**Prevention:** Keep `CLAUDE.md` on schema v1.10 or newer — the mid-session guard will catch accidental mid-session invocations and require explicit `!! ready confirm`.

---

## `!! wrap` overwrote an existing session summary

**Symptom:** You invoked `!! wrap` and discovered afterward that a previous session summary (that you hadn't consumed with `!! ready`) was overwritten and lost.

**Cause:** Older schema versions (≤1.9) did not check for existing wrapped content before overwriting.

**Fix:** The previous summary is gone and cannot be recovered.

**Prevention:** Schema v1.10+ requires explicit user confirmation when `!! wrap` detects a prior `MEMORY_STATE: WRAPPED` marker in `memory.md`. If you see the overwrite warning, say `no` if you need to preserve the existing summary first — consume it with `!! ready` in the current session, then `!! wrap` fresh.

---

## `memory.md` appears truncated after `!! wrap`

**Symptom:** `!! ready` next session shows only partial content and warns that the summary appears incomplete.

**Cause:** The session ended (or the agent was interrupted) before `!! wrap` finished writing. In schema v1.10+, the trailing `<!-- MEMORY_WRAP_COMPLETE -->` marker is missing, which is how `!! ready` detects truncation.

**Fix:** `!! ready` will NOT auto-wipe truncated memory. In schema v1.11+, it offers three options: `clear` (wipe back to EMPTY), `keep` (rewrite the opening marker to `MEMORY_STATE: TRUNCATED_ACKNOWLEDGED` so the warning does not re-fire on subsequent `!! ready` calls), or `edit` (hand the file back to you untouched for manual repair). In schema v1.10 there was no `keep` option — repeated `!! ready` calls would loop on the same warning until you manually cleared or edited the file.

**Prevention:** Say `!! wrap` earlier in the session — not at the very last message — so the agent has time to finish writing and append the completion marker.

---

## `!! wrap` or `!! ready` paused for approval on log append / hot.md refresh

**Symptom:** Agent ran `!! wrap` (or `!! ready`) and then stopped mid-procedure to request a separate approval for appending to `log.md` or refreshing `hot.md`. Felt redundant, since the user had just invoked the command.

**Cause:** Older schema versions (≤1.11) scoped the Approval Rule exception too narrowly — only `memory.md` write / wipe was covered. The companion `log.md` append and `hot.md` refresh fell under the general "explicit approval required" clause, so a strict agent would pause.

**Fix:** Schema v1.12+ broadened both exceptions so that the user invoking `!! wrap` or `!! ready` implicitly approves the **entire** procedure: memory.md touch + `memory | …` log append + `hot.md` refresh. No secondary approval request.

**Prevention:** Keep `CLAUDE.md` on schema v1.12 or newer.

---

## `!! ingest all` approval promised pages before the sources were read

**Symptom:** During `!! ingest all`, the B4 combined approval listed "all pages to be created / updated across the batch" but the numbers felt speculative — and sometimes a file ended up touching pages that weren't on the approval list.

**Cause:** In schema v1.11 and earlier, the batch preamble read `log.md` tail and `index.md` once, then immediately asked for approval (B4), and only read the actual source files per-file during B5. The approval was necessarily speculative because no source file had been opened yet.

**Fix:** Schema v1.12+ introduces a new step B3.5 — a batch-level pre-read of every source file in `wiki/inbox/` — before B4. B4's token estimate now accounts for those reads, and B5 no longer re-reads sources.

**Prevention:** Keep `CLAUDE.md` and `scheduled-tasks/ops/ingest.md` on schema v1.12 or newer — the blueprint sync will keep them in step if you follow the Blueprint Sync Rule in `CLAUDE.md`.

---

## Edited `blueprint/.gitignore` and nothing changed about my Obsidian vault

**Symptom:** Followed older setup-guide advice to "remove the `.obsidian/` line from `.gitignore` and commit the settings files you want to track," but `wiki/.obsidian/` behavior didn't change and the settings still weren't bundled with the blueprint.

**Cause:** The blueprint's `.gitignore` scopes only to files **inside** `blueprint/`. The Obsidian vault lives at `wiki/.obsidian/`, which is outside that scope — so the `.obsidian/` entry in `blueprint/.gitignore` was never governing the user's real vault settings. The v1.11 setup-guide note implied otherwise.

**Fix:** v1.12 setup-guide.md rewrote the note to explain the scope and to describe (without implementing) the bundling machinery that would actually ship vault settings with the blueprint (a curated `blueprint/template/.obsidian/`, an un-ignored entry, and a Step 2 copy rule).

**Prevention:** Don't edit `blueprint/.gitignore` expecting it to govern files outside `blueprint/`. Treat vault-setting bundling as a distribution-time concern, not a setup-time one.

---

## `!! audit [some-wiki-page]` returns "no match"

**Symptom:** Ran `!! audit [page-name]` expecting an audit of a wiki page and got "no match" or a redirect to `!! lint`.

**Cause:** `!! audit` scopes **exclusively** to files under `blueprint/` — the schema, the ops templates, and the distribution docs. It is designed to catch logic contradictions, approval leaks, and blueprint-sync drift in the system itself, not quality issues on wiki content.

**Fix:** Use the right command for the right scope:

- `!! lint [page-name]` or `!! lint all` — wiki-page quality (broken links, orphans, stale claims)
- `!! audit [file-name]` or `!! audit all` — blueprint integrity (schema, ops files, docs)

**Prevention:** Remember the split — **lint = wiki integrity, audit = blueprint integrity**.

---

## Bulk Edits Reference

Always use Python for any edit touching more than one file. Always anchor to an absolute root path (never rely on cwd) and always handle encoding errors explicitly:

```python
import os, re, pathlib

ROOT = pathlib.Path(os.environ.get("WIKI_ROOT", ".")).resolve()
pages = ROOT / "wiki" / "pages"
assert pages.is_dir(), f"pages dir not found at {pages}"

# Example: fix tag format across all pages
edited = 0
for f in pages.rglob("*.md"):
    try:
        text = f.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        print(f"skip {f}: {e}")
        continue
    new = text
    new = re.sub(r"tags: \[#(\w)", r"tags: [\1", new)
    new = re.sub(r", #(\w)", r", \1", new)
    if new != text:
        f.write_text(new, encoding="utf-8")
        edited += 1
print(f"edited {edited} files under {pages}")
```

Run via the agent's shell sandbox or in your own terminal. Always export `WIKI_ROOT` to the absolute working-folder path before running, and always sanity-check the printed edit count. A count of 0 usually means the regex matched nothing — investigate before claiming success.
