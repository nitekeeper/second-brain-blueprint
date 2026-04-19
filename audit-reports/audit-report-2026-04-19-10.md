# Blueprint Audit Report — 2026-04-19 (#20)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.16 (per CHANGELOG.md; no later entry found)  
**Prior audits reviewed:** #11–#19 (`audit-report-2026-04-19-01.md` through `audit-report-2026-04-19-09.md`) — read in full before this pass per user instruction  
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
- `CHANGELOG.md` (72,181 chars — first 130 lines read; v2.0.16 and v2.0.15 entries read in full)
- `LICENSE` (1,067 chars)

**Template**

- `template/CLAUDE.md` (20,641 chars)
- `template/scheduled-tasks/refresh-hot.md` (3,966 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,877 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/query.md` (2,586 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars)
- `template/scheduled-tasks/ops/audit.md` (6,590 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,797 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (4,185 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,533 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,838 chars)

**Not in audit scope:** `blueprint/` sub-directory internals (working-folder-level installed files), `ROADMAP.md` (planning doc, no logic content).

---

### 1.2 Verification that audit #19 findings are resolved and v2.0.16 changes are consistent

Audit #19 left v2.0.15 with two STYLE findings. v2.0.16 was applied before this pass. Direct re-verification:

| Item | Claim | Re-verified |
|---|---|---|
| #19 S1 | CHANGELOG v2.0.15 narrative cites `~87,900 / ~21,980` while token-reference.md and post-fix envelope both show `~88,500 / ~22,130` | ✗ **still present** — no fix applied between audits #19 and #20 |
| #19 S2 | Nine files fire the ~25% soft trigger; recalibration produces no value changes | ✓ resolved — v2.0.16 corrected the soft trigger threshold to ~10%; none of the nine files fire at the new threshold |
| v2.0.16 | `ops/token-reference.md` Recalibration Rule: soft trigger updated from ~25% to ~10% of measured actual | ✓ line 74 reads "below ~10% of its measured actual" |
| v2.0.16 | "No file-size or token-table changes" | ✓ confirmed — all 18 tracked file sizes match audit #19 measurements except CHANGELOG.md (+1,334 chars from the v2.0.16 entry itself, no other changes) |
| v2.0.16 | "All tracked files have headroom well above 10% (minimum 23.3% — `ingest-hook.md`)" | ✓ verified against current `wc -c` measurements (see §1.3) |
| v2.0.16 | No envelope change, no cold-start cascade required | ✓ token-reference table unchanged; envelope sum remains 62,950; cold-start figures unchanged |

---

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Current convention per `token-reference.md` (v2.0.16): **~125% of measured actual at calibration**, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom % of measured | Flag |
|---|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | ok |
| `setup-guide.md` | 10,564 | ~13,200 | 24.9% | ok |
| `user-guide.md` | 14,219 | ~17,800 | 25.2% | ok |
| `troubleshooting.md` | 22,670 | ~28,300 | 24.8% | ok |
| `CHANGELOG.md` | 72,181 | ~88,500 | 22.6% | ok |
| `LICENSE` | 1,067 | ~1,400 | 31.2% | ok |
| `template/CLAUDE.md` | 20,641 | ~25,800 | 25.0% | ok |
| `refresh-hot.md` | 3,966 | ~5,100 | 28.6% | ok |
| `ops/ingest.md` | 15,877 | ~19,800 | 24.7% | ok |
| `ops/lint.md` | 2,507 | ~3,100 | 23.7% | ok |
| `ops/query.md` | 2,586 | ~3,300 | 27.6% | ok |
| `ops/update.md` | 1,881 | ~2,400 | 27.6% | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 24.6% | ok |
| `ops/audit.md` | 6,590 | ~8,200 | 24.4% | ok |
| `ops/token-reference.md` | 6,797 | ~8,500 | 25.0% | ok |
| `skills/sqlite-query/SKILL.md` | 4,185 | ~5,200 | 24.2% | ok |
| `skills/sqlite-query/query-layer.md` | 2,533 | ~3,200 | 26.3% | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,838 | ~3,500 | 23.3% | ok |

No hard triggers (measured ≥ documented). No soft triggers (all headroom values ≥ 10% of measured actual — minimum 22.6% on CHANGELOG.md). No recalibration required.

Note on CHANGELOG.md: the v2.0.16 entry grew the file from 70,847 (audit #19) to 72,181 (+1,334 chars). At 125%: 72,181 × 1.25 = 90,226 → ~90,200, which differs from the documented ~88,500 by +1,700 chars (+425 tokens). Neither the hard trigger (72,181 < 88,500) nor the soft trigger (headroom 22.6% > 10%) fires. Optional note for next recalibration: when CHANGELOG.md next recalibrates, update to ~90,200 / ~22,550 (+420 token delta to table sum; envelope impact: sum rises from 62,950 to ~63,370, cushion drops from 2,050 to ~1,630 — still above the 2% floor of ~1,300). No action required now.

---

### 1.4 Envelope check (Recalibration Rule Step 5)

Documented rows sum from `token-reference.md` (unchanged since v2.0.15):

| Group | Tokens |
|---|---:|
| Blueprint-doc (README 1,500 + setup-guide 3,300 + user-guide 4,450 + troubleshooting 7,080 + CHANGELOG 22,130 + LICENSE 350) | 38,810 |
| Template-side (CLAUDE 6,450 + refresh-hot 1,280 + ingest 4,950 + lint 780 + query 830 + update 600 + conventions 2,100 + audit 2,050 + token-reference 2,120) | 21,160 |
| Skill rows (SKILL.md 1,300 + query-layer 800 + ingest-hook 880) | 2,980 |
| **Total** | **62,950** |

Envelope: `~30,000–65,000` (per `ops/audit.md:72`).  
Cushion: 65,000 − 62,950 = **2,050 tokens (3.15%)**. Above the 2% floor (~1,300 tokens on a 65,000-token envelope). No envelope widening required.

---

### 1.5 Cross-reference sanity checks

- `template/CLAUDE.md:9` cold-start self-cost `~6,450` = token-reference CLAUDE.md row (`~25,800 / ~6,450`). ✓
- `template/CLAUDE.md:17` cold-start total `~6,530` = 6,450 + 80 (hot.md). ✓
- `template/CLAUDE.md:17` `!! ready` total `~7,480` = 6,530 + 950 (memory.md full). ✓
- `user-guide.md:9` CLAUDE.md cost `~6,450` — matches token-reference row. ✓
- `user-guide.md:14` cold-start `~6,530` — consistent with CLAUDE.md:17. ✓
- `user-guide.md:94` and `:201` audit-all `~30,000–65,000` — matches `ops/audit.md:72`. ✓
- `user-guide.md` `!! wrap` realistic `~3,000` / `!! ready` realistic `~3,300` — derivable from current token-reference component values (refresh-hot 1,280 + index 250 + log-tail 625 + log-append 100 + memory-write ~750 ≈ 3,005 ≈ ~3,000; +950 −750 +50 ≈ 3,255 ≈ ~3,300). ✓
- `README.md:72` cold-start `~6,530` — matches CLAUDE.md:17. ✓
- `ops/audit.md:72` envelope `~30,000–65,000` — consistent with token-reference sum (62,950). ✓
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:70–72`, `README.md:73`, and `user-guide.md:175`. ✓
- Blueprint Sync Rule 12-row matrix — intact. ✓
- Versioning split (`Schema version: 2.0` in CLAUDE.md footer; patch bumps X.Y.Z in CHANGELOG only) — consistent. ✓
- Ingest atomic ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
- Hash canonicalization 6-step pipeline intact in `ops/ingest.md §Hash Canonicalization`. ✓
- `ops/ingest.md` B5 per-file step list `[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]` — confirmed. ✓
- `ops/ingest.md:55` cross-reference: "See `troubleshooting.md` 'URL ingest keeps regenerating the same source even when the article hasn't changed'" — matches actual section heading in `troubleshooting.md`. ✓
- Blueprint-authoring mode guard present in `template/CLAUDE.md`, `ops/audit.md:44`. ✓
- `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading. ✓
- `query-layer.md` uses `find`-based path resolution — satisfies Query Layer Hook Contract. ✓
- `ingest-hook.md` exception handler and Notes section second bullet — both point to `!! install sqlite-query` repair path. ✓
- `ops/conventions.md` Query Layer Hook Contract explicitly prohibits glob patterns. ✓
- `ops/update.md` Step 5.5 ingest-hook call — present and correct. ✓
- `ops/audit.md:23` scope parenthetical "currently `refresh-hot.md`" — accurate after `changelog-monitor.md` removal (v2.0.11). ✓
- `ops/token-reference.md` self-cost note header: both occurrences read `~2,120 tokens` — matches table row `~8,500 / ~2,120`. ✓
- **`CHANGELOG.md` v2.0.15 narrative cites `~87,900 / ~21,980` and `~62,800 tokens` (for CHANGELOG.md recalibration); token-reference.md and the post-fix envelope both show `~88,500 / ~22,130` and `~62,950 tokens`.** ⚠️ (see S1 — carry-forward from audit #19)

---

## 2. Findings

### CRITICAL

None.

### WARNING

None.

### STYLE

**S1 — `CHANGELOG.md` v2.0.15 narrative contains internally inconsistent calibration figures for the CHANGELOG.md row: narrative body says `~87,900 / ~21,980` and `~62,800 tokens`; post-fix envelope and `token-reference.md` (source of truth) both show `~88,500 / ~22,130` and `~62,950 tokens`. Carry-forward from audit #19; no fix applied between passes.**

*Evidence.*

`CHANGELOG.md` v2.0.15 narrative (lines ~59–63):
> "Adding the v2.0.15 entry grew CHANGELOG.md to 70,207 chars. Recalibrated at 125%: 70,207 × 1.25 = 87,759 → **~87,900 / ~21,980** (was ~84,600 / ~21,150). New table sum ~62,800 tokens pushed the cushion to 1,200 tokens (1.875% of 64,000 — below the 2% floor)…"

`CHANGELOG.md` v2.0.15 post-fix envelope (lines ~69–79):
> "CHANGELOG (**22,130**, see token-reference.md)" and "**Total ≈ 62,950 tokens**"

`token-reference.md` File Read Costs table:
> `| blueprint/CHANGELOG.md | ~88,500 | ~22,130 |`

*Root cause (unchanged from audit #19).* The narrative was drafted when CHANGELOG.md measured ~70,207 chars. By the time token-reference.md was actually updated (after the full v2.0.15 entry was finalized), CHANGELOG.md had grown to ~70,800 chars (70,800 × 1.25 = 88,500 → ~22,130, sum 62,950). The post-fix envelope section was updated to the final values but the narrative paragraph was not revised, leaving a single CHANGELOG entry that cites two different calibration values for the same file.

*Impact.* No functional impact. `token-reference.md` (source of truth) is correct at ~88,500 / ~22,130. The envelope decision (cushion below the 2% floor of 64,000, triggering widening to 65,000) is valid under either figure. A maintainer auditing the v2.0.15 entry arithmetic would observe the mismatch between the narrative body and the applied values.

*Recommended fix.* Update the v2.0.15 narrative to: (a) replace "70,207" with "~70,800", (b) replace "87,759" with "88,500", (c) replace "~87,900 / ~21,980" with "~88,500 / ~22,130", and (d) replace "~62,800 tokens" / "1,200 tokens (1.875%)" with "~62,950 tokens" / "~1,050 tokens (1.64%)". One-paragraph CHANGELOG edit; no downstream cascade required.

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
- **`ingest-hook.md` `type_` / `type` naming** — `type_` is the Python variable (reserved-word avoidance); `type` is the SQL column name; correctly threaded through the upsert. ✓
- **`ingest-hook.md` Notes section** — second bullet correctly points to `!! install sqlite-query` repair path (v2.0.13 W1). ✓
- **`ops/ingest.md` B5 step enumeration** — `11.5` present in per-file list (v2.0.13 W2). ✓
- **`ops/update.md` Step 5.5** — ingest-hook call present; non-fatal error handling consistent with hook contract. ✓
- **`ops/token-reference.md` self-cost note** — both occurrences read `~2,120 tokens`, matching the table row (v2.0.15 W1). ✓
- **`ops/ingest.md` cross-reference to troubleshooting.md** — "URL ingest keeps regenerating the same source even when the article hasn't changed" exists in `troubleshooting.md` (v2.0.15 W2). ✓
- **v2.0.16 soft-trigger rationale.** The claim that a ~25% threshold "fires immediately on any post-calibration growth" is arithmetically correct: fresh calibration sets Chars = 1.25 × measured, giving headroom = 25% of measured. Any subsequent growth causes headroom to drop below 25% of the new measured value, triggering the rule. ✓
- **v2.0.16 "back to ~10%" phrasing.** The CHANGELOG entry says "corrected from ~25% back to ~10%", implying ~10% was a prior value. The historical sequence was ~3% → ~25% (v2.0.14) → ~10% (v2.0.16); ~10% is a new intermediate value, not a restoration. The explanatory paragraph immediately below ("The correct ongoing threshold is ~10%, which gives meaningful lead time…") makes clear this is a fresh choice, so no reader confusion is likely. Not flagged — the paragraph body is accurate; the headline phrasing is mildly imprecise.
- **v2.0.16 Blueprint Sync cascade.** The only change was `ops/token-reference.md` Recalibration Rule (one sentence). No cold-start figures changed; no envelope changed; no skill files changed. No Blueprint Sync cascade beyond the CHANGELOG entry was required. ✓
- **`ops/audit.md` envelope-widening history note** — lists v2.0.6, v2.0.7, v2.0.9, v2.0.10, v2.0.11, v2.0.14, and v2.0.15. v2.0.16 correctly absent (it did not widen the envelope). ✓
- **`ops/audit.md` step 7 recalibration clause.** Step 7 says "only if an applied fix changed a tracked file's size enough to exceed its documented Chars value" — describes only the hard trigger. The soft trigger for an audit pass is covered by the §1.3 headroom table (format convention), not by a step-level rule. Consistent with all prior audits. Not flagged.
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form only; 3-argument GNU-awk form correctly avoided. ✓
- **`ops/audit.md` scope parenthetical** — "currently `refresh-hot.md`" accurate after `changelog-monitor.md` removal (v2.0.11). ✓
- **CHANGELOG.md row recalibration note.** The current measurement (72,181 chars) would round to ~90,200 at 125%, vs. the documented ~88,500 — a +1,700-char gap. Neither the hard nor soft trigger fires (headroom 22.6% > 10%). The gap is flagged informally in §1.3 for the next recalibration pass; no action required now.
- **`ROADMAP.md`** — planning doc; not in audit scope.
- **`LICENSE`** — MIT; no issues.

---

## 4. Questions for Clarification

None. All findings are self-contained.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#19 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:44`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md:72` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~10% of measured actual — corrected v2.0.16), envelope cushion floor (cushion < ~2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. ✓
11. sqlite-query skill follows Query Layer Hook Contract (`find`-based path resolution, no glob patterns) and Ingest Hook Contract (non-fatal errors, consistent repair messaging across exception handler, Notes section, and `SKILL.md §Fallback Behaviour`). ✓ fully satisfied.

---

## 6. Verdict

**The v2.0.16 blueprint has no CRITICAL or WARNING findings. One STYLE note: the CHANGELOG v2.0.15 narrative inconsistency (S1) carried forward from audit #19 remains unresolved.**

No architectural regressions. All prior findings from audits #11–#19 are verified clean. The ingest pipeline, approval flow, hash canonicalization, Blueprint Sync Rule, Recalibration Rule, and all sqlite-query hook contracts are fully intact.

The v2.0.16 change (soft trigger corrected from ~25% to ~10%) is internally consistent: token-reference.md line 74 reflects the new value, the CHANGELOG entry documents the rationale, and no cascade to other files was required. The nine files that fired the ~25% trigger in audit #19 are all clear at the ~10% threshold; the minimum headroom across all tracked files is 22.6% (CHANGELOG.md).

S1 is a documentation-only inconsistency in the v2.0.15 CHANGELOG narrative — the source-of-truth values in `token-reference.md` and the post-fix envelope are correct everywhere else. A one-paragraph CHANGELOG edit covers it with no downstream cascade.

**Priority order for follow-up (if any):**

1. **S1** — Update v2.0.15 CHANGELOG narrative to replace "70,207 chars" / "~87,900 / ~21,980" / "~62,800 tokens" / "1,200 tokens (1.875%)" with the values matching the applied calibration (~70,800 chars / ~88,500 / ~22,130 / ~62,950 tokens / ~1,050 tokens (1.64%)). One-paragraph fix; no downstream cascade — source-of-truth values are already correct everywhere else.

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
