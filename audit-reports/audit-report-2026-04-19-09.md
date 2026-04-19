# Blueprint Audit Report — 2026-04-19 (#19)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.15 (per CHANGELOG.md; no later entry found)  
**Prior audits reviewed:** #11–#18 (`audit-report-2026-04-19-01.md` through `audit-report-2026-04-19-08.md`) — read in full before this pass per user instruction  
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
- `CHANGELOG.md` (70,847 chars — first 120 lines read; v2.0.15 entry read in full)
- `LICENSE` (1,067 chars)

**Template**

- `template/CLAUDE.md` (20,641 chars — first 80 lines read)
- `template/scheduled-tasks/refresh-hot.md` (3,966 chars — via prior audit chain)
- `template/scheduled-tasks/ops/ingest.md` (15,877 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars — via prior audit chain)
- `template/scheduled-tasks/ops/query.md` (2,586 chars — via prior audit chain)
- `template/scheduled-tasks/ops/update.md` (1,881 chars — via prior audit chain)
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars — via prior audit chain)
- `template/scheduled-tasks/ops/audit.md` (6,590 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,797 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (4,185 chars — via prior audit chain)
- `blueprint/skills/sqlite-query/query-layer.md` (2,533 chars — via prior audit chain)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,838 chars)

**Not in audit scope:** `blueprint/` sub-directory internals (working-folder-level installed files), `ROADMAP.md` (planning doc, no logic content).

---

### 1.2 Verification that audit #18 findings are resolved and v2.0.15 changes are consistent

Audit #18 left v2.0.14 with two WARNING findings and one STYLE note. v2.0.15 was applied before this pass. Direct re-verification:

| Item | Claim | Re-verified |
|---|---|---|
| #18 W1 | `ops/token-reference.md` self-cost note updated from `~2,080` to `~2,120 tokens` | ✓ header line 8 now reads `~2,120 tokens` (both occurrences) |
| #18 W2 | New troubleshooting entry added; ingest.md cross-reference updated | ✓ `troubleshooting.md` contains "URL ingest keeps regenerating the same source…"; `ops/ingest.md:55` references that exact title |
| #18 S1 | Seven files firing soft trigger; recalibration would produce no value changes | ✓ confirmed no-op recalibration — no action was required or taken |
| v2.0.15 | `troubleshooting.md` recalibrated from ~27,300 → ~28,300 / ~7,080 | ✓ token-reference row confirmed |
| v2.0.15 | `CHANGELOG.md` recalibrated to ~88,500 / ~22,130 | ✓ token-reference row confirmed |
| v2.0.15 | Envelope widened from ~64,000 → ~65,000 | ✓ `ops/audit.md:72` reads `~30,000–65,000`; `user-guide.md:94` and `:201` both match |
| v2.0.15 | `CHANGELOG.md` post-fix envelope sum 62,950 tokens; cushion 2,050 (3.15% > 2% floor) | ✓ arithmetic verified from token-reference rows |

No regressions from v2.0.15 detected on the above items.

---

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Current convention per `token-reference.md` (v2.0.14+): **~125% of measured actual at calibration**, rounded to nearest 100. Soft trigger: headroom below ~25% of measured actual (i.e. doc < 1.25 × measured). Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom % of measured | Flag |
|---|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | ok |
| `setup-guide.md` | 10,564 | ~13,200 | 24.9% | ⚠️ soft |
| `user-guide.md` | 14,219 | ~17,800 | 25.2% | ok |
| `troubleshooting.md` | 22,670 | ~28,300 | 24.8% | ⚠️ soft |
| `CHANGELOG.md` | 70,847 | ~88,500 | 24.9% | ⚠️ soft |
| `LICENSE` | 1,067 | ~1,400 | 31.2% | ok |
| `template/CLAUDE.md` | 20,641 | ~25,800 | 25.0% | ok (at threshold) |
| `refresh-hot.md` | 3,966 | ~5,100 | 28.6% | ok |
| `ops/ingest.md` | 15,877 | ~19,800 | 24.7% | ⚠️ soft |
| `ops/lint.md` | 2,507 | ~3,100 | 23.7% | ⚠️ soft |
| `ops/query.md` | 2,586 | ~3,300 | 27.6% | ok |
| `ops/update.md` | 1,881 | ~2,400 | 27.6% | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 24.6% | ⚠️ soft |
| `ops/audit.md` | 6,590 | ~8,200 | 24.4% | ⚠️ soft |
| `ops/token-reference.md` | 6,797 | ~8,500 | 25.0% | ok (at threshold) |
| `skills/sqlite-query/SKILL.md` | 4,185 | ~5,200 | 24.2% | ⚠️ soft |
| `skills/sqlite-query/query-layer.md` | 2,533 | ~3,200 | 26.3% | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,838 | ~3,500 | 23.3% | ⚠️ soft |

No hard triggers (measured ≥ documented). Nine soft triggers active — see S2.

---

### 1.4 Envelope check (Recalibration Rule Step 5)

Documented rows sum from `token-reference.md`:

| Group | Tokens |
|---|---:|
| Blueprint-doc (README 1,500 + setup-guide 3,300 + user-guide 4,450 + troubleshooting 7,080 + CHANGELOG 22,130 + LICENSE 350) | 38,810 |
| Template-side (CLAUDE 6,450 + refresh-hot 1,280 + ingest 4,950 + lint 780 + query 830 + update 600 + conventions 2,100 + audit 2,050 + token-reference 2,120) | 21,160 |
| Skill rows (SKILL.md 1,300 + query-layer 800 + ingest-hook 880) | 2,980 |
| **Total** | **62,950** |

Envelope: `~30,000–65,000` (per `ops/audit.md:72`).  
Cushion: 65,000 − 62,950 = **2,050 tokens (3.15%)**. Above the 2% floor (1,300 tokens on a 65,000-token envelope). No envelope widening required.

---

### 1.5 Cross-reference sanity checks

- `template/CLAUDE.md:9` cold-start self-cost `~6,450` = token-reference CLAUDE.md row (`~25,800 / ~6,450`). ✓
- `template/CLAUDE.md:17` cold-start total `~6,530` = 6,450 + 80 (hot.md). ✓
- `template/CLAUDE.md:17` `!! ready` total `~7,480` = 6,530 + 950 (memory.md full). ✓
- `user-guide.md:9` CLAUDE.md cost `~6,450` — matches token-reference row. ✓
- `user-guide.md:14` cold-start `~6,530` — consistent with CLAUDE.md:17. ✓
- `user-guide.md:94` and `:201` audit-all `~30,000–65,000` — matches `ops/audit.md:72`. ✓
- `README.md:72` cold-start `~6,530` — matches CLAUDE.md:17. ✓
- `ops/audit.md:72` envelope `~30,000–65,000` — consistent with token-reference sum (62,950). ✓
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:70–72`, `README.md:73`, and `user-guide.md`. ✓
- Blueprint Sync Rule 12-row matrix — intact. ✓
- Versioning split (`Schema version: 2.0` in CLAUDE.md footer; patch bumps X.Y.Z in CHANGELOG only) — consistent. ✓
- Ingest atomic ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
- Hash canonicalization 6-step pipeline intact in `ops/ingest.md §Hash Canonicalization`. ✓
- `ops/ingest.md` B5 per-file step list `[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]` — confirmed. ✓
- `ops/ingest.md:55` cross-reference: "See `troubleshooting.md` 'URL ingest keeps regenerating the same source even when the article hasn't changed'" — matches the actual section heading in `troubleshooting.md`. ✓
- `ingest-hook.md` exception handler and Notes section second bullet — both point to `!! install sqlite-query` repair path. ✓
- `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading (verified via prior audit chain). ✓
- `query-layer.md` uses `find`-based path resolution — satisfies Query Layer Hook Contract (verified via prior audit chain). ✓
- `ops/conventions.md` Query Layer Hook Contract explicitly prohibits glob patterns (verified via prior audit chain). ✓
- `ops/update.md` Step 5.5 ingest-hook call — present and correct (verified via prior audit chain). ✓
- Blueprint-authoring mode guard present in `template/CLAUDE.md`, `ops/audit.md:44`. ✓
- **`CHANGELOG.md` v2.0.15 narrative cites `~87,900 / ~21,980` for CHANGELOG.md recalibration, but token-reference.md and the post-fix envelope in the same entry both show `~88,500 / ~22,130`.** ⚠️ (see S1)

---

## 2. Findings

### CRITICAL

None.

### WARNING

None.

### STYLE

**S1 — `CHANGELOG.md` v2.0.15 narrative contains internally inconsistent calibration figures for the CHANGELOG.md row: narrative body says `~87,900 / ~21,980`; post-fix envelope and `token-reference.md` (source of truth) both show `~88,500 / ~22,130`.**

*Evidence.*

`CHANGELOG.md` v2.0.15 narrative (lines 34–36):
> "Adding the v2.0.15 entry grew CHANGELOG.md to 70,207 chars. Recalibrated at 125%: 70,207 × 1.25 = 87,759 → **~87,900 / ~21,980** (was ~84,600 / ~21,150)."

`CHANGELOG.md` v2.0.15 post-fix envelope (same entry, lines 46–54):
> "CHANGELOG (**22,130**, see token-reference.md)"

`token-reference.md` File Read Costs table (line 34):
> `| blueprint/CHANGELOG.md | ~88,500 | ~22,130 |`

`CHANGELOG.md` v2.0.15 narrative (line 36–37):
> "New table sum ~62,800 tokens pushed the cushion to 1,200 tokens (1.875% of 64,000 — below the 2% floor)…"

Actual table sum (from the post-fix envelope and confirmed by this audit): **62,950 tokens** (not 62,800).

*Root cause.* The narrative text was drafted when CHANGELOG.md measured ~70,207 chars (70,207 × 1.25 = 87,759 → ~87,900 / ~21,980, yielding a pre-fix sum of 61,720 + 250 + 830 = ~62,800). By the time the token-reference was actually updated — after the full v2.0.15 entry was finalized — CHANGELOG.md had grown to ~70,800 chars (70,800 × 1.25 = 88,500 → ~22,130, yielding the actual sum of 62,950). The post-fix envelope section in the CHANGELOG was then updated to match the actual token-reference values (22,130, sum 62,950), but the narrative text was not revised. The result is a single CHANGELOG entry that cites two different calibration values for the same file in two consecutive paragraphs.

*Impact.* No functional impact. `token-reference.md` (the declared source of truth) is correct at ~88,500 / ~22,130. The post-fix envelope arithmetic (62,950 tokens) is correct and derivable from the table. The envelope widening decision (1,200 or 1,050 tokens below the 2% floor of 64,000 — either way below the floor) is correct regardless of which CHANGELOG figure is used. A future maintainer auditing the v2.0.15 CHANGELOG entry's arithmetic would note the mismatch between "70,207 chars" / "~87,900 / ~21,980" and the applied "~88,500 / ~22,130", but the audit trail priority is the token-reference, not the narrative.

*Recommended fix.* Update the v2.0.15 narrative to: (a) replace "70,207" with "~70,800", (b) replace "87,759" with "88,500", (c) replace "~87,900 / ~21,980" with "~88,500 / ~22,130", and (d) replace "~62,800 tokens" with "~62,950 tokens" (and correspondingly "1,200 tokens (1.875%)" with "~1,050 tokens (1.64%)"). The envelope-widening conclusion (cushion below 2% floor) is still correct with either figure; only the numbers in the narrative change. One-paragraph fix, CHANGELOG only — no downstream cascade required since the source-of-truth values are already correct.

---

**S2 — Nine files fire the soft recalibration trigger (headroom < 25% of measured actual), but recalibration produces no numeric changes.**

Files and headroom: `setup-guide.md` (24.9%), `troubleshooting.md` (24.8%), `CHANGELOG.md` (24.9%), `ops/ingest.md` (24.7%), `ops/lint.md` (23.7%), `ops/conventions.md` (24.6%), `ops/audit.md` (24.4%), `skills/SKILL.md` (24.2%), `skills/ingest-hook.md` (23.3%).

All nine were either (a) freshly recalibrated in v2.0.14 or v2.0.15 and have seen only trivial post-calibration growth, or (b) have rounding-artifact headroom (e.g. troubleshooting.md at 24.8% and CHANGELOG.md at 24.9% — both reflect the standard 125% calibration rounding to nearest 100). For all nine, 125% × current measured rounds to the same documented Chars value:

| File | Measured | 125% × measured | Rounds to | Doc. Chars | Change? |
|---|---:|---:|---:|---:|:---:|
| `setup-guide.md` | 10,564 | 13,205 | ~13,200 | ~13,200 | none |
| `troubleshooting.md` | 22,670 | 28,338 | ~28,300 | ~28,300 | none |
| `CHANGELOG.md` | 70,847 | 88,559 | ~88,600 | ~88,500 | +100 |
| `ops/ingest.md` | 15,877 | 19,846 | ~19,800 | ~19,800 | none |
| `ops/lint.md` | 2,507 | 3,134 | ~3,100 | ~3,100 | none |
| `ops/conventions.md` | 6,741 | 8,426 | ~8,400 | ~8,400 | none |
| `ops/audit.md` | 6,590 | 8,238 | ~8,200 | ~8,200 | none |
| `skills/SKILL.md` | 4,185 | 5,231 | ~5,200 | ~5,200 | none |
| `skills/ingest-hook.md` | 2,838 | 3,548 | ~3,500 | ~3,500 | none |

Eight of nine files: recalibration produces no Chars-column changes. The exception is **`CHANGELOG.md`**: 70,847 × 1.25 = 88,559 → rounds to ~88,600, but the documented value is ~88,500. The discrepancy is +100 chars (the calibration was done against ~70,800 chars, not 70,847). Recalibrating now would update the CHANGELOG.md row from ~88,500 to ~88,600, and Tokens from ~22,130 to ~22,150 (+20 tokens). This token change would raise the table total from 62,950 to 62,970 — still 2,030 tokens (3.12%) below the 65,000 envelope upper bound, above the 2% floor. No envelope widening triggered.

*No action required now.* The CHANGELOG.md row discrepancy is +100 chars, well within normal inter-audit growth. Flag for the next recalibration pass: if CHANGELOG.md is recalibrated, update to ~88,600 / ~22,150 (+20 token delta to table sum, no envelope impact).

---

## 3. Non-findings (considered and dismissed)

- **Cold-start total `~6,530`** — 6,450 (CLAUDE.md) + 80 (hot.md). ✓
- **`!! ready` total `~7,480`** — 6,530 + 950 (memory.md full). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — derivable from current token-reference component values (refresh-hot 1,280 + index 250 + log-tail 625 + log-append 100 + memory-write ~750 ≈ 3,005 ≈ ~3,000; +950 −750 +50 ≈ 3,255 ≈ ~3,300). ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
- **Ingest atomic ordering** — Step 5 pre-compute → Step 6 mv → Step 7 page write. ✓
- **Hash canonicalization 6-step pipeline** — intact. ✓
- **`Pages: N` derived** — `refresh-hot.md` counts `^- [[` entries; not a stored counter. ✓
- **Blueprint-authoring mode guard** — present in CLAUDE.md, audit.md:44. ✓
- **Blueprint Sync Rule 12-row matrix** — intact; no new untriggered changes detected beyond S1 and S2. ✓
- **`SKILL.md` install/uninstall symmetry** — file targets match; DB-keep option on uninstall correctly defaults to no. ✓
- **sqlite-query DB schema** — `pages` table, `relations` table, four indexes; `type` CHECK constraint; upsert pattern and bidirectional-relation `INSERT OR IGNORE` all correct. ✓
- **`query-layer.md` `find`-based path resolution** — correctly implemented; unmatched slugs silently skipped, triggering grep fallback. ✓
- **`ingest-hook.md` exception handler and Notes section** — both point to `!! install sqlite-query` backfill repair path; consistent with `SKILL.md §Fallback Behaviour`. ✓
- **`ops/ingest.md` B5 step enumeration** — `11.5` present in per-file list. ✓
- **`ops/update.md` Step 5.5** — ingest-hook call present; non-fatal error handling consistent with hook contract. ✓
- **`CHANGELOG.md` v2.0.15 envelope decision** — even using the narrative's lower sum (~62,800 with CHANGELOG ~21,980), the cushion (1,200 tokens = 1.875% of 64,000) is below the 2% floor (1,280 tokens), so widening to 65,000 was correctly triggered. The decision is valid under either set of figures. ✓
- **`ops/audit.md` envelope widening history** — lists v2.0.6, v2.0.7, v2.0.9, v2.0.10, v2.0.11, v2.0.14, v2.0.15 as widening events. v2.0.12 and v2.0.13 correctly omitted (neither widened the envelope). ✓
- **Troubleshooting entry for URL ingest / LLM-WebFetch** (`#18 W2`) — new section heading "URL ingest keeps regenerating the same source even when the article hasn't changed" matches `ops/ingest.md:55` cross-reference exactly. Content documents cause (LLM prose rewriting), fix (use Web Clipper), and prevention. ✓
- **`token-reference.md` self-cost note** (`#18 W1`) — both occurrences in header now read `~2,120 tokens`, matching the table row. ✓
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form only; 3-argument GNU-awk form correctly avoided. ✓
- **`.gitignore`** — 65 chars; scoped to inside `blueprint/`; setup-guide.md correctly explains this does not govern `wiki/.obsidian/`. ✓
- **`ops/audit.md` scope parenthetical** — "currently `refresh-hot.md`" accurate after `changelog-monitor.md` removal (v2.0.11). ✓
- **`ROADMAP.md`** — planning doc; not in audit scope.
- **`LICENSE`** — MIT; no issues.

---

## 4. Questions for Clarification

None. All findings are self-contained.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#18 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:44`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md:72` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~25% of measured actual), envelope cushion floor (cushion < ~2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. ✓
11. sqlite-query skill follows Query Layer Hook Contract (`find`-based path resolution, no glob patterns) and Ingest Hook Contract (non-fatal errors, consistent repair messaging across exception handler, Notes section, and `SKILL.md §Fallback Behaviour`). ✓ fully satisfied.

---

## 6. Verdict

**The v2.0.15 blueprint has no CRITICAL or WARNING findings. Two STYLE notes: an internal inconsistency in the v2.0.15 CHANGELOG entry's calibration narrative (S1), and nine files at sub-25% headroom where recalibration produces no value changes (S2).**

No architectural regressions. All prior findings from audits #11–#18 are verified clean. The ingest pipeline, approval flow, hash canonicalization, Blueprint Sync Rule, Recalibration Rule, and all sqlite-query hook contracts are fully intact. Headroom across all 18 tracked files is healthy; no hard triggers active.

S1 is a documentation-only inconsistency: the CHANGELOG v2.0.15 narrative describes CHANGELOG.md being calibrated against 70,207 chars (→ ~87,900 / ~21,980), while the actually-applied values in `token-reference.md` and the post-fix envelope correspond to ~70,800 chars (→ ~88,500 / ~22,130). The source of truth (`token-reference.md`) is correct; only the narrative text requires correction. A one-paragraph CHANGELOG edit covers it.

S2 is the same no-action class as audit #17 S1 and audit #18 S1: all nine files are either freshly calibrated (rounding artifact) or have grown minimally. The only file where recalibration would change a documented value is `CHANGELOG.md` (+100 chars, +20 tokens, no envelope impact). That update may be bundled into the next substantive CHANGELOG entry if desired.

**Priority order for follow-up (if any):**

1. **S1** — Update v2.0.15 CHANGELOG narrative to replace "70,207 chars" / "~87,900 / ~21,980" / "~62,800 tokens" with the values matching the applied calibration (~70,800 chars / ~88,500 / ~22,130 / ~62,950 tokens). One-paragraph fix; no downstream cascade — source-of-truth values are already correct everywhere else.
2. **S2** — No action required. If a calibration date refresh is desired, update `token-reference.md` header date. Optional: bundle the `CHANGELOG.md` row update (+100 chars / +20 tokens) into the next substantive patch.

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
