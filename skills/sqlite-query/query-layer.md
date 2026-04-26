# Query Layer: SQLite

Installed by the `sqlite-query` skill. Overrides the built-in grep query step in the Query Routing Rule embedded in `CLAUDE.md`.

This file is read by the agent when `scheduled-tasks/query-layer.md` exists. It replaces sub-steps 2–3 of Step 1 (wiki) in the Query Routing Rule waterfall.

---

## Input

A topic slug (lowercase-hyphenated) derived from the user's question.

## Steps

1. **Query `wiki.db`** for pages related to the topic slug — both directions:
   ```python
   import sqlite3, pathlib, os

   WORKDIR = pathlib.Path(os.environ.get("WIKI_ROOT", ".")).resolve()
   db = WORKDIR / "wiki" / "wiki.db"  # inside wiki/ folder; nolock+MEMORY avoids FUSE locking

   try:
       conn = sqlite3.connect(f"file:{db}?nolock=1", uri=True)
       conn.execute("PRAGMA journal_mode=MEMORY")
       conn.execute("PRAGMA synchronous=OFF")
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
           # Resolve each slug to a concrete file path using pathlib.rglob() —
           # cross-platform (works on Windows, macOS, and Linux).
           # Do NOT pass glob patterns to Python's open() or the Read tool —
           # they do not expand globs; unmatched bash globs return the literal
           # pattern string rather than empty.
           candidate_paths = []
           pages_dir = WORKDIR / "wiki" / "pages"
           for row in rows:
               matches = list(pages_dir.rglob(f"{row[0]}.md"))
               if matches:
                   candidate_paths.append(str(matches[0]))
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
   If grep also returns nothing, read `wiki/index.md` directly and continue from sub-step 4 of the query waterfall (read candidate pages; answer with [[wiki link]] citations).

4. **If fallback triggered by exception:** log the warning inline ("Note: SQLite query failed, using grep fallback") and proceed with grep as above.

## Output

A list of candidate page paths for the agent to read and synthesize from.
