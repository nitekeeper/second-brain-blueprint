# Cold-Start Optimization Design

**Date:** 2026-04-25  
**Schema target:** v2.1 → v2.2  
**Status:** Draft — pending implementation plan

---

## 1. Problem Statement

The current `CLAUDE.md` is ~24,500 chars / ~7,700 tokens and is loaded in full on every session cold-start. Best practice for agent instruction files is 500–2,000 tokens (under 200 lines). At ~7,700 tokens the file exceeds the effective instruction attention budget (~150–200 distinct instructions), meaning some rules are silently dropped by the model. The goal is to reduce cold-start cost by ~86% while improving rule-following reliability and adding cross-platform script support for Windows, macOS, and Linux.

---

## 2. Goals

- Reduce cold-start from ~7,780 tokens to ~1,080 tokens (~86% reduction)
- Keep all existing user-facing commands unchanged (`!! ingest`, `!! wrap`, `!! lint`, etc.)
- Replace bash-only commands with cross-platform Python scripts
- Support both Claude Desktop Cowork and Claude Code CLI environments
- Provide a safe, user-approved migration path for existing users
- Handle Python and SQLite availability checks with OS-aware instructions

---

## 3. Non-Goals

- Changing any user-facing command syntax
- Modifying the wiki page schema or ingest logic
- Aggressive query routing changes
- Reducing per-operation token cost (separate future effort)

---

## 4. Architecture — Two-Tier Loading Model

```
Tier 1 — Always loaded (cold start)
  CLAUDE.md              ~4,000 chars / ~1,000 tokens   routing table + always-active rules

Tier 2 — Deferred (loaded on trigger)
  ops/session-memory.md  ~3,000 chars / ~750 tokens     loaded on: !! wrap / !! ready
  ops/blueprint-sync.md  ~2,500 chars / ~625 tokens     loaded on: blueprint file edit
  ops/reference.md       ~1,600 chars / ~400 tokens     loaded on: explicit request only
```

**Loading mechanism:** Extend the existing ops file pattern. Each deferred file is read when the agent detects the relevant trigger. This is auditable — the `📋 Waterfall:` compliance line already tracks which ops file was read per response.

---

## 5. What Stays in CLAUDE.md

| Section | Rationale |
|---|---|
| Startup sequence | Needed every session |
| Query routing waterfall | Must be inline — a file read per query would increase cost |
| Ops routing table | Pointer map; trivially small |
| Approval rule (condensed) | Always-active safety constraint |
| Suggestion rule | Always-active, two lines |
| Blueprint-authoring mode guard | Needed at startup to detect environment |
| Response footer spec | Required on every response |
| Format specs (index, hot, log) | Needed for every wiki write |

## 6. What Moves Out

| Section | Destination | Trigger |
|---|---|---|
| Session Memory Commands (`!! wrap`/`!! ready` full state machine) | `ops/session-memory.md` | `!! wrap` or `!! ready` detected in user message |
| Blueprint Sync Rule (12-row cascade matrix) | `ops/blueprint-sync.md` | Agent is about to edit any file under `blueprint/` or `template/` |
| Directory Structure diagram | `ops/reference.md` | On demand |
| Tiered Read Structure table | `ops/reference.md` | On demand |
| Filing Answers sub-section | `ops/conventions.md` (appended as new section at end of file) | Already loaded before page writes |

---

## 7. File Structure Changes

### New files added to template

```
template/
  CLAUDE.md                                     ← rewritten (~4,000 chars / ~1,000 tokens)
  scheduled-tasks/
    ops/
      session-memory.md                         ← NEW
      blueprint-sync.md                         ← NEW
      reference.md                              ← NEW
      token-reference.md                        ← updated (new file rows, CLAUDE.md recalibrated)
  scripts/
    check_deps.py                               ← NEW (replaces planned check_python.py)
    wrap.py                                     ← NEW
    ready.py                                    ← NEW
    log_tail.py                                 ← NEW
    file_check.py                               ← NEW

blueprint/
  skills/
    claude-code-enhanced/                       ← NEW (optional, Claude Code CLI only)
      SKILL.md
      slash-commands.md
```

### Working folder changes (after migration)

```
<WorkingFolder>/
  backups/                                      ← NEW (gitignored)
    CLAUDE.md-v2.1-YYYY-MM-DD.bak              (created during !! migrate)
  scripts/                                      ← NEW (copied from template)
```

### Updated files (not new)

| File | Change |
|---|---|
| `template/CLAUDE.md` | Rewritten — 3 large sections removed, bash commands replaced |
| `ops/token-reference.md` | New rows for 8 new files; CLAUDE.md row recalibrated downward |
| `setup-guide.md` | New Step 2.5 (Python check); new Step 4.5 (environment offer); scripts/ copy step |
| `user-guide.md` | Scripts section; claude-code-enhanced skill mention |
| `ROADMAP.md` | Mark `claude-code-enhanced` as shipped |
| `CHANGELOG.md` | New section — v2.2.0 |
| `.gitignore` | Add `backups/` |

---

## 8. Cross-Platform Script Strategy

Python is the exclusive scripting language. Bash commands currently in `CLAUDE.md` are replaced with Python equivalents.

**Rationale:** Python ships on macOS and Linux; Windows requires installation (python.org or `winget`). A single Python codebase handles all three OSes via `pathlib`, `os`, and `platform` — no WSL or Git Bash dependency on Windows.

### Scripts

| Script | Replaces | Purpose |
|---|---|---|
| `check_deps.py` | — | Pre-flight check for Python 3.8+ and optionally SQLite |
| `wrap.py` | 8 paragraphs of prose in CLAUDE.md | `memory.md` write + marker handling |
| `ready.py` | 8 paragraphs of prose in CLAUDE.md | `memory.md` read / truncation detection / wipe |
| `log_tail.py` | `grep -E "^## \[" log.md \| tail -5` | Cross-platform last-5-entries log read |
| `file_check.py` | `[ -f path ] && echo exists` | Cross-platform file existence check |

### OS-aware patterns used throughout

```python
from pathlib import Path
import platform, os

OS = platform.system()          # 'Windows', 'Darwin', 'Linux'
WORKDIR = Path(__file__).parent.parent
MEMORY  = WORKDIR / "memory.md" # pathlib handles separators automatically

# Always write LF line endings
with open(MEMORY, "w", encoding="utf-8", newline="\n") as f:
    ...
```

### Python command resolution

The resolved command (`python` on Windows, `python3` on macOS/Linux) is stored in `hot.md` under a new `Python:` field at setup time. The agent reads it once per session — no re-probe on every script call.

---

## 9. Dependency Checks

### Python check (`check_deps.py --python`)

**Fires:** Setup time + before any script execution.

| OS | If missing |
|---|---|
| Windows | Instructions: `winget install Python.Python.3.12` or python.org download |
| macOS | Instructions: `brew install python3` |
| Linux (Ubuntu) | Instructions: `sudo apt install python3` |

### SQLite check (`check_deps.py --sqlite`)

**Fires:** `!! install sqlite-query` only. SQLite is not required for the base system.

| OS | If missing |
|---|---|
| Windows | Instructions: reinstall Python from python.org (SQLite bundled) |
| macOS | Instructions: `brew install sqlite3`, then reinstall Python |
| Linux (Ubuntu) | Auto-install: `sudo apt-get install -y python3-sqlite3`; show manual instructions on failure |

---

## 10. Dual Environment Support

| Feature | Cowork | Claude Code CLI |
|---|---|---|
| Lean `CLAUDE.md` cold-start | ✓ | ✓ |
| Deferred ops file loading | ✓ | ✓ |
| Python scripts | ✓ | ✓ |
| `!! command` syntax | ✓ | ✓ |
| Native slash commands (`/wrap`, `/ready`, `/sync`) | ✗ | ✓ (via `!! install claude-code-enhanced`) |

The `claude-code-enhanced` skill is optional. It registers slash command wrappers around the same Python scripts. Users who don't install it use `!! wrap` / `!! ready` as before.

---

## 11. Lean CLAUDE.md Structure

Target: ~4,000 chars / ~1,000 tokens. Representative structure:

```
# LLM Wiki Agent Schema v2.2

## Startup
1. Read this file
2. Read wiki/hot.md
3. Check drafts/ — list ≤20 filenames only
4. Environment: if .claude/ at working root → Claude Code; else Cowork
5. Python: read Python: from hot.md; if absent run python scripts/check_deps.py --python
6. If !! ready: read @scheduled-tasks/ops/session-memory.md, follow it — skip step 7
7. Announce readiness: hot.md one-liner + drafts
   If wiki/ absent: announce "Blueprint-authoring mode — only !! audit expected"

## Query Routing          [condensed waterfall — inline, no file read]
## Ops Routing            [11-row table including 2 new rows]
## Core Rules             [Approval + Suggestion — condensed to 4 lines each]
## Response Footer        [8-line footer spec — unchanged]
## Formats                [index.md, hot.md, log.md — hot.md gains Python: field]

*Schema version: 2.2*
```

---

## 12. hot.md Format Change

New `Python:` field added. Stores resolved command at setup/migration time.

```
Pages: N | Schema: v2.2 | Updated: YYYY-MM-DD
Last op: [op] YYYY-MM-DD ([result])
Gaps: [gaps]
Hot: [5 recent pages]
Active skills: [skills or "none"]
Python: [python | python3]
```

---

## 13. Migration Path (`!! migrate`)

For existing users upgrading from v2.1.x.

**Detection:** Agent reads `Schema:` from `hot.md` at startup. If below v2.2, announces once: *"Blueprint v2.2 is available — run `!! migrate` to update."*

**`!! migrate` steps:**

1. Run `python scripts/check_deps.py --python` — halt with instructions if Python missing
2. Show approval request listing all files replaced, added, and untouched
3. On approval:
   a. Back up `CLAUDE.md` → `backups/CLAUDE.md-v2.1-YYYY-MM-DD.bak`
   b. Write new `CLAUDE.md`
   c. Write `ops/session-memory.md`, `ops/blueprint-sync.md`, `ops/reference.md`
   d. Create `scripts/` directory; write 5 scripts
   e. Update `token-reference.md`
   f. Patch `hot.md` — add `Python:` field, update `Schema: v2.2`
   g. Append to `log.md`: `## [YYYY-MM-DD] migrate | v2.1 → v2.2 — lean cold-start restructure`
4. Confirm: *"Migration complete. Cold-start: ~7,780 → ~1,080 tokens. Backup at `backups/CLAUDE.md-v2.1-YYYY-MM-DD.bak` — delete when satisfied."*
5. Offer: *"Using Claude Code CLI? Run `!! install claude-code-enhanced` for native slash commands."*

**What is preserved:** `wiki/`, `memory.md`, `raw/`, `drafts/`, existing ops files, sqlite-query skill if installed.

**Rollback:** Rename `backups/CLAUDE.md-v2.1-YYYY-MM-DD.bak` → `CLAUDE.md`. All other v2.1 files are untouched; the three new ops files and `scripts/` are inert without the v2.2 `CLAUDE.md`.

---

## 14. Backup Storage

**Location:** `backups/` directory at working folder root.  
**Naming:** `<filename>-v<version>-<YYYY-MM-DD>.bak` (e.g. `CLAUDE.md-v2.1-2026-04-25.bak`)  
**Gitignore:** `backups/` added to `.gitignore` — backups are local-only ephemeral safety nets.  
**Pruning:** Manual. Agent reminds user to delete after confirming satisfaction with migration.

---

## 15. Schema Version

This is a **minor version bump: v2.1 → v2.2**.

- User-facing commands unchanged
- Startup token profile changes significantly
- New files added, no files deleted
- `hot.md` format gains one field (`Python:`)
- `CHANGELOG.md` gets a new `v2.2.0` section

---

## 16. Token Impact Summary

| Metric | Before (v2.1) | After (v2.2) | Delta |
|---|---|---|---|
| `CLAUDE.md` chars | ~24,500 | ~4,000 | −83% |
| `CLAUDE.md` tokens | ~7,700 | ~1,000 | −87% |
| Cold-start total | ~7,780 | ~1,080 | −86% |
| Session memory op (additional) | 0 | ~750 | +750 (on !! wrap/ready only) |
| Blueprint edit op (additional) | 0 | ~625 | +625 (on blueprint edits only) |

Net: users who never edit blueprint files or use `!! wrap`/`!! ready` see the full 86% saving. Heavy users pay back ~750 tokens per session on memory ops — still a large net gain.

---

## 17. Implementation Notes

- Implementation should be done with **Claude Opus 4.7** — the Blueprint Sync cascade (12-row matrix, 34 cross-reference checks) requires strong multi-file consistency reasoning
- Run `!! audit all` after implementation to verify no cross-reference drift
- Token-reference.md recalibration is required as part of implementation (new file rows + CLAUDE.md row updated)
