# Op: MIGRATE

Triggered when the user says `!! migrate`.

Upgrades an existing v2.1.x working folder to v2.2.

---

## Detection (runs at startup)

During startup step 7, compare `Schema:` in `hot.md` against the current schema
version (`v2.2`). If `Schema:` is below `v2.2`, announce once:

> "Blueprint v2.2 is available — run `!! migrate` to update your working folder.
> Cold-start will drop from ~7,780 to ~1,080 tokens after migration."

Announce at most once per session (do not repeat on every response).

---

## Steps

1. **Pre-flight:** Run `python scripts/check_deps.py --python`
   - If exit non-zero: stop. Show the printed instructions. Do not continue.

2. **Show approval request:**

   ```
   Migration: v2.1 → v2.2

   Files REPLACED:
     CLAUDE.md  (rewritten — ~86% smaller)

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
     scheduled-tasks/ops/conventions.md (updated for v2.2)

   Files UNTOUCHED:
     wiki/  (all pages, index, log, hot preserved)
     memory.md, raw/, drafts/
     ingest.md (beyond advisory update)
     sqlite-query skill (if installed)

   Shall I proceed?
   ```

3. **On approval, execute in order:**

   a. Create `backups/` directory if absent.
   b. Copy `CLAUDE.md` → `backups/CLAUDE.md-v2.1-<YYYY-MM-DD>.bak`
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
   h. Delete `scheduled-tasks/ops/token-reference.md` if it exists.
   i. Patch `hot.md`:
      - Add `Python: [python | python3]` line (detect by running
        `python --version` or `python3 --version` and using whichever succeeds)
      - Update `Schema: v2.1` → `Schema: v2.2`
   j. Append to `wiki/log.md`:
      `## [YYYY-MM-DD] migrate | v2.1 → v2.2 — lean cold-start restructure`
      (≤500 chars)

4. **Confirm:**
   > "Migration complete. Cold-start: ~7,780 → ~1,080 tokens.
   > Backup saved to `backups/CLAUDE.md-v2.1-<date>.bak` — delete when satisfied."

5. **Offer Claude Code enhanced skill:**
   > "Are you using Claude Code CLI? Run `!! install claude-code-enhanced` to add
   > /wrap, /ready, and /migrate as native slash commands."

---

## Rollback

Rename `backups/CLAUDE.md-v2.1-<date>.bak` → `CLAUDE.md`.
All other v2.1 files are untouched; the new ops files and `scripts/` are inert
without the v2.2 `CLAUDE.md` referencing them.
