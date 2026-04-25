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
