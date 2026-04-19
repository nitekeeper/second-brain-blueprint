# Blueprint Changelog

> Version history for the blueprint schema. See `troubleshooting.md` for specific
> symptom/cause/fix entries tied to these versions.

## v2.0.21 — 2026-04-19

### Remove CHANGELOG from `!! audit all` scope; fix v2.0.18 arithmetic residual (audit #25 — S1)

- **`blueprint/CHANGELOG.md` removed from `!! audit all` scope.** A changelog is an
  append-only log — auditing it for logic errors is not meaningful, and fixing narrative
  figures inside it is the exact pattern that created the cascade-miss class in the first
  place. Removed the `blueprint/CHANGELOG.md` line from `ops/audit.md`'s scope list.
  Removed the companion warning note (added in v2.0.19) that told the agent CHANGELOG
  was read-but-not-tracked — it is now neither read nor tracked. Cascade: `user-guide.md`
  audit cost figures updated from `~30,000–43,000+` to `~30,000–43,000` (both
  occurrences — the `+` existed solely because CHANGELOG was an unaccounted read).

- **v2.0.18 arithmetic residual corrected (S1).** Audit #25 S1 flagged that v2.0.20
  corrected the v2.0.18 narrative sentence (`"~75,346 chars (pre-entry ~73,333)"`) but
  left the adjacent arithmetic base unchanged (`75,344 × 1.25`). Corrected in-place to
  `75,346 × 1.25 = 94,182.5`. Arithmetic conclusion unchanged (~94,200). No cascade.

---

## v2.0.20 — 2026-04-19

### v2.0.18 narrative corrected; no table or cascade impact (audit #24 — S1)

- **CHANGELOG.md v2.0.18 narrative corrected.** Audit #24 S1 (carried from audit #23)
  flagged that the v2.0.18 narrative cited `"pre-entry ~73,334"` (actual: 73,333) and
  `"grew CHANGELOG.md to ~75,344 chars"` (actual: 75,346). Corrected in-place to
  `"pre-entry ~73,333"` and `"~75,346 chars"`. Fourth occurrence of the cascade-miss
  class (v2.0.15 first — 593 chars, source-of-truth impact; v2.0.17 second — 1,151 chars,
  cosmetic; v2.0.18 third — 2 chars, rounding artifact; v2.0.20 correction closes it).

- **No file-size or token-table changes.** `blueprint/CHANGELOG.md` was removed from
  `token-reference.md` in v2.0.19, so the corrected narrative figures have no calibration
  role anywhere in the system. No recalibration, no envelope change, no cold-start
  cascade required.

---

## v2.0.19 — 2026-04-19

### Remove `blueprint/CHANGELOG.md` from token-reference; add audit token warning

- **`blueprint/CHANGELOG.md` removed from `token-reference.md` tracked-files table.**
  CHANGELOG.md grows with every fix cycle and is only read during `!! audit all`,
  which is approval-exempt — tracking its size adds recalibration churn without
  protecting anything. Removed the row (~94,200 / ~23,550). New table sum: 40,820
  tokens. Envelope tightened from `~30,000–67,000` to `~30,000–43,000` (sum 40,820
  + ~2,180 cushion). Cascade: `ops/token-reference.md` (row removed, Step 5 envelope
  and floor note updated), `ops/audit.md` (envelope updated), `user-guide.md` (cost
  table and `!! audit` description updated).

- **Warning note added to `ops/audit.md`.** CHANGELOG.md is still read during every
  `!! audit all` pass but is no longer in the cost table. A note now instructs the
  agent to warn users that `!! audit all` may use significantly more tokens than the
  envelope suggests after many audit-and-fix cycles.

### Post-fix token-reference envelope

Blueprint-doc rows: README (1,500) + setup-guide (3,300) + user-guide (4,450) +
troubleshooting (7,080) + LICENSE (350) = **16,680**

Template-side rows: CLAUDE (6,450) + refresh-hot (1,280) + ingest (4,950) + lint (780) +
query (830) + update (600) + conventions (2,100) + audit (2,050) + token-reference (2,120)
= **21,160**

Skill rows: SKILL.md (1,300) + query-layer (800) + ingest-hook (880) = **2,980**

**Total ≈ 40,820 tokens** inside `~30,000–43,000`. Cushion ≈ 2,180 tokens (5.1% of
43,000 — above the 2% floor of ~860 tokens).

---

## v2.0.18 — 2026-04-19

### v2.0.17 narrative corrected; CHANGELOG.md recalibrated; envelope widened to ~30,000–67,000 (audit #22 — S1, S2)

- **v2.0.17 CHANGELOG narrative corrected (S1).** Audit #22 S1 flagged that the v2.0.17
  narrative cited the pre-entry CHANGELOG.md size (`~72,182 chars`, `22.6%` headroom)
  instead of the post-entry size. Corrected in-place to `~73,300` / `~20.7%` (+1 char).
  Same cascade-miss class as v2.0.15 → v2.0.17 retroactive fix; no token-table or
  envelope impact from the correction itself.

- **`blueprint/CHANGELOG.md` recalibrated; envelope widened (S2).** Audit #22 S2
  identified that CHANGELOG.md's measured size (73,333 chars) had grown ~4,800 chars
  above the last calibration point (~70,800), placing the next recalibration's token
  delta (+795 tokens) on a path that would breach the 2% envelope cushion floor.
  Adding v2.0.18 entry grew CHANGELOG.md to ~75,346 chars (pre-entry ~73,333).
  Recalibrated at 125%: 75,346 × 1.25 = 94,182.5 → **~94,200 / ~23,550**
  (was ~88,500 / ~22,130). New table sum ~64,370 tokens; cushion ~65,000 − 64,370 =
  630 tokens (0.97% — below the 2% floor of ~1,300). Envelope widened from
  `~30,000–65,000` to `~30,000–67,000` (sum + ~2,630 cushion = 3.93% of 67,000 —
  above the 2% floor). Cascade applied to: `ops/audit.md` Notes, `user-guide.md`
  cost table, `user-guide.md` !! audit description.

### Post-fix token-reference envelope

Blueprint-doc rows: README (1,500) + setup-guide (3,300) + user-guide (4,450) +
troubleshooting (7,080) + CHANGELOG (**23,550**) + LICENSE (350) = **40,230**

Template-side rows: CLAUDE (6,450) + refresh-hot (1,280) + ingest (4,950) + lint (780) +
query (830) + update (600) + conventions (2,100) + audit (2,050) + token-reference (2,120)
= **21,160**

Skill rows: SKILL.md (1,300) + query-layer (800) + ingest-hook (880) = **2,980**

**Total ≈ 64,370 tokens** inside `~30,000–67,000`. Cushion ≈ 2,630 tokens (3.93% of
67,000 — above the 2% floor).

---

## v2.0.17 — 2026-04-19

### Retroactive correction: v2.0.15 CHANGELOG narrative values updated (audit #21 — S1)

- **CHANGELOG v2.0.15 narrative corrected to show accurate post-recalibration values.**
  Audits #19 and #20 flagged that the v2.0.15 CHANGELOG narrative cited stale intermediate
  values — `"70,207 chars"`, `"~87,900/~21,980"`, and `"~62,800 tokens"` — that reflected
  the file size before the v2.0.15 entry itself was written, rather than the final
  post-entry measurements. The correct values are `"~70,800 chars"`, `"~88,500/~22,130"`,
  and `"~62,950 tokens"` (consistent with `ops/token-reference.md` and the post-fix
  envelope sum in the v2.0.15 entry). The correction was applied between audit #20 and
  audit #21 (+1 char, CHANGELOG.md 72,181 → 72,182). This entry documents that retroactive
  fix to close the audit trail gap identified in audit #21 S1.

- **No file-size or token-table changes.** The +1 char to CHANGELOG.md stays inside its
  existing documented headroom (~88,500 chars — current measured ~73,300, headroom ~20.7%).
  No recalibration, no envelope change, no cold-start cascade required.

---

## v2.0.16 — 2026-04-19

### Soft recalibration trigger corrected from ~25% back to ~10%

- **`ops/token-reference.md` Recalibration Rule: soft trigger threshold corrected from ~25%
  to ~10% of measured actual.**
  The v2.0.14 threshold raise from ~3% to ~25% was a one-time cleanup pass — intended to
  trigger a full recalibration of files that had accumulated significant drift. The ~25%
  value is not appropriate as a standing rule: since fresh calibration sets docs to exactly
  125% of measured (= 25% headroom), a ~25% threshold fires immediately on any post-
  calibration growth, making the soft trigger nearly indistinguishable from the hard trigger
  in practice. The correct ongoing threshold is ~10%, which gives meaningful lead time
  (soft trigger fires after ~15% of headroom has been consumed, with ~10% still remaining
  as a buffer before hard-fire). The v2.0.14 recalibration values remain in place — files
  recalibrated under the 25%-threshold pass now have generous headroom under the restored
  10% rule and do not need adjustment. No files fire the soft trigger at the corrected
  threshold.

- **No file-size or token-table changes.** All tracked files have headroom well above 10%
  (minimum 23.3% — `ingest-hook.md`). No recalibration, no envelope change, no cold-start
  cascade required.

---

## v2.0.15 — 2026-04-19

### token-reference.md self-cost note corrected; LLM-WebFetch troubleshooting entry added (audit #18 — W1, W2)

- **`ops/token-reference.md` self-cost note updated from ~2,080 to ~2,120 tokens (W1).**
  The v2.0.14 recalibration updated the `ops/token-reference.md` table row from
  `~8,300 / ~2,080` to `~8,500 / ~2,120` but did not propagate to the header's self-cost
  note, which still cited `~2,080` in two places. Agents using the header value would
  undercount the self-cost of reading `token-reference.md` by 40 tokens per approval
  request. Updated both occurrences to `~2,120`. Same cascade-miss class as audit #11 W1,
  #6 W1, and #8 W1 — a per-file recalibration number that didn't propagate to the file's
  own header self-reference.

- **New troubleshooting entry added for LLM-WebFetch prose-rewriting hash mismatches (W2).**
  `ops/ingest.md` §Hash Canonicalization referenced `troubleshooting.md "Changelog monitor
  reports 🆕 for a page I know hasn't changed"` — a dangling cross-reference present since
  at least v2.0.11 (when `changelog-monitor.md` was retired) and undetected through audits
  #11–#17. The referenced entry never existed in `troubleshooting.md`. Created new entry:
  "URL ingest keeps regenerating the same source even when the article hasn't changed" —
  documents the cause (LLM-based WebFetch prose rewriting produces different markdown on
  every call; the hash canonicalizer handles whitespace drift but not semantic rewrites) and
  fix (switch to Obsidian Web Clipper for stable hash behavior). Updated `ops/ingest.md`
  cross-reference to point at the new entry title.

- **`blueprint/troubleshooting.md` recalibrated (soft trigger).** Growing from 21,536 →
  22,670 chars fires the soft trigger (24.8% headroom, below the ~25% threshold). Recalibrated
  at 125%: 22,670 × 1.25 = 28,338 → **~28,300 / ~7,080** (was ~27,300 / ~6,830).

- **`blueprint/CHANGELOG.md` recalibrated; envelope widened to ~30,000–65,000.** Adding
  the v2.0.15 entry grew CHANGELOG.md to ~70,800 chars. Recalibrated at 125%:
  70,800 × 1.25 = 88,500 → **~88,500 / ~22,130** (was ~84,600 / ~21,150). New table sum
  ~62,950 tokens pushed the cushion to ~1,050 tokens (1.64% of 64,000 — below the 2% floor),
  requiring envelope widening. Widened `!! audit all` envelope from `~30,000–64,000` to
  `~30,000–65,000` (sum + ~2,200 cushion = 3.4% of 65,000 — above the 2% floor). Cascade
  applied to: `ops/audit.md:72`, `user-guide.md` cost table, `user-guide.md` !! audit
  description.

### Post-fix token-reference envelope

Blueprint-doc rows: README (1,500) + setup-guide (3,300) + user-guide (4,450) +
troubleshooting (**7,080**) + CHANGELOG (**22,130**, see token-reference.md) + LICENSE (350) = **38,810**

Template-side rows: CLAUDE (6,450) + refresh-hot (1,280) + ingest (4,950) + lint (780) +
query (830) + update (600) + conventions (2,100) + audit (2,050) + token-reference (2,120)
= **21,160**

Skill rows: SKILL.md (1,300) + query-layer (800) + ingest-hook (880) = **2,980**

**Total ≈ 62,950 tokens** inside `~30,000–65,000`. Cushion ≈ 2,050 tokens (3.15% of
65,000 — above the 2% floor).

---

## v2.0.14 — 2026-04-19

### Soft recalibration trigger raised from ~3% to ~25%; full recalibration pass; envelope widened

- **Soft recalibration trigger threshold raised from ~3% to ~25% of measured actual.**
  The prior 3% threshold caught files only when they had nearly exhausted all headroom —
  essentially a last-second warning before the hard trigger. The new 25% threshold fires
  pre-emptively while ~25% of the calibrated headroom still remains, giving a comfortable
  lead time and removing the pattern where CHANGELOG.md would approach the hard trigger
  before the soft trigger even fired (flagged as S1 in audit #17). Updated in
  `ops/token-reference.md` Recalibration Rule.

- **Full recalibration pass against all tracked files.** 11 files fired the new 25% soft
  trigger (headroom < 25% of measured actual). All Chars and Tokens values reset to 125%
  of measured actual and rounded per convention. Files recalibrated (old → new Chars):
  - `blueprint/setup-guide.md`: ~12,800 → ~13,200 (10,564 measured)
  - `blueprint/user-guide.md`: ~17,100 → ~17,800 (14,219 measured)
  - `blueprint/CHANGELOG.md`: ~69,100 → see post-entry row (64,280 measured pre-entry)
  - `template/CLAUDE.md`: ~25,000 → ~25,800 (20,641 measured)
  - `ops/ingest.md`: ~18,600 → ~19,800 (15,858 measured)
  - `ops/lint.md`: ~2,900 → ~3,100 (2,507 measured)
  - `ops/conventions.md`: ~8,000 → ~8,400 (6,741 measured)
  - `ops/audit.md`: ~8,200 → ~8,200 (6,572 measured — recalibration no-op; value unchanged)
  - `ops/token-reference.md`: ~8,300 → ~8,500 (6,796 measured pre-edits)
  - `blueprint/skills/sqlite-query/SKILL.md`: ~4,700 → ~5,200 (4,185 measured)
  - `blueprint/skills/sqlite-query/ingest-hook.md`: ~3,300 → ~3,500 (2,838 measured)
  Files not recalibrated (headroom ≥ 25%): README.md (28.5%), troubleshooting.md (26.8%),
  LICENSE (31.2%), refresh-hot.md (28.6%), ops/query.md (27.6%), ops/update.md (27.6%),
  skills/query-layer.md (26.3%).

- **Cold-start quotes cascaded.** `template/CLAUDE.md` line 9 updated from ~6,250 to
  ~6,450 tokens (reflects CLAUDE.md row recalibration). Cold-start totals updated:
  ~6,330 → ~6,530 (CLAUDE.md + hot.md); ~7,280 → ~7,480 (with full memory.md).
  Cascade applied to: `template/CLAUDE.md:17`, `user-guide.md:9`, `user-guide.md:14`,
  `README.md:72`.

- **Audit envelope widened from ~30,000–58,000 to ~30,000–64,000.** The recalibration
  raised the Tokens-column sum above the prior 58,000 upper bound. New table sum:
  ~61,530 tokens (post-recalibration, including CHANGELOG.md final row). Envelope set
  to ~64,000 (sum + ~2,470 cushion = 3.9% of 64,000 — above the 2% floor). Cascade
  applied to: `ops/audit.md:72`, `user-guide.md` cost table, `user-guide.md` !! audit
  description.

### Post-recalibration token-reference envelope

Blueprint-doc rows: README (1,500) + setup-guide (3,300) + user-guide (4,450) +
troubleshooting (6,830) + CHANGELOG (see token-reference.md) + LICENSE (350)

Template-side rows: CLAUDE (6,450) + refresh-hot (1,280) + ingest (4,950) + lint (780) +
query (830) + update (600) + conventions (2,100) + audit (2,050) + token-reference (2,120)
= **21,160**

Skill rows: SKILL.md (1,300) + query-layer (800) + ingest-hook (880) = **2,980**

**Total ≈ 61,720 tokens** inside `~30,000–64,000`. Cushion ≈ 2,280 tokens (3.6% of 64,000).

---

## v2.0.13 — 2026-04-19

### sqlite-query skill fixes (audit #15 — W1, W2)

- **`ingest-hook.md` Notes section corrected to point at the right repair path (W1).**
  The second bullet in the Notes section said "`!! lint` detects and repairs drift."
  `!! lint` checks wiki-page quality only (broken links, orphans, stale claims) and has
  no mechanism to detect or repair `wiki.db` desync — the same misdirection the v2.0.12
  W3 fix corrected in the exception handler, but that fix did not propagate to the Notes
  section. An operator reading Notes (rather than the exception handler) would follow the
  `!! lint` direction, see a clean report, and incorrectly conclude the desync was resolved
  while `wiki.db` remained out of sync. Updated to: "To repair: say `!! install
  sqlite-query` and choose yes to the backfill offer, or `!! uninstall sqlite-query` to
  revert to grep." Now consistent with the corrected exception handler and
  `SKILL.md §Fallback Behaviour`.

- **`ops/ingest.md` B5 batch-preamble step enumeration updated to include step 11.5 (W2).**
  Step 11.5 (run ingest hook if installed) was added in v2.0.11 to the main Steps
  sequence, but the `!! ingest all` B5 preamble's explicit per-file step list was not
  updated — it read `[main-steps 5, 6, 7, 8, 9, 10, 11]`. A strict agent following that
  enumeration would skip the ingest hook on every batch ingest, causing `wiki.db` to drift
  from the markdown files silently (the grep fallback absorbs the desync at query time,
  making the failure invisible). Updated to `[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]`.
  No skip-list change needed — 11.5 was not in the skip list, only absent from the per-file
  list.

### Post-fix headroom (modified files only)

| File | Measured (`wc -c`) | Doc. Chars | Headroom | Flag |
|---|---:|---:|---:|:---:|
| `blueprint/skills/sqlite-query/ingest-hook.md` | 2,838 | ~3,300 | 14.0% | ok |
| `template/scheduled-tasks/ops/ingest.md` | 15,858 | ~18,600 | 14.7% | ok |

No hard or soft recalibration triggers. Token-reference envelope unchanged at 56,715 tokens
(cushion 1,285 / 2.2% of 58,000 — above the 2% floor). No `token-reference.md` row edits
required.

---

## v2.0.12 — 2026-04-19

### sqlite-query skill fixes (audit #13 — W1, W2, W3)

- **`query-layer.md` glob pattern replaced with `find`-based path resolution (W2).**
  The prior implementation built candidate file paths as `wiki/pages/**/<slug>.md`
  glob patterns. Python's `open()` and the Read tool do not expand globs — an agent
  attempting to read such a path receives `FileNotFoundError`. Unmatched bash globs
  compound this by returning the literal pattern string rather than empty, so the
  no-match case also produces an unreadable path. Fixed: after the SQLite query
  returns slugs, a `subprocess.run(["find", pages_dir, "-name", "<slug>.md"])` call
  resolves each slug to a concrete path (e.g. `wiki/pages/concepts/slug.md`). Only
  paths that `find` actually locates are appended to `candidate_paths` — missing slugs
  produce no output from `find` and are silently skipped, triggering the existing grep
  fallback. `ops/conventions.md` Query Layer Hook Contract output spec updated to
  explicitly prohibit glob patterns and document the `find`-via-subprocess requirement.

- **`ingest-hook.md` error message corrected to point at the right repair path (W3).**
  The hook's exception handler previously printed "run !! lint to repair." `!! lint`
  checks wiki-page quality only and has no mechanism to detect or repair `wiki.db`
  desync. Updated to: "say `!! install sqlite-query` and choose yes to the backfill
  offer, or `!! uninstall sqlite-query` to revert to grep." `SKILL.md §Fallback
  Behaviour` updated with a matching "DB desync recovery" paragraph so all failure-mode
  recovery paths are documented in one place.

- **`SKILL.md` "Offered During Setup" step number corrected (W1).**
  Said "Step 4"; the correct step in `setup-guide.md` is "Step 4.5 — Offer SQLite
  Query Skill." Step 4 is "Initialize Wiki Files." One-word fix.

- **`query-layer.md` recalibrated (hard trigger).** The `find`-based fix grew the
  file from 1,962 chars (documented ~2,500) to 2,533 chars — exceeding the documented
  Chars cap and firing the hard recalibration trigger. Recalibrated at 125%:
  2,533 × 1.25 = 3,166 → **~3,200 / ~800**. `token-reference.md` skill row updated.
  Skill-rows sum moves from 2,640 → **2,810** tokens. New total 56,715; cushion
  1,285 tokens (2.2% of 58,000) — above the 2% floor. No envelope widening required.

### Token-reference envelope after v2.0.12

Blueprint-doc rows: README (1,500) + setup-guide (3,200) + user-guide (4,280) +
troubleshooting (6,830) + CHANGELOG (17,275) + LICENSE (350) = **33,435**

Template-side rows: CLAUDE (6,250) + refresh-hot (1,280) + ingest (4,650) + lint
(730) + query (830) + update (600) + conventions (2,000) + audit (2,050) +
token-reference (2,080) = **20,470**

Skill rows: SKILL.md (1,180) + query-layer (800) + ingest-hook (830) = **2,810**

**Total = 56,715 tokens** inside `~30,000–58,000`. Cushion = 1,285 tokens (2.2% of
58,000).

---

## v2.0.11 — 2026-04-19

### sqlite-query skill; headroom convention 110% → 125%; changelog-monitor retired; audit #11 follow-ups

- **sqlite-query skill bundle added (new skill).** Opt-in relational query layer using a local
  SQLite index (`wiki.db`). Install via `!! install sqlite-query` (offered at setup Step 4.5);
  uninstall via `!! uninstall sqlite-query`. Three files under `blueprint/skills/sqlite-query/`:
  `SKILL.md` (install/uninstall flow, compatibility guard, `wiki.db` schema creation, backfill
  offer), `query-layer.md` (SQLite candidate lookup with grep fallback), `ingest-hook.md` (page
  upsert + bidirectional relation sync after every ingest). Blueprint Sync "New skill bundle added"
  cascade: `ops/conventions.md` gains Query Layer Hook Contract and Ingest Hook Contract sections;
  `ops/ingest.md` gains Step 11.5 (run ingest-hook if installed); `ops/update.md` gains Step 5.5
  (same); `setup-guide.md` Step 4.5 offers the skill at setup time; `user-guide.md` `!! install`
  section documents it; `ROADMAP.md` marks it shipped. `template/CLAUDE.md` Directory Structure
  diagram corrected to show skills at `blueprint/skills/` level (audit #11 S2 fix).

- **Headroom convention raised from ~110% to ~125% (Recalibration Rule Step 1 amended).**
  The 110% convention was catching soft-trigger recalibrations in nearly every audit pass (#5, #7,
  #8, #9, #10). Widening to 125% absorbs more routine content growth before a recalibration fires,
  reducing churn. `token-reference.md` Recalibration Rule Step 1 updated to "~125% of measured
  actual." All tracked-file Chars values re-set to 125% of measured actual on 2026-04-19.

- **`changelog-monitor.md` retired and removed from template.** The daily changelog monitor
  (introduced v2.0.1; W1 spec fix applied v2.0.10) has been removed from the distribution
  template. `template/scheduled-tasks/changelog-monitor.md` deleted; its `token-reference.md` row
  and `setup-guide.md` Step 2 copy entry removed. The v2.0.10 W1 fix (`source_url:` reverse-lookup;
  mandatory `source_url:` frontmatter in `ops/ingest.md` Step 7) remains in the schema. Users with
  an installed `scheduled-tasks/changelog-monitor.md` retain it; no migration required.

- **`blueprint/CHANGELOG.md` re-added to `token-reference.md` (audit #11 W2).** The 2026-04-19
  recalibration pass dropped the row, breaking the `!! audit all` envelope's derivability from
  the table (audit #11 W2). Re-added at `~69,100 / ~17,275` (125% of 55,265 measured). Envelope
  widened from `~30,000–54,000` to **`~30,000–58,000`** (documented sum ~56,545 + ~1,455 cushion
  = 2.5% of 58,000, above the 2% floor). Cascaded to `ops/audit.md:71`, `user-guide.md` (command
  reference and cost table), and `token-reference.md` Step 5.

- **`template/CLAUDE.md:9` cold-start self-cost corrected (audit #11 W1).** Line 9 said
  `~5,500 tokens`; `token-reference.md` documents CLAUDE.md at ~6,250 tokens. Fixed to
  `~6,250 tokens`. Cold-start total line 17 (`~6,330`) was already correct.

- **Three files recalibrated at hard trigger (audit #11 S1).**
  `ops/query.md` (2,586 chars, was ~2,400 → now ~3,300 / ~830),
  `ops/update.md` (1,881 chars, was ~1,700 → now ~2,400 / ~600),
  `ops/conventions.md` (6,379 chars, was ~5,700 → now ~8,000 / ~2,000).

### Token-reference envelope after v2.0.11

Blueprint-doc rows: README (1,500) + setup-guide (3,200) + user-guide (4,280) + troubleshooting
(6,830) + CHANGELOG (17,275) + LICENSE (350) = **33,435**

Template-side rows: CLAUDE (6,250) + refresh-hot (1,280) + ingest (4,650) + lint (730) + query
(830) + update (600) + conventions (2,000) + audit (2,050) + token-reference (2,080) = **20,470**

Skill rows: SKILL.md (1,180) + query-layer (630) + ingest-hook (830) = **2,640**

**Total = 56,545 tokens** inside `~30,000–58,000`. Cushion = 1,455 tokens (2.5% of 58,000).

---

## v2.0.10 — 2026-04-18

### Follow-ups (audit-driven, tenth pass — final audit)

- **`changelog-monitor.md` Step 1 rewritten as `source_url:` reverse-lookup
  (W1).** Audit #10 identified a long-standing specification gap: Step 1
  instructed the monitor to look up each source page using "the same slug
  derivation rules as `ops/ingest.md` Step 0" — a rule whose valid inputs
  are H1, filename stem, or page title (for URL ingest, via U2). The
  monitor has none of those pre-fetch: Step 1 runs **before** Step 2's
  WebFetch, so the only available inputs are the monitored URL and the
  Source Title column of the `## Monitored Sources` table. The rule was
  literally unexecutable at the call site. Implementations had to silently
  improvise, typically using URL last-segment or lowercase-hyphenated
  Source Title — which matched ingest-time slugs for the four current
  monitored sources by coincidence (their URL last-segments happened to
  equal the ingested H1 slug) but would diverge on any future source
  whose fetched title didn't round-trip through `lowercase-hyphenated`
  to the URL's last segment. Divergence silently misclassified an
  ingested source as 🆘 UNINGESTED in the Slack DM, and acting on that
  hint by running `!! ingest <URL>` would create a duplicate source page
  under the monitor's computed slug — fragmenting the wiki. The bug was
  latent (never fired in production) but architecturally real. **Fix:**
  Step 1 now builds a URL → source-page map once per run by enumerating
  `wiki/pages/sources/*.md` and reading each file's `source_url:`
  frontmatter, then looks up each monitored URL in the map by exact
  string match. UNINGESTED is reported when no page matches; the new
  AMBIGUOUS status is reported when more than one page matches (should
  not occur absent wiki corruption, but failing loudly is cheaper than
  silent miscomparison). Pages with `source_url: unknown` or missing
  `source_url:` are excluded from the map.
- **`source_url:` frontmatter made mandatory on every source page
  (W1 prerequisite).** The W1 fix depends on `source_url:` being a
  reliable join key on source pages, but pre-v2.0.10 `ops/ingest.md`
  Step 7 only mandated `source_hash:` and `original_file:` — U3 already
  prepended `source_url:` for URL ingest, but Clipper-ingested pages
  had no such guarantee. Step 7 now lists three mandatory frontmatter
  fields (`source_hash:`, `original_file:`, `source_url:`) and
  documents the fallback: for URL ingest, reuse U3's value; for
  Clipper ingest, pull the URL from the Clipper preamble (Obsidian
  Web Clipper's `source:`, or `url:`, or equivalent) and propagate;
  if no URL is recoverable, write `source_url: unknown` and note the
  gap in the approval request so the user can correct post-ingest.
  The Notes-section bullet listing frontmatter requirements was
  updated to match.
- **New monitor status: AMBIGUOUS (⚠️).** Added to the `Classify each
  source` list in `changelog-monitor.md` Step 4, to the Slack message
  emoji legend (pointer: "run `!! lint` to surface the duplicate"),
  and to the trailing-hint-lines rule (⚠️ rows omit both trailing
  hints since their inline action hint is in the legend, not a
  batched directive). The example Slack message body also picked up
  a sample ⚠️ row.
- **Troubleshooting added two new entries.** `troubleshooting.md` now
  documents (i) "Changelog monitor reports 🆘 UNINGESTED for a source
  I know I ingested" — covering both the pre-v2.0.10 slug-drift case
  (upgrade to v2.0.10+ to self-heal most sources) and the `source_url:`-
  missing-or-unknown case (backfill by hand, no re-ingest needed);
  and (ii) "Changelog monitor reports ⚠️ AMBIGUOUS for a source" —
  covering the duplicate-page scenario and the `!! lint` recovery
  flow.
- **Four token-reference rows recalibrated (hard trigger, all four
  exceeded documented Chars post-edit).** The edits above grew four
  files past their v2.0.9-calibrated documented bounds — not just the
  3% soft trigger but the hard "measured ≥ documented" trigger.
  Measured `wc -c` after the edits: `ingest.md` 15,399 (documented
  15,500 → within bound, but 0.66% headroom, below soft trigger);
  `changelog-monitor.md` 7,758 (documented 6,100 → hard trigger,
  +27% over); `troubleshooting.md` 30,220 (documented 27,900 → hard
  trigger, +8% over); `CHANGELOG.md` 55,170 (documented 51,500 →
  hard trigger, +7% over). Recalibrating each row at 110% of
  post-edit actual, rounded to nearest 100 for Chars and nearest 10
  for Tokens (chars ÷ 4):

  | File | Before | After |
  |---|---|---|
  | `scheduled-tasks/changelog-monitor.md` | `~6,100 / ~1,530` | `~8,500 / ~2,130` |
  | `scheduled-tasks/ops/ingest.md` | `~15,500 / ~3,880` | `~17,000 / ~4,250` |
  | `blueprint/troubleshooting.md` | `~27,900 / ~6,980` | `~33,200 / ~8,300` |
  | `blueprint/CHANGELOG.md` | `~51,500 / ~12,880` | `~60,700 / ~15,180` |

  Calibration date header stays 2026-04-18 (same-day recalibration,
  per the routine-pass pattern).

- **Envelope widened from `~30,000–50,000` to `~30,000–54,000`
  (Step 5 trigger: sum exceeded the upper bound).** Post-recalibration
  Tokens sum: blueprint-doc rows = README (1,280) + setup-guide (3,350)
  + user-guide (4,150) + troubleshooting (8,300) + CHANGELOG (15,180)
  + LICENSE (300) = **32,560**; template-side rows = CLAUDE (5,475) +
  refresh-hot (1,100) + changelog-monitor (2,130) + ingest (4,250) +
  lint (630) + query (530) + update (350) + conventions (1,250) +
  audit (1,800) + token-reference (1,830) = **19,345**. Total
  **51,905** — which **exceeds** the v2.0.9 `~30,000–50,000` upper
  bound by ~1,905 tokens. Widened per the Step 5 formula
  (sum + ~1,500–3,000 cushion, rounded to nearest 1,000) to
  **`~30,000–54,000`** (51,905 + 2,095 = 54,000; cushion = 2,095 =
  3.88% of upper bound, above the 2% floor). Cascaded to
  `ops/audit.md:71`, `user-guide.md:94`, and `user-guide.md:215`.
  The envelope growth this pass (~4,000 tokens) is the largest since
  the v2.0.4 widen — a reflection of the scale of the W1 fix, which
  touched four of the sixteen tracked files.

### Outcome

Closes the last latent specification gap in the blueprint. The
written Recalibration Rule now owns the detection pattern for all
file-level drift (hard, soft, and envelope-cushion triggers). The
written Blueprint Sync Rule owns downstream propagation. Audit #10's
closing framing (final audit in the series; blueprint has reached a
steady state) is recorded in `audit-report-2026-04-18-10.md`. Future
recalibrations should fire via the rule, not via an audit pass.

---

## v2.0.9 — 2026-04-18

### Follow-ups (audit-driven, ninth pass)

- **`CHANGELOG.md` row recalibrated (S1).** Measured `wc -c` 43,457
  against documented Chars 44,000 — 1.25% headroom, well below the
  Recalibration Rule's 10% convention and by far the most drifted file
  in the table. Same drift class as audits #5 S2 (ops/audit.md), #7 W1
  (token-reference.md:54 prose), and #8 S1 (ops/audit.md again);
  CHANGELOG.md is the most churn-prone file in the blueprint (new
  section per version bump), so early recalibration is higher-value
  here than elsewhere. *Two-pass recalibration:* the first pass set the
  row to `~47,800 / ~11,950` (110% of 43,457 ≈ 47,800), but adding the
  v2.0.9 changelog entry itself (this one) grew the file to 46,832
  chars — which left only 2.07% headroom against the fresh 47,800
  target, below the newly-codified 3% soft trigger (see Q1 below). The
  final row is **`~51,500 / ~12,880`** (110% of 46,832 ≈ 51,500; tokens
  51,500 ÷ 4 = 12,875 rounded to nearest 10 = 12,880), giving ~9.97%
  headroom against the post-patch measured actual. The meta-lesson: a
  recalibration patch must account for its own content growth in the
  target-measurement baseline, not just the pre-patch `wc -c` figure.
  Calibration date header stays 2026-04-18.
- **Recalibration-Rule trigger amended with a soft 3%-headroom threshold
  (Q1).** Three consecutive audits (#7 W1, #8 S1, #9 S1) each caught a
  single file drifting past ~2% headroom and flagged it as a pre-emptive
  STYLE finding. That pattern was effectively the audit layer *acting as*
  a soft threshold that the written rule didn't encode — meaning catching
  the drift required a full audit pass rather than routine maintenance.
  Updated the **Recalibration trigger** paragraph in `token-reference.md:72`
  to add "Also fire pre-emptively when any file's remaining headroom drops
  below ~3% of its measured actual" with an explicit pointer to audits
  #5 S2, #7 W1, #8 S1, #9 S1 as the documented precedent. The hard
  trigger (measured ≥ documented) and the post-INGEST routine pass are
  unchanged. `update.md` (7.28%) and `ingest.md` (8.79%) stay well clear
  of the soft trigger, so no non-CHANGELOG file required recalibration
  for audit #9.
- **`token-reference.md` row recalibrated as a self-trigger side-effect
  (Q1 cascade).** Adding the Q1 + Q2 prose (this entry and the two
  paragraphs above/below) to `token-reference.md` grew the file from
  6,095 chars (at the start of audit #9) to 6,664 chars after the Q1/Q2
  edits — leaving only 2.04% headroom against its pre-patch documented
  Chars 6,800, below the newly-codified 3% soft trigger. Recalibrated
  the row from `~6,800 / ~1,700` to **`~7,300 / ~1,830`** (110% of 6,664
  ≈ 7,300; tokens 7,300 ÷ 4 = 1,825 rounded to nearest 10 = 1,830).
  Propagated the `~1,700 → ~1,830` self-cost figure to the two
  instances in the Self-cost note (line 8) and the two instances in the
  Ingest Estimate Formula section (lines 62, 64/66); fixed-floor
  computation moved `~3,025 → ~3,155` to match (625 + 200 + 1,830 +
  500). Same mechanical propagation pattern as audit #7 W1 (`refresh-
  hot.md` table-vs-prose reconciliation).
- **Recalibration-Rule Step 5 amended with a ~2%-cushion envelope floor
  (Q2).** As the Tokens column grows and per-file recalibrations land,
  the envelope's cushion shrinks even when every individual file stays
  within its own 10% headroom. Pre-v2.0.9 rule widened the envelope
  only when the documented sum *exceeded* the upper bound, meaning the
  cushion could get arbitrarily thin before the trigger fired. Added a
  second widening condition to Step 5: widen when the cushion drops
  below ~2% of the upper bound (~1,000 tokens on a 48,000-token
  envelope), even if the sum is still inside. Under the new rule,
  after the S1 + Q1-cascade recalibrations this patch applied,
  blueprint-doc sum moved 27,060 → 28,940 (+1,880 from the CHANGELOG.md
  row) and template-side sum moved 18,245 → 18,375 (+130 from the
  token-reference.md row). New total 47,315. Against the existing
  48,000 upper bound that would have left ~1.43% cushion — below the
  new 2% floor — so the envelope itself was widened from `~30,000–
  48,000` to **`~30,000–50,000`** per the widening formula (sum +
  ~1,500–3,000 cushion; 47,315 + 2,685 → 50,000 nearest-thousand).
  Cascaded to the three `!! audit all` mentions: `ops/audit.md:71`,
  `user-guide.md:94` (command reference), and `user-guide.md:215`
  (cost table). `ops/audit.md`'s envelope-history parenthetical was
  updated to include the v2.0.9 widen alongside the v2.0.6 and v2.0.7
  events. `token-reference.md` Step 5's own envelope literal was
  updated the same way. Post-patch cushion is 2,685 tokens ≈ 5.4% of
  the new upper bound — comfortably above the 2% floor.

*Pre-existing cold-start figures (`~5,530` / `~6,280` / `~5,475`) do
not change — neither `CHANGELOG.md` nor the envelope literal factors
into cold start. `README.md`, `setup-guide.md`, and `CLAUDE.md` do not
quote the envelope or `CHANGELOG.md`'s row directly, so no further
prose cascade is required.*

## v2.0.8 — 2026-04-18

### Follow-ups (audit-driven, eighth pass)

- **`user-guide.md:216–217` cascade miss fixed (W1).** v2.0.7's W1 entry
  bumped the realistic `!! wrap` / `!! ready` costs inside
  `token-reference.md:54` (`~2,700` → `~2,800` and `~2,800` → `~2,825`
  respectively) with the new per-read arithmetic spelled out, but the
  propagation stopped there. The user-guide cost table at lines 216–217
  duplicates both figures as user-facing planning numbers and was left at
  the stale values — a doc-vs-doc contradiction of the source-of-truth
  invariant declared in `token-reference.md`'s header ("Any quoted cost in
  CLAUDE.md, README.md, user-guide.md, or setup-guide.md must be
  re-derivable from this table — re-propagate when this table changes").
  Same cascade-miss class as audit #6's W1 (`user-guide.md:14` cold-start
  prose missed by v2.0.5) and #6's W2 (`user-guide.md:94` envelope prose
  missed by v2.0.5). Two-number string replacement; `!! wrap` → `~2,800`,
  `!! ready` → `~2,825`. No other files touched.
- **`CLAUDE.md:58` "two documented exceptions" → "three" (W2).** The
  Approval Rule header declared "two documented exceptions listed below"
  while the bullet list at lines 68–71 enumerated three (`!! wrap`,
  `!! ready`, `!! audit`). CHANGELOG v1.14 ("README `!! audit` exception
  drift fixed") documents that `!! audit` was deliberately added to the
  list at that time — but the intro sentence's count was never updated, and
  the drift has persisted through every subsequent schema bump. `README.md`
  and `user-guide.md` both correctly enumerate all three via fuzzy
  wording ("`!! wrap`, `!! ready`, and `!! audit`"); only `CLAUDE.md`'s own
  intro still said "two" — inside an **IMPORTANT**-tagged rule the agent
  re-reads every cold start, the worst possible place for a numeric
  contradiction to live. Single-word fix. No cascade — README and
  user-guide don't depend on the count.
- **`ops/audit.md` row pre-emptively recalibrated (S1).** Measured
  `wc -c` 6,482 against documented Chars 6,600 — 1.8% headroom, well
  below the Recalibration Rule's 10% convention. Same drift pattern audit
  #5 flagged as S2 on the same file; v2.0.7's own W2 + S2 edits
  (envelope-justification prose and the Note rewrite on line 71) pushed
  it back toward the trigger. Bumped row from `~6,600 / ~1,650` to
  `~7,200 / ~1,800` (110% of 6,482 = 7,130, rounded up to 7,200; tokens
  7,200 ÷ 4 = 1,800). Template-side sum moves 18,095 → 18,245; blueprint-
  doc sum unchanged at 27,060; new total ~45,305 — still inside the
  widened `~48,000` envelope upper bound with ~5.9% cushion. Per
  Recalibration Rule Step 5, since the updated sum stays inside the
  bound, no envelope edit is needed. Cold-start figures
  (`~5,530` / `~6,280` / `~5,475`) do not change — the `ops/audit.md`
  row does not factor into cold start. Calibration date header stays
  2026-04-18. Pre-emptive housekeeping, not a bug fix.

## v2.0.7 — 2026-04-18

### Follow-ups (audit-driven, seventh pass)

- **`token-reference.md:54` reconciled with the File Read Costs table (W1).**
  The "true session cost" note at line 54 quoted `refresh-hot.md` as
  `~1,030` tokens while the same file's table at line 22 documented it as
  `~1,100`. The 1,030 figure was a stale measured-actual from a prior
  calibration; today's measured actual is 992 tokens (3,966 chars), so the
  1,100 documented value is the 110%-headroom-inflated canonical number.
  Direct intra-file self-contradiction. Fixed by changing `~1,030` →
  `~1,100` and refreshing the two downstream realistic-cost figures:
  `!! wrap` ~2,700 → ~2,800 (`1,100 + 200 + 625 + 100 + 600–900` midpoint),
  `!! ready` ~2,800 → ~2,825 (`1,100 + 200 + 625 + 100 + 750 + 50` exact).
  Added an explicit note that all figures in the paragraph use the
  documented Tokens column so they stay coupled to the table on future
  recalibrations.
- **CHANGELOG v2.0.6 envelope-justification prose repaired (W2 + S2).** The
  v2.0.6 entry justifying the 45,000 upper bound said
  "(≈110% of current documented sum, rounded to nearest 1,000)". Arithmetic:
  45,000 / 43,575 = 103.3%, not 110%. If the next editor applied that rule
  literally on the next sum increase, the envelope would balloon far beyond
  intent (e.g., a sum of 48,000 would produce a 53,000 upper bound rather
  than the intended ~50,000). Rewrote the parenthetical to match the
  additive-cushion framing that `audit.md:71` already uses: "documented sum
  ~42,435 plus a ~2,565-token cushion, rounded to nearest 1,000 — additive
  cushion, NOT a multiplicative 110% scaling of the sum". Also amended
  `audit.md:71`'s note to drop the misleading "matching the 110% per-file
  headroom convention" tail (the 110% convention is per-file only and is
  already baked into each row's Chars value — re-applying it at the
  envelope level double-counts). Both docs now use the same methodology
  (S2 auto-closed).
- **Recalibration Rule Step 4 extended to cover the envelope cascade (S1).**
  Previously Step 4 of the Recalibration Rule mentioned only cold-start
  cascade targets (`CLAUDE.md`, `user-guide.md`, `README.md`) — a future
  editor following the rule would update the Tokens column and the
  cold-start figures but could miss that the `!! audit all` envelope at
  `ops/audit.md:71` is derived from the same column. The v2.0.6 pass caught
  this by editor judgment, not by following the rule. Added a new Step 5
  that explicitly re-sums the blueprint-doc + template-side rows, verifies
  the result still fits inside the documented envelope, and if not, widens
  the envelope (sum + ~1,000–1,500 cushion, rounded to nearest 1,000) and
  cascades to every `!! audit all` mention. Original "Update calibration
  date" step renumbered to Step 6.
- **Per-file schema footer asymmetry resolved — normalize down (Q1).**
  `changelog-monitor.md` was the only template file with a trailing
  `*Schema: v2.0 | Created: 2026-04-18*` footer; `refresh-hot.md` and every
  file under `ops/` lacked one. Unresolved across audits #3, #4, #5, #6, #7.
  Dropped the footer to align with the rest of the template tree. The
  canonical schema version continues to live in `CLAUDE.md`'s footer and in
  `hot.md`'s `Schema:` header; per-file footers were a parallel source of
  truth that added drift risk without value. This closes a question that
  had been carried for five consecutive audits.
- **`token-reference.md` and `CHANGELOG.md` recalibrated; envelope widened
  to `~30,000–48,000` (Recalibration-Rule Step 5 exercised).** Post-fix
  `wc -c` showed two files crossed their documented Chars caps:
  `token-reference.md` 6,094 (cap 6,000) and `CHANGELOG.md` grew past its
  38,500 cap as this v2.0.7 entry accumulated. Recalibration trigger fired
  for both rows. Applied 110% headroom per the convention (rounded
  liberally so the rows have room to absorb this very entry's growth):
  `ops/token-reference.md` row bumped from `~6,000/~1,500` to
  `~6,800/~1,700`; `blueprint/CHANGELOG.md` row bumped from
  `~38,500/~9,620` to `~44,000/~11,000`. The token-reference self-cost
  change (~1,500 → ~1,700) cascaded inside `token-reference.md` — the
  Self-cost note, the Ingest Estimate concrete, and the fixed-floor
  arithmetic (~2,825 → ~3,025) all updated. No change to cold-start
  figures (~5,530 / ~6,280 / ~5,475) because `CLAUDE.md` was not touched
  and the self-cost does not factor into cold start. Blueprint-doc sum
  moves 25,680 → 27,060 (CHANGELOG row +1,380); template-side sum moves
  17,895 → 18,095 (token-reference row +200); new total ~45,155 — over
  the previous 45,000 envelope upper bound by 155 tokens. Per the new
  Recalibration-Rule Step 5, widened the `!! audit all` envelope from
  `~30,000–45,000` to `~30,000–48,000` (sum ~45,155 + ~2,845 cushion,
  rounded to nearest 1,000) and cascaded to `ops/audit.md:71`,
  `user-guide.md:94`, `user-guide.md:215`, and the Step-5 literal in
  `token-reference.md:79`. The new cushion is ~6.3% — comparable to
  v2.0.6's ~5.9%, restoring the pre-recalibration margin.

## v2.0.6 — 2026-04-18

### Follow-ups (audit-driven, sixth pass)

- **`user-guide.md:14` cold-start prose updated from `~6,005` to `~6,280` (W1).**
  v2.0.5's cold-start cascade (documented `~5,200` → `~5,475`, total cold-start
  `~5,255` → `~5,530`, `!! ready` total `~6,005` → `~6,280`) propagated to
  `README.md`, `template/CLAUDE.md`, and the cost table at `user-guide.md:209`,
  but missed the prose sentence at `user-guide.md:14`. The miss produced a
  direct self-contradiction inside the same file — opening narrative said
  `~6,005`, cost table 195 lines later said `~6,280`. One-line string
  replacement; no behavioral change. Exactly the kind of drift the Blueprint
  Sync Rule exists to catch, hence flagged as WARNING rather than STYLE.
- **`user-guide.md:94` envelope prose updated from `~25,000–35,000` to
  `~30,000–45,000` (W2).** v2.0.5 bumped the `!! audit all` envelope from
  `~25,000–35,000` to `~30,000–40,000` across `ops/audit.md:71`,
  `user-guide.md:215`, and the CHANGELOG, but missed the command-reference
  prose at `user-guide.md:94`. Same intra-file self-contradiction pattern as
  W1. Fixed in the same pass as W4's envelope widen so line 94, line 215, and
  `audit.md:71` all report the new `~30,000–45,000` range without another
  propagation round.
- **`ops/ingest.md:64` dangling cross-reference dropped (W3).** Step 0's slug
  derivation said "same rules as Step 7 (lowercase-hyphenated from the H1 or
  filename stem; for URL ingest reuse the U2 slug)" — but Step 7 consumes a
  pre-computed `${slug}` and contains zero slug-derivation rules. The inline
  parenthetical on line 64 itself is the canonical source. Rewrote to drop the
  "same rules as Step 7" clause and added a positive pointer noting that
  `changelog-monitor.md` Step 3 relies on the same rules (which is what makes
  cross-path hash comparisons possible) and that Step 7 is a consumer, not a
  source. Low-severity today — the parenthetical was correct so no agent was
  ever actually stranded — but pre-empts the class of error (slug derivation
  divergence between ingest paths) that v2.0.2's hash canonicalization
  hardened against.
- **`!! audit all` envelope widened from `~30,000–40,000` to `~30,000–45,000`
  (W4).** `ops/audit.md:71` declared `token-reference.md`'s documented Tokens
  column as the envelope's source of truth, but re-deriving gave ~42,435
  (blueprint-doc rows 24,540 + template-side rows 17,895) — above the stated
  40,000 upper bound. The directive to derive from the table and the literal
  range disagreed. Chose Option A (widen the range) over Option B (re-point
  the directive at measured actuals) because the 110% per-file headroom
  convention already implies per-file Chars values overshoot measured actuals
  by ~10%, so an envelope that contains the sum of Chars values is the
  internally consistent choice. Widened to `~30,000–45,000` (documented sum
  ~42,435 plus a ~2,565-token cushion, rounded to nearest 1,000 — additive
  cushion, NOT a multiplicative 110% scaling of the sum) in `audit.md:71`,
  cascaded to `user-guide.md:215` and `user-guide.md:94` (W2). Amended the
  `audit.md:71` note to call the 45,000 upper bound "the documented sum plus
  a small cushion" so the next editor sees *why* the number is 45,000 rather
  than a hand-tuned figure. The 110% per-file headroom convention remains
  per-file only; the envelope is derived from the sum of the already-
  headroomed Chars values plus a small additional cushion to absorb tool-
  call and prompt-side overhead (i.e. the 10% headroom is already baked
  into the per-row figures being summed, so the envelope does NOT apply a
  second 110% multiplier on top).
- **`token-reference.md` CHANGELOG row recalibrated to absorb this v2.0.6
  entry.** Post-fix `wc -c` against every row: all other rows stayed within
  headroom (`ingest.md` 14,247 / 15,500; `ops/audit.md` 6,207 / 6,600;
  `user-guide.md` 15,076 / 16,600). `CHANGELOG.md` itself grew from 30,830 →
  ~35,000 for this v2.0.6 entry, crossing its 33,900 Chars cap and firing
  the recalibration trigger. Bumped the `blueprint/CHANGELOG.md` row to
  `~38,500 chars / ~9,620 tokens` per the 110%-of-measured convention (rounded
  to nearest 100 for chars, nearest 10 for tokens). The blueprint-doc sum in
  `token-reference.md` moves from 24,540 to ~25,680 tokens; new `!! audit all`
  envelope total is ~43,575, still inside the widened 30,000–45,000 range set
  by W4.

## v2.0.5 — 2026-04-18

### Follow-ups (audit-driven, fifth pass)

- **Retry-after-crash prose aligned with actual ingest behavior (W1).**
  v2.0.4's CHANGELOG and `troubleshooting.md` Prevention paragraph for the
  "Ingest interrupted mid-flight and retry silently deleted the inbox file"
  entry both described the post-Step-6-crash case as "retry finds the
  pre-moved raw file and writes the source page against it" / "the source
  page write on retry will see the pre-moved raw file and behave correctly."
  Tracing the op showed this is not what happens: `ops/ingest.md` has no
  Step 0.5 branch that detects and adopts a pre-moved raw file. Filename
  retry fails at Step 0's `wiki/inbox/<file>` read (the file is gone); URL
  retry pre-computes a fresh `ts` in Step 5 and writes a new
  `raw/<slug>-<new-ts>.md`, leaving the original pre-moved raw as an orphan.
  Both the CHANGELOG entry and the troubleshooting Prevention paragraph were
  rewritten to describe actual behavior — the source is preserved in `raw/`
  (the real data-loss fix), but manual recovery is required on retry: either
  re-clip to drive a fresh ingest (accepting an orphan raw file) or
  `mv raw/<slug>-<ts>.md wiki/inbox/<slug>.md` before retrying. No code
  change; the prose now matches the op. The alternative fix (add the
  Step 0.5 adoption branch to match the old prose) was rejected as a larger
  surface area for marginal retry continuity — the manual-recovery path is
  simple, documented, and preserves data either way.
- **`!! audit all` envelope re-summed and reframed as derivable (W2).**
  v2.0.4's envelope bump (~25,000–35,000 tokens, based on a ~33,000-token
  measurement) was itself pushed out of spec by the act of documenting it:
  post-v2.0.4 CHANGELOG and troubleshooting growth brought the summed cost
  to ~36,440. `ops/audit.md:71` and `user-guide.md:215` bumped to
  ~30,000–40,000 to absorb near-term drift, and the `audit.md` note now
  explicitly calls out `token-reference.md` as the source of truth rather
  than treating the range as a hand-tuned figure. Future envelope drift
  should be caught by summing the table rather than editing the literal.
- **`setup-guide.md` Step 3 MCP detection made deterministic (W3).** Step 3
  previously said "if the scheduled-tasks MCP is not yet configured to run
  `changelog-monitor.md` on a daily cadence, surface this in Step 8" but
  never specified how the setup-time agent was supposed to know. Three
  operators running setup could produce three different readiness
  announcements. Rewritten to prescribe: (i) call the scheduled-tasks MCP's
  list tool (e.g. `mcp__scheduled-tasks__list_scheduled_tasks`) and look
  for a task referencing `changelog-monitor.md`; (ii) if the list tool is
  unavailable, ask the user directly. Explicit prohibition against silent
  "always flag" default. Step 8's conditional wiring (added in v2.0.4 to
  close audit #4 C1) now has a well-defined input.
- **"New scheduled task" sync row tightened (W4).** `CLAUDE.md:100` listed
  `ops/audit.md (scope)` as a required touch-point, but v2.0.1's scope
  generalization (the glob `every file directly under scheduled-tasks/`)
  already covers new files automatically. The row now says
  `ops/audit.md (informational parenthetical on line 23 naming current tasks
  — the glob itself already covers new files, so this is a doc-hygiene
  touch, not a behavioral one)`. Eliminates the misdirection where an
  operator adding a new scheduled task would open `audit.md` looking for a
  scope block to edit.
- **`ingest.md` Step 5 execution mechanism made explicit (S1).** Step 5
  told the agent to "generate once and hold in working memory" a bash
  timestamp, but Cowork Bash does not persist env vars across tool calls,
  so "hold in working memory" required an unstated implementation choice.
  Step 5 now documents the two acceptable patterns: (i) standalone Bash
  call captures `date +%Y-%m-%d-%H%M%S` output into LLM working memory,
  then Step 6 inlines the literal as `export ts="..."`; or (ii) Steps 5
  and 6 fold into a single Bash invocation. The Step 6 `${ts:?…}` guard
  catches unset-variable leakage but cannot catch a *different* `ts`
  landing in Step 7 — that's load-bearing on the agent picking one of
  the two documented patterns and sticking with it.
- **`token-reference.md` headroom recalibrated across drifted rows (S2).**
  Three template-side rows sat below the 10% headroom convention
  (`template/CLAUDE.md` at 5.5%, `refresh-hot.md` at 3.4%, `ops/audit.md`
  at 6.0%). Bumped pre-emptively. The W1 / S1 / v2.0.5-changelog edits in
  this pass also grew `troubleshooting.md`, `setup-guide.md`,
  `ops/ingest.md`, and `CHANGELOG.md` into their prior headroom, so those
  rows were re-calibrated in the same pass rather than waiting for the
  next incidental edit to trip the recalibration trigger. CLAUDE.md's
  cold-start cascade (documented `~5,200` → `~5,475`, total cold-start
  `~5,255` → `~5,530`, `!! ready` total `~6,005` → `~6,280`) propagated
  to `README.md`, `user-guide.md`, and `template/CLAUDE.md` per the
  "File-size or cost change" Blueprint Sync Rule row.

### Not applied
- **Q1 (per-file schema footers).** Carried from v2.0.3 and v2.0.4.
  Still a judgment call — either add footers to every template file for
  provenance parity, or drop `changelog-monitor.md`'s for symmetry.
  Audit #5 could not resolve intent.

## v2.0.4 — 2026-04-18

### Follow-ups (audit-driven, fourth pass)

- **Ingest op reordered to close a silent data-loss window (CRITICAL).** In
  v2.0.0–v2.0.3, Step 5 wrote the source page (with `source_hash:` committed)
  **before** Step 9 moved the inbox file to `raw/`. A mid-flight failure
  between the two left the wiki in a state where `source_hash:` was committed
  but no raw file existed; the next retry's Step 0 hash check compared the
  still-present inbox content against the committed hash, matched, and executed
  the rerun-proof short-circuit — deleting the inbox file and printing `No
  change since last ingest — skipped.` The deletion was correct for the
  "rerun of a completed ingest" path but catastrophic for the crash-recovery
  path: the only remaining copy of the source was destroyed and the source
  page's `original_file:` pointer dangled permanently. The fix reorders the
  op so the raw-file move happens **before** the source-page write. New Step
  numbering: Step 5 pre-computes a single `ts=$(date +%Y-%m-%d-%H%M%S)` once
  per ingest; Step 6 moves `wiki/inbox/<file>` to `raw/<slug>-<ts>.md`; Step
  7 writes the source page with `source_hash:` AND `original_file:
  raw/<slug>-<ts>.md` using the pre-computed `ts`, with provenance footnotes
  citing the same path. Old Steps 6–8 (index read / page updates / index
  update) renumber to 8–10; old Steps 10–12 (log append / hot refresh /
  recalibrate) renumber to 11–13. A mid-flight failure now either leaves the
  inbox file untouched (crash before Step 6 — clean retry from Step 0) or
  leaves the raw file in place with no source page yet (crash between Step 6
  and 7 — the source is preserved in `raw/` but manual recovery is required
  on retry, see `troubleshooting.md` for the recovery paths). The inbox file
  is never silently deleted after a partial-write state, which is the real
  data-loss fix; the retry itself is not automatic (the op has no Step-0.5
  branch that adopts a pre-moved raw file), so operators either re-clip the
  article to drive a fresh ingest (leaving the pre-moved raw file as a
  harmless orphan) or move it back to `wiki/inbox/` under its original name
  before retrying. See `troubleshooting.md` "Ingest interrupted mid-flight
  and retry silently deleted the inbox file" for the symptom and the
  manual-recovery procedure.
- **Pre-computed `ts` closes a sub-second drift window (CRITICAL).** Old
  Step 9's bash snippet generated its own `ts` at move time; old Step 5's
  source-page write referenced `<YYYY-MM-DD-HHMMSS>` without a mandate to
  reuse the same value. In practice the two steps executed milliseconds
  apart and usually agreed, but nothing forced that — an ingest that
  straddled a second boundary would commit a source page whose
  `original_file:` and provenance footnotes pointed at a raw filename one
  second off from the actually-written file, producing a dangling provenance
  trail on the first try. The fix (Step 5 pre-compute + Step 6 / Step 7
  consume) makes agreement structural rather than probabilistic.
- **B-preamble step references renumbered.** `!! ingest all`'s B-preamble
  cross-references the main Steps by number in six places (B3, B3.6, B5,
  B6, B7). All six were rewritten to point at the new step numbers: B3's
  index read maps to Step 8; B3.6's "Steps 11/12 only run when at least one
  file is actually ingested" becomes Steps 12/13; B5's per-file range
  `[main-steps 5, 6, 7, 8, 9, 10]` becomes `[main-steps 5, 6, 7, 8, 9, 10,
  11]` and its skip list `[main-steps 1, 3, 4, 11, 12]` becomes
  `[main-steps 1, 3, 4, 12, 13]`, with the first-file index read and mutation
  referring to Steps 8 / 10; B6's end-of-batch `[main-steps 11 and 12]`
  becomes `[main-steps 12 and 13]`; B7's per-file log append points at Step
  11; U4's "Steps 5–12 unchanged" becomes "Steps 5–13 unchanged". Step 0's
  two internal references to Step 5 (slug derivation rules, regeneration
  branch) retarget to Step 7. Every cross-reference in the op is now
  consistent with the new numbering.
- **Hash Canonicalization: code-block indentation caveat documented (Q1).**
  Step 3 of the canonicalizer collapses intra-line whitespace runs, which
  also flattens code-block indentation for hashing purposes — a known and
  intentional tradeoff (absorbing fetcher-level indent drift is the whole
  point of the normalizer) but undefended in the docs. A new paragraph in
  the Hash Canonicalization section calls this out explicitly: two sources
  differing *only* in code-block indentation hash identically, and a source
  whose sole real change is an indentation refactor will not be detected.
  For personal-wiki use this is the right tradeoff; a code-aware downstream
  would want a language-sensitive normalizer. No code change — this is a
  documentation fix to close a "Question for Clarification" from the audit.
- **`token-reference.md` grew rows for blueprint docs (W2).** The cost
  table previously listed only `wiki/`- and `scheduled-tasks/`-level files;
  `README.md`, `setup-guide.md`, `user-guide.md`, `troubleshooting.md`,
  `CHANGELOG.md`, and `LICENSE` were missing, which meant `!! audit all`
  and any blueprint-edit operation had to be estimated from scratch each
  time. Six rows added (with a note that they apply only to
  blueprint-authoring sessions). A corresponding note documents that
  `!! ingest all` pays the `token-reference.md` self-cost once per batch,
  not per file.
- **Ingest Estimate Formula made complete (W3).** The formula previously
  read `raw source read + (500 × pages to create) + (200 × pages to update)
  + 500 overhead`, omitting the fixed reads every ingest pays (`log.md`
  tail at Step 1, `index.md` at Step 8, and `token-reference.md` self-cost
  at the Step 4 approval). Rewritten to include those terms and a concrete
  ~2,455-token fixed floor before variable reads.
- **`!! audit all` envelope recalibrated (W1).** Documented envelope was
  `~20,000–25,000` tokens; measured on 2026-04-18 it ran ~33,000 (34%
  over). Bumped to `~25,000–35,000` in both `ops/audit.md` Notes and
  `user-guide.md`'s Token Awareness table. The Notes entry now points at
  the blueprint-doc rows in `token-reference.md` as the source of truth
  for recalibration.
- **`!! ready` drafts surfacing guarded for blueprint-authoring mode (W4).**
  `CLAUDE.md`'s `!! ready` Step 5 previously surfaced "in-progress drafts
  from `drafts/`" without checking whether `drafts/` exists. On a
  blueprint-only checkout (the case `!! audit` most often runs in),
  `drafts/` is absent alongside `wiki/`, and the drafts surface could
  produce a noisy `ls drafts/` error that slips past the existing
  blueprint-authoring guard. A single `[ -d drafts ]` check now skips the
  surface transparently in that mode, matching the pattern the rest of the
  blueprint-authoring mode guards already use.
- **`setup-guide.md` Step 8 now actually surfaces changelog-monitor
  scheduling status (C1).** Step 3 has always told the AI operator to
  "surface in the Step 8 readiness announcement" if `changelog-monitor.md`
  is not yet on a scheduled-tasks cadence, but Step 8 had no corresponding
  instruction to do anything with that flag. Step 8 now has an explicit
  conditional block adding a quoted note to the readiness announcement
  when the scheduling gap exists, closing a dead cross-reference that had
  been silently ignored for the entire v2.0.x series.

## v2.0.3 — 2026-04-18

### Follow-ups (audit-driven, third pass)

- **`Pages: N` counter is now derived, not stored.** `refresh-hot.md` Step 1
  previously read the page count from a `**Stats:** N pages` header line in
  `wiki/index.md`, but no op file (ingest / lint / update / query-filing) was
  ever specified to bump that counter when pages were added or removed. Without
  explicit instruction, a strict agent would add entry rows to `index.md` and
  leave the Stats counter stale, causing `hot.md`'s `Pages: N` to silently go
  wrong. Step 1 now derives the count from the length of the `^- [[` entry list
  it already collects for the `Hot:` field — same read, same parse, one fewer
  invariant to maintain. `setup-guide.md`'s `wiki/index.md` template drops the
  Stats header line accordingly; the Field Reference row in `refresh-hot.md`
  updates to reflect the derived source.
- **Blueprint Sync Rule: versioning split made explicit.** A new note under
  the matrix states that the CLAUDE.md footer and `hot.md`'s `Schema:` field
  track only major.minor (`X.Y`), while patches (`X.Y.Z`) add a CHANGELOG
  section without moving either. The split was implicit in practice (v2.0.1 and
  v2.0.2 both landed without touching the footer) but not documented — a new
  operator reading the Sync Rule could reasonably have inferred that a patch
  should also rewrite the footer. The note closes that interpretation gap.
- **`ops/conventions.md` recalibrated.** Measured 4,500 chars against a
  documented 4,600 (2.2% headroom, well under the 10% headroom convention in
  `token-reference.md`). Documented value bumped to 5,000 / ~1,250 tokens
  (110% of measured, rounded to nearest 100). The file grew during v2.0.2's
  `source_hash:` frontmatter-doc expansion but was not re-calibrated at that
  time because the recalibration trigger fires on exceedance, not drift; this
  pass reclaims the headroom pre-emptively so the next small edit doesn't
  force an unplanned recalibration.

### Not applied
- **Q1 (per-file schema footers).** `changelog-monitor.md` carries a
  `*Schema: v2.0 | Created: 2026-04-18*` footer while `refresh-hot.md` and
  `ops/*.md` carry none. Left as a question rather than a fix — either
  direction (add footers everywhere for parity, or drop `changelog-monitor`'s
  for symmetry) is defensible, and the audit could not determine intent.

## v2.0.2 — 2026-04-18

### Follow-ups (audit-driven, second pass)

- **Canonical hash pipeline.** Both `ops/ingest.md` Step 0 and
  `changelog-monitor.md` Step 3 now feed the source body through a deterministic
  canonicalizer (preamble-strip-if-present → line-ending normalization →
  intra-line whitespace collapse → blank-line collapse → trim) before SHA-256.
  Before this change, Clipper-ingested source pages stored a hash of
  Clipper-normalized markdown while the monitor computed a hash of
  WebFetch-normalized markdown for the same URL — the two pipelines produced
  different markdown by design (Clipper strips more HTML boilerplate), so the
  monitor's hash could never match a Clipper-stored `source_hash:` even for
  byte-identical underlying pages. This broke v2.0's rerun-proof guarantee for
  every Clipper-ingested page in the wiki. The canonicalizer bridges both paths.
  LLM-mediated WebFetch nondeterminism is still out of scope by design — see
  `troubleshooting.md`'s new entry for the caveat and manual-verification
  workflow.
- **Blueprint-authoring mode threaded through startup and audit.**
  `template/CLAUDE.md`'s Blueprint-authoring Mode section now covers the
  unconditional `wiki/hot.md` read at Startup step 2 and the `drafts/` probe at
  step 3 — before this, a fresh blueprint-only clone would hit missing-file
  errors at startup. `ops/audit.md` steps 5 and 6 also gain an explicit
  blueprint-authoring callout — the log-append and `hot.md` refresh are now
  skipped transparently in blueprint-authoring workspaces rather than implicitly
  relying on CLAUDE.md's rule being cached. Same root cause as the v2.0 fix for
  other ops; v2.0 forgot to thread the rule through startup and audit.
- **`changelog-monitor.md` prose cleanup.** Three hardcoded "four"s (intro, step
  2, Slack-format note) replaced with language that references the
  `## Monitored Sources` table, so adding or removing rows no longer invalidates
  the prose. Slack message format gains an explicit rule: `🆕 items:` and
  `🆘 items:` trailing hint lines emit only when at least one matching row is
  present; messages containing only ✅ / ❌ rows omit both.
- **Blueprint Sync Rule `New scheduled task` row now mandates `CHANGELOG.md`.**
  Framed as "treat any new scheduled task as at minimum a patch version bump,
  so the Schema-version-bump row applies" — closes the gap that let the
  changelog monitor ship with a CHANGELOG entry in v2.0 despite the file never
  existing, and the follow-up in v2.0.1 get its own section only because the
  audit caught it.
- **Source-hash field doc updated.** `ops/conventions.md` now describes
  `source_hash:` as the hash of the *canonicalized* body with a pointer to the
  new `ops/ingest.md` §Hash Canonicalization section, and calls out that the
  same canonicalizer runs in the changelog monitor.
- **CHANGELOG v2.0 `### Estimate re-baselining` backfilled.** The
  `ops/ingest.md` ~7,900 → ~10,000 Chars jump that shipped with v2.0 now has a
  documented audit trail in v2.0's own section (flagged by the re-audit as
  persisting from the earlier audit-report).
- **Troubleshooting.** New entry "Changelog monitor reports 🆕 for a page I
  know hasn't changed" covers (i) legacy pre-v2.0.2 hashes that self-heal on
  next ingest, and (ii) the LLM-WebFetch nondeterminism caveat with a
  fetcher-swap recipe.
- **Token-reference recalibration.** Applied where any file's measured Chars
  crossed its documented value after this pass.

### Migration note
Source pages whose `source_hash:` was computed before v2.0.2 will produce a
one-shot hash mismatch on their next ingest or their next monitor comparison
(the canonicalized hash differs from the raw-body hash). The system
self-corrects: re-ingest once and the new canonical hash lands in the
frontmatter; the monitor will report ✅ from then on. No bulk migration
required.

## v2.0.1 — 2026-04-18

### Follow-ups (audit-driven)

- **`scheduled-tasks/changelog-monitor.md` authored.** v2.0's CHANGELOG entry
  described this file as "restored" but it was not actually landed — `!! audit all`
  caught the drift. This version lands the file to the spec already documented in
  `troubleshooting.md`'s "Changelog monitor ran but nothing was ingested." entry.
  The file ships with `[YOUR_SLACK_USER_ID]` as a personalization placeholder
  (replaced at setup time per `setup-guide.md` Step 3).
- **Blueprint Sync Rule row added** in `template/CLAUDE.md` for "New scheduled
  task" — enumerates the propagation matrix (ops/audit.md scope,
  token-reference.md file-size row, setup-guide.md copy/personalize/verify,
  README/user-guide mentions if user-visible, CLAUDE.md Directory Structure).
  Closes the gap that let v2.0 ship a CHANGELOG entry without the file.
- **`ops/audit.md` scope generalized** at the `scheduled-tasks/` level — specific
  filename enumeration replaced with "Every file directly under
  `scheduled-tasks/`" so future siblings to `refresh-hot.md` and
  `changelog-monitor.md` land in audit scope automatically.
- **`setup-guide.md` updated** — Step 2 copy table, Step 3 personalization
  (renamed to "Personalize Template Files" with `[YOUR_SLACK_USER_ID]`
  replacement instructions), Step 7 verify checklist.
- **`README.md` Key Features + `user-guide.md` Daily Workflow** gain a
  "Changelog monitor" entry.
- **`token-reference.md`** gains a file-read-cost row for
  `scheduled-tasks/changelog-monitor.md` (~5,200 chars / ~1,300 tokens at v2.0.1
  calibration).

## v2.0 — 2026-04-18

**Theme:** rerun-proofness. The entire ingest pipeline is now idempotent on duplicate input, with a content-hash dedupe primitive and timestamped immutable raw snapshots. This unblocks safe scheduled-task monitoring — a daily changelog monitor can now trigger re-ingests without fear of duplicating state. This is a breaking schema change; upgrades require touching every source page.

### Breaking changes
- **`raw/` files use timestamped naming.** Naming is now `raw/<slug>-<YYYY-MM-DD-HHMMSS>.md` instead of the old `<slug>.md` with collision-handling fallbacks. Second-precision timestamps are physically unique in single-user workflow, so the collision-handling bash snippet in `ops/ingest.md` Step 9 is gone — replaced with a simple `mv`. Existing files under the old naming stay as-is; only newly ingested files use the new scheme.
- **Source pages require `source_hash:` frontmatter.** 8-char SHA-256 hex prefix of the raw content body (preamble-stripped). This is the new dedupe primitive. Source pages without this field trigger a full regeneration on the next ingest — that's the migration path, not a bug. If you have existing v1.x source pages, expect them to be regenerated the next time their source is ingested.
- **Schema version bumped to 2.0.** Footer in `CLAUDE.md` (and blueprint template) now reads `Schema version: 2.0`.

### New behavior
- **`ops/ingest.md` Step 0: hash check.** First action of every ingest. Computes the 8-char SHA-256 prefix of the raw body, compares against the stored `source_hash:` on the existing source page. On match: deletes the inbox file, prints `No change since last ingest — skipped.`, exits cleanly. No log entry, no `hot.md` refresh, no recalibration. On mismatch: regenerates the source page from the new content (no in-place merge).
- **`!! ingest all` batch hash check (B3.6).** The batch flow hash-checks each file up front and excludes no-ops from the approval. Running `!! ingest all` twice in a row is now a guaranteed no-op on the second run.
- **Provenance footnotes in source pages.** Every curated bullet in the `## Key Takeaways` section ends with a `[^n]` footnote referencing the raw snapshot: `[^1]: raw/<filename> — fetched YYYY-MM-DD`. Makes "where did this fact come from and when" answerable from the page itself.
- **Rerun-proof guarantee.** Same input → zero state change. Re-running any ingest (manually or from a scheduled task) is safe by design.

### Force re-ingest escape hatch
If you need to regenerate a source page *without* the underlying content having changed (e.g. the previous generation was poorly worded and you want a do-over), delete the `source_hash:` line from the source page's frontmatter. The next ingest will treat the missing hash as a mismatch and regenerate. No `--force` flag, no ops change — the escape hatch is the absence of the field.

### Estimate re-baselining
- **`ops/ingest.md` recalibrated.** The new Step 0 hash-check + B3.5 batch-level pre-read + B3.6 batch hash-check + `source_hash:` discipline together pushed the file past its v1.14 headroom. Chars column bumped from ~7,900 → ~10,000; Tokens ~1,980 → ~2,500. *(This subsection was backfilled in v2.0.2 after `!! audit all` flagged the audit-trail gap — the Chars change itself shipped with v2.0 but was not accompanied by a changelog entry.)*

### New file
- **`scheduled-tasks/changelog-monitor.md` restored.** The original trigger for this migration. A daily scheduled task that fetches four monitored documentation pages, computes content hashes, compares against wiki state, and reports findings via Slack DM. Read-only — never writes files. The user runs `!! ingest` manually after reviewing the Slack summary.

### Migration note
Existing source pages without `source_hash:` will trigger a full re-ingest on next run for that source. This is the intended migration path — the next ingest for each source writes the hash in place. No bulk migration script is needed; the transition happens gradually as sources are re-ingested in normal operation.

## v1.14 — 2026-04-18

### Safety / footgun fixes
- **`!! ready` truncation-branch `clear` and `keep` now log and refresh `hot.md`.**
  In v1.13 and earlier, recovery choices on a truncated `memory.md` mutated the
  file but left no trace in `log.md` and didn't refresh `hot.md` — the "any
  wiki-state change → refresh hot.md" invariant was silently violated in that
  sub-branch, so `hot.md`'s `Last op:` could go stale and the recovery choice
  was invisible in the audit trail. `clear` now appends
  `## [YYYY-MM-DD] memory | Truncated summary cleared`; `keep` appends
  `## [YYYY-MM-DD] memory | Truncated summary acknowledged`. Both then refresh
  `hot.md`. `edit` remains a no-op (the file is untouched, so nothing to log
  or refresh).
- **Approval Rule exception broadened for `!! wrap` and `!! ready`.** The
  exception previously named specific log-entry shapes (`Session summary saved`
  / `Session summary consumed`). The new truncation-branch entries would have
  fallen outside the exception and required separate approval — defeating the
  purpose. Exception wording is now generic (`memory | …`) so all current and
  future memory-flow log entries are covered symmetrically for both commands.

### Estimate re-baselining
- **`ops/ingest.md` recalibrated.** File grew during v1.14 edits, leaving <2%
  headroom against documented Chars (well below the 10% convention). Chars
  column bumped from ~7,300 → ~7,900; Tokens ~1,830 → ~1,980.

### Scope & notation cleanup
- **README `!! audit` exception drift fixed.** `README.md`'s "Approval before
  every wiki write" bullet listed `!! wrap` and `!! ready` as "the only
  exceptions" — but `CLAUDE.md` and `user-guide.md` include `!! audit` as a
  third documented exception (read-only by default; any fix afterward goes
  through the normal approval flow). README now matches.
- **Tier 3 row renamed in `CLAUDE.md` Tiered Read Structure.** The old "Audit
  only" label semantically collided with `!! audit` (which reads nothing from
  `log.md`). Renamed to "History review" to remove the ambiguity.

### Style / readability
- **`ops/ingest.md` step 9: `$file` precondition made explicit.** Preamble now
  states that both `$WORKDIR` and `$file` must be exported in the same Bash
  invocation as the snippet. The `${file:?…}` guard still catches misuse at
  runtime; this change surfaces the requirement in prose.
- **`setup-guide.md` Step 7: verify checklist adds `wiki/pages/` subfolders.**
  Previously only `wiki/inbox/` was explicitly verified; the four
  `wiki/pages/{concepts,entities,sources,analyses}` subfolders created by
  Step 1's `mkdir -p` are now individually confirmed.

## v1.13 — 2026-04-18

### Spec additions
- **`!! ingest <URL>` branch spec'd (U1–U5).** The URL ingest path now has explicit
  steps for fetch → slug → preamble → approval to-do integration. User-guide text
  reframed as neutral "Web Clipper or URL — your choice" rather than implying
  URL is discouraged.
- **Blueprint Sync Rule: new row for `refresh-hot.md` changes.** Any edit to
  `refresh-hot.md` now propagates to `CLAUDE.md`'s hot.md Format block and
  `setup-guide.md`'s initial hot.md snippet.

### Estimate re-baselining
- **`memory.md` cost estimates raised to match the "detailed summary" spec.** Read
  cost went from ~125 → ~750 tokens. Cold-start-with-memory figure cascaded
  through `CLAUDE.md` and `user-guide.md` (~4,760 → ~5,385). Realistic `!! wrap`
  cost raised from ~2,000 → ~2,700; `!! ready` raised to ~2,800 (the command
  reads the full `memory.md` before wiping). The true-session-cost note now
  also calls out that `!! ready` reads the full `memory.md` before wiping
  (previously invisible in the estimate).

### Safety / footgun fixes
- **`!! wrap` pre-write safeguard extended to `TRUNCATED_ACKNOWLEDGED`.** Previously
  only `WRAPPED` triggered the overwrite warning, so a preserved truncated summary
  could be silently destroyed by the next `!! wrap`. The safeguard now catches
  both preserve states with differentiated warning wording. `keep` is no longer a
  one-shot preservation.

### Scope & notation cleanup
- **Path notation normalized to bare `@scheduled-tasks/...`.** The `@Library/`
  prefix was removed from all 9 references in `CLAUDE.md`. Setup-time
  find-and-replace step dropped from `setup-guide.md`. Paths are now
  working-folder-relative regardless of the folder name.
- **AUDIT scope clarification in `ops/audit.md`.** Blueprint files are not wiki
  pages, so `ops/conventions.md` does not apply. The Blueprint Sync Rule governs
  any downstream propagation after an audit fix.

### Style / readability
- **Footer-block discipline wording unified across `CLAUDE.md` + `user-guide.md`.**
  Both files now describe the footer as "5 command-hint lines + blank separator +
  💡 tip line = 7 physical lines total," resolving the ambiguous "six lines" /
  "five command lines" framing.
- **`cd "$WORKDIR"` reminder added at Steps 2, 4, and 7 of `setup-guide.md`.**
  The cwd-discipline rule was previously stated only at the end of Step 1;
  forgotten `cd` in a fresh sandbox could land files in the session root.
  Reminder is now repeated where it can fail.

### Operator note
- **Blueprint-authoring workspaces:** when an op runs against a workspace that
  contains only `blueprint/` (no live `wiki/`, no `scheduled-tasks/`), log append
  + `hot.md` refresh are skipped transparently rather than bootstrapping files
  that shouldn't live there.

## v1.12 and earlier

Version history prior to v1.13 is implicit in `troubleshooting.md` — each
Prevention bullet references the version in which the corresponding fix landed
(v1.10 mid-session guard, v1.11 `keep` option, v1.12 broadened approval scope
and ingest batch pre-read, etc.).
