# Op: MIGRATE

Triggered when the user says `!! migrate`.

Upgrades an existing working folder to v2.3.

---

## Detection (runs at startup)

During startup step 7, compare `Schema:` in `hot.md` against the current schema
version (`v2.3`). If `Schema:` is below `v2.3`, announce once:

> "Blueprint v2.3 is available — run `!! migrate` to update your working folder."

Announce at most once per session (do not repeat on every response).

---

## Steps

1. **Read `Schema:` from `hot.md`** to determine migration path:
   - `v2.2` → follow the **v2.2 → v2.3** path below
   - `v2.1` or below → follow the **v2.1 → v2.3** path below
   - `v2.3` → announce "Already on v2.3. Nothing to migrate." and stop.

---

## v2.2 → v2.3 Path

### Pre-flight

Run `python scripts/check_deps.py --python`
- If exit non-zero: stop. Show the printed instructions. Do not continue.

### Approval request

Show the user:

```
Migration: v2.2 → v2.3

Files UPDATED:
  CLAUDE.md  (Query Routing Rule section replaced — behavior change, no size change)
  scheduled-tasks/ops/conventions.md  (Filing Answers step labels updated to v2.3 numbering)
  scheduled-tasks/ops/blueprint-sync.md  (two new v2.3 cascade rows added)
  scheduled-tasks/refresh-hot.md  (Step 3 updated to detect claude-code-enhanced skill)
  wiki/hot.md  (Schema: v2.2 → v2.3)

Files UNTOUCHED:
  wiki/  (all pages, index, log preserved)
  memory.md, raw/, drafts/
  scheduled-tasks/ops/  (all other ops files preserved)
  scripts/  (all scripts preserved)
  sqlite-query skill (if installed)

Shall I proceed?
```

### On approval, execute in order

a. Create `backups/` directory if absent.
b. Copy `CLAUDE.md` → `backups/CLAUDE.md-v2.2-<YYYY-MM-DD>.bak`
b2. Copy `scheduled-tasks/ops/conventions.md` → `backups/conventions.md-v2.2-<YYYY-MM-DD>.bak`
b3. Copy `scheduled-tasks/ops/blueprint-sync.md` → `backups/blueprint-sync.md-v2.2-<YYYY-MM-DD>.bak`
c. In `CLAUDE.md`, replace the entire `## Query Routing Rule` section (from the
   `## Query Routing Rule` heading through and including its closing `---` separator,
   up to but not including `## Ops Routing`) with the following exact text:

```
## Query Routing Rule

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
- If the result **directly answered the question** → silently save to `wiki/inbox/` and read `@scheduled-tasks/ops/ingest.md` to ingest it
- If the result **directly answered the question AND Step 1 returned partial wiki content** → ingest the web result; answer citing both the wiki pages and the web result
- If the result is **loosely related but did not answer** → skip ingest; use partial findings to inform Step 3
- After summarizing: ask "Worth filing this as an analysis page?" — if yes, read `@scheduled-tasks/ops/conventions.md` first

**Step 3 — Training Knowledge** *(fallback only)*
Used when wiki and web both miss or are unavailable. Always append:
`Confidence: N/10 — [one-line caveat if score ≤ 7 or topic is time-sensitive]`

Omit the caveat when score is 8–10 and the topic is not time-sensitive.

**Edge cases:**
- Blueprint-authoring mode (no `wiki/` at root): Skip Step 1; go straight to Step 2 → Step 3
- Web search unavailable: Skip Step 2; fall to Step 3 with note: *"Web search unavailable."*

---
```

c2. Copy `blueprint/template/scheduled-tasks/ops/conventions.md` → `scheduled-tasks/ops/conventions.md`
c3. Copy `blueprint/template/scheduled-tasks/ops/blueprint-sync.md` → `scheduled-tasks/ops/blueprint-sync.md`
c4. Copy `blueprint/template/scheduled-tasks/refresh-hot.md` → `scheduled-tasks/refresh-hot.md`
d. Read `CLAUDE.md` footer (last non-empty line). If it already reads
   `Schema version: 2.3`, skip this step entirely.
   Otherwise (footer reads `Schema version: 2.2`), make these two edits:
   - Find the line containing `below v2.2` and replace the whole line with:
     `   - If \`hot.md\`'s \`Schema:\` is below \`v2.3\`: announce "Blueprint v2.3 is available — run \`!! migrate\` to update." (once per session)`
   - Find the footer line `*Schema version: 2.2 | Created:` and replace `2.2` with `2.3`.
e. Patch `hot.md`: update `Schema: v2.2` → `Schema: v2.3`
f. Append to `wiki/log.md`:
   `## [YYYY-MM-DD] migrate | v2.2 → v2.3 — wiki-first query routing redesign`
   (≤500 chars)

### Confirm

> "Migration complete. Query routing is now wiki-first.
> Backups saved to `backups/CLAUDE.md-v2.2-<date>.bak`, `backups/conventions.md-v2.2-<date>.bak`, and `backups/blueprint-sync.md-v2.2-<date>.bak` — delete when satisfied."

---

## v2.1 → v2.3 Path

Direct migration path from v2.1 to v2.3 in a single step — no intermediate v2.2 stop required. Step c copies `CLAUDE.md` from `blueprint/template/CLAUDE.md`, which already contains the v2.3 Query Routing Rule and v2.3 schema footer, so no separate routing patch is needed. The steps below are the complete v2.1→v2.3 procedure.

### Pre-flight

Run `python scripts/check_deps.py --python`
- If exit non-zero: stop. Show the printed instructions. Do not continue.

### Approval request

Show the user:

```
Migration: v2.1 → v2.3

Files REPLACED:
  CLAUDE.md  (rewritten — ~86% smaller, wiki-first query routing)

Files ADDED:
  scheduled-tasks/ops/session-memory.md
  scheduled-tasks/ops/blueprint-sync.md
  scheduled-tasks/ops/reference.md
  scheduled-tasks/ops/session-hygiene.md
  scheduled-tasks/ops/migrate.md
  scripts/check_deps.py
  scripts/wrap.py
  scripts/ready.py
  scripts/log_tail.py
  scripts/file_check.py
  scripts/estimate_tokens.py

Files DELETED:
  scheduled-tasks/ops/token-reference.md

Files UPDATED:
  scheduled-tasks/ops/audit.md       (recalibration sections removed)
  scheduled-tasks/ops/ingest.md      (bash → Python, post-op advisory added)
  scheduled-tasks/ops/lint.md        (bash → Python, post-op advisory added)
  scheduled-tasks/ops/conventions.md (updated for v2.3)
  scheduled-tasks/refresh-hot.md  (Step 3 updated to detect claude-code-enhanced skill)
  wiki/hot.md  (Schema bumped to v2.3; Python: field added)

Files UNTOUCHED:
  wiki/  (all pages, index, log preserved)
  memory.md, raw/, drafts/
  sqlite-query skill (if installed)

Shall I proceed?
```

### On approval, execute in order

a. Create `backups/` directory if absent.
b. Copy `CLAUDE.md` → `backups/CLAUDE.md-v2.1-<YYYY-MM-DD>.bak`
b2. Copy `scheduled-tasks/ops/conventions.md` → `backups/conventions.md-v2.1-<YYYY-MM-DD>.bak`
c. Read `blueprint/template/CLAUDE.md`, substitute `[created-date]` and
   `[updated-date]` with today's date, remove the `> **Setup note:**` block,
   write result to `CLAUDE.md`.
d. Copy each new ops file from `blueprint/template/scheduled-tasks/ops/` to
   `scheduled-tasks/ops/`:
   `session-memory.md`, `blueprint-sync.md`, `reference.md`,
   `session-hygiene.md`, `migrate.md`
e. Create `scripts/` directory if absent.
f. Copy each script from `blueprint/template/scripts/` to `scripts/`:
   `check_deps.py`, `wrap.py`, `ready.py`, `log_tail.py`,
   `file_check.py`, `estimate_tokens.py`
g. Copy updated ops files from `blueprint/template/scheduled-tasks/ops/` to
   `scheduled-tasks/ops/`:
   `audit.md`, `ingest.md`, `lint.md`, `conventions.md`
g2. Copy `blueprint/template/scheduled-tasks/refresh-hot.md` → `scheduled-tasks/refresh-hot.md`
h. Delete `scheduled-tasks/ops/token-reference.md` if it exists.
i. Patch `hot.md`:
   - Add `Python: [python | python3]` line (detect by running
     `python --version` or `python3 --version` and using whichever succeeds)
   - Update `Schema: v2.1` → `Schema: v2.3`
j. Append to `wiki/log.md`:
   `## [YYYY-MM-DD] migrate | v2.1 → v2.3 — lean cold-start + wiki-first routing`
   (≤500 chars)

### Confirm

> "Migration complete. Cold-start: ~7,780 → ~1,080 tokens. Query routing is now wiki-first.
> Backups saved to `backups/CLAUDE.md-v2.1-<date>.bak` and `backups/conventions.md-v2.1-<date>.bak` — delete when satisfied."

---

## Offer Claude Code enhanced skill (both paths)

> "Are you using Claude Code CLI? Run `!! install claude-code-enhanced` to add
> /wrap, /ready, and /migrate as native slash commands."

---

## Rollback

- **v2.2→v2.3:** Rename `backups/CLAUDE.md-v2.2-<date>.bak` → `CLAUDE.md`; rename `backups/conventions.md-v2.2-<date>.bak` → `scheduled-tasks/ops/conventions.md`; rename `backups/blueprint-sync.md-v2.2-<date>.bak` → `scheduled-tasks/ops/blueprint-sync.md`; revert `Schema:` in `hot.md` to `v2.2`.
- **v2.1→v2.3:** Rename `backups/CLAUDE.md-v2.1-<date>.bak` → `CLAUDE.md`; rename `backups/conventions.md-v2.1-<date>.bak` → `scheduled-tasks/ops/conventions.md`; revert `Schema:` in `hot.md` to `v2.1`. All new ops files and scripts/ are inert without the v2.1 `CLAUDE.md` referencing them.
