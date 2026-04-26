# Design Spec — AUD-2026-04-25-011 Fixes

**Date:** 2026-04-25
**Audit Report:** AUD-2026-04-25-011
**Findings:** AUD-042 (WARNING), AUD-043 (STYLE), AUD-044 (STYLE), AUD-045 (STYLE)
**Approach:** Approach A — sequential, severity-first; single spec → single plan → single fix commit

---

## Overview

Four open findings from AUD-2026-04-25-011 are resolved in this cycle. One WARNING (cross-platform code breakage on Windows) is addressed first, followed by three STYLE findings (documentation drift and omissions). All changes are small, targeted edits to existing files; no new files are created.

---

## Fix 1 — AUD-042: Cross-platform path resolution (WARNING)

**Files:** `skills/sqlite-query/query-layer.md`, `template/scheduled-tasks/ops/conventions.md`

### query-layer.md

The Step 1 Python block currently uses `subprocess.run(["find", ...])` to resolve page slugs to file paths. On Windows this silently invokes `C:\Windows\System32\find.exe` (a text-search utility with incompatible syntax), producing empty output and leaving `candidate_paths = []` on every query — the sqlite-query skill provides no benefit on Windows.

**Changes:**

1. Remove `subprocess` from the import line:
   - Before: `import sqlite3, pathlib, os, subprocess`
   - After: `import sqlite3, pathlib, os`

2. Replace the slug-to-path resolution block:
   - Before:
     ```python
     candidate_paths = []
     pages_dir = str(WORKDIR / "wiki" / "pages")
     for row in rows:
         result = subprocess.run(
             ["find", pages_dir, "-name", f"{row[0]}.md"],
             capture_output=True, text=True
         )
         path = result.stdout.strip()
         if path:
             candidate_paths.append(path)
     ```
   - After:
     ```python
     candidate_paths = []
     pages_dir = WORKDIR / "wiki" / "pages"
     for row in rows:
         matches = list(pages_dir.rglob(f"{row[0]}.md"))
         if matches:
             candidate_paths.append(str(matches[0]))
     ```

3. Update the inline comment above the resolution block from `# Resolve each slug to a concrete file path via \`find\`.` to explain that `pathlib.rglob()` is used for cross-platform compatibility. The existing caveat about not passing glob patterns to `open()` / the Read tool is preserved — it remains valid; we are using the proper Python API, not shell glob expansion.

### conventions.md

The Query Layer Hook Contract (under `## Query Layer Hook Contract`) contains one sentence directing future skill authors to use `subprocess.run(["find", ...])`. This propagates the Windows-incompatible pattern.

**Change:** Replace that sentence:
- Before: `Use \`find wiki/pages -name "<slug>.md"\` (via \`subprocess.run\`) to resolve slugs to concrete paths.`
- After: `Use \`pathlib.rglob(f"{slug}.md")\` on the \`wiki/pages\` directory (cross-platform — works on Windows, macOS, and Linux). Do NOT use \`subprocess.run(["find", ...])\` — it invokes OS-specific utilities that fail silently on Windows.`

---

## Fix 2 — AUD-043: Add "Worth filing?" prompt to CLAUDE.md Step 2 (STYLE)

**File:** `template/CLAUDE.md`

Step 2 (Web Search) in the Query Routing Rule has three condition bullets but omits the "Worth filing this as an analysis page?" prompt that `conventions.md` and `user-guide.md` both document as post-Step-2 behavior. Step 1 already includes this prompt (sub-step 5).

**Change:** Append one bullet after the three existing Step 2 condition bullets:
- After: `- After summarizing: ask "Worth filing this as an analysis page?" — if yes, read \`@scheduled-tasks/ops/conventions.md\` first`

Wording matches Step 1's sub-step 5 exactly for consistency.

---

## Fix 3 — AUD-044: Expand `docs/` subtree in reference.md (STYLE)

**File:** `template/scheduled-tasks/ops/reference.md`

The blueprint/ directory tree in the Directory Structure section lists `docs/` with only `audit-report-template.md`. The tracked repo contains `docs/superpowers/` (with `plans/` and `specs/` subdirectories) which is absent from the diagram.

**Change:** Expand the `docs/` subtree entry:
- Before:
  ```
  │   ├── docs/                   ← Audit report template and design specs. Developer use only.
  │   │   └── audit-report-template.md
  ```
- After:
  ```
  │   ├── docs/                   ← Audit report template and developer workfiles. Maintainer use only.
  │   │   ├── audit-report-template.md
  │   │   └── superpowers/        ← Implementation plans and design specs (not distributed to end users)
  │   │       ├── plans/
  │   │       └── specs/
  ```

The description is also updated from "design specs. Developer use only." to "developer workfiles. Maintainer use only." to avoid redundancy with the `superpowers/` line and to use consistent terminology.

---

## Fix 4 — AUD-045: Expand Step 3 in refresh-hot.md (STYLE)

**File:** `template/scheduled-tasks/refresh-hot.md`

Step 3 only checks for `scheduled-tasks/query-layer.md` (sqlite-query skill). The `claude-code-enhanced` skill — a first-party bundled skill already present in the blueprint — installs `scheduled-tasks/claude-code-enhanced.md` but is never checked, so `Active skills:` in `hot.md` omits it.

**Change:** Replace Step 3 with an expanded multi-check form:
- Before:
  ```
  3. **Derive `Active skills`:** Check whether `scheduled-tasks/query-layer.md` exists (`python scripts/file_check.py scheduled-tasks/query-layer.md`). If it exists, the `sqlite-query` skill is installed — emit `sqlite-query`. If absent, emit `none`. (As additional skills are added, this step expands to check their respective hook files and append their names to the list.)
  ```
- After:
  ```
  3. **Derive `Active skills`:** Check each skill's hook or installed file:
     - `python scripts/file_check.py scheduled-tasks/query-layer.md` — if present, add `sqlite-query` to the list
     - `python scripts/file_check.py scheduled-tasks/claude-code-enhanced.md` — if present, add `claude-code-enhanced` to the list

     If neither is present, emit `none`. If one or more are present, emit them comma-separated (e.g. `sqlite-query, claude-code-enhanced`). When a new skill is added to the blueprint, add its detection check here at the same time.
  ```

The forward-looking parenthetical from the old text is preserved as the final standing instruction.

---

## Audit Report Update

After all fixes are applied, update `audits/AUD-2026-04-25-011.md`:
- Mark all four action items checked (`- [x]`)
- Update the status of each finding from `OPEN` to `RESOLVED`

---

## Commit Strategy

Single commit after all six file edits (5 blueprint/skills files + 1 audit report update):
```
fix: resolve AUD-042 through AUD-045 from AUD-2026-04-25-011
```

No new files are created. No existing files are deleted.

---

## Files Affected

| File | Finding | Change Type |
|---|---|---|
| `skills/sqlite-query/query-layer.md` | AUD-042 | Code — replace subprocess with pathlib.rglob |
| `template/scheduled-tasks/ops/conventions.md` | AUD-042 | Prose — update Hook Contract |
| `template/CLAUDE.md` | AUD-043 | Prose — add Step 2 bullet |
| `template/scheduled-tasks/ops/reference.md` | AUD-044 | Prose — expand docs/ subtree |
| `template/scheduled-tasks/refresh-hot.md` | AUD-045 | Prose — expand Step 3 |
| `audits/AUD-2026-04-25-011.md` | All | Status update — mark RESOLVED |
