# Op: INGEST

Triggered when the user drops a new source and says "ingest this."

## If `!! ingest all`

Before starting steps below:
1. List all files in `wiki/inbox/` (Bash: `ls wiki/inbox/`)
2. If empty, tell the user "Nothing in wiki/inbox/ to ingest." and stop
3. Show a combined approval request listing every filename, estimated total token cost, and all pages to be created/updated across the batch
4. Process each file in sequence using steps 1–12 below, skipping step 4 (individual approval request) — the combined approval above covers all files
5. Write one log entry per file (not one combined entry)

---

## Steps

1. Read the last 5 entries of `wiki/log.md` for recent context
2. Read the source file from `wiki/inbox/`
3. Discuss key takeaways with the user (brief, 3–5 bullets)
4. Show approval request (summary + token estimate + to-do list) and wait for confirmation
5. Write a source summary page in `wiki/pages/sources/`
6. Read `wiki/index.md` to identify all affected concept/entity pages
7. Update affected pages; create any new concept or entity pages warranted
8. Update `wiki/index.md` with new and modified entries
9. Move the source file from `wiki/inbox/` to `raw/` (use Bash mv)
10. Append entry to `wiki/log.md`:
    `## [YYYY-MM-DD] ingest | [Title]`
11. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
12. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section)

## Notes

- A single source typically touches 5–15 pages. Be thorough.
- Read `@scheduled-tasks/ops/conventions.md` before creating or editing any pages.
- Source pages must include: `original_file:` frontmatter, Key Takeaways section, Connections section.
