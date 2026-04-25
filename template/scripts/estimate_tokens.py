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
