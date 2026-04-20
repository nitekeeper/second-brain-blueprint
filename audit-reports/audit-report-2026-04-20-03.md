# Blueprint Audit Report — 2026-04-20 (#33)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.1 (per `template/CLAUDE.md` footer — unchanged since audit #32)  
**Prior audit reviewed:** #32 (`audit-report-2026-04-20-02.md`) — read in full before this pass per user instruction  
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
- `.gitignore` (65 chars)

**Template**

- `template/CLAUDE.md` (24,564 chars)
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

### 1.2 Files changed since audit #32

Fifteen of sixteen previously-tracked files are **byte-identical** to audit #32. One file changed:

| File | Audit #32 bytes | This audit bytes | Delta | Evidence |
|---|---:|---:|---:|---|
| `template/CLAUDE.md` | 24,588 | 24,564 | −24 | Phantom phrase ", then a compliance line" removed from Response Footer first CRITICAL sentence — audit #32 S1 fix applied |

All other tracked files byte-identical to audit #32.

---

### 1.3 Audit #32 findings resolution status

| Finding | Description | Status |
|---|---|:---:|
| S1 | `CLAUDE.md` Response Footer: phantom "then a compliance line" in first CRITICAL sentence | ✅ **RESOLVED** — phrase removed; confirmed byte delta of −24 chars matches removal of `, then a compliance line` exactly |

Zero open findings carried from audit #32.

**S1 fix verification (detailed).** Audit #32 proposed:

> "Every single response — without exception — must end with the footer block exactly as shown: 5 command-hint lines, then a blank separator, then the 💡 tip line, then the 📋 compliance line (8 physical lines total). Missing any content line is an error."

Current `template/CLAUDE.md` line 305 reads:

> "**CRITICAL: Every single response — without exception — must end with the footer block exactly as shown: 5 command-hint lines, then a blank separator, then the 💡 tip line, then the 📋 compliance line (8 physical lines total). Missing any content line is an error.**"

The phantom phrase is gone. The second CRITICAL sentence (line 318) remains unchanged and correct: "All 5 command-hint lines, the compliance line, and the 💡 tip line are required in every response." The footer code block is unchanged and canonical. ✓

---

### 1.4 Per-file headroom check (Recalibration Rule Steps 1–2)

Convention: ~125% of measured actual at calibration, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom | 10% Soft Floor | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 1,329 | 467 | ok |
| `setup-guide.md` | 11,035 | ~13,800 | 2,765 | 1,103 | ok |
| `user-guide.md` | 14,617 | ~18,300 | 3,683 | 1,461 | ok |
| `troubleshooting.md` | 27,345 | ~34,200 | 6,855 | 2,734 | ok |
| `LICENSE` | 1,067 | ~1,400 | 333 | 106 | ok |
| `template/CLAUDE.md` | 24,564 | ~30,800 | 6,236 | 2,456 | ok |
| `refresh-hot.md` | 4,542 | ~5,100 | 558 | 454 | ok (marginal — watch) |
| `ops/ingest.md` | 15,877 | ~19,800 | 3,923 | 1,587 | ok |
| `ops/lint.md` | 2,507 | ~3,100 | 593 | 250 | ok |
| `ops/update.md` | 1,881 | ~2,400 | 519 | 188 | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 1,659 | 674 | ok |
| `ops/audit.md` | 5,908 | ~8,200 | 2,292 | 590 | ok |
| `ops/token-reference.md` | 6,711 | ~8,500 | 1,789 | 671 | ok |
| `skills/SKILL.md` | 5,602 | ~7,000 | 1,398 | 560 | ok |
| `skills/query-layer.md` | 2,810 | ~3,600 | 790 | 281 | ok |
| `skills/ingest-hook.md` | 3,024 | ~3,800 | 776 | 302 | ok |

No triggers fire. All files inside headroom bounds.

**`refresh-hot.md` remains the narrowest margin** (headroom 558 vs soft floor 454 — within bounds by 104 chars). Flagged for the **fourth** consecutive audit. The S1 fix to `CLAUDE.md` reduced its actual by 24 bytes, slightly improving its headroom (now 6,236 vs prior 6,212) — no effect on `refresh-hot.md` itself. No content has been added to `refresh-hot.md` since its last calibration; no action required this cycle. At this cadence any non-trivial addition will fire the soft trigger.

No recalibration needed for any file this cycle. The CLAUDE.md shrinkage (24,588 → 24,564) marginally *increases* headroom for that row; the Chars column does not need an update because the hard trigger only fires when actual *exceeds* documented, and the soft trigger only fires when headroom falls below the floor — both conditions are clearly unmet.

---

### 1.5 Envelope check (Recalibration Rule Step 5)

Token sums are identical to audit #32 — the CLAUDE.md Tokens column (~7,700) is unchanged because the Chars column (~30,800) is unchanged (actual shrank but did not cross any threshold).

| Group | Tokens (documented) |
|---|---:|
| Blueprint docs | 1,500 + 3,450 + 4,580 + 8,550 + 350 = 18,430 |
| Template — CLAUDE.md | 7,700 |
| Template — ops | 4,950 + 780 + 600 + 2,100 + 2,050 + 2,120 = 12,600 |
| Template — refresh-hot | 1,280 |
| Skills | 1,750 + 900 + 950 = 3,600 |
| **Audit-scope total** | **43,610** |

Full-table sum (audit-scope + wiki-side rows): 43,610 + 80 + 950 + 250 + 625 = **45,515 tokens**

Against current ~47,000 ceiling: cushion = 1,485 tokens (3.2% > 2% floor of ~940 tokens). **Inside envelope.** ✓

No recalibration or envelope adjustment needed this cycle.

---

### 1.6 Cross-reference sanity checks

| Check | Result |
|---|:---:|
| `template/CLAUDE.md:9` CLAUDE.md self-cost `~7,700 tokens` — matches token-reference row (~30,800 ÷ 4 = ~7,700) | ✓ |
| `template/CLAUDE.md:19` cold-start total `~7,780 tokens` — 7,700 + 80 | ✓ |
| `template/CLAUDE.md:19` `!! ready` total `~8,730 tokens` — 7,780 + 950 | ✓ |
| `user-guide.md:9` CLAUDE.md startup cost `~7,700 tokens` | ✓ |
| `user-guide.md` cold-start `~7,780` and `!! ready` total `~8,730` | ✓ |
| `user-guide.md` cost table `Cold start: ~7,780` and `Cold start with !! ready: ~8,730` | ✓ |
| `user-guide.md:94` audit-all `~30,000–47,000` | ✓ |
| `user-guide.md:204` audit-all cost table `~30,000–47,000` | ✓ |
| `ops/audit.md:71` envelope `~30,000–47,000` | ✓ |
| `ops/token-reference.md` Step 5 `(currently ~30,000–47,000)` | ✓ |
| `ops/token-reference.md` floor note `(~940 tokens on a 47,000-token envelope)` — 47,000 × 2% = 940 | ✓ |
| `README.md` cold-start `~7,780 tokens` | ✓ |
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
| `CLAUDE.md` `!! ready` step 5 directional reference: "Blueprint-authoring Mode **above**" — audit #31 S1 fix, confirmed in audits #32 and #33 | ✓ |
| `refresh-hot.md` awk pipeline uses 1-arg `match()` form only | ✓ |
| Remaining `query.md` references — nil | ✓ |
| Schema version: 2.1 in CLAUDE.md footer — unchanged | ✓ |
| `token-reference.md` calibration date: 2026-04-20 — matches calibration from audit #32 cycle | ✓ |
| Footer block identical across `template/CLAUDE.md`, `setup-guide.md` Step 8, and `user-guide.md` Footer Commands section | ✓ |
| `.gitignore` content — 3 entries (`.obsidian/`, `.idea/`, `.DS_Store`); appropriate for blueprint distribution repo | ✓ |
| **Response Footer first CRITICAL sentence** — phantom "then a compliance line" phrase absent; audit #32 S1 fix confirmed applied | ✓ |

All 34 checks pass.

---

## 2. Findings

**No findings.**

The blueprint is logically sound across all 16 tracked files. The only change since audit #32 is the clean application of the S1 fix. No new logic contradictions, approval leaks, token-estimate drift, blueprint-sync drift, or cross-reference inconsistencies were identified.

---

## 3. Non-findings (considered and dismissed)

- **`refresh-hot.md` headroom.** 4,542 chars; headroom 558 chars; soft floor 454 chars. Headroom 558 > 454 — no trigger. Fourth consecutive audit flagging this. Still 104 chars above the soft floor. Any meaningful content addition will fire the trigger. No action required this cycle.

- **`template/CLAUDE.md` Chars recalibration.** Actual shrank from 24,588 to 24,564 (−24 bytes). The documented Chars value (~30,800) and Tokens (~7,700) do not need updating: the Recalibration Rule only fires when the actual *exceeds* the documented value (hard trigger) or headroom drops below 10% of actual (soft trigger). Neither applies — headroom increased slightly. No change to token-reference.md needed.

- **CHANGELOG.md S1 patch note.** Audit #32 recommended a patch-level CHANGELOG note for the S1 fix. CHANGELOG.md is out of scope for `!! audit all` and could not be verified. This is noted for completeness; if no CHANGELOG entry was made, one is warranted at the next opportunity (a single-sentence entry under a new v2.1.Z patch section suffices).

- **token-reference.md self-cost rounding.** Documented self-cost note states "~2,120 tokens." Computed from documented Chars: 8,500 ÷ 4 = 2,125 → rounds to 2,130 at nearest-10. The 10-token delta is within the system's explicit "rough planning figures" tolerance. Not a finding (same non-finding as audit #32).

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
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~10% of measured actual), envelope cushion floor (cushion < ~2% of upper bound). No trigger currently active. ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. Non-cascade exception documented as opt-out path. ✓
11. sqlite-query skill follows Query Layer Hook Contract and Ingest Hook Contract; FUSE-safe pattern (`?nolock=1` + `journal_mode=MEMORY` + `synchronous=OFF`) applied consistently across SKILL.md, query-layer.md, and ingest-hook.md. ✓

---

## 5. Verdict

**The v2.1 blueprint has 0 CRITICAL, 0 WARNING, and 0 STYLE findings.**

Audit #32's sole finding (S1 — phantom "then a compliance line" phrase in the Response Footer first CRITICAL sentence) was applied cleanly between the two audits: `template/CLAUDE.md` shrank by exactly 24 bytes, matching the removed phrase character-for-character. The corrected sentence now accurately describes the 8-line footer with no phantom elements. Both CRITICAL sentences in the Response Footer section are now consistent with each other and with the canonical footer code block.

The headroom table is healthy across all 16 tracked files with no triggers firing. The envelope cushion holds at 1,485 tokens (3.2%), above the 2% floor of ~940. `refresh-hot.md` remains the file to watch — fourth consecutive audit at marginal headroom, still within bounds.

Read-only audit complete. No fixes applied.
