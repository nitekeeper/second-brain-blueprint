# Blueprint Audit Report — 2026-04-19 (#23)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.18 (per CHANGELOG.md; no later entry found)  
**Prior audits reviewed:** #11–#22 (`audit-report-2026-04-19-01.md` through `audit-report-2026-04-19-12.md`) — read in full before this pass per user instruction  
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
- `CHANGELOG.md` (75,346 chars — v2.0.18 and prior entries read)
- `LICENSE` (1,067 chars)

**Template**

- `template/CLAUDE.md` (20,641 chars)
- `template/scheduled-tasks/refresh-hot.md` (3,966 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,877 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/query.md` (2,586 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars)
- `template/scheduled-tasks/ops/audit.md` (6,599 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,797 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (4,185 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,533 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,838 chars)

**Not in audit scope:** `blueprint/` sub-directory internals (working-folder-level installed files), `ROADMAP.md` (planning doc, no logic content).

---

### 1.2 Verification that audit #22 findings are resolved and v2.0.18 changes are consistent

Audit #22 left two STYLE findings (S1: stale v2.0.17 narrative measurement; S2: forward-look on CHANGELOG.md calibration gap requiring envelope widening at next recalibration). v2.0.18 was applied before this pass. Direct re-verification:

| Item | Claim | Re-verified |
|---|---|---|
| #22 S1 | v2.0.17 CHANGELOG narrative cites `~72,182 chars` / `22.6%`; post-entry actual is 73,333 | ✓ v2.0.18 corrected in-place to `~73,300` / `~20.7%` (+1 char) — consistent with audit #21's retroactive fix pattern |
| #22 S2 | Next CHANGELOG.md recalibration would push table sum above 2% cushion floor; envelope widening required | ✓ v2.0.18 recalibrated CHANGELOG.md (~88,500 → ~94,200 / ~22,130 → ~23,550) and widened envelope from `~65,000` → `~67,000` |
| v2.0.18 cascade | `ops/audit.md` Notes envelope updated to `~30,000–67,000`; widening history includes v2.0.18 | ✓ line 72: `~30,000–67,000`; history: "v2.0.6 … v2.0.7, v2.0.9, v2.0.10, v2.0.11, v2.0.14, v2.0.15, and v2.0.18" |
| v2.0.18 cascade | `user-guide.md` cost table updated to `~30,000–67,000` | ✓ line 201 confirmed |
| v2.0.18 cascade | `user-guide.md` `!! audit` description updated to `~30,000–67,000` | ✓ line 94 confirmed |
| v2.0.18 | `token-reference.md` Step 5 inline envelope updated to `~30,000–67,000`; floor note updated to `~1,340 tokens on a 67,000-token envelope` | ✓ both confirmed |
| v2.0.18 | Post-fix table sum: 64,370 tokens; cushion: 2,630 (3.93% of 67,000 — above 2% floor) | ✓ arithmetic verified independently (see §1.4) |
| All #11–#22 prior fixes | Verified in prior passes; spot-checked | ✓ no regressions found |

No regressions from v2.0.18 detected on the above items.

---

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Current convention per `token-reference.md` (v2.0.16+): **~125% of measured actual at calibration**, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom % | 10% Soft Floor | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | 467 | ok |
| `setup-guide.md` | 10,564 | ~13,200 | 24.9% | 1,056 | ok |
| `user-guide.md` | 14,219 | ~17,800 | 25.2% | 1,422 | ok |
| `troubleshooting.md` | 22,670 | ~28,300 | 24.8% | 2,267 | ok |
| `CHANGELOG.md` | 75,346 | ~94,200 | 25.0% | 7,535 | ok |
| `LICENSE` | 1,067 | ~1,400 | 31.2% | 107 | ok |
| `template/CLAUDE.md` | 20,641 | ~25,800 | 25.0% | 2,064 | ok |
| `refresh-hot.md` | 3,966 | ~5,100 | 28.6% | 397 | ok |
| `ops/ingest.md` | 15,877 | ~19,800 | 24.7% | 1,588 | ok |
| `ops/lint.md` | 2,507 | ~3,100 | 23.7% | 251 | ok |
| `ops/query.md` | 2,586 | ~3,300 | 27.6% | 259 | ok |
| `ops/update.md` | 1,881 | ~2,400 | 27.6% | 188 | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 24.6% | 674 | ok |
| `ops/audit.md` | 6,599 | ~8,200 | 24.2% | 660 | ok |
| `ops/token-reference.md` | 6,797 | ~8,500 | 25.0% | 680 | ok |
| `skills/sqlite-query/SKILL.md` | 4,185 | ~5,200 | 24.2% | 419 | ok |
| `skills/sqlite-query/query-layer.md` | 2,533 | ~3,200 | 26.3% | 253 | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,838 | ~3,500 | 23.3% | 284 | ok |

No hard triggers (measured ≥ documented). No soft triggers (all headroom values ≥ 10% of measured actual — minimum 23.3% on `ingest-hook.md`). No recalibration required.

**CHANGELOG.md headroom note.** The CHANGELOG.md row was freshly calibrated in v2.0.18 against ~75,344 chars (narrative figure — see S1). The actual measured size is 75,346 chars. At 125%: 75,346 × 1.25 = 94,182.5 → rounds to ~94,200. The documented value is ~94,200. Headroom = (94,200 − 75,346) / 75,346 = 25.0%. No trigger fires; no recalibration required.

---

### 1.4 Envelope check (Recalibration Rule Step 5)

Documented rows sum from `token-reference.md` (updated in v2.0.18):

| Group | Tokens |
|---|---:|
| Blueprint-doc (README 1,500 + setup-guide 3,300 + user-guide 4,450 + troubleshooting 7,080 + CHANGELOG 23,550 + LICENSE 350) | 40,230 |
| Template-side (CLAUDE 6,450 + refresh-hot 1,280 + ingest 4,950 + lint 780 + query 830 + update 600 + conventions 2,100 + audit 2,050 + token-reference 2,120) | 21,160 |
| Skill rows (SKILL.md 1,300 + query-layer 800 + ingest-hook 880) | 2,980 |
| **Total** | **64,370** |

Envelope: `~30,000–67,000` (per `ops/audit.md` line 72).  
Cushion: 67,000 − 64,370 = **2,630 tokens (3.93%)**. Above the 2% floor (~1,340 tokens on a 67,000-token envelope). No envelope widening required.

---

### 1.5 Cross-reference sanity checks

- `template/CLAUDE.md:9` cold-start self-cost `~6,450` = token-reference CLAUDE.md row (`~25,800 / ~6,450`). ✓
- `template/CLAUDE.md:17` cold-start total `~6,530` = 6,450 + 80 (hot.md). ✓
- `template/CLAUDE.md:17` `!! ready` total `~7,480` = 6,530 + 950 (memory.md full). ✓
- `user-guide.md:9` CLAUDE.md cost `~6,450` — matches token-reference row. ✓
- `user-guide.md:14` cold-start `~6,530` — consistent with CLAUDE.md:17. ✓
- `user-guide.md:94` audit-all `~30,000–67,000` — matches `ops/audit.md`. ✓
- `user-guide.md:201` "Audit all (full blueprint) | ~30,000–67,000" — matches `ops/audit.md`. ✓
- `user-guide.md` `!! wrap` realistic `~3,000` / `!! ready` realistic `~3,300` — derivable from current token-reference component values (refresh-hot 1,280 + index 250 + log-tail 625 + log-append 100 + memory-write ~750 ≈ 3,005 ≈ ~3,000; +950 −750 +50 ≈ 3,255 ≈ ~3,300). ✓
- `README.md` cold-start `~6,530` — matches CLAUDE.md:17. ✓
- `ops/audit.md` envelope `~30,000–67,000` — consistent with token-reference sum (64,370 tokens, cushion 2,630). ✓
- `ops/audit.md` envelope widening history: lists v2.0.6, v2.0.7, v2.0.9, v2.0.10, v2.0.11, v2.0.14, v2.0.15, and v2.0.18 — v2.0.12, v2.0.13, v2.0.16, v2.0.17 correctly absent (none widened the envelope). ✓
- `ops/token-reference.md` self-cost note: both occurrences in header read `~2,120 tokens` — matches table row `~8,500 / ~2,120`. ✓
- `ops/token-reference.md` Recalibration Rule Step 5: inline "(currently `~30,000–67,000`)" — matches updated envelope. ✓
- `ops/token-reference.md` Recalibration Rule Step 5: floor note "(~1,340 tokens on a 67,000-token envelope)" — 67,000 × 2% = 1,340 ✓.
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
- `SKILL.md §Fallback Behaviour` documents DB desync recovery (!! install sqlite-query backfill). ✓
- `ops/conventions.md` Query Layer Hook Contract explicitly prohibits glob patterns; requires `find`-via-subprocess. ✓
- `ops/update.md` Step 5.5 ingest-hook call — present and correct. ✓
- `ops/audit.md` scope parenthetical "currently `refresh-hot.md`" — accurate after `changelog-monitor.md` removal (v2.0.11). ✓
- **`CHANGELOG.md` v2.0.18 narrative cites `"pre-entry ~73,334"` and `"~75,344 chars"` for CHANGELOG.md; actual measurements are 73,333 (audit #22) and 75,346 (this pass).** ⚠️ (see S1 — same cascade-miss class as v2.0.15 and v2.0.17, but at noise-floor scale)

---

## 2. Findings

### CRITICAL

None.

### WARNING

None.

### STYLE

**S1 — `CHANGELOG.md` v2.0.18 narrative contains minor measurement rounding discrepancies: cites `"pre-entry ~73,334"` (actual: 73,333) and `"grew CHANGELOG.md to ~75,344 chars"` (actual: 75,346). Third occurrence of the cascade-miss class; at noise-floor scale (1–2 chars) with zero downstream value impact.**

*Evidence.*

`CHANGELOG.md` v2.0.18 narrative:
> "Adding v2.0.18 entry grew CHANGELOG.md to ~75,344 chars (pre-entry ~73,334)."

`wc -c blueprint/CHANGELOG.md` (audit #22, pre-v2.0.18): **73,333 chars** (narrative: 73,334 — off by 1).  
`wc -c blueprint/CHANGELOG.md` (this audit, post-v2.0.18): **75,346 chars** (narrative: 75,344 — off by 2).

*Downstream impact: zero.*

- 75,344 × 1.25 = 94,180 → ~94,200
- 75,346 × 1.25 = 94,182.5 → ~94,200

Both measurements round to the same documented Chars value (~94,200). The token-reference.md row (~94,200 / ~23,550) is correct. The table sum (64,370 tokens), cushion (2,630 / 3.93%), and envelope (~30,000–67,000) are all unaffected. The envelope-widening decision was correct under either measurement (630 tokens = 0.97% of 65,000 → below the 2% floor, widening required).

*Historical pattern comparison.*

| Version | Pre-entry delta | Post-entry delta | Source-of-truth values wrong? |
|---|---:|---:|:---:|
| v2.0.15 | — | +593 chars | ✓ Yes (caused ~87,900 vs ~88,500 discrepancy) |
| v2.0.17 | — | +1,151 chars | No (narrative stale but no table values affected) |
| v2.0.18 | 1 char | 2 chars | No (rounds to same ~94,200 either way) |

This is the smallest instance of the pattern by two orders of magnitude and produces no source-of-truth errors whatsoever. The fix is a cosmetic one-sentence update to the CHANGELOG narrative: change `"pre-entry ~73,334"` to `"pre-entry ~73,333"` and `"~75,344 chars"` to `"~75,346 chars"`. May be bundled into the next substantive CHANGELOG entry if no other findings warrant a patch.

*Root cause.* Consistent with v2.0.15 and v2.0.17: the narrative was drafted against the pre-finalization file size; writing the entry itself added 2 chars, pushing the total above the quoted figure. The effect is now so small (< 0.003% difference) that it produces identical calibration values.

---

## 3. Non-findings (considered and dismissed)

- **Cold-start total `~6,530`** — 6,450 (CLAUDE.md) + 80 (hot.md). ✓
- **`!! ready` total `~7,480`** — 6,530 + 950 (memory.md full). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — derivable from current token-reference component values. ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
- **Ingest atomic ordering** — Step 5 pre-compute → Step 6 mv → Step 7 page write. ✓
- **Hash canonicalization 6-step pipeline** — intact. ✓
- **`Pages: N` derived** — `refresh-hot.md` counts `^- [[` entries; not a stored counter. ✓
- **Blueprint-authoring mode guard** — present in CLAUDE.md, audit.md:44. ✓
- **Blueprint Sync Rule 12-row matrix** — intact; no new untriggered changes detected beyond S1. ✓
- **`SKILL.md` install/uninstall symmetry** — file targets match; DB-keep option on uninstall correctly defaults to no. ✓
- **sqlite-query DB schema** — `pages` table, `relations` table, four indexes; `type` CHECK constraint; upsert pattern and bidirectional-relation `INSERT OR IGNORE` all correct. ✓
- **`query-layer.md` `find`-based path resolution** — correctly implemented; unmatched slugs silently skipped, triggering grep fallback. ✓
- **`ingest-hook.md` exception handler and Notes section** — both point to `!! install sqlite-query` backfill repair path; consistent with `SKILL.md §Fallback Behaviour`. ✓
- **`ops/ingest.md` B5 step enumeration** — `11.5` present in per-file list. ✓
- **`ops/update.md` Step 5.5** — ingest-hook call present; non-fatal error handling consistent with hook contract. ✓
- **`ops/token-reference.md` self-cost note** — both occurrences read `~2,120 tokens`, matching the table row. ✓
- **`ops/ingest.md` cross-reference to troubleshooting.md** — "URL ingest keeps regenerating the same source even when the article hasn't changed" exists in `troubleshooting.md`. ✓
- **v2.0.18 envelope arithmetic.** Pre-envelope table sum: 62,950 (from v2.0.15); new CHANGELOG.md token row: +1,420 (23,550 − 22,130); new total: 64,370. Old cushion: 65,000 − 64,370 = 630 tokens (0.97% of 65,000 — below 2% floor of ~1,300). Widening to 67,000 required and applied. Post-widening cushion: 67,000 − 64,370 = 2,630 tokens (3.93% of 67,000 — above 2% floor of ~1,340). ✓
- **v2.0.18 CHANGELOG cascade completeness.** The cascade list mentions `ops/audit.md`, `user-guide.md` (cost table), and `user-guide.md` (!! audit description). It does not explicitly list `ops/token-reference.md` Step 5's inline envelope reference, which was also updated. However, updating the CHANGELOG.md row and the envelope in token-reference.md is a single contiguous edit within that file; the inline "(currently `~30,000–67,000`)" update is implicit in the recalibration edit, not a separate cascade target enumerated in the Blueprint Sync Rule table. No finding — the cascade was executed correctly; only the level of cascade-list detail is debatable.
- **`ops/audit.md:71` line-number reference in `token-reference.md` Step 5.** The envelope note cites "`ops/audit.md:71`"; the actual envelope line in the current file is at line 72. Line numbers are informational only and not semantically binding. Not flagged.
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form only; 3-argument GNU-awk form correctly avoided. ✓
- **`.gitignore` scope** — correctly scopes to inside `blueprint/`; setup-guide.md correctly explains this does not govern `wiki/.obsidian/`. ✓
- **CHANGELOG.md v2.0.18 entry.** v2.0.18 CHANGELOG token arithmetic: blueprint-doc 40,230 + template-side 21,160 + skill 2,980 = 64,370 — independently verified. ✓
- **`ROADMAP.md`** — planning doc; not in audit scope.
- **`LICENSE`** — MIT; no issues.

---

## 4. Questions for Clarification

None. All findings are self-contained.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#22 re-verified:

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

**The v2.0.18 blueprint has no CRITICAL or WARNING findings. One STYLE note: the CHANGELOG v2.0.18 narrative contains 1–2 char measurement rounding discrepancies (pre-entry 73,334 vs actual 73,333; post-entry ~75,344 vs actual 75,346) that produce zero downstream value errors.**

No architectural regressions. All prior findings from audits #11–#22 are verified clean. The v2.0.18 changes (CHANGELOG.md recalibration and envelope widening to ~30,000–67,000) are internally consistent: token-reference.md correctly tracks ~94,200/~23,550, the table sum is independently verified at 64,370 tokens, the cushion is 2,630 tokens (3.93% of 67,000 — above the 2% floor), and all three cascade targets (ops/audit.md, user-guide.md cost table, user-guide.md !! audit description) are confirmed updated. All 18 tracked files pass their headroom checks; no triggers fire.

S1 is the third occurrence of the CHANGELOG narrative cascade-miss pattern (v2.0.15 was first — 593 chars, source-of-truth impact; v2.0.17 was second — 1,151 chars, cosmetic only; v2.0.18 is third — 2 chars, rounding artifact, zero impact). The pattern is inherent to writing CHANGELOG entries that reference the file's own pre-finalization size. At this scale it is essentially a rounding note, not a defect.

**Priority order for follow-up (if any):**

1. **S1** — Bundle a one-sentence correction of the v2.0.18 narrative (`"pre-entry ~73,334"` → `"pre-entry ~73,333"`, `"~75,344 chars"` → `"~75,346 chars"`) into the next substantive CHANGELOG entry. No downstream cascade required — all source-of-truth values are correct everywhere else.

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
