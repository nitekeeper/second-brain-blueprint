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
---
```

Source pages also include: `original_file:` pointing to the raw file.
Analysis pages also include: `query:` with the original question.

## Page Body
- Use `[[Wiki Links]]` for all cross-references
- Aim for dense, useful content — no padding
- End every page with a `## Related Pages` section listing key links

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

## Immutable Files
Never modify anything in `raw/` — these are the original source documents.
