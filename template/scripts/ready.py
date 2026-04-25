#!/usr/bin/env python3
"""
Session memory read, truncation detection, and state transitions.
Usage:
  python scripts/ready.py read    read state + full content
  python scripts/ready.py clear   wipe memory.md to EMPTY
  python scripts/ready.py keep    mark truncated snapshot as acknowledged

Exit codes for 'read':
  0 = EMPTY or TRUNCATED_ACKNOWLEDGED (no valid snapshot to consume)
  1 = WRAPPED + COMPLETE (valid snapshot, safe to consume and wipe)
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
    "*(empty — use `!! wrap` at the end of a session to save a snapshot here)*\n"
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
    print("[OK] memory.md cleared to EMPTY state")


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
    print("[OK] memory.md marked as TRUNCATED_ACKNOWLEDGED")


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
