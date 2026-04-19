# Blueprint Audit Report — 2026-04-19 (#11)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.10 (per CHANGELOG.md; no later CHANGELOG entry found)  
**Prior audit reviewed:** #10 (`audit-report-2026-04-18-10.md`)  
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)  
**Mode:** Blueprint-authoring (no `wiki/` present at working-folder root; log append and `hot.md` refresh skipped)  
**Note:** Audit reports directory (`audit-reports/`) was explicitly excluded from scope per user instruction.

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**

- `README.md` (4,671 chars)
- `setup-guide.md` (10,564 chars)
- `user-guide.md` (14,219 chars)
- `troubleshooting.md` (21,536 chars)
- `CHANGELOG.md` (55,265 chars)
- `LICENSE` (1,067 chars)
- `.gitignore` (65 chars)

**Template**

- `template/CLAUDE.md` (20,653 chars)
- `template/scheduled-tasks/refresh-hot.md` (3,966 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,852 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/query.md` (2,586 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,379 chars)
- `template/scheduled-tasks/ops/audit.md` (6,563 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,747 chars)

**Skills (blueprint/skills/)**

- `blueprint/skills/sqlite-query/SKILL.md` (3,742 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (1,962 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,639 chars)

**Not in audit scope:** `blueprint/` sub-directory internals (working-folder-level installed files), `ROADMAP.md` (planning doc, no logic content).

**Not present (previously tracked, now absent):** `template/scheduled-tasks/changelog-monitor.md` — confirmed missing from template directory; no CHANGELOG entry explains removal.

### 1.2 Verification that audit-#10 findings landed in v2.0.10

| Fix | Claim | Verified |
|---|---|---|
| W1 | `changelog-monitor.md` Step 1 rewritten as `source_url:` reverse-lookup | Cannot verify — `changelog-monitor.md` absent from template directory entirely |
| W1 | `source_url:` made mandatory frontmatter field in `ops/ingest.md` Step 7 | ✓ `ingest.md:90`: `source_url:` listed as mandatory with explicit fallback path |
| W1 cascade | `troubleshooting.md` entries added for UNINGESTED/AMBIGUOUS cases | — (changelog-monitor.md removed; no longer applicable) |
| W1 cascade | CHANGELOG v2.0.10 entry documents fix | ✓ present and detailed |

The v2.0.10 W1 fix is partially verifiable: the `ops/ingest.md` change landed correctly. The `changelog-monitor.md` half of the fix cannot be verified because the file has been removed from the template entirely; whether the fix was applied before removal is unknown.

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Current convention per `token-reference.md`: **~125% of measured actual at calibration**, rounded to nearest 100. (Changed from 110% in prior versions — see W3.)

| File | Measured (`wc -c`) | Doc. Chars | Doc. Tokens | Headroom | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | ~1,500 | 28.5% | ok |
| `setup-guide.md` | 10,564 | ~12,800 | ~3,200 | 21.2% | ok |
| `user-guide.md` | 14,219 | ~17,100 | ~4,280 | 20.3% | ok |
| `troubleshooting.md` | 21,536 | ~27,300 | ~6,830 | 26.8% | ok |
| `CHANGELOG.md` | 55,265 | **NOT IN TABLE** | — | — | ⚠️ MISSING |
| `LICENSE` | 1,067 | ~1,400 | ~350 | 31.3% | ok |
| `template/CLAUDE.md` | 20,653 | ~25,000 | ~6,250 | 21.1% | ok |
| `refresh-hot.md` | 3,966 | ~5,100 | ~1,280 | 28.6% | ok |
| `ops/ingest.md` | 15,852 | ~18,600 | ~4,650 | 17.3% | ok |
| `ops/lint.md` | 2,507 | ~2,900 | ~730 | 15.7% | ok |
| `ops/query.md` | 2,586 | ~2,400 | ~600 | **-7.8%** | 🔴 HARD TRIGGER |
| `ops/update.md` | 1,881 | ~1,700 | ~430 | **-10.6%** | 🔴 HARD TRIGGER |
| `ops/conventions.md` | 6,379 | ~5,700 | ~1,430 | **-11.9%** | 🔴 HARD TRIGGER |
| `ops/audit.md` | 6,563 | ~8,200 | ~2,050 | 25.0% | ok |
| `ops/token-reference.md` | 6,747 | ~8,300 | ~2,080 | 23.0% | ok |
| `skills/sqlite-query/SKILL.md` | 3,742 | ~4,700 | ~1,180 | 25.6% | ok |
| `skills/sqlite-query/query-layer.md` | 1,962 | ~2,500 | ~630 | 27.4% | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,639 | ~3,300 | ~830 | 25.0% | ok |

Three files fire the hard recalibration trigger (measured ≥ documented). `CHANGELOG.md` is absent from the table entirely (see W2).

Recommended recalibration values (125% × measured, rounded to nearest 100 / nearest 10):

| File | Current | Recommended |
|---|---|---|
| `ops/query.md` | ~2,400 / ~600 | ~3,300 / ~830 |
| `ops/update.md` | ~1,700 / ~430 | ~2,400 / ~600 |
| `ops/conventions.md` | ~5,700 / ~1,430 | ~8,000 / ~2,000 |

### 1.4 Envelope check (Recalibration Rule Step 5)

Documented rows sum (from `token-reference.md`):

Blueprint-doc rows (excluding missing CHANGELOG.md):
`README (1,500) + setup-guide (3,200) + user-guide (4,280) + troubleshooting (6,830) + LICENSE (350) = 16,160`

Template-side rows:
`CLAUDE (6,250) + refresh-hot (1,280) + ingest (4,650) + lint (730) + query (600) + update (430) + conventions (1,430) + audit (2,050) + token-reference (2,080) = 19,500`

Skill rows:
`SKILL.md (1,180) + query-layer (630) + ingest-hook (830) = 2,640`

**Table sum = 38,300 tokens** — appears to be 27.2% under the 54,000 envelope upper bound (15,700 token cushion = 29.1%).

**However**, `CHANGELOG.md` (55,265 chars / ~13,816 tokens actual) IS read during `!! audit all` per `ops/audit.md` line 15, but is NOT in the table. Actual `!! audit all` cost ≈ 38,300 + 13,816 = **~52,116 tokens**. Against the 54,000 upper bound, real cushion = **1,884 tokens ≈ 3.5%** — above the 2% floor (1,080 tokens) but tight, and not representable by re-summing the table per the documented instruction.

### 1.5 Cross-reference sanity checks

- `template/CLAUDE.md:17` cold-start `~6,330` = 6,250 (CLAUDE.md token-reference row) + 80 (hot.md). ✓
- `user-guide.md:8–11` cold-start quote `~6,330` / `!! ready` total `~7,280` matches token-reference math. ✓
- `user-guide.md` realistic `!! wrap` `~3,000` / `!! ready` `~3,300` matches token-reference calculation: `1,280 (refresh-hot) + 250 (index) + 625 (log tail) + 100 (log append) + 750 (memory write mid) = 3,005 ≈ ~3,000`. ✓
- `ops/audit.md:71` envelope `~30,000–54,000` is numerically correct for actual audit cost but no longer derivable from re-summing the table (see W2). ⚠️
- **`template/CLAUDE.md:9` says "~5,500 tokens" for its own read cost; token-reference row says ~6,250.** ⚠️ (see W1)
- `ingest.md` atomic ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 write source page. ✓
- Three Approval Rule exceptions in `template/CLAUDE.md:58–72` (`!! wrap`, `!! ready`, `!! audit`). ✓
- Blueprint Sync Rule 12-row matrix intact. ✓

---

## 2. Findings

### CRITICAL

None.

### WARNING

**W1 — `template/CLAUDE.md` line 9 quotes stale `~5,500 tokens` for its own read cost; contradicts `token-reference.md` row and breaks the cold-start figure's internal derivation.**

*Evidence.*

`template/CLAUDE.md:9`:
> `1. Read `CLAUDE.md` (this file) — ~5,500 tokens`

`token-reference.md` (File Read Costs table):
> `| CLAUDE.md | ~25,000 | ~6,250 |`

`template/CLAUDE.md:17`:
> `**Total cold-start cost: ~6,330 tokens**`

*Logical failure.* The cold-start total of ~6,330 is consistent with the token-reference row: 6,250 (CLAUDE.md) + 80 (hot.md) = 6,330 ✓. But line 9 says ~5,500 — an agent or user reading line 9 would compute cold-start as ~5,580 (5,500 + 80), not ~6,330. The total on line 17 is right; the per-file line 9 is stale. The ~5,500 figure appears to be a holdover from before the latest recalibration raised CLAUDE.md's documented size from ~21,900/~5,475 to ~25,000/~6,250. This is the same cascade-miss class as audit #6 W1 (`user-guide.md:14`) and #8 W1 (`user-guide.md:216–217`): a single-file recalibration number that didn't propagate to every self-reference.

*Recommended fix.* Update `template/CLAUDE.md:9` from `~5,500 tokens` to `~6,250 tokens`. One-line change; no other file depends on the line-9 figure (the cold-start total on line 17 and all downstream quotes derive from the token-reference row, which is already correct).

---

**W2 — `blueprint/CHANGELOG.md` absent from `token-reference.md`; source-of-truth invariant violated; `!! audit all` envelope no longer derivable from the table.**

*Evidence.*

`ops/audit.md:71` (Notes):
> "the source of truth. Re-derive by summing the blueprint-doc and template-side rows rather than hand-tuning this figure"

`ops/audit.md:15` (audit-all scope):
> `- blueprint/CHANGELOG.md`

`token-reference.md` (File Read Costs): `blueprint/CHANGELOG.md` row is absent.

`CHANGELOG.md` measured: 55,265 chars / ~13,816 tokens actual (at 125% headroom → ~69,100 chars / ~17,275 tokens for the table row).

*Logical failure.* `CHANGELOG.md` is a mandatory read in `!! audit all` scope, but is not tracked in the token-reference table. The consequence is two-fold:

1. **Source-of-truth invariant is broken.** `token-reference.md` header: "Any quoted cost in CLAUDE.md, README.md, user-guide.md, or setup-guide.md must be re-derivable from this table." `ops/audit.md:71` adds: re-derive by summing the table. Re-summing the table as instructed now yields ~38,300 tokens; the actual `!! audit all` cost is ~52,116 tokens. The 13,816-token gap makes the table-derived figure misleading.

2. **Envelope cushion appears inflated.** The 54,000 upper bound was set when CHANGELOG.md was in the table. An agent re-deriving from the table today would compute 38,300 tokens and see a 29% cushion (15,700 tokens) — far more comfortable than the actual 3.5% (1,884 tokens). A future per-file recalibration pass that pushed any row up by ~2,000 tokens would appear safe (still 27% below 54,000) while in reality the true cost would breach the envelope.

*Historical note.* `CHANGELOG.md` was tracked at `~60,700/~15,180` in the v2.0.10 recalibration. The current file is 55,265 chars (CHANGELOG shrank slightly since then, possibly from editing or a session reset). It was removed from the table as part of an undocumented recalibration pass on 2026-04-19 (see W3).

*Recommended fix.* Re-add `blueprint/CHANGELOG.md` to the blueprint-doc rows: 55,265 × 1.25 = 69,081 → **~69,100 / ~17,275**. This raises the table sum to ~55,575 tokens, which exceeds the 54,000 envelope upper bound. Per Recalibration Rule Step 5: widen the envelope (55,575 + ~1,500–3,000 cushion, rounded to nearest 1,000) → **`~30,000–58,000`**. Cascade to `ops/audit.md:71`, `user-guide.md` (command reference and cost table). This is the same Blueprint Sync cascade as every prior envelope widen.

---

**W3 — A substantial recalibration pass landed on 2026-04-19 with no CHANGELOG entry, violating the Blueprint Sync Rule schema-version-bump requirement.**

*Evidence.*

`token-reference.md` header: "last calibrated: 2026-04-19"

`CHANGELOG.md` most recent entry: v2.0.10, dated 2026-04-18. No entry for 2026-04-19.

`template/CLAUDE.md` Blueprint Sync Rule ("Schema version bump" row):
> "blueprint/CHANGELOG.md (new section documenting the version)"

The 2026-04-19 pass made the following schema/operations/file-size changes, each of which triggers a CHANGELOG requirement:

1. **Headroom convention changed from ~110% to ~125%.** The Recalibration Rule in `token-reference.md:71` now reads "set to ~125% of measured actual." The previous value was "~110% of measured actual" (confirmed by the v2.0.9 and v2.0.10 CHANGELOG entries which explicitly cite the 110% convention). This is a change to a documented rule — not a routine recalibration — and warrants a named patch entry.

2. **`blueprint/CHANGELOG.md` removed from the tracked-files table.** (See W2.)

3. **`changelog-monitor.md` removed from the template entirely.** The file `template/scheduled-tasks/changelog-monitor.md` is gone. It was read in audit #10, had its own token-reference row, and was listed in the v2.0.1 Blueprint Sync Rule "New scheduled task" row. No CHANGELOG entry records its deprecation or removal. The audit scope parenthetical in `ops/audit.md:23` ("currently `refresh-hot.md`") is now technically accurate but gives no hint that `changelog-monitor.md` was ever there.

4. **sqlite-query skill added.** `blueprint/skills/sqlite-query/` (three files) was added. The Blueprint Sync Rule "New skill bundle added" row mandates: `ops/token-reference.md`, `blueprint/user-guide.md`, `blueprint/setup-guide.md`, `blueprint/ROADMAP.md`, `ops/conventions.md`, and a CHANGELOG entry. The user-visible docs (user-guide, setup-guide, ROADMAP, conventions) were all updated correctly. Only the CHANGELOG entry is missing.

5. **All tracked-file Chars values recalibrated at the new 125% convention.** At minimum, the "File-size or cost change" row of the Blueprint Sync Rule applies, which triggers `token-reference.md` propagation (done) and re-propagation of cold-start totals to CLAUDE.md, README.md, user-guide.md (done, except W1 above). But the convention change itself — not just the resulting numbers — has no documented rationale anywhere in the changelog.

*Impact.* A future maintainer reading the CHANGELOG would have no record of why the headroom changed from 110% to 125%, why changelog-monitor.md was removed, or when the sqlite-query skill was introduced. The CHANGELOG's role is exactly to capture this — its absence leaves a gap in the audit trail.

*Recommended fix.* Create a CHANGELOG entry (v2.0.11) covering: (a) sqlite-query skill added, (b) headroom convention changed from 110% to 125% with rationale, (c) `changelog-monitor.md` deprecated and removed from template, (d) CHANGELOG.md row removal (to be remedied by W2's fix), and (e) all file-size recalibrations. Blueprint Sync Rule: "treat any new skill bundle as at minimum a patch version bump."

### STYLE

**S1 — Three files fire the hard recalibration trigger (measured actual ≥ documented Chars).**

`ops/query.md` (2,586 measured vs. ~2,400 documented, +7.8%), `ops/update.md` (1,881 vs. ~1,700, +10.6%), `ops/conventions.md` (6,379 vs. ~5,700, +11.9%). All three must be recalibrated immediately per the Recalibration Rule ("Fire immediately when any file's measured actual exceeds its documented Chars value"). Recalibrated values at 125% (detailed in §1.3 table above): `ops/query.md` → `~3,300/~830`, `ops/update.md` → `~2,400/~600`, `ops/conventions.md` → `~8,000/~2,000`. These three rows' token-column changes (+230, +170, +570 tokens) raise the template-side sum by ~970 tokens — within the current apparent cushion but slightly shrinking it.

**S2 — `template/CLAUDE.md` Directory Structure diagram locates sqlite-query skill files under `template/skills/`, but the canonical location used by all ops is `blueprint/skills/`.**

`template/CLAUDE.md` directory structure (lines ~128–154) shows:
```
│   └── template/
│       ...
│       └── skills/                ← Installable skill bundles
│           └── sqlite-query/
│               ├── SKILL.md
│               ├── query-layer.md
│               └── ingest-hook.md
```

But `ops/audit.md:25` scopes to `blueprint/skills/`; `SKILL.md:69` sources files from `blueprint/skills/sqlite-query/`; the actual files live at `blueprint/skills/sqlite-query/` relative to the working folder. The diagram would send an operator looking in `blueprint/template/skills/` (which does not exist) rather than `blueprint/skills/`. Low severity because the ops files reference the correct path, but the directory diagram is the most-read orientation artifact.

---

## 3. Non-findings (considered and dismissed)

- **Cold-start total `~6,330`** — consistent with token-reference math (6,250 + 80). ✓
- **`!! ready` total `~7,280`** — consistent (6,250 + 80 + 950). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — calculation checks out against current token-reference component values. ✓
- **`ingest.md` atomic ordering** — Step 5 `ts` pre-compute, Step 6 `mv`, Step 7 source-page write; ordering intact. ✓
- **`ingest.md` hash canonicalization pipeline** — 6-step pipeline (preamble-strip → CRLF normalize → whitespace collapse → blank-line collapse → trim → SHA-256[:8]) intact. ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently in `template/CLAUDE.md:58–72` and `README.md`. ✓
- **Blueprint Sync Rule matrix** — 12 rows intact; no new untriggered changes detected beyond those named in W3. ✓
- **sqlite-query skill functional correctness** — schema creation, upsert pattern, bidirectional-relation INSERT OR IGNORE, and exception-based fallback all appear correct. ✓
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form (portable GNU/BSD); 3-argument form correctly avoided. ✓
- **`ops/audit.md` scope parenthetical** — "currently `refresh-hot.md`" is now accurate given `changelog-monitor.md` removal, though no note explains the removal. Not flagged as a bug.
- **`ROADMAP.md`** — lightweight planning doc, no logic content, not in audit scope.
- **`LICENSE`** — MIT, no issues.
- **`.gitignore`** — 65 chars, correct entries.

---

## 4. Questions for Clarification

**Q1 — Was `changelog-monitor.md` intentionally deprecated, or accidentally dropped?**

The file was present in audit #10 (read at 5,542 chars, documented at ~8,500/~2,130 in v2.0.10). It is now absent from the template directory, removed from the token-reference table, and removed from the setup-guide step 2 copy table — suggesting intentional deprecation. If intentional, the CHANGELOG entry for v2.0.11 (see W3) should explain the rationale so future operators know the feature was deliberate, not accidentally lost. If unintentional, the file needs to be restored.

---

## 5. Architectural Invariants Verified

All invariants checked against source files during this audit. Items 1–10 from audit #10 are re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match with no state change. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 write source page. ✓
4. `Pages: N` is derived (count of `^- [[` lines), never stored. ✓
5. Blueprint-authoring Mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md` step 5. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md` and `README.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md:71` envelope declared to derive from its Tokens column. ✓ (invariant structurally intact; source-of-truth violated in practice by CHANGELOG.md omission — see W2)
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < 3%), envelope cushion floor (cushion < 2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. ✓

New invariant added this cycle:
11. sqlite-query skill follows Query Layer Hook Contract and Ingest Hook Contract in `ops/conventions.md`. Exception-based fallback in `query-layer.md` is correctly wired. ✓

---

## 6. Verdict

**The v2.0.10 blueprint has two WARNING-class documentation gaps and three STYLE-class recalibration overruns.**

No CRITICAL findings. No architectural regressions. The ingest pipeline, approval flow, hash canonicalization, Blueprint Sync Rule, and Recalibration Rule are all structurally intact. The sqlite-query skill integrates correctly with the hook contracts.

The three warnings are interconnected. A single recalibration pass on 2026-04-19 changed the headroom convention from 110% to 125%, recalibrated all file sizes, added the sqlite-query skill rows, removed `changelog-monitor.md`, and removed `CHANGELOG.md` from the table — without a CHANGELOG entry for any of it (W3). The CHANGELOG.md omission from the table (W2) is the most consequential consequence: the `!! audit all` envelope is no longer derivable from the table as documented, and the real cushion is 3.5% rather than the apparent 29%. W1 (CLAUDE.md self-cost quote stale at ~5,500 vs. documented ~6,250) is the same cascade-miss class caught in audits #6 and #8 and is a one-line fix.

**Priority order for follow-up:**

1. **W3** — Write CHANGELOG entry (v2.0.11) to document the sqlite-query skill addition, headroom convention change, changelog-monitor.md removal, and recalibration. This anchors the audit trail and unblocks the W2 fix.
2. **W2** — Re-add `blueprint/CHANGELOG.md` to token-reference (at ~69,100/~17,275); widen envelope to `~30,000–58,000`; cascade to `ops/audit.md:71` and `user-guide.md`.
3. **W1** — Update `template/CLAUDE.md:9` from `~5,500 tokens` to `~6,250 tokens`.
4. **S1** — Recalibrate three overrun files (`ops/query.md`, `ops/update.md`, `ops/conventions.md`).
5. **S2** — Correct directory structure diagram in `template/CLAUDE.md` to show skills at `blueprint/skills/`, not `template/skills/`.

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
