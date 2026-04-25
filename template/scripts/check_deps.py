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
