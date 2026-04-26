# Design: Fix AUD-2026-04-25-009 Findings

**Date:** 2026-04-25
**Audit Report:** `audits/AUD-2026-04-25-009.md`
**Approach:** Single batch commit — all 6 changes applied together, audit report updated to RESOLVED.

---

## Scope

6 changes across 5 files, plus the audit report update.

| File | Finding | Nature |
|---|---|---|
| `skills/sqlite-query/query-layer.md` | AUD-034 | Wording fix — remove ambiguous cross-reference |
| `template/scheduled-tasks/ops/migrate.md` | AUD-035 | Add backup step b3; extend rollback bullet; update Confirm message |
| `template/scheduled-tasks/ops/audit.md` | AUD-036 | Add `docs/audit-report-template.md` to scope list and token estimate command |
| `template/scheduled-tasks/ops/audit.md` | Related | Fix `open STYLEs only → MEDIUM` to `→ LOW` in Executive Summary step |
| `template/scheduled-tasks/ops/reference.md` | AUD-037 | Add `docs/` subtree entry to `blueprint/` tree |
| `docs/audit-report-template.md` | AUD-038 | Replace self-contradictory risk-level derivation |
| `audits/AUD-2026-04-25-009.md` | post-fix | Set all 5 findings RESOLVED; check off all Action Items |

---

## Exact Changes

### AUD-034 — `skills/sqlite-query/query-layer.md` step 3

**Remove:**
```
If grep also returns nothing, proceed to Step 3 of the core query op (read `index.md`).
```

**Replace with:**
```
If grep also returns nothing, read `wiki/index.md` directly and continue from sub-step 4 of the query waterfall (read candidate pages; answer with [[wiki link]] citations).
```

**Why:** The old cross-reference pointed at a step that includes a grep, so an agent following it literally would re-run the grep already executed in query-layer.md step 3. The new instruction is self-contained and removes any ambiguity.

---

### AUD-035 — `template/scheduled-tasks/ops/migrate.md`

**Add after step b2:**
```
b3. Copy `scheduled-tasks/ops/blueprint-sync.md` → `backups/blueprint-sync.md-v2.2-<YYYY-MM-DD>.bak`
```

**Extend the Rollback v2.2→v2.3 bullet** — insert before `; revert Schema:`:
```
; rename `backups/blueprint-sync.md-v2.2-<date>.bak` → `scheduled-tasks/ops/blueprint-sync.md`
```

**Update Confirm message** to add the third backup file:
```
Backups saved to `backups/CLAUDE.md-v2.2-<date>.bak`, `backups/conventions.md-v2.2-<date>.bak`, and `backups/blueprint-sync.md-v2.2-<date>.bak` — delete when satisfied.
```

**Why:** The migration mutates `blueprint-sync.md` (step c3) but the rollback section had no instruction to restore it. A developer rolling back v2.2→v2.3 would end up with a v2.3 `blueprint-sync.md` under a v2.2 `CLAUDE.md`.

---

### AUD-036 + Related — `template/scheduled-tasks/ops/audit.md`

**Append to `!! audit all` scope list:**
```
- `blueprint/docs/audit-report-template.md`
```

**Add to Notes token estimate command** — append `blueprint/docs/audit-report-template.md` to the file list in the `python scripts/estimate_tokens.py` invocation.

**Fix Executive Summary step (related fix):**

Remove: `open STYLEs only → \`MEDIUM\``
Replace with: `open STYLEs only → \`LOW\``

**Why (AUD-036):** The template previously drifted (AUD-033) and the scope omission meant no automated catch existed. Adding it ensures future schema bumps in the template are caught by the next `!! audit all`.

**Why (related):** The audit.md Executive Summary step was the *generator* of audit reports and still said MEDIUM for STYLE-only findings. Leaving it inconsistent with the fixed template would cause future audits to output the wrong risk level.

---

### AUD-037 — `template/scheduled-tasks/ops/reference.md`

**Add to `blueprint/` subtree after `ROADMAP.md`:**
```
│   ├── ROADMAP.md
│   ├── docs/                   ← Audit report template and design specs. Developer use only.
│   │   └── audit-report-template.md
│   ├── template/
```

**Why:** The `docs/` directory is committed and distributed with the blueprint. Its absence from the subtree diagram meant agents and developers consulting `reference.md` would see an incomplete picture.

---

### AUD-038 — `docs/audit-report-template.md`

**Remove:**
```
Risk is derived from the highest-severity open finding: any unresolved CRITICAL → CRITICAL; all resolved CRITICALs but open WARNINGs → HIGH; all resolved WARNINGs but open STYLEs → MEDIUM; only resolved or STYLE findings → LOW; zero findings → CLEAN.
```

**Replace with:**
```
Risk is derived from the highest-severity open finding in priority order: (1) any unresolved CRITICAL → CRITICAL; (2) open WARNINGs (no open CRITICALs) → HIGH; (3) only resolved findings and/or open STYLEs → LOW; (4) zero findings → CLEAN. STYLE findings do not elevate risk above LOW — they are documentation-only.
```

**Why:** The old derivation had two clauses that both applied to STYLE-only reports but produced different outputs (MEDIUM vs LOW). Observed convention (AUD-008, AUD-009) uses LOW. The fix removes the contradictory clause and makes the priority ordering explicit.

---

### Audit Report Update — `audits/AUD-2026-04-25-009.md`

For each of AUD-034, AUD-035, AUD-036, AUD-037, AUD-038:
- Set `**Status**` to `RESOLVED`
- Check off the corresponding Action Items entry (`- [ ]` → `- [x]`)

---

## Out of Scope

- No changes to `CHANGELOG.md`, `README.md`, or any wiki pages
- No changes to the v2.1→v2.3 migration path in `migrate.md` (the rollback section for that path was not flagged)
- No changes to other ops files

---

## Commit Strategy

Single commit. Message:
```
fix: resolve AUD-034 through AUD-038 from AUD-2026-04-25-009
```
