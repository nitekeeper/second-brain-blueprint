# Design: Apply AUD-2026-04-25-005 Findings

**Date:** 2026-04-25
**Audit report:** `audits/AUD-2026-04-25-005.md`
**Approach:** Single commit — all 4 findings + audit report update

---

## Scope

Four findings, three files edited, one audit report updated.

| File | Findings | Change summary |
|---|---|---|
| `template/scheduled-tasks/ops/migrate.md` | AUD-023, AUD-024 | Two edits to the v2.2→v2.3 path |
| `template/scheduled-tasks/ops/blueprint-sync.md` | AUD-025 | Two new rows in the cascade table |
| `template/scheduled-tasks/ops/audit.md` | AUD-026 | Notes section estimate command and range updated |
| `audits/AUD-2026-04-25-005.md` | All 4 | Status → RESOLVED, action items checked off |

Blueprint-authoring mode is active (no `wiki/` at root) — `wiki/log.md` appends and `hot.md` refreshes are skipped.

---

## Detailed Edits

### migrate.md — AUD-023 (CRITICAL)

In the step c replacement block, insert one bullet **between** the "directly answered" bullet and the "loosely related" bullet:

```
- If the result **directly answered the question AND Step 1 returned partial wiki content** → ingest the web result; answer citing both the wiki pages and the web result
```

Full corrected Step 2 block in step c:

```
**Step 2 — Web Search**
Runs when: (a) wiki returned nothing useful, OR (b) question needs current or recent information.
- Search and summarize
- If the result **directly answered the question** → silently save to `wiki/inbox/` and read `@scheduled-tasks/ops/ingest.md` to ingest it
- If the result **directly answered the question AND Step 1 returned partial wiki content** → ingest the web result; answer citing both the wiki pages and the web result
- If the result is **loosely related but did not answer** → skip ingest; use partial findings to inform Step 3
```

### migrate.md — AUD-024 (CRITICAL)

Two sub-edits:

**Sub-edit 1 — approval request block.** Replace the entire UPDATED+UNTOUCHED block:

```
Files UPDATED:
  CLAUDE.md  (Query Routing Rule section replaced — behavior change, no size change)

Files UNTOUCHED:
  wiki/  (all pages, index, log, hot preserved)
  memory.md, raw/, drafts/
  scheduled-tasks/ops/  (all ops files preserved)
  scripts/  (all scripts preserved)
  sqlite-query skill (if installed)
```

With:

```
Files UPDATED:
  CLAUDE.md  (Query Routing Rule section replaced — behavior change, no size change)
  scheduled-tasks/ops/conventions.md  (Filing Answers step labels updated to v2.3 numbering)

Files UNTOUCHED:
  wiki/  (all pages, index, log, hot preserved)
  memory.md, raw/, drafts/
  scheduled-tasks/ops/  (all other ops files preserved)
  scripts/  (all scripts preserved)
  sqlite-query skill (if installed)
```

**Sub-edit 2 — execution steps.** After step c (and before step d), insert:

```
c2. Copy `blueprint/template/scheduled-tasks/ops/conventions.md` → `scheduled-tasks/ops/conventions.md`
```

### blueprint-sync.md — AUD-025 (WARNING)

Append two new rows to the cascade table (after the existing last row):

```
| Query Routing Rule change | `blueprint/template/CLAUDE.md` (always) + `blueprint/template/scheduled-tasks/ops/migrate.md` (update the step c replacement block in the active migration path to match the new rule) |
| Ops file change that is copied by the v2.1→v2.3 migration step g | `blueprint/template/scheduled-tasks/ops/migrate.md` (verify the updated file is listed in step g; add it if absent) |
```

### audit.md — AUD-026 (WARNING)

In the Notes section, replace the existing estimate/range sentence:

**Old:**
```
For `!! audit all`, expect ~30,000–47,000 tokens of reads for the tracked files. Run `python scripts/estimate_tokens.py blueprint/README.md blueprint/setup-guide.md blueprint/user-guide.md blueprint/troubleshooting.md blueprint/template/CLAUDE.md blueprint/template/scheduled-tasks/refresh-hot.md blueprint/template/scheduled-tasks/ops/*.md blueprint/skills/sqlite-query/*.md blueprint/skills/claude-code-enhanced/*.md` for a live estimate. Warn the user up front if the session is already close to context limits.
```

**New:**
```
For `!! audit all`, expect ~60,000–70,000 tokens of reads for the tracked files (CHANGELOG.md alone accounts for ~30,000+ tokens and grows with every audit cycle). Run `python scripts/estimate_tokens.py blueprint/README.md blueprint/setup-guide.md blueprint/user-guide.md blueprint/troubleshooting.md blueprint/CHANGELOG.md blueprint/template/CLAUDE.md blueprint/template/scheduled-tasks/refresh-hot.md blueprint/template/scheduled-tasks/ops/*.md blueprint/skills/sqlite-query/*.md blueprint/skills/claude-code-enhanced/*.md` for a live estimate. Warn the user up front if the session is already close to context limits.
```

### audits/AUD-2026-04-25-005.md — All findings

For each of the four findings (AUD-023, AUD-024, AUD-025, AUD-026):
- Set `**Status**` field to `RESOLVED`
- Check off the corresponding action item line (`- [ ]` → `- [x]`)

---

## Constraints

- No changes to `template/CLAUDE.md` — it already has the correct Step 2 block (source of truth)
- No changes to `template/scheduled-tasks/ops/conventions.md` — already fixed by AUD-018
- Single commit; commit message format matches AUD-004 precedent
