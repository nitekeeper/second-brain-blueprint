# Blueprint Audit Report — 2026-04-19 (#17)

**Scope:** `!! audit all` — every tracked file under the blueprint root
**Schema under audit:** v2.0.13 (per CHANGELOG.md; no later entry found)
**Prior audits reviewed:** #11–#16 (`audit-report-2026-04-19-01.md` through `audit-report-2026-04-19-06.md`) — read in full before this pass per user instruction
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
- `CHANGELOG.md` (64,280 chars)
- `LICENSE` (1,067 chars)

**Template**

- `template/CLAUDE.md` (20,641 chars)
- `template/scheduled-tasks/refresh-hot.md` (3,966 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,858 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/query.md` (2,586 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars)
- `template/scheduled-tasks/ops/audit.md` (6,572 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,796 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (4,185 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,533 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,838 chars)

**Not in audit scope:** `blueprint/` sub-directory internals (working-folder-level installed files), `ROADMAP.md` (planning doc, no logic content).

---

### 1.2 Verification that audit #16 findings are clean

Audit #16 was a fix-verification pass confirming both audit #15 findings (W1, W2) were applied in v2.0.13. Direct re-verification:

| Fix | Claim | Re-verified |
|---|---|---|
| W1 | `ingest-hook.md` Notes section → points to `!! install sqlite-query` | ✓ line 76: "To repair: say `!! install sqlite-query` and choose yes to the backfill offer, or `!! uninstall sqlite-query` to revert to grep." |
| W2 | `ops/ingest.md` B5 per-file step list → `[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]` | ✓ confirmed in B5 preamble |

No regressions from #16. Schema v2.0.13 findings baseline is clean.

---

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Current convention per `token-reference.md`: **~125% of measured actual at calibration**, rounded to nearest 100.

| File | Measured (`wc -c`) | Doc. Chars | Headroom | Flag |
|---|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | ok |
| `setup-guide.md` | 10,564 | ~12,800 | 17.5% | ok |
| `user-guide.md` | 14,219 | ~17,100 | 16.9% | ok |
| `troubleshooting.md` | 21,536 | ~27,300 | 21.1% | ok |
| `CHANGELOG.md` | 64,280 | ~69,100 | 6.97% | ⚠️ approaching soft trigger (see S1) |
| `LICENSE` | 1,067 | ~1,400 | 23.8% | ok |
| `template/CLAUDE.md` | 20,641 | ~25,000 | 17.4% | ok |
| `refresh-hot.md` | 3,966 | ~5,100 | 22.2% | ok |
| `ops/ingest.md` | 15,858 | ~18,600 | 14.7% | ok |
| `ops/lint.md` | 2,507 | ~2,900 | 13.6% | ok |
| `ops/query.md` | 2,586 | ~3,300 | 21.6% | ok |
| `ops/update.md` | 1,881 | ~2,400 | 21.6% | ok |
| `ops/conventions.md` | 6,741 | ~8,000 | 15.7% | ok |
| `ops/audit.md` | 6,572 | ~8,200 | 20.1% | ok |
| `ops/token-reference.md` | 6,796 | ~8,300 | 18.1% | ok |
| `skills/sqlite-query/SKILL.md` | 4,185 | ~4,700 | 11.0% | ok |
| `skills/sqlite-query/query-layer.md` | 2,533 | ~3,200 | 20.8% | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,838 | ~3,300 | 14.0% | ok |

No hard triggers (measured ≥ documented). No soft triggers currently active (see S1 for pre-emptive note on CHANGELOG.md).

---

### 1.4 Envelope check (Recalibration Rule Step 5)

Documented rows sum from `token-reference.md` (unchanged since audit #16):

| Group | Tokens |
|---|---:|
| Blueprint-doc (README 1,500 + setup-guide 3,200 + user-guide 4,280 + troubleshooting 6,830 + CHANGELOG 17,275 + LICENSE 350) | 33,435 |
| Template-side (CLAUDE 6,250 + refresh-hot 1,280 + ingest 4,650 + lint 730 + query 830 + update 600 + conventions 2,000 + audit 2,050 + token-reference 2,080) | 20,470 |
| Skill rows (SKILL.md 1,180 + query-layer 800 + ingest-hook 830) | 2,810 |
| **Total** | **56,715** |

Cushion: 58,000 − 56,715 = **1,285 tokens (2.2%)**. Above the 2% floor (1,160 tokens). No envelope widening required.

---

### 1.5 Cross-reference sanity checks

- `template/CLAUDE.md:9` cold-start self-cost `~6,250` = token-reference CLAUDE.md row. ✓
- `template/CLAUDE.md:17` cold-start total `~6,330` = 6,250 + 80 (hot.md). ✓
- `template/CLAUDE.md:17` `!! ready` total `~7,280` = 6,330 + 950 (memory.md full). ✓
- `user-guide.md:9` CLAUDE.md cost `~6,250` — matches token-reference row. ✓
- `user-guide.md:14` cold-start prose `~6,330` — consistent with CLAUDE.md line 17. ✓
- `user-guide.md:201` audit all `~30,000–58,000` — matches `ops/audit.md:72`. ✓
- `user-guide.md` realistic `!! wrap` `~3,000` / `!! ready` `~3,300` — derivable from current token-reference component values. ✓
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:70–72`, `README.md:73`, and `user-guide.md:175`. ✓
- Blueprint Sync Rule 12-row matrix — intact. ✓
- Versioning split (major.minor in footer + hot.md; patches in CHANGELOG only) — documented and consistent. ✓
- `ops/ingest.md` B5 per-file step list `[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]` — confirmed. ✓
- Ingest atomic ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
- Hash canonicalization 6-step pipeline intact in `ops/ingest.md §Hash Canonicalization`. ✓
- Blueprint-authoring mode guard present in `template/CLAUDE.md`, `ops/audit.md:44`, and `!! ready` step 5 footnote. ✓
- `SKILL.md` install step 4 file copy targets (`scheduled-tasks/query-layer.md`, `scheduled-tasks/ingest-hook.md`) match `CLAUDE.md` directory structure. ✓
- `SKILL.md` uninstall targets match install targets. ✓
- `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading "## Step 4.5 — Offer SQLite Query Skill". ✓
- `query-layer.md` uses `find`-based path resolution (`subprocess.run(["find", pages_dir, "-name", f"{row[0]}.md"])`) — satisfies Query Layer Hook Contract. ✓
- `ingest-hook.md` exception handler points to correct repair path (`!! install sqlite-query`). ✓
- `ingest-hook.md` Notes section second bullet: correct repair path. ✓
- `ops/conventions.md` Query Layer Hook Contract explicitly prohibits glob patterns, documents `find`-via-subprocess requirement. ✓
- `ops/audit.md:23` scope parenthetical "currently `refresh-hot.md`" — accurate since `changelog-monitor.md` removal (v2.0.11). ✓
- `ops/update.md` Step 5.5 ingest-hook call present and correct. ✓

---

## 2. Findings

### CRITICAL

None.

### WARNING

None.

### STYLE

**S1 — `blueprint/CHANGELOG.md` is approaching the soft recalibration trigger and will likely cross it within 1–2 more audit passes.**

*Evidence.*

Soft trigger condition (from `token-reference.md` Recalibration Rule):
> "Fire pre-emptively when any file's remaining headroom drops below ~3% of its measured actual."

Current state:
- Measured: 64,280 chars
- Documented: ~69,100 chars
- Remaining headroom: 4,820 chars
- Soft trigger threshold: 3% × 64,280 = **1,928 chars**
- Current headroom (4,820) is above the threshold (1,928) → **not triggered today**

Soft trigger fires when measured exceeds **67,087 chars** (derived: 69,100 / 1.03). Gap from current: **2,807 chars**.

*Growth rate.* Audit #12 verification raised CHANGELOG.md from ~59,139 to ~62,089, adding ~2,950 chars. Audit #14 verification raised it from 62,089 to 64,280, adding ~2,191 chars. Average per audit-fix-verification cycle: ~2,500 chars. At that rate, the soft trigger fires approximately one full audit-and-verification cycle from now.

*Impact.* No action required today — the trigger has not fired. Documenting here so the next audit is primed to check CHANGELOG.md first and recalibrate proactively rather than discovering a mid-op hard trigger. Recommended recalibration when the soft trigger fires: 67,087 × 1.25 = 83,859 → **~83,900 chars / ~20,975 tokens**. This would raise the blueprint-doc row sum from 33,435 to ~37,135 tokens, pushing the table total to ~60,415 — exceeding the current 58,000 envelope upper bound. Plan for the cascade at that time: widen envelope (60,415 + ~1,500–3,000 cushion → **~62,000–64,000**) and cascade to `ops/audit.md:72`, `user-guide.md:94`, and `user-guide.md:201`.

*No fix required now.*

---

## 3. Non-findings (considered and dismissed)

- **Cold-start total `~6,330`** — 6,250 (CLAUDE.md) + 80 (hot.md). ✓
- **`!! ready` total `~7,280`** — 6,330 + 950 (memory.md full). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — derivable from current token-reference component values. ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
- **Ingest atomic ordering** — Step 5 pre-compute → Step 6 mv → Step 7 page write. ✓
- **Hash canonicalization 6-step pipeline** — intact. ✓
- **`Pages: N` derived** — `refresh-hot.md` counts `^- [[` entries; not a stored counter. ✓
- **Blueprint-authoring mode guard** — present in CLAUDE.md, audit.md, `!! ready` step 5. ✓
- **Blueprint Sync Rule 12-row matrix** — intact; no new untriggered changes detected. ✓
- **`SKILL.md` install/uninstall symmetry** — file targets match; DB-keep option on uninstall correctly defaults to no. ✓
- **sqlite-query DB schema** — `pages` table, `relations` table, four indexes; `type` CHECK constraint; upsert pattern and bidirectional-relation `INSERT OR IGNORE` all correct. ✓
- **`query-layer.md` `find`-based path resolution** — correctly implemented; unmatched slugs silently skipped, triggering grep fallback. ✓
- **`query-layer.md` potential multi-result from `find`.** If two files shared the same slug across different `wiki/pages/` subdirectories, `result.stdout.strip()` would contain a newline, producing an unreadable path. However, slug uniqueness is a core wiki invariant enforced by conventions and lint — duplicate slugs represent a pre-existing broken state, not a new code defect. The resulting failed read safely degrades to the grep fallback. Not flagged.
- **`ingest-hook.md` `type_` / `type` naming** — `type_` is the Python variable (reserved-word avoidance); `type` is the SQL column name; correctly threaded through the upsert. ✓
- **`ingest-hook.md` Notes section** — W1 fix from audit #15 confirmed correct in both the Notes bullet and the exception handler. ✓
- **`ops/ingest.md` B5 step enumeration** — W2 fix from audit #15 confirmed; `11.5` present in per-file list. ✓
- **`ops/update.md` Step 5.5** — ingest-hook call present, non-fatal error handling consistent with hook contract. ✓
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form only; 3-argument GNU-awk form correctly avoided. ✓
- **`refresh-hot.md` full log.md read** — reads full log for `Gaps:` extraction; documented as unbounded in token-reference and intentional. Not flagged.
- **`setup-guide.md` Step 7 checklist** — does not include conditional sqlite-query files (`scheduled-tasks/query-layer.md`, `scheduled-tasks/ingest-hook.md`). Coverage gap is minor: SKILL.md Step 6 provides its own confirmation, and the files are only present if the optional Step 4.5 was accepted. Not flagged.
- **`.gitignore` scope** — correctly scopes to inside `blueprint/`; setup-guide.md note accurately explains that `wiki/.obsidian/` is outside its reach. ✓
- **`ops/audit.md` scope parenthetical** — "currently `refresh-hot.md`" accurate after `changelog-monitor.md` removal (v2.0.11). ✓
- **CHANGELOG.md v2.0.13 entry** — complete; covers both W1 and W2 from audit #15; includes post-fix headroom table. ✓
- **Envelope cushion 2.2%** — above the 2% floor; no widening needed at current file sizes. ✓
- **`ROADMAP.md`** — planning doc; not in audit scope.
- **`LICENSE`** — MIT; no issues.

---

## 4. Questions for Clarification

None. All findings are self-contained.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#16 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:44`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md:72` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < 3% of measured actual), envelope cushion floor (cushion < 2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. ✓
11. sqlite-query skill follows Query Layer Hook Contract (no glob patterns, `find`-based resolution) and Ingest Hook Contract (non-fatal errors, consistent repair messaging across exception handler, Notes section, and `SKILL.md §Fallback Behaviour`). ✓ fully satisfied.

---

## 6. Verdict

**The v2.0.13 blueprint has no CRITICAL or WARNING findings. One STYLE note: `blueprint/CHANGELOG.md` is approaching the soft recalibration trigger and will likely cross it within the next 1–2 audit passes.**

No architectural regressions. All prior findings from audits #11–#16 are verified clean. The ingest pipeline, approval flow, hash canonicalization, Blueprint Sync Rule, Recalibration Rule, and all three sqlite-query hook contracts are fully intact.

The single STYLE finding (S1) requires no action today. The CHANGELOG.md measured size (64,280 chars) has not yet crossed the soft trigger threshold of ~67,087 chars, but the gap is roughly one full audit-and-verification cycle of content. Flag for the next audit: check CHANGELOG.md headroom first and recalibrate proactively if the threshold is crossed. When recalibration does fire, the new documented Chars (~83,900) will push the table total above the current 58,000 envelope upper bound — plan for that cascade in advance.

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
