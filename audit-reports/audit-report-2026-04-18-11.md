# Blueprint Audit Report #11 — 2026-04-18

**Scope:** `!! audit all` — every tracked file under `blueprint/` (16 files, 188,590 bytes)
**Mode:** Blueprint-authoring (no `wiki/` at working-folder root; log-append and `hot.md` refresh skipped per `audit.md` Step 5 and `template/CLAUDE.md` Blueprint-authoring Mode)
**Disposition:** Read-only. No fixes applied. No approval requested.
**Schema version audited:** 2.0 (CHANGELOG head: v2.0.10)
**Prior reports reviewed:** #1 through #10 (all ten reports read in full before this pass)

---

## Chain of Verification — Intended Logic (restated before findings)

The blueprint distributes a self-maintaining LLM wiki with six load-bearing invariants that audit passes #6–#10 progressively hardened:

1. **Hash canonicalization pipeline** (`ops/ingest.md` §Hash Canonicalization) — 6-step body normalization (YAML-preamble strip → CRLF/CR→LF → whitespace collapse → blank-line collapse → trim → SHA-256 first-8-hex) makes `source_hash:` stable across trivial formatting drift.
2. **Rerun-proof ingest** — Step 0 hashes the normalized body and short-circuits if the stored `source_hash:` matches, guaranteeing idempotency.
3. **Atomic ingest ordering** — Step 5 pre-computes `ts`; Step 6 `mv inbox→raw/<slug>-<ts>.md`; Step 7 writes the source page citing the same `ts`. `${ts:?}` / `${file:?}` / `${slug:?}` / `${WORKDIR:?}` guards refuse to run if any variable is unset, and the same-Bash-invocation requirement compensates for Cowork's non-persistent env.
4. **`source_url:` reverse-lookup monitor** (v2.0.10 invariant) — `changelog-monitor.md` Step 1 builds a URL→source-page map by reading each source page's `source_url:` once per run, looks up monitored URLs by exact string match, and emits UNINGESTED for misses or AMBIGUOUS for duplicate matches. Replaces the pre-v2.0.10 slug-derivation rule that was literally unexecutable at the call site (Step 1 runs before the fetch, so no H1 is available).
5. **Derived `Pages: N` counter** — `refresh-hot.md` counts `^- [[` entry lines across all `index.md` sections rather than reading a stored number, so the counter cannot go stale.
6. **Token-reference source-of-truth** — `ops/token-reference.md` owns the Chars column for every tracked file; all downstream doc costs (CLAUDE.md cold-start, README.md, user-guide.md, setup-guide.md) re-derive from it. Hard trigger (measured ≥ documented) + soft trigger (<3% headroom) + envelope 2% cushion floor keep drift from accumulating.

Approval discipline: three documented exceptions — `!! wrap`, `!! ready`, `!! audit` (CLAUDE.md lines 58, 68–71). All other writes are approval-gated. Blueprint Sync Rule owns downstream propagation when schema/startup/ops/conventions change.

Versioning: CLAUDE.md footer and `hot.md` quote X.Y; CHANGELOG entries use X.Y.Z. Patch-level recalibrations inherit the X.Y displayed in the footer without bumping it.

---

## Audit Findings

### CRITICAL

**No critical findings.**

### WARNING

**No warnings found.**

### STYLE

**No style findings.**

### Questions for Clarification

**None.** Audits #6–#10 systematically closed the specification gaps; this pass found the blueprint in the steady state audit #10 described.

---

## Architectural Invariants — Verified

Every invariant from the Chain-of-Verification list was re-checked against the current file bodies:

| # | Invariant | Verified at | Status |
|---|---|---|---|
| 1 | Hash canonicalization pipeline | `ops/ingest.md` §Hash Canonicalization (6 steps, preamble strip before normalization) | ✅ intact |
| 2 | Rerun-proof ingest (Step 0 short-circuit) | `ops/ingest.md` Step 0 | ✅ intact |
| 3 | Atomic ingest ordering (Step 5 pre-compute ts → Step 6 mv → Step 7 write source page) | `ops/ingest.md:80–89`; `${ts:?}` / `${file:?}` / `${slug:?}` / `${WORKDIR:?}` guards present | ✅ intact |
| 4a | `source_url:` frontmatter mandatory on every source page | `ops/ingest.md:89`; Notes bullet `ops/ingest.md:105` | ✅ intact |
| 4b | Monitor Step 1 reverse-lookup by `source_url:` (exact match, no URL normalization) | `changelog-monitor.md:24–31` | ✅ intact |
| 4c | AMBIGUOUS status for duplicate matches | `changelog-monitor.md:28, 37–38, 65, 77` | ✅ intact |
| 4d | `source_url: unknown` pages excluded from the map | `changelog-monitor.md:29` | ✅ intact |
| 5 | Derived `Pages: N` counter (count `^- [[`, not stored) | `refresh-hot.md:9, 47` | ✅ intact |
| 5a | Portable awk 1-arg `match()` (BSD/GNU compatibility) | `refresh-hot.md:11–20` | ✅ intact |
| 6 | Token-reference source-of-truth | `ops/token-reference.md:10, 14` | ✅ intact |
| 7 | Three documented approval exceptions | `template/CLAUDE.md:58, 68–71` | ✅ intact (exact count "three" matches bullet count) |
| 8 | Blueprint-authoring Mode guard (`[ -e wiki/log.md ]` check) | `ops/audit.md:43, 45` | ✅ intact |
| 9 | Versioning split (X.Y in footer, X.Y.Z in CHANGELOG) | `template/CLAUDE.md:292` (`Schema version: 2.0`); CHANGELOG head `v2.0.10` | ✅ intact |
| 10 | Blueprint Sync Rule | `template/CLAUDE.md` matrix | ✅ intact |

All v2.0.10 invariants introduced by the audit #10 W1 fix are present and consistent with their documentation in CHANGELOG v2.0.10, `troubleshooting.md` (UNINGESTED and AMBIGUOUS entries), and the monitor/ingest sources.

---

## Recalibration Check

### Per-file headroom (all tracked files, `wc -c` on 2026-04-18)

| File | Documented Chars | Measured Chars | Headroom | Status |
|---|---:|---:|---:|---|
| `blueprint/README.md` | 5,100 | 4,644 | 9.82% | ✅ |
| `blueprint/setup-guide.md` | 13,400 | 12,204 | 9.80% | ✅ |
| `blueprint/user-guide.md` | 16,600 | 15,076 | 10.11% | ✅ |
| `blueprint/troubleshooting.md` | 33,200 | 30,220 | 9.86% | ✅ |
| `blueprint/CHANGELOG.md` | 60,700 | 55,265 | 9.83% | ✅ |
| `blueprint/LICENSE` | 1,200 | 1,067 | 12.47% | ✅ |
| `template/CLAUDE.md` | 21,900 | 19,875 | 10.19% | ✅ |
| `scheduled-tasks/refresh-hot.md` | 4,400 | 3,966 | 10.94% | ✅ |
| `scheduled-tasks/changelog-monitor.md` | 8,500 | 7,758 | 9.56% | ✅ |
| `ops/ingest.md` | 17,000 | 15,399 | 10.40% | ✅ |
| `ops/lint.md` | 2,500 | 2,243 | 11.46% | ✅ |
| `ops/query.md` | 2,100 | 1,901 | 10.47% | ✅ |
| `ops/update.md` | 1,400 | 1,305 | 7.28% | ✅ |
| `ops/conventions.md` | 5,000 | 4,500 | 11.11% | ✅ |
| `ops/audit.md` | 7,200 | 6,503 | 10.72% | ✅ |
| `ops/token-reference.md` | 7,300 | 6,664 | 9.54% | ✅ |

**Hard trigger (measured ≥ documented):** No file trips this trigger.
**Soft trigger (<3% headroom):** No file trips this trigger. The closest is `update.md` at 7.28%, still more than 2x the threshold. All other files sit at ≥9.54%.

### Envelope check

Documented Tokens column sum, re-summed by row:

- Blueprint-doc rows: 1,280 + 3,350 + 4,150 + 8,300 + 15,180 + 300 = **32,560**
- Template-side rows: 5,475 + 1,100 + 2,130 + 4,250 + 630 + 530 + 350 + 1,250 + 1,800 + 1,830 = **19,345**
- **Total: 51,905**

Envelope upper bound: **54,000**. Cushion = 54,000 − 51,905 = **2,095 tokens = 3.88% of upper bound**, safely above the 2% floor (1,080 tokens on a 54,000-token envelope).

Envelope is consistently quoted as `~30,000–54,000` across all four expected touchpoints (`ops/audit.md:71`, `user-guide.md:94`, `user-guide.md:215`, `ops/token-reference.md:79`). No drift.

### Cross-reference consistency

Cold-start figures (`~5,530` total, `~6,280` with `!! ready` summary, `~5,475` CLAUDE.md read cost) appear in the expected files (`README.md:64`, `user-guide.md:12, 14, 208, 209, 219, 240`, `template/CLAUDE.md:9, 17`). All quotations are internally consistent. Realistic `!! wrap` ~2,800 and `!! ready` ~2,825 appear in `user-guide.md:216–217` and in `ops/token-reference.md:54`, again internally consistent.

**No recalibration needed.** The table remains an accurate source of truth for every downstream quotation.

---

## Verdict

**No bugs found.**

This is the eleventh consecutive audit. Audits #1–#5 eliminated logic bugs and schema footguns; #6–#9 closed minor specification nits; #10 fixed the last latent architectural gap (the monitor's unexecutable slug-derivation rule) by re-platforming the monitor's lookup onto a mandatory `source_url:` reverse-lookup. This pass re-verified every invariant introduced by those fixes and re-ran the calibration check end-to-end.

The blueprint is in a true steady state:

- All tracked files sit at 7–13% headroom against their documented Chars — no hard-trigger or soft-trigger drift.
- The documented-Tokens sum (51,905) is inside the envelope (54,000) with a 3.88% cushion, above the 2% floor.
- Every cross-reference (cold-start, envelope, realistic session costs) is internally consistent.
- The v2.0.10 `source_url:` invariant is uniformly enforced: monitor Step 1 reverse-lookup, ingest Step 7 three-field frontmatter, troubleshooting entries for UNINGESTED and AMBIGUOUS, and Clipper `source_url: unknown` fallback with gap-note-in-approval — all present.
- Blueprint-authoring Mode guards correctly fired this pass (skipped the `wiki/log.md` append and the `hot.md` refresh since `wiki/` is absent). Audit is read-only, so no approval flow engaged.

Recommendation: continue to let the written Recalibration Rule and Blueprint Sync Rule carry routine maintenance. Future audits should fire only in response to a specific user concern or a scheduled post-release pass; the blueprint has earned the light-touch cadence audit #10 anticipated.

---

*Audit performed by: Senior Software Architect role per `ops/audit.md` Audit Prompt.*
*Files in scope: 16 (see `ops/audit.md` §If `!! audit all`).*
*Total read: ~51,905 documented tokens of file content, within the `~30,000–54,000` envelope.*
