# Design Spec: Query Routing Rule Redesign

**Date:** 2026-04-25
**Status:** Approved
**Author:** nitekeeper + Claude Sonnet 4.6

---

## Problem

The current Query Routing Rule places training knowledge at Step 1, requiring the agent to judge whether a question "clearly does not touch wiki content" before every response. This judgment is ambiguous — almost any question could theoretically be answered by wiki content — causing the agent to visibly deliberate about the routing rule itself instead of answering. The confusion surfaces as visible meta-reasoning shown to the user.

---

## Goal

A waterfall with zero ambiguous conditions. The agent always knows which step to execute next, with no judgment calls at the top of the chain.

---

## Design

### New Waterfall

**Step 1 — Wiki** *(always first, no conditions)*

1. Run `python scripts/log_tail.py` for last 5 log entries
2. If `scheduled-tasks/query-layer.md` exists → read and follow it; fall back to step 3 on empty/failure
3. Grep `wiki/pages` for topic slug; if no match, read `wiki/index.md`
4. Read candidate pages; answer with `[[wiki link]]` citations

If wiki answers the question → stop here.

**Step 2 — Web Search**

Runs when:
- (a) wiki returned nothing useful, OR
- (b) the question needs current or recent information

On result:
- If the result **directly answered the question** → silently save to `wiki/inbox/` and run INGEST op (no user prompt)
- If the result is **loosely related but did not answer** → skip ingest; use partial findings to inform Step 3

**Step 3 — Training Knowledge** *(fallback)*

Used when wiki and web both miss or are unavailable. Always append:

```
Confidence: N/10 — [one-line caveat if score ≤ 7 or topic is time-sensitive]
```

Example: `Confidence: 6/10 — based on training data; may not reflect changes after August 2025.`

The caveat line is omitted when score is 8–10 and the topic is not time-sensitive.

---

### Confidence Score Semantics

| Score | Meaning |
|---|---|
| 9–10 | High confidence, timeless or well-established fact |
| 7–8 | Reasonably confident; topic may have evolved |
| 5–6 | Moderate confidence; answer may be outdated or incomplete |
| 0–4 | Low confidence; treat as a starting point only |

---

### Edge Cases

| Condition | Behaviour |
|---|---|
| Blueprint-authoring mode (no `wiki/` at root) | Skip Step 1 entirely; go straight to Step 2 → Step 3 |
| Web search unavailable | Skip Step 2; fall directly to Step 3 with note: *"Web search unavailable."* |
| Web finds answer + wiki had partial info | Ingest web result; answer using both sources with citations from each |
| Wiki answered the question | "Worth filing as an analysis page?" prompt remains (covers synthesized analysis, not raw sources) |

---

## What Changes in CLAUDE.md

The `## Query Routing Rule` section is replaced in full. The new rule:

- Removes Step 1 (training knowledge) as the first check
- Makes wiki unconditionally first
- Makes web search the second step (no condition needed — if wiki missed, go to web)
- Demotes training knowledge to Step 3 with mandatory confidence scoring
- Adds auto-ingest trigger on successful web results
- Preserves all existing Step 2 sub-steps (log_tail, query-layer, grep, index)

No other sections of CLAUDE.md are affected.

---

## Out of Scope

- Changes to the INGEST op itself (`ops/ingest.md`)
- Changes to the query-layer skill (`scheduled-tasks/query-layer.md`)
- Changes to the footer format or compliance line
