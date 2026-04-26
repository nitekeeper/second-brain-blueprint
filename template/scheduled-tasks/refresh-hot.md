# Task: Refresh hot.md

Overwrite `wiki/hot.md` with a fresh orientation snapshot after any operation that changes wiki state (Ingest, Lint, Update, filed Query, Audit-with-fix, `!! wrap`, `!! ready`). This keeps session startup cost low — the next session reads only hot.md instead of index.md and log.md.

---

## Steps

1. Read `wiki/index.md` — collect every entry line across ALL sections (Sources, Concepts, Entities, Analyses) by matching `^- \[\[`. The page count for `Pages: N` is the length of that list (not a separate counter anywhere in `index.md` — derived from the entries themselves so it cannot go stale). To identify the 5 pages with the most recent `updated:` dates, sort the same list in memory by the `updated: YYYY-MM-DD` field inside each line (ISO-8601 dates are lexicographically sortable) and take the top 5. If fewer than 5 total pages exist, list all of them; if none, emit `Hot: none yet` and `Pages: 0`.

   If a shell alternative is needed, extract the date into a leading sort key first — a naive `sort -t: -k2` is unsafe because any colon in a title or summary shifts the key off the date. Use `awk`'s **1-argument** `match(str, regex)` form (portable across GNU and BSD/macOS awk — it sets `RSTART` and `RLENGTH` on both). Avoid the 3-argument form `match(str, regex, array)`, which is a GNU-awk-only extension and silently produces no output on macOS's default BSD awk. Avoid `sed -E '... \t ...'` too — BSD sed does not interpret `\t` as a tab in the replacement string, so downstream `cut -f` breaks. Emitting the tab from awk guarantees a real tab byte:
   ```bash
   awk 'match($0, /updated: [0-9]{4}-[0-9]{2}-[0-9]{2}/) {
          d = substr($0, RSTART + 9, 10)
          print d "\t" $0
        }' wiki/index.md \
     | sort -r \
     | head -5 \
     | cut -f2-
   ```
   If you prefer a one-step Python alternative, use `pathlib` + `re.findall` and sort in memory — safer than any shell pipeline when titles may contain unusual punctuation.
2. Read `wiki/log.md` — get the last log entry (use `grep -E "^## \[" wiki/log.md | tail -1`) and the most recent open gaps list from the latest lint entry. `ops/lint.md` guarantees every lint entry contains a canonical `Gaps:` line immediately under the header, so extract the most recent one portably:
   ```bash
   grep -E '^Gaps:' wiki/log.md | tail -1 | sed -E 's/^Gaps:[[:space:]]*//'
   ```
   If no lint entry exists yet (no `Gaps:` line anywhere in `log.md`), use `none yet — add sources to discover gaps` as the Gaps value. If the most recent lint wrote `Gaps: none`, pass `none` through verbatim — it correctly reflects "lint ran and found no open gaps", which is different from "never linted".
3. **Derive `Active skills`:** Check each skill's hook or installed file:
   - `python scripts/file_check.py scheduled-tasks/query-layer.md` — if present, add `sqlite-query` to the list
   - `python scripts/file_check.py scheduled-tasks/claude-code-enhanced.md` — if present, add `claude-code-enhanced` to the list

   If neither is present, emit `none`. If one or more are present, emit them comma-separated (e.g. `sqlite-query, claude-code-enhanced`). When a new skill is added to the blueprint, add its detection check here at the same time.

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
Active skills: [comma-separated installed skill names, or "none"]
Python: [python | python3]
```

## Field Reference

| Field | Source |
|-------|--------|
| `updated` | Today's date (YYYY-MM-DD) |
| `Pages: N` | Count of `^- [[` entry lines across all sections of index.md (derived, not stored) |
| `Schema: vX.Y` | Current schema version in CLAUDE.md footer |
| `Updated: YYYY-MM-DD` | Today's date |
| `Last op` | Most recent `## [date] operation \| title` line in log.md |
| `Gaps` | Open gaps list from most recent lint entry in log.md |
| `Hot` | 5 pages with highest `updated:` dates in index.md |
| `Active skills` | `none` if no skill hook files present; otherwise comma-separated skill names derived from hook files in `scheduled-tasks/` (see Step 3) |
| `Python` | Preserved from existing `hot.md` — do not overwrite this field; copy the current value forward unchanged |

## Rules

- Keep total file size ≤500 characters — truncate Gaps or Hot lists if needed (verify with `wc -c wiki/hot.md` after writing)
- Never append — always overwrite the entire file
- Do not add any extra text, commentary, or blank lines beyond the format above
- Schema version must match the current value in `CLAUDE.md`'s footer — do not hardcode; read it fresh each refresh
