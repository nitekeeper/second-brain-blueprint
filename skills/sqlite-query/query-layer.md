# Query Layer: SQLite

Installed by the `sqlite-query` skill. Overrides the built-in grep query step in `ops/query.md`.

This file is read by the agent when `scheduled-tasks/query-layer.md` exists. It replaces Steps 2–3 of the core query op.

---

## Input

A topic slug (lowercase-hyphenated) derived from the user's question.

## Steps

1. **Query `wiki.db`** for pages related to the topic slug — both directions:
   ```python
   import sqlite3, pathlib, os, subprocess

   WORKDIR = pathlib.Path(os.environ.get("WIKI_ROOT", ".")).resolve()
   db = WORKDIR / "wiki.db"

   try:
       conn = sqlite3.connect(db)
       rows = conn.execute("""
           SELECT DISTINCT p.slug, p.title, p.summary
           FROM pages p
           WHERE p.slug = ?
              OR p.slug IN (
                  SELECT to_slug FROM relations WHERE from_slug = ?
                  UNION
                  SELECT from_slug FROM relations WHERE to_slug = ?
              )
       """, (slug, slug, slug)).fetchall()
       conn.close()

       if rows:
           # Resolve each slug to a concrete file path via `find`.
           # Do NOT use glob patterns (e.g. wiki/pages/**/<slug>.md) — they are
           # not expanded by Python's open() or the Read tool, and unmatched bash
           # globs return the literal pattern string rather than empty.
           candidate_paths = []
           pages_dir = str(WORKDIR / "wiki" / "pages")
           for row in rows:
               result = subprocess.run(
                   ["find", pages_dir, "-name", f"{row[0]}.md"],
                   capture_output=True, text=True
               )
               path = result.stdout.strip()
               if path:
                   candidate_paths.append(path)
       else:
           candidate_paths = []

   except Exception as e:
       print(f"[sqlite-query] DB error: {e} — falling back to grep")
       candidate_paths = None  # triggers fallback
   ```

2. **If `candidate_paths` is populated:** read those pages and synthesize the answer. Skip the grep fallback.

3. **If `candidate_paths` is empty (topic not in DB):** fall back to grep:
   ```bash
   grep -rl "topic-slug" wiki/pages --include="*.md"
   ```
   If grep also returns nothing, proceed to Step 3 of the core query op (read `index.md`).

4. **If fallback triggered by exception:** log the warning inline ("Note: SQLite query failed, using grep fallback") and proceed with grep as above.

## Output

A list of candidate page paths for the agent to read and synthesize from.
