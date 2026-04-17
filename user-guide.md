# User Guide

---

## How the Agent Works

Every new chat session starts cold — the agent has no memory. It re-orients itself by reading two files at startup:

1. `wiki/CLAUDE.md` — its operating instructions (~900 tokens)
2. `wiki/hot.md` — a brief orientation snapshot (~100 tokens)

**Total cold-start cost: ~1,000 tokens.** This is intentionally lean. The agent defers reading the full index and log until it actually needs them for an operation.

---

## Daily Workflow

### Adding Knowledge — Ingest

**The recommended path:**
1. Find an article or document you want to add
2. Clip it with Obsidian Web Clipper → saves to `Library/raw/` as clean markdown
3. Tell the agent: `ingest [filename]`

**What happens:**
- Agent discusses 3–5 key takeaways with you
- Shows you a to-do list of every page it will create or update
- Shows a token cost estimate
- Waits for your approval before writing anything
- After approval: creates/updates wiki pages, refreshes hot.md, recalibrates token estimates

> You can also say `ingest all` to process every uningested file in `Library/raw/` at once.

**Why Web Clipper instead of URL:**
Clipped markdown files are 40–60% cheaper to ingest than raw URLs — no HTML boilerplate, no navigation noise.

---

### Asking Questions — Query

Just ask naturally. No special command needed. The agent follows a waterfall:

1. **High confidence** → answers directly from training knowledge
2. **Wiki topic** → checks `index.md`, reads relevant pages, answers with citations
3. **Not in wiki** → searches the web, summarizes findings, asks if you want to ingest the source

After a Step 2 or Step 3 answer, the agent will ask: *"Worth filing this as an analysis page?"* Say yes to preserve the answer in your wiki permanently.

---

### Health Check — Lint

Run periodically to keep the wiki clean.

- `lint all` — full wiki health check
- `lint [page-name]` — check a specific page

**What lint checks:**
- Broken wiki links
- Orphan pages (no inbound links)
- Missing cross-references
- Stale or contradicted claims
- Data gaps worth filling

The agent always reports findings first and asks approval before fixing anything.

---

## Footer Commands

Every agent response ends with:

```
📥 ingest: [URL | Page Name | All]
🧹 lint: [Page Name | All]
```

These are hints showing what the commands accept. Just type them naturally — e.g. `ingest my-article.md` or `lint all`.

---

## Approval Rule

The agent will never edit or create files without showing you a plan first. Every write action comes with:

- A one-line summary of what it's about to do
- A token cost estimate
- A to-do list of every file affected
- "Shall I proceed?"

Read-only actions (answering questions, reading files) happen without approval.

---

## Suggestions Always Come with Pros and Cons

Whenever the agent recommends a change to your system, it will always show both sides — what you gain and what you risk — before asking for approval.

---

## Token Awareness

The context window is 200,000 tokens per session. The agent tracks estimated costs in `scheduled-tasks/ops/token-reference.md` and recalibrates after every ingest.

**Typical session costs:**
| Action | Estimated tokens |
|---|---|
| Cold start | ~1,000 |
| Ingest a short article | ~3,000–5,000 |
| Ingest a long document | ~8,000–15,000 |
| Lint all (23 pages) | ~8,000–12,000 |
| Simple query (wiki) | ~2,000–4,000 |

If a session gets long, the agent may auto-compact. All critical state is in files on disk — starting a new session costs only ~1,000 tokens to re-orient.

---

## Wiki Structure

| Folder | Contents |
|---|---|
| `wiki/pages/concepts/` | Ideas, frameworks, methodologies |
| `wiki/pages/entities/` | People, tools, organizations, products |
| `wiki/pages/sources/` | One summary page per ingested source |
| `wiki/pages/analyses/` | Filed answers to queries worth preserving |

---

## Tips

- **Clip first, ingest later** — build up a batch of articles in `raw/`, then ingest them in one session
- **Ask questions freely** — the query waterfall handles routing automatically
- **Run lint monthly** — or after every 5–10 ingests to keep cross-references tight
- **New session anytime** — starting fresh costs only ~1,000 tokens; the wiki state is always preserved on disk
