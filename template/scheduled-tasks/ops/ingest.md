# Op: INGEST

Triggered when the user drops a new source and says "ingest this."

## If `!! ingest all`

Before starting steps below:
1. List all files in `wiki/inbox/` (Bash: `ls wiki/inbox/`)
2. If empty, tell the user "Nothing in wiki/inbox/ to ingest." and stop
3. Show a combined approval request listing every filename, estimated total token cost, and all pages to be created/updated across the batch
4. Process each file in sequence using steps 1–11 below
5. Write one log entry per file (not one combined entry)

---

## Steps

1. Read the source file from `wiki/inbox/`
2. Discuss key takeaways with the user (brief, 3–5 bullets)
3. Show approval request (summary + token estimate + to-do list) and wait for confirmation
4. Write a source summary page in `wiki/pages/sources/`
5. Read `wiki/index.md` to identify all affected concept/entity pages
6. Update affected pages; create any new concept or entity pages warranted
7. Update `wiki/index.md` with new and modified entries
8. Move the source file from `wiki/inbox/` to `raw/` (use Bash mv)
9. Append entry to `wiki/log.md`:
   `## [YYYY-MM-DD] ingest | [Title]`
10. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
11. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section)

## Notes

- A single source typically touches 5–15 pages. Be thorough.
- Read `@scheduled-tasks/ops/conventions.md` before creating or editing any pages.
- Source pages must include: `original_file:` frontmatter, Key Takeaways section, Connections section.
