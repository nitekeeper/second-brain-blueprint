# Blueprint Audit Report — 2026-04-19 (#25)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.20 (per CHANGELOG.md; latest entry is v2.0.20)  
**Prior audit reviewed:** #24 (`audit-report-2026-04-19-14.md`) — read in full before this pass per user instruction  
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)  
**Mode:** Blueprint-authoring (no `wiki/` present at working-folder root; log append and `hot.md` refresh skipped)  
**Note:** Audit reports directory (`audit-reports/`) excluded from scope per standing user instruction.  
**Token cost note:** `blueprint/CHANGELOG.md` (77,900 chars) is read during every `!! audit all` pass but is intentionally excluded from `token-reference.md` since v2.0.19 — actual session cost will exceed the ~30,000–43,000 envelope.

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**

- `README.md` (4,671 chars)
- `setup-guide.md` (10,564 chars)
- `user-guide.md` (14,221 chars)
- `troubleshooting.md` (22,670 chars)
- `CHANGELOG.md` (77,900 chars — v2.0.20 and prior entries read)
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
- `template/scheduled-tasks/ops/audit.md` (6,357 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,746 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (4,185 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,533 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,838 chars)

**Not in audit scope:** `ROADMAP.md` (planning doc, no logic content).

---

### 1.2 v2.0.20 changes verified

v2.0.20 was applied between audit #24 and this pass. It is a single-file patch: the CHANGELOG.md v2.0.18 narrative was corrected in-place to address the S1 finding carried through audits #23 and #24. Direct verification:

| Item | Claim | Re-verified |
|---|---|---|
| v2.0.18 narrative `"pre-entry ~73,334"` corrected to `"pre-entry ~73,333"` | Corrected | ✓ `grep "pre-entry ~73,333" CHANGELOG.md` confirms corrected value present |
| v2.0.18 narrative `"~75,344 chars"` corrected to `"~75,346 chars"` | Corrected | ✓ `"grew CHANGELOG.md to ~75,346 chars (pre-entry ~73,333)"` confirmed |
| No file-size or token-table changes | "No file-size or token-table changes" per v2.0.20 entry | ✓ All tracked files at identical sizes to audit #24; only CHANGELOG.md grew (+913 chars) |
| No recalibration, envelope change, or cold-start cascade | Stated in v2.0.20 entry | ✓ token-reference.md, ops/audit.md, user-guide.md, CLAUDE.md, README.md all unchanged |

One residual noted — see S1 below.

---

### 1.3 Prior audit #24 findings status

Audit #24 carried one STYLE finding (S1: CHANGELOG v2.0.18 narrative cited `"pre-entry ~73,334"` and `"~75,344 chars"`). v2.0.20 corrected both figures in the narrative sentence. **S1 is substantially resolved.** A residual inconsistency remains within the v2.0.18 CHANGELOG section: the arithmetic line immediately following the corrected narrative sentence still reads `75,344 × 1.25 = 94,180`, using the pre-correction base. The narrative now says `~75,346 chars` while the adjacent arithmetic uses `75,344`. This is a new narrow inconsistency (see S1 below), but of even lesser significance than the original: the arithmetic conclusion is unchanged (both round to ~94,200), and CHANGELOG.md is not tracked in token-reference.md.

---

### 1.4 Per-file headroom check (Recalibration Rule Steps 1–2)

Convention: ~125% of measured actual at calibration, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom % | 10% Soft Floor | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | 467 | ok |
| `setup-guide.md` | 10,564 | ~13,200 | 24.9% | 1,056 | ok |
| `user-guide.md` | 14,221 | ~17,800 | 25.2% | 1,422 | ok |
| `troubleshooting.md` | 22,670 | ~28,300 | 24.8% | 2,267 | ok |
| `CHANGELOG.md` | 77,900 | not tracked | — | — | ok |
| `LICENSE` | 1,067 | ~1,400 | 31.2% | 107 | ok |
| `template/CLAUDE.md` | 20,641 | ~25,800 | 25.0% | 2,064 | ok |
| `refresh-hot.md` | 3,966 | ~5,100 | 28.6% | 397 | ok |
| `ops/ingest.md` | 15,877 | ~19,800 | 24.7% | 1,588 | ok |
| `ops/lint.md` | 2,507 | ~3,100 | 23.7% | 251 | ok |
| `ops/query.md` | 2,586 | ~3,300 | 27.6% | 259 | ok |
| `ops/update.md` | 1,881 | ~2,400 | 27.6% | 188 | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 24.6% | 674 | ok |
| `ops/audit.md` | 6,357 | ~8,200 | 29.0% | 636 | ok |
| `ops/token-reference.md` | 6,746 | ~8,500 | 26.0% | 675 | ok |
| `skills/sqlite-query/SKILL.md` | 4,185 | ~5,200 | 24.2% | 419 | ok |
| `skills/sqlite-query/query-layer.md` | 2,533 | ~3,200 | 26.3% | 253 | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,838 | ~3,500 | 23.3% | 284 | ok |

No hard triggers. No soft triggers (minimum headroom 23.3% on `ingest-hook.md` — unchanged from audit #24). No recalibration required.

All 17 tracked files are byte-for-byte identical to audit #24. Only `CHANGELOG.md` grew (+913 chars, from v2.0.20 entry), and it is not tracked.

---

### 1.5 Envelope check (Recalibration Rule Step 5)

Unchanged from audit #24. Table sum 40,820 tokens; envelope `~30,000–43,000`; cushion 2,180 tokens (5.07% of 43,000 — above the 2% floor of ~860). No envelope widening required.

---

### 1.6 Cross-reference sanity checks

All 25 cross-references verified in audit #24 re-verified; all pass. Unchanged files, unchanged values. Spot-check of items most relevant to v2.0.20:

- `template/CLAUDE.md:9` cold-start self-cost `~6,450` — matches token-reference CLAUDE.md row. ✓
- `template/CLAUDE.md:17` cold-start total `~6,530` — consistent. ✓
- `user-guide.md:94` audit-all `~30,000–43,000+` — matches `ops/audit.md` envelope. ✓
- `user-guide.md:201` "Audit all (full blueprint) | ~30,000–43,000+" — consistent. ✓
- `ops/token-reference.md` Step 5 envelope `(currently ~30,000–43,000)` — consistent. ✓
- `ops/token-reference.md` floor note `(~860 tokens on a 43,000-token envelope)` — 43,000 × 2% = 860. ✓
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:70–72`, `README.md:73`, and `user-guide.md:175`. ✓
- Blueprint Sync Rule 12-row matrix — intact. ✓
- Versioning split (`Schema version: 2.0` in CLAUDE.md footer; patch bumps X.Y.Z in CHANGELOG only) — consistent. ✓
- `ops/audit.md:71` envelope `~30,000–43,000` — consistent with token-reference sum. ✓
- `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading. ✓
- **CHANGELOG.md v2.0.18 narrative** now reads `"grew CHANGELOG.md to ~75,346 chars (pre-entry ~73,333)"` — corrected values confirmed. ✓ (residual: `75,344 × 1.25` arithmetic on the line below — see S1)

---

## 2. Findings

### CRITICAL

None.

### WARNING

None.

### STYLE

**S1 (new, replaces prior S1) — `CHANGELOG.md` v2.0.18 section contains a residual internal inconsistency: the narrative sentence was corrected by v2.0.20 to `"~75,346 chars"` but the adjacent arithmetic line still reads `75,344 × 1.25 = 94,180`.**

*Evidence.*

`CHANGELOG.md` v2.0.18 section, consecutive lines:

> "Adding v2.0.18 entry grew CHANGELOG.md to ~75,346 chars (pre-entry ~73,333)."  
> "Recalibrated at 125%: **75,344** × 1.25 = 94,180 → ~94,200 / ~23,550"

The narrative figure (`~75,346`) was corrected by v2.0.20. The arithmetic base on the following line (`75,344`) was not updated and now diverges from the narrative above it.

*Downstream impact: zero.* 75,346 × 1.25 = 94,182.5 → ~94,200 and 75,344 × 1.25 = 94,180 → ~94,200 both round to the same calibrated value. CHANGELOG.md has been removed from `token-reference.md` since v2.0.19, so neither figure drives any active estimate anywhere in the system.

*Historical pattern.* This is the fifth occurrence in the cascade-miss class (v2.0.15 first — 593 chars, source-of-truth impact; v2.0.17 second — 1,151 chars, cosmetic; v2.0.18 third — 2 chars, rounding artifact; v2.0.20 fourth — corrected narrative but missed arithmetic; present — residual from v2.0.20 partial correction). The class is structurally inherent to writing CHANGELOG narratives that reference the file's own size during authoring.

*Recommendation.* May be corrected by updating `75,344 × 1.25 = 94,180` to `75,346 × 1.25 = 94,182.5 → ~94,200` in the v2.0.18 arithmetic line; or left as-is given the outcome is identical and CHANGELOG is no longer tracked. No cascade required under either choice.

---

## 3. Non-findings (considered and dismissed)

- **CHANGELOG.md v2.0.18 narrative** — `"pre-entry ~73,333"` and `"~75,346 chars"` now correct. v2.0.20 closed the S1 finding from audits #23–#24. ✓
- **v2.0.20 cascade completeness.** v2.0.20 was a CHANGELOG-only patch; no tracked files changed; no recalibration needed; no cold-start cascade needed. ✓
- **Cold-start total `~6,530`** — 6,450 (CLAUDE.md) + 80 (hot.md). ✓
- **`!! ready` total `~7,480`** — 6,530 + 950 (memory.md full). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — derivable from current token-reference component values. ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently in all three locations. ✓
- **Ingest atomic ordering** — Step 5 `ts` pre-compute → Step 6 `mv` → Step 7 page write. ✓
- **Hash canonicalization 6-step pipeline** — intact. ✓
- **`Pages: N` derived** — `refresh-hot.md` counts `^- [[` entries; not a stored counter. ✓
- **Blueprint-authoring mode guard** — present in CLAUDE.md, audit.md:44. ✓
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
- **`template/CLAUDE.md` footer placeholders** — `[created-date]` and `[updated-date]` are intentional scaffolding per the Setup note at the file's end; setup-guide.md Step 3 instructs their replacement. Not a defect in the template.

---

## 4. Questions for Clarification

None. All findings are self-contained.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#24 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:44`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~10% of measured actual), envelope cushion floor (cushion < ~2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. ✓
11. sqlite-query skill follows Query Layer Hook Contract (`find`-based path resolution, no glob patterns) and Ingest Hook Contract (non-fatal errors, consistent repair messaging). ✓

---

## 6. Verdict

**The v2.0.20 blueprint has no CRITICAL or WARNING findings. One STYLE note (S1, new): the v2.0.20 correction of the v2.0.18 narrative updated the description sentence (`"~75,346 chars (pre-entry ~73,333)"`) but left the adjacent arithmetic base unchanged (`75,344 × 1.25`). These are now internally inconsistent within the v2.0.18 section. Downstream impact: zero — the arithmetic conclusion rounds identically (~94,200), and CHANGELOG.md is not tracked in token-reference.md.**

The prior audit #24 S1 finding is substantially resolved: both narrative figures (`73,334` → `73,333`, `75,344` → `75,346`) were corrected in the description sentence by v2.0.20. The residual S1 above is a narrower follow-on miss of lesser significance.

All 17 tracked files pass headroom checks; no hard or soft triggers fire. Token envelope unchanged: sum 40,820 tokens, cushion 2,180 (5.07% of 43,000 — above the 2% floor of ~860).

**Priority order for follow-up (if any):**

1. **S1** — Update the v2.0.18 arithmetic line from `75,344 × 1.25 = 94,180` to `75,346 × 1.25 = 94,182.5 → ~94,200` for internal consistency; or leave as-is — the conclusion is identical and CHANGELOG is no longer tracked. Either choice is defensible.

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
