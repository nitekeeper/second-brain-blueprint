# Blueprint Changelog

> Version history for the blueprint schema. See `troubleshooting.md` for specific
> symptom/cause/fix entries tied to these versions.

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
  through `CLAUDE.md` and `user-guide.md` (~4,380 → ~5,005). Realistic
  `!! wrap`/`!! ready` cost raised from ~2,000 → ~2,700. The true-session-cost
  note now also calls out that `!! ready` reads the full `memory.md` before
  wiping (previously invisible in the estimate).

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
