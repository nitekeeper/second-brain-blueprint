# Token Reference

Use this file to estimate token cost before any approval request.
Format: `~N tokens (R read / W write)`

> **Estimates only:** Every number in this file is `chars ÷ 4`. Real token usage depends on the model's tokenizer, exact file contents, and runtime overhead (tool calls, system prompt) — treat these as rough planning figures, not precise accounting. Quote them as approximate when citing in approval requests.

> **Self-cost note:** This file itself is ~880 tokens to read. Every approval request requires reading it unless the relevant numbers are already cached in working memory from earlier in the same operation. Include the ~880-token cost in quoted estimates for the first approval of an operation; subsequent approvals within the same op can cache.

> **Source of truth:** The Chars column below is the source of truth for file-read cost estimates. Any quoted cost in CLAUDE.md, README.md, user-guide.md, or setup-guide.md must be re-derivable from this table — re-propagate when this table changes.

## File Read Costs (last calibrated: 2026-04-18 — recalibrate after each ingest)

| File | Chars | Tokens (~chars÷4) |
|---|---|---|
| `wiki/hot.md` | ~210 | ~55 |
| `memory.md` | ~500 (when full) | ~125 |
| `CLAUDE.md` | ~13,700 | ~3,430 |
| `wiki/index.md` | ~800 (grows with pages) | ~200 |
| `wiki/log.md` tail (5 entries) | ~2,500 max (500 × 5 cap) | ~625 |
| `wiki/log.md` full | audit only — unbounded | — |
| `scheduled-tasks/refresh-hot.md` | ~3,300 | ~830 |
| `ops/ingest.md` | ~3,800 | ~950 |
| `ops/lint.md` | ~1,800 | ~450 |
| `ops/query.md` | ~1,900 | ~480 |
| `ops/update.md` | ~1,500 | ~380 |
| `ops/conventions.md` | ~2,600 | ~650 |
| `ops/token-reference.md` | ~3,500 | ~880 |
| Average concept page | ~2,000 | ~500 |
| Average source page | ~1,500 | ~375 |
| Raw source document | varies | ~1,000–8,000 |

## Write Cost Estimates

| Action | Tokens |
|---|---|
| Write a new wiki page | ~400–600 |
| Edit an existing page | ~150–300 |
| Append to `log.md` | ~100 |
| Overwrite `hot.md` | ~100 |
| Write `memory.md` (`!! wrap`) | ~150–250 |
| Wipe `memory.md` (`!! ready`) | ~50 |

## Ingest Estimate Formula
`raw source read + (500 × pages to create) + (200 × pages to update) + 500 overhead`

## Recalibration Rule

**Headroom convention:** Chars column is set to ~110% of measured actual at calibration time, rounded to nearest 100. Tokens = chars ÷ 4, rounded to nearest 10. The 10% headroom absorbs small edits so the table doesn't need to move on every change.

**Recalibration trigger:** Fire immediately when any file's measured actual exceeds its documented Chars value — the headroom has been consumed. Also recalibrate after every INGEST operation as a routine pass.

**Steps:**
1. Run `wc -c` on all key files listed above
2. For each file, set Chars to 110% of measured actual, rounded to nearest 100
3. Recalculate Tokens column (chars ÷ 4, rounded to nearest 10)
4. Propagate changes to any cascading cold-start estimates (CLAUDE.md, user-guide.md, README.md)
5. Update the calibration date in the header
