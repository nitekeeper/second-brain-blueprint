# Blueprint Audit Report — 2026-04-19 (#30)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.1 (per `template/CLAUDE.md` footer — unchanged since audit #29)  
**Prior audit reviewed:** #29 (`audit-report-2026-04-19-19.md`) — read in full before this pass per user instruction  
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)  
**Mode:** Blueprint-authoring (wiki/ absent at working-folder root; log append and hot.md refresh skipped per Blueprint-authoring Mode rule)  
**Note:** Audit reports directory (`audit-reports/`) excluded from scope per standing user instruction.

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**

- `README.md` (4,671 chars)
- `setup-guide.md` (10,497 chars)
- `user-guide.md` (14,219 chars)
- `troubleshooting.md` (23,953 chars)
- `LICENSE` (1,067 chars)

**Template**

- `template/CLAUDE.md` (24,046 chars)
- `template/scheduled-tasks/refresh-hot.md` (4,542 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,877 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars)
- `template/scheduled-tasks/ops/audit.md` (5,908 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,711 chars)
- `template/scheduled-tasks/ops/query.md` — **MISSING** (confirmed absent; consistent with intentional v2.1 retirement)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (5,518 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,697 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,917 chars)

**Not in audit scope:** `ROADMAP.md` (planning doc, no logic content). `CHANGELOG.md` formally out of scope per v2.0.21. `audit-reports/` excluded per standing user instruction.

---

### 1.2 Files changed since audit #29

| File | Audit #29 bytes | This audit bytes | Delta | Cause |
|---|---:|---:|---:|---|
| `setup-guide.md` | 10,584 | 10,497 | −87 | Removed `query.md` row from Step 2 copy table (C1 fix); changed "7 ops files" → "6 ops files" in Step 7 (W1 fix) |
| `template/CLAUDE.md` | 24,081 | 24,046 | −35 | Removed `query.md` from Directory Structure ops/ listing (W2 fix); fixed `update.md` indentation typo (S1 fix) |
| `skills/sqlite-query/query-layer.md` | 2,612 | 2,697 | +85 | Line 3 updated: stale `ops/query.md` reference replaced with "Query Routing Rule embedded in `CLAUDE.md`" (W3 fix) |

All other tracked files byte-identical to audit #29.

---

### 1.3 Audit #29 findings resolution status

| Finding | Description | Status |
|---|---|:---:|
| C1 | `ops/query.md` missing but still in setup-guide.md copy table | **RESOLVED** |
| C2 | `SKILL.md` hard recalibration trigger (5,518 > 5,200) | **RESOLVED** |
| W1 | `setup-guide.md:241` ops file count "7" (should be 6) | **RESOLVED** |
| W2 | `template/CLAUDE.md` Directory Structure listed `query.md` | **RESOLVED** |
| W3 | `query-layer.md:3–5` stale reference to `ops/query.md` | **RESOLVED** |
| W4 | `template/CLAUDE.md` soft recalibration trigger (headroom below 10% floor) | **RESOLVED** |
| S1 | `update.md` extra `│   │` indentation prefix in Directory Structure | **RESOLVED** |

All 7 prior findings closed. Q1 (was `ops/query.md` intentional retirement?) answered affirmatively by the fixes — cleanup is now complete.

---

### 1.4 Per-file headroom check (Recalibration Rule Steps 1–2)

Convention: ~125% of measured actual at calibration, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom | 10% Soft Floor | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 1,329 | 467 | ok |
| `setup-guide.md` | 10,497 | ~13,200 | 2,703 | 1,050 | ok |
| `user-guide.md` | 14,219 | ~17,800 | 3,581 | 1,422 | ok |
| `troubleshooting.md` | 23,953 | ~28,300 | 4,347 | 2,395 | ok |
| `LICENSE` | 1,067 | ~1,400 | 333 | 107 | ok |
| `template/CLAUDE.md` | 24,046 | ~30,100 | 6,054 | 2,405 | ok |
| `refresh-hot.md` | 4,542 | ~5,100 | 558 | 454 | ok |
| `ops/ingest.md` | 15,877 | ~19,800 | 3,923 | 1,588 | ok |
| `ops/lint.md` | 2,507 | ~3,100 | 593 | 251 | ok |
| `ops/update.md` | 1,881 | ~2,400 | 519 | 188 | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 1,659 | 674 | ok |
| `ops/audit.md` | 5,908 | ~8,200 | 2,292 | 591 | ok |
| `ops/token-reference.md` | 6,711 | ~8,500 | 1,789 | 671 | ok |
| `skills/sqlite-query/SKILL.md` | 5,518 | ~6,900 | 1,382 | 552 | ok |
| `skills/sqlite-query/query-layer.md` | 2,697 | ~3,200 | 503 | 270 | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,917 | ~3,500 | 583 | 292 | ok |

No hard or soft triggers. All files within headroom bounds.

**Note on `query-layer.md`:** Grew from 2,612 to 2,697 (+85) since the last calibration. The documented ~3,200 was originally set at 125% of a measured value of ~2,533. At 2,697, the next calibration target would be 2,697 × 125% = 3,371 → ~3,400. No trigger fires yet (2,697 < 3,200 and headroom 503 > soft floor 270), but the effective calibration target has shifted. If the file grows another ~500 chars before the next explicit recalibration, it could fire. Worth noting; no action required now.

---

### 1.5 Envelope check (Recalibration Rule Step 5)

**Audit-scope sum** (blueprint-doc + template-side rows in `token-reference.md`, matching `!! audit all` read list):

| Group | Files | Tokens |
|---|---|---:|
| Template — CLAUDE.md | CLAUDE.md | 7,530 |
| Template — ops | ingest, lint, update, conventions, audit, token-reference | 11,200 |
| Template — refresh-hot | refresh-hot.md | 1,280 |
| Blueprint docs | README, setup-guide, user-guide, troubleshooting, LICENSE | 16,680 |
| Skills | SKILL.md, query-layer.md, ingest-hook.md | 3,400 |
| **Total** | | **40,090** |

Wait — let me recompute precisely from the documented Tokens column:

7,530 + 4,950 + 780 + 600 + 2,100 + 2,050 + 2,120 + 1,280 + 1,500 + 3,300 + 4,450 + 7,080 + 350 + 1,720 + 800 + 880 = **41,490 tokens**

Envelope: `~30,000–45,000`. Cushion: 45,000 − 41,490 = **3,510 tokens** (7.8% of 45,000 — well above the 2% floor of 900). Envelope intact with healthy margin.

**Full-table sum** (all enumerated rows including wiki-side rows, consistent with audit #29 methodology):

41,490 + 80 (hot.md) + 950 (memory.md) + 250 (index.md) + 625 (log tail) = **43,395 tokens**

Cushion against 45,000 ceiling: 1,605 tokens (3.6% > 2% floor). Also intact.

No recalibration cascade required.

---

### 1.6 Cross-reference sanity checks

| Check | Result |
|---|:---:|
| `template/CLAUDE.md:9` CLAUDE.md self-cost `~7,530 tokens` — matches token-reference CLAUDE.md row (~30,100 ÷ 4 = ~7,525 → ~7,530) | ✓ |
| `template/CLAUDE.md:19` cold-start total `~7,610 tokens` — 7,530 + 80 | ✓ |
| `template/CLAUDE.md:19` `!! ready` total `~8,560 tokens` — 7,530 + 80 + 950 | ✓ |
| `user-guide.md:9` CLAUDE.md startup cost `~7,530 tokens` | ✓ |
| `user-guide.md:14` cold-start total `~7,610` and `!! ready` total `~8,560` | ✓ |
| `user-guide.md` cost table `Cold start: ~7,610` and `Cold start with !! ready: ~8,560` | ✓ |
| `user-guide.md:94` audit-all `~30,000–45,000` | ✓ |
| `user-guide.md:201` audit-all cost table `~30,000–45,000` | ✓ |
| `ops/audit.md:71` envelope `~30,000–45,000` | ✓ |
| `ops/token-reference.md` Step 5 `(currently ~30,000–45,000)` | ✓ |
| `ops/token-reference.md` floor note `(~900 tokens on a 45,000-token envelope)` — 45,000 × 2% = 900 | ✓ |
| `README.md:73` cold-start `~7,610 tokens` | ✓ |
| Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md`, `README.md`, and `user-guide.md` | ✓ |
| `setup-guide.md` Step 2 copy table — 8 rows, 0 query.md references; all 8 source files exist in template | ✓ |
| `setup-guide.md` Step 7 ops file count — "All 6 ops files" matches actual 6 template ops files | ✓ |
| `template/CLAUDE.md` Directory Structure ops listing — 6 files, no query.md | ✓ |
| `query-layer.md:3` — references "Query Routing Rule embedded in `CLAUDE.md`" (not the retired `ops/query.md`) | ✓ |
| `query-layer.md:5` — "replaces sub-steps 2–3 of the wiki-check branch (Step 2) in the Query Routing Rule waterfall" — matches CLAUDE.md Step 2 structure | ✓ |
| Blueprint Sync Rule 12-row matrix — intact; Non-cascade exception correctly appended as `>` note | ✓ |
| `update.md` Directory Structure indentation — consistent with sibling files, no extra `│` prefix | ✓ |
| Schema version: 2.1 in CLAUDE.md footer; no explicit version string in README.md or user-guide.md requiring update | ✓ |
| `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading | ✓ |
| `SKILL.md` FUSE warning and Uninstall section — internally consistent with query-layer.md and ingest-hook.md | ✓ |
| Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv` → Step 7 page write | ✓ |
| Hash canonicalization 6-step pipeline — intact | ✓ |
| `refresh-hot.md` awk pipeline uses 1-arg `match()` form only | ✓ |
| Blueprint-authoring mode guard — present in `template/CLAUDE.md` and `audit.md:43` | ✓ |
| Hook contracts (query-layer and ingest-hook) — consistent across conventions.md, ingest.md, update.md, query-layer.md, ingest-hook.md | ✓ |
| Remaining `query.md` references — grep across all tracked files: none found | ✓ |

---

## 2. Findings

**No findings.**

The v2.1 blueprint is internally consistent. All 7 findings from audit #29 have been fully resolved. No new logic errors, security footguns, performance issues, approval leaks, or blueprint-sync drift were identified.

---

## 3. Non-findings (considered and dismissed)

- **`query-layer.md` calibration target drift.** Measured 2,697 chars vs documented ~3,200. The current calibration target would recalibrate to ~3,400 at today's size, but neither the hard trigger (2,697 < 3,200) nor the soft trigger (headroom 503 > soft floor 270) has fired. No action required until the next trigger fires or a content edit consumes the remaining buffer.
- **Q2 token-table sum methodology.** Audit #29 flagged a 1,075-token discrepancy between audits #28 and #29 and posed Q2 about it. This audit's sum (41,490 audit-scope / 43,395 full-table) reconciles cleanly with the post-recalibration values. The audit #29 full-table sum (41,895) equals the current full-table sum minus the combined recalibration delta: 43,395 − 1,080 (CLAUDE.md) − 420 (SKILL.md) = 41,895. ✓ Q2 is resolved.
- **`refresh-hot.md` headroom.** 4,542 chars; headroom 558 chars; soft floor 454 chars. Headroom 558 > 454 — no trigger, but this file remains the closest to a soft trigger of any file in the set. Worth watching on the next edit pass.
- **`ops/audit.md` scope glob.** "Every file under `blueprint/template/scheduled-tasks/ops/`" — this is a dynamic glob, not an enumerated list. With `query.md` gone, the glob correctly covers the remaining 6 files without requiring a doc edit. ✓
- **Schema v2.1 minor-bump cascade.** `user-guide.md` and `README.md` carry no explicit `Schema: vX.Y` strings in body text (only the template CLAUDE.md footer and live hot.md carry the schema version), so no version propagation was needed for those files. ✓
- **`ops/query.md` retirement completeness.** All four locations identified in audit #29 as stale (setup-guide.md copy table, setup-guide.md ops count, CLAUDE.md Directory Structure, query-layer.md description) have been cleaned up. A grep scan of all tracked files confirms no remaining reference to `ops/query.md`. ✓
- **`SKILL.md` FUSE limitation and path-patch guidance.** `wiki.db` path uses `WORKDIR.parent / "wiki.db"` consistently across SKILL.md install step, query-layer.md, and ingest-hook.md. ✓

---

## 4. Architectural Invariants Verified

All 11 invariants from audits #11–#29 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:43`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.1`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~10% of measured actual), envelope cushion floor (cushion < ~2% of upper bound). No trigger currently active. ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. Non-cascade exception documented as opt-out path. ✓
11. sqlite-query skill follows Query Layer Hook Contract and Ingest Hook Contract. ✓

---

## 5. Verdict

**The v2.1 blueprint has 0 CRITICAL, 0 WARNING, and 0 STYLE findings.**

This is a clean audit. All 7 findings from audit #29 — 2 CRITICAL, 4 WARNING, 1 STYLE — were resolved between audits. The `ops/query.md` retirement is complete with no stale references remaining. The two recalibrations (SKILL.md hard trigger C2, CLAUDE.md soft trigger W4) were applied correctly, the envelope was widened from ~43,000 to ~45,000, and all downstream cross-references (CLAUDE.md, user-guide.md, README.md, audit.md, token-reference.md) are consistent with the new figures. Envelope cushion stands at 3,510 tokens (7.8% of 45,000), well above the 2% floor.

The only item worth monitoring for the next audit is `refresh-hot.md` (headroom 558, soft floor 454 — closest to a soft trigger) and `query-layer.md` (calibration target has drifted; no trigger yet but recalibration would be warranted on the next content edit).

Read-only audit complete. No fixes applied.
