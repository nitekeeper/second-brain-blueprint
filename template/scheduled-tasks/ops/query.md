# Op: QUERY

Triggered automatically whenever the user asks any question. No explicit command needed.

## Waterfall

**Step 1 — Answer from training knowledge**
If highly confident in the answer, respond directly with citations where relevant. Stop here.

**Step 2 — Check the wiki**
If not highly confident, or if the question touches topics this wiki covers:
1. Read the last 5 entries of `wiki/log.md` for recent context (`grep -E "^## \[" wiki/log.md | tail -5`)
2. Derive a slug from the key topic in the question (lowercase-hyphenated). Run a grep pre-filter to find candidate pages without reading their content:
   ```bash
   grep -rl "topic-slug" wiki/pages --include="*.md"
   ```
   If the grep returns matches, those are your candidate pages — skip to step 4. If no matches, fall back to reading `wiki/index.md` (step 3).
3. Read `wiki/index.md` to find relevant pages (fallback only — use when grep returns no matches or the topic slug is ambiguous)
4. Read the candidate pages identified in step 2 or 3
5. Synthesize an answer with `[[wiki link]]` citations

**Step 3 — Search the internet**
If the wiki does not contain a good answer:
1. Search the web for the best available source
2. Summarize the key findings clearly
3. Ask the user: "I found a good source on this — want me to ingest it into the wiki?"
4. If yes, save the source to `wiki/inbox/` and run the full INGEST operation (ingest will move it to `raw/` after processing)

## Filing Answers

After any Step 2 or Step 3 answer, ask: "Worth filing this as an analysis page?"
If yes:
1. Read `@scheduled-tasks/ops/conventions.md` before writing the analysis page — this enforces slug, frontmatter, tag, and wiki-link conventions that analysis pages must follow
2. Show approval request and wait for confirmation — include the cost of re-reading `token-reference.md` itself (see the self-cost figure in its header) in the estimate
3. Write to `wiki/pages/analyses/`
4. Update `wiki/index.md` and append to `wiki/log.md` — **log entry must be ≤500 chars total**
5. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
6. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section) — only if any file's measured actual now exceeds its documented Chars value

Log format: `## [YYYY-MM-DD] query | [Question summary]` (≤500 chars)
