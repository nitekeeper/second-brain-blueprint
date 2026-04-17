# Op: LINT

Triggered when the user says "lint the wiki" or "lint [page-name]".

## Steps

1. Read `wiki/index.md` to get the full page catalog
2. Read the last 5 entries of `wiki/log.md` for recent context
3. For each page in scope (all pages or named page), check for:
   - Broken `[[wiki links]]` — target page does not exist
   - Orphan pages — no inbound links from other pages
   - Stale claims — superseded by a newer source
   - Contradictions — conflicts between pages
   - Missing cross-references — concept mentioned but not linked
   - Data gaps — important topic with no page and no raw source
4. Report all findings to the user
5. Show approval request (summary + token estimate + to-do list) for any fixes
6. Apply approved fixes
7. Append entry to `wiki/log.md`:
   `## [YYYY-MM-DD] lint | [Summary of findings]`
8. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
9. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section)

## Notes

- Never fix without approval — always report first.
- Bulk edits across pages: use Python, never `sed -i` (leaves XX* temp files).
