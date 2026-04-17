# Setup Guide

> This file is written for AI execution. When the user says "read setup-guide.md and set it up", follow every step below in order. Ask for confirmation before any write action.

---

## Pre-flight Check

Before starting, confirm:
1. You have access to the vault folder (the Cowork working directory)
2. The `blueprint/` folder exists inside it (you are reading this file from there)
3. Ask the user: **"What is your name? I'll use it to personalize your wiki."** Wait for the answer before proceeding.

---

## Step 1 — Create Folder Structure

Show approval request, then execute:

```bash
mkdir -p raw
mkdir -p wiki/pages/concepts
mkdir -p wiki/pages/entities
mkdir -p wiki/pages/sources
mkdir -p wiki/pages/analyses
mkdir -p scheduled-tasks/ops
```

**What each folder is for:**
- `raw/` — drop source articles here before ingesting
- `wiki/pages/` — all wiki content organized by type
- `scheduled-tasks/` — agent operation instruction files

---

## Step 2 — Copy Template Files

Show approval request, then copy all files from `blueprint/template/` to their correct locations:

| From | To |
|---|---|
| `blueprint/template/wiki/CLAUDE.md` | `wiki/CLAUDE.md` |
| `blueprint/template/scheduled-tasks/refresh-hot.md` | `scheduled-tasks/refresh-hot.md` |
| `blueprint/template/scheduled-tasks/ops/ingest.md` | `scheduled-tasks/ops/ingest.md` |
| `blueprint/template/scheduled-tasks/ops/lint.md` | `scheduled-tasks/ops/lint.md` |
| `blueprint/template/scheduled-tasks/ops/query.md` | `scheduled-tasks/ops/query.md` |
| `blueprint/template/scheduled-tasks/ops/update.md` | `scheduled-tasks/ops/update.md` |
| `blueprint/template/scheduled-tasks/ops/conventions.md` | `scheduled-tasks/ops/conventions.md` |
| `blueprint/template/scheduled-tasks/ops/token-reference.md` | `scheduled-tasks/ops/token-reference.md` |

---

## Step 3 — Personalize CLAUDE.md

In `wiki/CLAUDE.md`, replace `[YourName]` with the name the user gave in the pre-flight check.

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

> In Obsidian, go to **Settings → Files and links → Default location for new notes**
> Set it to `wiki/pages`
>
> This prevents Obsidian from creating stray pages at the vault root when clicking unresolved wiki links.

---

## Step 6 — Configure Obsidian Web Clipper

Instruct the user to do this manually in the Chrome extension settings:

> In the Obsidian Web Clipper extension settings:
> - Set vault to your vault folder
> - Set save location to `raw/`
> - Set output format to Markdown
>
> This ensures clipped articles land in the right place for ingestion, and saves 40–60% in token costs vs fetching URLs directly.

---

## Step 7 — Verify Setup

Check the following and report status to the user:

- [ ] `wiki/CLAUDE.md` exists and contains the user's name
- [ ] `wiki/index.md` exists with 0 pages
- [ ] `wiki/log.md` exists with init entry
- [ ] `wiki/hot.md` exists with today's date
- [ ] All 6 ops files exist in `scheduled-tasks/ops/`
- [ ] `scheduled-tasks/refresh-hot.md` exists

---

## Step 8 — Announce Readiness

Tell the user:

> "Setup complete. Your wiki is ready.
>
> **Next step:** Clip an article with Obsidian Web Clipper — it will save to `raw/`. Then tell me: `ingest [filename]`
>
> For daily usage, see `blueprint/user-guide.md`."

Then display the standard footer:
```
📥 ingest: [URL | Page Name | All]
🧹 lint: [Page Name | All]

💡 Using Obsidian Web Clipper to save articles as markdown before ingesting is 40–60% cheaper in token usage than fetching directly from a URL.
```
