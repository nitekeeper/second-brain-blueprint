# Op: INGEST

Triggered when the user drops a new source and says "ingest this."

## If `!! ingest <URL>`

Triggered when the user passes a URL (e.g. `!! ingest https://example.com/article`).

U1. Fetch the URL using an HTML-to-markdown fetcher (WebFetch or equivalent) — read-only, no approval needed. Abort with a clear error if the fetch fails or returns empty.
U2. Derive a slug from the page title (lowercase-hyphenated); fall back to the URL's last path segment if the title is unusable. Proposed filename: `wiki/inbox/<slug>.md`.
U3. Prepend a short YAML preamble with `source_url:` and `fetched:` (today's date) to the fetched markdown, held in working memory. Do NOT write yet.
U4. Run main **Steps** as follows:
    - Step 0 (hash check) — runs on the in-memory content from U1. If the stored `source_hash:` matches, exit cleanly with `No change since last ingest — skipped.` No inbox file is written, no approval is requested — nothing would have changed.
    - Step 1 (log tail read) — unchanged.
    - Step 2 — source content is already in working memory; skip the `wiki/inbox/` read.
    - Step 3 (discuss takeaways) — use the in-memory content.
    - Step 4 (approval) — to-do list **must** include "Save fetched article to `wiki/inbox/<slug>.md`" as the first item; the rest (source page create, index/log update, inbox→raw move, etc.) is identical to a filename-based ingest.
    - On approval, write the inbox file first, then run Steps 5–12 unchanged.
U5. Note to the user once per `!! ingest <URL>` invocation (inline, not gated): "URL ingest is ~40–60% more expensive in tokens than a Web Clipper clip. Either path works — clipping is cheaper for future sources." If the user fires multiple URL ingests in the same session, emit the note on each one — "once" means once per invocation, not once per session.

## If `!! ingest all`

> Step numbers inside square brackets (e.g. `[main-step 5]`) refer to the numbered items in the **Steps** section below. The items in *this* batch preamble are numbered B1–B7 to keep the two lists from colliding.

Before running the main Steps:
B1. List all files in `wiki/inbox/` (Bash: `ls wiki/inbox/`)
B2. If empty, tell the user "Nothing in wiki/inbox/ to ingest." and stop
B3. Read `wiki/log.md` tail and `wiki/index.md` **ONCE** at the start of the batch — this stands in for `[main-step 1]` and the first file's index read inside `[main-step 6]`
B3.5. Read every source file in `wiki/inbox/` into working memory — this is a batch-level execution of `[main-step 2]` for every file at once. It is required so B4's approval request can list the exact pages each file will create or update. The combined cost of these reads must be included in the B4 token estimate. Do not skip this step — a B4 that lists pages without having read the sources is a lie by omission.
B3.6. For each file loaded in B3.5, run `[main-step 0]` (hash check). For any file whose 8-char SHA-256 prefix matches an existing source page's `source_hash:`, delete the inbox file and exclude it from the rest of the batch. Report these as `Skipped (no change): <file>` to the user BEFORE the B4 approval. If all files are no-ops, print `Nothing to ingest — all inbox files match existing source pages.` and stop (do not continue to B4, B5, B6, B7). Steps 11/12 only run when at least one file is actually ingested.
B4. Show a combined approval request listing every filename, the per-file and total token cost (including the B3.5 pre-reads and **one** (not per-file) read of `token-reference.md`), and all pages to be created/updated across the batch. Use the same per-approval `token-reference.md` cost as a single-file ingest. This stands in for `[main-steps 3 and 4]`
B5. Process each file in sequence using **`[main-steps 5, 6, 7, 8, 9, 10]`** per file — `[main-step 2]` was already executed at batch level in B3.5, so do NOT re-read sources here; also skip `[main-steps 1, 3, 4, 11, 12]`, which are handled at batch level (B3, B4, B6). **For the first file only,** `[main-step 6]` uses the cached `index.md` from B3. **For every subsequent file,** re-read `wiki/index.md` fresh at `[main-step 6]` — the previous file's `[main-step 8]` mutated it, and reusing the stale cache causes duplicate page creation and missed cross-links. The log.md tail stays cached across the batch; only index.md needs the per-file refresh.
B6. After all files are processed, run `[main-steps 11 and 12]` **ONCE** at the end of the batch (not per file)
B7. Write one log entry per file during `[main-step 10]` (not one combined entry)

---

## Steps

0. **Hash check (no-op guard).** First action of every ingest, before any other reads or writes:
    - Load the raw source body into working memory. For filename ingest: read `wiki/inbox/<file>`. For URL ingest: content is already in memory from U1 (this step does not re-read).
    - Strip any YAML preamble (e.g. the `source_url:` / `fetched:` block prepended in U3) — hash only the content body so the hash is stable across re-fetches of the same content.
    - Compute the 8-char SHA-256 hex prefix of the body.
    - Derive the expected source-page slug — same rules as Step 5 (lowercase-hyphenated from the H1 or filename stem; for URL ingest reuse the U2 slug).
    - If `wiki/pages/sources/<slug>.md` exists, read its `source_hash:` frontmatter.
    - **If stored `source_hash:` matches the computed hash:** delete the inbox file (if present), print `No change since last ingest — skipped.` to the user, and exit cleanly. Do NOT continue to Step 1. Do NOT append to `log.md`. Do NOT refresh `hot.md`. Do NOT recalibrate. This is the rerun-proof guarantee — same input, zero state change.
    - **Otherwise** (hash differs, source page doesn't exist, or source page is missing `source_hash:`): continue to Step 1. Step 5 will (re)generate the source page from the new content; there is no in-place merge.
1. Read the last 5 entries of `wiki/log.md` for recent context (`grep -E "^## \[" wiki/log.md | tail -5`)
2. Source content is already in working memory from Step 0 — do not re-read.
3. Discuss key takeaways with the user (brief, 3–5 bullets)
4. Show approval request (summary + token estimate + to-do list) and wait for confirmation — include the cost of re-reading `token-reference.md` itself (see the self-cost figure in its header) in the estimate
5. Write (or regenerate) a source summary page in `wiki/pages/sources/`. The frontmatter MUST include `source_hash: <8-char-hex>` — the same hash computed in Step 0. This is the dedupe primitive; a missing or stale `source_hash:` will cause the next ingest to trigger a full regeneration. On hash mismatch, fully regenerate the page from the new raw content — do not attempt to merge with the prior page body.
6. Read `wiki/index.md` to identify all affected concept/entity pages
7. Update affected pages; create any new concept or entity pages warranted
8. Update `wiki/index.md` with new and modified entries
9. Move the source file from `wiki/inbox/` to `raw/<slug>-<YYYY-MM-DD-HHMMSS>.md`. Second-precision timestamps are physically unique in single-user workflow, so no collision handling is needed — every raw snapshot is a unique immutable record. **Ordering matters:** Step 5's source-page write (with the new `source_hash:`) MUST complete before this move. If Step 5 fails, the inbox file stays in `wiki/inbox/` and retry is clean — no orphan raw files with mismatched page state.
    ```bash
    cd "${WORKDIR:?WORKDIR must be set to the working-folder absolute path — see setup-guide.md Step 1}"
    : "${file:?file path is required — set \$file to the wiki/inbox/... source before running}"
    : "${slug:?slug is required — set \$slug to the derived source slug before running}"
    [ -e "$file" ] || { echo "source not found: $file"; exit 1; }
    ts=$(date +%Y-%m-%d-%H%M%S)
    dest="raw/${slug}-${ts}.md"
    mv "$file" "$dest"
    ```
    `WORKDIR`, `file`, and `slug` must all be exported in the **same** Bash invocation as the snippet — env vars do not persist across Cowork Bash calls. The `${…:?}` guards refuse to run if any variable is unset rather than silently operating on the wrong path.
10. Append entry to `wiki/log.md` — **must be ≤500 chars total (header + body)**:
    `## [YYYY-MM-DD] ingest | [Title]`
    If the entry would exceed 500 chars, compress the title/body (or split into a follow-up entry).
11. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
12. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section)

## Notes

- A single source typically touches 5–15 pages. Be thorough.
- Read `@scheduled-tasks/ops/conventions.md` before creating or editing any pages.
- Source pages must include: `original_file:` and `source_hash:` frontmatter, Key Takeaways section, Connections section, and `[^n]:` provenance footnotes on every curated bullet.
- Rerun-proof guarantee: running the same ingest twice produces zero state change. See Step 0.
