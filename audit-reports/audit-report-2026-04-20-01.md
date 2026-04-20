# Blueprint Audit Report — 2026-04-20 (#31)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.1 (per `template/CLAUDE.md` footer — unchanged since audit #30)  
**Prior audit reviewed:** #30 (`audit-report-2026-04-19-20.md`) — read in full before this pass per user instruction  
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)  
**Mode:** Blueprint-authoring (wiki/ absent at working-folder root; log append and hot.md refresh skipped per Blueprint-authoring Mode rule)  
**Note:** Audit reports directory (`audit-reports/`) excluded from scope per standing user instruction.

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**

- `README.md` (4,671 chars)
- `setup-guide.md` (11,035 chars)
- `user-guide.md` (14,617 chars)
- `troubleshooting.md` (27,345 chars)
- `LICENSE` (1,067 chars)

**Template**

- `template/CLAUDE.md` (24,588 chars)
- `template/scheduled-tasks/refresh-hot.md` (4,542 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,877 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars)
- `template/scheduled-tasks/ops/audit.md` (5,908 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,711 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (5,602 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,810 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (3,024 chars)

**Not in audit scope:** `ROADMAP.md` (planning doc, no logic content). `CHANGELOG.md` formally out of scope per v2.0.21. `audit-reports/` excluded per standing user instruction.

---

### 1.2 Files changed since audit #30

| File | Audit #30 bytes | This audit bytes | Delta | Probable cause |
|---|---:|---:|---:|---|
| `setup-guide.md` | 10,497 | 11,035 | +538 | Step 3 rewrite (Read→substitute→Write replacing cp+Edit); `.obsidian/` note added to Step 5 |
| `user-guide.md` | 14,219 | 14,617 | +398 | Session memory tip bullet and other minor additions |
| `troubleshooting.md` | 23,953 | 27,345 | +3,392 | Two new sections: "Edit tool rejects files copied into place via Bash cp" (v2.1.5 fix) and "SQLite disk I/O error on FUSE-mounted library" (v2.1.7 fix) |
| `template/CLAUDE.md` | 24,046 | 24,588 | +542 | Blueprint-authoring mode startup-behavior detail added; `!! ready` step 5 blueprint-authoring mode guard added |
| `skills/sqlite-query/SKILL.md` | 5,518 | 5,602 | +84 | FUSE section expanded; DB Desync Recovery sub-section added |
| `skills/sqlite-query/query-layer.md` | 2,697 | 2,810 | +113 | `?nolock=1` + `PRAGMA journal_mode=MEMORY` + `PRAGMA synchronous=OFF` applied; comment confirming FUSE-safe path |
| `skills/sqlite-query/ingest-hook.md` | 2,917 | 3,024 | +107 | Same FUSE-safe pattern applied consistently |

All other tracked files byte-identical to audit #30.

---

### 1.3 Audit #30 findings resolution status

Audit #30 was a clean pass — 0 findings. No resolution tracking required this cycle.

---

### 1.4 Per-file headroom check (Recalibration Rule Steps 1–2)

Convention: ~125% of measured actual at calibration, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom | 10% Soft Floor | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 1,329 | 467 | ok |
| `setup-guide.md` | 11,035 | ~13,200 | 2,165 | 1,103 | ok |
| `user-guide.md` | 14,617 | ~17,800 | 3,183 | 1,462 | ok |
| `troubleshooting.md` | 27,345 | ~28,300 | 955 | 2,735 | **⚠ SOFT TRIGGER** |
| `LICENSE` | 1,067 | ~1,400 | 333 | 107 | ok |
| `template/CLAUDE.md` | 24,588 | ~30,100 | 5,512 | 2,459 | ok |
| `refresh-hot.md` | 4,542 | ~5,100 | 558 | 454 | ok (marginal — watch) |
| `ops/ingest.md` | 15,877 | ~19,800 | 3,923 | 1,588 | ok |
| `ops/lint.md` | 2,507 | ~3,100 | 593 | 251 | ok |
| `ops/update.md` | 1,881 | ~2,400 | 519 | 188 | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 1,659 | 674 | ok |
| `ops/audit.md` | 5,908 | ~8,200 | 2,292 | 591 | ok |
| `ops/token-reference.md` | 6,711 | ~8,500 | 1,789 | 671 | ok |
| `skills/SKILL.md` | 5,602 | ~6,900 | 1,298 | 560 | ok |
| `skills/query-layer.md` | 2,810 | ~3,200 | 390 | 281 | ok (drift noted) |
| `skills/ingest-hook.md` | 3,024 | ~3,500 | 476 | 302 | ok |

**`troubleshooting.md` soft trigger fires.** Headroom 955 < soft floor 2,735. Hard trigger: 27,345 < 28,300 — does not fire yet, but the file is within 955 chars of the ceiling.

**`query-layer.md` calibration target drift (continued from audit #30).** The documented ~3,200 was set at 125% of a prior measured value of ~2,533. At 2,810, the current recalibration target would be 2,810 × 125% = 3,513 → ~3,600. No trigger fires yet (headroom 390 > soft floor 281), but the table is increasingly misaligned with the current actual. A content edit of ~110 chars would fire the soft trigger. Recalibration is warranted as part of the W1 recalibration cascade.

---

### 1.5 Envelope check (Recalibration Rule Step 5)

**Current documented audit-scope sum** (blueprint-doc + template-side rows in `token-reference.md`):

| Group | Tokens (documented) |
|---|---:|
| Template — CLAUDE.md | 7,530 |
| Template — ops | 4,950 + 780 + 600 + 2,100 + 2,050 + 2,120 = 12,600 |
| Template — refresh-hot | 1,280 |
| Blueprint docs | 1,500 + 3,300 + 4,450 + 7,080 + 350 = 16,680 |
| Skills | 1,720 + 800 + 880 = 3,400 |
| **Audit-scope total** | **41,490** |

Full-table sum (audit-scope + wiki-side rows): 41,490 + 80 + 950 + 250 + 625 = **43,395 tokens**

Against current ~45,000 ceiling: cushion = 1,605 tokens (3.6% > 2% floor). Documented table: **still inside envelope**.

**However — post-recalibration envelope projection:**

Recalibrating all seven grown files to 125% of current actuals yields these new Chars / Tokens values:

| File | Current doc Chars | New actual | New Chars (×125%) | Token delta |
|---|---:|---:|---:|---:|
| `setup-guide.md` | ~13,200 | 11,035 | ~13,800 | +150 |
| `user-guide.md` | ~17,800 | 14,617 | ~18,300 | +125 |
| `troubleshooting.md` | ~28,300 | 27,345 | ~34,200 | +1,475 |
| `template/CLAUDE.md` | ~30,100 | 24,588 | ~30,800 | +175 |
| `SKILL.md` | ~6,900 | 5,602 | ~7,000 | +25 |
| `query-layer.md` | ~3,200 | 2,810 | ~3,600 | +100 |
| `ingest-hook.md` | ~3,500 | 3,024 | ~3,800 | +75 |
| **Total delta** | | | | **+2,125** |

Post-recalibration audit-scope sum: 41,490 + 2,125 = **43,615 tokens**  
Post-recalibration full-table sum: 43,615 + 80 + 950 + 250 + 625 = **45,520 tokens**

**45,520 > 45,000 — envelope ceiling breached.** Additionally, cushion = 45,000 − 45,520 = −520 (negative). The 2% cushion floor (900 tokens on 45,000) is violated before any breach even occurs.

Required envelope: 45,520 + ~1,500 cushion = 47,020 → **~30,000–47,000**.  
Cushion check: 47,000 − 45,520 = 1,480 tokens (3.1% of 47,000 > 2% floor ✓).

Cascade locations for envelope update: `ops/audit.md:71`, `user-guide.md` (§ "Blueprint Audit" command reference and cost table row), plus CHANGELOG entry for the patch. `README.md` and `setup-guide.md` do not quote the envelope — no change needed there.

---

### 1.6 Cross-reference sanity checks

| Check | Result |
|---|:---:|
| `template/CLAUDE.md:9` CLAUDE.md self-cost `~7,530 tokens` — matches token-reference row (~30,100 ÷ 4 = ~7,525 → ~7,530) | ✓ |
| `template/CLAUDE.md:19` cold-start total `~7,610 tokens` — 7,530 + 80 | ✓ |
| `template/CLAUDE.md:19` `!! ready` total `~8,560 tokens` — 7,530 + 80 + 950 | ✓ |
| `user-guide.md:9` CLAUDE.md startup cost `~7,530 tokens` | ✓ |
| `user-guide.md:14` cold-start total `~7,610` and `!! ready` total `~8,560` | ✓ |
| `user-guide.md` cost table `Cold start: ~7,610` and `Cold start with !! ready: ~8,560` | ✓ |
| `user-guide.md:94` audit-all `~30,000–45,000` | ✓ (stale after recalibration — see W2) |
| `user-guide.md:204` audit-all cost table `~30,000–45,000` | ✓ (stale after recalibration — see W2) |
| `ops/audit.md:71` envelope `~30,000–45,000` | ✓ (stale after recalibration — see W2) |
| `ops/token-reference.md` Step 5 `(currently ~30,000–45,000)` | ✓ (stale after recalibration — see W2) |
| `ops/token-reference.md` floor note `(~900 tokens on a 45,000-token envelope)` — 45,000 × 2% = 900 | ✓ (must update if envelope widened) |
| `README.md:73` cold-start `~7,610 tokens` | ✓ |
| Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md`, `README.md`, and `user-guide.md` | ✓ |
| `setup-guide.md` Step 2 copy table — 7 rows, no CLAUDE.md; all 7 source files exist in template | ✓ |
| `setup-guide.md` Step 3 — uses Read → substitute → Write for CLAUDE.md (no cp); consistent with troubleshooting "Edit tool rejects files" fix | ✓ |
| `setup-guide.md` Step 7 ops file count — "All 6 ops files" matches actual 6 template ops files | ✓ |
| `template/CLAUDE.md` Directory Structure ops listing — 6 files, no query.md | ✓ |
| `SKILL.md` Step 3 Python — uses `?nolock=1` + `PRAGMA journal_mode=MEMORY` + `PRAGMA synchronous=OFF`; consistent with troubleshooting "SQLite disk I/O" fix | ✓ |
| `query-layer.md` — uses same `?nolock=1` + MEMORY + OFF pattern; DB at `WORKDIR / "wiki" / "wiki.db"` | ✓ |
| `ingest-hook.md` — uses same `?nolock=1` + MEMORY + OFF pattern; DB at `WORKDIR / "wiki" / "wiki.db"` | ✓ |
| `troubleshooting.md` "SQLite disk I/O" fix claims DB at `wiki/wiki.db` — matches all three skill files | ✓ |
| `query-layer.md` line 3 — references "Query Routing Rule embedded in `CLAUDE.md`" (not retired `ops/query.md`) | ✓ |
| Blueprint Sync Rule 12-row matrix — intact; Non-cascade exception correctly appended as `>` note | ✓ |
| `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading | ✓ |
| `SKILL.md` DB Desync Recovery — "detect existing DB, skips creation" behavior delivered by `CREATE TABLE IF NOT EXISTS` in Step 3 Python (idempotent by design) | ✓ |
| Blueprint-authoring mode guard — present in `template/CLAUDE.md` and `audit.md:43` | ✓ |
| Hook contracts (query-layer and ingest-hook) — consistent across conventions.md, ingest.md, update.md, query-layer.md, ingest-hook.md | ✓ |
| `CLAUDE.md` `!! ready` step 5 directional reference: "Blueprint-authoring Mode **below**" — Blueprint-authoring Mode section is at §8 (line 165), above Session Memory Commands at §12 (line 232) | **✗ — see S1** |
| `refresh-hot.md` awk pipeline uses 1-arg `match()` form only | ✓ |
| Remaining `query.md` references — nil (established clean in audit #30) | ✓ |
| Schema version: 2.1 in CLAUDE.md footer — patch-level additions (v2.1.5, v2.1.7) correctly leave footer unchanged per Versioning Split rule | ✓ |

---

## 2. Findings

### W1 — `troubleshooting.md` soft recalibration trigger

**Evidence:** `wc -c` measured 27,345 chars. Documented Chars: ~28,300. Headroom: 955. 10% soft floor: 2,735 (10% of 27,345). 955 < 2,735 → soft trigger fires.

**Cause:** Two new troubleshooting sections added since calibration (2026-04-19):
1. "Edit tool rejects files copied into place via Bash cp" (v2.1.5 fix, ~1,300 chars)
2. "SQLite disk I/O error on FUSE-mounted library (Cowork)" (v2.1.7 fix, ~2,100 chars)

**Fix:** Per Recalibration Rule, recalibrate all files (not just the trigger file) using `wc -c` actuals. Seven files need updated rows in `token-reference.md` (see §1.5 table above for new Chars / Token values). The calibration date header must also advance to 2026-04-20.

---

### W2 — Post-recalibration envelope ceiling breach

**Evidence:** After applying the W1 recalibration cascade, the full-table token sum rises from 43,395 to ~45,520 — 520 tokens above the current 45,000 ceiling. The 2% cushion floor (900 tokens on 45,000) is violated even before reaching the ceiling. Neither condition is currently violated by the stale documented table, but the recalibration mandated by W1 cannot be completed without also widening the envelope.

**Fix:** Widen the envelope from `~30,000–45,000` to `~30,000–47,000`. Cascade to:
- `ops/audit.md:71` — update envelope figure and the floor-note token count
- `user-guide.md` § "Blueprint Audit" command reference — update `!! audit all` parenthetical
- `user-guide.md` cost table — update "Audit all (full blueprint)" row
- `ops/token-reference.md` Step 5 — update the `(currently ~30,000–45,000)` parenthetical and the floor note (`~900 tokens on a 45,000-token envelope` → `~940 tokens on a 47,000-token envelope`)
- CHANGELOG.md — new patch-level section documenting the recalibration and envelope widening

`README.md` and `setup-guide.md` do not quote the envelope — no changes needed there.

---

### S1 — `CLAUDE.md` `!! ready` step 5: directional reference error

**Evidence:** `!! ready` step 5 (Session Memory Commands section, line ~299):

> "…skip the drafts surface transparently **(same guard as Blueprint-authoring Mode below**; a single `[ -d drafts ]` check…)"

Blueprint-authoring Mode section begins at line 165. Session Memory Commands begins at line 232. The Blueprint-authoring Mode section is **above** Session Memory Commands in the document, not below.

**Fix:** Replace "below" with "above" in that parenthetical:

> "…(same guard as Blueprint-authoring Mode **above**; a single `[ -d drafts ]` check…)"

**Scope:** Single-file edit to `template/CLAUDE.md` only. This is an agent-internal document reference; no user-facing behavioral change, no Blueprint Sync cascade required. Acceptable as a non-cascade under the existing exception with a patch-level CHANGELOG note.

---

## 3. Non-findings (considered and dismissed)

- **`refresh-hot.md` headroom.** 4,542 chars; headroom 558 chars; soft floor 454 chars. Headroom 558 > 454 — no trigger. This file remains the closest (after troubleshooting.md) to a soft trigger. Flagged again for watching on the next edit pass.

- **`query-layer.md` calibration drift (continued).** Measured 2,810; documented ~3,200. Calibration target has drifted to ~3,600. Soft trigger does not fire (headroom 390 > soft floor 281). No independent action required — the W1 recalibration cascade covers it.

- **CLAUDE.md blueprint-authoring mode startup additions.** New paragraphs added to the Blueprint-authoring Mode section and to `!! ready` step 5 describe startup and draft-surface behavior in blueprint-authoring mode. These are agent-internal additions with no user-facing behavioral change for end-users operating a live wiki. Consistent with the non-cascade exception. Cascade to README.md, setup-guide.md, and user-guide.md is not required. CHANGELOG entry expected but out of scope for this audit.

- **setup-guide.md Step 5 `.obsidian/` note.** New explanatory paragraph about `.gitignore` scope and vault-setting bundling. Content matches the existing troubleshooting.md "Edited blueprint/.gitignore and nothing changed" entry. No contradiction found. ✓

- **SKILL.md `IF NOT EXISTS` as desync-detection.** The "Fallback Behaviour" section states the reinstall flow "detects the existing DB" — the detection mechanism is the `CREATE TABLE IF NOT EXISTS` in Step 3, which is idempotent and leaves existing data intact while effectively no-oping creation. This is a reasonable implementation pattern; the wording is slightly imprecise but not misleading.

- **Patch version references in troubleshooting.md.** Two new entries reference specific patch versions (v2.1.5, v2.1.7). These are historical records for users troubleshooting legacy schema setups. The schema footer stays at "2.1" per the Versioning Split rule. No inconsistency.

---

## 4. Architectural Invariants Verified

All 11 invariants re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:43`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.1`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~10% of measured actual), envelope cushion floor (cushion < ~2% of upper bound). Soft trigger currently active on troubleshooting.md (see W1). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. Non-cascade exception documented as opt-out path. ✓
11. sqlite-query skill follows Query Layer Hook Contract and Ingest Hook Contract; FUSE-safe pattern (`?nolock=1` + `journal_mode=MEMORY` + `synchronous=OFF`) applied consistently across SKILL.md, query-layer.md, and ingest-hook.md. ✓

---

## 5. Verdict

**The v2.1 blueprint has 0 CRITICAL, 2 WARNING, and 1 STYLE findings.**

The two new troubleshooting sections (Edit-tool cp-rejection and SQLite FUSE locking) are well-written and internally consistent with the corresponding schema fixes in setup-guide.md and the skill bundle. The blueprint-authoring-mode startup additions to CLAUDE.md are coherent. All cross-references checked clean except the directional error in S1.

The primary action item is the recalibration cascade (W1 → W2): troubleshooting.md's soft trigger requires a full-table recalibration, and that recalibration pushes the full-table sum past the current 45,000 ceiling, requiring the envelope to widen to ~47,000. Both findings resolve in a single pass: update the seven token-reference.md rows, advance the calibration date, widen the envelope to ~30,000–47,000, cascade the new figure to the three downstream locations (audit.md:71, user-guide.md × 2, token-reference.md Step 5 parenthetical), and add a CHANGELOG entry. S1 is a one-line fix in template/CLAUDE.md.

Read-only audit complete. No fixes applied.
