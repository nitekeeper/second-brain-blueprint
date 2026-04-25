# Op: UPDATE

Triggered when the user makes a correction, adds context, or requests a change mid-conversation.

## Steps

1. Read the last 5 entries of `wiki/log.md` for recent context (run `python scripts/log_tail.py`)
2. Identify the relevant page(s) to change
3. Show approval request (summary + token estimate + to-do list) and wait for confirmation
4. Apply the change to the relevant page(s)
5. Update the `updated:` date in each page's frontmatter. If the change touches a page's `related:` field, maintain bidirectionality — add the changed page's slug to any newly linked page's `related:` list, and remove it from any unlinked page's list.
5.5. If `scheduled-tasks/ingest-hook.md` exists, read it and execute it for each page touched — passing `slug`, `title`, `type`, `summary`, `tags`, `created`, `updated`, `related` from working memory. Hook errors are non-fatal; log a warning and continue.
6. Append entry to `wiki/log.md` — **must be ≤500 chars total**:
   `## [YYYY-MM-DD] update | [What changed]`
   If the change touches many pages, list the count rather than full filenames.
7. If the change affects the index summary, update `wiki/index.md`
8. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`

## Notes

- Read `@scheduled-tasks/ops/conventions.md` before editing any pages.
- Keep updates atomic — one logical change per log entry.
- If a correction contradicts another page, flag the conflict before applying.
- `related:` bidirectionality is enforced in Step 5 — treat it the same way `!! lint` does: every link must be mutual.
