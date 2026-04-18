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
3. Ask the user: **"What is your name? I'll use it to personalize your wiki."** Wait for the answer before proceeding.

---

## Step 1 — Create Folder Structure

Show approval request, then execute:

```bash
mkdir -p raw
mkdir -p drafts
mkdir -p wiki/inbox
mkdir -p wiki/pages/concepts
mkdir -p wiki/pages/entities
mkdir -p wiki/pages/sources
mkdir -p wiki/pages/analyses
mkdir -p scheduled-tasks/ops
```

**What each folder is for:**
- `raw/` — immutable source archive; Claude moves files here after ingesting
- `drafts/` — Claude's scrapbook for in-progress planning and drafting; outside the Obsidian vault
- `wiki/inbox/` — drop clipped articles here; Obsidian Web Clipper saves here
- `wiki/pages/` — all wiki content organized by type
- `scheduled-tasks/` — agent operation instruction files

---

## Step 2 — Copy Template Files

Show approval request, then copy all files from `blueprint/template/` to their correct locations:

| From | To |
|---|---|
| `blueprint/template/CLAUDE.md` | `CLAUDE.md` |
| `blueprint/template/scheduled-tasks/refresh-hot.md` | `scheduled-tasks/refresh-hot.md` |
| `blueprint/template/scheduled-tasks/ops/ingest.md` | `scheduled-tasks/ops/ingest.md` |
| `blueprint/template/scheduled-tasks/ops/lint.md` | `scheduled-tasks/ops/lint.md` |
| `blueprint/template/scheduled-tasks/ops/query.md` | `scheduled-tasks/ops/query.md` |
| `blueprint/template/scheduled-tasks/ops/update.md` | `scheduled-tasks/ops/update.md` |
| `blueprint/template/scheduled-tasks/ops/conventions.md` | `scheduled-tasks/ops/conventions.md` |
| `blueprint/template/scheduled-tasks/ops/token-reference.md` | `scheduled-tasks/ops/token-reference.md` |

---

## Step 3 — Personalize CLAUDE.md

In `CLAUDE.md`, replace `[YourName]` with the name the user gave in the pre-flight check.

---

## Step 4 — Initialize Wiki Files

Show approval request, then create these three files:

**`wiki/index.md`**
```markdown
# Wiki Index

> Master catalog of all pages. Updated on every ingest, query, or lint pass.
> To find pages relevant to a query, read this file first, then drill into specific pages.

**Stats:** 0 pages | Last updated: YYYY-MM-DD

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
> Grep tip: `grep "^## \[" log.md | tail -10` gives the last 10 entries.

---

## [YYYY-MM-DD] init | Wiki created

- Vault folder selected and confirmed
- Folder structure created: raw/, wiki/pages/concepts/, entities/, sources/, analyses/
- CLAUDE.md schema installed from blueprint template
- Scheduled-tasks ops files installed
- Wiki initialized and ready for first ingest
```

**`wiki/hot.md`**
```markdown
---
updated: YYYY-MM-DD
---
Pages: 0 | Schema: v1.3 | Updated: YYYY-MM-DD
Last op: init YYYY-MM-DD (wiki created, ready for first ingest)
Gaps: none yet — add sources to discover gaps
Hot: none yet
```

Replace all `YYYY-MM-DD` placeholders with today's date.

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

Check the following and report status to the user:

- [ ] `CLAUDE.md` exists at the Library root and contains the user's name
- [ ] `wiki/inbox/` folder exists
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
> **Next step:** Clip an article with Obsidian Web Clipper — it will save to `wiki/inbox/`. Then tell me: `ingest [filename]`
>
> For daily usage, see `blueprint/user-guide.md`."

Then display the standard footer:
```
📥 ingest: [URL | Page Name | All]
🧹 lint: [Page Name | All]

💡 Using Obsidian Web Clipper to save articles as markdown before ingesting is 40–60% cheaper in token usage than fetching directly from a URL.
```
