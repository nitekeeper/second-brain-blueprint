# Design: `!! wrap` Compact Redesign

**Date:** 2026-04-25
**Status:** Approved

---

## Problem

The current `!! wrap` command produces a human-readable structured summary (`Thread`, `Next`, `Decisions`, `Changed`, `Watch out`) intended to bridge sessions. This format is optimized for human readability, not for Claude's context restoration. It also enforces a 2,400-character hard limit that can force dropping necessary content.

The core purpose of `!! wrap` is: **mid-task context preservation for Claude, not the user.** The user stops working in a bloated session; Claude saves exactly what it needs to continue the task in a fresh session.

---

## Goals

- `!! wrap` produces a compact, Claude-internal context snapshot
- Format is optimized for Claude's fast context restoration, not human readability
- No artificial size restriction — the filter (exclude resolved/wiki content) is the only compression mechanism
- `!! ready` and `wrap.py` script lifecycle remain unchanged

---

## Out of Scope

- `!! ready` behavior — no changes
- `ready.py` script — no changes
- State markers (`MEMORY_STATE: WRAPPED`, `MEMORY_WRAP_COMPLETE`) — no changes

---

## Snapshot Format

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

The block is wrapped in the existing state markers by `wrap.py`:

```
<!-- MEMORY_STATE: WRAPPED -->
[SNAPSHOT]
...
[/SNAPSHOT]
<!-- MEMORY_WRAP_COMPLETE -->
```

---

## Composition Rules

**Include:**
- What task is in flight
- Exactly where in the task execution we stopped
- The single next action to take
- Decisions already locked in that should not be revisited
- File paths actively in play
- Real blockers or gotchas (only if they exist)

**Exclude:**
- Anything already captured in the wiki
- Resolved steps and completed work
- Conversation history and back-and-forth
- Rationale that is visible by reading the current file state

**No token target.** The filter above is the compression mechanism. Do not drop necessary content to hit a size number.

**WATCH is optional.** Omit the line entirely if there is nothing real to flag.

---

## Changes Required

### 1. `template/scripts/wrap.py`

- Remove `MAX_BODY_CHARS = 2400` constant
- Remove exit code 3 and the over-target warning path from the `write` subcommand
- `write` subcommand exit codes after change: `0` (success only)
- `check` subcommand exit codes unchanged: `0` (EMPTY), `1` (WRAPPED), `2` (TRUNCATED_ACKNOWLEDGED)
- Update docstring to remove exit 3 reference

### 2. `template/scheduled-tasks/ops/session-memory.md`

In the `!! wrap` section:

- **Step 3:** Replace the current summary format and composition rules with the new `[SNAPSHOT]` format and composition rules above
- **Remove** the "Target: ≤2,400 characters" guidance
- **Remove** the exit 3 handling (trim/keep prompt and user decision flow)
- **Update** exit 0 confirmation: just confirm snapshot saved and instruct to close and reopen session

---

## Files Affected

- `template/scripts/wrap.py`
- `template/scheduled-tasks/ops/session-memory.md`
