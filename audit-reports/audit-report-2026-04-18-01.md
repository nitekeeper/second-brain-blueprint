# Blueprint Audit — `!! audit all`

**Date:** 2026-04-18
**Scope:** Every tracked file under `blueprint/` per `ops/audit.md` §"If `!! audit all`"
**Mode:** Read-only (no fixes applied)
**Auditor role:** Senior Software Architect — strict, objective, evidence-cited, severity-labeled

Files reviewed: `README.md`, `setup-guide.md`, `user-guide.md`, `troubleshooting.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore`, `template/CLAUDE.md`, `template/scheduled-tasks/refresh-hot.md`, and all seven ops files under `template/scheduled-tasks/ops/`.

---

## Chain of Verification — Intended System Logic

The blueprint is a distributable template for an LLM-maintained "second brain" wiki. Its core invariants are:

1. **Lean cold-start** — agent reads only `CLAUDE.md` + `wiki/hot.md` at session start (~4,635 tokens). Index, log, and ops files defer until an operation fires.
2. **Approval-gated writes** — every file create/edit/delete pauses with a plan + token estimate, *except* three documented exceptions (`!! wrap`, `!! ready`, `!! audit`).
3. **Idempotent ingest** — `source_hash:` frontmatter + content-hash pre-check means re-running `!! ingest` on unchanged content is a guaranteed no-op.
4. **Blueprint sync discipline** — schema/ops/conventions edits must propagate across a documented matrix of downstream docs; sync edits log under `sync | …`, audit-driven edits log under `audit | …` (exclusive).
5. **Blueprint-authoring mode** — if `wiki/` is absent at the root, skip all `wiki/log.md` appends and `wiki/hot.md` refreshes across every op.
6. **Token-reference as source of truth** — all quoted costs must be re-derivable from the table; recalibrate when any file's measured size exceeds its documented Chars value.

Measured against these invariants, I found one CRITICAL inconsistency, four WARNINGs, two STYLE notes, and two Questions for Clarification. The rest of the blueprint is internally tight.

---

## CRITICAL

### C1 — `changelog-monitor.md` is documented but does not exist

**Evidence:**

`CHANGELOG.md` v2.0 §"New file" (lines 24–25):

> **`scheduled-tasks/changelog-monitor.md` restored.** The original trigger for this migration. A daily scheduled task that fetches four monitored documentation pages, computes content hashes, compares against wiki state, and reports findings via Slack DM.

`troubleshooting.md` "Changelog monitor ran but nothing was ingested" (lines 259–267) documents its behavioral contract:

> In schema v2.0+, the changelog monitor is strictly read-only — it fetches the monitored pages, computes content hashes, compares against stored `source_hash:` values in the wiki, and posts findings to Slack.

**Reality:** `ls blueprint/template/scheduled-tasks/` returns only `ops/` and `refresh-hot.md`. `git log --all -- '**/changelog-monitor.md'` returns empty — the file has never existed in git history, on any branch.

**Failure:** v2.0 ships incomplete vs. its own changelog. A user following the CHANGELOG will look for the file and find nothing. A user hitting the troubleshooting symptom described in the "Changelog monitor ran but nothing was ingested" entry has, by that document's own logic, been running a task that does not exist — a self-contradictory state. Because `changelog-monitor.md` would be a new scheduled task, the Blueprint Sync Rule would also require at minimum a README mention and a user-guide entry; neither exists. The v2.0 delivery is partial.

**Fix options (require approval):**
- (a) Author the missing `blueprint/template/scheduled-tasks/changelog-monitor.md` to the spec implied by troubleshooting.md, and propagate per Blueprint Sync Rule to README/user-guide/setup-guide. OR
- (b) Strike the "New file" section from CHANGELOG v2.0 and the "Changelog monitor ran but nothing was ingested" entry from troubleshooting.md, document the feature as descoped, and land a subsequent version that introduces it properly.

---

## WARNING

### W1 — v2.0 CHANGELOG silently skips the `ops/ingest.md` re-baselining

**Evidence:**

CHANGELOG v1.14 §"Estimate re-baselining" (lines 50–53):

> `ops/ingest.md` recalibrated. File grew during v1.14 edits, leaving <2% headroom against documented Chars. Chars column bumped from ~7,300 → ~7,900; Tokens ~1,830 → ~1,980.

Current `token-reference.md` (line 24): `ops/ingest.md | ~10,000 | ~2,500`.

Measured: `wc -c` on `ops/ingest.md` returns **9,045 chars**. 110% = 9,950 → rounds to 10,000 per the recalibration rule. So the current 10,000/2,500 figure is *correct* — but CHANGELOG v2.0 has no "Estimate re-baselining" section documenting the 7,900 → 10,000 jump. That jump is the direct consequence of v2.0 adding Step 0 (hash check), B3.5, B3.6, and the `source_hash:` discipline to `ops/ingest.md`.

**Failure:** The token-reference.md header states "Source of truth: … Any quoted cost … must be re-derivable from this table — re-propagate when this table changes." The table was re-propagated, but the changelog record is missing the audit trail. An operator trying to reconstruct why a given version's cold-start estimate moved will find the trail stops at v1.14.

**Fix (requires approval):** Add an "Estimate re-baselining" section to CHANGELOG v2.0 documenting `ops/ingest.md`'s 7,900 → 10,000 char jump driven by the new hash-check + batch-check infrastructure.

---

### W2 — `ops/audit.md` steps 5–6 don't cross-reference Blueprint-authoring Mode

**Evidence:**

`ops/audit.md` step 5 (line 43) and step 6 (line 44), paraphrased: on applied fix, "Append one entry to `wiki/log.md`…" and "refresh `hot.md` — follow `@scheduled-tasks/refresh-hot.md`". No mention of the wiki-absent skip.

`CLAUDE.md` Blueprint-authoring Mode (line 109):

> This rule applies to Ingest, Lint, Update, filed Query, **Audit-with-fix**, `!! wrap`, and `!! ready`.

**Failure:** An agent in a blueprint-only checkout (no `wiki/`) who follows `ops/audit.md` literally after an approved fix will attempt to append to a nonexistent `wiki/log.md`. The rule *is* in CLAUDE.md, which is always read at session start, so the correctly-behaving agent will cache and apply it — but the op file is structurally out of step with the schema file. Every other op file that mutates `wiki/log.md` has the same omission, but `audit.md` is the most likely to run in blueprint-authoring mode (it's the op that makes sense to run on a blueprint-only clone).

**Fix (requires approval):** Add a one-line reminder at the top of `ops/audit.md` Steps section, or in step 5, pointing to CLAUDE.md's Blueprint-authoring Mode rule. Minimum-churn option: a `> **Blueprint-authoring mode:** if wiki/ is absent, skip steps 5 (log append) and 6 (hot.md refresh) — see CLAUDE.md.` callout.

---

### W3 — Startup step 2 is unconditional and will fail in blueprint-authoring mode

**Evidence:**

`CLAUDE.md` Startup (lines 9–13):

> 1. Read `CLAUDE.md` (this file) — ~4,580 tokens
> 2. Read `wiki/hot.md` — ~55 tokens
> 3. Check `drafts/`…

`CLAUDE.md` Blueprint-authoring Mode (line 109) only governs operational side-effects — "skip every `wiki/log.md` append and `wiki/hot.md` **refresh**". It is silent on `wiki/hot.md` **reads**, and on the directory probes in startup step 3.

**Failure:** A fresh blueprint-only clone has no `wiki/hot.md` and no `drafts/`. An agent following startup verbatim will encounter a missing-file error at step 2. A defensive reading (absent file → proceed with no hot.md summary) is not written down. This is the exact scenario the current session just exercised: `wiki/` is absent, and the agent has no canonical script for startup-in-blueprint-authoring-mode. The rule covers the commit side but not the startup side.

**Fix (requires approval):** Extend the Blueprint-authoring Mode section to explicitly cover startup: if `wiki/hot.md` is missing, skip step 2 and announce readiness from `CLAUDE.md` alone; if `drafts/` is missing, skip step 3. Optionally note that in this mode only `!! audit` is expected to run — other ops will fail on missing `wiki/` subpaths by design.

---

### W4 — `!! audit all` scope is brittle to additions at the `scheduled-tasks/` level

**Evidence:**

`ops/audit.md` "If `!! audit all`" list (lines 15–24) uses explicit enumeration for the `scheduled-tasks/` level:

> - `blueprint/template/scheduled-tasks/refresh-hot.md`
> - Every file under `blueprint/template/scheduled-tasks/ops/`

The `ops/` directory uses a glob ("Every file under") — robust. The `scheduled-tasks/` directory names exactly one file. If `changelog-monitor.md` (C1) is ever authored, or any other file lands at the `scheduled-tasks/` level, it will not be in audit scope unless `audit.md` itself is edited in the same change.

**Failure:** The brittleness is real and already bit v2.0 — if `changelog-monitor.md` had been authored as the CHANGELOG claims, audit-all would still skip it silently. A maintainer adding a file wouldn't get a warning; the audit would simply not cover it.

**Fix (requires approval):** Change the `refresh-hot.md` bullet to a glob ("Every file under `blueprint/template/scheduled-tasks/` directly, non-recursive — i.e. files in `scheduled-tasks/` but not inside `ops/`") or restructure the scope to "Every tracked file under `blueprint/` not in `.git/`". The latter is the most robust and matches the prose summary at line 13.

---

## STYLE

### S1 — `ops/ingest.md` Step 0 ordering for URL ingest is verbally ambiguous

**Evidence:**

`ops/ingest.md` U4 (line 13): "Step 0 (hash check) — runs on the in-memory content from U1."

`ops/ingest.md` Step 0 (line 42): "Strip any YAML preamble (e.g. the `source_url:` / `fetched:` block prepended in U3) — hash only the content body so the hash is stable across re-fetches of the same content."

U3 has not run when Step 0 fires per U4 ordering, so the preamble strip is a no-op for URL ingest. For filename ingest, the Clipper-saved inbox file may have its own preamble, so the strip matters there. This is internally consistent, but the prose reads as if the preamble might already be present from U3 at Step 0 time, which it isn't.

**Recommended prose tweak:** Reword Step 0 to "Strip any YAML preamble if present…" — "if present" disambiguates and covers both paths without implying U3 preceded Step 0 in the URL branch.

---

### S2 — `CHANGELOG.md` v1.12-and-earlier is implicit-by-cross-reference

**Evidence:**

`CHANGELOG.md` §"v1.12 and earlier" (lines 127–132):

> Version history prior to v1.13 is implicit in `troubleshooting.md` — each Prevention bullet references the version in which the corresponding fix landed (v1.10 mid-session guard, v1.11 `keep` option, v1.12 broadened approval scope and ingest batch pre-read, etc.).

This is an intentional tradeoff against double-writing version history. It works for readers already deep in the system. A new user tracing v1.10's arrival of the mid-session guard, or v1.12's batch pre-read, has to grep troubleshooting.md rather than read a dedicated section. Not a defect — a conscious brevity choice — but worth flagging if you ever plan to distribute the blueprint publicly, where the changelog is often a reader's first orientation.

**Recommended action:** None required. If you later want symmetry, backfill explicit v1.10 / v1.11 / v1.12 headings with one-line entries pointing into troubleshooting.md.

---

## Questions for Clarification

### Q1 — Was `changelog-monitor.md` descoped or deferred?

CHANGELOG v2.0's "New file" wording ("restored") implies prior existence. Git history shows none. Was the CHANGELOG entry written ahead of the file, with the file dropping off the v2.0 cut? Or did the file exist only in an ancestor project (e.g. an `llm-wiki/` repo hinted at in `.obsidian/workspace.json`'s `lastOpenFiles`)? The fix for C1 depends on whether the intent is to ship the file (option a) or document it as deferred (option b).

### Q2 — Does a new scheduled task trigger README / user-guide / setup-guide updates?

`CLAUDE.md`'s Blueprint Sync Rule table does not have an explicit row for "new scheduled task". The closest rows ("Schema or startup change", "Operation step change") don't quite match. If C1 is fixed by authoring `changelog-monitor.md`, should the sync rule table gain a "new scheduled task" row? Or is a scheduled task considered an "operation step change" for the purposes of sync? Documenting this explicitly would close the gap that caused C1 in the first place.

---

## Summary

| Severity | Count | Highlights |
|---|---|---|
| CRITICAL | 1 | Missing `changelog-monitor.md` vs. CHANGELOG + troubleshooting claims |
| WARNING | 4 | Changelog gap, audit.md / startup / scope brittleness vs. blueprint-authoring mode |
| STYLE | 2 | Step 0 prose; implicit pre-v1.13 history |
| Questions | 2 | Scope and path forward for C1 |

**Overall health:** the blueprint's core invariants — approval gating, hash-check idempotence, the `sync` / `audit` log label split, the footer-block discipline, the blueprint-sync table — are internally consistent and well-specified. The findings above cluster into one execution gap (C1) and a family of blueprint-authoring-mode blind spots (W2, W3, W4) that share a common root: the blueprint-authoring mode rule was added in v1.13 but hasn't yet been threaded through every op file and the startup sequence. Fixing the threading would close W2–W4 together.

No schema-logic contradictions. No approval-path leaks. No unreachable state-machine branches in the memory flow. Severity bar held high per the Audit Prompt.

---

*Audit produced by the `!! audit all` op per `blueprint/template/scheduled-tasks/ops/audit.md`. Read-only — no files modified. If you want any of the flagged items fixed, reply with which ones (by ID, e.g. "fix C1 via option b, W1, W2") and I'll return with a normal approval request covering the edits and their propagation per the Blueprint Sync Rule.*
