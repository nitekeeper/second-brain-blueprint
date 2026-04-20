# Setup Guide

> This file is written for AI execution. When the user says "read setup-guide.md and set it up", follow every step below in order. Ask for confirmation before any write action.

---

## Step 0 — Select the Cowork Working Folder

Before anything else, the user must select a working folder in the Cowork window. This is the folder Claude will read from and write to throughout the session.

Instruct the user:

> In the Cowork window, click **"Select folder"** and choose the folder where your wiki will live (e.g. `Library/`).
> Once selected, Claude will have access to all files inside it.

Do not proceed until the user confirms the folder is selected.

---

## Pre-flight Check

Before starting, confirm:
1. You have access to the working folder (the Cowork working directory)
2. The `blueprint/` folder exists inside it (you are reading this file from there)

---

## Step 1 — Create Folder Structure

Show approval request, then execute.

**Important:** The Cowork Bash sandbox does not start its working directory at the user's selected folder — it runs from an isolated session root. Resolve the user's selected Cowork folder as an absolute path, export it as `WORKDIR`, then `cd` into it before running any relative `mkdir`. Without this step the folders end up in the sandbox root instead of the wiki:

```bash
# Replace /absolute/path/to/working-folder with the absolute path of the folder
# the user selected in Cowork (e.g. /Users/you/Library).
export WORKDIR="/absolute/path/to/working-folder"
cd "$WORKDIR"

mkdir -p raw
mkdir -p drafts
mkdir -p wiki/inbox
mkdir -p wiki/pages/concepts
mkdir -p wiki/pages/entities
mkdir -p wiki/pages/sources
mkdir -p wiki/pages/analyses
mkdir -p scheduled-tasks/ops
```

All subsequent shell commands in this setup run with your working folder as cwd. Cowork's Bash tool preserves cwd between commands (env vars like `$WORKDIR` do **not** persist between Bash calls, but cwd does), so no re-cd is required. Verify with `pwd` if uncertain.

**What each folder is for:**
- `raw/` — immutable source archive; Claude moves files here after ingesting
- `drafts/` — Claude's scrapbook for in-progress planning and drafting; outside the Obsidian vault
- `wiki/inbox/` — drop clipped articles here; Obsidian Web Clipper saves here
- `wiki/pages/` — all wiki content organized by type
- `scheduled-tasks/` — agent operation instruction files

---

## Step 2 — Copy Template Files

> **Reminder:** cwd persists between Bash commands in Cowork — verify with `pwd` if in doubt. You do not need to re-run `cd`. (Env vars like `$WORKDIR` do not persist; only cwd does.)

Show approval request, then copy all files from `blueprint/template/` to their correct locations:

| From | To |
|---|---|
| `blueprint/template/scheduled-tasks/refresh-hot.md` | `scheduled-tasks/refresh-hot.md` |
| `blueprint/template/scheduled-tasks/ops/ingest.md` | `scheduled-tasks/ops/ingest.md` |
| `blueprint/template/scheduled-tasks/ops/lint.md` | `scheduled-tasks/ops/lint.md` |
| `blueprint/template/scheduled-tasks/ops/audit.md` | `scheduled-tasks/ops/audit.md` |
| `blueprint/template/scheduled-tasks/ops/update.md` | `scheduled-tasks/ops/update.md` |
| `blueprint/template/scheduled-tasks/ops/conventions.md` | `scheduled-tasks/ops/conventions.md` |
| `blueprint/template/scheduled-tasks/ops/token-reference.md` | `scheduled-tasks/ops/token-reference.md` |

---

## Step 3 — Write CLAUDE.md Directly (Read → Substitute → Write)

Do **not** copy `blueprint/template/CLAUDE.md` via Bash `cp`. Instead:

1. Read `blueprint/template/CLAUDE.md` into working memory.
2. In memory, make the following substitutions:
   - Replace `[created-date]` and `[updated-date]` in the schema footer with today's date (YYYY-MM-DD)
   - Remove the `> **Setup note:** …` block at the very end (immediately under the `Schema version:` footer) — it is setup scaffolding only and must not appear in the live file
3. Write the final result directly to `CLAUDE.md` using the Write tool — one shot, no intermediate `cp`.

> **Why Write instead of cp+Edit:** The Edit tool requires a prior Read call on the exact file path it is editing. Files created via Bash `cp` do not satisfy this requirement — the Edit tool has no record of them, and the first edit attempt will fail with "File has not been read yet." Writing the final content directly with the Write tool sidesteps this entirely.

> **Note:** The `@`-prefixed paths in `CLAUDE.md` (Ops File Reminder table, Approval Rule) are working-folder-relative and resolve correctly regardless of the folder's name — no find-and-replace is needed during setup.

---

## Step 4 — Initialize Wiki Files

> **Reminder:** cwd persists between Bash commands in Cowork — verify with `pwd` if in doubt. You do not need to re-run `cd`. (Env vars like `$WORKDIR` do not persist; only cwd does.)

Show approval request, then create these four files:

**`wiki/index.md`**
```markdown
# Wiki Index

> Master catalog of all pages. Updated on every ingest or lint pass, and when a query results in a filed analysis page.
> To find pages relevant to a query, read this file first, then drill into specific pages.

---

## Sources
*One page per ingested raw source.*

*(none yet)*

---

## Concepts
*Ideas, frameworks, methodologies, themes.*

*(none yet)*

---

## Entities
*People, organizations, tools, products.*

*(none yet)*

---

## Analyses
*Filed answers to queries, comparisons, syntheses.*

*(none yet)*

---

## Quick Search Tips

To find pages by topic, look for keywords in the one-line summaries above.
To find all pages touching a source, check the `sources:` frontmatter on each page.
To see recent activity, read `log.md`.
```

**`wiki/log.md`**
```markdown
# Wiki Log

> Append-only chronological record of all wiki activity.
> Grep tip: `grep -E "^## \[" log.md | tail -5` gives the last 5 entries.

---

## [YYYY-MM-DD] init | Wiki created

- Cowork working folder selected and confirmed (Obsidian vault is configured separately to point at `wiki/`)
- Folder structure created: raw/, drafts/, wiki/inbox/, wiki/pages/{concepts,entities,sources,analyses}/, scheduled-tasks/ops/
- CLAUDE.md schema installed from blueprint template
- Scheduled-tasks ops files installed
- Wiki initialized and ready for first ingest
```

**`wiki/hot.md`**

Read the current schema version from `blueprint/template/CLAUDE.md`'s footer line (`Schema version: X.Y`). Do not hardcode — substitute the live value:

```markdown
---
updated: YYYY-MM-DD
---
Pages: 0 | Schema: vX.Y | Updated: YYYY-MM-DD
Last op: init YYYY-MM-DD (wiki created, ready for first ingest)
Gaps: none yet — add sources to discover gaps
Hot: none yet
Active skills: none
```

**`memory.md`** (at working folder root)
```markdown
<!-- MEMORY_STATE: EMPTY -->
# Session Memory

*(empty — use `!! wrap` at the end of a session to save a summary here)*
```

Replace all `YYYY-MM-DD` placeholders with today's date. Replace `vX.Y` in `hot.md` with the schema version read from `CLAUDE.md`.

---

## Step 4.5 — Offer SQLite Query Skill

Ask the user:

> "Would you like to install the SQLite query layer? It replaces the built-in grep-based lookup with a local database (`wiki.db`) for faster relationship queries — recommended if you expect your wiki to grow beyond ~500 pages. You can always install it later with `!! install sqlite-query`."

- **If yes:** run the `!! install sqlite-query` flow from `blueprint/skills/sqlite-query/SKILL.md` — skip the backfill step (no pages exist yet). On completion, continue to Step 5.
- **If no:** continue to Step 5. The basic grep layer is active by default.

---

## Step 5 — Configure Obsidian

Instruct the user to do this manually in Obsidian (you cannot do this via file edits):

> Open Obsidian and select **Open folder as vault**.
> Choose the **`wiki/`** folder — not the parent working folder.
> This keeps `raw/`, `blueprint/`, and `scheduled-tasks/` outside the vault so Obsidian only indexes wiki content.
>
> Then go to **Settings → Files and links → Default location for new notes**
> Set it to `pages`
>
> This prevents Obsidian from creating stray pages at the vault root when clicking unresolved wiki links.

> **Note on `.obsidian/`:** The blueprint's `.gitignore` ignores `.obsidian/` directories *inside the `blueprint/` repo*. Your actual Obsidian vault lives at `wiki/.obsidian/`, **outside** `blueprint/`, so this rule does not affect your personal vault settings — you do not need to edit `.gitignore` for your own use. (If you are distributing the blueprint to others and want to ship pre-configured vault settings along with it, you would need to bundle them at `blueprint/template/.obsidian/`, remove the `.obsidian/` line from `.gitignore`, and add a Step 2 copy rule that deploys `blueprint/template/.obsidian/` into the new `wiki/.obsidian/` on setup. This blueprint does not include that machinery today — most users don't need it.)

---

## Step 6 — Configure Obsidian Web Clipper

Instruct the user to do this manually in the Chrome extension settings:

> In the Obsidian Web Clipper extension settings:
> - Set vault to your `wiki/` folder
> - Set save location to `inbox`
> - Set output format to Markdown
>
> Clipped articles will land in `wiki/inbox/`. Claude will read them from there during ingest, then automatically move them to `raw/` (outside the vault) as an immutable archive.
> This saves 40–60% in token costs vs fetching URLs directly.

---

## Step 7 — Verify Setup

> **Reminder:** cwd persists between Bash commands in Cowork — verify with `pwd` if in doubt. You do not need to re-run `cd`. (Env vars like `$WORKDIR` do not persist; only cwd does.)

Check the following and report status to the user:

- [ ] `CLAUDE.md` exists at the working folder root
- [ ] `memory.md` exists at the working folder root (empty)
- [ ] `wiki/inbox/` folder exists
- [ ] `wiki/pages/` subfolders exist: `concepts/`, `entities/`, `sources/`, `analyses/`
- [ ] `wiki/index.md` exists with 0 pages
- [ ] `wiki/log.md` exists with init entry
- [ ] `wiki/hot.md` exists with today's date
- [ ] All 6 ops files exist in `scheduled-tasks/ops/`
- [ ] `scheduled-tasks/refresh-hot.md` exists
- [ ] `raw/` folder exists
- [ ] `drafts/` folder exists

---

## Step 8 — Announce Readiness

Tell the user:

> "Setup complete. Your wiki is ready.
>
> **Next step:** Clip an article with Obsidian Web Clipper — it will save to `wiki/inbox/`. Then tell me: `!! ingest [filename]`
>
> For daily usage, see `blueprint/user-guide.md`."

Then display the standard footer:
```
📥 !! ingest: [URL | Page Name | All]
🧹 !! lint: [Page Name | All]
🔍 !! audit: [Page Name | All]
💾 !! wrap: [save session summary to memory]
🔄 !! ready: [load session summary at start of new session]

💡 Using Obsidian Web Clipper to save articles as markdown before ingesting is 40–60% cheaper in token usage than fetching directly from a URL.
```
