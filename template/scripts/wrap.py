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
