# Blueprint Changelog

> Version history for the blueprint schema. See `troubleshooting.md` for specific
> symptom/cause/fix entries tied to these versions.

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
