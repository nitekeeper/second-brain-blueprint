# Design: Fix AUD-2026-04-26-002 Findings (AUD-050, AUD-051)

**Date:** 2026-04-26
**Scope:** `template/scheduled-tasks/ops/migrate.md`, `audits/AUD-2026-04-26-002.md`
**Approach:** Single-pass edit — all changes in one commit

---

## Summary

Two STYLE findings from audit AUD-2026-04-26-002, both in `migrate.md`:

- **AUD-050** — v2.1→v2.3 confirm message states stale `~1,080` token figure; correct value is `~2,100` (per README.md and user-guide.md post-AUD-048).
- **AUD-051** — Both migration paths overwrite `refresh-hot.md` without a preceding backup step; rollback sections omit `refresh-hot.md` restoration.

---

## Changes to `template/scheduled-tasks/ops/migrate.md`

All edits are in-place text substitutions in document order.

### Edit 1 — v2.2→v2.3 Approval request: refresh-hot.md line

Add `; backed up to backups/` to the refresh-hot.md entry so the approval request accurately reflects that the file will be backed up.

```
Before:
  scheduled-tasks/refresh-hot.md  (Step 3 updated to detect claude-code-enhanced skill)

After:
  scheduled-tasks/refresh-hot.md  (Step 3 updated to detect claude-code-enhanced skill; backed up to backups/)
```

### Edit 2 — v2.2→v2.3 Backup steps: insert b4

Insert `b4` immediately after `b3` and before `c`, following the established backup-before-overwrite pattern.

```
b4. Copy `scheduled-tasks/refresh-hot.md` → `backups/refresh-hot.md-v2.2-<YYYY-MM-DD>.bak`
```

### Edit 3 — v2.2→v2.3 Confirm: add refresh-hot.md backup to list

```
Before:
Backups saved to `backups/CLAUDE.md-v2.2-<date>.bak`, `backups/conventions.md-v2.2-<date>.bak`, and `backups/blueprint-sync.md-v2.2-<date>.bak` — delete when satisfied.

After:
Backups saved to `backups/CLAUDE.md-v2.2-<date>.bak`, `backups/conventions.md-v2.2-<date>.bak`, `backups/blueprint-sync.md-v2.2-<date>.bak`, and `backups/refresh-hot.md-v2.2-<date>.bak` — delete when satisfied.
```

### Edit 4 — v2.2→v2.3 Rollback: add refresh-hot.md restoration

Insert after the `blueprint-sync.md` rename, before `revert Schema:`.

```
rename backups/refresh-hot.md-v2.2-<date>.bak → scheduled-tasks/refresh-hot.md;
```

### Edit 5 — v2.1→v2.3 Approval request: refresh-hot.md line

Same addition as Edit 1, for the v2.1→v2.3 path.

```
Before:
  scheduled-tasks/refresh-hot.md  (Step 3 updated to detect claude-code-enhanced skill)

After:
  scheduled-tasks/refresh-hot.md  (Step 3 updated to detect claude-code-enhanced skill; backed up to backups/)
```

### Edit 6 — v2.1→v2.3 Backup steps: insert g1.5

Insert `g1.5` immediately after `g` and before `g2`.

```
g1.5. Copy `scheduled-tasks/refresh-hot.md` → `backups/refresh-hot.md-v2.1-<YYYY-MM-DD>.bak`
```

### Edit 7 — v2.1→v2.3 Confirm: fix token figure + add refresh-hot.md backup

Fixes AUD-050 (token figure) and AUD-051 (backup list) in the same block.

```
Before:
"Migration complete. Cold-start: ~7,780 → ~1,080 tokens. Query routing is now wiki-first.
Backups saved to `backups/CLAUDE.md-v2.1-<date>.bak` and `backups/conventions.md-v2.1-<date>.bak` — delete when satisfied."

After:
"Migration complete. Cold-start: ~7,780 → ~2,100 tokens. Query routing is now wiki-first.
Backups saved to `backups/CLAUDE.md-v2.1-<date>.bak`, `backups/conventions.md-v2.1-<date>.bak`, and `backups/refresh-hot.md-v2.1-<date>.bak` — delete when satisfied."
```

### Edit 8 — v2.1→v2.3 Rollback: add refresh-hot.md restoration

Insert after the `conventions.md` rename, before `revert Schema:`.

```
rename backups/refresh-hot.md-v2.1-<date>.bak → scheduled-tasks/refresh-hot.md;
```

---

## Changes to `audits/AUD-2026-04-26-002.md`

- Set `Status` to `RESOLVED` in the AUD-050 finding table.
- Set `Status` to `RESOLVED` in the AUD-051 finding table.
- Check off both action items in the Action Items section (`- [ ]` → `- [x]`).

---

## What is NOT changing

- No other files touched.
- No structural changes to `migrate.md` — step labels, section headings, and ordering are preserved except for the inserted b4 and g1.5 steps.
- The v2.2→v2.3 confirm message token figures are not mentioned (that path has no token figure in its confirm) — no change needed there.
