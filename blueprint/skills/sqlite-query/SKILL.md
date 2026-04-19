# Skill: sqlite-query

Replaces the built-in grep-based query layer with a SQLite index (`wiki.db`) for faster, more powerful relationship queries. Recommended for wikis with 500+ pages.

---

## What This Skill Installs

| File | Destination |
|---|---|
| `query-layer.md` | `scheduled-tasks/query-layer.md` |
| `ingest-hook.md` | `scheduled-tasks/ingest-hook.md` |

Plus creates `wiki.db` at the working folder root.

---

## Install Command

`!! install sqlite-query`

### Steps

1. **Compatibility check.** Run:
   ```python
   import sqlite3
   print("ok")
   ```
   If this fails, inform the user: "Python sqlite3 is unavailable on this system — falling back to the built-in grep layer. No changes made." Stop here.

2. **Show approval request:**
   - Summary: "Install sqlite-query skill — create wiki.db, copy query-layer.md and ingest-hook.md to scheduled-tasks/"
   - Files affected: `wiki.db` (create), `scheduled-tasks/query-layer.md` (copy), `scheduled-tasks/ingest-hook.md` (copy)
   - Token estimate: ~200 tokens
   - "Shall I proceed?"

3. **Create `wiki.db`** using Python:
   ```python
   import sqlite3, pathlib, os

   WORKDIR = pathlib.Path(os.environ.get("WIKI_ROOT", ".")).resolve()
   conn = sqlite3.connect(WORKDIR / "wiki.db")
   conn.executescript("""
       CREATE TABLE IF NOT EXISTS pages (
           slug     TEXT PRIMARY KEY,
           title    TEXT NOT NULL,
           type     TEXT NOT NULL CHECK(type IN ('concept','entity','source','analysis')),
           summary  TEXT,
           tags     TEXT DEFAULT '[]',
           created  TEXT,
           updated  TEXT
       );
       CREATE TABLE IF NOT EXISTS relations (
           from_slug TEXT NOT NULL,
           to_slug   TEXT NOT NULL,
           PRIMARY KEY (from_slug, to_slug)
       );
       CREATE INDEX IF NOT EXISTS idx_relations_from ON relations(from_slug);
       CREATE INDEX IF NOT EXISTS idx_relations_to   ON relations(to_slug);
       CREATE INDEX IF NOT EXISTS idx_pages_type     ON pages(type);
       CREATE INDEX IF NOT EXISTS idx_pages_updated  ON pages(updated);
   """)
   conn.commit()
   conn.close()
   print("wiki.db created")
   ```

4. **Copy skill files** into `scheduled-tasks/`:
   - `blueprint/skills/sqlite-query/query-layer.md` → `scheduled-tasks/query-layer.md`
   - `blueprint/skills/sqlite-query/ingest-hook.md` → `scheduled-tasks/ingest-hook.md`

5. **Backfill check.** If `wiki/pages/` contains any pages:
   - Ask: "Your wiki has existing pages. Backfill wiki.db from them now? (yes/no)"
   - If yes: read every page in `wiki/pages/` and for each, extract `slug`, `title`, `type`, `summary`, `tags`, `created`, `updated` from frontmatter, and `related:` slugs for relations. Insert into `wiki.db` using the ingest-hook pattern. Report count on completion.
   - If no: skip. The DB will populate naturally as pages are ingested or updated going forward.

6. **Confirm:** "sqlite-query skill installed. Query and ingest ops will now use wiki.db."

---

## Fallback Behaviour

If `wiki.db` becomes corrupted or a query fails at runtime, `query-layer.md` catches the exception and falls back to the built-in grep layer transparently, logging a warning.

**DB desync recovery.** If the ingest hook logs a hook error (e.g. `[sqlite-query] hook error for <slug>: …`), `wiki.db` may have drifted from the markdown files. To repair: say `!! install sqlite-query` — the install flow detects the existing DB, skips creation, and re-offers the backfill step. Choose yes to re-sync all pages. Alternatively, say `!! uninstall sqlite-query` to remove the skill and revert to the built-in grep layer.

---

## Uninstall

Tell the agent: `!! uninstall sqlite-query`

Steps:
1. Delete `scheduled-tasks/query-layer.md`
2. Delete `scheduled-tasks/ingest-hook.md`
3. Ask: "Delete wiki.db too? (yes/no)" — default no, since it may be useful to keep as a cache
4. Confirm: "sqlite-query skill removed. Query and ingest ops have reverted to the built-in grep layer."

---

## Offered During Setup

`setup-guide.md` Step 4.5 offers this skill during initial setup. Choosing yes runs the install flow above (skipping the backfill step since no pages exist yet).
