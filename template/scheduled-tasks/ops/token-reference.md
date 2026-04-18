# Token Reference

Use this file to estimate token cost before any approval request.
Format: `~N tokens (R read / W write)`

## File Read Costs (calibrated at setup — recalibrate after first ingest)

| File | Chars | Tokens (~chars÷4) |
|---|---|---|
| `wiki/hot.md` | ~400 | ~100 |
| `CLAUDE.md` | ~4,000 | ~1,000 |
| `wiki/index.md` | ~500 (grows with pages) | ~125 |
| `wiki/log.md` tail (5 entries) | ~1,600 | ~400 |
| `wiki/log.md` full | ~500 (grows with activity) | ~125 |
| `scheduled-tasks/refresh-hot.md` | ~1,600 | ~400 |
| `ops/ingest.md` | ~1,100 | ~275 |
| `ops/lint.md` | ~1,200 | ~300 |
| `ops/query.md` | ~1,100 | ~275 |
| `ops/update.md` | ~850 | ~215 |
| `ops/conventions.md` | ~1,500 | ~375 |
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

## Ingest Estimate Formula
`raw source read + (500 × pages to create) + (200 × pages to update) + 500 overhead`

## Recalibration Rule

Recalibrate this table after every INGEST operation:
1. Run `wc -c` on all key files listed above
2. Update the Chars column with actual values
3. Recalculate Tokens column (chars ÷ 4)
4. Update the calibration date in the header

Also recalibrate if any file grows by more than 20% since last calibration.
