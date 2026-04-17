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

```python
import re, pathlib
for f in pathlib.Path("wiki/pages").rglob("*.md"):
    text = f.read_text()
    text = re.sub(r"pattern", "replacement", text)
    f.write_text(text)
```

## Immutable Files
Never modify anything in `raw/` — these are the original source documents.
