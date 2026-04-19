# User Guide

---

## How the Agent Works

Every new chat session starts cold — the agent has no memory. It re-orients itself by reading two files at startup:

1. `CLAUDE.md` — its operating instructions (~5,500 tokens)
2. `wiki/hot.md` — a brief orientation snapshot (~80 tokens)

**Total cold-start cost: ~5,580 tokens.** This is intentionally lean. The agent defers reading the full index and log until it actually needs them for an operation.

If you saved a session summary with `!! wrap`, say `!! ready` at the start of your next session — the agent will load and read that summary before clearing it (~6,330 tokens total when the summary is full).

---

## Daily Workflow

### Adding Knowledge — Ingest

**The recommended path:**
1. Find an article or document you want to add
2. Clip it with Obsidian Web Clipper → saves to `wiki/inbox/` as clean markdown
3. Tell the agent: `!! ingest [filename]`

**What happens:**
- **Hash check first.** Before any work, the agent runs the source body through a deterministic canonicalizer (preamble-strip + whitespace / line-ending normalization) and computes an 8-char SHA-256 hash of the canonicalized content. It compares this against the stored `source_hash:` on the existing source page (if one exists). The same canonicalizer runs for both Clipper ingest and URL ingest, so the same underlying source produces the same hash either way. If the hashes match, the agent prints `No change since last ingest — skipped.`, deletes the inbox file, and stops. No log entry, no page edits, no cost. This is the rerun-proof guarantee.
- If the hash differs (or there's no existing source page), the agent proceeds:
  - Discusses 3–5 key takeaways with you
  - Shows you a to-do list of every page it will create or update
  - Shows a token cost estimate
  - Waits for your approval before writing anything
- After approval: creates or **regenerates** the source page (no in-place merge — a hash mismatch means the content actually changed, so the page is rewritten from scratch with a new `source_hash:`), updates affected concept/entity pages, then moves the source file from `wiki/inbox/` to `raw/<slug>-<YYYY-MM-DD-HHMMSS>.md`. Every successful ingest writes a new timestamped snapshot — `raw/` is a monotonically growing archive you can prune manually if desired.

> You can also say `!! ingest all` to process every file currently in `wiki/inbox/` at once. The batch flow also hash-checks each file up front and silently skips any that haven't changed, so re-running `!! ingest all` after an interruption is safe.

**Web Clipper or URL — your choice:**
You can also pass a URL directly: `!! ingest https://example.com/article`. The agent fetches the page, saves it to `wiki/inbox/` with URL provenance, and runs the same ingest flow. URL ingest is ~40–60% more expensive in tokens than a Web Clipper clip because the fetch pulls HTML boilerplate that Clipper strips beforehand. Either path works — pick whichever fits your session.

**Rerun safety (new in v2.0):** Same input → zero state change. You can re-run any ingest — manually, or as part of a scheduled task — without worrying about duplicates, drift, or log pollution. If you *want* to force a re-ingest (e.g. the page wording matters to you and the source hasn't changed but the previous page output was poor), delete the `source_hash:` line from the source page's frontmatter — the next ingest will treat it as a mismatch and regenerate. This is the documented force-reingest escape hatch.

**Provenance footnotes:** Source pages now cite their raw snapshot on every curated bullet in Key Takeaways — `[^1]: raw/<filename> — fetched YYYY-MM-DD`. When a page is regenerated from a newer snapshot, the footnotes point to the new filename; older snapshots stay in `raw/` as immutable archives.

---

### Asking Questions — Query

Just ask naturally. No special command needed. The agent follows a waterfall:

1. **High confidence** → answers directly from training knowledge
2. **Wiki topic** → checks `index.md`, reads relevant pages, answers with citations
3. **Not in wiki** → searches the web, summarizes findings, asks if you want to ingest the source

After a Step 2 or Step 3 answer, the agent will ask: *"Worth filing this as an analysis page?"* Say yes to preserve the answer in your wiki permanently.

---

### Planning & Drafting

When working through a complex idea or system change, the agent uses `drafts/` as a scrapbook — creating a working file to think through the problem across the conversation.

**What happens:**
- Agent creates a file in `drafts/` (e.g. `drafts/topic-name.md`) and iterates on it with you
- At startup, the agent checks `drafts/` and surfaces any in-progress files in its readiness announcement — so nothing gets lost between sessions
- When a draft is ready to become a source, the agent moves it to `wiki/inbox/` for ingestion

`drafts/` lives outside the Obsidian vault, so none of its contents appear in your wiki graph.

---

### Health Check — Lint

Run periodically to keep the wiki clean.

- `!! lint all` — full wiki health check
- `!! lint [page-name]` — check a specific page

**What lint checks:**
- Broken wiki links
- Orphan pages (no inbound links)
- Missing cross-references
- Stale or contradicted claims
- Data gaps worth filling

The agent always reports findings first and asks approval before fixing anything.

---

### Blueprint Audit — `!! audit`

Runs a strict, Senior-Software-Architect-style audit of the blueprint files themselves (the schema, the ops files, the guides). Unlike `!! lint` (which targets your wiki pages), audit targets only `blueprint/` — the distribution template and its docs.

- `!! audit all` — audit every file under `blueprint/` (~30,000–54,000 tokens)
- `!! audit [page-name]` — audit one matched file (~1,000–5,000 tokens)

**What audit checks:**
- Logic contradictions (rules that conflict, unreachable branches, missing edge cases in state machines)
- Security / safety footguns (approval bypasses, silent overwrites, data-loss paths)
- Performance / token waste (redundant reads, cold-start bloat, tiered-read violations)
- Blueprint-sync drift (the template and its downstream docs falling out of step)

Audits are **read-only by default** — no approval needed to run one. If the audit surfaces fixes you want applied, the agent will go through the normal approval flow before writing anything. Each finding comes with quoted evidence and a severity label (CRITICAL / WARNING / STYLE); if nothing is wrong the audit says so instead of padding the list.

---

### Updating Pages — `!! update`

You don't need a special command to trigger an update — just make a correction or add context mid-conversation. The agent detects it and runs the update op automatically.

You can also say it explicitly: `!! update [page-name]` or `"Update the Claude Code page with this new info: …"` The agent will show you a plan and wait for approval before changing anything.

---

### Session Memory — `!! wrap` and `!! ready`

**This is temporary, intentional memory — designed to bridge one session to the next. It is not a permanent log.**

At the end of a productive session, say `!! wrap`. The agent will ask if there's anything specific to include, then write a detailed summary to `memory.md` — covering what was worked on, key decisions, files changed, and open next steps. Each `!! wrap` overwrites the previous summary, so only one summary exists at a time. **If a prior wrapped summary — or a truncated summary you preserved via `!! ready` → `keep` — is still in `memory.md`, the agent will warn you before overwriting.** Reply `no` to cancel, then consume or clear the existing content first.

At the start of your next session, say `!! ready` as your first message. The agent will display the summary in full (verbatim) to bring you back up to speed, then immediately wipe `memory.md` and confirm it's clear. From that point, the session proceeds normally.

**Mid-session safeguard:** If you accidentally say `!! ready` in the middle of a session (not as the first message), the agent will refuse to wipe memory without explicit `!! ready confirm`. This prevents the older footgun where a casual "ready" wiped a saved summary.

**Truncation detection:** If `!! wrap` was interrupted before writing the completion marker, `!! ready` will display what's present, warn that the summary appears truncated, and ask you to choose one of three options — `clear` (wipe back to empty), `keep` (mark the partial summary as acknowledged so the warning stops firing), or `edit` (hand the file back untouched for manual repair). It will never silently wipe truncated content. In schema v1.14+, `clear` and `keep` each log their recovery choice to `log.md` and refresh `hot.md`, so the audit trail stays intact; `edit` leaves the file untouched and writes nothing.

If you start a session without saying `!! ready`, the summary stays in `memory.md` untouched until you explicitly ask for it. It won't be read automatically.

> **Note:** This is not a history log — it's a single-use memory bridge. Once consumed with `!! ready`, the summary is gone. If you need a permanent record of a decision, ingest it or file it as an analysis page.

---

## Footer Commands

Every agent response ends with the footer block: five command hints, a blank separator, and the 💡 Web Clipper tip (7 physical lines total):

```
📥 !! ingest: [URL | Page Name | All]
🧹 !! lint: [Page Name | All]
🔍 !! audit: [Page Name | All]
💾 !! wrap: [save session summary to memory]
🔄 !! ready: [load session summary at start of new session]

💡 Using Obsidian Web Clipper to save articles as markdown before ingesting is 40–60% cheaper in token usage than fetching directly from a URL.
```

These are hints showing what the commands accept. Just type them naturally — e.g. `!! ingest my-article.md`, `!! lint all`, `!! audit all`, `!! wrap`, or `!! ready`.

---

## Approval Rule

The agent will never edit or create files without showing you a plan first. Every write action comes with:

- A one-line summary of what it's about to do
- A token cost estimate (including the re-read of `token-reference.md` — see the self-cost figure in its header)
- A to-do list of every file affected
- "Shall I proceed?"

Read-only actions (answering questions, reading files) happen without approval.

**Documented exceptions (no separate approval prompt):** `!! wrap`, `!! ready`, and `!! audit`. Your invocation is implicit approval — `!! wrap` and `!! ready` have built-in safeguards (`!! wrap` warns before overwriting an existing summary, `!! ready` refuses to wipe memory mid-session without explicit `!! ready confirm`); `!! audit` is read-only by default, and any fix you request afterward goes through the normal approval flow.

---

## Suggestions Always Come with Pros and Cons

Whenever the agent recommends a change to your system, it will always show both sides — what you gain and what you risk — before asking for approval.

---

## Token Awareness

> **Note:** All token numbers below — and everywhere else in this system — are **estimates** derived from `chars ÷ 4`. Actual usage depends on the model's tokenizer, the exact file contents at read time, and runtime overhead from tool calls and the system prompt, so the real numbers will differ (sometimes noticeably). Use these figures for rough planning, not precise accounting.

The context window is 200,000 tokens per session. The agent tracks estimated costs in `scheduled-tasks/ops/token-reference.md` and recalibrates after every ingest.

**Typical session costs:**
| Action | Estimated tokens |
|---|---|
| Cold start | ~5,530 |
| Cold start with `!! ready` (full memory) | ~6,280 |
| Ingest a short article | ~3,000–5,000 |
| Ingest a long document | ~8,000–15,000 |
| Lint all | ~8,000–12,000 (scales with page count) |
| Simple query (wiki) | ~2,000–4,000 |
| Audit a single blueprint file | ~1,000–5,000 |
| Audit all (full blueprint) | ~30,000–54,000 |
| `!! wrap` (realistic) | ~2,800 |
| `!! ready` (realistic) | ~2,825 |

If a session gets long, the agent may auto-compact. All critical state is in files on disk — starting a new session costs only ~5,530 tokens to re-orient.

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

- **Clip first, ingest later** — build up a batch of articles in `wiki/inbox/`, then ingest them in one session
- **Draft before ingesting** — use `drafts/` to think through ideas with Claude before they're wiki-ready; drafts surface automatically at session startup
- **Ask questions freely** — the query waterfall handles routing automatically
- **Run lint monthly** — or after every 5–10 ingests to keep cross-references tight
- **New session anytime** — starting fresh costs only ~5,530 tokens; the wiki state is always preserved on disk
- **Bridge sessions with memory** — say `!! wrap` at the end of any productive session, then `!! ready` next time to pick up exactly where you left off. This is temporary, intentional memory — it clears after being read.
