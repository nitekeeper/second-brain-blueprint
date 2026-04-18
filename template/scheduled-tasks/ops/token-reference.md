# Token Reference

Use this file to estimate token cost before any approval request.
Format: `~N tokens (R read / W write)`

> **Estimates only:** Every number in this file is `chars ÷ 4`. Real token usage depends on the model's tokenizer, exact file contents, and runtime overhead (tool calls, system prompt) — treat these as rough planning figures, not precise accounting. Quote them as approximate when citing in approval requests.

> **Self-cost note:** This file itself is ~1,830 tokens to read. Every approval request requires reading it unless the relevant numbers are already cached in working memory from earlier in the same operation. Include the ~1,830-token cost in quoted estimates for the first approval of an operation; subsequent approvals within the same op can cache.

> **Source of truth:** The Chars column below is the source of truth for file-read cost estimates. Any quoted cost in CLAUDE.md, README.md, user-guide.md, or setup-guide.md must be re-derivable from this table — re-propagate when this table changes.

## File Read Costs (last calibrated: 2026-04-18 — recalibrate after each ingest)

| File | Chars | Tokens (~chars÷4) |
|---|---|---|
| `wiki/hot.md` | ~210 | ~55 |
| `memory.md` | ~3,000 (when full) | ~750 |
| `CLAUDE.md` | ~21,900 | ~5,475 |
| `wiki/index.md` | ~800 (grows with pages) | ~200 |
| `wiki/log.md` tail (5 entries) | ~2,500 max (500 × 5 cap) | ~625 |
| `wiki/log.md` full | audit only — unbounded | — |
| `scheduled-tasks/refresh-hot.md` | ~4,400 | ~1,100 |
| `scheduled-tasks/changelog-monitor.md` | ~8,500 | ~2,130 |
| `ops/ingest.md` | ~17,000 | ~4,250 |
| `ops/lint.md` | ~2,500 | ~630 |
| `ops/query.md` | ~2,100 | ~530 |
| `ops/update.md` | ~1,400 | ~350 |
| `ops/conventions.md` | ~5,000 | ~1,250 |
| `ops/audit.md` | ~7,200 | ~1,800 |
| `ops/token-reference.md` | ~7,300 | ~1,830 |
| `blueprint/README.md` | ~5,100 | ~1,280 |
| `blueprint/setup-guide.md` | ~13,400 | ~3,350 |
| `blueprint/user-guide.md` | ~16,600 | ~4,150 |
| `blueprint/troubleshooting.md` | ~33,200 | ~8,300 |
| `blueprint/CHANGELOG.md` | ~60,700 | ~15,180 |
| `blueprint/LICENSE` | ~1,200 | ~300 |
| Average concept page | ~2,000 | ~500 |
| Average source page | ~1,500 | ~375 |
| Raw source document | varies | ~1,000–8,000 |

> **Blueprint-doc rows apply only to blueprint-authoring sessions** (working inside `blueprint/` itself). A regular end-user wiki never reads these files — they ship with the distribution but live above `wiki/`. Include them in audit / blueprint-edit estimates only.

## Write Cost Estimates

| Action | Tokens |
|---|---|
| Write a new wiki page | ~400–600 |
| Edit an existing page | ~150–300 |
| Append to `log.md` | ~100 |
| Overwrite `hot.md` | ~100 |
| Write `memory.md` (`!! wrap`) | ~600–900 |
| Wipe `memory.md` (`!! ready`) | ~50 |

> **`!! wrap` / `!! ready` true session cost.** The per-touch costs above cover *only* the `memory.md` operation itself. Both commands also execute the full `hot.md` refresh flow (read `refresh-hot.md` ~1,100 + re-read `wiki/index.md` ~200 + re-read `wiki/log.md` tail ~625) and append one entry to `log.md` (~100). `!! ready` additionally reads the full `memory.md` (~750 when the summary is present) before wiping it. Realistic per-command cost when none of those files are already cached is ~2,800 tokens for `!! wrap` and ~2,825 for `!! ready`, not the raw ~50–900 range from the table above. All figures quoted here use the documented Tokens column above (so they stay consistent as the table recalibrates). Quote ~2,800 when asked unless the relevant reads are warm from a prior op in the same session. `!! wrap` and `!! ready` are **not** approval-gated (they are documented exceptions in `CLAUDE.md`'s Approval Rule), so `token-reference.md` itself does not need to be re-read for either command.

## Ingest Estimate Formula

`raw source read + log-tail + index read + token-reference self-cost + (500 × pages to create) + (200 × pages to update) + 500 overhead`

Concretely, the fixed-cost reads for a single-file ingest sum to roughly:
- `wiki/log.md` tail (Step 1) — ~625
- `wiki/index.md` (Step 8, first-file read under B3 cache) — ~200
- `ops/token-reference.md` self-cost (Step 4 approval, once per op) — ~1,830
- overhead for approval + acknowledgments — ~500

That fixed floor is ~3,155 tokens **before** the raw source and per-page writes are counted. Add the variable terms on top: raw source read (typically 1,000–8,000) plus 500 × new pages plus 200 × updated pages. `!! ingest all` pays the ~1,830 `token-reference.md` cost once for the whole batch (not per file), but pays the raw-source-read and per-page write terms once per file.

## Recalibration Rule

**Headroom convention:** Chars column is set to ~110% of measured actual at calibration time, rounded to nearest 100. Tokens = chars ÷ 4, rounded to nearest 10. The 10% headroom absorbs small edits so the table doesn't need to move on every change.

**Recalibration trigger:** Fire immediately when any file's measured actual exceeds its documented Chars value — the headroom has been fully consumed. Also fire pre-emptively when any file's remaining headroom drops below ~3% of its measured actual, so the trigger catches drift before it hard-fires mid-op (this codifies the pattern caught by audits #5 S2, #7 W1, #8 S1, and #9 S1). Also recalibrate after every INGEST operation as a routine pass.

**Steps:**
1. Run `wc -c` on all key files listed above
2. For each file, set Chars to 110% of measured actual, rounded to nearest 100
3. Recalculate Tokens column (chars ÷ 4, rounded to nearest 10)
4. Propagate changes to any cascading cold-start estimates (CLAUDE.md, user-guide.md, README.md)
5. Re-sum the blueprint-doc and template-side Tokens-column rows and verify the result still fits inside the `!! audit all` envelope quoted at `ops/audit.md:71` (currently `~30,000–54,000`). If the updated sum exceeds the upper bound, widen the envelope (documented sum + ~1,500–3,000 cushion, rounded to nearest 1,000) and cascade to every `!! audit all` mention — `ops/audit.md:71`, `user-guide.md` (both the command reference and the cost table), and the CHANGELOG entry for this patch. Additionally, widen the envelope when the cushion (upper bound minus documented sum) drops below ~2% of the upper bound (~1,080 tokens on a 54,000-token envelope), even if the sum is still inside the bound — this prevents the cushion from being exhausted by ordinary churn before the next calibration. If both the sum stays inside the bound AND the cushion stays above ~2%, no envelope edit is needed.
6. Update the calibration date in the header
