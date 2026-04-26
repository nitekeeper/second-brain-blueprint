---
name: AUD-2026-04-25-007 Fixes + CHANGELOG Audit Scope Removal
description: Fix AUD-030 (migrate.md v2.2→v2.3 missing blueprint-sync.md copy), AUD-031 (reference.md missing ROADMAP.md), and remove CHANGELOG.md from audit scope permanently with exclusion note
type: project
---

# Design: AUD-2026-04-25-007 Fixes + CHANGELOG Audit Scope Removal

## Summary

Three logical changes across five files. No schema version bump. No cascade to `template/CLAUDE.md`.

---

## Change 1 — Fix AUD-030: `migrate.md` v2.2→v2.3 path missing `blueprint-sync.md` copy

**File:** `template/scheduled-tasks/ops/migrate.md`

**Problem:** The v2.2→v2.3 approval request lists `blueprint-sync.md` as implicitly UNTOUCHED ("all other ops files preserved"). But the current v2.3 template has two new cascade rows (`Query Routing Rule change` and `Ops file change that is copied by the v2.1→v2.3 migration step g`) that a v2.2 migrator never receives. A blueprint maintainer who migrates from v2.2 and then edits the Query Routing Rule will silently skip the `migrate.md` step-c update.

**Fix:**

1. In the approval request block, add to the Files UPDATED section:
   ```
   scheduled-tasks/ops/blueprint-sync.md  (two new v2.3 cascade rows added)
   ```
2. In execution steps, add after step `c2`:
   ```
   c3. Copy blueprint/template/scheduled-tasks/ops/blueprint-sync.md → scheduled-tasks/ops/blueprint-sync.md
   ```

`blueprint-sync.md` is now explicitly UPDATED, so it falls out of the "all other ops files preserved" UNTOUCHED umbrella naturally — no additional wording change needed there.

---

## Change 2 — Fix AUD-031: `reference.md` blueprint/ tree missing `ROADMAP.md`

**File:** `template/scheduled-tasks/ops/reference.md`

**Problem:** The `blueprint/` node in the directory tree lists `CHANGELOG.md` then immediately `template/`. `ROADMAP.md` is a tracked first-class blueprint file — referenced in `blueprint-sync.md` as a cascade target for "New skill bundle added" — but is absent from the tree.

**Fix:** Insert `├── ROADMAP.md` between `CHANGELOG.md` and `template/` in the blueprint/ node:

```
├── CHANGELOG.md
├── ROADMAP.md
├── template/
```

---

## Change 3 — Remove CHANGELOG.md from `!! audit all` scope permanently

**Files:** `template/scheduled-tasks/ops/audit.md`, `user-guide.md`

**Problem:** CHANGELOG.md was correctly removed from audit scope in v2.0.21 ("a changelog is an append-only log — auditing it for logic errors is not meaningful"). AUD-026 re-added it. AUD-027 updated user-guide.md to reflect the higher token cost. CHANGELOG.md does not contain auditable logic — it is append-only narrative. Auditing it wastes ~31,100 tokens per `!! audit all` run and created the cascade-miss class problem (auditors correcting narrative figures inside CHANGELOG caused further cascades).

**Fix in `audit.md`:**

1. Remove `- blueprint/CHANGELOG.md` from the `!! audit all` scope list.
2. Add one exclusion note directly after the scope list (before `## If !! audit [Page Name]`):
   > `> **Note:** CHANGELOG.md is excluded — it is an append-only log and is not auditable for logic errors.`
3. In the Notes section:
   - Remove `blueprint/CHANGELOG.md` from the `estimate_tokens` command string.
   - Update the token range from `~60,000–70,000` to `~35,000–45,000`.
   - Remove the parenthetical `(CHANGELOG.md alone accounts for ~30,000+ tokens and grows with every audit cycle)`.

**Fix in `user-guide.md`:**

- Update the "Audit all (full blueprint)" token row from:
  `~60,000–70,000 (CHANGELOG.md alone accounts for ~30,000+ tokens and grows with every audit cycle)`
  to: `~35,000–45,000`

**Token math:** AUD-007 appendix total = ~68,929. CHANGELOG.md = ~31,100. Without it: ~37,829 → rounded range `~35,000–45,000`.

---

## Change 4 — Update AUD-007 audit report

**File:** `audits/AUD-2026-04-25-007.md`

- AUD-030 Status: `OPEN` → `RESOLVED`
- AUD-031 Status: `OPEN` → `RESOLVED`
- Action item checkboxes: `- [ ]` → `- [x]` for both entries

---

## Files Affected

| File | Change |
|---|---|
| `template/scheduled-tasks/ops/migrate.md` | Add c3 step; move blueprint-sync.md to UPDATED block |
| `template/scheduled-tasks/ops/reference.md` | Add ROADMAP.md to blueprint/ tree node |
| `template/scheduled-tasks/ops/audit.md` | Remove CHANGELOG from scope; add exclusion note; update token estimate |
| `user-guide.md` | Update "Audit all" token row |
| `audits/AUD-2026-04-25-007.md` | Mark AUD-030 and AUD-031 RESOLVED |

## Out of Scope

- No `template/CLAUDE.md` changes (no schema or startup behavior changes)
- No `blueprint-sync.md` changes (existing cascade rows are not affected)
- No `CHANGELOG.md` entry (ops-file correction, not a schema version bump)
