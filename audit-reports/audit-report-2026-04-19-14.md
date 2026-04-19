# Blueprint Audit Report — 2026-04-19 (#24)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.19 (per CHANGELOG.md; latest entry is v2.0.19)  
**Prior audit reviewed:** #23 (`audit-report-2026-04-19-13.md`) — read in full before this pass per user instruction  
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)  
**Mode:** Blueprint-authoring (no `wiki/` present at working-folder root; log append and `hot.md` refresh skipped)  
**Note:** Audit reports directory (`audit-reports/`) excluded from scope per standing user instruction.  
**Token cost note:** `blueprint/CHANGELOG.md` (76,987 chars) is read during every `!! audit all` pass but is intentionally excluded from `token-reference.md` since v2.0.19 — actual session cost will exceed the ~30,000–43,000 envelope.

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**

- `README.md` (4,671 chars)
- `setup-guide.md` (10,564 chars)
- `user-guide.md` (14,221 chars)
- `troubleshooting.md` (22,670 chars)
- `CHANGELOG.md` (76,987 chars — v2.0.19 and prior entries read)
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

### 1.2 v2.0.19 changes verified

v2.0.19 was applied between audit #23 and this pass. Direct verification of all stated cascade targets:

| Item | Claim | Re-verified |
|---|---|---|
| CHANGELOG.md row removed from `token-reference.md` | Row `blueprint/CHANGELOG.md \| ~94,200 \| ~23,550` deleted | ✓ Not present in table |
| `token-reference.md` Step 5 envelope updated | `(currently ~30,000–43,000)` | ✓ line 80 confirmed |
| `token-reference.md` Step 5 floor note updated | `~860 tokens on a 43,000-token envelope` (43,000 × 2% = 860) | ✓ confirmed |
| `ops/audit.md` envelope updated | `~30,000–43,000` (line 70) | ✓ confirmed |
| Warning note added to `ops/audit.md` | CHANGELOG.md excluded / warn about excess tokens note | ✓ present at line 70 |
| `user-guide.md` `!! audit` description | `~30,000–43,000+` | ✓ line 94 confirmed |
| `user-guide.md` cost table | `Audit all (full blueprint) \| ~30,000–43,000+` | ✓ line 201 confirmed |
| `token-reference.md` header self-cost | `~2,120 tokens` (both occurrences) | ✓ matches `~8,500 / ~2,120` table row |

No missed cascade targets detected for v2.0.19.

---

### 1.3 Prior audit #23 findings status

Audit #23 left one STYLE finding (S1: CHANGELOG v2.0.18 narrative cited `"pre-entry ~73,334"` (actual: 73,333) and `"~75,344 chars"` (actual: 75,346)). v2.0.19 did **not** correct this cosmetic narrative — the numbers remain in the CHANGELOG body. However, v2.0.19 removed CHANGELOG.md from `token-reference.md` entirely, which eliminates even the theoretical possibility of downstream calibration impact. The finding carries forward at lower-than-before severity (see S1 below).

---

### 1.4 Per-file headroom check (Recalibration Rule Steps 1–2)

Convention: ~125% of measured actual at calibration, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom % | 10% Soft Floor | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | 467 | ok |
| `setup-guide.md` | 10,564 | ~13,200 | 24.9% | 1,056 | ok |
| `user-guide.md` | 14,221 | ~17,800 | 25.2% | 1,422 | ok |
| `troubleshooting.md` | 22,670 | ~28,300 | 24.8% | 2,267 | ok |
| `CHANGELOG.md` | 76,987 | not tracked | — | — | ok |
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

No hard triggers. No soft triggers (minimum headroom 23.3% on `ingest-hook.md`). No recalibration required.

**ops/audit.md size note.** File shrank from 6,599 chars (audit #23) to 6,357 chars now (−242 chars). The v2.0.19 warning note was added to the file, but the envelope text was also shortened (`~30,000–67,000` → `~30,000–43,000`) and related surrounding text revised, netting a reduction. Documented value is ~8,200; headroom 29.0%. No trigger fires.

**ops/token-reference.md size note.** File shrank from 6,797 (audit #23) to 6,746 (−51 chars) — consistent with the single CHANGELOG.md table row removed in v2.0.19 (~50 chars). Documented value is ~8,500; headroom 26.0%. No trigger fires.

---

### 1.5 Envelope check (Recalibration Rule Step 5)

Documented rows sum from `token-reference.md` (post-v2.0.19, CHANGELOG row removed):

| Group | Tokens |
|---|---:|
| Blueprint-doc (README 1,500 + setup-guide 3,300 + user-guide 4,450 + troubleshooting 7,080 + LICENSE 350) | 16,680 |
| Template-side (CLAUDE 6,450 + refresh-hot 1,280 + ingest 4,950 + lint 780 + query 830 + update 600 + conventions 2,100 + audit 2,050 + token-reference 2,120) | 21,160 |
| Skill rows (SKILL.md 1,300 + query-layer 800 + ingest-hook 880) | 2,980 |
| **Total** | **40,820** |

Envelope: `~30,000–43,000` (per `ops/audit.md` line 70).  
Cushion: 43,000 − 40,820 = **2,180 tokens (5.07%)**. Above the 2% floor (~860 tokens on a 43,000-token envelope). No envelope widening required.

CHANGELOG v2.0.19 Post-fix arithmetic independently verified: 16,680 + 21,160 + 2,980 = 40,820. Cushion 2,180 / 43,000 = 5.07%. ✓

---

### 1.6 Cross-reference sanity checks

- `template/CLAUDE.md:9` cold-start self-cost `~6,450` = token-reference CLAUDE.md row (`~25,800 / ~6,450`). ✓
- `template/CLAUDE.md:17` cold-start total `~6,530` = 6,450 + 80 (hot.md). ✓
- `template/CLAUDE.md:17` `!! ready` total `~7,480` = 6,530 + 950 (memory.md full). ✓
- `user-guide.md:9` CLAUDE.md cost `~6,450` — matches token-reference row. ✓
- `user-guide.md:14` cold-start `~6,530` — consistent with CLAUDE.md:17. ✓
- `user-guide.md:94` audit-all `~30,000–43,000+` — matches `ops/audit.md`. ✓
- `user-guide.md:201` "Audit all (full blueprint) | ~30,000–43,000+" — matches `ops/audit.md`. ✓
- `user-guide.md` `!! wrap` realistic `~3,000` / `!! ready` realistic `~3,300` — derivable from current token-reference component values (refresh-hot 1,280 + index 250 + log-tail 625 + log-append 100 + memory-write ~750 ≈ 3,005 ≈ ~3,000; +950 −750 +50 ≈ 3,255 ≈ ~3,300). ✓
- `README.md` cold-start `~6,530` — matches CLAUDE.md:17. ✓
- `ops/audit.md` envelope `~30,000–43,000` — consistent with token-reference sum (40,820 tokens, cushion 2,180). ✓
- `ops/token-reference.md` self-cost note: both occurrences in header read `~2,120 tokens` — matches table row `~8,500 / ~2,120`. ✓
- `ops/token-reference.md` Recalibration Rule Step 5: inline `(currently ~30,000–43,000)` — matches updated envelope. ✓
- `ops/token-reference.md` Recalibration Rule Step 5: floor note `(~860 tokens on a 43,000-token envelope)` — 43,000 × 2% = 860 ✓.
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:70–72`, `README.md:73`, and `user-guide.md:175`. ✓
- Blueprint Sync Rule 12-row matrix — intact. ✓
- Versioning split (`Schema version: 2.0` in CLAUDE.md footer; patch bumps X.Y.Z in CHANGELOG only) — consistent. ✓
- Ingest atomic ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
- Hash canonicalization 6-step pipeline intact in `ops/ingest.md §Hash Canonicalization`. ✓
- `ops/ingest.md` B5 per-file step list `[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]` — confirmed. ✓
- `ops/ingest.md:55` cross-reference: "See `troubleshooting.md` 'URL ingest keeps regenerating the same source even when the article hasn't changed'" — heading present in `troubleshooting.md`. ✓
- Blueprint-authoring mode guard present in `template/CLAUDE.md`, `ops/audit.md:44`. ✓
- `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading "## Step 4.5 — Offer SQLite Query Skill". ✓
- `query-layer.md` uses `subprocess.run(["find", pages_dir, "-name", ...])` — no glob patterns — satisfies Query Layer Hook Contract. ✓
- `ingest-hook.md` exception handler: points to `!! install sqlite-query` repair path. ✓
- `ingest-hook.md` Notes section second bullet: points to `!! install sqlite-query` repair path. ✓
- `SKILL.md §Fallback Behaviour` documents DB desync recovery (`!! install sqlite-query` backfill). ✓
- `ops/conventions.md` Query Layer Hook Contract explicitly prohibits glob patterns; requires `find`-via-subprocess. ✓
- `ops/update.md` Step 5.5 ingest-hook call — present and correct. ✓
- `ops/audit.md` scope parenthetical "currently `refresh-hot.md`" — accurate. ✓
- `.gitignore` scope — correctly scopes to inside `blueprint/`; `setup-guide.md` correctly explains this does not govern `wiki/.obsidian/`. ✓
- CHANGELOG.md v2.0.19 entry. v2.0.19 blueprint-doc sum: 16,680; template-side: 21,160; skill: 2,980; total 40,820 — independently verified. ✓
- **CHANGELOG.md v2.0.18 narrative cites `"pre-entry ~73,334"` and `"~75,344 chars"` for CHANGELOG.md; actual measurements are 73,333 (audit #22) and 75,346 (audit #23).** ⚠️ (see S1 — same cascade-miss class, now fully inert since CHANGELOG.md removed from token table in v2.0.19)

---

## 2. Findings

### CRITICAL

None.

### WARNING

None.

### STYLE

**S1 (carried from audit #23) — `CHANGELOG.md` v2.0.18 narrative contains minor measurement rounding discrepancies: cites `"pre-entry ~73,334"` (actual: 73,333) and `"grew CHANGELOG.md to ~75,344 chars"` (actual: 75,346). Now fully inert: CHANGELOG.md was removed from `token-reference.md` in v2.0.19, eliminating even theoretical downstream calibration impact.**

*Evidence.*

`CHANGELOG.md` v2.0.18 narrative:
> "Adding v2.0.18 entry grew CHANGELOG.md to ~75,344 chars (pre-entry ~73,334)."

`wc -c` pre-v2.0.18 (audit #22): **73,333 chars** (narrative: 73,334 — off by 1).  
`wc -c` post-v2.0.18 (audit #23): **75,346 chars** (narrative: 75,344 — off by 2).

*Downstream impact: zero.* These numbers no longer drive any table value anywhere — `blueprint/CHANGELOG.md` was removed from `token-reference.md` in v2.0.19 precisely because tracking its size adds churn without protecting anything.

*Historical pattern.* Third occurrence of the cascade-miss class (v2.0.15 first — 593 chars, had source-of-truth impact; v2.0.17 second — 1,151 chars, cosmetic; v2.0.18 third — 2 chars, rounding artifact). The pattern is inherent to writing CHANGELOG entries that reference the file's own pre-finalization size. v2.0.19 removes the incentive to correct it by removing CHANGELOG from the tracking table entirely.

*Recommendation.* May be bundled into the next substantive CHANGELOG entry (one-sentence correction: `"pre-entry ~73,333"` and `"~75,346 chars"`), or left as-is given it no longer has any calibration role. No downstream cascade required under either choice.

---

## 3. Non-findings (considered and dismissed)

- **Cold-start total `~6,530`** — 6,450 (CLAUDE.md) + 80 (hot.md). ✓
- **`!! ready` total `~7,480`** — 6,530 + 950 (memory.md full). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — derivable from current token-reference component values. ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
- **Ingest atomic ordering** — Step 5 `ts` pre-compute → Step 6 mv → Step 7 page write. ✓
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
- **`ops/token-reference.md` self-cost note** — both occurrences read `~2,120 tokens`, matching the table row. ✓
- **`ops/ingest.md` cross-reference to troubleshooting.md** — "URL ingest keeps regenerating the same source even when the article hasn't changed" exists in `troubleshooting.md`. ✓
- **v2.0.19 envelope arithmetic.** Pre-v2.0.19 table sum: 64,370 (included CHANGELOG ~23,550); removing CHANGELOG row: 64,370 − 23,550 = 40,820. Envelope tightened from 67,000 → 43,000. Old cushion: 67,000 − 64,370 = 2,630 (3.93%). New cushion: 43,000 − 40,820 = 2,180 (5.07%). Both above 2% floor. ✓
- **v2.0.19 cascade completeness.** The cascade covered `ops/token-reference.md`, `ops/audit.md`, and `user-guide.md` (both locations). Cold-start totals in CLAUDE.md and README.md are based on CLAUDE.md + hot.md file sizes — neither changed in v2.0.19 — so no cold-start propagation was required. Cascade is complete. ✓
- **`ops/audit.md:71` line-number reference in `token-reference.md` Step 5.** Reference cites `ops/audit.md:71`; envelope line is at line 70 in the current file (was 72 in audit #23). Line numbers are informational only and not semantically binding. Not flagged.
- **ops/audit.md size reduction.** File shrank 6,599 → 6,357 chars (−242) despite v2.0.19 adding a warning note. Net shrinkage consistent with the envelope text shortening (`~30,000–67,000` → `~30,000–43,000`) and surrounding Notes edits outweighing the added sentences. Documented value ~8,200; headroom 29.0%. No trigger. ✓
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form only; 3-argument GNU-awk form correctly avoided. ✓
- **`.gitignore` scope** — correctly scopes to inside `blueprint/`; setup-guide.md correctly explains this does not govern `wiki/.obsidian/`. ✓
- **`ROADMAP.md`** — planning doc; not in audit scope.
- **`LICENSE`** — MIT; NiteKeeper copyright; no issues.

---

## 4. Questions for Clarification

None. All findings are self-contained.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#23 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:44`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~10% of measured actual — v2.0.16 correction), envelope cushion floor (cushion < ~2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. ✓
11. sqlite-query skill follows Query Layer Hook Contract (`find`-based path resolution, no glob patterns) and Ingest Hook Contract (non-fatal errors, consistent repair messaging across exception handler, Notes section, and `SKILL.md §Fallback Behaviour`). ✓ fully satisfied.

---

## 6. Verdict

**The v2.0.19 blueprint has no CRITICAL or WARNING findings. One STYLE note (S1, carried from audit #23): the CHANGELOG v2.0.18 narrative contains 1–2 char measurement rounding discrepancies that are now fully inert — v2.0.19 removed CHANGELOG.md from `token-reference.md`, eliminating any calibration dependency on CHANGELOG's own narrative figures.**

v2.0.19 changes verified clean: CHANGELOG.md row removed from token-reference, envelope tightened to `~30,000–43,000` and propagated consistently to all three cascade targets (`ops/token-reference.md`, `ops/audit.md`, `user-guide.md`). Table sum independently confirmed at 40,820 tokens; cushion 2,180 tokens (5.07% of 43,000 — above the 2% floor of ~860). All 18 tracked files pass headroom checks; no hard or soft triggers fire.

**Priority order for follow-up (if any):**

1. **S1** — Bundle a one-sentence correction of the v2.0.18 narrative (`"pre-entry ~73,334"` → `"pre-entry ~73,333"`, `"~75,344 chars"` → `"~75,346 chars"`) into the next substantive CHANGELOG entry, or leave permanently as-is — the CHANGELOG row is no longer tracked, so the narrative numbers have zero calibration role. Either choice is defensible.

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
