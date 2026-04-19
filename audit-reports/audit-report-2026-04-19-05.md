# Blueprint Audit Report — 2026-04-19 (#15)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.12 (per CHANGELOG.md; no later entry found)  
**Prior audits reviewed:** #11–#14 (`audit-report-2026-04-19-01.md` through `audit-report-2026-04-19-04.md`) — read before this audit pass per user instruction  
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
- `troubleshooting.md` (21,536 chars)
- `CHANGELOG.md` (62,089 chars)
- `LICENSE` (1,067 chars)

**Template**

- `template/CLAUDE.md` (20,641 chars)
- `template/scheduled-tasks/refresh-hot.md` (3,966 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,852 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/query.md` (2,586 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars)
- `template/scheduled-tasks/ops/audit.md` (6,572 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,796 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (4,185 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,533 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,746 chars)

**Not in audit scope:** `blueprint/` sub-directory internals (working-folder-level installed files), `ROADMAP.md` (planning doc, no logic content).

### 1.2 Verification that audit #14 findings are clean

Audit #14 was a fix-verification pass confirming all three audit #13 findings (W1–W3) were applied in v2.0.12. Direct re-verification of each:

| Fix | Claim | Re-verified |
|---|---|---|
| W1 | `SKILL.md` "Offered During Setup" → "Step 4.5" | ✓ confirmed |
| W2 | `query-layer.md` uses `find`-based path resolution, not glob patterns | ✓ confirmed |
| W2 cascade | `ops/conventions.md` Query Layer Hook Contract prohibits glob patterns | ✓ confirmed |
| W3 | `ingest-hook.md` exception handler points to `!! install sqlite-query` | ✓ confirmed |
| W3 cascade | `SKILL.md §Fallback Behaviour` documents DB desync recovery | ✓ confirmed |
| query-layer.md | Recalibrated to ~3,200 / ~800 | ✓ confirmed (2,533 chars; ~3,200 / 26.4% headroom) |

No regressions from #14. Schema v2.0.12 findings baseline is clean.

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Current convention per `token-reference.md`: **~125% of measured actual at calibration**, rounded to nearest 100.

| File | Measured (`wc -c`) | Doc. Chars | Headroom | Flag |
|---|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 22.2% | ok |
| `setup-guide.md` | 10,564 | ~12,800 | 17.5% | ok |
| `user-guide.md` | 14,219 | ~17,100 | 16.9% | ok |
| `troubleshooting.md` | 21,536 | ~27,300 | 21.1% | ok |
| `CHANGELOG.md` | 62,089 | ~69,100 | 10.1% | ok |
| `LICENSE` | 1,067 | ~1,400 | 23.8% | ok |
| `template/CLAUDE.md` | 20,641 | ~25,000 | 17.4% | ok |
| `refresh-hot.md` | 3,966 | ~5,100 | 22.2% | ok |
| `ops/ingest.md` | 15,852 | ~18,600 | 14.8% | ok |
| `ops/lint.md` | 2,507 | ~2,900 | 13.6% | ok |
| `ops/query.md` | 2,586 | ~3,300 | 21.6% | ok |
| `ops/update.md` | 1,881 | ~2,400 | 21.6% | ok |
| `ops/conventions.md` | 6,741 | ~8,000 | 15.7% | ok |
| `ops/audit.md` | 6,572 | ~8,200 | 19.9% | ok |
| `ops/token-reference.md` | 6,796 | ~8,300 | 18.1% | ok |
| `skills/sqlite-query/SKILL.md` | 4,185 | ~4,700 | 11.0% | ok |
| `skills/sqlite-query/query-layer.md` | 2,533 | ~3,200 | 20.8% | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,746 | ~3,300 | 16.8% | ok |

No hard triggers (measured ≥ documented). No soft triggers (headroom < 3% of measured actual). No recalibration required.

### 1.4 Envelope check (Recalibration Rule Step 5)

Documented rows sum from `token-reference.md`:

| Group | Tokens |
|---|---:|
| Blueprint-doc (README 1,500 + setup-guide 3,200 + user-guide 4,280 + troubleshooting 6,830 + CHANGELOG 17,275 + LICENSE 350) | 33,435 |
| Template-side (CLAUDE 6,250 + refresh-hot 1,280 + ingest 4,650 + lint 730 + query 830 + update 600 + conventions 2,000 + audit 2,050 + token-reference 2,080) | 20,470 |
| Skill rows (SKILL.md 1,180 + query-layer 800 + ingest-hook 830) | 2,810 |
| **Total** | **56,715** |

Cushion: 58,000 − 56,715 = **1,285 tokens (2.2%)**. Above the 2% floor (1,160 tokens). No envelope widening required. Cushion is tighter than audit #12 (1,455 tokens / 2.5%) due to the query-layer.md recalibration in v2.0.12 — monitor at next calibration.

### 1.5 Cross-reference sanity checks

- `template/CLAUDE.md:9` cold-start self-cost `~6,250` = token-reference CLAUDE.md row. ✓
- `template/CLAUDE.md:17` cold-start total `~6,330` = 6,250 + 80 (hot.md). ✓
- `template/CLAUDE.md:17` `!! ready` total `~7,280` = 6,330 + 950 (memory.md full). ✓
- `user-guide.md:9` CLAUDE.md cost `~6,250` — matches token-reference row. ✓
- `user-guide.md:14` cold-start prose `~6,330` — consistent with CLAUDE.md line 17. ✓
- `user-guide.md:201` audit all `~30,000–58,000` — matches `ops/audit.md:72`. ✓
- `user-guide.md` realistic `!! wrap` `~3,000` / `!! ready` `~3,300` — derivable from current token-reference component values (1,280 + 250 + 625 + 100 + 750 mid-write ≈ 3,005 ≈ ~3,000; 1,280 + 250 + 625 + 100 + 950 + 50 = 3,255 ≈ ~3,300). ✓
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:59,69–72`, `README.md:73`, and `user-guide.md:175`. ✓
- Blueprint Sync Rule 12-row matrix — intact. ✓
- Versioning split (major.minor in footer + hot.md; patches in CHANGELOG only) — documented and consistent. ✓
- `ops/audit.md:72` envelope `~30,000–58,000` — matches token-reference.md and all user-guide.md citations. ✓
- Ingest atomic ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 write source page. ✓
- Hash canonicalization 6-step pipeline intact in `ops/ingest.md §Hash Canonicalization`. ✓
- Blueprint-authoring mode guard present in `template/CLAUDE.md`, `ops/audit.md:44`, and `!! ready` step 5 footnote. ✓
- `SKILL.md` install step 4 file copy targets (`scheduled-tasks/query-layer.md`, `scheduled-tasks/ingest-hook.md`) match `CLAUDE.md` directory structure. ✓
- `SKILL.md` uninstall targets match install targets. ✓
- `SKILL.md` "Offered During Setup" — "Step 4.5" — matches `setup-guide.md` heading "## Step 4.5 — Offer SQLite Query Skill". ✓
- `query-layer.md` returns resolved paths via `subprocess.run(["find", ...])` — satisfies Query Layer Hook Contract. ✓
- `ingest-hook.md` exception handler points to correct repair path (`!! install sqlite-query`). ✓
- **`ingest-hook.md` Notes section second bullet says "`!! lint` detects and repairs drift."** ⚠️ (see W1)
- **`ops/ingest.md` B5 per-file step list is `[main-steps 5, 6, 7, 8, 9, 10, 11]` — step 11.5 absent.** ⚠️ (see W2)

---

## 2. Findings

### CRITICAL

None.

### WARNING

**W1 — `blueprint/skills/sqlite-query/ingest-hook.md` Notes section still directs users to `!! lint` for DB desync repair; contradicts the corrected exception handler and `SKILL.md §Fallback Behaviour`.**

*Evidence.*

`ingest-hook.md` Notes section, second bullet:
> `Errors are non-fatal: the ingest op continues, but wiki.db may drift from the markdown files. !! lint detects and repairs drift.`

`ingest-hook.md` exception handler (last line, corrected in v2.0.12 W3):
> `"…wiki.db may be out of sync. To repair: say '!! install sqlite-query' and choose yes to the backfill offer, or '!! uninstall sqlite-query' to revert to grep."`

`SKILL.md §Fallback Behaviour` (added in v2.0.12 W3):
> `"To repair: say !! install sqlite-query — the install flow detects the existing DB, skips creation, and re-offers the backfill step. Choose yes to re-sync all pages. Alternatively, say !! uninstall sqlite-query to remove the skill and revert to the built-in grep layer."`

`ops/lint.md` Steps 3.i–ix: all check wiki-page quality (broken links, orphans, stale claims, contradictions, etc.) — no step reads `wiki.db`, compares it against markdown files, or reconciles desync.

*Logical failure.* The W3 fix in v2.0.12 correctly updated the exception handler (pointing to the backfill repair path) and added the `SKILL.md §Fallback Behaviour` recovery note. The Notes section's second bullet was not touched in the same pass. An operator reading the Notes section — rather than the exception handler — would follow the `!! lint` direction, see a clean lint report (assuming the wiki pages themselves are fine), and conclude the desync is resolved while `wiki.db` remains out of sync. Subsequent queries via the SQLite layer would then silently degrade to grep fallback on every query until the DB is properly backfilled. This is the same partial-cascade class as audit #8 W1 (`user-guide.md:216–217` missed by the v2.0.7 propagation) and the v2.0.12 W3 fix itself only half-landed.

*Recommended fix.* Update `ingest-hook.md` Notes section second bullet from:
```
- Errors are non-fatal: the ingest op continues, but wiki.db may drift from the markdown files. `!! lint` detects and repairs drift.
```
to:
```
- Errors are non-fatal: the ingest op continues, but wiki.db may drift from the markdown files. To repair: say `!! install sqlite-query` and choose yes to the backfill offer, or `!! uninstall sqlite-query` to revert to grep.
```
This aligns the Notes section with the exception handler and `SKILL.md §Fallback Behaviour`, making all three representations of desync recovery consistent.

---

**W2 — `ops/ingest.md` B5 batch-preamble step enumeration omits step 11.5; a strict agent following the list would skip the ingest hook on every `!! ingest all` run.**

*Evidence.*

`ops/ingest.md` B5:
> Process each file in sequence using **`[main-steps 5, 6, 7, 8, 9, 10, 11]`** per file — `[main-step 2]` was already executed at batch level in B3.5, so do NOT re-read sources here; also skip `[main-steps 1, 3, 4, 12, 13]`, which are handled at batch level

`ops/ingest.md` Step 11.5:
> **Run ingest hook if installed.** If `scheduled-tasks/ingest-hook.md` exists, read it and execute it — passing the current page's `slug`, `title`, `type`, `summary`, `tags`, `created`, `updated`, and `related` from working memory. **Run once per page touched in this ingest** (source page + every concept/entity page created or updated in Steps 7–9). Hook errors are non-fatal — log the warning and continue.

`ops/update.md` Step 5.5: explicitly and correctly lists "If `scheduled-tasks/ingest-hook.md` exists, read it and execute it for each page touched" — there is no equivalent issue in the update op.

*Logical failure.* Step 11.5 was introduced in v2.0.11 as part of the sqlite-query skill addition. The main Steps sequence was correctly updated (11.5 inserted between 11 and 12), but the B5 batch-preamble's explicit per-file step enumeration was not updated to include 11.5. The enumeration explicitly names steps to use (5, 6, 7, 8, 9, 10, 11) and explicitly names steps to skip (1, 3, 4, 12, 13). Step 11.5 appears in neither list. A strict agent following the enumeration — which explicitly partitions "per-file steps" from "skip these" — has no unambiguous signal to run 11.5 during batch ingest.

The consequence is a silent wiki.db desync on every `!! ingest all` run when the sqlite-query skill is installed: pages are created/updated in markdown (Steps 7–9), but the ingest hook that writes them to `wiki.db` is never called. The DB and the markdown files diverge silently from the first batch ingest onward. No error is raised; the fallback to grep absorbs the desync at query time, so the failure is invisible.

The CHANGELOG v2.0.11 entry documents that "ops/ingest.md gains Step 11.5 (run ingest-hook if installed)" but does not mention updating B5 — the cascade was incomplete.

*Recommended fix.* Update B5's step enumeration from:
```
[main-steps 5, 6, 7, 8, 9, 10, 11]
```
to:
```
[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]
```
No skip-list change needed (11.5 is already not in the skip list — it's simply absent from both lists). One-phrase change; no logic impact on the main Steps sequence.

---

### STYLE

None. All files within documented headroom; no recalibration overruns; envelope cushion 2.2% above the 2% floor.

---

## 3. Non-findings (considered and dismissed)

- **Cold-start total `~6,330`** — 6,250 (CLAUDE.md) + 80 (hot.md). ✓
- **`!! ready` total `~7,280`** — 6,330 + 950 (memory.md full). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — derivable from current token-reference component values. ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
- **Ingest atomic ordering** — Step 5 pre-compute → Step 6 mv → Step 7 page write. ✓
- **Hash canonicalization 6-step pipeline** — intact. ✓
- **`Pages: N` derived** — refresh-hot.md counts `^- [[` entries; not a stored counter. ✓
- **Blueprint-authoring mode guard** — present in CLAUDE.md, audit.md, `!! ready` step 5. ✓
- **Blueprint Sync Rule 12-row matrix** — intact; no new untriggered changes detected. ✓
- **`SKILL.md` install/uninstall symmetry** — file targets match; DB-keep option on uninstall correctly defaults to no. ✓
- **sqlite-query DB schema** — `pages` table, `relations` table, four indexes; `type` CHECK constraint; upsert pattern and bidirectional-relation INSERT OR IGNORE all correct. ✓
- **`query-layer.md` `find`-based path resolution** — W2 fix from audit #13 verified in place and complete. ✓
- **`ingest-hook.md` exception handler** — W3 fix from audit #13 verified in place and correct. ✓
- **`SKILL.md §Fallback Behaviour`** — W3 cascade from audit #13 verified in place and correct. ✓
- **CHANGELOG.md v2.0.12 envelope arithmetic** — total 56,715, cushion 1,285 tokens (2.2%) verified correct. ✓
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form only; 3-argument GNU-awk form correctly avoided. ✓
- **`.gitignore` scope** — correctly scopes to inside `blueprint/`; setup-guide.md note accurately explains that `wiki/.obsidian/` is outside its reach. ✓
- **`ops/audit.md` scope parenthetical** — "currently `refresh-hot.md`" remains accurate after `changelog-monitor.md` removal (v2.0.11). ✓
- **Envelope cushion narrative.** The 2.2% cushion (1,285 tokens) is above the 2% floor (1,160 tokens). The CHANGELOG.md row accounts for the most cushion consumption risk — currently at 10.1% headroom against its own documented cap, so ordinary version-bump growth will not immediately breach the row-level trigger. No action required now; monitor at next calibration.
- **`ROADMAP.md`** — planning doc; not in audit scope.
- **`LICENSE`** — MIT; no issues.

---

## 4. Questions for Clarification

**Q1 — Does step 11.5 also need to appear explicitly in the `!! ingest all` B5 skip-list as "not batch-level" (i.e. "skip [main-steps 1, 3, 4, 12, 13]" → "skip [main-steps 1, 3, 4, 12, 13]; step 11.5 runs per-file")?**

B5's current skip-list enumerates only the steps handled at batch level (B3, B4, B6). Step 11.5 is per-page/per-file and should run inside B5's loop, not at batch level. The recommended W2 fix (add 11.5 to the per-file list) is sufficient — no skip-list change is needed. But an explicit explanatory note ("step 11.5 runs per-page inside the per-file loop, like steps 7–9") could pre-empt future confusion if more hook steps are added. Depends on whether clarity here is worth the added prose.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#14 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in index.md), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in template/CLAUDE.md and ops/audit.md step 5. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and hot.md Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md:72` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < 3% of measured actual), envelope cushion floor (cushion < 2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. ✓
11. sqlite-query skill follows Query Layer Hook Contract (no glob patterns, `find`-based resolution) and Ingest Hook Contract (non-fatal errors, wiki.db sync) in `ops/conventions.md` — with the caveat noted in W2 (hook is silently skipped during `!! ingest all` due to B5 enumeration gap). ✗ partially

---

## 6. Verdict

**The v2.0.12 blueprint has two WARNING-class findings and no CRITICAL or STYLE issues.**

The ingest pipeline, approval flow, hash canonicalization, Blueprint Sync Rule, and Recalibration Rule are all structurally intact. All prior findings from audits #11–#14 are clean. Headroom across all 18 tracked files is healthy; no recalibration is due.

Both warnings are confined to the sqlite-query skill bundle, which was added in v2.0.11 and last audited in #13/#14. They are related: both stem from incomplete propagation of the v2.0.11 skill addition into the existing ingest op documentation. W1 is a partial cascade miss from the v2.0.12 W3 fix (the exception handler was corrected, the Notes section was not). W2 is a carry-over from v2.0.11 itself (step 11.5 was added to the main Steps sequence but the `!! ingest all` B5 enumeration was not updated).

W2 is the higher-severity finding: it causes the sqlite-query ingest hook to be silently skipped on every `!! ingest all` run, causing wiki.db to drift from the markdown files without any error or warning — the fallback to grep absorbs the desync at query time, making the failure invisible. W1 would mislead an operator trying to manually repair a drift condition that W2 silently caused.

**Priority order for follow-up:**

1. **W2** — Update `ops/ingest.md` B5 per-file step list from `[main-steps 5, 6, 7, 8, 9, 10, 11]` to `[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]`. This ensures the ingest hook runs during batch ingests.
2. **W1** — Update `ingest-hook.md` Notes section second bullet to point at `!! install sqlite-query` (backfill) instead of `!! lint`. Aligns all three representations of desync recovery.

Both fixes are in `blueprint/skills/sqlite-query/` files and `blueprint/template/scheduled-tasks/ops/ingest.md`. A single CHANGELOG patch entry (v2.0.13) covers both. Blueprint Sync Rule "New skill bundle added" cascade does not re-trigger (no new files); "Operation step change" row applies for the B5 edit (`blueprint/user-guide.md` and `blueprint/template/CLAUDE.md` do not quote B5 directly, so no further cascade is required beyond the ops file itself and the CHANGELOG entry).

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
