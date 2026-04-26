# Design: Fix AUD-2026-04-25-006 Findings (027, 028, 029)

**Date:** 2026-04-25
**Audit Report:** AUD-2026-04-25-006
**Severity:** 3× WARNING (Overall Risk: HIGH)
**Files affected:** `user-guide.md`, `template/scheduled-tasks/ops/migrate.md`

---

## Overview

Three findings from audit cycle AUD-2026-04-25-006, all in two files:

| Finding | File | Nature |
|---|---|---|
| AUD-027 | `user-guide.md` | Stale token estimate in Token Awareness table |
| AUD-028 | `migrate.md` | `hot.md` listed as UNTOUCHED in both approval blocks, but patched by both migration paths |
| AUD-029 | `migrate.md` | Rollback procedures do not revert `conventions.md`; no backup taken during migration |

---

## AUD-027 — Token Awareness table (`user-guide.md`)

### Problem

The Token Awareness table at line 228 of `user-guide.md` shows `~30,000–47,000` for `!! audit all`. AUD-026 updated `audit.md` to `~60,000–70,000` and added `CHANGELOG.md` to the estimate command, but did not cascade to `user-guide.md`. The two sources now contradict each other.

### Fix

Update the `!! audit all` row in the Token Awareness table:

**Before:**
```
| Audit all (full blueprint) | ~30,000–47,000 |
```

**After:**
```
| Audit all (full blueprint) | ~60,000–70,000 (CHANGELOG.md alone accounts for ~30,000+ tokens and grows with every audit cycle) |
```

---

## AUD-028 — `hot.md` disclosure in approval blocks (`migrate.md`)

### Problem

Both migration approval blocks list `wiki/ (all pages, index, log, hot preserved)` in `Files UNTOUCHED`, while immediately following steps explicitly patch `hot.md` (step e for v2.2→v2.3; step i for v2.1→v2.3). This violates the Core Rules transparency requirement.

### Fix

**v2.2→v2.3 approval block:**

Move `wiki/hot.md` to `Files UPDATED` and remove `hot` from the UNTOUCHED line.

```
Files UPDATED:
  CLAUDE.md  (Query Routing Rule section replaced — behavior change, no size change)
  scheduled-tasks/ops/conventions.md  (Filing Answers step labels updated to v2.3 numbering)
  wiki/hot.md  (Schema: v2.2 → v2.3)

Files UNTOUCHED:
  wiki/  (all pages, index, log preserved)
  memory.md, raw/, drafts/
  scheduled-tasks/ops/  (all other ops files preserved)
  scripts/  (all scripts preserved)
  sqlite-query skill (if installed)
```

**v2.1→v2.3 approval block:**

Move `wiki/hot.md` to `Files UPDATED` and remove `hot` from the UNTOUCHED line.

```
Files UPDATED:
  scheduled-tasks/ops/audit.md       (recalibration sections removed)
  scheduled-tasks/ops/ingest.md      (bash → Python, post-op advisory added)
  scheduled-tasks/ops/lint.md        (bash → Python, post-op advisory added)
  scheduled-tasks/ops/conventions.md (updated for v2.3)
  wiki/hot.md  (Schema bumped to v2.3; Python: field added)

Files UNTOUCHED:
  wiki/  (all pages, index, log preserved)
  memory.md, raw/, drafts/
  sqlite-query skill (if installed)
```

---

## AUD-029 — Rollback gap: `conventions.md` not backed up or reverted (`migrate.md`)

### Problem

Both migration paths copy a new `conventions.md` over the user's existing file (v2.2→v2.3 step c2; v2.1→v2.3 step g), but neither path backs up the original. The rollback instructions only restore `CLAUDE.md` and revert `hot.md`'s Schema field. After rollback, `conventions.md` retains v2.3 step labels while `CLAUDE.md` uses pre-v2.3 routing — reintroducing the AUD-018 step-label mismatch.

### Approach

**Approach A (chosen):** Back up `conventions.md` alongside `CLAUDE.md` during migration, enabling fully automated rollback consistent with the existing backup-and-rename pattern.

### Fix

#### Step b2 — added to both migration paths (after existing step b)

**v2.2→v2.3:**
```
b2. Copy `scheduled-tasks/ops/conventions.md` → `backups/conventions.md-v2.2-<YYYY-MM-DD>.bak`
```

**v2.1→v2.3:**
```
b2. Copy `scheduled-tasks/ops/conventions.md` → `backups/conventions.md-v2.1-<YYYY-MM-DD>.bak`
```

#### Confirm messages — updated to mention conventions.md backup

**v2.2→v2.3:**
```
"Migration complete. Query routing is now wiki-first.
Backups saved to `backups/CLAUDE.md-v2.2-<date>.bak` and `backups/conventions.md-v2.2-<date>.bak` — delete when satisfied."
```

**v2.1→v2.3:**
```
"Migration complete. Cold-start: ~7,780 → ~1,080 tokens. Query routing is now wiki-first.
Backups saved to `backups/CLAUDE.md-v2.1-<date>.bak` and `backups/conventions.md-v2.1-<date>.bak` — delete when satisfied."
```

#### Rollback section — both bullets extended

```
- **v2.2→v2.3:** Rename `backups/CLAUDE.md-v2.2-<date>.bak` → `CLAUDE.md`; rename `backups/conventions.md-v2.2-<date>.bak` → `scheduled-tasks/ops/conventions.md`; revert `Schema:` in `hot.md` to `v2.2`.
- **v2.1→v2.3:** Rename `backups/CLAUDE.md-v2.1-<date>.bak` → `CLAUDE.md`; rename `backups/conventions.md-v2.1-<date>.bak` → `scheduled-tasks/ops/conventions.md`; revert `Schema:` in `hot.md` to `v2.1`. All new ops files and scripts/ are inert without the v2.1 `CLAUDE.md` referencing them.
```

---

## Audit report update

After all fixes are applied, mark findings 027, 028, 029 as RESOLVED in `audits/AUD-2026-04-25-006.md` by checking their action items (`- [x]`).

---

## Out of scope

- CLAUDE.md backup not being disclosed in approval blocks (pre-existing omission, not flagged by AUD-006)
- Any other files referencing token estimates (no others found)
