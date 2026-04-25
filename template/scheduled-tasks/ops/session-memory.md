# Session Memory Commands

**Temporary, intentional memory — designed to bridge one session to the next, not to accumulate.**
Read this file when the user says `!! wrap` or `!! ready`.

---

## Explicit state markers

`memory.md` uses HTML-comment markers:
- Empty: `<!-- MEMORY_STATE: EMPTY -->`
- Valid summary: begins with `<!-- MEMORY_STATE: WRAPPED -->`, ends with `<!-- MEMORY_WRAP_COMPLETE -->`
- Acknowledged truncated: `<!-- MEMORY_STATE: TRUNCATED_ACKNOWLEDGED -->` — treated identically to EMPTY

**Truncation:** If file contains `MEMORY_STATE: WRAPPED` but is missing `MEMORY_WRAP_COMPLETE`, it is truncated.

---

## `!! wrap`

1. **Pre-write safeguard:** Run `python scripts/wrap.py check`
   - Exit 0 (EMPTY): proceed without prompt
   - Exit 1 (WRAPPED): warn user — "A previous session summary is still in memory.md. Overwriting will destroy it. Proceed? (yes/no)" — wait for explicit confirmation
   - Exit 2 (TRUNCATED_ACKNOWLEDGED): warn user — "A preserved (truncated) summary is still in memory.md. Overwriting will destroy it. Proceed? (yes/no)" — wait for explicit confirmation

2. Ask: "Anything specific you'd like included in the summary?"

3. Compose a detailed summary structured as:
   ```
   # Session Memory — [YYYY-MM-DD]

   ## Worked on
   …

   ## Key decisions
   …

   ## Files created / modified
   …

   ## Open questions / next steps
   …
   ```
   Then pipe it to: `python scripts/wrap.py write`
   The script writes the summary with the correct state markers and completion marker.

4. Append to `wiki/log.md`: `## [YYYY-MM-DD] memory | Session summary saved` (≤500 chars)

5. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`

6. Confirm: "Session summary saved. Say `!! ready` next session to load it."

---

## `!! ready`

1. **Mid-session guard:** If this is NOT the first user message of the session, reply: "`!! ready` is meant as a session-opening command. You seem to be mid-session — say `!! ready confirm` if you really want to read and wipe the summary now." Only proceed on `!! ready confirm`.

2. Run `python scripts/ready.py read` and check exit code:

3. **Exit 0 (EMPTY or TRUNCATED_ACKNOWLEDGED):** Announce readiness normally from `hot.md`. Do not wipe. If TRUNCATED_ACKNOWLEDGED: prior session already shown content and user chose to keep it — leave it alone.

4. **Exit 2 (TRUNCATED):** Display what was printed to stdout. Warn it appears incomplete. Do NOT wipe. Offer three options and wait for explicit choice:
   - `clear` — run `python scripts/ready.py clear`, then append to `wiki/log.md`: `## [YYYY-MM-DD] memory | Truncated summary cleared` (≤500 chars), refresh `hot.md`
   - `keep`  — run `python scripts/ready.py keep`,  then append to `wiki/log.md`: `## [YYYY-MM-DD] memory | Truncated summary acknowledged` (≤500 chars), refresh `hot.md`
   - `edit`  — hand control back to user; touch nothing, write nothing

5. **Exit 1 (WRAPPED + COMPLETE):** Display the full summary verbatim (do not paraphrase, do not truncate).
   - Append to `wiki/log.md`: `## [YYYY-MM-DD] memory | Session summary consumed` (≤500 chars)
   - Run `python scripts/ready.py clear` to wipe memory.md
   - Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
   - Confirm: "Memory cleared. Ready to work."
   - Surface any in-progress drafts from `drafts/` (same as normal startup step 3). If `drafts/` is absent, skip transparently.

**Blueprint-authoring mode:** If `wiki/` absent at working folder root, skip all `wiki/log.md` appends and `hot.md` refreshes above — see CLAUDE.md Blueprint-authoring mode note.
