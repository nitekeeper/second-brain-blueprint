# Blueprint Audit Report — 2026-04-18 (#4)

**Scope:** `!! audit all` — every tracked file under `blueprint/` per `ops/audit.md` §If `!! audit all`
**Mode:** Read-only (blueprint-authoring workspace — no `wiki/` present)
**Operator:** hchung@frontrowgroup.com
**Prior audits this day:**
- `audit-report-2026-04-18.md` — C1, W1–W4, S1–S2, Q1–Q2 (landed in v2.0 / v2.0.1)
- `audit-report-2026-04-18-02.md` — C1-new (hash canonicalization), W1–W4 (landed in v2.0.2)
- `audit-report-2026-04-18-03.md` — W1 (Pages-counter), S1 (conventions.md recalibration), S2 (versioning split), Q1 (footer asymmetry) — W1/S1/S2 landed in v2.0.3; Q1 remains open ("Not applied")

---

## 1. Restatement of intended logic (Chain of Verification)

The blueprint is a self-contained template for an LLM-driven personal wiki. `template/CLAUDE.md` is the agent schema; `template/scheduled-tasks/ops/*` are operation handbooks invoked by `!! <op>` commands; `refresh-hot.md` and `changelog-monitor.md` are the two scheduled tasks. `README.md`, `user-guide.md`, `setup-guide.md`, `troubleshooting.md`, and `CHANGELOG.md` are human-facing docs. The Blueprint Sync Rule keeps these in lock-step.

Invariants carried from prior audits (now stable):

1. **Rerun-proof ingest.** Step 0 canonicalizes the body, hashes it, and exits on match — no writes, no log entry, no cost.
2. **Detector-only changelog monitor.** Stored `source_hash:` is read and compared; only Slack is written. `!! ingest` is the sole wiki writer.
3. **Single canonicalization pipeline.** `ops/ingest.md` §Hash Canonicalization defines a deterministic 6-step pipeline used by both ingest Step 0 and monitor Step 3.
4. **Derived `Pages: N`.** As of v2.0.3, `refresh-hot.md` counts `^- \[\[` entry lines rather than reading a stored Stats header — eliminating the prior-audit W1 maintenance gap.
5. **Blueprint-authoring Mode.** No `wiki/` at working-folder root ⇒ skip `wiki/log.md` append and `wiki/hot.md` refresh across all ops and Startup.
6. **Explicit versioning split.** Patch bumps (`X.Y.Z`) add only a CHANGELOG section; `X.Y` bumps propagate to the CLAUDE.md footer and `hot.md`'s `Schema:` field.

This pass focuses on three load-bearing state-machine questions that prior audits did not directly examine: (a) atomicity of the ingest write sequence in Steps 5–10, (b) consistency of the raw-file timestamp across Steps 5 and 9, and (c) internal cross-references within `setup-guide.md` that were edited across v2.0.1–v2.0.3.

---

## 2. Findings

### CRITICAL

**C1. `setup-guide.md` Step 3 forwards to Step 8 for a callout that Step 8 no longer surfaces (dead cross-reference).**

`setup-guide.md:92`:

> If the scheduled-tasks MCP is not yet configured to run `changelog-monitor.md` on a daily cadence, surface this in the Step 8 readiness announcement — the file is in place but nothing is scheduling it until the user registers it.

Step 8 (`setup-guide.md:246–263`) reads in full:

> "Setup complete. Your wiki is ready.
>
> **Next step:** Clip an article with Obsidian Web Clipper — it will save to `wiki/inbox/`. Then tell me: `!! ingest [filename]`
>
> For daily usage, see `blueprint/user-guide.md`."
>
> Then display the standard footer: [footer block]

There is no mention of the changelog-monitor scheduling status. A setup-time agent following Step 3 literally will look for a hook in Step 8, find none, and either (i) inject unscheduled prose ad-hoc (drift), (ii) skip it silently (users don't learn the task isn't running), or (iii) surface it in a non-canonical location (inconsistent across setups).

**Logical failure:** Step 3 promises a downstream surfacing that Step 8 does not provide. One of the two steps is wrong — either Step 3's instruction should be dropped (or moved), or Step 8 should include a conditional "If the scheduled-tasks MCP was not configured to run `changelog-monitor.md`, say: '⚠️  `changelog-monitor.md` is in place but nothing is scheduling it — register its 2-line prompt in your Cowork scheduled-tasks MCP to activate the daily fetch.'" line.

**Severity:** CRITICAL — this is a concrete contradiction between two steps in a load-bearing operator-facing document. The blueprint distribution ships the changelog monitor as a user-visible feature (README Key Features, user-guide Daily Workflow), and the setup flow needs to tell users whether it is actually scheduled. Silent omission in the readiness announcement is the kind of footgun `!! audit` exists to catch.

**Suggested remediation (not applied — read-only audit):**

Add the conditional line to Step 8, keeping Step 3's instruction intact. Example body:

```markdown
(Optional — only if the scheduled-tasks MCP is NOT yet configured for `changelog-monitor.md`:)
> "⚠️  `scheduled-tasks/changelog-monitor.md` is in place, but nothing is scheduling it yet. To activate the daily fetch, register its 2-line invocation prompt in your Cowork scheduled-tasks MCP — see the file's §Invocation section for the exact prompt."
```

Alternative (smaller footprint): drop the "surface this in the Step 8 readiness announcement" clause from Step 3 entirely, on the theory that the scheduler-registration step belongs in `user-guide.md`'s "Scheduling the task" paragraph (`user-guide.md:130`) and doesn't need a setup-time announcement. Trade-off: users who never read `user-guide.md` carefully may leave the monitor indefinitely unscheduled.

Blueprint Sync Rule rows triggered: "Setup step change" (touches `setup-guide.md` only).

---

**C2. `ops/ingest.md` Steps 5 and 9 do not share a pre-computed timestamp — the raw-file naming invariant is implicit.**

Step 5 (`ops/ingest.md:70`) writes (or regenerates) the source page, which per `conventions.md:33–34` MUST include `original_file:` pointing to `raw/<slug>-<YYYY-MM-DD-HHMMSS>.md`. Per `conventions.md:54` the `## Key Takeaways` footnote citations also use the timestamped filename: `[^1]: raw/claude-code-overview-2026-04-18-091532.md — fetched 2026-04-18`.

Step 9 (`ops/ingest.md:75–83`) computes the timestamp at move time:

```bash
ts=$(date +%Y-%m-%d-%H%M%S)
dest="raw/${slug}-${ts}.md"
mv "$file" "$dest"
```

Nothing in Step 5, Step 9, or the preamble instructs the agent to pre-compute `ts` once and reuse it across both steps. A literal agent running step-by-step will:

1. At Step 5, decide what to write for `original_file:` and the footnote timestamp — the op does not specify. Options: (i) fabricate a timestamp at Step-5-write time; (ii) use a placeholder like `raw/<slug>-<pending>.md`; (iii) read the agent's best guess of "now." None are specified.
2. At Step 9, compute a fresh `ts`. The bash snippet's `date +%Y-%m-%d-%H%M%S` is guaranteed to differ from (i) by some number of seconds, and can't match (ii) at all.

**Concrete logical failure:** Under any scenario except an agent that silently pre-computes and threads `ts` (behavior the op does not mandate), the source page's `original_file:` and its `[^n]:` footnote timestamps will drift from the actual `raw/<slug>-<ts>.md` filename produced by Step 9. The footnote trail the conventions call "provenance" is broken on the first ingest of every source.

**Evidence:** `ops/ingest.md:84` — "`WORKDIR`, `file`, and `slug` must all be exported in the **same** Bash invocation as the snippet" — the preamble threads three variables, but notably not `ts`. The omission suggests `ts` was treated as a local variable to Step 9 only.

**Severity:** CRITICAL — this breaks the provenance-footnote guarantee described in `user-guide.md:43`: "Source pages now cite their raw snapshot on every curated bullet in Key Takeaways — `[^1]: raw/<filename> — fetched YYYY-MM-DD`." It also weakens the `original_file:` frontmatter contract in `conventions.md`. The defect is silent — Obsidian renders the footnotes as dead links, and the `raw/` archive still exists, just at a slightly-different filename, so the user doesn't see an error.

**Suggested remediation (not applied):**

Add a new step between the current Steps 4 and 5 (or as a sub-bullet at the top of Step 5):

> **Step 4.5 — Pre-compute `ts`.** Generate `ts=$(date +%Y-%m-%d-%H%M%S)` once for this ingest. Use the same `ts` value for the `original_file:` frontmatter and all `[^n]:` footnotes in Step 5, and for the `mv` destination in Step 9. Export `ts` alongside `WORKDIR`, `file`, and `slug` in every Bash invocation.

Also update Step 9's bash snippet to NOT re-compute `ts`:

```bash
cd "${WORKDIR:?…}"
: "${file:?…}"
: "${slug:?…}"
: "${ts:?ts must be pre-computed in Step 4.5 and exported for this Bash invocation}"
[ -e "$file" ] || { echo "source not found: $file"; exit 1; }
dest="raw/${slug}-${ts}.md"
mv "$file" "$dest"
```

Blueprint Sync Rule rows triggered: "Operation step change" (`ops/ingest.md`), "File-size or cost change" if the delta exceeds the `token-reference.md` headroom (measured 11,207 → ~11,400 estimated, still inside the 12,300 bound — no recalibration needed).

---

**C3. Partial failure between Steps 5 and 9 defeats the rerun-proof guarantee and can silently delete the inbox file without writing a raw snapshot.**

**Intended behavior:** `user-guide.md:41`, `CHANGELOG.md:147`, and `ops/ingest.md:96` all assert "Rerun-proof guarantee: Same input → zero state change. Re-running any ingest (manually or from a scheduled task) is safe by design." Step 0's hash check is the enforcement mechanism.

**Actual behavior on partial failure:** Consider the sequence Step 5 (write source page with `source_hash:`) → Steps 6–8 (update pages, index) → Step 9 (move inbox file to `raw/`) → Step 10 (log append). If Step 9 fails — `mv` rejected by permissions, disk full, process killed, SIGINT between Steps 5 and 9, etc. — the source page exists with the new `source_hash:` but the inbox file is still in `wiki/inbox/` and no `raw/<slug>-<ts>.md` exists.

On retry:

- `ops/ingest.md:63` Step 0 reads `wiki/pages/sources/<slug>.md`, finds the stored `source_hash:` matching the canonicalized inbox body.
- `ops/ingest.md:64` — "**If stored `source_hash:` matches the computed hash:** delete the inbox file (if present), print `No change since last ingest — skipped.`, and exit cleanly."
- The inbox file is **deleted**, not moved. No raw snapshot ever lands. The source page's `original_file:` frontmatter and footnotes reference a `raw/<slug>-<ts>.md` that does not and will never exist.

**Logical failure:** Step 0's short-circuit treats `source_hash:` presence as proof that a prior ingest ran to completion. It isn't. `source_hash:` is committed at Step 5, but "ran to completion" means Steps 5 through 10 all succeeded. A Step-5-succeeded-but-Step-9-failed state is indistinguishable from a Step-5-through-10-succeeded state by hash-check alone.

The same argument applies if Step 10 (log append) is the step that fails: on retry, hash matches, inbox is deleted, log never gets the ingest entry. The wiki's audit trail has a silent gap for that source.

**Evidence the op recognized partial-failure risk but only for Step 5:**

`ops/ingest.md:74` — "**Ordering matters:** Step 5's source-page write (with the new `source_hash:`) MUST complete before this move. If Step 5 fails, the inbox file stays in `wiki/inbox/` and retry is clean — no orphan raw files with mismatched page state."

The op explicitly reasons about "Step 5 failing" but stops there. Steps 6, 7, 8, 9, 10 failing are not considered, and each leaves the system in a "hash-matches-but-ingest-did-not-complete" state that Step 0 cannot detect.

**Severity:** CRITICAL — this is the exact failure mode the rerun-proof guarantee was introduced to eliminate, re-introduced through an incomplete atomicity argument. Single-user, happy-path runs are unaffected; any real-world interruption (network timeout during an URL ingest's Step 5 write, sandbox termination, user Ctrl-C) breaks the invariant silently. The inbox-file deletion on retry is the data-loss surface.

**Suggested remediation (not applied — two viable paths, trade-offs shown):**

- **(a) Extend Step 0's match branch with a raw-file existence check.** After computing the hash and confirming it matches the stored `source_hash:`, also resolve the source page's `original_file:` frontmatter and verify the raw file exists on disk. If present → genuine no-op, delete inbox file as before, exit. If absent → treat as incomplete prior ingest, fall through to the mismatch branch (Steps 1–12) so Step 9 finally writes the raw snapshot. Trade-off: one extra file-stat per ingest (negligible); adds a second invariant (`source_hash` matches + raw file exists) that future ops must preserve; documentation touches Step 0 and possibly `conventions.md`'s `original_file:` section.

- **(b) Reorder: move the raw file before writing the source page.** New Step 4.5 pre-computes `ts` (see C2 remediation); new Step 4.6 moves `wiki/inbox/<file>` to `raw/<slug>-<ts>.md`; current Step 5 then writes the source page from the raw-file content. Step 9 is collapsed into 4.6. Now `source_hash:` is only committed after the raw file is physically in place. Trade-off: if Step 5 fails after 4.6, the raw file exists but the source page does not — Step 0's hash check would find no source page on retry and fall through to mismatch, which correctly re-regenerates the page; the only cost is a leftover raw file with no immediate backing page (inspectable but harmless). This path also cleanly subsumes C2.

Recommend **(b)** — it subsumes C2, removes a cross-step invariant, and the leftover-raw-file failure mode is strictly less bad than the inbox-deletion failure mode it replaces. The documentation delta is larger but the state machine shrinks.

Blueprint Sync Rule rows triggered: "Operation step change" (`ops/ingest.md`, `template/CLAUDE.md` Ops File Reminder if Step numbers shift), "New known issue or fix" (`troubleshooting.md` should document the prior failure mode and the v-next fix), "Schema change that introduces a new footgun" is arguably not hit since this is a bug fix, not a new footgun — the old footgun was the unwritten rule. Judgment call: add a `troubleshooting.md` entry titled e.g. "Ingest failed mid-flight and retry silently deleted the inbox file" describing the v<pre-fix> behavior and the v<post-fix> fix, regardless of the remediation path chosen.

---

### WARNING

**W1. `ops/audit.md:71` token envelope (~20,000–25,000) is materially lower than the actual summed read cost (~33,000 tokens).**

Actual file sizes (from `wc -c` via `ls -la` on the current tree):

| File | Chars | Tokens (÷4) |
|---|---:|---:|
| `README.md` | 4,600 | 1,150 |
| `setup-guide.md` | 11,000 | 2,750 |
| `user-guide.md` | 15,000 | 3,750 |
| `troubleshooting.md` | 22,000 | 5,500 |
| `CHANGELOG.md` | 18,000 | 4,500 |
| `LICENSE` | 1,100 | 275 |
| `.gitignore` | 65 | 16 |
| `template/CLAUDE.md` | ~20,800 | ~5,200 |
| `refresh-hot.md` | 4,100 | 1,025 |
| `changelog-monitor.md` | 5,585 | 1,396 |
| `ops/ingest.md` | 11,207 | 2,802 |
| `ops/lint.md` | 2,500 | 625 |
| `ops/audit.md` | 5,765 | 1,441 |
| `ops/query.md` | 1,901 | 475 |
| `ops/update.md` | 1,305 | 326 |
| `ops/conventions.md` | 4,500 | 1,125 |
| `ops/token-reference.md` | 4,104 | 1,026 |
| **Total** | **~133,532** | **~33,380** |

`ops/audit.md:71` — "For `!! audit all`, expect ~20,000–25,000 tokens of reads." `user-guide.md:215` duplicates the figure.

If `CLAUDE.md` is cached from Startup (the common case), the residual audit-read cost is ~28,180 tokens — still above the 25,000 upper bound by ~13%. If it isn't cached, the full ~33,380 is ~33% above the upper bound.

**Evidence this was correct at one point:** prior audit `audit-report-2026-04-18-03.md:123–126` computed **~32,180** tokens for the in-scope reads at the time of that audit, already above the envelope, and noted "the envelope was written for a pure in-scope read; factoring in the growing audit-report corpus, the envelope may be slightly low and could benefit from an update on the next fix pass." The fix was not applied in v2.0.3.

**Consequence:** The "warn the user up front if the session is already close to context limits" directive at `ops/audit.md:71` is calibrated against the wrong number. A user at ~170k tokens who reads the envelope as "~25,000" and proceeds could exceed the 200k context window when the actual cost is closer to 33k. Low-risk in practice (most sessions aren't that close to the wall), but the envelope is the only quantitative guidance an operator has.

**Severity:** WARNING — factual drift in a documented figure that governs a user-facing warning. Not blocking, but cleanly fixable.

**Suggested remediation (not applied):** bump the envelope in `ops/audit.md:71` and `user-guide.md:215` to ~25,000–35,000, matching the summed read cost with the existing 10% headroom convention. The 5-token range width preserves its rough-estimate framing; the lower bound moves to the previously-stated upper bound so operator expectations under the old figure remain covered.

Blueprint Sync Rule rows triggered: "Operation step change" (`ops/audit.md`), and by the Blueprint Sync matrix row for user-visible token figures, also `user-guide.md`'s Token Awareness table.

---

**W2. `ops/token-reference.md` does not list `README.md`, `setup-guide.md`, `user-guide.md`, `troubleshooting.md`, `CHANGELOG.md`, or `LICENSE` — yet `!! audit all` reads all of them.**

`ops/token-reference.md:10` — "**Source of truth:** The Chars column below is the source of truth for file-read cost estimates. Any quoted cost in CLAUDE.md, README.md, user-guide.md, or setup-guide.md must be re-derivable from this table."

The table does not include the blueprint-top-level docs that `!! audit all` reads. W1's envelope figure therefore cannot be re-derived from `token-reference.md` alone — the audit-scope files not tracked here sum to ~18,300 tokens (README + setup + user + trouble + CHANGELOG + LICENSE + .gitignore), which is more than half the audit's read cost.

**Severity:** WARNING — the "source of truth" claim is narrower than the audit-all read scope. Either the claim needs a scope caveat ("source of truth for ops-read costs, not blueprint-doc audit reads"), or the table should gain rows for the blueprint docs so the audit envelope is derivable.

**Suggested remediation (not applied):** add rows for the six audit-scope top-level files (README, setup-guide, user-guide, troubleshooting, CHANGELOG, LICENSE) to `ops/token-reference.md`. This also unlocks a mechanical re-derivation of the `!! audit all` envelope from the table — which, combined with the recalibration rule at `ops/token-reference.md:55`, would keep the envelope self-updating on future doc growth. `.gitignore` is trivially small; not worth a row.

Blueprint Sync Rule rows triggered: "File-size or cost change" (`ops/token-reference.md`).

---

**W3. `ops/ingest.md` Ingest Estimate Formula (`ops/token-reference.md:48–49`) predates Step 0 and does not account for the hash-check path.**

Formula as written:

> `raw source read + (500 × pages to create) + (200 × pages to update) + 500 overhead`

Actual pre-approval reads in a v2.0+ ingest include: `log.md` tail (~625 tokens), `wiki/index.md` (~200 tokens), the source page frontmatter lookup at Step 0 (~50 tokens amortized), and for `!! ingest all` the B3.5 batch-level pre-read of every inbox file (scales with inbox size). None are in the formula.

**Severity:** WARNING — the formula is documented as the source for token estimates in approval requests (`token-reference.md:10`). Estimates quoted from this formula will systematically undershoot actuals by ~750–1,000 tokens per single-file ingest and more for `!! ingest all`. Approval requests already layered onto this formula (e.g. via `ops/ingest.md:69` Step 4) inherit the undershoot.

**Suggested remediation (not applied):** rewrite the formula to reflect v2.0+ behavior:

> `log.md tail (~625) + index.md (~200) + raw source read + (500 × pages to create) + (200 × pages to update) + token-reference.md self-cost (~1,130, once per op) + 500 overhead`

Optional: add a separate `!! ingest all` row that includes the B3.5 batch-pre-read as `Σ(raw source reads across inbox)`.

Blueprint Sync Rule rows triggered: "File-size or cost change" (`ops/token-reference.md`). Downstream cascade to `CLAUDE.md`, `README.md`, `user-guide.md` is not triggered — the formula is an internal derivation, not a cited figure.

---

**W4. `template/CLAUDE.md` `!! ready` Step 5 says "surface any in-progress drafts from `drafts/`" without guarding for Blueprint-authoring Mode.**

`template/CLAUDE.md:241`:

> Confirm: "Memory cleared. Ready to work." Then surface any in-progress drafts from `drafts/` (same as normal startup Step 4) so resuming via `!! ready` never drops drafts that a non-`!! ready` startup would have announced.

But `template/CLAUDE.md:114` — "Startup in blueprint-authoring mode. … if `drafts/` is missing, skip step 3 (do not announce drafts)." — scopes the drafts-skip only to Startup step 3, not to the `!! ready` step 5 surfacing.

**Consequence:** In blueprint-authoring mode, a user who says `!! ready` (unusual but possible) triggers a probe of `drafts/` that will fail by `ls` exit code. A defensive agent will skip transparently; a literal agent will surface an error. The Blueprint-authoring Mode rule at line 112 ("skip every `wiki/log.md` append and `wiki/hot.md` refresh across all ops") governs wiki-state mutations but doesn't cover this read.

**Severity:** WARNING — low-likelihood in blueprint-authoring workspaces (nobody realistically says `!! ready` in an empty checkout), but a narrow contradiction between the Startup mode rule and the `!! ready` procedure. The failure mode is cosmetic (extra error line or skipped step), not data-destructive.

**Suggested remediation (not applied):** add a one-line guard in `!! ready` step 5 — "If `drafts/` is missing (blueprint-authoring mode), skip this surfacing." — or generalize the Blueprint-authoring Mode rule at line 112 to cover `drafts/` probes in addition to `wiki/` mutations.

Blueprint Sync Rule rows triggered: "Schema or startup change" if done via line-112 generalization; "Operation step change" if done as a per-step guard. Either way touches `template/CLAUDE.md` only.

---

## 3. Questions for Clarification

**Q1. Is the intra-line whitespace collapse in the Hash Canonicalization pipeline supposed to destroy code-block indentation?**

`ops/ingest.md:46` Hash Canonicalization Step 3 — "Collapse intra-line whitespace runs. Replace any run of spaces or tabs with a single space."

Markdown source bodies that contain code blocks, nested lists, or any semantically-significant indentation will have that indentation canonicalized to a single space. A page like:

```markdown
    def foo():
        return 1
```

canonicalizes to:

```
 def foo():
 return 1
```

— which hashes identically to a different page with the same text but a different indent. Two reasonable interpretations:

- **Intentional.** The canonicalizer's stated purpose (`ingest.md:53`) is to survive "Clipper-vs-WebFetch whitespace differences, CRLF/LF drift, trailing-whitespace jitter, and indentation-normalization differences." The last phrase — "indentation-normalization differences" — is the tell. If Clipper and WebFetch produce different indentation for the same underlying content, collapsing indentation is the fix. The comment "Do not lowercase, strip punctuation, or strip HTML tags … Case and punctuation are legitimate content signals" explicitly excludes indentation from the "legitimate signal" set.
- **Unintentional.** Code-block indentation is semantically meaningful; collapsing it makes the hash match pages that are demonstrably different in rendered form. If an ingested source is a programming article with code samples, two edits that change code-sample content but not the surrounding prose could hash identically if the prose is untouched and the code-block indentation is the only signal.

Filing as a clarification rather than a finding because the pipeline's author appears to have considered the trade-off and chosen collapse, but the doc does not explicitly defend the choice against the code-block-indentation case. A one-sentence note in `ops/ingest.md:51` like "Indentation — including semantically-meaningful code-block indentation — is intentionally normalized; content changes inside indented code blocks still modify the hash via their non-whitespace characters" would close the ambiguity either way.

---

**Q2. Prior audit Q1 (per-file schema footers) remains "Not applied" per `CHANGELOG.md:37–43` — carried forward, still open.**

No new information this pass. `changelog-monitor.md:93` still carries `*Schema: v2.0 | Created: 2026-04-18*`; `refresh-hot.md` and `ops/*.md` still carry none. The project direction question (add footers everywhere for parity vs. drop `changelog-monitor`'s for symmetry) remains undecided. Not re-raising as a finding — restating as Q2 only so this pass's open-questions list is complete.

---

## 4. Verdict

**Three CRITICAL findings landed this pass** — one dead cross-reference in `setup-guide.md` (C1), and two atomicity issues in `ops/ingest.md` (C2 timestamp threading, C3 partial-failure recovery) that are closely related and best remediated together via reordering (C3 option b subsumes C2). The ingest defects have been in the schema since v2.0 introduced timestamped `raw/` naming and the Step-0 hash check; they were not surfaced by prior audits because those audits focused on doc drift and hash-pipeline consistency, not ingest state-machine atomicity.

Four WARNINGs target token-estimate drift (W1, W3) and coverage gaps in the estimate source-of-truth (W2, W4 for a narrower startup-mode issue). All four are one-touch fixes touching at most two files.

Two questions for clarification (Q1 new, Q2 carried forward).

**Blueprint is sound at the architectural level.** The invariants — rerun-proof ingest by intent, detector/writer separation, single canonicalization pipeline, derived `Pages:` counter, Blueprint-authoring Mode, explicit versioning split — are all internally consistent. C2 and C3 are bugs in the ingest op's implementation of its own "rerun-proof" contract, not flaws in the contract itself; the contract is sound and the implementation can be brought into compliance with a small reorder.

**Token cost of this audit (estimated, chars ÷ 4):**

- In-scope reads: `README.md` (~1,150) + `setup-guide.md` (~2,750) + `user-guide.md` (~3,750) + `troubleshooting.md` (~5,500) + `CHANGELOG.md` (~4,500) + `LICENSE` (~275) + `.gitignore` (~16) + `template/CLAUDE.md` (~5,200) + `refresh-hot.md` (~1,025) + `changelog-monitor.md` (~1,396) + 7 ops files (~7,820) = **~33,380 input tokens**.
- Context reads: three prior audit reports (~6,000 tokens combined if cached in-session).
- Total ~33,000–39,000 input tokens — reinforcing W1.

**Recommended priority order if applying:**

1. **C3 option (b)** — reorder ingest Steps 4.5/4.6/5/9 so the raw file moves before the source page writes. Subsumes C2 (shared-`ts` problem disappears because the move-time `ts` is known before the page write). Fixes the data-loss failure mode. Largest doc delta (~3 step-text edits in `ops/ingest.md` plus a `troubleshooting.md` entry), highest impact.
2. **C1** — one-line addition to `setup-guide.md` Step 8, or one-clause removal from Step 3. Trivial.
3. **W3** — rewrite the Ingest Estimate Formula in `ops/token-reference.md` to reflect v2.0+ pre-approval reads. One-block edit.
4. **W1 + W2 together** — bump the `!! audit all` envelope and add blueprint-doc rows to `ops/token-reference.md` in the same pass so the envelope becomes mechanically re-derivable from the table going forward.
5. **W4** — one-line guard in `!! ready` step 5, or scope generalization at `template/CLAUDE.md:112`.
6. **Q1** — add a one-sentence note to `ops/ingest.md:51` defending the indentation-collapse choice explicitly, whichever way the project wants it documented.
7. **Q2** — still a judgment call for the project author.

Blueprint-authoring Mode detected (no `wiki/` at working-folder root) — `wiki/log.md` append and `wiki/hot.md` refresh skipped per `ops/audit.md` Step 5/6 guidance. Read-only audit; no writes applied; no approval flow invoked.
