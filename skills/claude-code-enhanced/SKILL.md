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
