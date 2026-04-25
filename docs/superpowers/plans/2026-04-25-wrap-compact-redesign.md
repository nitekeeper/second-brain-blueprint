# `!! wrap` Compact Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the human-readable session summary format in `!! wrap` with a compact Claude-internal context snapshot, and remove the 2,400-character hard limit from `wrap.py`.

**Architecture:** Two files change. `wrap.py` loses the `MAX_BODY_CHARS` constant and exit-3 warning path — `write` always exits 0 on success. `session-memory.md` replaces step 3's human-readable format and composition rules with the new `[SNAPSHOT]` block format and updated exit-0 confirmation.

**Tech Stack:** Python 3, Markdown

---

## File Map

| File | Change |
|---|---|
| `template/scripts/wrap.py` | Remove `MAX_BODY_CHARS`, remove exit-3 path, update docstring |
| `template/scheduled-tasks/ops/session-memory.md` | Replace step 3 of `!! wrap` section with new snapshot format and rules |

---

### Task 1: Update `wrap.py`

**Files:**
- Modify: `template/scripts/wrap.py`

- [ ] **Step 1: Replace the file with the updated version**

Full replacement of `template/scripts/wrap.py`:

```python
#!/usr/bin/env python3
"""
Session memory write with marker-state handling.
Usage:
  python scripts/wrap.py check         check memory.md state
  python scripts/wrap.py write         write snapshot (reads body from stdin)

Exit codes for 'check':
  0 = EMPTY or file missing (safe to write)
  1 = WRAPPED (existing snapshot present — warn user before overwrite)
  2 = TRUNCATED_ACKNOWLEDGED (kept truncated snapshot — warn user before overwrite)

Exit codes for 'write':
  0 = success
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
    chars = len(summary)
    tokens = chars // 4
    content = f"{MARKER_WRAPPED}\n{summary}\n{MARKER_COMPLETE}\n"
    MEMORY.write_bytes(content.encode("utf-8"))
    print(f"[OK] Snapshot written to memory.md ({chars} chars, ~{tokens} tokens)")


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

- [ ] **Step 2: Verify `write` exits 0 and writes the snapshot correctly**

Run from the project root:

```bash
echo "[SNAPSHOT]
TASK: test task
STATE: test state
NEXT: test next
LOCKED: decision-a, decision-b
FILES: template/scripts/wrap.py
[/SNAPSHOT]" | python template/scripts/wrap.py write
```

Expected output:
```
[OK] Snapshot written to memory.md (... chars, ~... tokens)
```

Verify `template/memory.md` was written:

```bash
cat template/memory.md
```

Expected: file begins with `<!-- MEMORY_STATE: WRAPPED -->` and ends with `<!-- MEMORY_WRAP_COMPLETE -->`, with the `[SNAPSHOT]` block in between.

- [ ] **Step 3: Verify `check` returns WRAPPED after a write**

```bash
python template/scripts/wrap.py check
echo "exit: $?"
```

Expected output:
```
WRAPPED
exit: 1
```

- [ ] **Step 4: Clean up the test memory.md**

```bash
rm template/memory.md
python template/scripts/wrap.py check
echo "exit: $?"
```

Expected:
```
EMPTY
exit: 0
```

- [ ] **Step 5: Commit**

```bash
git add template/scripts/wrap.py
git commit -m "feat: remove MAX_BODY_CHARS limit and exit-3 path from wrap.py"
```

---

### Task 2: Update `session-memory.md`

**Files:**
- Modify: `template/scheduled-tasks/ops/session-memory.md`

- [ ] **Step 1: Replace step 3 of the `!! wrap` section**

In `template/scheduled-tasks/ops/session-memory.md`, replace everything from line 28 through line 60 (the entire step 3 block, from `3. **Digest pass:**` through `The script writes the summary with the correct state markers and completion marker.`) with:

```markdown
3. **Snapshot pass:** Scan the conversation and compose a Claude-internal context snapshot. This is for Claude's use only — not for human reading.

   **Include:**
   - What task is in flight
   - Exactly where in the task execution we stopped
   - The single next action to take
   - Decisions locked in that should not be revisited
   - File paths actively in play
   - Real blockers or gotchas (only if they exist)

   **Exclude:**
   - Anything already captured in the wiki
   - Resolved steps and completed work
   - Conversation history and back-and-forth
   - Rationale visible by reading the current file state

   **Format:**
   ```
   [SNAPSHOT]
   TASK: <one sentence — what is being built or fixed>
   STATE: <one sentence — exactly where in the task we stopped>
   NEXT: <one sentence — the single first action to take next session>
   LOCKED: <comma-separated decisions already made, not to revisit>
   FILES: <comma-separated file paths currently in play>
   WATCH: <one sentence — real blocker or gotcha only; omit line entirely if none>
   [/SNAPSHOT]
   ```

   Do not add prose, markdown headers, or explanation outside the `[SNAPSHOT]` block.

   Then pipe it to: `python scripts/wrap.py write`
   - **Exit 0:** Snapshot written. Confirm: "Snapshot saved (~N tokens). **Close this conversation and start a new one**, then say `!! ready` as your first message. Starting a new conversation is the only way to get a clean context — `!! wrap` saves state to a file but does not free the current session's context."
```

- [ ] **Step 2: Verify the full `!! wrap` section reads correctly**

Read `template/scheduled-tasks/ops/session-memory.md` and confirm:
- Step 3 uses `[SNAPSHOT]` format
- No mention of `≤2,400 characters`, `~600 tokens`, `trim`, or `ok`
- Exit 3 handling is gone
- Steps 1, 2, 4, 5, 6 are unchanged

- [ ] **Step 3: Commit**

```bash
git add template/scheduled-tasks/ops/session-memory.md
git commit -m "feat: replace !! wrap summary format with Claude-internal snapshot"
```

---

## Done

Both files updated. `!! wrap` now produces a compact `[SNAPSHOT]` block with no size restriction, optimized for Claude's context restoration in the next session.
