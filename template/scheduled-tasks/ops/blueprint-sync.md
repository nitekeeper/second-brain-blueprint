# Blueprint Sync Rule

Read this file whenever you are about to edit any file under `blueprint/` or `template/`.

**CRITICAL: Whenever the schema, operations, or conventions are updated, the blueprint files must also be updated. Skipping this step causes template drift and breaks new wiki setups.**

| Change type | Files to update |
|---|---|
| Schema or startup change | `blueprint/README.md`, `blueprint/setup-guide.md`, `blueprint/user-guide.md`, `blueprint/template/CLAUDE.md` |
| Operation step change | `blueprint/user-guide.md`, `blueprint/template/CLAUDE.md`, `blueprint/template/scheduled-tasks/ops/[op].md` |
| Refresh-hot.md change | `blueprint/template/scheduled-tasks/refresh-hot.md`, `blueprint/template/CLAUDE.md` (hot.md Format block), `blueprint/setup-guide.md` (initial hot.md snippet) |
| New known issue or fix | `blueprint/troubleshooting.md` |
| Schema change that introduces a new footgun | `blueprint/troubleshooting.md` in addition to the Schema row above |
| Setup step change | `blueprint/setup-guide.md` |
| File-size or cost change | (token-reference.md removed in v2.2 — no propagation required) |
| Conventions change | `blueprint/template/scheduled-tasks/ops/conventions.md` |
| Any schema change | `blueprint/template/CLAUDE.md` always |
| Footer content change | ALL of: `blueprint/template/CLAUDE.md`, `blueprint/setup-guide.md`, `blueprint/user-guide.md` (keep them identical) |
| Schema version bump | `blueprint/CHANGELOG.md` (new section) in addition to any rows above |
| New scheduled task | `blueprint/template/scheduled-tasks/<name>.md` + `ops/audit.md` (informational parenthetical) + `ops/token-reference.md` (removed in v2.2; skip) + `setup-guide.md` + `README.md` and `user-guide.md` if user-visible + `template/CLAUDE.md` Directory Structure + `CHANGELOG.md` |
| New skill bundle added | `blueprint/skills/<skill>/` + `blueprint/user-guide.md` + `blueprint/setup-guide.md` + `blueprint/ROADMAP.md` + `ops/conventions.md` if skill introduces a new hook contract |

> **Non-cascade exception:** For startup or schema changes that are agent-internal with no user-facing behavioral impact, listed cascade files may require no content update. Document any deliberate non-cascade in `CHANGELOG.md` with explicit justification.

**Versioning split.** CLAUDE.md footer and `hot.md`'s `Schema:` field track `X.Y` only. Patch-level bumps add a new `CHANGELOG.md` section but do not move the footer or `hot.md` field. Minor/major bumps propagate through "Any schema change" row.

After updating blueprint files, append to `log.md`: `## [YYYY-MM-DD] sync | Blueprint synced — [what changed]` (≤500 chars). For audit-driven edits, `ops/audit.md` step 5 mandates `## [YYYY-MM-DD] audit | [fix summary]` instead — do not write both.

**Blueprint-authoring mode:** If `wiki/` absent at working folder root, skip all `log.md` appends and `hot.md` refreshes — see CLAUDE.md Blueprint-authoring mode note.
