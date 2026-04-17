# Task: Refresh hot.md

Overwrite `wiki/hot.md` with a fresh orientation snapshot after any operation that changes wiki state (Ingest, Lint, Update). This keeps session startup cost low — the next session reads only hot.md instead of index.md and log.md.

---

## Steps

1. Read `wiki/index.md` — get the current page count from the Stats header line
2. Read `wiki/log.md` — get the last log entry (use `grep "^## \[" log.md | tail -1`) and the most recent open gaps list from the latest lint entry
3. Read `wiki/index.md` again — identify the 5 pages with the most recent `updated:` dates

## Output Format

Overwrite `wiki/hot.md` with exactly this structure. Total file content must be ≤500 characters.

```
---
updated: YYYY-MM-DD
---
Pages: N | Schema: vX.X | Updated: YYYY-MM-DD
Last op: [operation] YYYY-MM-DD ([one-line result])
Gaps: [comma-separated open data gaps]
Hot: [comma-separated titles of 5 most recently updated pages]
```

## Field Reference

| Field | Source |
|-------|--------|
| `updated` | Today's date (YYYY-MM-DD) |
| `Pages: N` | Stats line in index.md |
| `Schema: vX.X` | Current schema version in CLAUDE.md footer |
| `Updated: YYYY-MM-DD` | Today's date |
| `Last op` | Most recent `## [date] operation \| title` line in log.md |
| `Gaps` | Open gaps list from most recent lint entry in log.md |
| `Hot` | 5 pages with highest `updated:` dates in index.md |

## Rules

- Keep total file size ≤500 characters — truncate Gaps or Hot lists if needed
- Never append — always overwrite the entire file
- Do not add any extra text, commentary, or blank lines beyond the format above
