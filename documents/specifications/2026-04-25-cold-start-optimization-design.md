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
- Remove `token-reference.md` and replace with dynamic file-size estimation at approval time
- Add post-op soft block after `!! ingest`, `!! lint`, `!! audit` to guide users toward new sessions

---

## 3. Non-Goals

- Changing any user-facing command syntax
- Modifying the wiki page schema or ingest logic
- Aggressive query routing changes
- Modifying existing ops file content beyond what is needed for the restructuring

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
      session-hygiene.md                        ← NEW
  scripts/
    check_deps.py                               ← NEW (replaces planned check_python.py)
    wrap.py                                     ← NEW
    ready.py                                    ← NEW
    log_tail.py                                 ← NEW
    file_check.py                               ← NEW
    estimate_tokens.py                          ← NEW

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
| `template/CLAUDE.md` | Rewritten — 3 large sections removed, bash commands replaced, token-reference.md row removed from ops routing table, session hygiene rule added |
| `setup-guide.md` | New Step 2.5 (Python check); new Step 4.5 (environment offer); scripts/ copy step |
| `user-guide.md` | Scripts section; claude-code-enhanced skill mention; token-reference.md references removed; session hygiene + soft block behavior documented |
| `ops/audit.md` | Remove per-file headroom check, envelope check, and recalibration rule sections; add post-op advisory step |
| `ops/ingest.md` | Add post-op advisory step |
| `ops/lint.md` | Add post-op advisory step |
| `ops/conventions.md` | Append Filing Answers sub-section |
| `ROADMAP.md` | Mark `claude-code-enhanced` as shipped |
| `CHANGELOG.md` | New section — v2.2.0 |
| `.gitignore` | Add `backups/` |

### Deleted files

| File | Reason |
|---|---|
| `template/scheduled-tasks/ops/token-reference.md` | Replaced by dynamic estimation via `estimate_tokens.py` |
| `scheduled-tasks/ops/token-reference.md` | Deleted during `!! migrate` (working folder copy) |

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
| `estimate_tokens.py` | Reading `token-reference.md` before every write | Dynamic token estimation from live file sizes |

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

### Dynamic Token Estimation (`estimate_tokens.py`)

Replaces `token-reference.md` entirely. Called by the agent before any approval request to compute live token estimates from actual file sizes.

```python
# Usage: python scripts/estimate_tokens.py path/to/file1 path/to/file2 ...
# Output: one line per file — "~N tokens  path/to/file"
#         final line        — "Total: ~N tokens"

import sys
from pathlib import Path

def estimate(path: Path) -> int:
    return path.stat().st_size // 4

paths = [Path(p) for p in sys.argv[1:]]
total = 0
for p in paths:
    t = estimate(p)
    total += t
    print(f"~{t} tokens  {p}")
print(f"Total: ~{total} tokens")
```

**Why this is better than `token-reference.md`:**
- Always accurate — reads live file sizes, no drift between documented and actual
- Zero maintenance — no recalibration rule, no headroom tables, no envelope math
- Simpler audit — the per-file headroom check and envelope check sections are removed from `ops/audit.md`

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
## Ops Routing            [10-row table — token-reference.md row removed, 2 new rows added]
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
   e. Delete `scheduled-tasks/ops/token-reference.md`
   f. Write `scripts/estimate_tokens.py`
   g. Patch `hot.md` — add `Python:` field, update `Schema: v2.2`
   h. Append to `log.md`: `## [YYYY-MM-DD] migrate | v2.1 → v2.2 — lean cold-start restructure`
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
- New files added; `token-reference.md` deleted
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
| Per-write approval cost (token-reference.md read) | ~2,120 | 0 | −2,120 per write op |

Net: users who never edit blueprint files or use `!! wrap`/`!! ready` see the full 86% cold-start saving plus ~2,120 tokens saved on every write approval. Heavy users pay back ~750 tokens per session on memory ops — still a significant net gain.

---

## 17. Session Hygiene — Post-Op Soft Block

### Motivation

Every turn in a session re-reads the full conversation history. After a heavy operation (`!! ingest`, `!! lint`, `!! audit`), the session context is already large. Any follow-up work in the same session compounds this cost unnecessarily — all prior tool results and responses are reprocessed on every subsequent turn.

### Behavior

After `!! ingest`, `!! lint`, or `!! audit` completes, the agent appends the following soft-block advisory as the final element of its response:

```
---
⚠️  Session advisory: This session has completed a !! [op] operation and the context
is now heavy. Starting a new session for follow-up work avoids reprocessing this
session's history on every turn.

Before you leave:
  💾 Say !! wrap to save a session summary.
  🔄 Say !! ready at the start of your next session to restore it.

To continue in this session anyway, say !! proceed.
---
```

If the user issues any `!! command` (other than `!! wrap`, `!! ready`, or `!! proceed`) after this advisory has been shown in the current session, the agent intercepts it and responds:

```
⚠️  A !! [op] operation completed earlier in this session. Continuing will reprocess
~[N] tokens of prior context on every turn.

  💾 !! wrap  — save context now, then start a new session
  🔄 !! ready — restore it next session

Say !! proceed to continue here anyway.
```

`!! wrap` and `!! ready` are always allowed — they are the recommended exit path. `!! proceed` clears the soft block for the remainder of the session.

### Scope

| Op | Soft block applied |
|---|---|
| `!! ingest [file]` | ✓ |
| `!! ingest all` | ✓ |
| `!! lint [page]` | ✓ |
| `!! lint all` | ✓ |
| `!! audit [page]` | ✓ |
| `!! audit all` | ✓ |
| `!! wrap` | ✗ (always allowed) |
| `!! ready` | ✗ (always allowed) |
| `!! update`, `!! install`, queries | ✗ (no block) |

### Implementation

Each of the three ops files (`ops/ingest.md`, `ops/lint.md`, `ops/audit.md`) gains a new final step:

> **Post-op: session advisory**
> Append the soft-block advisory block (from Section 17 of the design spec) to the final response. Set an in-memory flag `SESSION_HEAVY = true`. For the remainder of this session, intercept any `!! command` (except `!! wrap`, `!! ready`, `!! proceed`) and show the intercept message. `!! proceed` clears the flag.

`CLAUDE.md` gains one line in Core Rules:

> **Session hygiene:** If `SESSION_HEAVY` is set, intercept `!! commands` per `ops/session-hygiene.md`.

A new file `ops/session-hygiene.md` holds the intercept message template and the flag-clearing logic — keeping the two message strings in one place so they stay in sync if wording changes.

### Files affected (additions to Section 7)

| File | Change |
|---|---|
| `template/scheduled-tasks/ops/ingest.md` | Add post-op advisory step |
| `template/scheduled-tasks/ops/lint.md` | Add post-op advisory step |
| `template/scheduled-tasks/ops/audit.md` | Add post-op advisory step |
| `template/scheduled-tasks/ops/session-hygiene.md` | NEW — intercept message template + flag logic |
| `template/CLAUDE.md` | Add one-line session hygiene rule to Core Rules |
| `user-guide.md` | Document soft block behavior and `!! proceed` override |

---

## 18. Implementation Notes

- Implementation should be done with **Claude Opus 4.7** — the Blueprint Sync cascade (12-row matrix, 34 cross-reference checks) requires strong multi-file consistency reasoning
- Run `!! audit all` after implementation to verify no cross-reference drift
- `ops/audit.md` must be simplified as part of implementation — remove the per-file headroom check (Section 1.4) and envelope check (Section 1.5) sections; these are no longer needed without `token-reference.md`
