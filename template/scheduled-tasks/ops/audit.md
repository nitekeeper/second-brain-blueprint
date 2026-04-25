# Op: AUDIT

Triggered when the user says `!! audit all` or `!! audit [Page Name]`.

Audits files under `blueprint/` — the distribution template, its docs, and its ops files — for logic contradictions, security / safety footguns, performance / token waste, and blueprint-sync drift. Audits are **read-only by default**; any fix the user asks you to apply afterward goes through the normal approval flow.

> **Scope reminder:** AUDIT targets `blueprint/` files only. Use `!! lint` for wiki-page quality (broken links, orphans, stale claims). If the user asks to audit a wiki page, redirect them to `!! lint`.

---

## If `!! audit all`

Audit every tracked file under `blueprint/` — specifically the files listed below. `blueprint/.git/` is VCS state and is always excluded.

- `blueprint/README.md`
- `blueprint/setup-guide.md`
- `blueprint/user-guide.md`
- `blueprint/troubleshooting.md`
- `blueprint/CHANGELOG.md`
- `blueprint/LICENSE`
- `blueprint/.gitignore`
- `blueprint/template/CLAUDE.md`
- Every file directly under `blueprint/template/scheduled-tasks/` (currently `refresh-hot.md`; do not recurse into `ops/`)
- Every file under `blueprint/template/scheduled-tasks/ops/`
- Every file under `blueprint/skills/` (skill bundles — recurse into subdirectories)

## If `!! audit [Page Name]`

Resolve the name to a single file under `blueprint/`, matching by slug (case-insensitive, hyphen-flexible — e.g. `conventions`, `Conventions`, `ops/conventions`, `conventions.md` all resolve to `blueprint/template/scheduled-tasks/ops/conventions.md`). If the name is ambiguous (matches multiple files), list the candidates and ask the user to pick before reading anything. If no match, say so and stop.

---

## Steps

0. **Load prior audit context.** Check whether an `audits/` directory exists (`python scripts/file_check.py audits/`). If it does, list `.md` files inside and identify the most recent audit report (reports are named `AUD-YYYY-MM-DD-NNN.md` — sort lexicographically, take the last). Read its **Action Items** and **Detailed Findings** sections. Extract all findings whose **Status** is `OPEN` or `IN PROGRESS` — these are "carried-over findings" to verify in the new report's **Previous Findings Verification** section. Flag any finding that appeared in the two most recent reports as a **repeat finding** (`⚠️ Repeat finding — systemic drift`). If `audits/` is absent or empty, set carried-over findings to none.

1. Resolve scope (all blueprint files, or a single matched file).
2. Read the file(s) in scope.
3. Apply the **Audit Prompt** below verbatim as your operating instructions while reviewing. Hold the findings in working memory — do not print them yet.

4. **Generate and save the audit report.**

   a. Assign report ID: `AUD-YYYY-MM-DD-NNN` — NNN starts at `001`; if a report with today's date already exists in `audits/`, increment NNN.
   b. Read `@blueprint/documents/audit-report-template.md` (blueprint-authoring mode: `@documents/audit-report-template.md`).
   c. Fill in every section of the template:
      - **Report Header**: report ID, today's date, scope, schema version (read from `CLAUDE.md` footer), previous report ID or `None`.
      - **Executive Summary**: 2–3 sentences; overall risk level (CRITICAL if any open CRITICALs → `CRITICAL`; open WARNINGs only → `HIGH`; open STYLEs only → `MEDIUM`; zero open findings → `CLEAN`); finding counts by severity broken into new vs. carried-over.
      - **Previous Findings Verification**: for each carried-over finding, state its verified status (`RESOLVED` / `OPEN` / `IN PROGRESS`) with a one-line evidence note (e.g. `"Fixed in commit abc1234"` or `"Still present at Step 3"`). Repeat findings get the `⚠️ Repeat finding` flag.
      - **Scope**: list every file read in Step 2.
      - **Detailed Findings**: one `###` section per finding, IDs assigned in discovery order. Fill all five fields — **Condition** (quoted evidence), **Criteria** (the rule violated), **Cause** (root cause), **Consequence** (specific failure mode), **Recommendation** (exact fix). If no findings: replace the section with "No findings. The blueprint is logically sound in the audited scope."
      - **Action Items**: `- [ ]` checklist sorted by severity (CRITICAL first). One line per finding: `` `ID` **[SEV]** Title — Owner: ___ | Target: ___ ``
      - **Appendix**: list of files audited with token estimates from `python scripts/estimate_tokens.py <files>`.
   d. Create `audits/` directory if absent (`mkdir -p audits` via Bash, or Write tool — Write creates parent directories automatically).
   e. Write the completed report to `audits/AUD-YYYY-MM-DD-NNN.md`. Writing the audit report is an implicit side-effect of `!! audit` — no separate approval is needed (even for a clean audit).

5. **Report summary to the user.** Print: overall risk level, finding counts by severity (new + carried-over), and the report path. Example: `"Audit complete. Risk: HIGH — 0 CRITICALs, 3 WARNINGs, 1 STYLE. Carried over: 1 (now RESOLVED). Report saved to audits/AUD-2026-04-25-001.md."`

6. **If the user asks for any fix to be applied:**
   - Blueprint files are not wiki pages — `ops/conventions.md` does not apply. Edit blueprint files directly; the Blueprint Sync Rule governs downstream propagation.
   - Show a normal approval request (summary + token estimate via `python scripts/estimate_tokens.py <affected-files>` + to-do list of affected files).
   - After approval, apply fixes.
   - Re-open the saved audit report and update each resolved finding: set **Status** to `RESOLVED`, check off the corresponding Action Items entry (`- [x]`).
   - If any fix touches the schema, startup behavior, operations, or conventions, follow the Blueprint Sync Rule in `CLAUDE.md`.
   - **Blueprint-authoring mode:** if `wiki/` is absent, skip the `wiki/log.md` append below AND step 7's `hot.md` refresh. Check once (`python scripts/file_check.py wiki/log.md`) and skip transparently without prompting.
   - Append one entry to `wiki/log.md` (≤500 chars): `## [YYYY-MM-DD] audit | [fix summary]`

7. If a fix was applied in step 6, refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`. **Blueprint-authoring mode:** skip.

8. **Post-op advisory.** Append the session advisory block from `@scheduled-tasks/ops/session-hygiene.md` (Post-op advisory block section) to this response. Set `SESSION_HEAVY = true`.

---

## Audit Prompt

Use the prompt below **verbatim** as the operating instructions when reading the file(s) in scope. Do not soften it, do not add theoretical nitpicks, do not pad the report.

> **Role:** Act as a Senior Software Architect performing a strict, objective audit.
>
> **Task:** Review all files in scope for logic errors, security vulnerabilities, or performance bottlenecks.
>
> **Rules for Accuracy:**
>
> 1. **Zero-Defect Permission:** If the code is logically sound and follows best practices, you MUST state "No bugs found." Do not manufacture minor style nitpicks or theoretical issues just to provide a list.
> 2. **Evidence Required:** For every bug you claim to find, you must quote the specific line of code and explain the exact logical failure.
> 3. **Distinguish Severity:** If you find an issue, label it as **CRITICAL** (breaks logic), **WARNING** (potential edge case), or **STYLE** (readability only).
> 4. **Chain of Verification:** Before listing any bugs, briefly restate the code's intended logic to ensure you understand the context correctly.
>
> **Goal:** Provide a high-precision audit. If you are unsure whether something is a bug, list it as a "Question for Clarification" rather than a definitive error.

## Notes

- Audits of instructional markdown are still meaningful: rules can contradict each other, state machines can have unreachable branches, approval paths can leak, documented token estimates can drift from reality. Treat these as the analog of "logic errors" for this codebase.
- Keep the severity bar high. If the blueprint is sound, say so.
- For `!! audit all`, expect ~30,000–47,000 tokens of reads for the tracked files. Run `python scripts/estimate_tokens.py blueprint/README.md blueprint/setup-guide.md blueprint/user-guide.md blueprint/troubleshooting.md blueprint/template/CLAUDE.md blueprint/template/scheduled-tasks/refresh-hot.md blueprint/template/scheduled-tasks/ops/*.md blueprint/skills/sqlite-query/*.md blueprint/skills/claude-code-enhanced/*.md` for a live estimate. Warn the user up front if the session is already close to context limits.
- For `!! audit [Page Name]`, expect ~1,000–5,000 tokens depending on file size.
