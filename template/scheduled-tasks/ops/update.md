# Op: UPDATE

Triggered when the user makes a correction, adds context, or requests a change mid-conversation.

## Steps

1. Identify the relevant page(s) to change
2. Show approval request (summary + token estimate + to-do list) and wait for confirmation
3. Apply the change to the relevant page(s)
4. Update the `updated:` date in each page's frontmatter
5. Append entry to `wiki/log.md`:
   `## [YYYY-MM-DD] update | [What changed]`
6. If the change affects the index summary, update `wiki/index.md`
7. Refresh `hot.md` if the update is significant — follow `@scheduled-tasks/refresh-hot.md`
8. Recalibrate token estimates if affected files grew significantly — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section)

## Notes

- Read `@scheduled-tasks/ops/conventions.md` before editing any pages.
- Keep updates atomic — one logical change per log entry.
- If a correction contradicts another page, flag the conflict before applying.
