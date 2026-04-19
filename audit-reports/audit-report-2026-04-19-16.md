# Blueprint Audit Report — 2026-04-19 (#26)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.21 (per CHANGELOG.md; latest entry is v2.0.21)  
**Prior audit reviewed:** #25 (`audit-report-2026-04-19-15.md`) — read in full before this pass per user instruction  
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)  
**Mode:** Blueprint-authoring (no `wiki/` present at working-folder root; log append and `hot.md` refresh skipped)  
**Note:** Audit reports directory (`audit-reports/`) excluded from scope per standing user instruction.

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**

- `README.md` (4,671 chars)
- `setup-guide.md` (10,564 chars)
- `user-guide.md` (14,219 chars)
- `troubleshooting.md` (22,670 chars)
- `CHANGELOG.md` (79,076 chars — v2.0.21 and prior entries read; head of file only per new scope rule; see §1.2)
- `LICENSE` (1,067 chars)
- `.gitignore` (65 chars)

**Template**

- `template/CLAUDE.md` (20,641 chars)
- `template/scheduled-tasks/refresh-hot.md` (3,966 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,877 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/query.md` (2,586 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars)
- `template/scheduled-tasks/ops/audit.md` (5,908 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,746 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (4,185 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,533 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,838 chars)

**Not in audit scope:** `ROADMAP.md` (planning doc, no logic content). `CHANGELOG.md` is now also formally out of scope per v2.0.21 (its head was read to identify the latest version; it was not audited for logic errors).

---

### 1.2 Files changed since audit #25

Three files changed. All others (15 tracked files) are byte-for-byte identical to audit #25.

| File | Audit #25 bytes | This audit bytes | Delta | Cause |
|---|---:|---:|---:|---|
| `CHANGELOG.md` | 77,900 | 79,076 | +1,176 | v2.0.21 entry added |
| `ops/audit.md` | 6,357 | 5,908 | −449 | CHANGELOG scope line + warning note removed; `+` stripped from envelope |
| `user-guide.md` | 14,221 | 14,219 | −2 | Two `~30,000–43,000+` → `~30,000–43,000` |

---

### 1.3 v2.0.21 changes verified

v2.0.21 was applied between audit #25 and this pass. It declares two changes:

**Change 1 — `blueprint/CHANGELOG.md` removed from `!! audit all` scope:**

| Claim | File | Re-verified |
|---|---|---|
| `blueprint/CHANGELOG.md` line removed from `ops/audit.md` scope list | `ops/audit.md` §"If `!! audit all`" | ✓ CHANGELOG.md not present in scope enumeration |
| Companion warning note (v2.0.19) removed | `ops/audit.md` §Notes | ✓ No CHANGELOG warning note in Notes section |
| `~30,000–43,000+` → `~30,000–43,000` in `ops/audit.md:71` | `ops/audit.md` line 71 | ✓ Reads `~30,000–43,000` |
| `~30,000–43,000+` → `~30,000–43,000` in `user-guide.md` (both occurrences) | `user-guide.md` lines 94 and 201 | ✓ Both read `~30,000–43,000` (no `+`) |

**Change 2 — v2.0.18 arithmetic residual corrected (audit #25 S1):**

| Claim | File | Re-verified |
|---|---|---|
| `75,344 × 1.25 = 94,180` → `75,346 × 1.25 = 94,182.5` in v2.0.18 section | `CHANGELOG.md` v2.0.18 section | ✓ Line reads: `"75,346 × 1.25 = 94,182.5 → **~94,200 / ~23,550**"` |
| Arithmetic conclusion unchanged (~94,200) | `CHANGELOG.md` v2.0.18 section | ✓ `~94,200` confirmed |
| No cascade required | — | ✓ No other files reference this arithmetic |

**Prior audit #25 S1 status: FULLY RESOLVED.** Both the narrative sentence (corrected in v2.0.20) and the adjacent arithmetic line (corrected in v2.0.21) now agree. The cascade-miss class entry is closed.

---

### 1.4 Per-file headroom check (Recalibration Rule Steps 1–2)

Convention: ~125% of measured actual at calibration, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom % | 10% Soft Floor | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | 467 | ok |
| `setup-guide.md` | 10,564 | ~13,200 | 24.9% | 1,056 | ok |
| `user-guide.md` | 14,219 | ~17,800 | 25.2% | 1,422 | ok |
| `troubleshooting.md` | 22,670 | ~28,300 | 24.8% | 2,267 | ok |
| `CHANGELOG.md` | 79,076 | not tracked | — | — | ok |
| `LICENSE` | 1,067 | ~1,400 | 31.2% | 107 | ok |
| `template/CLAUDE.md` | 20,641 | ~25,800 | 25.0% | 2,064 | ok |
| `refresh-hot.md` | 3,966 | ~5,100 | 28.6% | 397 | ok |
| `ops/ingest.md` | 15,877 | ~19,800 | 24.7% | 1,588 | ok |
| `ops/lint.md` | 2,507 | ~3,100 | 23.7% | 251 | ok |
| `ops/query.md` | 2,586 | ~3,300 | 27.6% | 259 | ok |
| `ops/update.md` | 1,881 | ~2,400 | 27.6% | 188 | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 24.6% | 674 | ok |
| `ops/audit.md` | 5,908 | ~8,200 | 38.8% | 591 | ok |
| `ops/token-reference.md` | 6,746 | ~8,500 | 26.0% | 675 | ok |
| `skills/sqlite-query/SKILL.md` | 4,185 | ~5,200 | 24.2% | 419 | ok |
| `skills/sqlite-query/query-layer.md` | 2,533 | ~3,200 | 26.3% | 253 | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,838 | ~3,500 | 23.3% | 284 | ok |

No hard triggers. No soft triggers. Minimum headroom remains 23.3% (`ingest-hook.md` — unchanged since audit #24). No recalibration required.

`ops/audit.md` headroom widened from 29.0% (audit #25) to 38.8% because the file shrank 449 bytes. The documented Chars value (~8,200) is now a larger overestimate than usual; this will self-correct on the next routine ingest recalibration pass, which recalibrates all tracked files regardless of trigger state.

---

### 1.5 Envelope check (Recalibration Rule Step 5)

Unchanged from audit #25. No token-reference.md rows changed. Table sum 40,820 tokens; envelope `~30,000–43,000`; cushion 2,180 tokens (5.07% of 43,000 — above the 2% floor of ~860). No envelope widening required.

---

### 1.6 Cross-reference sanity checks

All cross-references verified in audit #25 re-verified. Spot-checks most relevant to v2.0.21:

- `template/CLAUDE.md:9` cold-start self-cost `~6,450` — matches token-reference CLAUDE.md row. ✓
- `template/CLAUDE.md:17` cold-start total `~6,530` — 6,450 (CLAUDE.md) + 80 (hot.md). ✓
- `user-guide.md:94` audit-all `~30,000–43,000` — matches `ops/audit.md:71` (no `+`). ✓
- `user-guide.md:201` "Audit all (full blueprint) | ~30,000–43,000" — consistent (no `+`). ✓
- `ops/token-reference.md` Step 5 `(currently ~30,000–43,000)` — consistent with ops/audit.md:71. ✓
- `ops/token-reference.md` floor note `(~860 tokens on a 43,000-token envelope)` — 43,000 × 2% = 860. ✓
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:70–72`, `README.md:73`, and `user-guide.md:175`. ✓
- Blueprint Sync Rule 12-row matrix — intact. ✓
- Versioning split (`Schema version: 2.0` in CLAUDE.md footer; patch bumps X.Y.Z in CHANGELOG only) — consistent. ✓
- `ops/audit.md:71` envelope `~30,000–43,000` — consistent with token-reference sum. ✓
- `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading. ✓
- **CHANGELOG.md v2.0.18 arithmetic** now reads `75,346 × 1.25 = 94,182.5 → ~94,200` — corrected. ✓ (S1 from audit #25 closed.)

---

## 2. Findings

### CRITICAL

None.

### WARNING

None.

### STYLE

None.

---

## 3. Non-findings (considered and dismissed)

- **audit #25 S1 fully resolved.** v2.0.20 corrected the narrative sentence; v2.0.21 corrected the adjacent arithmetic line. Both figures now agree (`75,346 × 1.25 = 94,182.5`). The cascade-miss class instance is closed with no further residual. ✓
- **`ops/audit.md` over-calibrated headroom (38.8%).** The file shrank 449 bytes via v2.0.21. The documented Chars value (~8,200) is larger than usual relative to actual. This is not a trigger under the Recalibration Rule (measured 5,908 < documented 8,200; headroom 2,292 > soft-floor 591). Will self-correct on the next ingest recalibration pass. Not a defect.
- **`CHANGELOG.md` now out of scope for `!! audit all`.** Confirmed by ops/audit.md scope list — CHANGELOG.md is not enumerated. The `+` suffix was correctly removed from all three locations that declared the audit-all envelope (`ops/audit.md:71`, `user-guide.md:94`, `user-guide.md:201`). ✓
- **`ops/token-reference.md` envelope unchanged.** Its Step 5 `(currently ~30,000–43,000)` was already `+`-free (it derives from the table sum, not from the audit scope list). No change needed. ✓
- **v2.0.21 cascade completeness.** v2.0.21 changed: `ops/audit.md` (scope list + note + envelope string), `user-guide.md` (two envelope strings), `CHANGELOG.md` (new entry + v2.0.18 arithmetic in-place correction). Token-reference.md was correctly not updated — no row changed, no trigger fired. ✓
- **Cold-start total `~6,530`** — 6,450 (CLAUDE.md) + 80 (hot.md). ✓
- **`!! ready` total `~7,480`** — 6,530 + 950 (memory.md full). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — derivable from current token-reference component values. ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently in all three locations. ✓
- **Ingest atomic ordering** — Step 5 `ts` pre-compute → Step 6 `mv` → Step 7 page write. ✓
- **Hash canonicalization 6-step pipeline** — intact. ✓
- **`Pages: N` derived** — `refresh-hot.md` counts `^- [[` entries; not a stored counter. ✓
- **Blueprint-authoring mode guard** — present in CLAUDE.md, audit.md:43. ✓
- **Blueprint Sync Rule 12-row matrix** — intact; no untriggered changes detected. ✓
- **`SKILL.md` install/uninstall symmetry** — file targets match; DB-keep option on uninstall correctly defaults to no. ✓
- **sqlite-query DB schema** — `pages` table, `relations` table, four indexes; `type` CHECK constraint; upsert pattern and bidirectional-relation `INSERT OR IGNORE` all correct. ✓
- **`query-layer.md` `find`-based path resolution** — correctly implemented; unmatched slugs silently skipped, triggering grep fallback. ✓
- **`ingest-hook.md` exception handler and Notes section** — both point to `!! install sqlite-query` backfill repair path; consistent with `SKILL.md §Fallback Behaviour`. ✓
- **`ops/ingest.md` B5 step enumeration** — `11.5` present in per-file list. ✓
- **`ops/update.md` Step 5.5** — ingest-hook call present; non-fatal error handling consistent with hook contract. ✓
- **`ops/token-reference.md` self-cost note** — both occurrences read `~2,120 tokens`. ✓
- **`ops/ingest.md` cross-reference to troubleshooting.md** — "URL ingest keeps regenerating the same source even when the article hasn't changed" exists in `troubleshooting.md`. ✓
- **Envelope arithmetic.** Table sum 40,820 tokens; cushion 2,180 (5.07% of 43,000 — above 2% floor). ✓
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form only. ✓
- **`.gitignore` scope** — correctly scopes to inside `blueprint/`; setup-guide.md correctly explains this does not govern `wiki/.obsidian/`. ✓
- **`ROADMAP.md`** — planning doc; not in audit scope.
- **`LICENSE`** — MIT; NiteKeeper copyright; no issues.
- **`template/CLAUDE.md` footer placeholders** — `[created-date]` and `[updated-date]` are intentional scaffolding; setup-guide.md Step 3 instructs their replacement. Not a defect.

---

## 4. Questions for Clarification

None. All findings are self-contained.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#25 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:43`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~10% of measured actual), envelope cushion floor (cushion < ~2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. ✓
11. sqlite-query skill follows Query Layer Hook Contract (`find`-based path resolution, no glob patterns) and Ingest Hook Contract (non-fatal errors, consistent repair messaging). ✓

---

## 6. Verdict

**The v2.0.21 blueprint has no CRITICAL, WARNING, or STYLE findings.**

v2.0.21 made two clean changes: (1) `blueprint/CHANGELOG.md` was removed from `!! audit all` scope, with the `+` suffix correctly stripped from all three envelope declarations (`ops/audit.md:71`, `user-guide.md:94`, `user-guide.md:201`); and (2) the v2.0.18 arithmetic residual carried as audit #25 S1 was corrected (`75,344 × 1.25` → `75,346 × 1.25 = 94,182.5`). Both changes verified. Cascade complete.

The prior audit #25 S1 is fully resolved. No new findings.

All 17 tracked files pass headroom checks; no hard or soft triggers fire. Token envelope unchanged: sum 40,820 tokens, cushion 2,180 (5.07% of 43,000 — above the 2% floor of ~860).

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
