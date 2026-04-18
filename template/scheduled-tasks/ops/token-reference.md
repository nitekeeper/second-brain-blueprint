# Token Reference

Use this file to estimate token cost before any approval request.
Format: `~N tokens (R read / W write)`

> **Estimates only:** Every number in this file is `chars ÷ 4`. Real token usage depends on the model's tokenizer, exact file contents, and runtime overhead (tool calls, system prompt) — treat these as rough planning figures, not precise accounting. Quote them as approximate when citing in approval requests.

> **Self-cost note:** This file itself is ~1,130 tokens to read. Every approval request requires reading it unless the relevant numbers are already cached in working memory from earlier in the same operation. Include the ~1,130-token cost in quoted estimates for the first approval of an operation; subsequent approvals within the same op can cache.

> **Source of truth:** The Chars column below is the source of truth for file-read cost estimates. Any quoted cost in CLAUDE.md, README.md, user-guide.md, or setup-guide.md must be re-derivable from this table — re-propagate when this table changes.

## File Read Costs (last calibrated: 2026-04-18 — recalibrate after each ingest)

| File | Chars | Tokens (~chars÷4) |
|---|---|---|
| `wiki/hot.md` | ~210 | ~55 |
| `memory.md` | ~3,000 (when full) | ~750 |
| `CLAUDE.md` | ~20,800 | ~5,200 |
| `wiki/index.md` | ~800 (grows with pages) | ~200 |
| `wiki/log.md` tail (5 entries) | ~2,500 max (500 × 5 cap) | ~625 |
| `wiki/log.md` full | audit only — unbounded | — |
| `scheduled-tasks/refresh-hot.md` | ~4,100 | ~1,030 |
| `scheduled-tasks/changelog-monitor.md` | ~6,100 | ~1,530 |
| `ops/ingest.md` | ~12,300 | ~3,080 |
| `ops/lint.md` | ~2,500 | ~630 |
| `ops/query.md` | ~2,100 | ~530 |
| `ops/update.md` | ~1,400 | ~350 |
| `ops/conventions.md` | ~4,600 | ~1,150 |
| `ops/audit.md` | ~6,300 | ~1,580 |
| `ops/token-reference.md` | ~4,500 | ~1,130 |
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
| Write `memory.md` (`!! wrap`) | ~600–900 |
| Wipe `memory.md` (`!! ready`) | ~50 |

> **`!! wrap` / `!! ready` true session cost.** The per-touch costs above cover *only* the `memory.md` operation itself. Both commands also execute the full `hot.md` refresh flow (read `refresh-hot.md` ~1,030 + re-read `wiki/index.md` ~200 + re-read `wiki/log.md` tail ~625) and append one entry to `log.md` (~100). `!! ready` additionally reads the full `memory.md` (~750 when the summary is present) before wiping it. Realistic per-command cost when none of those files are already cached is ~2,700 tokens for `!! wrap` and ~2,800 for `!! ready`, not the raw ~50–900 range from the table above. Quote ~2,700 when asked unless the relevant reads are warm from a prior op in the same session. `!! wrap` and `!! ready` are **not** approval-gated (they are documented exceptions in `CLAUDE.md`'s Approval Rule), so `token-reference.md` itself does not need to be re-read for either command.

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
