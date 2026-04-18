# Audit Report — 2026-04-18 (#6)

**Operation:** `!! audit all` (read-only blueprint-authoring audit)
**Scope:** Every tracked file under `blueprint/` — `README.md`, `setup-guide.md`, `user-guide.md`, `troubleshooting.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore`, and the full `template/` tree (`CLAUDE.md` + `scheduled-tasks/refresh-hot.md`, `changelog-monitor.md`, and `ops/*.md`).
**Mode:** Blueprint-authoring (no `wiki/` present at workspace root — `hot.md` refresh and `log.md` append correctly skipped per `CLAUDE.md` Blueprint-authoring Mode rule).
**Prior audit reports reviewed:** `audit-report-2026-04-18.md` through `audit-report-2026-04-18-05.md` (five prior reports, all findings landed in v2.0–v2.0.5).

---

## Chain of Verification

1. Read all five prior audit reports end-to-end and recorded the disposition of every CRITICAL / WARNING / STYLE / Question item so I would not re-flag already-fixed issues.
2. Read every file in scope in full: `blueprint/README.md`, `setup-guide.md`, `user-guide.md`, `troubleshooting.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore`, `template/CLAUDE.md`, `template/scheduled-tasks/refresh-hot.md`, `changelog-monitor.md`, and all six `ops/*.md` files (`ingest.md`, `lint.md`, `query.md`, `update.md`, `conventions.md`, `audit.md`, `token-reference.md`).
3. Spot-checked the v2.0.5 cold-start-cost propagation (`~5,530` / `~6,280`) across `CLAUDE.md`, `README.md`, `user-guide.md`, and `CHANGELOG.md` via Grep — found one stale instance still reading `~6,005` (see W1).
4. Spot-checked the v2.0.5 `!! audit all` envelope bump (`~30,000–40,000`) across `audit.md`, `user-guide.md`, and `CHANGELOG.md` via Grep — found one stale instance still reading `~25,000–35,000` (see W2).
5. Re-derived the `!! audit all` envelope from the `token-reference.md` Tokens column (blueprint-doc rows + template-side rows per the "source of truth" directive at `ops/audit.md:71`) and compared against the documented `~30,000–40,000` range (see W4).
6. Verified the atomic ingest ordering fix from v2.0.4 is still in place: `ingest.md` Step 5 pre-computes `ts`, Step 6 moves inbox → raw, Step 7 writes the source page. Cross-checked the `${ts:?…}` guard is present at `ingest.md:80`.
7. Verified the hash-canonicalization pipeline (v2.0.2) is consistent across `ingest.md` Step 0 and `changelog-monitor.md` Step 3 — still aligned.
8. Verified the "same rules as Step 7" cross-reference at `ingest.md:64` by reading Step 7 in full — the cross-reference is dangling (see W3).
9. Verified the `Pages:` derived-counter fix (v2.0.3) in `refresh-hot.md` still counts `^- \[\[` entries rather than reading a stored Stats header.
10. Verified the token-reference.md 110% headroom convention holds for every row by computing `110% × measured_actual ÷ 100 ≈ documented_chars` — no row has consumed its headroom since the 2026-04-18 calibration.
11. Verified every documented exception to the Approval Rule (`!! wrap`, `!! ready`, `!! audit`) is explicitly listed in `CLAUDE.md`'s Approval Rule section and matches `user-guide.md` / `README.md`.
12. Grepped for remaining stale `~2,455` (the pre-v2.0.5 ingest fixed floor) — one historical reference remains in `CHANGELOG.md:173` (see S1).

---

## Findings

### CRITICAL
None. The architectural invariants from the v2.0.4 atomic-ingest fix and the v2.0.2 hash-canonicalization fix remain intact. No data-loss, approval-bypass, or schema-divergence issues detected.

---

### WARNING

#### W1 — v2.0.5 cold-start propagation missed one prose reference in `user-guide.md`

**File:** `blueprint/user-guide.md:14`
**Severity:** WARNING (self-contradiction within the same document)

`user-guide.md:14` still quotes the pre-v2.0.5 figure:

> If you saved a session summary with `!! wrap`, say `!! ready` at the start of your next session — the agent will load and read that summary before clearing it (**~6,005 tokens** total when the summary is full).

But the same file at line 209 (the cost table), `template/CLAUDE.md:17`, and `CHANGELOG.md:79` all report the post-v2.0.5 figure `~6,280`:

> `template/CLAUDE.md:17`: Total cold-start cost: ~5,530 tokens (**~6,280 tokens** when memory.md holds a full summary loaded via `!! ready`)
> `user-guide.md:209`: Cold start with `!! ready` (full memory) | **~6,280**
> `CHANGELOG.md:79`: `~5,255` → `~5,530`, `!! ready` total `~6,005` → `~6,280`) propagated

The `CHANGELOG.md:79` entry for v2.0.5 explicitly claims this cascade was propagated, so the miss at line 14 is exactly the kind of drift the Blueprint Sync Rule exists to prevent. Users who open `user-guide.md` top-to-bottom will see a direct internal contradiction (~6,005 in the opening narrative vs ~6,280 in the reference table 195 lines later).

**Recommended fix:** Change `~6,005 tokens` → `~6,280 tokens` at `user-guide.md:14`.

---

#### W2 — v2.0.5 `!! audit all` envelope bump missed one prose reference in `user-guide.md`

**File:** `blueprint/user-guide.md:94`
**Severity:** WARNING (self-contradiction within the same document)

`user-guide.md:94` still quotes the pre-v2.0.5 envelope:

> `!! audit all` — audit every file under `blueprint/` (**~25,000–35,000 tokens**)

But line 215 of the same file and `template/scheduled-tasks/ops/audit.md:71` both quote the post-v2.0.5 envelope `~30,000–40,000`:

> `user-guide.md:215`: Audit all (full blueprint) | **~30,000–40,000**
> `ops/audit.md:71`: For `!! audit all`, expect **~30,000–40,000 tokens** of reads …

Same failure mode as W1: the v2.0.5 envelope update cascaded through `audit.md`, the `user-guide.md` cost table, and `CHANGELOG.md`, but missed the command reference at line 94. Within `user-guide.md` the two values directly contradict each other (line 94 vs line 215, 121 lines apart).

**Recommended fix:** Change `~25,000–35,000 tokens` → `~30,000–40,000 tokens` at `user-guide.md:94`.

---

#### W3 — Dangling cross-reference in `ingest.md` Step 0

**File:** `blueprint/template/scheduled-tasks/ops/ingest.md:64`
**Severity:** WARNING (load-bearing reference points at content that does not exist)

Step 0 derives the source-page slug and says:

> Derive the expected source-page slug — **same rules as Step 7** (lowercase-hyphenated from the H1 or filename stem; for URL ingest reuse the U2 slug).

I read Step 7 (line 86) in full:

> Write (or regenerate) a source summary page in `wiki/pages/sources/`. The frontmatter MUST include `source_hash: <8-char-hex>` … `original_file: raw/<slug>-<ts>.md` using the Step-5 `ts`. …

Step 7 contains **no** slug-derivation rules — it consumes a pre-computed `${slug}`. The actual rules cited in the parenthetical at line 64 ("lowercase-hyphenated from the H1 or filename stem; for URL ingest reuse the U2 slug") are the canonical rules, but they live inline in Step 0 itself (and in the U2 lineage for URL ingest), not in Step 7.

This is a semantic pointer to nothing. An agent following the cross-reference will find no rules in Step 7 and either fall back to the inline parenthetical (lucky) or invent a rule (unlucky — this is the class of error that causes cross-path hash mismatches between Clipper ingest and URL monitor fetch, since both paths must derive the identical slug).

**Recommended fix:** Drop the "same rules as Step 7" clause so the inline parenthetical is the source of truth, e.g.:

> Derive the expected source-page slug (lowercase-hyphenated from the H1 or filename stem; for URL ingest reuse the U2 slug).

Alternately, move the rules into a single named anchor (e.g. a `### Slug derivation` sub-heading in `conventions.md`) and point both Step 0 and any future reference at it.

---

#### W4 — `!! audit all` envelope source-of-truth arithmetic does not match the stated range

**File:** `blueprint/template/scheduled-tasks/ops/audit.md:71`
**Severity:** WARNING (self-referential spec disagrees with its own cited source)

`ops/audit.md:71` declares:

> For `!! audit all`, expect ~30,000–40,000 tokens of reads (envelope measured 2026-04-18 after blueprint docs grew through v2.0.5; **source of truth is the sum of blueprint-doc and template-side rows in `token-reference.md`** — re-derive from that table rather than hand-tuning this figure).

Summing the documented Tokens column from `ops/token-reference.md` (2026-04-18 calibration):

Blueprint-doc rows: README 1,280 + setup-guide 3,350 + user-guide 4,150 + troubleshooting 6,980 + CHANGELOG 8,480 + LICENSE 300 = **24,540**
Template-side rows: CLAUDE.md 5,475 + refresh-hot 1,100 + changelog-monitor 1,530 + ingest 3,880 + lint 630 + query 530 + update 350 + conventions 1,250 + audit 1,650 + token-reference 1,500 = **17,895**
**Total: ~42,435 tokens**

42,435 is above the stated upper bound of 40,000. The 110% headroom convention baked into the Chars column means the Tokens column will always overshoot measured actuals by ~10% — but the spec in `audit.md:71` points at that column as the source of truth without acknowledging the headroom gap. Re-deriving from the table exactly as instructed produces a number outside the stated envelope.

Two ways to resolve:
- **Option A (tighter):** Bump the envelope in `audit.md:71` (and the cascade in `user-guide.md:215`, `CHANGELOG.md`) to `~30,000–45,000 tokens` so the documented-column sum fits inside the range.
- **Option B (cleaner):** Change the "source of truth" directive to say "measured actuals (run `wc -c` on the files and divide by 4)" rather than the documented Tokens column, since those are the numbers that actually fit inside the envelope. Keep the 110% headroom convention as-is for per-file estimates where it does its job; just don't use it as the basis for the aggregate envelope.

Either option is defensible; leaving the current mismatch in place means the spec contradicts the arithmetic it tells you to do.

---

### STYLE

#### S1 — Historical `~2,455` floor in `CHANGELOG.md:173` now stale

**File:** `blueprint/CHANGELOG.md:173`

`CHANGELOG.md:173` describes the v2.0.3 ingest-estimate formula state with:

> … **~2,455-token fixed floor** before variable reads.

The current floor (per `ops/token-reference.md:66`) is `~2,825` — bumped in v2.0.5 when the `token-reference.md` self-cost row went from `~1,250` to `~1,500`.

The prior audit convention (reaffirmed across reports #2 through #5) is that historical CHANGELOG prose is **not** rewritten when superseded, because the CHANGELOG is an append-only record of what was true at each version. Under that convention this is working as designed. I am flagging it as STYLE rather than WARNING because there is a weak case for a one-time editorial pass — someone skimming the CHANGELOG today for the current floor will pick up the stale figure without noticing they're reading a v2.0.3 entry.

**No fix recommended unless the convention changes.** If a convention change is desired, the cleanest approach is to add a short "current state" inline note (e.g. "superseded by v2.0.5; current floor ~2,825") rather than rewriting the historical figure.

---

#### S2 — `ops/audit.md` token-reference row is the only row documented without a measured-actual anchor

**File:** `blueprint/template/scheduled-tasks/ops/token-reference.md:29`

Every other row in the File Read Costs table was calibrated on 2026-04-18 against a measured `wc -c`. The `ops/audit.md` row (`~6,600 chars / ~1,650 tokens`) is consistent with the 110% rule against its current length, so the row is not stale — but I could not find a recorded calibration artifact for it in any prior audit report. This is a recordkeeping observation, not a correctness issue: the number is correct today, it just hasn't been explicitly cross-checked in the prior audits the way the other ops files have been.

**No fix recommended.** Noted only so the next recalibration pass explicitly verifies this row rather than trusting it by transitive consistency.

---

## Questions for Clarification

### Q1 — Per-file schema-version footer parity (carried forward from audits #3, #4, #5)

`template/scheduled-tasks/changelog-monitor.md` ends with a `<!-- Schema vX.Y -->`-style footer; `refresh-hot.md` and the six `ops/*.md` files do not. The asymmetry has persisted across the last three audits unresolved.

Two consistent answers are available:
- **Normalize up:** every template file gets a schema footer (aligns with the "single source of truth" philosophy of the Blueprint Sync Rule).
- **Normalize down:** `changelog-monitor.md` drops its footer (aligns with the fact that the canonical version lives in `CLAUDE.md` and `hot.md`, and per-file footers are a parallel source that must be kept in sync).

If neither normalization is desired, a one-line comment in `CLAUDE.md` or `conventions.md` explaining *why* the asymmetry exists would close the question.

---

## Verdict

**PASS with drift.** The blueprint is architecturally sound: the v2.0.4 atomic-ingest ordering, the v2.0.2 hash canonicalization, the v2.0.3 derived `Pages:` counter, and the v2.0.5 self-cost propagation all hold. No CRITICAL findings.

The four WARNINGs are the normal kind of drift an audit exists to catch:
- W1 / W2 are the same failure mode — a v2.0.5 cascade that cleaned up the cost tables and the canonical specs but missed two prose references in `user-guide.md`. Both produce *intra-file* contradictions, which are the highest-visibility type. One-line fixes each.
- W3 is a small semantic defect in a load-bearing spec (`ingest.md` Step 0's cross-reference points at nothing). Low risk today because the inline parenthetical is correct, but the class-of-error it belongs to (slug derivation divergence between ingest paths) is exactly what v2.0.2 hardened against.
- W4 is a self-referential inconsistency between the envelope range and the table it cites as source of truth. Resolvable by either loosening the range or re-pointing the source-of-truth directive.

The STYLE items and Q1 are editorial / convention questions. None block the blueprint from being distributed.

**Recommended next action:** If you want me to fix, the minimum viable patch is W1 + W2 (two string replacements in `user-guide.md`) plus W3 (dropping the dangling clause in `ingest.md:64`). W4 requires a directional choice between Option A (loosen envelope) or Option B (re-point source of truth) before I can apply it. Per the audit op's read-only contract, I will wait for explicit approval before touching any file.
