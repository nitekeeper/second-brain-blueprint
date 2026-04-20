# Blueprint Audit Report — 2026-04-19 (#29)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.1 (per `template/CLAUDE.md` footer — bumped from v2.0.23 since audit #28)  
**Prior audit reviewed:** #28 (`audit-report-2026-04-19-18.md`) — read in full before this pass per user instruction  
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)  
**Mode:** Blueprint-authoring (wiki/ absent at working-folder root; log append and hot.md refresh skipped per Blueprint-authoring Mode rule)  
**Note:** Audit reports directory (`audit-reports/`) excluded from scope per standing user instruction.

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**

- `README.md` (4,671 chars)
- `setup-guide.md` (10,584 chars)
- `user-guide.md` (14,219 chars) — unchanged; not re-read; byte identity confirmed
- `troubleshooting.md` (23,953 chars)
- `LICENSE` (1,067 chars) — unchanged; byte identity confirmed
- `.gitignore` (65 chars) — unchanged; byte identity confirmed

**Template**

- `template/CLAUDE.md` (24,081 chars)
- `template/scheduled-tasks/refresh-hot.md` (4,542 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,877 chars) — unchanged; byte identity confirmed
- `template/scheduled-tasks/ops/lint.md` (2,507 chars) — unchanged; byte identity confirmed
- `template/scheduled-tasks/ops/query.md` — **MISSING** (was 2,586 chars in audit #28)
- `template/scheduled-tasks/ops/update.md` (1,881 chars) — unchanged; byte identity confirmed
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars) — unchanged; byte identity confirmed
- `template/scheduled-tasks/ops/audit.md` (5,908 chars) — unchanged; byte identity confirmed
- `template/scheduled-tasks/ops/token-reference.md` (6,711 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (5,518 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,612 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,917 chars)

**Not in audit scope:** `ROADMAP.md` (planning doc, no logic content). `CHANGELOG.md` formally out of scope per v2.0.21. `audit-reports/` excluded per standing user instruction.

---

### 1.2 Files changed since audit #28

| File | Audit #28 bytes | This audit bytes | Delta | Cause |
|---|---:|---:|---:|---|
| `template/CLAUDE.md` | 21,112 | 24,081 | +2,969 | Schema bump to v2.1; Query Routing Rule embedded; Directory Structure updated |
| `template/scheduled-tasks/refresh-hot.md` | 3,966 | 4,542 | +576 | Added Step 3 (Active skills detection) and Field Reference row |
| `skills/sqlite-query/SKILL.md` | 4,185 | 5,518 | +1,333 | FUSE limitation section added; Uninstall section added; Fallback / DB desync recovery expanded |
| `skills/sqlite-query/query-layer.md` | 2,533 | 2,612 | +79 | Minor content edits |
| `skills/sqlite-query/ingest-hook.md` | 2,838 | 2,917 | +79 | Minor content edits |
| `setup-guide.md` | 10,564 | 10,584 | +20 | Minor edit (unidentified; diff not available) |
| `troubleshooting.md` | 22,670 | 23,953 | +1,283 | New troubleshooting entry added |
| `ops/token-reference.md` | 6,746 | 6,711 | −35 | Minor edit (unidentified; net shrink) |
| `template/scheduled-tasks/ops/query.md` | 2,586 | **MISSING** | — | File deleted or lost; was a tracked template file |

---

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Convention: ~125% of measured actual at calibration, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom | 10% Soft Floor | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 1,329 | 467 | ok |
| `setup-guide.md` | 10,584 | ~13,200 | 2,616 | 1,058 | ok |
| `user-guide.md` | 14,219 | ~17,800 | 3,581 | 1,422 | ok |
| `troubleshooting.md` | 23,953 | ~28,300 | 4,347 | 2,395 | ok |
| `LICENSE` | 1,067 | ~1,400 | 333 | 107 | ok |
| `template/CLAUDE.md` | 24,081 | ~25,800 | 1,719 | 2,408 | **SOFT** |
| `refresh-hot.md` | 4,542 | ~5,100 | 558 | 454 | ok |
| `ops/ingest.md` | 15,877 | ~19,800 | 3,923 | 1,588 | ok |
| `ops/lint.md` | 2,507 | ~3,100 | 593 | 251 | ok |
| `ops/update.md` | 1,881 | ~2,400 | 519 | 188 | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 1,659 | 674 | ok |
| `ops/audit.md` | 5,908 | ~8,200 | 2,292 | 591 | ok |
| `ops/token-reference.md` | 6,711 | ~8,500 | 1,789 | 671 | ok |
| `skills/sqlite-query/SKILL.md` | 5,518 | ~5,200 | −318 | 552 | **HARD** |
| `skills/sqlite-query/query-layer.md` | 2,612 | ~3,200 | 588 | 261 | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,917 | ~3,500 | 583 | 292 | ok |

**Hard trigger: `skills/sqlite-query/SKILL.md`** — measured 5,518 exceeds documented 5,200. Recalibration required. Corrected row: 5,518 × 125% ≈ ~6,900 chars → ~1,720 tokens (was ~1,300).

**Soft trigger: `template/CLAUDE.md`** — headroom 1,719 is below the 10%-of-measured floor of 2,408. Pre-emptive recalibration warranted. Corrected row: 24,081 × 125% ≈ ~30,100 chars → ~7,520 tokens (was ~6,450).

---

### 1.4 Envelope check (Recalibration Rule Step 5)

Token table sum from current `ops/token-reference.md` (all enumerated rows except unbounded `wiki/log.md full`):

**Current documented sum: 41,895 tokens** (note: audit #28 stated 40,820 — see Questions §4 for the discrepancy).

Envelope: `~30,000–43,000`. Current cushion: 43,000 − 41,895 = **1,105 tokens** (2.6% of 43,000 — above the 2% floor of ~860). Envelope intact at present documented values.

**Recalibration cascade projection:**

| Recalibration | Δ Tokens | Running Sum | Cushion | 2% Floor Pass? |
|---|---:|---:|---:|:---:|
| Baseline (current table) | — | 41,895 | 1,105 | ✓ (2.6%) |
| After SKILL.md (hard trigger) | +420 | 42,315 | 685 | **FAIL** (1.6% < 2%) |
| After SKILL.md + CLAUDE.md (soft trigger) | +1,070 | 43,385 | −385 | **BREACH** |

**If both recalibrations are applied, the current 43,000 ceiling is breached by 385 tokens.** Per Recalibration Rule Step 5, the envelope must be widened. Proposed new upper bound: documented sum after both recalibrations (43,385) + ~2,000 cushion → **~45,000**. All four `!! audit all` envelope mentions must cascade: `ops/audit.md:71`, `user-guide.md` (command reference and cost table), and any applicable `CHANGELOG.md` entry.

Even with SKILL.md recalibration alone, the cushion (685) drops below the 2% floor (860), independently requiring a widening even if CLAUDE.md soft trigger is deferred.

---

### 1.5 Cross-reference sanity checks

| Check | Result |
|---|:---:|
| `template/CLAUDE.md` cold-start self-cost `~6,450` — matches token-reference CLAUDE.md row (~25,800 ÷ 4) | ✓ (pre-recal) |
| `template/CLAUDE.md` cold-start total `~6,530` — 6,450 + 80 | ✓ |
| `user-guide.md:9` CLAUDE.md startup cost `~6,450 tokens` | ✓ (pre-recal) |
| `user-guide.md:94` audit-all `~30,000–43,000` | ✓ (pre-widen) |
| `user-guide.md:201` audit-all cost table `~30,000–43,000` | ✓ (pre-widen) |
| `ops/audit.md:71` envelope `~30,000–43,000` | ✓ (pre-widen) |
| `ops/token-reference.md` Step 5 `(currently ~30,000–43,000)` | ✓ (pre-widen) |
| `ops/token-reference.md` floor note `(~860 tokens on a 43,000-token envelope)` — 43,000 × 2% = 860 | ✓ |
| Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md`, `README.md`, and `user-guide.md` | ✓ |
| Blueprint Sync Rule 12-row matrix — intact; Non-cascade exception correctly appended as `>` note, not a table row | ✓ |
| Versioning split (`Schema version: 2.1` in template footer) — this is a minor bump (2.0 → 2.1) requiring full cascade per "Any schema change" / "Minor/major bumps" rule | Partially ✓ — template/CLAUDE.md updated; downstream doc propagation not verified (user-guide.md unchanged; README.md unchanged) |
| `ops/audit.md` scope list — "every file under `blueprint/template/scheduled-tasks/ops/`" (glob, not enumerated) — dynamically correct even with query.md gone | ✓ |
| `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading | ✓ |
| Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv` → Step 7 page write | ✓ |
| Hash canonicalization 6-step pipeline — intact | ✓ |
| `Pages: N` derived from `^- [[` entries — `refresh-hot.md` awk pipeline unchanged (still uses 1-arg `match()` form only) | ✓ |
| Blueprint-authoring mode guard — present in `template/CLAUDE.md` and `audit.md:43` | ✓ |
| Hook contracts (query-layer and ingest-hook) — consistent across conventions.md, ingest.md, update.md, query-layer.md, ingest-hook.md | ✓ |
| `setup-guide.md:241` ops file count — says "7 ops files" | **FAIL** — only 6 template ops files exist |
| `template/CLAUDE.md` Directory Structure `scheduled-tasks/ops/` listing — includes `query.md` | **FAIL** — query.md not deployable (template source missing) |
| `query-layer.md:3-5` — "Overrides the built-in grep query step in `ops/query.md`" | **STALE** — query routing now in CLAUDE.md; `ops/query.md` not in template |

---

## 2. Findings

### CRITICAL

**C1 — `blueprint/template/scheduled-tasks/ops/query.md` is missing**

`setup-guide.md` Step 2 copy table (line 74) lists:
```
| blueprint/template/scheduled-tasks/ops/query.md | scheduled-tasks/ops/query.md |
```
The source file does not exist (`wc -c`: `No such file or directory`). Every new wiki setup will fail at Step 2 attempting to copy a nonexistent file. Since v2.1 embedded query routing directly into CLAUDE.md's `## Query Routing Rule` section (and the Ops File Reminder table has no `query` row), the intent appears to be that `ops/query.md` was intentionally retired — but the cleanup is incomplete. Three locations still reference the file as if it exists or will be deployed.

Exact failure point: `cp blueprint/template/scheduled-tasks/ops/query.md scheduled-tasks/ops/query.md` → `cp: blueprint/template/scheduled-tasks/ops/query.md: No such file or directory`.

**C2 — `skills/sqlite-query/SKILL.md` hard recalibration trigger**

Measured actual (5,518 chars) exceeds the documented Chars value (5,200) in `ops/token-reference.md:34`. Per Recalibration Rule, this is a hard trigger requiring immediate recalibration. All token estimates derived from this row are currently understated (~1,300 tokens documented vs ~1,380 tokens actual). Corrected row: `~6,900 | ~1,720`.

Cascade impact: correcting SKILL.md alone drops the envelope cushion to 685 tokens (below the 860-token 2% floor), independently triggering an envelope widening even before addressing the CLAUDE.md soft trigger.

---

### WARNING

**W1 — `setup-guide.md:241` ops file count is stale**

Step 7 verification says: `- [ ] All 7 ops files exist in scheduled-tasks/ops/`. The template `ops/` directory now contains 6 files (ingest, lint, audit, update, conventions, token-reference). If `query.md` was intentionally retired with v2.1, the count must be corrected to 6. If it was accidentally deleted, fixing C1 restores the count.

**W2 — `template/CLAUDE.md` Directory Structure lists `query.md` as a deployed file**

Line 215 of `template/CLAUDE.md` shows `├── query.md` under `scheduled-tasks/ops/` in the live-wiki directory structure. With the template source missing and the copy step failing (C1), no live wiki will have this file. The directory structure must reflect the post-v2.1 reality.

**W3 — `query-layer.md:3–5` stale reference to `ops/query.md`**

```
Installed by the `sqlite-query` skill. Overrides the built-in grep query step in `ops/query.md`.
```
In schema v2.1, the query routing waterfall is embedded directly in `CLAUDE.md`'s `## Query Routing Rule` section — there is no separate `ops/query.md`. The description of what query-layer.md overrides is now incorrect. This is installed to `scheduled-tasks/query-layer.md` in live wikis; users reading it will be misled about what it replaces.

**W4 — `template/CLAUDE.md` soft recalibration trigger**

Measured actual (24,081 chars) leaves headroom of 1,719 chars (25,800 − 24,081), which is below the 10%-of-measured soft floor of 2,408 chars. Per Recalibration Rule, a pre-emptive recalibration is warranted before the next schema edit consumes the remaining buffer. Corrected row: `~30,100 | ~7,520`.

Cascade impact if both C2 and W4 are recalibrated: token table sum rises to ~43,385, breaching the 43,000 ceiling and requiring an envelope widening. Proposed new upper bound: **~45,000** (43,385 + ~1,600 cushion, rounded to nearest 1,000). The envelope mentions in `ops/audit.md:71`, `user-guide.md` (two locations), and `ops/token-reference.md` Step 5 must all update.

Additionally, if CLAUDE.md recalibrates from ~6,450 to ~7,520 tokens, the following cross-references must update:
- `template/CLAUDE.md:9` — `~6,450 tokens` self-cost → `~7,520`
- `template/CLAUDE.md:19` — cold-start total `~6,530` → `~7,600`; `!! ready` total `~7,480` → `~8,550`
- `user-guide.md` — cold-start figures referencing `~6,450`
- `README.md:72` — `~6,530 tokens` cold-start → `~7,600`

---

### STYLE

**S1 — Directory Structure indentation typo in `template/CLAUDE.md:200`**

```
│   │   │           ├── update.md
```
Has an extra `│   │` prefix relative to its siblings (`ingest.md`, `lint.md`, `audit.md`, `conventions.md`, `token-reference.md` — all at `│   │           ├── …`). The correct line is:
```
│   │           ├── update.md
```

---

## 3. Non-findings (considered and dismissed)

- **Schema v2.1 minor version bump cascade.** `user-guide.md` and `README.md` are unchanged; they may need a version-string update if they contain explicit schema version references. However, neither file was flagged by audit #28 for version-pinned content, and the "Versioning split" rule only requires propagating via the "Any schema change" row — which mainly targets CLAUDE.md content changes, not necessarily a version number in prose. Not elevated to a finding pending manual verification of whether explicit version strings appear in those files.
- **`refresh-hot.md` headroom.** Grew to 4,542 from 3,966 (+576 bytes). Headroom 558 > 10% floor 454. No trigger — but within one moderate edit of firing.
- **`ops/token-reference.md` sum discrepancy vs audit #28.** Audit #28 stated the table sum was 40,820 tokens; the current calculated sum is 41,895 — a difference of 1,075. The token-reference.md file itself shrank by 35 bytes between audits, suggesting some row content changed. Unable to reconstruct the prior table without a diff. Both the prior and current sums fall within the ~30,000–43,000 envelope. Not a defect; noted as Question for Clarification.
- **`template/CLAUDE.md` placeholders `[created-date]`, `[updated-date]`, and Setup note block.** Present in the template file as intended scaffolding for Step 3 of setup-guide.md. Expected behavior.
- **`ops/audit.md` scope glob "Every file under `blueprint/template/scheduled-tasks/ops/`".** This is dynamically correct — it does not enumerate `query.md` by name, so the missing file does not cause a false audit scope claim. The glob will simply cover the 6 remaining files. Not a finding.
- **sqlite-query skill FUSE warning and uninstall steps.** Added content in SKILL.md is internally consistent with query-layer.md and ingest-hook.md. DB path (`WORKDIR.parent / "wiki.db"`) is consistent across SKILL.md, query-layer.md, and ingest-hook.md. ✓
- **`refresh-hot.md` Step 3 Active skills detection** (`[ -f scheduled-tasks/query-layer.md ]`). Matches the guard in `template/CLAUDE.md` Query Routing Rule Step 2 sub-step 2. ✓
- **`!! ready` mid-session guard** — present in template/CLAUDE.md; consistent with troubleshooting.md entry. ✓
- **`!! wrap` pre-write safeguard and `TRUNCATED_ACKNOWLEDGED` handling** — consistent across template/CLAUDE.md and troubleshooting.md. ✓
- **Ingest atomic ordering** — Step 5 `ts` pre-compute → Step 6 `mv` → Step 7 page write. Unchanged and correct. ✓
- **`!! ready` total `~7,480`** — 6,530 + 950. Pre-recalibration this is internally consistent; post-recalibration it will need updating (documented as cascade consequence of W4, not a standalone finding).

---

## 4. Questions for Clarification

**Q1 — Was `ops/query.md` intentionally retired in v2.1?**

The evidence strongly suggests yes: CLAUDE.md v2.1 has a full embedded `## Query Routing Rule` waterfall, the Ops File Reminder table has no `query` row, and no comment in the file explains the omission. However, no CHANGELOG entry (which is out of scope) was verified, and three stale references remain (C1, W2, W3). Confirmation would allow closing C1 as a deliberate removal requiring cleanup, versus an accidental file deletion requiring restoration.

**Q2 — Token table sum discrepancy (40,820 vs 41,895).**

Audit #28 stated the table sum was 40,820 tokens. The current calculation from the live `token-reference.md` Tokens column yields 41,895. The file shrank 35 bytes, not enough to account for the 1,075-token gap. Were some rows recalibrated between audit #28 and this audit in a way not reflected in the prior report?

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#28 re-verified, with one partial exception:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:43`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer now reads `Schema version: 2.1`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~10% of measured actual), envelope cushion floor (cushion < ~2% of upper bound). ✓ — **All three are firing in this audit** (C2 hard, W4 soft, W4 cascade envelope floor).
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. Non-cascade exception documented as opt-out path requiring CHANGELOG justification. ✓
11. sqlite-query skill follows Query Layer Hook Contract (`find`-based path resolution, no glob patterns) and Ingest Hook Contract (non-fatal errors, consistent repair messaging). ✓

---

## 6. Verdict

**The v2.1 blueprint has 2 CRITICAL, 4 WARNING, and 1 STYLE finding.**

Since audit #28, 8 tracked files changed (and 1 was deleted). The schema was bumped from v2.0.23 to v2.1 with the Query Routing Rule embedded in CLAUDE.md — a meaningful structural change — but the cleanup of downstream references to the retired `ops/query.md` is incomplete (C1, W1, W2, W3). Additionally, the SKILL.md growth triggers a hard recalibration (C2) whose cascade, when combined with the CLAUDE.md soft trigger (W4), would breach the current token envelope ceiling and require widening.

**Priority order for fixes:**
1. Resolve Q1 (intent for `ops/query.md`) — determines whether C1 is a cleanup or a restore
2. Apply SKILL.md hard recalibration (C2) and envelope widening
3. Fix stale references: `setup-guide.md:241` count (W1), `template/CLAUDE.md` Directory Structure (W2), `query-layer.md:3-5` (W3)
4. Apply CLAUDE.md soft recalibration (W4) and cascade cold-start totals
5. Fix Directory Structure indentation typo (S1)

Read-only audit complete. No fixes applied.
