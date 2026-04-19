# Blueprint Audit Report — 2026-04-19 (#22)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.17 (per CHANGELOG.md; no later entry found)  
**Prior audits reviewed:** #11–#21 (`audit-report-2026-04-19-01.md` through `audit-report-2026-04-19-11.md`) — read in full before this pass per user instruction  
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
- `CHANGELOG.md` (73,333 chars — v2.0.17 and prior entries read)
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

### 1.2 Verification that audit #21 finding is resolved and v2.0.17 is consistent

Audit #21 left one STYLE finding: a missing CHANGELOG entry for the retroactive v2.0.15 narrative fix. v2.0.17 was applied before this pass. Direct re-verification:

| Item | Claim | Re-verified |
|---|---|---|
| #21 S1 | Missing CHANGELOG entry for retroactive v2.0.15 narrative correction | ✓ v2.0.17 entry present, documents the +1-char retroactive fix, confirms no token-table changes |
| v2.0.17 | CHANGELOG.md measured at entry time: "~72,182" | ✓ consistent with audit #21 measurement (72,182 before v2.0.17 was written) |
| v2.0.17 | No file-size or token-table changes | ✓ confirmed — token-reference.md values unchanged |
| v2.0.17 | Headroom claim "22.6%" based on ~72,182 chars | ⚠️ post-entry measurement is 73,333 (headroom 20.7%) — see S1 |

All prior findings from audits #11–#21 carry forward as verified clean. No regressions.

---

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Current convention per `token-reference.md` (v2.0.16+): **~125% of measured actual at calibration**, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom | 10% Soft Floor | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | 467 chars | ok |
| `setup-guide.md` | 10,564 | ~13,200 | 24.9% | 1,056 chars | ok |
| `user-guide.md` | 14,219 | ~17,800 | 25.2% | 1,422 chars | ok |
| `troubleshooting.md` | 22,670 | ~28,300 | 24.8% | 2,267 chars | ok |
| `CHANGELOG.md` | 73,333 | ~88,500 | 20.7% | 7,333 chars | ok (see S2) |
| `LICENSE` | 1,067 | ~1,400 | 31.2% | 107 chars | ok |
| `template/CLAUDE.md` | 20,641 | ~25,800 | 25.0% | 2,064 chars | ok |
| `refresh-hot.md` | 3,966 | ~5,100 | 28.6% | 397 chars | ok |
| `ops/ingest.md` | 15,877 | ~19,800 | 24.7% | 1,588 chars | ok |
| `ops/lint.md` | 2,507 | ~3,100 | 23.7% | 251 chars | ok |
| `ops/query.md` | 2,586 | ~3,300 | 27.6% | 259 chars | ok |
| `ops/update.md` | 1,881 | ~2,400 | 27.6% | 188 chars | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 24.6% | 674 chars | ok |
| `ops/audit.md` | 6,590 | ~8,200 | 24.4% | 659 chars | ok |
| `ops/token-reference.md` | 6,797 | ~8,500 | 25.0% | 680 chars | ok |
| `skills/sqlite-query/SKILL.md` | 4,185 | ~5,200 | 24.2% | 419 chars | ok |
| `skills/sqlite-query/query-layer.md` | 2,533 | ~3,200 | 26.3% | 253 chars | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,838 | ~3,500 | 23.3% | 284 chars | ok |

No hard triggers (measured ≥ documented). No soft triggers (all headroom values ≥ 10% of measured actual — minimum 20.7% on CHANGELOG.md). No recalibration required.

---

### 1.4 Envelope check (Recalibration Rule Step 5)

Documented rows sum from `token-reference.md` (unchanged since v2.0.15):

| Group | Tokens |
|---|---:|
| Blueprint-doc (README 1,500 + setup-guide 3,300 + user-guide 4,450 + troubleshooting 7,080 + CHANGELOG 22,130 + LICENSE 350) | 38,810 |
| Template-side (CLAUDE 6,450 + refresh-hot 1,280 + ingest 4,950 + lint 780 + query 830 + update 600 + conventions 2,100 + audit 2,050 + token-reference 2,120) | 21,160 |
| Skill rows (SKILL.md 1,300 + query-layer 800 + ingest-hook 880) | 2,980 |
| **Total** | **62,950** |

Envelope: `~30,000–65,000` (per `ops/audit.md`).  
Cushion: 65,000 − 62,950 = **2,050 tokens (3.15%)**. Above the 2% floor (~1,300 tokens on a 65,000-token envelope). No envelope widening required.

**Forward-look (S2):** CHANGELOG.md at 73,333 chars would recalibrate to ~91,700 / ~22,925 (73,333 × 1.25 = 91,666 → rounded). This would raise the blueprint-doc sum from 38,810 to 39,605 and the table total from 62,950 to 63,745. Cushion: 65,000 − 63,745 = 1,255 tokens (1.93% of 65,000 — **below** the 2% floor of ~1,300). The next CHANGELOG.md recalibration will therefore require an envelope widening. No action today; flagged in S2.

---

### 1.5 Cross-reference sanity checks

- `template/CLAUDE.md:9` cold-start self-cost `~6,450` = token-reference CLAUDE.md row (`~25,800 / ~6,450`). ✓
- `template/CLAUDE.md:17` cold-start total `~6,530` = 6,450 + 80 (hot.md). ✓
- `template/CLAUDE.md:17` `!! ready` total `~7,480` = 6,530 + 950 (memory.md full). ✓
- `user-guide.md:9` CLAUDE.md cost `~6,450` — matches token-reference row. ✓
- `user-guide.md:14` cold-start `~6,530` — consistent with CLAUDE.md:17. ✓
- `user-guide.md:94` and `:201` audit-all `~30,000–65,000` — matches `ops/audit.md` envelope. ✓
- `README.md:72` cold-start `~6,530` — matches CLAUDE.md:17. ✓
- `ops/audit.md` envelope `~30,000–65,000` — consistent with token-reference sum (62,950). ✓
- `ops/token-reference.md` self-cost note: both occurrences in header read `~2,120 tokens` — matches table row `~8,500 / ~2,120`. ✓
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:70–72`, `README.md:72–73`, and `user-guide.md:175`. ✓
- Blueprint Sync Rule 12-row matrix — intact. ✓
- Versioning split (`Schema version: 2.0` in CLAUDE.md footer; patch bumps X.Y.Z in CHANGELOG only) — consistent. ✓
- `ops/token-reference.md` Recalibration Rule soft trigger: "below ~10% of its measured actual" — confirmed (v2.0.16 correction). ✓
- Ingest atomic ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
- Hash canonicalization 6-step pipeline intact in `ops/ingest.md §Hash Canonicalization`. ✓
- `ops/ingest.md` B5 per-file step list `[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]` — confirmed. ✓
- `ops/ingest.md` cross-reference: "See `troubleshooting.md` 'URL ingest keeps regenerating the same source even when the article hasn't changed'" — heading present in `troubleshooting.md`. ✓
- Blueprint-authoring mode guard present in `template/CLAUDE.md`, `ops/audit.md:44`. ✓
- `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading "## Step 4.5 — Offer SQLite Query Skill". ✓
- `query-layer.md` uses `subprocess.run(["find", pages_dir, "-name", ...])` — no glob patterns — satisfies Query Layer Hook Contract. ✓
- `ingest-hook.md` exception handler: points to `!! install sqlite-query` repair path. ✓
- `ingest-hook.md` Notes section second bullet: points to `!! install sqlite-query` repair path. ✓
- `SKILL.md §Fallback Behaviour` documents DB desync recovery (!! install sqlite-query backfill). ✓
- `ops/conventions.md` Query Layer Hook Contract explicitly prohibits glob patterns; requires `find`-via-subprocess. ✓
- `ops/update.md` Step 5.5 ingest-hook call — present and correct. ✓
- `ops/audit.md` envelope widening history: "v2.0.6 ... v2.0.7, v2.0.9, v2.0.10, v2.0.11, v2.0.14, and v2.0.15" — v2.0.16 and v2.0.17 correctly absent (neither widened the envelope). ✓
- **`CHANGELOG.md` v2.0.17 narrative cites `~72,182` chars and `22.6%` headroom for CHANGELOG.md; actual post-entry size is 73,333 (headroom 20.7%).** ⚠️ (see S1)

---

## 2. Findings

### CRITICAL

None.

### WARNING

None.

### STYLE

**S1 — `CHANGELOG.md` v2.0.17 narrative cites stale pre-entry measurement (`~72,182 chars`, `22.6%` headroom); actual post-entry measured size is 73,333 (headroom 20.7%). Same cascade-miss pattern as v2.0.15 / audits #19–#20.**

*Evidence.*

`CHANGELOG.md` v2.0.17 narrative (lines 21–22):
> "The +1 char to CHANGELOG.md stays inside its existing documented headroom (~88,500 chars — current measured ~72,182, headroom 22.6%)."

`wc -c blueprint/CHANGELOG.md` (measured in this audit pass): **73,333 chars**.  
Post-entry headroom: (88,500 − 73,333) / 73,333 = **20.7%**.

*Root cause.* The v2.0.17 narrative was drafted before the entry itself was written, using the pre-entry CHANGELOG.md size (72,182 — the file size immediately after the S1 retroactive fix was applied). Writing the ~1,151-char v2.0.17 entry raised the file to 73,333. The narrative's `~72,182` and `22.6%` claims are now stale by 1,151 chars and ~1.9 percentage points respectively.

*Impact.* The no-action conclusion is still correct: 20.7% headroom is well above the 10% soft trigger. No token-reference values are contradicted (v2.0.17 made no token-table changes). The inconsistency is cosmetic — a future maintainer checking v2.0.17 arithmetic against `wc -c` would observe the mismatch. Lower severity than v2.0.15 (which contradicted `token-reference.md` values) because no source-of-truth values are affected here.

*Recommended fix.* Update the v2.0.17 narrative to replace `~72,182` with `~73,300` (or the exact post-entry measurement) and `22.6%` with `~20.7%`. One-sentence change; no downstream cascade required. May be bundled into the next substantive CHANGELOG entry if no other findings warrant a patch.

---

**S2 — Forward-look: CHANGELOG.md calibration gap will require envelope widening at next recalibration.**

*Evidence.*

- CHANGELOG.md measured: 73,333 chars
- CHANGELOG.md documented: ~88,500 chars
- CHANGELOG.md at 125%: 73,333 × 1.25 = 91,666 → **~91,700 / ~22,925** (vs. current ~88,500 / ~22,130)

When CHANGELOG.md next recalibrates (at the 10% soft trigger or the next hard trigger), the token row rises by +795 tokens (22,925 − 22,130). The table total rises from 62,950 to **63,745 tokens**. Cushion: 65,000 − 63,745 = **1,255 tokens (1.93% of 65,000)** — below the 2% floor (~1,300 tokens). An envelope widening to ~67,000 (63,745 + ~2,000 cushion, rounded to nearest 1,000) will be required.

*Impact.* No action today — no triggers fire and the table is within the envelope. This is a planning note: the next CHANGELOG.md recalibration, whenever it occurs, will trigger the envelope-widening cascade to `ops/audit.md`, `user-guide.md` (cost table and `!! audit` description), and the CHANGELOG entry for that patch. Knowing this in advance avoids a mid-op surprise.

*Recommended action.* None today. Monitor at next recalibration.

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
- **`ops/token-reference.md` self-cost note** — both occurrences read `~2,120 tokens`, matching the table row. ✓
- **`ops/ingest.md` cross-reference to troubleshooting.md** — "URL ingest keeps regenerating the same source even when the article hasn't changed" exists in `troubleshooting.md`. ✓
- **`ops/audit.md` line-reference `ops/audit.md:71`** in token-reference.md Step 5 — stale line number (envelope is now on line ~73), but line numbers are informational only and not semantically binding. Not flagged.
- **`template/CLAUDE.md` setup note block** — the `> **Setup note:** Replace [created-date]…` block at the file's end is intentional scaffolding: `setup-guide.md` Step 3 explicitly instructs the agent to remove it during setup. Its presence in the template is load-bearing. Not a defect.
- **Recalibration convention "after every INGEST operation"** — not triggered in blueprint-authoring mode (no INGEST ops run). ✓
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form only; 3-argument GNU-awk form correctly avoided. ✓
- **`ops/audit.md` envelope widening history** — lists v2.0.6, v2.0.7, v2.0.9, v2.0.10, v2.0.11, v2.0.14, v2.0.15; v2.0.16 and v2.0.17 correctly absent. ✓
- **`ROADMAP.md`** — planning doc; not in audit scope.
- **`LICENSE`** — MIT; no issues.

---

## 4. Questions for Clarification

None. All findings are self-contained.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#21 re-verified:

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

**The v2.0.17 blueprint has no CRITICAL or WARNING findings. Two STYLE notes: a stale measurement in the v2.0.17 CHANGELOG narrative (S1) and a forward-look on the CHANGELOG.md calibration gap that will require an envelope widening at next recalibration (S2).**

No architectural regressions. All prior findings from audits #11–#21 are verified clean. The ingest pipeline, approval flow, hash canonicalization, Blueprint Sync Rule, Recalibration Rule, and all sqlite-query hook contracts are fully intact. All 18 tracked files pass their headroom checks; no triggers fire.

S1 is the third occurrence of the same pattern (v2.0.15 narrative was the first, corrected retroactively by v2.0.17 itself; v2.0.17 narrative is now the second instance). The pattern is inherent to writing CHANGELOG entries that reference the file's own pre-entry size: the entry's own bytes push the total above the quoted figure. The fix is a one-sentence CHANGELOG correction, deferred to the next substantive patch entry.

S2 is a pure forward-look: no triggers fire today, but the next CHANGELOG.md recalibration will require a ~2,000-token envelope widening to ~67,000 (sum ~63,745 + cushion → ~67,000). Knowing this in advance avoids mid-op surprise.

**Priority order for follow-up (if any):**

1. **S1** — Bundle a one-sentence correction of the v2.0.17 narrative (`~72,182 chars` → `~73,300 chars`, `22.6%` → `~20.7%`) into the next substantive CHANGELOG entry. No downstream cascade required.
2. **S2** — No action required today. At next CHANGELOG.md recalibration: update CHANGELOG.md row to ~91,700 / ~22,925; widen envelope from ~65,000 to ~67,000; cascade to `ops/audit.md`, `user-guide.md` (cost table and `!! audit` description).

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
