# Conventions

Read this file before creating or editing any wiki pages.

## File Naming (Slugs)
Lowercase, hyphenated: `cognitive-load.md`, `elon-musk.md`, `claude-code.md`

## Dates
Always ISO 8601: `YYYY-MM-DD`

## Wiki Links
Use `[[Page Title]]` (Obsidian-style) for cross-references within pages.
Piped links: `[[Page Title|display text]]`

## Tags
No `#` prefix in YAML frontmatter — Obsidian treats `#tag` as invalid there.
✅ Correct: `tags: [concept, llm, tool]`
❌ Wrong: `tags: [#concept, #llm, #tool]`
The `#` prefix is only valid for inline body text tags.

## Page Frontmatter
```yaml
---
title: "Page Title"
type: concept | entity | source | analysis
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [source-slug-1, source-slug-2]
related: [page-slug-1, page-slug-2]
---
```

The `related:` field lists slugs of directly connected pages — concepts, entities, analyses, or sources that share a meaningful relationship with this page. Use lowercase-hyphenated slugs (same as filenames, without `.md`). This field is the relationship layer: the agent queries it with grep instead of reading page content, keeping cross-page lookups fast and token-cheap as the wiki grows.

**Grep query pattern** — find all pages that reference a given slug:
```bash
grep -rl "slug-name" wiki/pages --include="*.md"
```
This scans frontmatter and body in one pass. For frontmatter-only precision (faster on large wikis):
```bash
grep -rl "^related:.*slug-name" wiki/pages --include="*.md"
```

Source pages also include:
- `original_file:` pointing to the raw file (timestamped: `raw/<slug>-<YYYY-MM-DD-HHMMSS>.md`)
- `source_hash: <8-char-hex>` — 8-char SHA-256 hex prefix of the **canonicalized** source body (see `@scheduled-tasks/ops/ingest.md` §Hash Canonicalization for the normalizer spec: preamble-strip-if-present + line-ending normalization + whitespace collapse + trim). Required. This is the dedupe primitive used by Step 0 of the ingest op — the canonicalizer ensures Clipper-ingested and URL-fetched versions of the same source converge on the same hash. Deleting or blanking this line will force a full regeneration on the next ingest — that is the documented "force re-ingest" escape hatch.

Analysis pages also include: `query:` with the original question.

## Page Body
- Use `[[Wiki Links]]` for all cross-references
- Aim for dense, useful content — no padding
- End every page with a `## Related Pages` section listing key links

## Provenance Footnotes (source pages)

Every curated bullet in a source page's `## Key Takeaways` section MUST end with a footnote reference that cites the raw snapshot it came from. This lets a reader answer "where did this fact come from, and when was it fetched?" without leaving the page.

Format:

```markdown
- Agentic coding: the agent plans, edits across files, runs commands, and verifies results[^1]
- Supports hooks before/after actions for deterministic enforcement[^1]

[^1]: raw/claude-code-overview-2026-04-18-091532.md — fetched 2026-04-18
```

Rules:
- One footnote per raw snapshot, reused across bullets that derive from the same snapshot.
- When a source page is regenerated from a newer raw snapshot (hash-mismatch regeneration), the footnotes point to the NEW raw filename. The old raw file stays in `raw/` as an immutable archive but is no longer cited by the source page.
- Format the date as ISO 8601 (YYYY-MM-DD), not locale-dependent formats.

## Bulk File Edits
Always use Python — never `sed -i`. The `sed -i` command leaves `XX*` temp files that Obsidian cannot open.

**Important: set an absolute root before globbing.** Relative paths like `"wiki/pages"` silently match zero files if cwd is not the working folder root, and the agent will think the edit succeeded.

```python
import os, re, pathlib

# Anchor to the working folder — pass in explicitly, don't rely on cwd
ROOT = pathlib.Path(os.environ.get("WIKI_ROOT", ".")).resolve()
pages = ROOT / "wiki" / "pages"
assert pages.is_dir(), f"pages dir not found at {pages}"

edited = 0
for f in pages.rglob("*.md"):
    try:
        text = f.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        print(f"skip {f}: {e}")
        continue
    new = re.sub(r"pattern", "replacement", text)
    if new != text:
        f.write_text(new, encoding="utf-8")
        edited += 1
print(f"edited {edited} files under {pages}")
```

The agent should always print the edit count and the resolved root path before considering the bulk edit complete — a count of 0 is a red flag, not a success.

## Query Layer Hook Contract

A file at `scheduled-tasks/query-layer.md` overrides the built-in grep query step. Skills that provide a query layer must follow this contract:

- **Input:** a topic slug (lowercase-hyphenated) derived from the user's question, available in working memory as `slug`
- **Output:** a list of candidate page file paths for the agent to read, or `None` / empty list to trigger fallback to grep. Paths must be fully resolved (e.g. `wiki/pages/concepts/slug.md`) — do NOT return glob patterns such as `wiki/pages/**/slug.md`. Python's `open()` and the Read tool do not expand globs; unmatched bash globs return the literal pattern string rather than empty. Use `find wiki/pages -name "<slug>.md"` (via `subprocess.run`) to resolve slugs to concrete paths.
- **Fallback:** if the query layer fails or returns empty, the agent falls back to grep automatically — query layers must never hard-fail the op

## Ingest Hook Contract

A file at `scheduled-tasks/ingest-hook.md` runs after Step 11 of the ingest op. Skills that provide an ingest hook must follow this contract:

- **Input:** per-page values from working memory — `slug`, `title`, `type`, `summary`, `tags`, `created`, `updated`, `related` (list of slugs)
- **Runs:** once per page touched in the ingest (source page + every concept/entity page created or updated)
- **Errors:** must be non-fatal — log a warning and let the ingest op continue
- **Side effects:** hook is responsible for keeping any external index (e.g. `wiki.db`) in sync with the markdown files

## Immutable Files
Never modify anything in `raw/` — these are the original source documents.

`raw/` files use timestamped naming: `<slug>-<YYYY-MM-DD-HHMMSS>.md`. Every successful ingest writes a new timestamped snapshot — filenames are physically unique at second precision, so the directory grows monotonically. The user is free to prune `raw/` manually (e.g. keep only the most recent snapshot per slug) — the agent must not prune autonomously. A missing raw file only breaks the footnote trail for that specific snapshot; it does not affect the source page's `source_hash:` dedupe behavior.

## Filing Answers (Query Step 2 / Step 3)

After any Step 2 (wiki) or Step 3 (web) answer, ask: "Worth filing this as an analysis page?"

If yes:
1. Read this file (`@scheduled-tasks/ops/conventions.md`) — already loaded, no extra read needed
2. Show approval request with token estimate (`python scripts/estimate_tokens.py wiki/pages/analyses/<slug>.md` after drafting) and file list
3. Wait for confirmation
4. Write to `wiki/pages/analyses/<slug>.md` following all conventions above
5. Update `wiki/index.md` and append to `wiki/log.md` (≤500 chars):
   `## [YYYY-MM-DD] query | [Question summary]`
6. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`

Log format: `## [YYYY-MM-DD] query | [Question summary]` (≤500 chars)
