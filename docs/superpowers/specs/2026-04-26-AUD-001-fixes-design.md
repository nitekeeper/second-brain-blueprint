# Design: Fix AUD-2026-04-26-001 Findings (AUD-046 through AUD-049)

**Date:** 2026-04-26  
**Audit Report:** AUD-2026-04-26-001  
**Approach:** Option B — script-computed token figures; fix all stale occurrences  

---

## Overview

Four findings from AUD-2026-04-26-001: one WARNING and three STYLE. All fixes are surgical — no behavioral redesign, no new files. Token figures derived from running `estimate_tokens.py` directly.

---

## Finding AUD-046 (WARNING) — `migrate.md` v2.2→v2.3 step c missing "Worth filing?" bullet

**File:** `template/scheduled-tasks/ops/migrate.md`

The v2.2→v2.3 step c replacement block's Step 2 bullet list is missing the fourth bullet present in `template/CLAUDE.md`:
> `- After summarizing: ask "Worth filing this as an analysis page?" — if yes, read \`@scheduled-tasks/ops/conventions.md\` first`

**Change:** Append that bullet immediately after the "loosely related but did not answer" bullet, before the `**Step 3 — Training Knowledge**` heading inside the replacement block.

No other changes to the replacement block. The v2.1→v2.3 path is unaffected (it copies `template/CLAUDE.md` wholesale).

---

## Finding AUD-047 (STYLE) — Migration paths don't propagate AUD-045 `refresh-hot.md` fix; cascade table gap

**Files:** `template/scheduled-tasks/ops/migrate.md`, `template/scheduled-tasks/ops/blueprint-sync.md`

`refresh-hot.md` (updated by AUD-045 to detect `claude-code-enhanced`) is not copied by either migration path. The blueprint-sync.md cascade table has no rule requiring migrate.md to be updated when `refresh-hot.md` changes.

### migrate.md — v2.2→v2.3 path

1. **Approval request** — add to `Files UPDATED`:
   ```
     scheduled-tasks/refresh-hot.md  (Step 3 updated to detect claude-code-enhanced skill)
   ```

2. **Execution steps** — add after step `c3`:
   ```
   c4. Copy `blueprint/template/scheduled-tasks/refresh-hot.md` → `scheduled-tasks/refresh-hot.md`
   ```

### migrate.md — v2.1→v2.3 path

3. **Approval request** — add to `Files UPDATED`:
   ```
     scheduled-tasks/refresh-hot.md  (Step 3 updated to detect claude-code-enhanced skill)
   ```

4. **Execution steps** — add after step `g`:
   ```
   g2. Copy `blueprint/template/scheduled-tasks/refresh-hot.md` → `scheduled-tasks/refresh-hot.md`
   ```

### blueprint-sync.md — cascade table

5. Update the `Refresh-hot.md change` row to include `migrate.md`:

   From:
   ```
   | Refresh-hot.md change | `blueprint/template/scheduled-tasks/refresh-hot.md`, `blueprint/template/CLAUDE.md` (hot.md Format block), `blueprint/setup-guide.md` (initial hot.md snippet) |
   ```
   To:
   ```
   | Refresh-hot.md change | `blueprint/template/scheduled-tasks/refresh-hot.md`, `blueprint/template/CLAUDE.md` (hot.md Format block), `blueprint/setup-guide.md` (initial hot.md snippet), `blueprint/template/scheduled-tasks/ops/migrate.md` (add copy step for both migration paths; update Files UPDATED lists) |
   ```

---

## Finding AUD-048 (STYLE) — Cold-start token estimate (~1,080) stale

**Files:** `README.md`, `user-guide.md`

Figures from `estimate_tokens.py` (chars ÷ 4):
- `template/CLAUDE.md`: ~2,013 tokens
- `wiki/hot.md`: ~80 tokens (from audit appendix)
- Cold-start total: 2,013 + 80 = **~2,093 → round to ~2,100**
- `template/scheduled-tasks/ops/session-memory.md`: ~1,320 tokens
- `memory.md` full snapshot (estimated from SNAPSHOT format, ~700 chars): ~175 tokens
- `!! ready` total: 2,093 + 1,320 + 175 = **~3,588 → round to ~3,500**

Note: The audit recommended ~2,000 and ~2,750; those figures are superseded by the script output.  
Note: The historical `migrate.md` confirmation message ("Cold-start: ~7,780 → ~1,080 tokens") describes the state at v2.1→v2.3 migration time and is intentionally left unchanged.

### `README.md` changes (1)

| Line | From | To |
|---|---|---|
| "Lean startup" bullet | `~1,080 tokens` | `~2,100 tokens` |

### `user-guide.md` changes (8)

| Location | From | To |
|---|---|---|
| Line 9 — CLAUDE.md item | `(~1,000 tokens)` | `(~2,000 tokens)` |
| Line 12 — intro cold-start total | `~1,080 tokens` | `~2,100 tokens` |
| Line 14 — `!! ready` intro | `~1,830 tokens total` | `~3,500 tokens total` |
| Line 144 — clean-slate note | `~1,080 tokens` | `~2,100 tokens` |
| Line 221 — Token Awareness table: Cold start | `~1,080` | `~2,100` |
| Line 222 — Token Awareness table: `!! ready` | `~1,830` | `~3,500` |
| Line 231 — re-orient note | `~1,080 tokens` | `~2,100 tokens` |
| Line 252 — Tips: "starting fresh" | `~1,080 tokens` | `~2,100 tokens` |

---

## Finding AUD-049 (STYLE) — `audit-report-template.md` lists unreachable `MEDIUM` risk level

**File:** `docs/audit-report-template.md`

The Overall Risk line lists `MEDIUM` as a valid option, but the derivation rule maps only four states: CRITICAL, HIGH, LOW, CLEAN.

**Change:** Remove `/ \`MEDIUM\`` from the Overall Risk line.

From:
```
**Overall Risk:** `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` / `CLEAN`
```
To:
```
**Overall Risk:** `CRITICAL` / `HIGH` / `LOW` / `CLEAN`
```

The derivation note is already correct and needs no change.

---

## Files Affected

| File | Finding(s) | Change type |
|---|---|---|
| `template/scheduled-tasks/ops/migrate.md` | AUD-046, AUD-047 | Edit |
| `template/scheduled-tasks/ops/blueprint-sync.md` | AUD-047 | Edit |
| `README.md` | AUD-048 | Edit |
| `user-guide.md` | AUD-048 | Edit |
| `docs/audit-report-template.md` | AUD-049 | Edit |

No new files. No deletions.

---

## Out of Scope

- `migrate.md` rollback section for v2.2→v2.3 does not mention `refresh-hot.md` — left as-is (not called out by audit)
- `migrate.md` confirmation messages — not updated (migration copy is not a behavior change worth surfacing in the confirm message)
- Any other token estimates not specifically identified in AUD-048
