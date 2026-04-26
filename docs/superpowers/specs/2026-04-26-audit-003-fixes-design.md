# Design: Fix AUD-2026-04-26-003 Findings (AUD-052, AUD-053, AUD-054)

**Date:** 2026-04-26
**Scope:** `template/scheduled-tasks/ops/session-hygiene.md`, `template/scheduled-tasks/ops/audit.md`, `audits/AUD-2026-04-26-003.md`
**Approach:** Single commit — all edits + audit report status updates together

---

## Summary

Three findings from audit AUD-2026-04-26-003:

- **AUD-052** (WARNING) — `ROADMAP.md` referenced in `reference.md` tree and `blueprint-sync.md` cascade but audit claimed file does not exist. Finding was based on incorrect analysis — `ROADMAP.md` does exist (committed in `cf5a932`). No file changes needed; status updated to RESOLVED only.
- **AUD-053** (STYLE) — `session-hygiene.md` `!![op]` placeholder produces `!!ingest` / `!!lint` / `!!audit` — missing the standard command space. Fix: add space between `!!` and `[op]` in both template blocks.
- **AUD-054** (STYLE) — `audit.md` step 0 file-check references `python scripts/file_check.py audits/` without a blueprint-authoring mode fallback, inconsistent with the fallback pattern established in the Note section. Fix: extend the step 0 parenthetical to include the fallback.

---

## Changes to `template/scheduled-tasks/ops/session-hygiene.md`

Two in-place substitutions in the template blocks.

### Edit 1 — Intercept message: add space in `!![op]`

```
Before:
⚠️  A !![op] operation completed earlier in this session.

After:
⚠️  A !! [op] operation completed earlier in this session.
```

### Edit 2 — Post-op advisory block: add space in `!![op]`

```
Before:
⚠️  Session advisory: This session has completed a !![op] operation and the

After:
⚠️  Session advisory: This session has completed a !! [op] operation and the
```

---

## Changes to `template/scheduled-tasks/ops/audit.md`

One in-place substitution in step 0.

### Edit 3 — Step 0: extend file-check parenthetical with blueprint-authoring mode fallback

```
Before:
Check whether an `audits/` directory exists (`python scripts/file_check.py audits/`).

After:
Check whether an `audits/` directory exists (`python scripts/file_check.py audits/`; blueprint-authoring mode: `python template/scripts/file_check.py audits/` or `ls audits/`).
```

---

## Changes to `audits/AUD-2026-04-26-003.md`

Status updates and action item checkoffs for all three findings.

### AUD-052
- Set `**Status**` field: `OPEN` → `RESOLVED`
- Action Items: `- [ ] \`AUD-2026-04-26-052\`` → `- [x] \`AUD-2026-04-26-052\``

### AUD-053
- Set `**Status**` field: `OPEN` → `RESOLVED`
- Action Items: `- [ ] \`AUD-2026-04-26-053\`` → `- [x] \`AUD-2026-04-26-053\``

### AUD-054
- Set `**Status**` field: `OPEN` → `RESOLVED`
- Action Items: `- [ ] \`AUD-2026-04-26-054\`` → `- [x] \`AUD-2026-04-26-054\``

---

## What Is NOT Changing

- `ROADMAP.md` — file already exists with richer content than the audit's minimum placeholder; no edit needed.
- `reference.md` — already lists `ROADMAP.md` correctly in the blueprint/ tree; no edit needed.
- `blueprint-sync.md` — already references `blueprint/ROADMAP.md` in the "New skill bundle added" cascade; no edit needed.
- No structural changes to `session-hygiene.md` or `audit.md` — only the two `!![op]` occurrences and the one step 0 parenthetical are touched.
- No other files touched.
