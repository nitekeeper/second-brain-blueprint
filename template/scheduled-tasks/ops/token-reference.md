# Token Reference

Use this file to estimate token cost before any approval request.
Format: `~N tokens (R read / W write)`

## File Read Costs (last calibrated: YYYY-MM-DD — recalibrate after each ingest)

| File | Chars | Tokens (~chars÷4) |
|---|---|---|
| `wiki/hot.md` | ~210 | ~55 |
| `memory.md` | ~500 (when full) | ~125 |
| `CLAUDE.md` | ~9,200 | ~2,300 |
| `wiki/index.md` | ~800 (grows with pages) | ~200 |
| `wiki/log.md` tail (5 entries) | ~2,500 max (500 × 5 cap) | ~625 |
| `wiki/log.md` full | audit only — unbounded | — |
| `scheduled-tasks/refresh-hot.md` | ~1,735 | ~435 |
| `ops/ingest.md` | ~1,760 | ~440 |
| `ops/lint.md` | ~1,185 | ~295 |
| `ops/query.md` | ~1,455 | ~365 |
| `ops/update.md` | ~1,050 | ~260 |
| `ops/conventions.md` | ~1,555 | ~390 |
| `ops/token-reference.md` | ~1,900 | ~475 |
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
