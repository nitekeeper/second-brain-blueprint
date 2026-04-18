# Op: QUERY

Triggered automatically whenever the user asks any question. No explicit command needed.

## Waterfall

**Step 1 — Answer from training knowledge**
If highly confident in the answer, respond directly with citations where relevant. Stop here.

**Step 2 — Check the wiki**
If not highly confident, or if the question touches topics this wiki covers:
1. Read `wiki/index.md` to find relevant pages
2. Read those specific pages
3. Synthesize an answer with `[[wiki link]]` citations

**Step 3 — Search the internet**
If the wiki does not contain a good answer:
1. Search the web for the best available source
2. Summarize the key findings clearly
3. Ask the user: "I found a good source on this — want me to ingest it into the wiki?"
4. If yes, save the source to `wiki/inbox/` and run the full INGEST operation (ingest will move it to `raw/` after processing)

## Filing Answers

After any Step 2 or Step 3 answer, ask: "Worth filing this as an analysis page?"
If yes:
1. Show approval request and wait for confirmation
2. Write to `wiki/pages/analyses/`
3. Update `wiki/index.md` and append to `wiki/log.md`
4. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`

Log format: `## [YYYY-MM-DD] query | [Question summary]`
