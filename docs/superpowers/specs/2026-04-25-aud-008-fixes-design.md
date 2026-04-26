---
title: AUD-2026-04-25-008 Fixes Design
date: 2026-04-25
audit_report: AUD-2026-04-25-008
---

# AUD-008 Fixes Design

## Scope

Fix all open findings from audit report `AUD-2026-04-25-008`. Both findings are STYLE severity — documentation-only with no runtime impact.

## Findings

| ID | File | Summary |
|---|---|---|
| AUD-032 | `README.md` | Approval exceptions bullet omits `!! audit` |
| AUD-033 | `docs/audit-report-template.md` | Schema version hardcoded as v2.2 (should be v2.3) |

## Edits

### Edit 1 — `README.md` line 73

**Current:**
```
- **Approval before every wiki write** — `!! wrap` and `!! ready` are the only exceptions (each gated by built-in safeguards); every other write pauses with a plan + token estimate before touching a file
```

**New:**
```
- **Approval before every wiki write** — `!! wrap`, `!! ready`, and `!! audit` are the only exceptions (`!! audit` writes its report as an implicit side-effect; `!! wrap` and `!! ready` have additional built-in safeguards); every other write pauses with a plan + token estimate before touching a file
```

Adds `!! audit` to the exceptions list and distinguishes the three exceptions with a parenthetical, matching the wording in `CLAUDE.md` Core Rules and `user-guide.md` Approval Rule.

### Edit 2 — `docs/audit-report-template.md` Report Header table

Two cells updated:

| Row | Current | New |
|---|---|---|
| `**Schema Version**` | `v2.2` | `v2.3` |
| `**Auditor**` | `LLM Wiki Agent — audit.md v2.2` | `LLM Wiki Agent — audit.md v2.3` |

The bracketed example text elsewhere in the template (Criteria/Cause fields) that mentions "v2.2" as illustrative placeholder text is left unchanged — those are not version references.

### Edit 3 — `audits/AUD-2026-04-25-008.md` closure

- Finding status fields: `OPEN` → `RESOLVED` for AUD-032 and AUD-033
- Executive summary table: 2 open / 0 resolved → 0 open / 2 resolved
- Action item checkboxes: `[ ]` → `[x]` for both items

## Approach

Option A — follow audit report recommendations exactly. No paraphrasing or scope changes.

## Out of Scope

- Any refactoring of the Key Features section
- Changes to bracketed placeholder examples in `audit-report-template.md`
- Any other files not named above
