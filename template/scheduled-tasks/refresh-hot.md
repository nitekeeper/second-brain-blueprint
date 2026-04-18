# Task: Refresh hot.md

Overwrite `wiki/hot.md` with a fresh orientation snapshot after any operation that changes wiki state (Ingest, Lint, Update). This keeps session startup cost low — the next session reads only hot.md instead of index.md and log.md.

---

## Steps

1. Read `wiki/index.md` — get the current page count from the Stats header line. To identify the 5 pages with the most recent `updated:` dates, collect every entry line across ALL sections (Sources, Concepts, Entities, Analyses), then sort in memory by the `updated: YYYY-MM-DD` field inside each line (ISO-8601 dates are lexicographically sortable) and take the top 5. If fewer than 5 total pages exist, list all of them; if none, emit `Hot: none yet`.

   If a shell alternative is needed, extract the date into a leading sort key first — a naive `sort -t: -k2` is unsafe because any colon in a title or summary shifts the key off the date. Use `sed` (portable across GNU and BSD/macOS) rather than `awk`'s `match(string, regex, array)` three-arg form — that form is a GNU-awk-only extension and silently produces no output on macOS's default BSD awk:
   ```bash
   grep -oE '\[\[[^]]+\]\].*updated: [0-9]{4}-[0-9]{2}-[0-9]{2}' wiki/index.md \
     | sed -E 's/.*updated: ([0-9]{4}-[0-9]{2}-[0-9]{2}).*/\1\t&/' \
     | sort -r \
     | head -5 \
     | cut -f2-
   ```
   If you prefer a one-step Python alternative, use `pathlib` + `re.findall` and sort in memory — safer than any shell pipeline when titles may contain unusual punctuation.
2. Read `wiki/log.md` — get the last log entry (use `grep -E "^## \[" wiki/log.md | tail -1`) and the most recent open gaps list from the latest lint entry. If no lint entry exists yet, use `none yet — add sources to discover gaps` as the Gaps value.

## Output Format

Overwrite `wiki/hot.md` with exactly this structure. Total file content must be ≤500 characters.

```
---
updated: YYYY-MM-DD
---
Pages: N | Schema: vX.Y | Updated: YYYY-MM-DD
Last op: [operation] YYYY-MM-DD ([one-line result])
Gaps: [comma-separated open data gaps]
Hot: [comma-separated titles of 5 most recently updated pages]
```

## Field Reference

| Field | Source |
|-------|--------|
| `updated` | Today's date (YYYY-MM-DD) |
| `Pages: N` | Stats line in index.md |
| `Schema: vX.Y` | Current schema version in CLAUDE.md footer |
| `Updated: YYYY-MM-DD` | Today's date |
| `Last op` | Most recent `## [date] operation \| title` line in log.md |
| `Gaps` | Open gaps list from most recent lint entry in log.md |
| `Hot` | 5 pages with highest `updated:` dates in index.md |

## Rules

- Keep total file size ≤500 characters — truncate Gaps or Hot lists if needed (verify with `wc -c wiki/hot.md` after writing)
- Never append — always overwrite the entire file
- Do not add any extra text, commentary, or blank lines beyond the format above
- Schema version must match the current value in `CLAUDE.md`'s footer — do not hardcode; read it fresh each refresh
