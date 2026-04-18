# Blueprint Changelog

> Version history for the blueprint schema. See `troubleshooting.md` for specific
> symptom/cause/fix entries tied to these versions.

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
