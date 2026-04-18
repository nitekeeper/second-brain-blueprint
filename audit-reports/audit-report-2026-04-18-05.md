# Blueprint Audit Report — 2026-04-18 (#5)

**Scope:** `!! audit all` — every tracked file under `blueprint/` per `ops/audit.md` §If `!! audit all`
**Mode:** Read-only (blueprint-authoring workspace — no `wiki/` present)
**Operator:** hchung@frontrowgroup.com
**Prior audits this day:**
- `audit-report-2026-04-18.md` — C1, W1–W4, S1–S2, Q1–Q2 (landed v2.0 / v2.0.1)
- `audit-report-2026-04-18-02.md` — C1-new (hash canonicalization), W1–W4 (landed v2.0.2)
- `audit-report-2026-04-18-03.md` — W1 (Pages counter), S1 (conventions.md headroom), S2 (versioning split), Q1 (footer asymmetry) — W1/S1/S2 landed v2.0.3; Q1 still open
- `audit-report-2026-04-18-04.md` — C1 (setup-guide dead cross-ref), C2 (ts threading), C3 (partial-failure data loss), W1–W4, Q1 (indent collapse), Q2 (carried) — all applied in v2.0.4 per CHANGELOG

---

## 1. Restatement of intended logic (Chain of Verification)

The blueprint is a self-contained template for an LLM-driven personal wiki. `template/CLAUDE.md` is the agent schema; `template/scheduled-tasks/ops/*` are operation handbooks invoked by `!! <op>` commands; `refresh-hot.md` and `changelog-monitor.md` are the two scheduled tasks. `README.md`, `user-guide.md`, `setup-guide.md`, `troubleshooting.md`, and `CHANGELOG.md` are human-facing docs. The Blueprint Sync Rule keeps these in lock-step.

Invariants carried from prior audits (all intended to be stable after v2.0.4):

1. **Rerun-proof ingest.** Step 0 canonicalizes the body, hashes it, exits on match — no writes, no log entry, no cost.
2. **Detector-only changelog monitor.** Stored `source_hash:` is read and compared; only Slack is written.
3. **Single canonicalization pipeline.** `ops/ingest.md` §Hash Canonicalization defines a deterministic 6-step pipeline used by both ingest Step 0 and monitor Step 3.
4. **Derived `Pages: N`.** `refresh-hot.md` counts `^- \[\[` entry lines rather than reading a stored Stats header.
5. **Blueprint-authoring Mode.** No `wiki/` at working-folder root ⇒ skip `wiki/log.md` append and `wiki/hot.md` refresh across all ops and Startup.
6. **Explicit versioning split.** Patch bumps (`X.Y.Z`) add only a CHANGELOG section; `X.Y` bumps propagate to the CLAUDE.md footer and `hot.md`'s `Schema:` field.
7. **Atomic ingest ordering (v2.0.4).** Pre-compute `ts` once (Step 5); move inbox→raw *before* the source-page write (Step 6 precedes Step 7). `source_hash:` is committed only after the raw file is physically in place.

This pass focuses on three angles prior audits didn't directly examine: (a) whether v2.0.4's reorder actually delivers the retry-continuity it claims in prose, (b) whether the envelope/recalibration discipline stabilized or drifted again after v2.0.4's edits, and (c) whether the doc-set has any residual vestigial instructions from the v2.0.1–v2.0.3 cleanup passes.

---

## 2. Findings

### CRITICAL

No CRITICAL findings. The architectural fixes from audits #1–#4 have held: the hash pipeline is singly-sourced, blueprint-authoring mode is threaded through Startup + audit + `!! ready`, the ingest reorder eliminates the silent-inbox-deletion data-loss path, and the versioning split is explicit. Severity bar held high per the Audit Prompt.

---

### WARNING

**W1. v2.0.4's prose overclaims the "clean retry" story after a Step 6 → Step 7 crash — the retry logic it describes is not implemented in `ops/ingest.md`.**

`CHANGELOG.md:28–31` (v2.0.4 entry):

> A mid-flight failure now either leaves the inbox file untouched (crash before Step 6 — clean retry from Step 0) or leaves the raw file in place with no source page yet (crash between Step 6 and 7 — **retry finds the pre-moved raw file and writes the source page against it**).

`troubleshooting.md:245` (Prevention paragraph for the "Ingest interrupted mid-flight…" entry) makes the same claim in slightly different words:

> **the source page write on retry will see the pre-moved raw file and behave correctly**

Walking the ingest op (`ops/ingest.md`) for a filename retry after a crash between Step 6 and Step 7:

- `ops/ingest.md:62` Step 0 — "Load the raw source body into working memory. For filename ingest: read `wiki/inbox/<file>`." The inbox file is gone (Step 6 moved it on the prior run). Step 0 cannot read a nonexistent file.
- No branch in Step 0 exists for "inbox missing, raw/<slug>-*.md present" — Step 0 proceeds directly to hashing what it just read, which is now nothing.
- Step 6 has a `[ -e "$file" ] || { echo "source not found"; exit 1; }` guard that also aborts if inbox is empty.

Walking a URL retry after the same crash:

- U1 re-fetches the URL, content back in memory.
- Step 0 compares against the source page's `source_hash:` — the source page doesn't exist (Step 7 never ran on the prior attempt), so mismatch, proceed.
- Step 5 pre-computes a **new** `ts` (Step 5 runs per-ingest, not per-source).
- Step 6 moves the newly-written inbox file to `raw/<slug>-<new-ts>.md`.
- The **old** `raw/<slug>-<old-ts>.md` from the first (crashed) run is left orphaned; the new source page's `original_file:` and footnotes reference the new filename. Nothing in the op looks for or reuses the pre-existing raw file.

**Logical failure:** The troubleshooting and CHANGELOG prose describe a recovery mechanism (retry detects the pre-moved raw file, reuses it, writes the source page against it) that the op does not implement. In practice:
- Filename retry after Step-6-crash fails at Step 0's read.
- URL retry succeeds but creates an orphan raw file — not "retry finds the pre-moved raw file."

**Severity:** WARNING (not CRITICAL). The data-loss fix v2.0.4 was really delivering (the inbox file is no longer silently deleted in the crash window — it lives on in `raw/`) is real. The overclaim is about retry continuity, not data preservation. But the doc-vs-code gap is the exact kind of drift `!! audit` exists to catch, and a user relying on the troubleshooting prose to understand the recovery path will be confused when the op behaves differently.

**Fix options (not applied — read-only audit):**

- **(a) Match the code to the prose.** Add a Step 0.5 branch: if the inbox file is missing AND a matching `raw/<slug>-*.md` exists AND no source page exists yet, adopt the existing raw file as `$dest`, derive `ts` from the filename, and jump directly to Step 7. This is the behavior the prose claims.
- **(b) Match the prose to the code.** Rewrite `CHANGELOG.md:29–31` and `troubleshooting.md:245` to describe actual v2.0.4 behavior: crash between Step 6 and Step 7 leaves the source intact in `raw/` (no data loss) but requires manual recovery on retry — either re-clip the article to trigger a fresh ingest (leaving an orphan raw file) or move the raw file back to `wiki/inbox/` under its original name.

Recommend **(b)** — the manual-recovery framing is accurate, cheap to document, and the orphan-raw-file outcome is strictly less bad than the prior silent-deletion failure mode. (a) buys a tighter retry story at the cost of a new branch that future audits would need to reason about.

Blueprint Sync Rule rows triggered: if (a), "Operation step change" (ops/ingest.md) + "New known issue or fix" (troubleshooting.md). If (b), just the CHANGELOG and troubleshooting prose — same row category under the Sync Rule.

---

**W2. `!! audit all` envelope was bumped to `25,000–35,000` tokens in v2.0.4 but post-v2.0.4 CHANGELOG/troubleshooting growth already pushes the summed cost back above the upper bound — the exact drift audit #4 W1 was meant to close.**

Measured file sizes on the current tree (from `wc -c`/`ls -la`):

| File | Chars | Tokens (÷4) |
|---|---:|---:|
| `README.md` | 4,644 | 1,161 |
| `setup-guide.md` | 11,549 | 2,887 |
| `user-guide.md` | 15,076 | 3,769 |
| `troubleshooting.md` | 24,568 | 6,142 |
| `CHANGELOG.md` | 25,002 | 6,251 |
| `LICENSE` | 1,067 | 267 |
| `.gitignore` | 65 | 16 |
| `template/CLAUDE.md` | 19,720 | 4,930 |
| `refresh-hot.md` | 3,966 | 992 |
| `changelog-monitor.md` | 5,585 | 1,396 |
| `ops/audit.md` | 5,944 | 1,486 |
| `ops/conventions.md` | 4,500 | 1,125 |
| `ops/ingest.md` | 13,212 | 3,303 |
| `ops/lint.md` | 2,243 | 561 |
| `ops/query.md` | 1,901 | 475 |
| `ops/token-reference.md` | 5,408 | 1,352 |
| `ops/update.md` | 1,305 | 326 |
| **Total** | **145,755** | **~36,440** |

`ops/audit.md:71` — "For `!! audit all`, expect ~25,000–35,000 tokens of reads."
`user-guide.md:215` — `Audit all (full blueprint) | ~25,000–35,000`.

Measured 36,440 is ~4% over the 35,000 upper bound. Not dramatic, but the envelope is already wrong — and it was set in v2.0.4 based on an audit #4 measurement of ~33,000. The delta between then and now is roughly CHANGELOG.md's v2.0.4 section (which itself documented the envelope bump) plus the new troubleshooting entry — i.e. the act of fixing W1 in audit #4 pushed the envelope back out of spec. `ops/audit.md:71` even anticipates this pattern ("Recalibrate this range by summing the blueprint-doc rows in `token-reference.md` whenever those rows move"), but nothing in the v2.0.4 applied-fix set re-summed after the new CHANGELOG prose landed.

**Severity:** WARNING — same category as audit #4 W1 (factual drift in a documented figure that governs the operator warning about context-window proximity). Low real-world impact; clean fix available.

**Fix (not applied):** Re-sum the blueprint-doc rows in `token-reference.md` against current measurements, bump the envelope to `~28,000–40,000` (or `~30,000–40,000` for rounded-nearest-5k), and note in `ops/audit.md:71` that the bump is derivable from the table. The recurring pattern suggests this envelope is structurally hard to stabilize via a hand-tuned range — a future pass could consider replacing the literal figure with a `see token-reference.md blueprint-doc rows` pointer, avoiding the recurrence entirely.

Blueprint Sync Rule rows triggered: "File-size or cost change" (`ops/audit.md`, `user-guide.md`).

---

**W3. `setup-guide.md` Step 3's scheduled-tasks-MCP detection has no documented mechanism.**

`setup-guide.md:92`:

> If the scheduled-tasks MCP is not yet configured to run `changelog-monitor.md` on a daily cadence, surface this in the Step 8 readiness announcement — the file is in place but nothing is scheduling it until the user registers it.

`setup-guide.md:254–256` (Step 8's conditional block — added in v2.0.4 to close audit #4 C1):

> **If Step 3 flagged that `changelog-monitor.md` is not yet on a daily scheduled-tasks cadence,** append this line to the readiness announcement … :
>
> > "One loose end: `scheduled-tasks/changelog-monitor.md` is in place but nothing is scheduling it yet. When you're ready to turn on daily changelog monitoring, register it…"

The Step 8 block correctly handles the flagged-vs-not-flagged branch — but Step 3 never says *how* the setup-time agent determines whether the MCP is configured. The agent running setup has three reasonable interpretations:

1. **Always flag.** Pessimistic: assume not configured, always surface the note. Safe but noisy for users who already wired it up.
2. **Ask the user.** Add an interactive step not documented in Step 3 or Step 8.
3. **Query the MCP.** Call `mcp__scheduled-tasks__list_scheduled_tasks` (or whatever the available tool name is) and check for a task running `changelog-monitor.md`. This is the right answer but the setup-guide does not mention the tool, does not say to call it, and the tool's availability isn't guaranteed across Cowork setups.

**Logical failure:** Step 3's conditional is unreachable in a well-defined way. Three different operators running setup will produce three different readiness announcements. Once v2.0.4 wired Step 8 to Step 3 (closing audit #4 C1), the underlying ambiguity at Step 3 became the new rate-limiting defect — the conditional flag has correct wiring but no correct source.

**Severity:** WARNING — not data-loss, but a documented operator-facing decision with no specified input. The Step 8 note is harmless if emitted unnecessarily (user just ignores it), so the likely real-world outcome is "always-emit" drift → always-noisy readiness announcement → users learn to ignore it → the flag loses its signal value.

**Fix (not applied):** Rewrite `setup-guide.md:90–92` to specify the detection mechanism explicitly. Suggested prose:

> **How to detect whether the MCP is already scheduling the task:** run the scheduled-tasks MCP's list tool (the exact call depends on your MCP registration; in Cowork the tool name is usually `list_scheduled_tasks` or equivalent) and look for a task whose prompt references `changelog-monitor.md`. If no such tool is available in the current Cowork session, ask the user directly: "Is the changelog-monitor scheduled task already registered? (yes/no)" and flag based on the answer.

Alternatively, simplify: unconditionally include the scheduler-registration note in Step 8 (drop the conditional) and trust the user to recognize "already done, ignore." That removes the detection problem entirely at the cost of a one-time noisy line for already-configured users.

Blueprint Sync Rule rows triggered: "Setup step change" (touches `setup-guide.md` only).

---

**W4. Blueprint Sync Rule's "New scheduled task" row mandates an `ops/audit.md` (scope) update that v2.0.1's scope generalization made unnecessary.**

`CLAUDE.md:100` ("New scheduled task" row):

> blueprint/template/scheduled-tasks/<name>.md + **`ops/audit.md` (scope)** + `ops/token-reference.md` (file-size row) + `setup-guide.md` … + `README.md` and `user-guide.md` if user-visible + `template/CLAUDE.md` Directory Structure + `CHANGELOG.md` …

`ops/audit.md:23` (current `!! audit all` scope):

> Every file directly under `blueprint/template/scheduled-tasks/` (currently `refresh-hot.md` and `changelog-monitor.md`; do not recurse into `ops/`)

This is the glob that v2.0.1 introduced to close audit #1 W4 (scope brittleness at the scheduled-tasks level). A new scheduled task at that level is automatically in audit scope — no `audit.md` edit required for coverage.

The sync-rule row predates the scope generalization. A literal future operator adding a new scheduled task will open `ops/audit.md`, look for a scope block to edit, and either (i) realize the glob already covers them and wonder why the sync row said to touch the file, or (ii) edit the parenthetical on line 23 — "(currently `refresh-hot.md` and `changelog-monitor.md`; …)" — which is the only piece of audit.md that would go stale on a new scheduled task. The parenthetical is informational, not load-bearing.

**Severity:** WARNING — the misdirection is small (one extra file opened, one parenthetical tweaked), but it reads as internal inconsistency to a careful operator. The whole point of the Sync Rule is to give them a precise checklist.

**Fix (not applied):** Rewrite the "ops/audit.md (scope)" token in the row. Two viable reframings:

- **(a) Be precise about what actually needs editing.** Replace `ops/audit.md (scope)` with `ops/audit.md (informational scope list on line 23, not the glob itself)` — accurate and signals that the rule is a doc-hygiene touch, not a behavioral one.
- **(b) Drop it.** If the operator wants to bring the parenthetical up-to-date they will; if not, the glob keeps them safe. Not everything needs to be in the matrix.

Recommend (a). The parenthetical is pedagogical value for future readers of `ops/audit.md`, and marking it as a sync responsibility keeps that value intact; dropping it entirely risks drift.

Blueprint Sync Rule rows triggered: "Any schema change" (CLAUDE.md).

---

### STYLE

**S1. `ops/ingest.md` Step 5's "generate once and hold in working memory" leaves the execution mechanism under-specified for a Cowork Bash environment.**

`ops/ingest.md:72` Step 5:

> **Pre-compute `ts` for this ingest.** Generate once — `ts=$(date +%Y-%m-%d-%H%M%S)` — and hold it in working memory for the rest of the op.

`ops/ingest.md:83` Step 6 preamble note:

> `WORKDIR`, `file`, `slug`, and `ts` must all be exported in the **same** Bash invocation as the snippet — env vars do not persist across Cowork Bash calls.

The two statements are internally consistent, but the mechanism for Step 5 itself is unstated. `ts=$(date +%Y-%m-%d-%H%M%S)` is a bash command — to "generate once" the agent either:

- Runs a Bash tool call to execute `date +%Y-%m-%d-%H%M%S`, captures the output into LLM working memory, then inlines the literal value as `export ts="..."` inside Step 6's Bash call. Or,
- Combines Steps 5 and 6 into a single Bash call where `ts=$(...)` is assigned locally and used in the same invocation.

Both work. Neither is written down. A strict literal reader of Step 5 might try to run `ts=$(date +%Y-%m-%d-%H%M%S)` in its own Bash call (treating Step 5 as a discrete bash step), then hit Step 6 expecting `$ts` to be set and be surprised when it isn't — the Step 6 preamble note even anticipates this failure mode but doesn't explain how Step 5 fills the gap.

**Severity:** STYLE — the Step 6 `${ts:?…}` guard catches the failure at runtime with a clear error, and the likely agent behaviors (inline the value, or combine the steps) both produce correct results. But the prose leaves the mechanism implicit where being explicit is cheap.

**Suggested prose (not applied):** extend Step 5 to say:

> Two acceptable implementations: (i) run `date +%Y-%m-%d-%H%M%S` in a standalone Bash call, capture the printed timestamp into LLM working memory, and inline it as `export ts="<captured-value>"` at the top of Step 6's Bash call; (ii) fold Steps 5 and 6 into a single Bash call that assigns `ts=$(date +%Y-%m-%d-%H%M%S)` before the `mv`. Either way, the `ts` value used by Step 6 MUST be the same value inlined into Step 7's `original_file:` frontmatter and all `[^n]:` footnotes.

---

**S2. Documented Chars headroom has drifted below 10% on three template-side rows in `ops/token-reference.md` — same pattern audit #3 S1 closed for `conventions.md`.**

`ops/token-reference.md:70` — "**Headroom convention:** Chars column is set to ~110% of measured actual at calibration time, rounded to nearest 100."

Measured vs. documented spot-check (current tree):

| File | Measured (chars) | Documented | Headroom | 110% target |
|---|---:|---:|---:|---:|
| `template/CLAUDE.md` | 19,720 | 20,800 | **5.5%** | 21,700 |
| `refresh-hot.md` | 3,966 | 4,100 | **3.4%** | 4,400 |
| `ops/audit.md` | 5,944 | 6,300 | **6.0%** | 6,500 |
| `ops/ingest.md` | 13,212 | 14,500 | 9.7% | 14,500 |
| `ops/token-reference.md` | 5,408 | 6,000 | 10.9% | 5,900 |
| `ops/conventions.md` | 4,500 | 5,000 | 11.1% | 4,950 |

All six blueprint-doc rows that were freshly added in v2.0.4 sit right at ~10% (calibrated on addition). The drift is specifically on template-side rows that *weren't* pre-emptively recalibrated during v2.0.4's touches — the same failure mode audit #3 S1 called out on `conventions.md` ("the recalibration trigger fires on exceedance, not drift; this pass reclaims the headroom pre-emptively so the next small edit doesn't force an unplanned recalibration").

**Severity:** STYLE — the Recalibration Rule at `ops/token-reference.md:72` is technically satisfied (no trigger event on any row, all measured < documented). The 10% convention is calibration-time, not continuous. But `refresh-hot.md` is 134 chars below its trigger (a single-paragraph edit exceeds that), `CLAUDE.md` is 1,080 chars below (any minor schema clarification trips it), and `ops/audit.md` is 356 chars below. The next routine edit to any of these will force a recalibration cascade — for `CLAUDE.md` specifically that cascade propagates to `README.md` and `user-guide.md`'s cold-start figures, which is non-trivial churn compared to the one-line token-reference update.

**Suggested remediation (not applied):** Bump the three drifted rows to their 110% targets (21,700 / 4,400 / 6,500) pre-emptively. Single-file edit on `ops/token-reference.md`; no downstream cascade triggered by these specific rows (CLAUDE.md's chars didn't actually change — only its documented ceiling did — and the `chars÷4` cold-start figure derived from the documented ceiling would move from `~5,200` to `~5,425`, a real cascade that *would* touch README.md / user-guide.md / CLAUDE.md itself). Decision trade-off: accept the cascade now on the agent's terms vs. let the next small edit trigger it involuntarily.

---

## 3. Questions for Clarification

**Q1. (Carried from audits #3 and #4.) Per-file schema footers — parity vs. symmetry.**

`changelog-monitor.md:93` still carries `*Schema: v2.0 | Created: 2026-04-18*`; `refresh-hot.md` and all `ops/*.md` files carry none. `CHANGELOG.md:141–145` explicitly marks this as "Not applied" in v2.0.3 because the intent direction is ambiguous. The question has not moved since audit #3 and I have no new signal to resolve it — still a judgment call for the project author (add footers everywhere for provenance parity, or drop `changelog-monitor.md`'s for symmetry). Noted here so the open-questions list is complete, not as a fresh finding.

---

## 4. Verdict

**Blueprint is architecturally sound.** Five audits deep, the load-bearing invariants — rerun-proof ingest by intent *and* implementation, detector/writer separation, single canonicalization pipeline, derived `Pages:` counter, blueprint-authoring mode threading, explicit versioning split, and post-v2.0.4 atomic ingest ordering — all hold. No CRITICAL findings; the v2.0.4 reorder closed the last real data-loss path.

Remaining surface is drift of the kind audits exist to catch: one prose-vs-code contradiction from the v2.0.4 fix (W1 — the retry story is oversold), one recurrence of the audit-envelope drift the v2.0.4 W1 fix thought it solved (W2 — the act of documenting the bump pushed the envelope back out), one setup-time ambiguity (W3 — MCP detection mechanism unspecified), one vestigial Sync Rule instruction (W4 — `ops/audit.md (scope)` row is a no-op after v2.0.1), plus STYLE-level tidying (S1 — Step 5 execution mechanism implicit, S2 — three token-reference rows sit below the 10% headroom convention).

**Token cost of this audit (measured, chars ÷ 4):**

- In-scope reads: `README.md` (~1,161) + `setup-guide.md` (~2,887) + `user-guide.md` (~3,769) + `troubleshooting.md` (~6,142) + `CHANGELOG.md` (~6,251) + `LICENSE` (~267) + `.gitignore` (~16) + `template/CLAUDE.md` (~4,930) + `refresh-hot.md` (~992) + `changelog-monitor.md` (~1,396) + 7 ops files (~8,628) = **~36,439 input tokens**.
- Context reads: four prior audit reports (~14,800 tokens combined if all cached in-session).
- Total ~36,000–51,000 input tokens this session — directly evidencing W2.

**Recommended priority order if applying:**

1. **W1 fix option (b)** — rewrite the CHANGELOG and troubleshooting prose to describe actual v2.0.4 behavior (manual recovery, accept orphan raw files). Doc-only edit, two files, ~200 chars. Highest clarity-per-token ratio.
2. **W2** — re-sum the blueprint-doc rows and bump the envelope in `ops/audit.md:71` and `user-guide.md:215`. Consider replacing the literal figure with a pointer to prevent the next recurrence.
3. **W3** — rewrite `setup-guide.md:90–92` to specify the MCP detection mechanism (or drop the conditional on Step 8 and unconditionally include the loose-end note).
4. **S2** — pre-emptively bump the three drifted rows in `ops/token-reference.md`; accept the CLAUDE.md cascade deliberately rather than by accident.
5. **W4** — tighten the "New scheduled task" row in `CLAUDE.md:100` to say what actually needs editing in `ops/audit.md`.
6. **S1** — extend `ops/ingest.md` Step 5 prose to specify the two acceptable execution mechanisms.
7. **Q1** — still a judgment call for the project author.

Blueprint-authoring Mode detected (no `wiki/` at working-folder root) — `wiki/log.md` append and `wiki/hot.md` refresh skipped per `ops/audit.md` Step 5/6 guidance. Read-only audit; no writes applied; no approval flow invoked.
