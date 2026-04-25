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
