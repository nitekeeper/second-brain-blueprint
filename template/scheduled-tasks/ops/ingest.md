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
    - On approval, write the inbox file first, then run Steps 5–13 unchanged.
U5. Note to the user once per `!! ingest <URL>` invocation (inline, not gated): "URL ingest is ~40–60% more expensive in tokens than a Web Clipper clip. Either path works — clipping is cheaper for future sources." If the user fires multiple URL ingests in the same session, emit the note on each one — "once" means once per invocation, not once per session.

## If `!! ingest all`

> Step numbers inside square brackets (e.g. `[main-step 5]`) refer to the numbered items in the **Steps** section below. The items in *this* batch preamble are numbered B1–B7 to keep the two lists from colliding.

Before running the main Steps:
B1. List all files in `wiki/inbox/` (Bash: `ls wiki/inbox/`)
B2. If empty, tell the user "Nothing in wiki/inbox/ to ingest." and stop
B3. Read `wiki/log.md` tail and `wiki/index.md` **ONCE** at the start of the batch — this stands in for `[main-step 1]` and the first file's index read inside `[main-step 8]`
B3.5. Read every source file in `wiki/inbox/` into working memory — this is a batch-level execution of `[main-step 2]` for every file at once. It is required so B4's approval request can list the exact pages each file will create or update. The combined cost of these reads must be included in the B4 token estimate. Do not skip this step — a B4 that lists pages without having read the sources is a lie by omission.
B3.6. For each file loaded in B3.5, run `[main-step 0]` (hash check). For any file whose 8-char SHA-256 prefix matches an existing source page's `source_hash:`, delete the inbox file and exclude it from the rest of the batch. Report these as `Skipped (no change): <file>` to the user BEFORE the B4 approval. If all files are no-ops, print `Nothing to ingest — all inbox files match existing source pages.` and stop (do not continue to B4, B5, B6, B7). Steps 12/13 only run when at least one file is actually ingested.
B4. Show a combined approval request listing every filename, the per-file and total token cost (including the B3.5 pre-reads and **one** (not per-file) read of `token-reference.md`), and all pages to be created/updated across the batch. Use the same per-approval `token-reference.md` cost as a single-file ingest. This stands in for `[main-steps 3 and 4]`
B5. Process each file in sequence using **`[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]`** per file — `[main-step 2]` was already executed at batch level in B3.5, so do NOT re-read sources here; also skip `[main-steps 1, 3, 4, 12, 13]`, which are handled at batch level (B3, B4, B6). **For the first file only,** `[main-step 8]` uses the cached `index.md` from B3. **For every subsequent file,** re-read `wiki/index.md` fresh at `[main-step 8]` — the previous file's `[main-step 10]` mutated it, and reusing the stale cache causes duplicate page creation and missed cross-links. The log.md tail stays cached across the batch; only index.md needs the per-file refresh.
B6. After all files are processed, run `[main-steps 12 and 13]` **ONCE** at the end of the batch (not per file)
B7. Write one log entry per file during `[main-step 11]` (not one combined entry)

---

## Hash Canonicalization

Step 0 of this op feeds the source body through this canonical pipeline **before** computing the SHA-256. Applying the normalizer ensures that Clipper ingest and URL ingest produce the same hash for identical underlying content — two paths that would otherwise produce visibly different markdown.

Steps (applied in order, producing the hash input):

1. **Strip any YAML preamble if present.** If the body begins with a `---` fence, drop everything from that fence through the next `---` fence (inclusive). Covers both the Clipper-saved frontmatter and the U3-prepended `source_url:` / `fetched:` block; a no-op if no preamble is present.
2. **Normalize line endings.** Convert CRLF and lone CR to LF.
3. **Collapse intra-line whitespace runs.** Replace any run of spaces or tabs with a single space.
4. **Collapse blank-line runs.** Replace any run of two or more consecutive blank lines with exactly one blank line.
5. **Trim.** Drop leading and trailing whitespace from the whole body.
6. **Hash.** Compute SHA-256 over the UTF-8 bytes of the result; take the first 8 hex characters as the source hash.

Do **not** lowercase, strip punctuation, or strip HTML tags in this pipeline. Case and punctuation are legitimate content signals; HTML tag leakage is an upstream fetcher bug and should be fixed there, not absorbed here.

Step 3's intra-line whitespace collapse also flattens **code-block indentation** — a line like `    if x:` canonicalizes to ` if x:` before hashing. This is intentional: different fetchers re-indent code differently (4 spaces vs tabs vs 2 spaces), and absorbing that drift here is the whole point of the normalizer. The consequence is that two sources differing *only* in code-block indentation will hash to the same value; a source whose real content change **is** the indentation level (e.g. a Python refactor whose only visible diff is re-indenting a block) will not be detected by this hash. For a personal wiki this is the right tradeoff — real edits almost always change tokens, not just indentation — but a code-aware downstream would want a language-sensitive normalizer.

This canonicalizer survives: Clipper-vs-WebFetch whitespace differences, CRLF/LF drift, trailing-whitespace jitter, and indentation-normalization differences. It does **not** survive: real content edits, CDN-driven body variation (timestamps, visitor counters, CSRF tokens leaking into markdown), or LLM-based WebFetch prose rewriting — all of which will correctly produce hash mismatches. See `troubleshooting.md` "URL ingest keeps regenerating the same source even when the article hasn't changed" for the LLM-WebFetch caveat.

---

## Steps

0. **Hash check (no-op guard).** First action of every ingest, before any other reads or writes:
    - Load the raw source body into working memory. For filename ingest: read `wiki/inbox/<file>`. For URL ingest: content is already in memory from U1 (this step does not re-read).
    - Run the body through the **Hash Canonicalization** pipeline above (preamble-strip if present → line-ending normalization → whitespace collapse → trim). Compute SHA-256 over the canonicalized bytes and take the first 8 hex characters as the computed hash. The same pipeline is used for both Clipper ingest and URL ingest, so both paths produce comparable hashes for identical underlying content.
    - Derive the expected source-page slug (lowercase-hyphenated from the H1 or filename stem; for URL ingest reuse the U2 slug). Step 7 consumes the already-derived `${slug}` and does not re-derive.
    - If `wiki/pages/sources/<slug>.md` exists, read its `source_hash:` frontmatter.
    - **If stored `source_hash:` matches the computed hash:** delete the inbox file (if present), print `No change since last ingest — skipped.` to the user, and exit cleanly. Do NOT continue to Step 1. Do NOT append to `log.md`. Do NOT refresh `hot.md`. Do NOT recalibrate. This is the rerun-proof guarantee — same input, zero state change.
    - **Otherwise** (hash differs, source page doesn't exist, or source page is missing `source_hash:`): continue to Step 1. Step 7 will (re)generate the source page from the new content; there is no in-place merge.
1. Read the last 5 entries of `wiki/log.md` for recent context (`grep -E "^## \[" wiki/log.md | tail -5`)
2. Source content is already in working memory from Step 0 — do not re-read.
3. Discuss key takeaways with the user (brief, 3–5 bullets)
4. Show approval request (summary + token estimate + to-do list) and wait for confirmation — include the cost of re-reading `token-reference.md` itself (see the self-cost figure in its header) in the estimate
5. **Pre-compute `ts` for this ingest.** Generate once — `ts=$(date +%Y-%m-%d-%H%M%S)` — and hold it in working memory for the rest of the op. The same `ts` is used by Step 6's raw-file move and by Step 7's `original_file:` frontmatter + every `[^n]:` footnote in the source page. Pre-computation is load-bearing: Step 7 writes filenames referencing the Step-6 snapshot, so the two must agree to the second. If Steps 6 and 7 each generated their own `ts`, the source page's `original_file:` and footnote trail would dangle against the actual raw filename.

    **Execution mechanism (two acceptable patterns):** Cowork Bash does not persist env vars across tool calls, so "hold in working memory" must be implemented deliberately. Either (i) run `date +%Y-%m-%d-%H%M%S` in a standalone Bash call, capture the printed timestamp into LLM working memory, and inline it as `export ts="<captured-value>"` at the top of Step 6's Bash call (alongside `export WORKDIR=...`, `export file=...`, `export slug=...`); or (ii) fold Steps 5 and 6 into a single Bash invocation that assigns `ts=$(date +%Y-%m-%d-%H%M%S)` before the `mv` and uses `$ts` locally. Either way, the `ts` value Step 6 consumes MUST be the exact value Step 7 inlines into `original_file:` and every `[^n]:` footnote — Step 6's `${ts:?…}` guard will fail loudly if an unset variable leaks through, but it cannot catch a *different* `ts` being written into Step 7's source page.
6. Move the source file from `wiki/inbox/` to `raw/<slug>-<ts>.md` **before** writing the source page. Second-precision timestamps are physically unique in single-user workflow, so no collision handling is needed — every raw snapshot is a unique immutable record. **Ordering matters:** the move MUST complete before Step 7 so that a mid-flight failure leaves the inbox file intact — retry's Step 0 hash check then sees the inbox content and proceeds cleanly. If the order were reversed (source page written first, then move), a crash between the two would commit a `source_hash:` without a matching raw file; the next retry's Step 0 would hash-match and silently delete the inbox file, losing the source entirely. See `troubleshooting.md` "Ingest interrupted mid-flight…" for the prior-version failure mode this ordering fixes.
    ```bash
    cd "${WORKDIR:?WORKDIR must be set to the working-folder absolute path — see setup-guide.md Step 1}"
    : "${file:?file path is required — set \$file to the wiki/inbox/... source before running}"
    : "${slug:?slug is required — set \$slug to the derived source slug before running}"
    : "${ts:?ts is required — pre-compute it once in Step 5 via date +%Y-%m-%d-%H%M%S and export it alongside \$WORKDIR / \$file / \$slug}"
    [ -e "$file" ] || { echo "source not found: $file"; exit 1; }
    dest="raw/${slug}-${ts}.md"
    mv "$file" "$dest"
    ```
    `WORKDIR`, `file`, `slug`, and `ts` must all be exported in the **same** Bash invocation as the snippet — env vars do not persist across Cowork Bash calls. The `${…:?}` guards refuse to run if any variable is unset rather than silently operating on the wrong path.
7. Write (or regenerate) a source summary page in `wiki/pages/sources/`. The frontmatter MUST include:
    - `related: [slug-1, slug-2]` — slugs of every concept and entity page created or updated as part of this ingest. This is the relationship layer: populated here so query and lint ops can find connections via grep without reading page content. Update this list whenever related pages change.
    - `source_hash: <8-char-hex>` — the same hash computed in Step 0. Dedupe primitive; a missing or stale `source_hash:` will cause the next ingest to trigger a full regeneration.
    - `original_file: raw/<slug>-<ts>.md` — using the Step-5 `ts`. Every `[^n]:` provenance footnote in the Key Takeaways section must cite the same `raw/<slug>-<ts>.md` path.
    - `source_url: <URL>` — the canonical URL this source was pulled from. For URL ingest, reuse the value U3 already prepended. For filename (Clipper) ingest, pull the URL from the Clipper's own preamble (Obsidian Web Clipper writes `source:` by default; accept that, `url:`, or any equivalent field that carries the origin URL) and propagate it verbatim into `source_url:`. If no URL is recoverable from the Clipper preamble, write `source_url: unknown` and note the gap in the approval request so the user can correct it post-ingest. This field records source provenance and is useful for manually tracking whether a source has been updated.

    On hash mismatch, fully regenerate the page from the new raw content — do not attempt to merge with the prior page body.
8. Read `wiki/index.md` to identify all affected concept/entity pages
9. Update affected pages; create any new concept or entity pages warranted. For every concept and entity page created or updated: populate or extend its `related:` frontmatter field with slugs of other pages touched in this ingest. Relationships should be bidirectional — if page A lists page B in `related:`, page B should list page A. This is enforced by lint, so a missed direction here will surface on the next `!! lint` pass.
10. Update `wiki/index.md` with new and modified entries
11. Append entry to `wiki/log.md` — **must be ≤500 chars total (header + body)**:
    `## [YYYY-MM-DD] ingest | [Title]`
    If the entry would exceed 500 chars, compress the title/body (or split into a follow-up entry).
11.5. **Run ingest hook if installed.** If `scheduled-tasks/ingest-hook.md` exists, read it and execute it — passing the current page's `slug`, `title`, `type`, `summary`, `tags`, `created`, `updated`, and `related` from working memory. Run once per page touched in this ingest (source page + every concept/entity page created or updated in Steps 7–9). Hook errors are non-fatal — log the warning and continue.
12. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
13. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section)

## Notes

- A single source typically touches 5–15 pages. Be thorough.
- Read `@scheduled-tasks/ops/conventions.md` before creating or editing any pages.
- Source pages must include: `original_file:`, `source_hash:`, and `source_url:` frontmatter; Key Takeaways section; Connections section; and `[^n]:` provenance footnotes on every curated bullet. See Step 7 for the `source_url:` fallback path when no URL is recoverable from the Clipper preamble.
- Rerun-proof guarantee: running the same ingest twice produces zero state change. See Step 0.
