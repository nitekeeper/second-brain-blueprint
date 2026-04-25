# Claude Code Enhanced — Slash Command Wrappers

This file is read when the user invokes `/wrap`, `/ready`, or `/migrate` in Claude Code CLI.
These are thin wrappers — all logic lives in the ops files and scripts.

---

## /wrap

Equivalent to `!! wrap`. Read `@scheduled-tasks/ops/session-memory.md` and follow the `!! wrap` flow.

## /ready

Equivalent to `!! ready`. Read `@scheduled-tasks/ops/session-memory.md` and follow the `!! ready` flow.

## /migrate

Equivalent to `!! migrate`. Read `@scheduled-tasks/ops/migrate.md` and follow the migration flow.

---

> **Blueprint-authoring only:** `/sync` is intentionally not listed in SKILL.md or user-guide.md. It is a developer tool for blueprint maintainers — use it when editing blueprint files to check cascade requirements. Regular wiki users do not need it.

## /sync

Equivalent to triggering the blueprint sync rule. Read `@scheduled-tasks/ops/blueprint-sync.md` and confirm which files need updating based on the change just made.
