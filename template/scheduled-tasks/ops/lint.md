# Op: LINT

Triggered when the user says "lint the wiki" or "lint [page-name]".

## Steps

1. Read `wiki/index.md` to get the full page catalog
2. Read the last 5 entries of `wiki/log.md` for recent context: run `python scripts/log_tail.py`
3. For each page in scope (all pages or named page), check for:
   - Broken `[[wiki links]]` — target page does not exist
   - Orphan pages — no inbound links from other pages
   - Stale claims — superseded by a newer source
   - Contradictions — conflicts between pages
   - Missing cross-references — concept mentioned but not linked
   - Data gaps — important topic with no page and no raw source
   - Missing `related:` field — page has no `related:` frontmatter at all
   - Dangling `related:` slugs — a slug listed in `related:` has no matching page file
   - Broken bidirectionality — page A lists page B in `related:` but page B does not list page A
4. Report all findings to the user
5. Show approval request (summary + token estimate + to-do list) for any fixes — run `python scripts/estimate_tokens.py <files-to-write>` to compute the estimate
6. If any approved fix creates or edits a page, read `@scheduled-tasks/ops/conventions.md` first — lint fixes are page writes and must obey the same conventions as ingest/update
7. Apply approved fixes
8. Append entry to `wiki/log.md` — **must be ≤500 chars total** and **must include a canonical `Gaps:` line** so `refresh-hot.md` can parse it deterministically:
   ```
   ## [YYYY-MM-DD] lint | [Summary of findings]
   Gaps: topic-a, topic-b, topic-c
   ```
   The `Gaps:` line is mandatory even when there are none — write `Gaps: none` in that case. List only open data gaps (comma-separated, lowercase slugs or short phrases); do not mix in resolved issues. If the whole entry would exceed 500 chars, compress the Summary line first and keep the Gaps line intact — `refresh-hot.md` depends on it.
9. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
10. **Post-op advisory.** Append the session advisory block from `@scheduled-tasks/ops/session-hygiene.md` (Post-op advisory block section) to this response. Set `SESSION_HEAVY = true`.

## Notes

- Never fix without approval — always report first.
- Bulk edits across pages: use Python, never `sed -i` (leaves XX* temp files).
- All bulk-edit snippets must `cd` to the working folder root first, or use absolute paths, so the glob doesn't silently match zero files.
