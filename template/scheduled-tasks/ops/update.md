# Op: UPDATE

Triggered when the user makes a correction, adds context, or requests a change mid-conversation.

## Steps

1. Read the last 5 entries of `wiki/log.md` for recent context (`grep -E "^## \[" wiki/log.md | tail -5`)
2. Identify the relevant page(s) to change
3. Show approval request (summary + token estimate + to-do list) and wait for confirmation — include the cost of re-reading `token-reference.md` itself (~850 tokens) in the estimate
4. Apply the change to the relevant page(s)
5. Update the `updated:` date in each page's frontmatter
6. Append entry to `wiki/log.md` — **must be ≤500 chars total**:
   `## [YYYY-MM-DD] update | [What changed]`
   If the change touches many pages, list the count rather than full filenames.
7. If the change affects the index summary, update `wiki/index.md`
8. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
9. Recalibrate token estimates if any tracked file's actual size now exceeds its documented value — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section)

## Notes

- Read `@scheduled-tasks/ops/conventions.md` before editing any pages.
- Keep updates atomic — one logical change per log entry.
- If a correction contradicts another page, flag the conflict before applying.
