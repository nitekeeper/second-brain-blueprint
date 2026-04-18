# Blueprint Changelog

> Version history for the blueprint schema. See `troubleshooting.md` for specific
> symptom/cause/fix entries tied to these versions.

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
