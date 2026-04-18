# Op: AUDIT

Triggered when the user says `!! audit all` or `!! audit [Page Name]`.

Audits files under `blueprint/` — the distribution template, its docs, and its ops files — for logic contradictions, security / safety footguns, performance / token waste, and blueprint-sync drift. Audits are **read-only by default**; any fix the user asks you to apply afterward goes through the normal approval flow.

> **Scope reminder:** AUDIT targets `blueprint/` files only. Use `!! lint` for wiki-page quality (broken links, orphans, stale claims). If the user asks to audit a wiki page, redirect them to `!! lint`.

---

## If `!! audit all`

Audit every file under `blueprint/`, including:

- `blueprint/README.md`
- `blueprint/setup-guide.md`
- `blueprint/user-guide.md`
- `blueprint/troubleshooting.md`
- `blueprint/LICENSE`
- `blueprint/.gitignore`
- `blueprint/template/CLAUDE.md`
- `blueprint/template/scheduled-tasks/refresh-hot.md`
- Every file under `blueprint/template/scheduled-tasks/ops/`

## If `!! audit [Page Name]`

Resolve the name to a single file under `blueprint/`, matching by slug (case-insensitive, hyphen-flexible — e.g. `conventions`, `Conventions`, `ops/conventions`, `conventions.md` all resolve to `blueprint/template/scheduled-tasks/ops/conventions.md`). If the name is ambiguous (matches multiple files), list the candidates and ask the user to pick before reading anything. If no match, say so and stop.

---

## Steps

1. Resolve scope (all blueprint files, or a single matched file).
2. Read the file(s) in scope.
3. Apply the **Audit Prompt** below verbatim as your operating instructions while reviewing.
4. Report findings to the user. No approval request is needed to run the audit — it is read-only.
5. If the user asks for any fix to be applied:
   - Blueprint files are not wiki pages — `ops/conventions.md` does not apply. Edit blueprint files directly; the Blueprint Sync Rule bullet below governs any downstream propagation.
   - Show a normal approval request (summary + token estimate including the `token-reference.md` self-cost (see `@scheduled-tasks/ops/token-reference.md` header) + to-do list of affected files).
   - After approval, apply fixes.
   - If any fix touches the schema, startup behavior, operations, or conventions, follow the Blueprint Sync Rule in `CLAUDE.md` — update every downstream doc the table lists before closing the op.
   - Append one entry to `wiki/log.md` (≤500 chars): `## [YYYY-MM-DD] audit | [fix summary]`
6. If a fix was applied in step 5, refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`. The log-append is a wiki-state mutation, so `hot.md`'s `Last op` must reflect it. If no fix was applied (read-only audit), skip — the audit leaves no trace.
7. Recalibrate token estimates — follow `@scheduled-tasks/ops/token-reference.md` (Recalibration section) — only if an applied fix changed a tracked file's size enough to exceed its documented Chars value.

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
- For `!! audit all`, expect ~20,000–25,000 tokens of reads. Warn the user up front if the session is already close to context limits.
- For `!! audit [Page Name]`, expect ~1,000–5,000 tokens depending on file size.
