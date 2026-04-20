# Ingest Hook: SQLite

Installed by the `sqlite-query` skill. Runs after Step 11 of the core ingest op when `scheduled-tasks/ingest-hook.md` exists.

Keeps `wiki.db` in sync with the wiki after every ingest.

---

## Input

Available from the current ingest op's working memory:
- `slug` — the ingested page's slug
- `title` — page title
- `type` — page type (`source`, `concept`, `entity`, `analysis`)
- `summary` — one-line summary (from the index.md entry written in Step 10)
- `tags` — list of tags from frontmatter
- `created`, `updated` — dates from frontmatter
- `related` — list of related slugs from the page's `related:` frontmatter

Also runs for every concept/entity page created or updated in Steps 7–9 of the ingest op. Each such page triggers this hook with its own values.

---

## Steps

```python
import sqlite3, pathlib, os, json

WORKDIR = pathlib.Path(os.environ.get("WIKI_ROOT", ".")).resolve()
db = WORKDIR / "wiki" / "wiki.db"  # inside wiki/ folder; nolock+MEMORY avoids FUSE locking

# Values injected from ingest op working memory:
# slug, title, type_, summary, tags, created, updated, related

try:
    conn = sqlite3.connect(f"file:{db}?nolock=1", uri=True)
    conn.execute("PRAGMA journal_mode=MEMORY")
    conn.execute("PRAGMA synchronous=OFF")

    # Upsert the page
    conn.execute("""
        INSERT INTO pages (slug, title, type, summary, tags, created, updated)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET
            title   = excluded.title,
            type    = excluded.type,
            summary = excluded.summary,
            tags    = excluded.tags,
            updated = excluded.updated
    """, (slug, title, type_, summary, json.dumps(tags), created, updated))

    # Replace relations for this page
    conn.execute("DELETE FROM relations WHERE from_slug = ?", (slug,))
    for to_slug in related:
        conn.execute(
            "INSERT OR IGNORE INTO relations (from_slug, to_slug) VALUES (?, ?)",
            (slug, to_slug)
        )
        # Bidirectional — ensure reverse exists too
        conn.execute(
            "INSERT OR IGNORE INTO relations (from_slug, to_slug) VALUES (?, ?)",
            (to_slug, slug)
        )

    conn.commit()
    conn.close()
    print(f"[sqlite-query] synced: {slug} ({len(related)} relations)")

except Exception as e:
    print(f"[sqlite-query] hook error for {slug}: {e} — wiki.db may be out of sync. To repair: say '!! install sqlite-query' and choose yes to the backfill offer, or '!! uninstall sqlite-query' to revert to grep.")
```

---

## Notes

- Runs once per page touched in the ingest op — source page + every concept/entity page updated
- Errors are non-fatal: the ingest op continues, but wiki.db may drift from the markdown files. To repair: say `!! install sqlite-query` and choose yes to the backfill offer, or `!! uninstall sqlite-query` to revert to grep.
- Bidirectional relation insert uses `INSERT OR IGNORE` so duplicate pairs are silently skipped
