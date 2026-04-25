# Query Routing Rule Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Query Routing Rule in `template/CLAUDE.md` with a wiki-first waterfall that eliminates agent meta-reasoning confusion, adds auto-ingest on successful web results, and demotes training knowledge to a confidence-scored fallback.

**Architecture:** Single-section edit to `template/CLAUDE.md`. The `## Query Routing Rule` block (lines 27–45) is replaced in full. No other files change.

**Tech Stack:** Markdown, git

---

### Task 1: Replace the Query Routing Rule section

**Files:**
- Modify: `template/CLAUDE.md:27-45`

- [ ] **Step 1: Verify current content before editing**

Read `template/CLAUDE.md` lines 25–47 and confirm the section starts with:
```
**CRITICAL: Follow this waterfall for every user question — no exception for perceived simplicity or confidence level.**

**Step 1 — Training knowledge**
```
and ends before `---` / `## Ops Routing`.

- [ ] **Step 2: Replace the Query Routing Rule block**

In `template/CLAUDE.md`, replace everything from line 27 (`**CRITICAL: Follow this waterfall...`) through line 45 (`Search → summarize → ask to ingest...`) with the following:

```markdown
**CRITICAL: Follow this waterfall for every user question — no exception for perceived simplicity or confidence level.**

**Step 1 — Wiki** *(always first, no conditions)*
1. Run `python scripts/log_tail.py` for last 5 log entries
2. If `scheduled-tasks/query-layer.md` exists → read and follow it; fall back to step 3 on empty/failure
3. Grep `wiki/pages` for topic slug; if no match, read `wiki/index.md`
4. Read candidate pages; answer with `[[wiki link]]` citations
5. Ask: "Worth filing as an analysis page?" — if yes, read `@scheduled-tasks/ops/conventions.md` first

If wiki answers the question → stop here.

**Step 2 — Web Search**
Runs when: (a) wiki returned nothing useful, OR (b) question needs current or recent information.
- Search and summarize
- If the result **directly answered the question** → silently save to `wiki/inbox/` and run INGEST op
- If the result is **loosely related but did not answer** → skip ingest; use partial findings to inform Step 3

**Step 3 — Training Knowledge** *(fallback only)*
Used when wiki and web both miss or are unavailable. Always append:
`Confidence: N/10 — [one-line caveat if score ≤ 7 or topic is time-sensitive]`

Omit the caveat when score is 8–10 and the topic is not time-sensitive.

**Edge cases:**
- Blueprint-authoring mode (no `wiki/` at root): Skip Step 1; go straight to Step 2 → Step 3
- Web search unavailable: Skip Step 2; fall to Step 3 with note: *"Web search unavailable."*
```

- [ ] **Step 3: Verify the edit**

Read `template/CLAUDE.md` lines 25–55 and confirm:
- `Step 1 — Wiki` appears before `Step 2 — Web Search`
- `Step 3 — Training Knowledge` is the last step
- `Confidence: N/10` line is present
- The old `Step 1 — Training knowledge` block and its skip conditions are gone
- `## Ops Routing` section immediately follows (no content was accidentally deleted)

- [ ] **Step 4: Commit**

```bash
git add template/CLAUDE.md
git commit -m "feat: redesign Query Routing Rule — wiki-first waterfall with auto-ingest and confidence scoring"
```

Expected output: `1 file changed`
