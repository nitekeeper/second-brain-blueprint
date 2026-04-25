# Cold-Start Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce LLM Wiki blueprint cold-start from ~7,780 to ~1,080 tokens by restructuring CLAUDE.md into a lean routing table, extracting three large sections into deferred ops files, replacing bash commands with cross-platform Python scripts, deleting token-reference.md in favour of dynamic estimation, and adding session hygiene soft blocks after heavy ops.

**Architecture:** Two-tier loading — lean CLAUDE.md (~1,000 tokens) always loaded; `ops/session-memory.md`, `ops/blueprint-sync.md`, `ops/reference.md` loaded on-trigger. Six Python scripts replace bash and prose state machines. `estimate_tokens.py` replaces `token-reference.md`. Post-op soft block added to `!! ingest`, `!! lint`, `!! audit`.

**Tech Stack:** Python 3.8+ stdlib only (pathlib, platform, sys, subprocess, hashlib). No third-party dependencies.

**Implementation model:** Use Claude Opus 4.7 — the Blueprint Sync cascade (12-row matrix, 34 cross-reference checks) requires strong multi-file consistency reasoning. Run `!! audit all` after Phase 8 to verify no cross-reference drift.

**Spec:** `documents/specifications/2026-04-25-cold-start-optimization-design.md`

---

## File Map

### Created
```
template/scripts/check_deps.py
template/scripts/log_tail.py
template/scripts/file_check.py
template/scripts/estimate_tokens.py
template/scripts/wrap.py
template/scripts/ready.py
template/scheduled-tasks/ops/session-memory.md
template/scheduled-tasks/ops/blueprint-sync.md
template/scheduled-tasks/ops/reference.md
template/scheduled-tasks/ops/session-hygiene.md
template/scheduled-tasks/ops/migrate.md
blueprint/skills/claude-code-enhanced/SKILL.md
blueprint/skills/claude-code-enhanced/slash-commands.md
```

### Rewritten
```
template/CLAUDE.md
```

### Modified
```
template/scheduled-tasks/ops/audit.md
template/scheduled-tasks/ops/ingest.md
template/scheduled-tasks/ops/lint.md
template/scheduled-tasks/ops/conventions.md
setup-guide.md
user-guide.md
ROADMAP.md
CHANGELOG.md
.gitignore
```

### Deleted
```
template/scheduled-tasks/ops/token-reference.md
```

---

## Phase 1 — Python Scripts

### Task 1: create template/scripts/check_deps.py

**Files:**
- Create: `template/scripts/check_deps.py`

- [ ] **Step 1: Create the file**

```python
#!/usr/bin/env python3
"""
Dependency checker for the LLM Wiki blueprint.
Usage:
  python scripts/check_deps.py --python    check Python 3.8+
  python scripts/check_deps.py --sqlite    check sqlite3 module
  python scripts/check_deps.py --all       check both
Exit 0 = all checked deps present. Exit 1 = one or more missing.
"""
import sys
import platform
import subprocess

OS = platform.system()  # 'Windows', 'Darwin', 'Linux'


def check_python() -> bool:
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 8):
        _python_instructions(v)
        return False
    print(f"✓ Python {v.major}.{v.minor}.{v.micro}")
    return True


def check_sqlite() -> bool:
    try:
        import sqlite3
        sqlite3.connect(":memory:").close()
        print("✓ SQLite available")
        return True
    except ImportError:
        _sqlite_instructions()
        return False


def _python_instructions(v) -> None:
    print(f"\nPython 3.8+ is required. Found: {v.major}.{v.minor}.{v.micro}\n")
    if OS == "Windows":
        print(
            "Install options (Windows):\n"
            "  Option 1 — winget (recommended):\n"
            "    winget install Python.Python.3.12\n"
            "  Option 2 — python.org:\n"
            "    https://www.python.org/downloads/windows/\n"
            "    ✓ Check 'Add Python to PATH' during install\n\n"
            "After installing, restart your terminal and retry."
        )
    elif OS == "Darwin":
        print("Install: brew install python3\nThen restart your terminal and retry.")
    else:
        print("Install: sudo apt install python3\nThen retry.")


def _sqlite_instructions() -> None:
    print("\nSQLite (python sqlite3 module) not found.\n")
    if OS == "Windows":
        print(
            "SQLite is bundled with Python from python.org.\n"
            "Fix: reinstall Python from https://www.python.org/downloads/windows/"
        )
    elif OS == "Darwin":
        print("Fix:\n  brew install sqlite3\n  brew reinstall python3")
    else:
        print("Attempting auto-install...")
        result = subprocess.run(
            ["sudo", "apt-get", "install", "-y", "python3-sqlite3"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✓ SQLite installed. Please retry your command.")
        else:
            print(
                "Auto-install failed. Install manually:\n"
                "  sudo apt-get install python3-sqlite3\n"
                "  # or for custom Python builds:\n"
                "  sudo apt-get install libsqlite3-dev"
            )


if __name__ == "__main__":
    args = set(sys.argv[1:])
    if not args or args == {"--all"}:
        args = {"--python", "--sqlite"}

    ok = True
    if "--python" in args:
        ok = check_python() and ok
    if "--sqlite" in args:
        ok = check_sqlite() and ok

    sys.exit(0 if ok else 1)
```

- [ ] **Step 2: Verify it runs on current OS**

Run: `python scripts/check_deps.py --python`
Expected: `✓ Python 3.x.x` and exit 0

- [ ] **Step 3: Commit**

```bash
git add template/scripts/check_deps.py
git commit -m "feat: add check_deps.py — cross-platform Python/SQLite checker"
```

---

### Task 2: create template/scripts/log_tail.py

**Files:**
- Create: `template/scripts/log_tail.py`

- [ ] **Step 1: Create the file**

```python
#!/usr/bin/env python3
"""
Cross-platform replacement for: grep -E "^## \[" wiki/log.md | tail -5
Usage: python scripts/log_tail.py [path/to/log.md] [N]
Defaults: wiki/log.md, last 5 entries.
"""
import sys
from pathlib import Path


def log_tail(log_path: Path, n: int = 5) -> list:
    if not log_path.is_file():
        print(f"log not found: {log_path}", file=sys.stderr)
        sys.exit(1)
    entries = [
        line for line in log_path.read_text(encoding="utf-8").splitlines()
        if line.startswith("## [")
    ]
    return entries[-n:]


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("wiki/log.md")
    n    = int(sys.argv[2])  if len(sys.argv) > 2 else 5
    for line in log_tail(path, n):
        print(line)
```

- [ ] **Step 2: Verify with a test log file**

```bash
echo "## [2026-01-01] ingest | Test" > /tmp/test_log.md
python template/scripts/log_tail.py /tmp/test_log.md 5
```

Expected: `## [2026-01-01] ingest | Test`

- [ ] **Step 3: Commit**

```bash
git add template/scripts/log_tail.py
git commit -m "feat: add log_tail.py — cross-platform grep+tail replacement"
```

---

### Task 3: create template/scripts/file_check.py

**Files:**
- Create: `template/scripts/file_check.py`

- [ ] **Step 1: Create the file**

```python
#!/usr/bin/env python3
"""
Cross-platform replacement for: [ -f path ] && echo exists
Usage: python scripts/file_check.py <path>
Exit 0 + prints "exists" if file present. Exit 1 + prints "not found" otherwise.
"""
import sys
from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: file_check.py <path>", file=sys.stderr)
        sys.exit(2)
    p = Path(sys.argv[1])
    if p.is_file():
        print("exists")
        sys.exit(0)
    else:
        print("not found")
        sys.exit(1)
```

- [ ] **Step 2: Verify**

```bash
python template/scripts/file_check.py template/scripts/file_check.py
```
Expected: `exists` and exit 0

```bash
python template/scripts/file_check.py nonexistent.md
```
Expected: `not found` and exit 1

- [ ] **Step 3: Commit**

```bash
git add template/scripts/file_check.py
git commit -m "feat: add file_check.py — cross-platform file existence check"
```

---

### Task 4: create template/scripts/estimate_tokens.py

**Files:**
- Create: `template/scripts/estimate_tokens.py`

- [ ] **Step 1: Create the file**

```python
#!/usr/bin/env python3
"""
Dynamic token estimation from live file sizes.
Replaces token-reference.md entirely — always accurate, zero maintenance.
Usage: python scripts/estimate_tokens.py path/to/file1 [path/to/file2 ...]
Output: one line per file ("~N tokens  path"), then "Total: ~N tokens".
"""
import sys
from pathlib import Path


def estimate(path: Path) -> int:
    return path.stat().st_size // 4


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: estimate_tokens.py <file1> [file2 ...]", file=sys.stderr)
        sys.exit(1)

    paths = [Path(p) for p in sys.argv[1:]]
    total = 0
    for p in paths:
        if not p.is_file():
            print(f"not found: {p}", file=sys.stderr)
            continue
        t = estimate(p)
        total += t
        print(f"~{t} tokens  {p}")
    print(f"Total: ~{total} tokens")
```

- [ ] **Step 2: Verify**

```bash
python template/scripts/estimate_tokens.py template/CLAUDE.md
```
Expected: one line with `~NNNN tokens  template/CLAUDE.md` and `Total: ~NNNN tokens`

- [ ] **Step 3: Commit**

```bash
git add template/scripts/estimate_tokens.py
git commit -m "feat: add estimate_tokens.py — dynamic token estimation replacing token-reference.md"
```

---

### Task 5: create template/scripts/wrap.py

**Files:**
- Create: `template/scripts/wrap.py`

- [ ] **Step 1: Create the file**

```python
#!/usr/bin/env python3
"""
Session memory write with marker-state handling.
Usage:
  python scripts/wrap.py check         check memory.md state
  python scripts/wrap.py write         write summary (reads body from stdin)

Exit codes for 'check':
  0 = EMPTY or file missing (safe to write)
  1 = WRAPPED (existing summary present — warn user before overwrite)
  2 = TRUNCATED_ACKNOWLEDGED (kept truncated summary — warn user before overwrite)
"""
import sys
from pathlib import Path

WORKDIR = Path(__file__).parent.parent
MEMORY  = WORKDIR / "memory.md"

MARKER_WRAPPED  = "<!-- MEMORY_STATE: WRAPPED -->"
MARKER_TRUNC    = "<!-- MEMORY_STATE: TRUNCATED_ACKNOWLEDGED -->"
MARKER_COMPLETE = "<!-- MEMORY_WRAP_COMPLETE -->"


def check() -> None:
    if not MEMORY.is_file():
        print("EMPTY")
        sys.exit(0)
    content = MEMORY.read_text(encoding="utf-8")
    if MARKER_WRAPPED in content:
        print("WRAPPED")
        sys.exit(1)
    if MARKER_TRUNC in content:
        print("TRUNCATED_ACKNOWLEDGED")
        sys.exit(2)
    print("EMPTY")
    sys.exit(0)


def write() -> None:
    summary = sys.stdin.read().replace("\r\n", "\n").replace("\r", "\n")
    content = f"{MARKER_WRAPPED}\n{summary}\n{MARKER_COMPLETE}\n"
    MEMORY.write_bytes(content.encode("utf-8"))
    print("✓ Summary written to memory.md")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        check()
    elif cmd == "write":
        write()
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 2: Verify check on missing file**

```bash
python template/scripts/wrap.py check
```
Expected: `EMPTY` and exit 0 (memory.md does not exist in blueprint-authoring mode)

- [ ] **Step 3: Commit**

```bash
git add template/scripts/wrap.py
git commit -m "feat: add wrap.py — session memory write with marker-state handling"
```

---

### Task 6: create template/scripts/ready.py

**Files:**
- Create: `template/scripts/ready.py`

- [ ] **Step 1: Create the file**

```python
#!/usr/bin/env python3
"""
Session memory read, truncation detection, and state transitions.
Usage:
  python scripts/ready.py read    read state + full content
  python scripts/ready.py clear   wipe memory.md to EMPTY
  python scripts/ready.py keep    mark truncated summary as acknowledged

Exit codes for 'read':
  0 = EMPTY or TRUNCATED_ACKNOWLEDGED (no valid summary to consume)
  1 = WRAPPED + COMPLETE (valid summary, safe to display and wipe)
  2 = WRAPPED but COMPLETE marker missing (truncated — do NOT auto-wipe)
"""
import sys
from pathlib import Path

WORKDIR = Path(__file__).parent.parent
MEMORY  = WORKDIR / "memory.md"

MARKER_WRAPPED  = "<!-- MEMORY_STATE: WRAPPED -->"
MARKER_TRUNC    = "<!-- MEMORY_STATE: TRUNCATED_ACKNOWLEDGED -->"
MARKER_COMPLETE = "<!-- MEMORY_WRAP_COMPLETE -->"

EMPTY_CONTENT = (
    "<!-- MEMORY_STATE: EMPTY -->\n"
    "# Session Memory\n\n"
    "*(empty — use `!! wrap` at the end of a session to save a summary here)*\n"
)


def read() -> None:
    if not MEMORY.is_file():
        print("STATE:EMPTY")
        sys.exit(0)
    content = MEMORY.read_text(encoding="utf-8")
    if MARKER_TRUNC in content:
        print("STATE:TRUNCATED_ACKNOWLEDGED")
        sys.exit(0)
    if MARKER_WRAPPED in content:
        if MARKER_COMPLETE in content:
            print("STATE:WRAPPED")
            print(content)
            sys.exit(1)
        else:
            print("STATE:TRUNCATED")
            print(content)
            sys.exit(2)
    print("STATE:EMPTY")
    sys.exit(0)


def clear() -> None:
    MEMORY.write_bytes(EMPTY_CONTENT.encode("utf-8"))
    print("✓ memory.md cleared to EMPTY state")


def keep() -> None:
    if not MEMORY.is_file():
        print("memory.md not found", file=sys.stderr)
        sys.exit(1)
    content = MEMORY.read_text(encoding="utf-8")
    if MARKER_WRAPPED not in content:
        print("No WRAPPED state found in memory.md", file=sys.stderr)
        sys.exit(1)
    updated = content.replace(MARKER_WRAPPED, MARKER_TRUNC, 1)
    MEMORY.write_bytes(updated.encode("utf-8"))
    print("✓ memory.md marked as TRUNCATED_ACKNOWLEDGED")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "read"
    if cmd == "read":
        read()
    elif cmd == "clear":
        clear()
    elif cmd == "keep":
        keep()
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 2: Verify read on missing file**

```bash
python template/scripts/ready.py read
```
Expected: `STATE:EMPTY` and exit 0

- [ ] **Step 3: Commit**

```bash
git add template/scripts/ready.py
git commit -m "feat: add ready.py — session memory read/truncation-detect/wipe"
```

---

## Phase 2 — New Deferred Ops Files

### Task 7: create ops/session-memory.md

Extract Session Memory Commands from CLAUDE.md and update to use scripts.

**Files:**
- Create: `template/scheduled-tasks/ops/session-memory.md`

- [ ] **Step 1: Create the file**

```markdown
# Session Memory Commands

**Temporary, intentional memory — designed to bridge one session to the next, not to accumulate.**
Read this file when the user says `!! wrap` or `!! ready`.

---

## Explicit state markers

`memory.md` uses HTML-comment markers:
- Empty: `<!-- MEMORY_STATE: EMPTY -->`
- Valid summary: begins with `<!-- MEMORY_STATE: WRAPPED -->`, ends with `<!-- MEMORY_WRAP_COMPLETE -->`
- Acknowledged truncated: `<!-- MEMORY_STATE: TRUNCATED_ACKNOWLEDGED -->` — treated identically to EMPTY

**Truncation:** If file contains `MEMORY_STATE: WRAPPED` but is missing `MEMORY_WRAP_COMPLETE`, it is truncated.

---

## `!! wrap`

1. **Pre-write safeguard:** Run `python scripts/wrap.py check`
   - Exit 0 (EMPTY): proceed without prompt
   - Exit 1 (WRAPPED): warn user — "A previous session summary is still in memory.md. Overwriting will destroy it. Proceed? (yes/no)" — wait for explicit confirmation
   - Exit 2 (TRUNCATED_ACKNOWLEDGED): warn user — "A preserved (truncated) summary is still in memory.md. Overwriting will destroy it. Proceed? (yes/no)" — wait for explicit confirmation

2. Ask: "Anything specific you'd like included in the summary?"

3. Compose a detailed summary structured as:
   ```
   # Session Memory — [YYYY-MM-DD]

   ## Worked on
   …

   ## Key decisions
   …

   ## Files created / modified
   …

   ## Open questions / next steps
   …
   ```
   Then pipe it to: `python scripts/wrap.py write`
   The script writes the summary with the correct state markers and completion marker.

4. Append to `wiki/log.md`: `## [YYYY-MM-DD] memory | Session summary saved` (≤500 chars)

5. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`

6. Confirm: "Session summary saved. Say `!! ready` next session to load it."

---

## `!! ready`

1. **Mid-session guard:** If this is NOT the first user message of the session, reply: "`!! ready` is meant as a session-opening command. You seem to be mid-session — say `!! ready confirm` if you really want to read and wipe the summary now." Only proceed on `!! ready confirm`.

2. Run `python scripts/ready.py read` and check exit code:

3. **Exit 0 (EMPTY or TRUNCATED_ACKNOWLEDGED):** Announce readiness normally from `hot.md`. Do not wipe. If TRUNCATED_ACKNOWLEDGED: prior session already shown content and user chose to keep it — leave it alone.

4. **Exit 2 (TRUNCATED):** Display what was printed to stdout. Warn it appears incomplete. Do NOT wipe. Offer three options and wait for explicit choice:
   - `clear` — run `python scripts/ready.py clear`, then append to `wiki/log.md`: `## [YYYY-MM-DD] memory | Truncated summary cleared` (≤500 chars), refresh `hot.md`
   - `keep`  — run `python scripts/ready.py keep`,  then append to `wiki/log.md`: `## [YYYY-MM-DD] memory | Truncated summary acknowledged` (≤500 chars), refresh `hot.md`
   - `edit`  — hand control back to user; touch nothing, write nothing

5. **Exit 1 (WRAPPED + COMPLETE):** Display the full summary verbatim (do not paraphrase, do not truncate).
   - Append to `wiki/log.md`: `## [YYYY-MM-DD] memory | Session summary consumed` (≤500 chars)
   - Run `python scripts/ready.py clear` to wipe memory.md
   - Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
   - Confirm: "Memory cleared. Ready to work."
   - Surface any in-progress drafts from `drafts/` (same as normal startup step 3). If `drafts/` is absent, skip transparently.

**Blueprint-authoring mode:** If `wiki/` absent at working folder root, skip all `wiki/log.md` appends and `hot.md` refreshes above — see CLAUDE.md Blueprint-authoring mode note.
```

- [ ] **Step 2: Verify the file exists and is readable**

```bash
python template/scripts/file_check.py template/scheduled-tasks/ops/session-memory.md
```
Expected: `exists`

- [ ] **Step 3: Commit**

```bash
git add template/scheduled-tasks/ops/session-memory.md
git commit -m "feat: add ops/session-memory.md — extracted from CLAUDE.md, updated to use scripts"
```

---

### Task 8: create ops/blueprint-sync.md

Extract Blueprint Sync Rule from CLAUDE.md verbatim.

**Files:**
- Create: `template/scheduled-tasks/ops/blueprint-sync.md`

- [ ] **Step 1: Create the file**

```markdown
# Blueprint Sync Rule

Read this file whenever you are about to edit any file under `blueprint/` or `template/`.

**CRITICAL: Whenever the schema, operations, or conventions are updated, the blueprint files must also be updated. Skipping this step causes template drift and breaks new wiki setups.**

| Change type | Files to update |
|---|---|
| Schema or startup change | `blueprint/README.md`, `blueprint/setup-guide.md`, `blueprint/user-guide.md`, `blueprint/template/CLAUDE.md` |
| Operation step change | `blueprint/user-guide.md`, `blueprint/template/CLAUDE.md`, `blueprint/template/scheduled-tasks/ops/[op].md` |
| Refresh-hot.md change | `blueprint/template/scheduled-tasks/refresh-hot.md`, `blueprint/template/CLAUDE.md` (hot.md Format block), `blueprint/setup-guide.md` (initial hot.md snippet) |
| New known issue or fix | `blueprint/troubleshooting.md` |
| Schema change that introduces a new footgun | `blueprint/troubleshooting.md` in addition to the Schema row above |
| Setup step change | `blueprint/setup-guide.md` |
| File-size or cost change | (token-reference.md removed in v2.2 — no propagation required) |
| Conventions change | `blueprint/template/scheduled-tasks/ops/conventions.md` |
| Any schema change | `blueprint/template/CLAUDE.md` always |
| Footer content change | ALL of: `blueprint/template/CLAUDE.md`, `blueprint/setup-guide.md`, `blueprint/user-guide.md` (keep them identical) |
| Schema version bump | `blueprint/CHANGELOG.md` (new section) in addition to any rows above |
| New scheduled task | `blueprint/template/scheduled-tasks/<name>.md` + `ops/audit.md` (informational parenthetical) + `ops/token-reference.md` (removed in v2.2; skip) + `setup-guide.md` + `README.md` and `user-guide.md` if user-visible + `template/CLAUDE.md` Directory Structure + `CHANGELOG.md` |
| New skill bundle added | `blueprint/skills/<skill>/` + `blueprint/user-guide.md` + `blueprint/setup-guide.md` + `blueprint/ROADMAP.md` + `ops/conventions.md` if skill introduces a new hook contract |

> **Non-cascade exception:** For startup or schema changes that are agent-internal with no user-facing behavioral impact, listed cascade files may require no content update. Document any deliberate non-cascade in `CHANGELOG.md` with explicit justification.

**Versioning split.** CLAUDE.md footer and `hot.md`'s `Schema:` field track `X.Y` only. Patch-level bumps add a new `CHANGELOG.md` section but do not move the footer or `hot.md` field. Minor/major bumps propagate through "Any schema change" row.

After updating blueprint files, append to `log.md`: `## [YYYY-MM-DD] sync | Blueprint synced — [what changed]` (≤500 chars). For audit-driven edits, `ops/audit.md` step 5 mandates `## [YYYY-MM-DD] audit | [fix summary]` instead — do not write both.

**Blueprint-authoring mode:** If `wiki/` absent at working folder root, skip all `log.md` appends and `hot.md` refreshes — see CLAUDE.md Blueprint-authoring mode note.
```

- [ ] **Step 2: Commit**

```bash
git add template/scheduled-tasks/ops/blueprint-sync.md
git commit -m "feat: add ops/blueprint-sync.md — extracted Blueprint Sync Rule from CLAUDE.md"
```

---

### Task 9: create ops/reference.md

Extract Directory Structure and Tiered Read sections from CLAUDE.md.

**Files:**
- Create: `template/scheduled-tasks/ops/reference.md`

- [ ] **Step 1: Create the file**

```markdown
# Reference — Directory Structure and Tiered Read

Read this file when the user asks about the wiki folder layout, file locations, or read tiers.

---

## Directory Structure

> `<WorkingFolder>` below is whatever the user named their Cowork working folder (e.g. `Library`, `MyWiki`). Substitute mentally — this diagram is layout-only, not a literal path.

```
<WorkingFolder>/
├── CLAUDE.md                   ← This file. Auto-read every session. Lean core schema.
├── memory.md                   ← Session memory. Written by `!! wrap`, read+wiped by `!! ready`.
├── backups/                    ← Migration backups. Gitignored. e.g. CLAUDE.md-v2.1-YYYY-MM-DD.bak
├── raw/                        ← Timestamped source snapshots — naming: <slug>-<YYYY-MM-DD-HHMMSS>.md
├── drafts/                     ← In-progress planning files. Claude's scrapbook.
├── scripts/                    ← Cross-platform Python utility scripts
│   ├── check_deps.py
│   ├── wrap.py
│   ├── ready.py
│   ├── log_tail.py
│   ├── file_check.py
│   ├── estimate_tokens.py
│   └── migrate.py              ← present only if manually added
├── blueprint/                  ← Setup guide and templates for sharing this system
│   ├── LICENSE
│   ├── .gitignore
│   ├── README.md
│   ├── setup-guide.md
│   ├── user-guide.md
│   ├── troubleshooting.md
│   ├── CHANGELOG.md
│   ├── template/
│   │   ├── CLAUDE.md
│   │   └── scheduled-tasks/
│   │       ├── refresh-hot.md
│   │       └── ops/
│   │           ├── ingest.md
│   │           ├── lint.md
│   │           ├── audit.md
│   │           ├── update.md
│   │           ├── conventions.md
│   │           ├── session-memory.md
│   │           ├── blueprint-sync.md
│   │           ├── reference.md
│   │           ├── session-hygiene.md
│   │           └── migrate.md
│   └── skills/
│       ├── sqlite-query/
│       │   ├── SKILL.md
│       │   ├── query-layer.md
│       │   └── ingest-hook.md
│       └── claude-code-enhanced/
│           ├── SKILL.md
│           └── slash-commands.md
├── scheduled-tasks/            ← Reusable task and ops instruction files
│   ├── refresh-hot.md
│   ├── query-layer.md          ← Present only if a query-layer skill is installed
│   ├── ingest-hook.md          ← Present only if an ingest-hook skill is installed
│   └── ops/
│       ├── ingest.md
│       ├── lint.md
│       ├── audit.md
│       ├── update.md
│       ├── conventions.md
│       ├── session-memory.md
│       ├── blueprint-sync.md
│       ├── reference.md
│       ├── session-hygiene.md
│       └── migrate.md
└── wiki/                       ← Obsidian vault root
    ├── index.md
    ├── log.md
    ├── hot.md
    ├── inbox/
    └── pages/
        ├── concepts/
        ├── entities/
        ├── sources/
        └── analyses/
```

---

## Tiered Read Structure

| Tier | Files | When |
|---|---|---|
| 1 — Always | `CLAUDE.md` + `hot.md` | Every session start |
| 1 — Conditional | `memory.md` via `ready.py` | Only when user says `!! ready` |
| 2 — Operations | `index.md` + `log.md` tail (via `log_tail.py`) | Before any wiki operation |
| 3 — On demand | Individual wiki pages | Only pages needed for current task |
| 3 — History review | Full `log.md` | Only when user requests history |
```

- [ ] **Step 2: Commit**

```bash
git add template/scheduled-tasks/ops/reference.md
git commit -m "feat: add ops/reference.md — directory structure + tiered read table"
```

---

### Task 10: create ops/session-hygiene.md

**Files:**
- Create: `template/scheduled-tasks/ops/session-hygiene.md`

- [ ] **Step 1: Create the file**

```markdown
# Session Hygiene — Post-Op Soft Block

Read this file when `SESSION_HEAVY` is set and the user issues a `!! command`
(other than `!! wrap`, `!! ready`, `!! proceed`).

---

## Intercept message

Reply with exactly this (substitute `[op]` and `[N]`):

```
⚠️  A !![op] operation completed earlier in this session. Continuing will
reprocess ~[N] tokens of prior context on every turn.

  💾 !! wrap  — save context now, then start a new session
  🔄 !! ready — restore it next session

Say !! proceed to continue here anyway.
```

- Replace `[op]` with the op that set SESSION_HEAVY (ingest / lint / audit).
- Replace `[N]` with a rough estimate of prior session context tokens (sum of approximate chars typed and received ÷ 4).

---

## Post-op advisory block

Append to the final response of every `!! ingest`, `!! lint`, and `!! audit` op:

```
---
⚠️  Session advisory: This session has completed a !![op] operation and the
context is now heavy. Starting a new session for follow-up work avoids
reprocessing this history on every turn.

Before you leave:
  💾 Say !! wrap to save a session summary.
  🔄 Say !! ready at the start of your next session to restore it.

To continue in this session anyway, say !! proceed.
---
```

Replace `[op]` with the completed op name.

---

## Flag behaviour

| Event | Effect on SESSION_HEAVY |
|---|---|
| `!! ingest` completes | Set |
| `!! lint` completes | Set |
| `!! audit` completes | Set |
| User says `!! proceed` | Clear |
| `!! wrap` or `!! ready` | No change (always allowed regardless of flag) |
| New session | Cleared automatically (flag is in-memory only) |
```

- [ ] **Step 2: Commit**

```bash
git add template/scheduled-tasks/ops/session-hygiene.md
git commit -m "feat: add ops/session-hygiene.md — soft block intercept after heavy ops"
```

---

### Task 11: create ops/migrate.md

**Files:**
- Create: `template/scheduled-tasks/ops/migrate.md`

- [ ] **Step 1: Create the file**

```markdown
# Op: MIGRATE

Triggered when the user says `!! migrate`.

Upgrades an existing v2.1.x working folder to v2.2.

---

## Detection (runs at startup)

During startup step 7, compare `Schema:` in `hot.md` against the current schema
version (`v2.2`). If `Schema:` is below `v2.2`, announce once:

> "Blueprint v2.2 is available — run `!! migrate` to update your working folder.
> Cold-start will drop from ~7,780 to ~1,080 tokens after migration."

Announce at most once per session (do not repeat on every response).

---

## Steps

1. **Pre-flight:** Run `python scripts/check_deps.py --python`
   - If exit non-zero: stop. Show the printed instructions. Do not continue.

2. **Show approval request:**

   ```
   Migration: v2.1 → v2.2

   Files REPLACED:
     CLAUDE.md  (rewritten — ~86% smaller)

   Files ADDED:
     scheduled-tasks/ops/session-memory.md
     scheduled-tasks/ops/blueprint-sync.md
     scheduled-tasks/ops/reference.md
     scheduled-tasks/ops/session-hygiene.md
     scheduled-tasks/ops/migrate.md
     scripts/check_deps.py
     scripts/wrap.py
     scripts/ready.py
     scripts/log_tail.py
     scripts/file_check.py
     scripts/estimate_tokens.py

   Files DELETED:
     scheduled-tasks/ops/token-reference.md

   Files UPDATED:
     scheduled-tasks/ops/audit.md  (recalibration sections removed)
     scheduled-tasks/ops/ingest.md (bash → Python, post-op advisory added)
     scheduled-tasks/ops/lint.md   (bash → Python, post-op advisory added)

   Files UNTOUCHED:
     wiki/  (all pages, index, log, hot preserved)
     memory.md, raw/, drafts/
     scheduled-tasks/ops/conventions.md, ingest.md* (beyond advisory update)
     sqlite-query skill (if installed)

   Shall I proceed?
   ```

3. **On approval, execute in order:**

   a. Create `backups/` directory if absent.
   b. Copy `CLAUDE.md` → `backups/CLAUDE.md-v2.1-<YYYY-MM-DD>.bak`
   c. Read `blueprint/template/CLAUDE.md`, substitute `[created-date]` and
      `[updated-date]` with today's date, remove the `> **Setup note:**` block,
      write result to `CLAUDE.md`.
   d. Copy each new ops file from `blueprint/template/scheduled-tasks/ops/` to
      `scheduled-tasks/ops/`:
      `session-memory.md`, `blueprint-sync.md`, `reference.md`,
      `session-hygiene.md`, `migrate.md`
   e. Create `scripts/` directory if absent.
   f. Copy each script from `blueprint/template/scripts/` to `scripts/`:
      `check_deps.py`, `wrap.py`, `ready.py`, `log_tail.py`,
      `file_check.py`, `estimate_tokens.py`
   g. Copy updated ops files from `blueprint/template/scheduled-tasks/ops/` to
      `scheduled-tasks/ops/`:
      `audit.md`, `ingest.md`, `lint.md`, `conventions.md`
   h. Delete `scheduled-tasks/ops/token-reference.md` if it exists.
   i. Patch `hot.md`:
      - Add `Python: [python | python3]` line (detect by running
        `python --version` or `python3 --version` and using whichever succeeds)
      - Update `Schema: v2.1` → `Schema: v2.2`
   j. Append to `wiki/log.md`:
      `## [YYYY-MM-DD] migrate | v2.1 → v2.2 — lean cold-start restructure`
      (≤500 chars)

4. **Confirm:**
   > "Migration complete. Cold-start: ~7,780 → ~1,080 tokens.
   > Backup saved to `backups/CLAUDE.md-v2.1-<date>.bak` — delete when satisfied."

5. **Offer Claude Code enhanced skill:**
   > "Are you using Claude Code CLI? Run `!! install claude-code-enhanced` to add
   > /wrap, /ready, and /migrate as native slash commands."

---

## Rollback

Rename `backups/CLAUDE.md-v2.1-<date>.bak` → `CLAUDE.md`.
All other v2.1 files are untouched; the new ops files and `scripts/` are inert
without the v2.2 `CLAUDE.md` referencing them.
```

- [ ] **Step 2: Commit**

```bash
git add template/scheduled-tasks/ops/migrate.md
git commit -m "feat: add ops/migrate.md — v2.1 → v2.2 migration flow"
```

---

## Phase 3 — Update Existing Ops Files

### Task 12: update ops/audit.md

Remove recalibration step, update token estimate reference, add post-op advisory, update audit-all token note.

**Files:**
- Modify: `template/scheduled-tasks/ops/audit.md`

- [ ] **Step 1: Remove step 7 (recalibration)**

Find and delete the entire step 7 line:
```
7. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section) — only if an applied fix changed a tracked file's size enough to exceed its documented Chars value.
```

- [ ] **Step 2: Update step 5 — replace token-reference.md cost with estimate_tokens.py**

Replace:
```
Show a normal approval request (summary + token estimate including the `token-reference.md` self-cost (see `@scheduled-tasks/ops/token-reference.md` header) + to-do list of affected files).
```

With:
```
Show a normal approval request (summary + token estimate via `python scripts/estimate_tokens.py <affected-files>` + to-do list of affected files).
```

- [ ] **Step 3: Update the audit-all token note (Notes section)**

Replace:
```
For `!! audit all`, expect ~30,000–47,000 tokens of reads for the tracked files (re-derive by summing the blueprint-doc and template-side rows in `token-reference.md`). Warn the user up front if the session is already close to context limits.
```

With:
```
For `!! audit all`, expect ~30,000–47,000 tokens of reads for the tracked files. Run `python scripts/estimate_tokens.py blueprint/README.md blueprint/setup-guide.md blueprint/user-guide.md blueprint/troubleshooting.md blueprint/template/CLAUDE.md blueprint/template/scheduled-tasks/refresh-hot.md blueprint/template/scheduled-tasks/ops/*.md blueprint/skills/sqlite-query/*.md` for a live estimate. Warn the user up front if the session is already close to context limits.
```

- [ ] **Step 4: Add post-op advisory step**

Append to the Steps section (after the renumbered final step 6):

```
7. **Post-op advisory.** Append the session advisory block from `@scheduled-tasks/ops/session-hygiene.md` (Post-op advisory block section) to this response. Set `SESSION_HEAVY = true`.
```

- [ ] **Step 5: Commit**

```bash
git add template/scheduled-tasks/ops/audit.md
git commit -m "fix: update audit.md — remove recalibration step, use estimate_tokens.py, add post-op advisory"
```

---

### Task 13: update ops/ingest.md

Replace bash grep+tail, replace token-reference.md references, remove step 13, add post-op advisory.

**Files:**
- Modify: `template/scheduled-tasks/ops/ingest.md`

- [ ] **Step 1: Replace grep+tail in Step 1**

Replace:
```
1. Read the last 5 entries of `wiki/log.md` for recent context (`grep -E "^## \[" wiki/log.md | tail -5`)
```
With:
```
1. Read the last 5 entries of `wiki/log.md` for recent context: run `python scripts/log_tail.py`
```

- [ ] **Step 2: Update Step 4 — replace token-reference.md with estimate_tokens.py**

Replace:
```
4. Show approval request (summary + token estimate + to-do list) and wait for confirmation — include the cost of re-reading `token-reference.md` itself (see the self-cost figure in its header) in the estimate
```
With:
```
4. Show approval request (summary + token estimate + to-do list) and wait for confirmation — run `python scripts/estimate_tokens.py <files-to-write>` to compute the estimate
```

- [ ] **Step 3: Update B4 — remove token-reference.md mention**

Replace:
```
B4. Show a combined approval request listing every filename, the per-file and total token cost (including the B3.5 pre-reads and **one** (not per-file) read of `token-reference.md`), and all pages to be created/updated across the batch. Use the same per-approval `token-reference.md` cost as a single-file ingest. This stands in for `[main-steps 3 and 4]`
```
With:
```
B4. Show a combined approval request listing every filename, the per-file and total token cost (including the B3.5 pre-reads — run `python scripts/estimate_tokens.py <files-to-write>` for the estimate), and all pages to be created/updated across the batch. This stands in for `[main-steps 3 and 4]`
```

- [ ] **Step 4: Remove step 13 (recalibration)**

Find and delete:
```
13. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section)
```

Also remove its reference in B5:
```
skip `[main-steps 1, 3, 4, 12, 13]`
```
→ Change to:
```
skip `[main-steps 1, 3, 4, 12]`
```

And update B6:
```
B6. After all files are processed, run `[main-steps 12 and 13]` **ONCE** at the end of the batch
```
→ Change to:
```
B6. After all files are processed, run `[main-step 12]` **ONCE** at the end of the batch
```

- [ ] **Step 5: Add post-op advisory (new step 13)**

Append to the Steps section:
```
13. **Post-op advisory.** Append the session advisory block from `@scheduled-tasks/ops/session-hygiene.md` (Post-op advisory block section) to this response. Set `SESSION_HEAVY = true`.
```

Also update B6 to include the advisory at batch level:
```
B6. After all files are processed, run `[main-step 12]` **ONCE** at the end of the batch, then run `[main-step 13]` (post-op advisory).
```

- [ ] **Step 6: Commit**

```bash
git add template/scheduled-tasks/ops/ingest.md
git commit -m "fix: update ingest.md — use log_tail.py, estimate_tokens.py, remove recalibration, add advisory"
```

---

### Task 14: update ops/lint.md

Replace bash grep+tail, replace token-reference.md references, remove step 10, add post-op advisory.

**Files:**
- Modify: `template/scheduled-tasks/ops/lint.md`

- [ ] **Step 1: Replace grep+tail in Step 2**

Replace:
```
2. Read the last 5 entries of `wiki/log.md` for recent context (`grep -E "^## \[" wiki/log.md | tail -5`)
```
With:
```
2. Read the last 5 entries of `wiki/log.md` for recent context: run `python scripts/log_tail.py`
```

- [ ] **Step 2: Update Step 5 — replace token-reference.md with estimate_tokens.py**

Replace:
```
5. Show approval request (summary + token estimate + to-do list) for any fixes — include the cost of re-reading `token-reference.md` itself (see the self-cost figure in its header) in the estimate
```
With:
```
5. Show approval request (summary + token estimate + to-do list) for any fixes — run `python scripts/estimate_tokens.py <files-to-write>` to compute the estimate
```

- [ ] **Step 3: Remove step 10 (recalibration)**

Find and delete:
```
10. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section) — only if any file's measured actual now exceeds its documented Chars value
```

- [ ] **Step 4: Add post-op advisory (new step 10)**

Append to the Steps section:
```
10. **Post-op advisory.** Append the session advisory block from `@scheduled-tasks/ops/session-hygiene.md` (Post-op advisory block section) to this response. Set `SESSION_HEAVY = true`.
```

- [ ] **Step 5: Commit**

```bash
git add template/scheduled-tasks/ops/lint.md
git commit -m "fix: update lint.md — use log_tail.py, estimate_tokens.py, remove recalibration, add advisory"
```

---

### Task 15: update ops/conventions.md — append Filing Answers

**Files:**
- Modify: `template/scheduled-tasks/ops/conventions.md`

- [ ] **Step 1: Append the Filing Answers section at end of file**

Append to the very end of `template/scheduled-tasks/ops/conventions.md`:

```markdown

## Filing Answers (Query Step 2 / Step 3)

After any Step 2 (wiki) or Step 3 (web) answer, ask: "Worth filing this as an analysis page?"

If yes:
1. Read this file (`@scheduled-tasks/ops/conventions.md`) — already loaded, no extra read needed
2. Show approval request with token estimate (`python scripts/estimate_tokens.py wiki/pages/analyses/<slug>.md` after drafting) and file list
3. Wait for confirmation
4. Write to `wiki/pages/analyses/<slug>.md` following all conventions above
5. Update `wiki/index.md` and append to `wiki/log.md` (≤500 chars):
   `## [YYYY-MM-DD] query | [Question summary]`
6. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`

Log format: `## [YYYY-MM-DD] query | [Question summary]` (≤500 chars)
```

- [ ] **Step 2: Commit**

```bash
git add template/scheduled-tasks/ops/conventions.md
git commit -m "fix: append Filing Answers section to conventions.md"
```

---

## Phase 4 — Rewrite template/CLAUDE.md

### Task 16: write lean CLAUDE.md

This is the critical step. Read the current `template/CLAUDE.md` in full before writing to understand every section being removed.

**Files:**
- Rewrite: `template/CLAUDE.md`

- [ ] **Step 1: Read current template/CLAUDE.md in full**

Confirm you have read the entire file before proceeding.

- [ ] **Step 2: Write the new lean CLAUDE.md**

Write the following content to `template/CLAUDE.md`:

````markdown
# LLM Wiki — Agent Schema

You are the **LLM Wiki Agent**. Your job is to maintain a persistent, compounding wiki — reading sources, extracting knowledge, and keeping everything interconnected and up to date.

---

## Startup (Every Session)

1. Read `CLAUDE.md` (this file)
2. Read `wiki/hot.md`
3. Check `drafts/` — list filenames only, up to 20 (if more than 20 exist, list the 20 most recently modified and note the overflow count)
4. Detect environment: if `.claude/` exists at working folder root → Claude Code mode; else → Cowork mode
5. Detect Python: read `Python:` field from `hot.md`; if absent, run `python scripts/check_deps.py --python`, cache the resolved command (`python` or `python3`) in `hot.md`
6. If opening message is `!! ready`: read `@scheduled-tasks/ops/session-memory.md` and follow it — skip step 7
7. Announce readiness: one-line summary from `hot.md`, plus any in-progress drafts (e.g. "1 draft in progress: `topic-name.md`"). If no drafts, say nothing about it.
   - If `hot.md`'s `Schema:` is below `v2.2`: announce "Blueprint v2.2 is available — run `!! migrate` to update." (once per session)
   - If `wiki/` absent at working folder root: announce "Blueprint-authoring mode — no wiki/ at working-folder root; only `!! audit` is expected to run."

**CRITICAL: Complete ALL startup steps (1–7) before composing your first response. No exceptions.**

> **Estimates only:** All token figures are `chars ÷ 4` estimates. Actual usage varies by tokenizer, file contents, and runtime overhead.

---

## Query Routing Rule

**CRITICAL: Follow this waterfall for every user question — no exception for perceived simplicity or confidence level.**

**Step 1 — Training knowledge**
If highly confident AND question clearly does not touch wiki content → answer directly with citations where relevant. Stop.

Skip Step 1 for:
- Wiki-topology questions ("which pages cover X", "is X in the wiki", "what pages exist for Y")
- Any question that could be answered by wiki content ("what is X", "how does X work", "tell me about X")
- Any question when `Active skills` in `hot.md` lists an installed query layer

**Step 2 — Wiki**
1. Run `python scripts/log_tail.py` for last 5 log entries
2. If `scheduled-tasks/query-layer.md` exists → read and follow it; fall back to step 3 on empty/failure
3. Grep `wiki/pages` for topic slug; if no match, read `wiki/index.md`
4. Read candidate pages; answer with `[[wiki link]]` citations
5. Ask: "Worth filing as an analysis page?" — if yes, read `@scheduled-tasks/ops/conventions.md` first

**Step 3 — Web**
Search → summarize → ask to ingest. If yes: save to `wiki/inbox/`, run INGEST op.

---

## Ops Routing

**CRITICAL: Read the matching file before starting any operation.**

| Trigger | Read |
|---|---|
| Ingest a source | `@scheduled-tasks/ops/ingest.md` |
| Lint the wiki | `@scheduled-tasks/ops/lint.md` |
| Audit the blueprint | `@scheduled-tasks/ops/audit.md` |
| Update a page | `@scheduled-tasks/ops/update.md` |
| Create or edit any page | `@scheduled-tasks/ops/conventions.md` |
| `!! install <skill>` | `@blueprint/skills/<skill>/SKILL.md` |
| After any wiki-state change | `@scheduled-tasks/refresh-hot.md` |
| `!! wrap` / `!! ready` | `@scheduled-tasks/ops/session-memory.md` |
| Blueprint file edit | `@scheduled-tasks/ops/blueprint-sync.md` |
| `!! migrate` | `@scheduled-tasks/ops/migrate.md` |
| Directory / structure query | `@scheduled-tasks/ops/reference.md` |

> **`@`-prefixed paths** are working-folder-relative — they resolve against whichever folder you selected at setup, regardless of its name.

> **Token estimates:** Before any approval request, run `python scripts/estimate_tokens.py <file1> [file2 ...]` on the files to be written or edited. Use the output as the estimate.

> **File existence checks:** Use `python scripts/file_check.py <path>` — never Glob for specific files.

> **Tool reliability:** Never use the Glob tool to test whether a specific file exists. Glob can silently return empty for files that are present.

---

## Core Rules

**Approval:** Before any file create/edit/delete — present: (1) one-line summary, (2) token estimate from `estimate_tokens.py`, (3) to-do list of every file affected, (4) "Shall I proceed?" Read-only actions do not require approval.

Exceptions (user invocation is implicit approval): `!! wrap`, `!! ready`, `!! audit` — see `@scheduled-tasks/ops/session-memory.md` for wrap/ready detail.

**Suggestion:** Whenever suggesting a change, always present both pros and cons before asking for approval. Never recommend without showing trade-offs.

**Session hygiene:** After any `!! ingest`, `!! lint`, or `!! audit` op completes, set `SESSION_HEAVY = true`. If `SESSION_HEAVY` is set and the user issues any `!! command` (except `!! wrap`, `!! ready`, `!! proceed`), read `@scheduled-tasks/ops/session-hygiene.md` and follow it. `!! proceed` clears `SESSION_HEAVY`.

**Blueprint-authoring mode:** If `wiki/` is absent at the working folder root, skip all `wiki/log.md` appends and `hot.md` refreshes across all ops. Check once per op (`python scripts/file_check.py wiki/log.md`); if absent, skip transparently without prompting.

---

## Response Footer

**CRITICAL: Every single response — without exception — must end with the footer block exactly as shown: 5 command-hint lines, then a blank separator, then the 💡 tip line, then the 📋 compliance line (8 physical lines total). Missing any content line is an error.**

```
📥 !! ingest: [URL | Page Name | All]
🧹 !! lint: [Page Name | All]
🔍 !! audit: [Page Name | All]
💾 !! wrap: [save session summary to memory]
🔄 !! ready: [load session summary at start of new session]

💡 Using Obsidian Web Clipper to save articles as markdown before ingesting is 40–60% cheaper in token usage than fetching directly from a URL.
📋 Waterfall: [step taken] | Ops: [file read or N/A]
```

**CRITICAL: All 5 command-hint lines, the compliance line, and the 💡 tip line are required in every response. Missing any content line is an error.**

Fill `📋 Waterfall:` accurately on every response — waterfall step taken (e.g. `Step 2 via sqlite-query`, `Step 1 (training knowledge)`) and ops file read (e.g. `ingest.md`, or `N/A` if none). This makes rule adherence externally visible.

Show brackets literally for command-hint lines.

---

## Formats

**index.md:** `- [[Page Title]] — one-line summary | updated: YYYY-MM-DD | sources: N`

**hot.md:**
```
---
updated: YYYY-MM-DD
---
Pages: N | Schema: vX.Y | Updated: YYYY-MM-DD
Last op: [operation] YYYY-MM-DD ([one-line result])
Gaps: [comma-separated open data gaps]
Hot: [comma-separated titles of 5 most recently updated pages]
Active skills: [comma-separated installed skill names, or "none"]
Python: [python | python3]
```

**log.md:** Append-only. Each entry: `## [YYYY-MM-DD] operation | title` (≤500 chars).
Always read tail only — run `python scripts/log_tail.py`. Fallback (if scripts/ absent): `grep -E "^## \[" wiki/log.md | tail -5`

---

*Schema version: 2.2 | Created: [created-date] | Updated: [updated-date]*

> **Setup note:** Replace `[created-date]` and `[updated-date]` with today's date in YYYY-MM-DD format.
````

- [ ] **Step 3: Verify character count is under ~5,000 chars**

```bash
python -c "print(len(open('template/CLAUDE.md').read()), 'chars')"
```
Expected: under 5,000 chars (~1,250 tokens)

- [ ] **Step 4: Commit**

```bash
git add template/CLAUDE.md
git commit -m "feat: rewrite CLAUDE.md to lean v2.2 — 86% cold-start reduction"
```

---

## Phase 5 — Delete token-reference.md and Update .gitignore

### Task 17: delete token-reference.md and update .gitignore

**Files:**
- Delete: `template/scheduled-tasks/ops/token-reference.md`
- Modify: `.gitignore`

- [ ] **Step 1: Delete token-reference.md**

```bash
git rm template/scheduled-tasks/ops/token-reference.md
```

- [ ] **Step 2: Add backups/ to .gitignore**

Append to `.gitignore`:
```
# Migration backups
backups/
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "feat: delete token-reference.md (replaced by estimate_tokens.py); gitignore backups/"
```

---

## Phase 6 — Update Blueprint Docs

### Task 18: update setup-guide.md

**Files:**
- Modify: `setup-guide.md`

- [ ] **Step 1: Update Step 1 — add scripts/ to mkdir list**

In the `mkdir -p` block, add after `mkdir -p scheduled-tasks/ops`:
```bash
mkdir -p scripts
mkdir -p backups
```

- [ ] **Step 2: Update Step 2 — remove token-reference.md row, add new ops file rows and scripts copy**

Remove this row from the copy table:
```
| `blueprint/template/scheduled-tasks/ops/token-reference.md` | `scheduled-tasks/ops/token-reference.md` |
```

Add these rows:
```
| `blueprint/template/scheduled-tasks/ops/session-memory.md` | `scheduled-tasks/ops/session-memory.md` |
| `blueprint/template/scheduled-tasks/ops/blueprint-sync.md` | `scheduled-tasks/ops/blueprint-sync.md` |
| `blueprint/template/scheduled-tasks/ops/reference.md` | `scheduled-tasks/ops/reference.md` |
| `blueprint/template/scheduled-tasks/ops/session-hygiene.md` | `scheduled-tasks/ops/session-hygiene.md` |
| `blueprint/template/scheduled-tasks/ops/migrate.md` | `scheduled-tasks/ops/migrate.md` |
| `blueprint/template/scripts/check_deps.py` | `scripts/check_deps.py` |
| `blueprint/template/scripts/wrap.py` | `scripts/wrap.py` |
| `blueprint/template/scripts/ready.py` | `scripts/ready.py` |
| `blueprint/template/scripts/log_tail.py` | `scripts/log_tail.py` |
| `blueprint/template/scripts/file_check.py` | `scripts/file_check.py` |
| `blueprint/template/scripts/estimate_tokens.py` | `scripts/estimate_tokens.py` |
```

- [ ] **Step 3: Add Step 2.5 — Python check**

Insert after Step 2 and before Step 3:

```markdown
## Step 2.5 — Check Python

Run `python scripts/check_deps.py --python` (or `python3 scripts/check_deps.py --python` on macOS/Linux).

- If it prints `✓ Python X.Y.Z`: record the working command (`python` or `python3`) — you will write it to `hot.md` in Step 4.
- If it prints installation instructions: follow them, then retry before continuing.
```

- [ ] **Step 4: Update Step 4 — add Python: field to hot.md initialisation**

In the hot.md template block, add `Python: [python | python3]` as the last line (substituting the resolved command found in Step 2.5):

```markdown
Active skills: none
Python: python
```
(or `python3` depending on what Step 2.5 resolved)

- [ ] **Step 5: Update Step 4.5 — rename and extend the offer step**

Rename the existing "Step 4.5 — Offer SQLite Query Skill" to keep its numbering but add a new sub-offer:

After the existing SQLite offer block, append:

```markdown
**Claude Code CLI users:** If you are using Claude Code CLI (not Claude Desktop Cowork), also ask:

> "Would you like to install the Claude Code enhanced skill? It adds native slash commands `/wrap`, `/ready`, and `/migrate` as alternatives to the `!! command` syntax. Install with `!! install claude-code-enhanced`."
```

- [ ] **Step 6: Update Step 7 — update ops file count and add scripts/ check**

Replace:
```
- [ ] All 6 ops files exist in `scheduled-tasks/ops/`
```
With:
```
- [ ] All 11 ops files exist in `scheduled-tasks/ops/`
      (ingest, lint, audit, update, conventions, session-memory, blueprint-sync, reference, session-hygiene, migrate, refresh-hot)
- [ ] All 6 scripts exist in `scripts/`
      (check_deps.py, wrap.py, ready.py, log_tail.py, file_check.py, estimate_tokens.py)
```

- [ ] **Step 7: Commit**

```bash
git add setup-guide.md
git commit -m "fix: update setup-guide.md for v2.2 — scripts/, Python check, new ops files"
```

---

### Task 19: update user-guide.md

**Files:**
- Modify: `user-guide.md`

- [ ] **Step 1: Update cold-start figures**

Replace all occurrences of `~7,780 tokens` with `~1,080 tokens`.
Replace all occurrences of `~7,700 tokens` (CLAUDE.md self-cost) with `~1,000 tokens`.
Replace `~8,730 tokens` (`!! ready` total) with `~1,830 tokens` (1,080 + 750 for session-memory.md).

- [ ] **Step 2: Remove token-reference.md references**

Remove any sentence referencing `token-reference.md` or the Recalibration Rule. Replace with a note that token estimates are computed dynamically via `scripts/estimate_tokens.py`.

- [ ] **Step 3: Add Session Hygiene section**

Add after the `!! wrap` / `!! ready` section:

```markdown
### Session Hygiene

After `!! ingest`, `!! lint`, or `!! audit` completes, the agent will show a session advisory recommending you start a new session before doing more work. This is because each turn in a long session re-reads the entire conversation history, increasing cost non-linearly.

**Recommended workflow:**
- One ingest (or batch ingest) per session
- One lint pass per session  
- `!! audit all` always in its own session

To dismiss the advisory and continue anyway, say `!! proceed`. The agent will resume normally.
```

- [ ] **Step 4: Add Scripts section**

Add after the `!! install` section:

```markdown
### Cross-Platform Scripts

The agent uses a set of Python scripts under `scripts/` for file operations that previously required bash. These scripts work identically on Windows, macOS, and Linux.

You do not need to call them directly — the agent uses them automatically. If a script fails, the agent will show the error and suggest a fix.

Python 3.8+ is required. If Python is not installed, the agent will show OS-specific installation instructions the first time a script is needed.
```

- [ ] **Step 5: Update the cost table**

In the "Typical session costs" table, update:
```
| Cold start | ~7,780 |
```
To:
```
| Cold start | ~1,080 |
```

And update:
```
| Cold start with `!! ready` (full memory) | ~8,730 |
```
To:
```
| Cold start with `!! ready` (full memory) | ~1,830 |
```

And update the `!! audit all` range if it mentions deriving from token-reference.md.

- [ ] **Step 6: Add claude-code-enhanced mention to the !! install section**

In the "Installing Skills — `!! install`" section, add:

```markdown
- `!! install claude-code-enhanced` — (Claude Code CLI only) registers `/wrap`, `/ready`, and `/migrate` as native slash commands. Works alongside the `!! command` syntax — both remain available.
```

- [ ] **Step 7: Commit**

```bash
git add user-guide.md
git commit -m "fix: update user-guide.md for v2.2 — token figures, session hygiene, scripts section"
```

---

### Task 20: update ROADMAP.md and CHANGELOG.md

**Files:**
- Modify: `ROADMAP.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Update ROADMAP.md — mark claude-code-enhanced as shipped**

Add to the skills table:
```
| `claude-code-enhanced` | ✅ Shipped | Optional Claude Code CLI skill. Registers /wrap, /ready, /migrate as native slash commands. |
```

- [ ] **Step 2: Add CHANGELOG.md entry for v2.2.0**

Prepend a new section at the top of CHANGELOG.md (after the header):

```markdown
## v2.2.0 — 2026-04-25

### Cold-start optimization, cross-platform scripts, session hygiene

**Cold-start reduction (~86%):** `CLAUDE.md` rewritten from ~7,700 to ~1,000 tokens. Three large sections extracted into deferred ops files loaded only when triggered:
- `ops/session-memory.md` — `!! wrap`/`!! ready` full state machine (~750 tokens, loaded on command)
- `ops/blueprint-sync.md` — Blueprint Sync 12-row cascade (~625 tokens, loaded on blueprint edit)
- `ops/reference.md` — directory structure + tiered read table (~400 tokens, on demand)

**Cross-platform Python scripts:** Six scripts added to `template/scripts/`. Bash commands replaced:
- `log_tail.py` replaces `grep -E "^## \[" log.md | tail -5`
- `file_check.py` replaces `[ -f path ] && echo exists`
- `wrap.py` / `ready.py` replace `!! wrap`/`!! ready` state machine prose
- `check_deps.py` — OS-aware Python 3.8+ and SQLite availability checks (Windows/macOS/Linux)
- `estimate_tokens.py` — dynamic token estimation replacing `token-reference.md`

**token-reference.md removed:** Replaced by `estimate_tokens.py` which reads live file sizes at approval time. No more recalibration rule, headroom tables, or envelope math. `ops/audit.md` simplified accordingly.

**Session hygiene soft block:** After `!! ingest`, `!! lint`, or `!! audit` completes, agent shows advisory recommending a new session. Follow-up `!! commands` trigger a soft intercept with `!! wrap`/`!! ready` instructions. `!! proceed` clears the block.

**New commands:** `!! migrate` upgrades existing v2.1.x working folders to v2.2 with full backup and rollback support.

**Optional claude-code-enhanced skill:** Claude Code CLI users can `!! install claude-code-enhanced` for native `/wrap`, `/ready`, `/migrate` slash commands.

**hot.md format:** New `Python:` field stores resolved Python command (`python` or `python3`) at setup time.

**Schema:** v2.1 → v2.2. No user-facing command syntax changes.
```

- [ ] **Step 3: Commit**

```bash
git add ROADMAP.md CHANGELOG.md
git commit -m "docs: update ROADMAP.md and CHANGELOG.md for v2.2.0"
```

---

## Phase 7 — Claude Code Enhanced Skill

### Task 21: create claude-code-enhanced skill

**Files:**
- Create: `blueprint/skills/claude-code-enhanced/SKILL.md`
- Create: `blueprint/skills/claude-code-enhanced/slash-commands.md`

- [ ] **Step 1: Create SKILL.md**

```markdown
# Skill: claude-code-enhanced

**Environment:** Claude Code CLI only. This skill has no effect in Claude Desktop Cowork.

**Purpose:** Registers `/wrap`, `/ready`, and `/migrate` as native Claude Code slash commands, wrapping the same Python scripts used by the `!! command` equivalents.

---

## Install

```
!! install claude-code-enhanced
```

The agent will:
1. Verify `.claude/` exists at working folder root (confirms Claude Code environment)
2. Copy `blueprint/skills/claude-code-enhanced/slash-commands.md` to `scheduled-tasks/claude-code-enhanced.md`
3. Confirm: "claude-code-enhanced installed. You can now use /wrap, /ready, and /migrate alongside the !! command syntax."

## Uninstall

```
!! uninstall claude-code-enhanced
```

Deletes `scheduled-tasks/claude-code-enhanced.md`. The `!! wrap`, `!! ready`, and `!! migrate` commands remain available.

---

## Offered During Setup

**Step 4.5** of `setup-guide.md` offers this skill to Claude Code CLI users after the SQLite skill offer.
```

- [ ] **Step 2: Create slash-commands.md**

```markdown
# Claude Code Enhanced — Slash Command Wrappers

This file is read when the user invokes `/wrap`, `/ready`, or `/migrate` in Claude Code CLI.
These are thin wrappers — all logic lives in the ops files and scripts.

---

## /wrap

Equivalent to `!! wrap`. Read `@scheduled-tasks/ops/session-memory.md` and follow the `!! wrap` flow.

## /ready

Equivalent to `!! ready`. Read `@scheduled-tasks/ops/session-memory.md` and follow the `!! ready` flow.

## /migrate

Equivalent to `!! migrate`. Read `@scheduled-tasks/ops/migrate.md` and follow the migration flow.

## /sync

Equivalent to triggering the blueprint sync rule. Read `@scheduled-tasks/ops/blueprint-sync.md` and confirm which files need updating based on the change just made.
```

- [ ] **Step 3: Commit**

```bash
git add blueprint/skills/claude-code-enhanced/
git commit -m "feat: add claude-code-enhanced skill — /wrap /ready /migrate slash commands for Claude Code CLI"
```

---

## Phase 8 — Final Verification

### Task 22: run audit and verify no cross-reference drift

- [ ] **Step 1: Verify all new files exist**

```bash
python template/scripts/file_check.py template/scripts/check_deps.py
python template/scripts/file_check.py template/scripts/log_tail.py
python template/scripts/file_check.py template/scripts/file_check.py
python template/scripts/file_check.py template/scripts/estimate_tokens.py
python template/scripts/file_check.py template/scripts/wrap.py
python template/scripts/file_check.py template/scripts/ready.py
python template/scripts/file_check.py template/scheduled-tasks/ops/session-memory.md
python template/scripts/file_check.py template/scheduled-tasks/ops/blueprint-sync.md
python template/scripts/file_check.py template/scheduled-tasks/ops/reference.md
python template/scripts/file_check.py template/scheduled-tasks/ops/session-hygiene.md
python template/scripts/file_check.py template/scheduled-tasks/ops/migrate.md
python template/scripts/file_check.py blueprint/skills/claude-code-enhanced/SKILL.md
python template/scripts/file_check.py blueprint/skills/claude-code-enhanced/slash-commands.md
```
Expected: `exists` for every line

- [ ] **Step 2: Verify token-reference.md is deleted**

```bash
python template/scripts/file_check.py template/scheduled-tasks/ops/token-reference.md
```
Expected: `not found`

- [ ] **Step 3: Verify lean CLAUDE.md character count**

```bash
python -c "s=open('template/CLAUDE.md').read(); print(len(s), 'chars,', len(s)//4, 'est tokens')"
```
Expected: under 5,000 chars

- [ ] **Step 4: Run estimate_tokens.py on new files to confirm they have content**

```bash
python template/scripts/estimate_tokens.py \
  template/CLAUDE.md \
  template/scheduled-tasks/ops/session-memory.md \
  template/scheduled-tasks/ops/blueprint-sync.md \
  template/scheduled-tasks/ops/reference.md \
  template/scheduled-tasks/ops/session-hygiene.md \
  template/scheduled-tasks/ops/migrate.md
```
Expected: all files show non-zero token estimates

- [ ] **Step 5: Open a new session and run `!! audit all`**

Start a fresh session (new chat). The agent should cold-start reading only the lean CLAUDE.md and hot.md.

Run: `!! audit all`

Expected:
- No CRITICAL findings
- No blueprint-sync drift between CLAUDE.md, user-guide.md, setup-guide.md, README.md
- All 34+ cross-reference checks pass
- Audit notes no references to deleted `token-reference.md`
- Footer block identical across template/CLAUDE.md, setup-guide.md Step 8, user-guide.md Footer Commands

- [ ] **Step 6: Commit final state**

```bash
git add -A
git commit -m "chore: v2.2.0 implementation complete — verified by audit"
```
