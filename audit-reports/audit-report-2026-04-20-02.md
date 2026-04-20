# Blueprint Audit Report — 2026-04-20 (#32)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.1 (per `template/CLAUDE.md` footer — unchanged since audit #31)  
**Prior audit reviewed:** #31 (`audit-report-2026-04-20-01.md`) — read in full before this pass per user instruction  
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
- `.gitignore` (65 chars) ← read this audit for the first time; audit.md scope includes it

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

### 1.2 Files changed since audit #31

All sixteen previously-tracked files have **identical byte counts** to audit #31. Two files changed content without changing byte count:

| File | Change | Evidence |
|---|---|---|
| `template/CLAUDE.md` | S1 fix: "below" → "above" in `!! ready` step 5 | Both words are 5 bytes; count unchanged at 24,588 |
| `ops/token-reference.md` | W1/W2 recalibration cascade applied — 7 rows updated, calibration date advanced to 2026-04-20, envelope widened to ~47,000 | Numeric edits cancelled out; count unchanged at 6,711 |

All other tracked files byte-identical to audit #31.

---

### 1.3 Audit #31 findings resolution status

| Finding | Description | Status |
|---|---|:---:|
| W1 | `troubleshooting.md` soft recalibration trigger | ✅ **RESOLVED** — token-reference.md recalibrated; all 7 flagged rows updated to 125% of actuals; calibration date advanced |
| W2 | Post-recalibration envelope ceiling breach | ✅ **RESOLVED** — envelope widened from `~30,000–45,000` to `~30,000–47,000`; cascaded to `ops/audit.md:71`, `user-guide.md` (command reference + cost table), `token-reference.md` Step 5 parenthetical and floor note |
| S1 | `CLAUDE.md` `!! ready` step 5: "below" should be "above" | ✅ **RESOLVED** — confirmed "above" in `!! ready` step 5 body |

Zero open findings carried from audit #31.

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
| `template/CLAUDE.md` | 24,588 | ~30,800 | 6,212 | 2,458 | ok |
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

**`refresh-hot.md` remains the narrowest margin** (headroom 558 vs soft floor 454 — within bounds by 104 chars). Flagged for the third consecutive audit. No content has been added since its last calibration; no action required this cycle.

---

### 1.5 Envelope check (Recalibration Rule Step 5)

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
| `CLAUDE.md` `!! ready` step 5 directional reference: "Blueprint-authoring Mode **above**" — S1 fix from audit #31 confirmed | ✓ |
| `refresh-hot.md` awk pipeline uses 1-arg `match()` form only | ✓ |
| Remaining `query.md` references — nil | ✓ |
| Schema version: 2.1 in CLAUDE.md footer — unchanged | ✓ |
| `token-reference.md` calibration date: 2026-04-20 — matches today, consistent with W1/W2 recalibration | ✓ |
| Footer block identical across `template/CLAUDE.md`, `setup-guide.md` Step 8, and `user-guide.md` Footer Commands section | ✓ |
| `.gitignore` content — 3 entries (`.obsidian/`, `.idea/`, `.DS_Store`); all appropriate for a blueprint distribution repo | ✓ |
| **Response Footer first CRITICAL sentence** — prose describes phantom element; see S1 | **✗** |

---

## 2. Findings

### S1 — `CLAUDE.md` Response Footer: phantom element in first CRITICAL sentence

**Evidence:** `template/CLAUDE.md`, Response Footer section, first CRITICAL sentence:

> "Every single response — without exception — must end with the footer block exactly as shown: 5 command-hint lines, **then a compliance line**, then a blank separator, then the 💡 tip line, then the 📋 compliance line (8 physical lines total)."

The phrase "then a compliance line" describes an element at position 6 (immediately after the 5 command-hint lines), but no such element exists in the footer code block. The actual footer is:

```
Line 1-5: 5 command-hint lines
Line 6:   (blank separator)
Line 7:   💡 tip line
Line 8:   📋 Waterfall compliance line
```

Counting the described elements literally: 5 + 1 ("compliance line") + 1 (blank) + 1 (💡) + 1 (📋) = **9 elements for 8 physical lines**. This is internally inconsistent.

The second CRITICAL sentence in the same section is correct and unambiguous: `"All 5 command-hint lines, the compliance line, and the 💡 tip line are required in every response."` This correctly identifies three required elements (5 command hints, the 📋 compliance line, the 💡 tip) without the phantom middle term.

**Root cause:** Editing artifact — the phrase "then a compliance line" is a vestigial forward-reference to the 📋 line (or a remnant of a prior footer structure) that was not removed when the prose was last edited.

**Risk:** Low. The footer code block immediately below the sentence is canonical and unambiguous; agents follow the code block. The second CRITICAL sentence is also correct. However, a strict literal parse of the first sentence would produce 9-line footer attempts.

**Fix:** Remove the phantom phrase from the first CRITICAL sentence:

> "Every single response — without exception — must end with the footer block exactly as shown: 5 command-hint lines, then a blank separator, then the 💡 tip line, then the 📋 compliance line (8 physical lines total). Missing any content line is an error."

**Scope:** Single-file edit to `template/CLAUDE.md` only. No user-facing behavioral change; no Blueprint Sync cascade required (the footer code block and second CRITICAL sentence are both correct, and user-guide.md / setup-guide.md / README.md do not quote the prose description). Acceptable as a non-cascade under the existing exception with a patch-level CHANGELOG note.

---

## 3. Non-findings (considered and dismissed)

- **`refresh-hot.md` headroom.** 4,542 chars; headroom 558 chars; soft floor 454 chars. Headroom 558 > 454 — no trigger. Third consecutive audit flagging this. The file is ~104 chars from the soft trigger. Any meaningful content addition (a new rule, an extended comment) will fire it. Still within bounds; no action required this cycle.

- **`.gitignore` absent from prior audit reads.** `audit.md` explicitly lists `blueprint/.gitignore` in its `!! audit all` scope. Audits #1–#31 did not include `.gitignore` in their "files read in full" section, with no documented justification for the omission. This audit reads it. Content is trivially correct (3 entries: `.obsidian/`, `.idea/`, `.DS_Store`); no logic, no references to other files, no findings. Given that `.gitignore` is 65 bytes (≈16 tokens) and has no logic content, omitting it from future audit reads is reasonable — but the omission should be made explicit rather than silent. A standing note in `ops/audit.md` that `.gitignore` is de-minimis (read only if recently modified) would formalize the practice.

- **token-reference.md self-cost rounding.** The self-cost note states "~2,120 tokens to read." Computed from documented Chars: 8,500 ÷ 4 = 2,125, which rounds to nearest 10 as 2,130 — not 2,120. The 10-token delta is within the system's explicit "rough planning figures" tolerance. Not a finding.

- **S1 (audit #31) verification.** `!! ready` step 5 confirmed to say "Blueprint-authoring Mode **above**". Fix applied cleanly between audits. ✓

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

**The v2.1 blueprint has 0 CRITICAL, 0 WARNING, and 1 STYLE findings.**

All three findings from audit #31 (W1 recalibration, W2 envelope widening, S1 directional reference) have been cleanly resolved. The recalibration widened all seven flagged token-reference.md rows to 125% of current actuals, advanced the calibration date to 2026-04-20, widened the envelope to ~47,000 tokens, and cascaded the new figure to all four required locations. The headroom table is healthy across all 16 tracked files with no triggers firing. The envelope cushion is 1,485 tokens (3.2%) — well above the 2% floor of 940.

The single new finding (S1) is a minor prose inconsistency in `CLAUDE.md`'s Response Footer description that has no behavioral effect (the code block is canonical). A one-phrase removal fixes it: delete "then a compliance line" from the first CRITICAL sentence.

Read-only audit complete. No fixes applied.
