# Changelog Monitor

Daily scheduled task. Read-only. Fetches every URL listed in `## Monitored Sources` below, computes content hashes, compares against the wiki's last-known `source_hash:` values, and reports findings via Slack DM. Never writes files. Never runs ingest automatically.

The monitor is the detector; `!! ingest` is the writer. This separation is intentional — it guarantees the user retains approval control over every wiki mutation.

---

## Monitored Sources

| # | Source Title | URL |
|---|---|---|
| 1 | SP-API Release Notes | https://developer-docs.amazon.com/sp-api/docs/sp-api-release-notes |
| 2 | SP-API Deprecations | https://developer-docs.amazon.com/sp-api/docs/sp-api-deprecations |
| 3 | SP-API Product Metadata Updates | https://developer-docs.amazon.com/sp-api/docs/sp-api-metadata-updates |
| 4 | Claude Code Changelog | https://code.claude.com/docs/en/changelog |

Add a source by appending a row here. Remove one by deleting its row. Keep the numbering stable for Slack readability, but gaps are fine — the task iterates the table, not a numeric range.

---

## Execution

1. **Read the wiki's stored hashes.** For each monitored source:
   - Look up the corresponding source page under `wiki/pages/sources/` (slug-matched — reuse the same slug derivation rules as `ops/ingest.md` Step 0).
   - If the source page exists, read its `source_hash:` frontmatter into memory.
   - If the source page does not exist, record the source as UNINGESTED and skip the hash lookup.
2. **Fetch all URLs in parallel via WebFetch.** Run every fetch concurrently — one per row in `## Monitored Sources`. The task is otherwise I/O-bound and should complete in under a minute regardless of row count.
3. **For each fetched source:** run the fetched body through the **Hash Canonicalization** pipeline defined in `@scheduled-tasks/ops/ingest.md` and take the first 8 hex characters of the resulting SHA-256. This is the SAME pipeline the ingest op uses at Step 0, which is what makes cross-path comparison (Clipper-ingested page's stored `source_hash:` vs monitor fetch) meaningful. The canonicalizer cannot fully defeat LLM-mediated WebFetch nondeterminism — see `troubleshooting.md`'s "Changelog monitor reports 🆕 for a page I know hasn't changed" entry for the caveat and manual-verification flow.
4. **Classify each source:**
   - **NO_CHANGE** — computed hash matches stored `source_hash:`.
   - **NEW_ENTRY** — computed hash differs from stored `source_hash:` (existing source page, content changed).
   - **UNINGESTED** — no source page exists for this URL in the wiki yet.
   - **FETCH_FAILED** — WebFetch error, timeout, empty response, or non-2xx status.
5. **Build the Slack message** using the format below.
6. **Send via `slack_send_message`** to Slack user `[YOUR_SLACK_USER_ID]` (self-DM).

---

## Rules

- **Read-only.** Never writes to `wiki/`, `raw/`, or `inbox/`. The only side effect is the Slack post.
- **Autonomous.** No approval prompts. The scheduler runs this task without a user present.
- **Fail soft.** One source failing (network error, parse error, etc.) must not break the others. A FETCH_FAILED entry in the Slack message is the correct behavior — do not abort the whole task.
- **No log entry.** The Slack message is the audit trail. Writing to `log.md` would violate the read-only contract and couple this task to the live-wiki invariants (`hot.md` refresh, etc.) it explicitly avoids.
- **No hash caching across runs.** Each run re-reads the source pages for stored hashes. This keeps the task stateless and self-correcting — if you manually edit a `source_hash:`, the next run picks it up.

---

## Slack Message Format

One compact message, one line per monitored source, emoji-prefixed by status:

```
📅 Changelog monitor — YYYY-MM-DD
✅ SP-API Release Notes — no change (stored: a3f8b2d1)
🆕 Claude Code Changelog — CHANGED (stored: c12ef09a → fetched: 7b4d82e1)
🆘 SP-API Deprecations — UNINGESTED (no wiki page yet)
❌ SP-API Product Metadata Updates — fetch failed (timeout)
🆕 items: run `!! ingest <URL>` to pull the update
🆘 items: run `!! ingest <URL>` to bootstrap
```

Emoji legend:

| Emoji | Status | Meaning |
|---|---|---|
| ✅ | NO_CHANGE | Stored hash matched fetched hash |
| 🆕 | NEW_ENTRY | Content changed — ready for manual re-ingest |
| 🆘 | UNINGESTED | No wiki page yet for this source |
| ❌ | FETCH_FAILED | Network/parse error; retry next run |

If every row in `## Monitored Sources` reports ✅, the message still posts — the "silent success" pattern (no message on no change) is rejected because it makes task-failure indistinguishable from task-success-with-nothing-to-report.

**Trailing hint lines.** Emit `🆕 items: run \`!! ingest <URL>\` to pull the update` only if the message contains at least one 🆕 row; emit `🆘 items: run \`!! ingest <URL>\` to bootstrap` only if it contains at least one 🆘 row. When the message contains only ✅ and/or ❌ rows, omit both trailing hint lines — there is no action for the user to take on those statuses.

---

## Invocation

The scheduler invokes this file via the 2-line prompt registered in the scheduled-tasks MCP:

```
Read changelog-monitor.md file located in scheduled-tasks folder.
Understand the instruction in that file and execute the instructions.
```

That prompt is the entire scheduler contract — do not expand it. Any logic added to the scheduler prompt drifts out of version control; keep the logic here in this file.

---

*Schema: v2.0 | Created: 2026-04-18*
