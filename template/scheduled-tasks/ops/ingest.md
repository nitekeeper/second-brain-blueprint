# Op: INGEST

Triggered when the user drops a new source and says "ingest this."

## If `!! ingest all`

> Step numbers inside square brackets (e.g. `[main-step 5]`) refer to the numbered items in the **Steps** section below. The items in *this* batch preamble are numbered B1–B7 to keep the two lists from colliding.

Before running the main Steps:
B1. List all files in `wiki/inbox/` (Bash: `ls wiki/inbox/`)
B2. If empty, tell the user "Nothing in wiki/inbox/ to ingest." and stop
B3. Read `wiki/log.md` tail and `wiki/index.md` **ONCE** at the start of the batch — this stands in for `[main-step 1]` and the first file's index read inside `[main-step 6]`
B3.5. Read every source file in `wiki/inbox/` into working memory — this is a batch-level execution of `[main-step 2]` for every file at once. It is required so B4's approval request can list the exact pages each file will create or update. The combined cost of these reads must be included in the B4 token estimate. Do not skip this step — a B4 that lists pages without having read the sources is a lie by omission.
B4. Show a combined approval request listing every filename, the per-file and total token cost (including the B3.5 pre-reads and **one** (not per-file) read of `token-reference.md`), and all pages to be created/updated across the batch. Use the same per-approval `token-reference.md` cost as a single-file ingest. This stands in for `[main-steps 3 and 4]`
B5. Process each file in sequence using **`[main-steps 5, 6, 7, 8, 9, 10]`** per file — `[main-step 2]` was already executed at batch level in B3.5, so do NOT re-read sources here; also skip `[main-steps 1, 3, 4, 11, 12]`, which are handled at batch level (B3, B4, B6). **For the first file only,** `[main-step 6]` uses the cached `index.md` from B3. **For every subsequent file,** re-read `wiki/index.md` fresh at `[main-step 6]` — the previous file's `[main-step 8]` mutated it, and reusing the stale cache causes duplicate page creation and missed cross-links. The log.md tail stays cached across the batch; only index.md needs the per-file refresh.
B6. After all files are processed, run `[main-steps 11 and 12]` **ONCE** at the end of the batch (not per file)
B7. Write one log entry per file during `[main-step 10]` (not one combined entry)

---

## Steps

1. Read the last 5 entries of `wiki/log.md` for recent context (`grep -E "^## \[" wiki/log.md | tail -5`)
2. Read the source file from `wiki/inbox/`
3. Discuss key takeaways with the user (brief, 3–5 bullets)
4. Show approval request (summary + token estimate + to-do list) and wait for confirmation — include the cost of re-reading `token-reference.md` itself (see the self-cost figure in its header) in the estimate
5. Write a source summary page in `wiki/pages/sources/`
6. Read `wiki/index.md` to identify all affected concept/entity pages
7. Update affected pages; create any new concept or entity pages warranted
8. Update `wiki/index.md` with new and modified entries
9. Move the source file from `wiki/inbox/` to `raw/` — **with collision handling**:
    ```bash
    : "${file:?file path is required — set \$file to the wiki/inbox/... source before running}"
    [ -e "$file" ] || { echo "source not found: $file"; exit 1; }
    base=$(basename "$file")
    dest="raw/$base"
    if [ -e "$dest" ]; then
      ts=$(date +%Y%m%d-%H%M%S)
      dest="raw/${ts}-${base}"
      i=0
      while [ -e "$dest" ]; do
        i=$((i+1))
        dest="raw/${ts}-${i}-${base}"
      done
    fi
    mv -n "$file" "$dest"
    [ -e "$file" ] && { echo "refusing to overwrite: $dest"; exit 1; }
    ```
    Never allow an overwrite into `raw/` — it breaks the immutable-archive promise. A bare timestamp isn't enough when two files land in the same second; the counter loop + `mv -n` + post-check together close the race.
10. Append entry to `wiki/log.md` — **must be ≤500 chars total (header + body)**:
    `## [YYYY-MM-DD] ingest | [Title]`
    If the entry would exceed 500 chars, compress the title/body (or split into a follow-up entry).
11. Refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`
12. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section)

## Notes

- A single source typically touches 5–15 pages. Be thorough.
- Read `@scheduled-tasks/ops/conventions.md` before creating or editing any pages.
- Source pages must include: `original_file:` frontmatter, Key Takeaways section, Connections section.
