# User Guide

---

## How the Agent Works

Every new chat session starts cold — the agent has no memory. It re-orients itself by reading two files at startup:

1. `CLAUDE.md` — its operating instructions (~2,000 tokens)
2. `wiki/hot.md` — a brief orientation snapshot (~80 tokens)

**Total cold-start cost: ~2,100 tokens.** This is intentionally lean. The agent defers reading the full index and log until it actually needs them for an operation.

If you saved a session snapshot with `!! wrap`, say `!! ready` at the start of your next session — the agent will load and restore it before clearing it (~3,500 tokens total).

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

1. **Wiki** → checks recent log, reads relevant pages via `index.md`, answers with `[[wiki link]]` citations
2. **Web search** → when wiki has nothing useful, or question needs current information; successful results auto-save to `wiki/inbox/`
3. **Training knowledge** *(fallback)* → when wiki and web both miss; answer includes `Confidence: N/10` staleness caveat

After a Step 1 (wiki synthesis) or Step 2 (web) answer, the agent will ask: *"Worth filing this as an analysis page?"* Say yes to preserve the answer in your wiki permanently.

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

### Blueprint Audit *(developer / maintainer tool)*

> **Regular wiki users do not need this command.** `!! audit` is a blueprint-maintainer tool — it audits the blueprint files themselves (schema, ops files, guides), not your wiki pages. It is not shown in the response footer. Use `!! lint` for wiki health checks.

If you are maintaining or distributing the blueprint and need to check its internal consistency:

- `!! audit all` — audits every blueprint file; generates a structured report saved to `audits/`
- `!! audit [file-name]` — audits one matched file; same report format, narrower scope

**What it checks:** logic contradictions, approval-path leaks, cross-file drift, stale references, token-estimate accuracy.

Each run produces a professional audit report (`audits/AUD-YYYY-MM-DD-NNN.md`) with: executive summary, previous-findings verification, per-finding detail (condition, criteria, cause, consequence, recommendation), and an action-item to-do checklist. Findings from prior reports are carried forward until resolved — the next run verifies them before adding new ones.

---

### Installing Skills — `!! install`

Skills extend the core system without changing the blueprint itself. Available skills:

- `!! install sqlite-query` — installs the SQLite query layer. Replaces the built-in grep lookup with a local `wiki.db` index. Recommended when your wiki grows beyond ~500 pages. If your wiki already has pages, the agent will offer to backfill `wiki.db` from them.
- `!! uninstall sqlite-query` — removes the skill and reverts to the grep layer.
- `!! install claude-code-enhanced` — (Claude Code CLI only) registers `/wrap`, `/ready`, and `/migrate` as native slash commands. Works alongside the `!! command` syntax — both remain available.
- `!! uninstall claude-code-enhanced` — removes the slash commands.

**Fallback:** if SQLite is unavailable or a query fails at runtime, the system falls back to grep automatically.

**Query layer precedence:** Basic (grep) → SQLite (if installed) → future skills. Only one query layer is active at a time.

---

### Cross-Platform Scripts

The agent uses a set of Python scripts under `scripts/` for file operations that previously required bash. These scripts work identically on Windows, macOS, and Linux.

You do not need to call them directly — the agent uses them automatically. If a script fails, the agent will show the error and suggest a fix.

Python 3.8+ is required. If Python is not installed, the agent will show OS-specific installation instructions the first time a script is needed.

---

### Updating Pages — `!! update`

You don't need a special command to trigger an update — just make a correction or add context mid-conversation. The agent detects it and runs the update op automatically.

You can also say it explicitly: `!! update [page-name]` or `"Update the Claude Code page with this new info: …"` The agent will show you a plan and wait for approval before changing anything.

---

### Session Memory — `!! wrap` and `!! ready`

**This is temporary, intentional memory — designed to bridge one session to the next. It is not a permanent log.**

At the end of a productive session, say `!! wrap`. The agent will ask if there's anything specific to include, then write a compact context snapshot to `memory.md` capturing the task in flight, exact stopping point, next action, locked decisions, and active files. The format is machine-oriented and intentionally terse — the wiki stores permanent knowledge; the snapshot only bridges the current task thread to the next session.

> **`!! wrap` saves a file — it does not free the current session's context.** To actually get a clean slate, **close this conversation and open a new one**, then say `!! ready` as your first message. That new session starts at ~2,100 tokens regardless of how heavy the previous one was. Running `!! ready` in the same conversation (or after `/compact`) does not reset the context window.

Each `!! wrap` overwrites the previous snapshot, so only one snapshot exists at a time. **If a prior wrapped snapshot — or a truncated snapshot you preserved via `!! ready` → `keep` — is still in `memory.md`, the agent will warn you before overwriting.** Reply `no` to cancel, then consume or clear the existing content first.

At the start of your next session, say `!! ready` as your first message. The agent will silently parse the snapshot to restore context, then announce: "Resuming: [task]. Next: [next action]. Ready to continue." It will then wipe `memory.md` and confirm it's clear. From that point, the session proceeds normally.

**Mid-session safeguard:** If you accidentally say `!! ready` in the middle of a session (not as the first message), the agent will refuse to wipe memory without explicit `!! ready confirm`. This prevents the older footgun where a casual "ready" wiped a saved snapshot.

**Truncation detection:** If `!! wrap` was interrupted before writing the completion marker, `!! ready` will display what's present, warn that the snapshot appears truncated, and ask you to choose one of three options — `clear` (wipe back to empty), `keep` (mark the partial snapshot as acknowledged so the warning stops firing), or `edit` (hand the file back untouched for manual repair). It will never silently wipe truncated content. In schema v1.14+, `clear` and `keep` each log their recovery choice to `log.md` and refresh `hot.md`, so the audit trail stays intact; `edit` leaves the file untouched and writes nothing.

If you start a session without saying `!! ready`, the snapshot stays in `memory.md` untouched until you explicitly ask for it. It won't be read automatically.

> **Note:** This is not a history log — it's a single-use memory bridge. Once consumed with `!! ready`, the snapshot is gone. If you need a permanent record of a decision, ingest it or file it as an analysis page.

### Session Hygiene

After `!! ingest`, `!! lint`, or `!! audit` completes, the agent will show a session advisory recommending you start a new session before doing more work. This is because each turn in a long session re-reads the entire conversation history, increasing cost non-linearly.

**Recommended workflow:**
- One ingest (or batch ingest) per session
- One lint pass per session
- `!! audit all` always in its own session

To dismiss the advisory and continue anyway, say `!! proceed`. The agent will resume normally.

---

## Footer Commands

Every agent response ends with the footer block: four command hints, a blank separator, the 💡 Web Clipper tip, and a compliance line (7 physical lines total):

```
📥 !! ingest: [URL | Page Name | All]
🧹 !! lint: [Page Name | All]
💾 !! wrap: [save session snapshot to memory]
🔄 !! ready: [load session snapshot at start of new session]

💡 Using Obsidian Web Clipper to save articles as markdown before ingesting is 40–60% cheaper in token usage than fetching directly from a URL.
📋 Waterfall: [step taken] | Ops: [file read or N/A]
```

The first four lines are command hints — just type them naturally, e.g. `!! ingest my-article.md`, `!! lint all`, `!! wrap`, or `!! ready`.

The `📋 Waterfall:` line is a compliance indicator filled in by the agent on every response — it shows which query waterfall step was taken and which ops file was read. If you see `Step 3` (training knowledge) on a question that should be in your wiki, or a missing ops file read before an operation, the agent skipped a mandatory step and you can call it out immediately.

---

## Approval Rule

The agent will never edit or create files without showing you a plan first. Every write action comes with:

- A one-line summary of what it's about to do
- A token cost estimate (from `scripts/estimate_tokens.py`)
- A to-do list of every file affected
- "Shall I proceed?"

Read-only actions (answering questions, reading files) happen without approval.

**Documented exceptions (no separate approval prompt):** `!! wrap`, `!! ready`, and `!! audit`. Your invocation is implicit approval — `!! wrap` and `!! ready` have built-in safeguards (`!! wrap` warns before overwriting an existing snapshot, `!! ready` refuses to wipe memory mid-session without explicit `!! ready confirm`); `!! audit` is read-only by default, and any fix you request afterward goes through the normal approval flow.

---

## Suggestions Always Come with Pros and Cons

Whenever the agent recommends a change to your system, it will always show both sides — what you gain and what you risk — before asking for approval.

---

## Token Awareness

> **Note:** All token numbers below — and everywhere else in this system — are **estimates** derived from `chars ÷ 4`. Actual usage depends on the model's tokenizer, the exact file contents at read time, and runtime overhead from tool calls and the system prompt, so the real numbers will differ (sometimes noticeably). Use these figures for rough planning, not precise accounting.

The context window is 200,000 tokens per session. Token estimates are computed dynamically via `scripts/estimate_tokens.py` (file size ÷ 4).

**Typical session costs:**
| Action | Estimated tokens |
|---|---|
| Cold start | ~2,100 |
| Cold start with `!! ready` (full memory) | ~3,500 |
| Ingest a short article | ~3,000–5,000 |
| Ingest a long document | ~8,000–15,000 |
| Lint all | ~8,000–12,000 (scales with page count) |
| Simple query (wiki) | ~2,000–4,000 |
| Audit a single blueprint file | ~1,000–5,000 |
| Audit all (full blueprint) | ~35,000–45,000 |
| `!! wrap` (realistic) | ~1,500–2,500 |

If a session gets long, the agent may auto-compact. All critical state is in files on disk — starting a new session costs only ~2,100 tokens to re-orient.

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
- **New session anytime** — starting fresh costs only ~2,100 tokens; the wiki state is always preserved on disk
- **Bridge sessions with memory** — say `!! wrap` at the end of any productive session, then `!! ready` next time to pick up exactly where you left off. This is temporary, intentional memory — it clears after being read.
