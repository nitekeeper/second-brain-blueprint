# Reference — Directory Structure and Tiered Read

Read this file when the user asks about the wiki folder layout, file locations, or read tiers.

---

## Directory Structure

> `<WorkingFolder>` below is whatever the user named their Cowork working folder (e.g. `Library`, `MyWiki`). Substitute mentally — this diagram is layout-only, not a literal path.

```
<WorkingFolder>/
├── CLAUDE.md                   ← This file. Auto-read every session. Lean core schema.
├── memory.md                   ← Session memory. Written by `!! wrap`, read+wiped by `!! ready`.
├── audits/                     ← Blueprint audit reports. Named AUD-YYYY-MM-DD-NNN.md. Developer use only.
├── docs/                       ← Design specs and implementation plans. Developer use only.
├── backups/                    ← Migration backups. Gitignored. e.g. CLAUDE.md-v2.1-YYYY-MM-DD.bak
├── raw/                        ← Timestamped source snapshots — naming: <slug>-<YYYY-MM-DD-HHMMSS>.md
├── drafts/                     ← In-progress planning files. Claude's scrapbook.
├── scripts/                    ← Cross-platform Python utility scripts
│   ├── check_deps.py
│   ├── wrap.py
│   ├── ready.py
│   ├── log_tail.py
│   ├── file_check.py
│   └── estimate_tokens.py
├── blueprint/                  ← Setup guide and templates for sharing this system
│   ├── LICENSE
│   ├── .gitignore
│   ├── README.md
│   ├── setup-guide.md
│   ├── user-guide.md
│   ├── troubleshooting.md
│   ├── CHANGELOG.md
│   ├── ROADMAP.md
│   ├── docs/                   ← Audit report template and design specs. Developer use only.
│   │   └── audit-report-template.md
│   ├── template/
│   │   ├── CLAUDE.md
│   │   ├── scripts/
│   │   │   ├── check_deps.py
│   │   │   ├── estimate_tokens.py
│   │   │   ├── file_check.py
│   │   │   ├── log_tail.py
│   │   │   ├── ready.py
│   │   │   └── wrap.py
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
---
