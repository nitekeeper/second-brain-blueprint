# Blueprint Audit Report — 2026-04-19 (#18)

**Scope:** `!! audit all` — every tracked file under the blueprint root
**Schema under audit:** v2.0.14 (per CHANGELOG.md; no later entry found)
**Prior audits reviewed:** #11–#17 (`audit-report-2026-04-19-01.md` through `audit-report-2026-04-19-07.md`) — read in full before this pass per user instruction
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
- `CHANGELOG.md` (67,651 chars)
- `LICENSE` (1,067 chars)
- `.gitignore` (65 chars)

**Template**

- `template/CLAUDE.md` (20,641 chars)
- `template/scheduled-tasks/refresh-hot.md` (3,966 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,858 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/query.md` (2,586 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars)
- `template/scheduled-tasks/ops/audit.md` (6,581 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,797 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (4,185 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,533 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,838 chars)

**Not in audit scope:** `blueprint/` sub-directory internals (working-folder-level installed files), `ROADMAP.md` (planning doc, no logic content).

---

### 1.2 Verification that audit #17 findings are clean and v2.0.14 changes are consistent

Audit #17 left the blueprint with one STYLE finding (S1: CHANGELOG.md approaching soft trigger). Between audit #17 and this pass, schema v2.0.14 was applied. Direct re-verification:

| Item | Claim | Re-verified |
|---|---|---|
| #17 S1 | CHANGELOG.md soft trigger was expected to fire within 1–2 cycles | ✓ v2.0.14 recalibration corrected it (new threshold and envelope) |
| v2.0.14 | Soft trigger raised from ~3% to ~25% in `token-reference.md` Recalibration Rule | ✓ confirmed |
| v2.0.14 | 11 files recalibrated; Chars/Tokens column updates in `token-reference.md` | ✓ confirmed |
| v2.0.14 | `template/CLAUDE.md:9` updated from ~6,250 to ~6,450 tokens | ✓ line 9 reads `~6,450 tokens` |
| v2.0.14 | Cold-start totals: ~6,330 → ~6,530; ~7,280 → ~7,480 | ✓ CLAUDE.md:17, user-guide.md, README.md |
| v2.0.14 | Envelope widened from ~58,000 to ~64,000 | ✓ ops/audit.md:72, user-guide.md cost table and description |
| CHANGELOG | v2.0.14 entry present and documents all four changes above | ✓ lines 6–62 |
| All #11–#17 prior fixes | Verified in prior pass; no regressions found | ✓ spot-checked |

No regressions from v2.0.14 detected on the above items.

---

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Current convention per `token-reference.md` (v2.0.14): **~125% of measured actual at calibration**, rounded to nearest 100. Soft trigger: fires when remaining headroom drops below ~25% of measured actual (= any growth from calibration size). Hard trigger: fires when measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom % of measured | Flag |
|---|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | ok |
| `setup-guide.md` | 10,564 | ~13,200 | 24.9% | ⚠️ soft |
| `user-guide.md` | 14,219 | ~17,800 | 25.2% | ok |
| `troubleshooting.md` | 21,536 | ~27,300 | 26.8% | ok |
| `CHANGELOG.md` | 67,651 | ~84,600 | 25.1% | ok |
| `LICENSE` | 1,067 | ~1,400 | 31.2% | ok |
| `template/CLAUDE.md` | 20,641 | ~25,800 | 25.0% | ok (at threshold) |
| `refresh-hot.md` | 3,966 | ~5,100 | 28.6% | ok |
| `ops/ingest.md` | 15,858 | ~19,800 | 24.9% | ⚠️ soft |
| `ops/lint.md` | 2,507 | ~3,100 | 23.7% | ⚠️ soft |
| `ops/query.md` | 2,586 | ~3,300 | 27.6% | ok |
| `ops/update.md` | 1,881 | ~2,400 | 27.6% | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 24.6% | ⚠️ soft |
| `ops/audit.md` | 6,581 | ~8,200 | 24.6% | ⚠️ soft |
| `ops/token-reference.md` | 6,797 | ~8,500 | 25.1% | ok |
| `skills/sqlite-query/SKILL.md` | 4,185 | ~5,200 | 24.2% | ⚠️ soft |
| `skills/sqlite-query/query-layer.md` | 2,533 | ~3,200 | 26.3% | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,838 | ~3,500 | 23.3% | ⚠️ soft |

No hard triggers (measured ≥ documented). Seven soft triggers active — see S1.

---

### 1.4 Envelope check (Recalibration Rule Step 5)

Documented rows sum from `token-reference.md`:

| Group | Tokens |
|---|---:|
| Blueprint-doc (README 1,500 + setup-guide 3,300 + user-guide 4,450 + troubleshooting 6,830 + CHANGELOG 21,150 + LICENSE 350) | 37,580 |
| Template-side (CLAUDE 6,450 + refresh-hot 1,280 + ingest 4,950 + lint 780 + query 830 + update 600 + conventions 2,100 + audit 2,050 + token-reference 2,120) | 21,160 |
| Skill rows (SKILL.md 1,300 + query-layer 800 + ingest-hook 880) | 2,980 |
| **Total** | **61,720** |

Envelope: `~30,000–64,000` (per `ops/audit.md:72`).
Cushion: 64,000 − 61,720 = **2,280 tokens (3.6%)**. Above the 2% floor (1,280 tokens). No envelope widening required.

---

### 1.5 Cross-reference sanity checks

- `template/CLAUDE.md:9` cold-start self-cost `~6,450` = token-reference CLAUDE.md row (`~25,800 / ~6,450`). ✓
- `template/CLAUDE.md:17` cold-start total `~6,530` = 6,450 + 80 (hot.md). ✓
- `template/CLAUDE.md:17` `!! ready` total `~7,480` = 6,530 + 950 (memory.md full). ✓
- `user-guide.md:9` CLAUDE.md cost `~6,450` — matches token-reference row. ✓
- `user-guide.md:14` cold-start `~6,530` — consistent with CLAUDE.md:17. ✓
- `user-guide.md:94` and `:201` audit-all `~30,000–64,000` — matches `ops/audit.md:72`. ✓
- `user-guide.md` table: cold-start `~6,530`, with `!! ready` `~7,480` — matches CLAUDE.md:17. ✓
- `user-guide.md` `!! wrap` realistic `~3,000` / `!! ready` realistic `~3,300` — derivable from current token-reference component values (refresh-hot 1,280 + index 250 + log-tail 625 + log-append 100 + memory-write ~750 ≈ 3,005 ≈ ~3,000; +950 memory-read −750 write +50 wipe ≈ 3,255 ≈ ~3,300). ✓
- `README.md:72` cold-start `~6,530` — matches CLAUDE.md:17. ✓
- `ops/audit.md:72` envelope `~30,000–64,000` — consistent with token-reference sum (61,720). ✓
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:70–72`, `README.md:73`, and `user-guide.md:175`. ✓
- Blueprint Sync Rule 12-row matrix — intact. ✓
- Versioning split (`Schema version: 2.0` in CLAUDE.md footer; patch bumps X.Y.Z in CHANGELOG only) — consistent. ✓
- Ingest atomic ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
- Hash canonicalization 6-step pipeline intact in `ops/ingest.md §Hash Canonicalization`. ✓
- `ops/ingest.md` B5 per-file step list `[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]` — confirmed. ✓
- Blueprint-authoring mode guard present in `template/CLAUDE.md`, `ops/audit.md:44`, `!! ready` step 5. ✓
- `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading. ✓
- `query-layer.md` uses `find`-based path resolution — satisfies Query Layer Hook Contract. ✓
- `ingest-hook.md` exception handler and Notes section second bullet — both point to `!! install sqlite-query` repair path. ✓
- `ops/conventions.md` Query Layer Hook Contract explicitly prohibits glob patterns. ✓
- `ops/update.md` Step 5.5 ingest-hook call — present and correct. ✓
- `ops/audit.md:23` scope parenthetical "currently `refresh-hot.md`" — accurate after `changelog-monitor.md` removal (v2.0.11). ✓
- `.gitignore` — 65 chars; `.obsidian/`, `.idea/`, `.DS_Store` entries; scoped to inside `blueprint/`. ✓
- **`ops/token-reference.md` header self-cost note says `~2,080 tokens`; table row shows `~2,120 tokens`.** ⚠️ (see W1)
- **`ops/ingest.md` Hash Canonicalization final paragraph cross-references `troubleshooting.md "Changelog monitor reports 🆕 for a page I know hasn't changed"` — entry does not exist in `troubleshooting.md`.** ⚠️ (see W2)

---

## 2. Findings

### CRITICAL

None.

### WARNING

**W1 — `ops/token-reference.md` self-cost note in the header cites stale `~2,080 tokens`; the Tokens column in the table below shows `~2,120`. Cascade miss from v2.0.14 recalibration.**

*Evidence.*

`ops/token-reference.md` header (line 8):
> "Self-cost note: This file itself is **~2,080 tokens** to read. Every approval request requires reading it unless the relevant numbers are already cached in working memory from earlier in the same operation. Include the **~2,080-token** cost in quoted estimates for the first approval of an operation…"

`ops/token-reference.md` File Read Costs table (line 29):
> `| ops/token-reference.md | ~8,500 | ~2,120 |`

*Logical failure.* The v2.0.14 recalibration pass updated the `ops/token-reference.md` row from `~8,300 / ~2,080` to `~8,500 / ~2,120` — reflecting the file's measured growth. However, the self-cost note in the header was not updated; it still cites `~2,080`. The header explicitly directs agents to include `~2,080` in approval estimates, while the table (the declared source of truth) says `~2,120`. The two self-references disagree by 40 tokens per approval request.

This is the same cascade-miss class caught in audit #11 W1 (`template/CLAUDE.md:9` stale self-cost after recalibration), audit #6 W1, and audit #8 W1 — a per-file recalibration number that doesn't propagate to the file's own header self-reference. The v2.0.14 entry documents the recalibration of `ops/token-reference.md` but the cascade row (update the self-cost note) was not applied.

*Recommended fix.* Update the two occurrences of `~2,080` in the header self-cost note to `~2,120`. One-paragraph change; no other file depends on the header paragraph (downstream docs cite only the table Tokens column).

---

**W2 — `ops/ingest.md` Hash Canonicalization section cross-references `troubleshooting.md "Changelog monitor reports 🆕 for a page I know hasn't changed"` — this troubleshooting entry does not exist.**

*Evidence.*

`ops/ingest.md` §Hash Canonicalization, final paragraph:
> "…or LLM-based WebFetch prose rewriting — all of which will correctly produce hash mismatches. See `troubleshooting.md` 'Changelog monitor reports 🆕 for a page I know hasn't changed' for the LLM-WebFetch caveat."

`troubleshooting.md` — all twenty section headings reviewed: no entry matching "Changelog monitor" or "🆕" exists. The section headings are: Obsidian tag errors, XX\* files, stray .md files at vault root, phantom graph node, agent reads full log.md on startup, agent forgot ops file, stale wiki/raw/ folder, session ended before !! wrap, !! ready mid-session wipe, !! wrap overwrote summary, memory.md appears truncated, !! wrap/!! ready paused for approval, !! ingest all approval promised pages speculatively, edited .gitignore and nothing changed, !! audit [wiki-page] returns no match, source page regenerated on every ingest, ingest interrupted mid-flight, raw/ keeps growing, force re-ingest an unchanged source, Bulk Edits Reference.

*Logical failure.* `changelog-monitor.md` was a scheduled task retired in v2.0.11. The troubleshooting entry it referenced — presumably intended to document why the monitor would report 🆕 for a page that hadn't actually changed (LLM-based WebFetch prose rewriting causes a hash mismatch between Clipper-saved and URL-fetched versions of the same source) — was either never created or was removed alongside the feature. The cross-reference in `ops/ingest.md` was not cleaned up.

An operator or user reading the Hash Canonicalization section and following the cross-reference gets a dead end: no matching troubleshooting entry exists. The LLM-WebFetch caveat itself — that prose rewriting during URL fetch produces hash mismatches that look like content changes — is a legitimate and practically important warning. It is currently undocumented in `troubleshooting.md`.

This cross-reference was present in `ops/ingest.md` throughout today's audit series (#11–#17) at 15,852–15,858 chars and was not flagged by any prior pass.

*Recommended fix.* Two options:

(a) **Add the troubleshooting entry.** Create a new section in `troubleshooting.md` titled "Source page gets regenerated repeatedly despite no real content change / URL ingest" (or matching the literal cross-reference slug if one can be inferred) documenting: Symptom (source page regenerated on every URL ingest despite identical underlying content), Cause (LLM-based WebFetch prose rewriting produces a different hash each time even when the article body hasn't changed), Fix (switch to Obsidian Web Clipper for that source — the Clipper saves verbatim markdown that canonicalizes consistently; alternatively accept the hash drift and allow the regeneration), Prevention (prefer Clipper ingest for frequently-changing or LLM-rendered sources). Blueprint Sync Rule "New known issue or fix" row applies.

(b) **Remove the cross-reference.** Update the final sentence of `ops/ingest.md` §Hash Canonicalization to note the LLM-WebFetch caveat inline rather than pointing to a non-existent troubleshooting entry. Simpler, but loses the discoverability benefit of a troubleshooting-section entry for a real operational issue.

Option (a) is preferred — the issue is real, practically encountered, and warrants its own entry. Either fix lands in a single CHANGELOG entry; "New known issue or fix" cascade row from Blueprint Sync Rule applies.

---

### STYLE

**S1 — Seven files fire the soft recalibration trigger (headroom < ~25% of measured actual) per the v2.0.14 threshold.**

Files and headroom percentages: `setup-guide.md` (24.9%), `ops/ingest.md` (24.9%), `ops/lint.md` (23.7%), `ops/conventions.md` (24.6%), `ops/audit.md` (24.6%), `SKILL.md` (24.2%), `ingest-hook.md` (23.3%).

All seven have grown past their v2.0.14 calibration sizes. At the new 25% threshold, any post-calibration growth fires the soft trigger — this is the intended behavior (the rule says "catches drift before it hard-fires mid-op" and "recalibrate after every INGEST operation as a routine pass").

Critical observation: **for all seven files, 125% × current measured rounds to the same documented Chars value as the v2.0.14 calibration.** Recalibration produces no column changes:

| File | Measured | 125% × measured | Rounds to | Doc. Chars | Change? |
|---|---:|---:|---:|---:|:---:|
| `setup-guide.md` | 10,564 | 13,205 | ~13,200 | ~13,200 | none |
| `ops/ingest.md` | 15,858 | 19,823 | ~19,800 | ~19,800 | none |
| `ops/lint.md` | 2,507 | 3,134 | ~3,100 | ~3,100 | none |
| `ops/conventions.md` | 6,741 | 8,426 | ~8,400 | ~8,400 | none |
| `ops/audit.md` | 6,581 | 8,226 | ~8,200 | ~8,200 | none |
| `SKILL.md` | 4,185 | 5,231 | ~5,200 | ~5,200 | none |
| `ingest-hook.md` | 2,838 | 3,548 | ~3,500 | ~3,500 | none |

No Chars-column updates required. The soft trigger is correctly firing per the new rule; no action beyond noting is necessary. If a formal recalibration pass is run, the calibration date in the header should be refreshed, but the numeric values stay the same.

---

## 3. Non-findings (considered and dismissed)

- **Cold-start total `~6,530`** — 6,450 (CLAUDE.md) + 80 (hot.md). ✓
- **`!! ready` total `~7,480`** — 6,530 + 950 (memory.md full). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — derivable from current token-reference component values. ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
- **Ingest atomic ordering** — Step 5 pre-compute → Step 6 mv → Step 7 page write. ✓
- **Hash canonicalization 6-step pipeline** — intact. ✓
- **`Pages: N` derived** — `refresh-hot.md` counts `^- [[` entries; not a stored counter. ✓
- **Blueprint-authoring mode guard** — present in CLAUDE.md, audit.md, `!! ready` step 5. ✓
- **Blueprint Sync Rule 12-row matrix** — intact; no new untriggered changes detected beyond W1 and W2. ✓
- **`SKILL.md` install/uninstall symmetry** — file targets match; DB-keep option on uninstall correctly defaults to no. ✓
- **sqlite-query DB schema** — `pages` table, `relations` table, four indexes; `type` CHECK constraint; upsert pattern and bidirectional-relation `INSERT OR IGNORE` all correct. ✓
- **`query-layer.md` `find`-based path resolution** — correctly implemented; unmatched slugs silently skipped, triggering grep fallback. ✓
- **`ingest-hook.md` `type_` / `type` naming** — `type_` is the Python variable (reserved-word avoidance); `type` is the SQL column name; correctly threaded through the upsert. ✓
- **`ingest-hook.md` Notes section** — second bullet now correctly points to `!! install sqlite-query` repair path (v2.0.13 W1 fix). ✓
- **`ops/ingest.md` B5 step enumeration** — `11.5` present in per-file list (v2.0.13 W2 fix). ✓
- **`ops/update.md` Step 5.5** — ingest-hook call present; non-fatal error handling consistent with hook contract. ✓
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form only; 3-argument GNU-awk form correctly avoided. ✓
- **`setup-guide.md` template/CLAUDE.md placeholder and Setup Note block** — `[created-date]` / `[updated-date]` and the `> **Setup note:**` block are intentional template scaffolding, removed during `!! setup`. Not a defect in blueprint-authoring mode. ✓
- **v2.0.14 CHANGELOG envelope arithmetic** — blueprint-doc (37,580) + template-side (21,160) + skill (2,980) = 61,720. Cushion 2,280 tokens (3.6% of 64,000). ✓
- **v2.0.14 recalibration list completeness** — CHANGELOG lists 11 files recalibrated; cross-checked against token-reference.md rows: all 11 match. Files excluded from recalibration (headroom ≥ 25%) listed and verified. ✓
- **`ops/audit.md` envelope history note** — lists v2.0.6, v2.0.7, v2.0.9, v2.0.10, v2.0.11, v2.0.14 as widening events; v2.0.12 and v2.0.13 correctly omitted (neither widened the envelope). ✓
- **`ROADMAP.md`** — planning doc; not in audit scope.
- **`LICENSE`** — MIT; no issues.
- **`.gitignore`** — 65 chars; `.obsidian/`, `.idea/`, `.DS_Store`. Scoped to inside `blueprint/`; setup-guide.md correctly explains this does not govern `wiki/.obsidian/`. ✓

---

## 4. Questions for Clarification

**Q1 — Was the "Changelog monitor reports 🆕" troubleshooting entry ever drafted, or was the cross-reference always a forward-reference to an entry that was planned but never written?**

The answer affects which W2 fix option is preferable. If the entry was drafted and then lost when `changelog-monitor.md` was retired, recovering its content (from memory or git history) is faster than writing it from scratch. If it was always a forward-reference, option (a) requires writing the entry fresh. Either way, the cross-reference must be resolved.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#17 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:44`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md:72` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~25% of measured actual — updated v2.0.14), envelope cushion floor (cushion < ~2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. ✓
11. sqlite-query skill follows Query Layer Hook Contract (no glob patterns, `find`-based resolution) and Ingest Hook Contract (non-fatal errors, consistent repair messaging across exception handler, Notes section, and `SKILL.md §Fallback Behaviour`). ✓ fully satisfied.

---

## 6. Verdict

**The v2.0.14 blueprint has two WARNING-class findings and one STYLE note. No CRITICAL findings. No architectural regressions.**

The ingest pipeline, approval flow, hash canonicalization, Blueprint Sync Rule, Recalibration Rule, and all sqlite-query hook contracts are fully intact. The v2.0.14 recalibration is internally consistent: all token figures cross-reference correctly, the envelope derivation from the table matches `ops/audit.md:72`, and the CHANGELOG entry documents all four changes (threshold raise, full recalibration pass, cold-start cascade, envelope widening).

W1 is the same cascade-miss class as audit #11 W1 and multiple prior cycles — a self-referencing file whose header self-cost note wasn't updated when the table row was recalibrated. W2 is a dangling cross-reference to a troubleshooting entry that doesn't exist, surviving undetected through all 7 prior audits today — the LLM-WebFetch caveat it references is real and the entry is worth creating.

**Priority order for follow-up:**

1. **W1** — Update `ops/token-reference.md` header self-cost note from `~2,080 tokens` to `~2,120 tokens` (two occurrences). One-paragraph fix; prevents approval-estimate undercounting.
2. **W2** — Either (a) add a troubleshooting entry documenting the LLM-WebFetch prose-rewriting hash-mismatch caveat and update the cross-reference in `ops/ingest.md` to match, or (b) remove the cross-reference and document the caveat inline. Option (a) preferred. Blueprint Sync Rule "New known issue or fix" cascade applies.
3. **S1** — No action required; soft triggers are borderline and recalibration produces no value changes.

Both W1 and W2 can land in a single CHANGELOG patch (v2.0.15). W2's troubleshooting entry addition triggers the "New known issue or fix" Blueprint Sync row; W1 triggers the "File-size or cost change" row (ops/token-reference.md self-cost update). No envelope change is needed.

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
