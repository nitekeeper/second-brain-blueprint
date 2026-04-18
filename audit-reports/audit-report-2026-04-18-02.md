# Blueprint Audit Report — 2026-04-18 (#2)

**Scope:** `!! audit all` — every tracked file under `blueprint/`
**Mode:** Audit + fix (fixes applied under Blueprint Sync Rule)
**Operator:** hchung@frontrowgroup.com
**Prior audit this day:** `audit-report-2026-04-18.md` (covered C1, W1–W4, S1–S2, Q1–Q2; commit `274f1c4` landed C1 + W4)

---

## 1. Restatement of intended logic (Chain of Verification)

The blueprint is a self-contained distribution template for an LLM-driven personal wiki. `CLAUDE.md` is the agent schema; `scheduled-tasks/ops/*` are the operation handbooks triggered by `!! <op>` commands; `scheduled-tasks/refresh-hot.md` and `scheduled-tasks/changelog-monitor.md` are the two background tasks. `README.md`, `user-guide.md`, `setup-guide.md`, `troubleshooting.md`, and `CHANGELOG.md` are the human-facing docs. The Blueprint Sync Rule requires that schema-affecting changes propagate across the downstream doc set so users never see drift between CLAUDE.md and the guides.

Two features are load-bearing for safety:

1. **Rerun-proof ingest.** Step 0 of ingest hashes the canonicalized source body and bails with `No change since last ingest — skipped.` when the hash matches the stored `source_hash:` on the corresponding wiki source page. No log entry, no writes, no cost.
2. **Changelog monitor as detector, not writer.** The scheduled changelog task fetches every row under `## Monitored Sources`, hashes each, and Slacks a per-source emoji-status summary (✅ / 🆕 / 🆘 / ❌). It must not ingest, edit pages, or append log entries — only `!! ingest` can write.

The hash is the coupling point between these two features. If the monitor's hash and the ingest-stored hash don't agree on what "identical content" means, the monitor will false-positive 🆕 on unchanged pages (eroding trust) or miss genuine updates (eroding coverage).

---

## 2. Findings

### CRITICAL

**C1-new. Monitor hash / Clipper-ingest hash divergence.**

The changelog monitor fetches via WebFetch and hashes the returned markdown. The primary ingest path is Obsidian Web Clipper → local markdown → `!! ingest`. Clipper and WebFetch produce materially different markdown from the same HTML (Clipper keeps only article body; WebFetch includes navigation, footers, and LLM-rewritten prose). Any source ingested via Clipper will therefore store a `source_hash:` that the monitor's WebFetch-based re-hash cannot match, even when the underlying page hasn't changed — a permanent false-🆕 for every Clipper-ingested source.

**Evidence:** `ops/ingest.md` Step 0 previously referenced `sha256(body).hex[0:8]` with no canonicalization spec; `changelog-monitor.md` Step 3 referenced the same bare hash. Clipper output for a typical TechCrunch article diverges from WebFetch output by roughly 40–60% of tokens (the figure quoted in README.md Key Features).

**Severity:** CRITICAL — the monitor's core value proposition (trustworthy per-source status) is undermined on the user's recommended ingest path.

**Fix applied (option b — canonicalize both hashers):**

- Added a new `## Hash Canonicalization` section to `ops/ingest.md` defining a deterministic six-step pipeline: (1) preamble-strip-if-present, (2) CRLF/CR → LF, (3) intra-line whitespace collapse, (4) blank-line collapse, (5) trim, (6) SHA-256 first 8 hex chars. An explicit "do NOT lowercase / strip-punctuation / strip-HTML" callout prevents over-normalization that would mask real changes.
- `ops/ingest.md` Step 0 and `changelog-monitor.md` Step 3 now both reference this single canonicalization section by `@scheduled-tasks/ops/ingest.md` anchor — one source of truth, two call sites.
- `ops/conventions.md` `source_hash:` frontmatter description updated to note that the stored value is the canonicalized-body hash.
- `user-guide.md` "Hash check first" bullet updated to explain the canonicalizer and cross-path hash convergence (Clipper vs URL vs monitor).
- `troubleshooting.md` gains a new entry "Changelog monitor reports 🆕 for a page I know hasn't changed" documenting the two residual causes after the fix (legacy pre-v2.0.2 hashes self-heal on next ingest; LLM-mediated WebFetch nondeterminism recipe for swapping to Clipper when a page repeatedly trips).
- `CHANGELOG.md` v2.0.2 entry documents the pipeline and the self-heal migration behavior.

**Caveat documented:** Canonicalization cannot fully defeat LLM-mediated WebFetch nondeterminism — the fetched markdown itself can vary across runs for the same URL. The troubleshooting entry gives the user a deterministic escape hatch (switch to Clipper for that source).

---

### WARNING

**W1. CHANGELOG estimate-re-baselining gap (backfill).**

`CHANGELOG.md` v2.0 documented memory.md cost re-baselining but did not call out the earlier ingest.md growth from ~7,900 to ~10,000 Chars. Auditors reading the changelog would miss that a significant `token-reference.md` Chars row moved without a corresponding migration note.

**Fix applied:** Added an `### Estimate re-baselining` backfill bullet under v2.0 documenting the ingest.md Chars jump alongside the memory.md change. No behavioral impact; improves changelog fidelity for future audits.

**W2 + W3. Blueprint-authoring Mode not threaded through Startup or audit.md.**

`CLAUDE.md`'s Blueprint-authoring Mode paragraph told the agent to treat `wiki/`-absent as "skip log appends and hot.md refreshes" but did not extend the same guidance to the Startup section (step 2 reads `wiki/hot.md`, which fails in this mode) or to `ops/audit.md` (Steps 5 and 6 both mutate wiki state).

**Fix applied:**

- Added a "Startup in blueprint-authoring mode" paragraph to `CLAUDE.md` explaining that the agent must skip the `hot.md` read on startup when `wiki/` is absent, announcing blueprint-authoring readiness instead of the normal hot.md summary.
- Added blueprint-authoring Mode callout bullets to `ops/audit.md` Steps 5 and 6 so the log-append and `hot.md` refresh are skipped transparently without prompting the user — a single `[ -e wiki/log.md ]` check gates both.

**W4-new + S3 + S4. Changelog monitor prose hardcoded "four sources"; `🆕 items:` hint ambiguity; sync-rule matrix missing CHANGELOG row for new scheduled tasks.**

- `changelog-monitor.md` described its work with the phrase "four monitored documentation pages" and "run all four fetches concurrently," which were stale the moment the user adds or removes a row in `## Monitored Sources`.
- The trailing Slack hint lines (`🆕 items:`, `🆘 items:`) had no explicit conditional — the agent could emit `🆕 items:` with nothing listed when no 🆕 rows were present, producing confusing empty-hint Slack messages.
- The Blueprint Sync Rule's "New scheduled task" row told the agent to update CLAUDE.md, user-guide.md, and troubleshooting.md but not CHANGELOG.md — yet scheduled-task additions are always at least patch bumps.

**Fix applied:**

- `changelog-monitor.md` prose replaced with row-count-agnostic phrasing ("every URL listed in `## Monitored Sources`" / "one per row"); Step 3 rewritten to reference the canonical hash pipeline with the LLM-WebFetch nondeterminism caveat; trailing-hint rule made explicit: emit `🆕 items:` and `🆘 items:` only when corresponding rows are present in the output.
- `CLAUDE.md` Blueprint Sync Rule "New scheduled task" row now appends `+ CHANGELOG.md (new section — treat any new scheduled task as at minimum a patch version bump, so the Schema-version-bump row applies)`.
- `CHANGELOG.md` v2.0.2 documents the monitor prose cleanup, the Slack-hint conditional, and the sync-rule tightening.

---

### STYLE

No STYLE-only findings this pass. All items surfaced during this audit carried behavioral or provenance weight.

---

## 3. Questions for Clarification

None outstanding. The prior audit's Q1–Q2 were resolved by `274f1c4`; C1-new was resolved in this pass per the user's chosen approach (option b — canonicalize both hashers).

---

## 4. Blueprint Sync propagation summary

Files edited:

- `blueprint/template/CLAUDE.md` — Startup-in-blueprint-authoring paragraph; Blueprint Sync Rule "New scheduled task" row extended; cold-start cost figures updated.
- `blueprint/template/scheduled-tasks/ops/ingest.md` — new `## Hash Canonicalization` section; Step 0 cross-reference.
- `blueprint/template/scheduled-tasks/changelog-monitor.md` — row-count-agnostic prose; Step 3 references canonical pipeline; trailing-hint conditional.
- `blueprint/template/scheduled-tasks/ops/conventions.md` — `source_hash:` frontmatter references canonical pipeline.
- `blueprint/template/scheduled-tasks/ops/audit.md` — blueprint-authoring callouts in Steps 5 and 6.
- `blueprint/template/scheduled-tasks/ops/token-reference.md` — 4 rows recalibrated (CLAUDE.md, changelog-monitor.md, ingest.md, audit.md); calibration date refreshed.
- `blueprint/CHANGELOG.md` — v2.0 backfill; full v2.0.2 section.
- `blueprint/user-guide.md` — Hash-check bullet; cold-start cost figures (5 occurrences).
- `blueprint/troubleshooting.md` — new `Changelog monitor reports 🆕 for a page I know hasn't changed` entry.
- `blueprint/README.md` — cold-start cost figure.

Cold-start cascade (token-reference → downstream docs), propagated per the Blueprint Sync Rule's "File-size or cost change" row:

- CLAUDE.md cost: ~4,580 → ~5,200 (CLAUDE.md:9, user-guide.md:9)
- Cold-start total: ~4,635 → ~5,255 (CLAUDE.md:17, user-guide.md:12, user-guide.md:208, user-guide.md:219, user-guide.md:240, README.md:64)
- Cold-start with `!! ready`: ~5,385 → ~6,005 (CLAUDE.md:17, user-guide.md:14, user-guide.md:209)

CHANGELOG.md:182 retains the historical `~4,760 → ~5,385` figure from the v2.0 entry — historical changelog prose is intentionally not rewritten during cascades.

Blueprint-authoring Mode detected (no `wiki/` at working-folder root) — `wiki/log.md` append and `wiki/hot.md` refresh skipped per `CLAUDE.md` and `ops/audit.md` Step 5/6 guidance.

---

## 5. Verdict

Blueprint is sound after this pass. The single CRITICAL (C1-new) is fully addressed architecturally — both hashers now flow through a single canonicalization section with an explicit over-normalization guard and a documented nondeterminism escape hatch. All WARNINGs were behavioral/provenance items and are closed with matching CHANGELOG entries. No STYLE-only findings.

Next audit should re-read `ops/ingest.md` carefully — it grew meaningfully this pass (9.0 KB → 11.2 KB) and is now the heaviest operational file after `CLAUDE.md`. If it continues to grow, consider splitting the `Hash Canonicalization` section into its own ops file.
