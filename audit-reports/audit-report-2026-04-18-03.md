# Blueprint Audit Report — 2026-04-18 (#3)

**Scope:** `!! audit all` — every tracked file under `blueprint/` per `ops/audit.md` §If `!! audit all`
**Mode:** Read-only (blueprint-authoring workspace — no `wiki/` present)
**Operator:** hchung@frontrowgroup.com
**Prior audits this day:**
- `audit-report-2026-04-18.md` — C1, W1–W4, S1–S2, Q1–Q2 (landed `274f1c4`)
- `audit-report-2026-04-18-02.md` — C1-new (hash canonicalization), W1–W4 (changelog backfill / blueprint-authoring threading / monitor prose / sync-rule CHANGELOG row)

---

## 1. Restatement of intended logic (Chain of Verification)

The blueprint ships a self-contained template for an LLM-driven personal wiki: `template/CLAUDE.md` is the agent schema; `template/scheduled-tasks/ops/*` are the operation handbooks for `!! <op>` commands; `refresh-hot.md` and `changelog-monitor.md` are the two scheduled tasks. `README.md`, `user-guide.md`, `setup-guide.md`, `troubleshooting.md`, and `CHANGELOG.md` are the human-facing docs. The Blueprint Sync Rule keeps these in lock-step so downstream doc drift doesn't leak to end users.

Three load-bearing invariants carry from the prior two audits:

1. **Rerun-proof ingest.** Step 0 hashes the canonicalized body and exits on a match — no writes, no log entry, no cost.
2. **Changelog monitor as detector-only.** The monitor reads stored `source_hash:` values and Slacks a per-source emoji status. `!! ingest` is the sole writer.
3. **Single canonicalization pipeline.** `ops/ingest.md` §Hash Canonicalization defines a deterministic 6-step pipeline (preamble-strip → CRLF/CR → LF → intra-line whitespace collapse → blank-line collapse → trim → SHA-256[0:8]). Both `ops/ingest.md` Step 0 and `changelog-monitor.md` Step 3 reference it, so Clipper / URL / monitor paths produce comparable hashes on identical underlying content.

Blueprint-authoring Mode (no `wiki/` at working-folder root) gates `log.md` append + `hot.md` refresh across every op and the Startup sequence. Approval Rule carves out three documented exceptions: `!! wrap`, `!! ready`, `!! audit` (read-only by default). All three are now consistent across `CLAUDE.md`, `user-guide.md`, and `README.md`.

This pass focuses on drift the first two audits couldn't detect because they were introducing the fixes that now define "consistent."

---

## 2. Findings

### CRITICAL

No CRITICAL findings. The C1 / C1-new issues closed by the first two audits are stable — the canonical hash pipeline is singly-sourced, the Blueprint-authoring Mode rule is threaded through Startup and `ops/audit.md`, and the `!! audit` exception text matches across all three doc tiers.

---

### WARNING

**W1. `**Stats:** N pages` counter in `wiki/index.md` has no documented maintainer.**

`scheduled-tasks/refresh-hot.md` fills the `Pages: N` field of `hot.md` by reading the Stats header line from `wiki/index.md`:

> `refresh-hot.md:9` — "Read `wiki/index.md` — get the current page count from the Stats header line."
> `refresh-hot.md:47` — `| `Pages: N` | Stats line in index.md |`

The Stats line is initialized by `setup-guide.md:111` at wiki-creation time:

> `**Stats:** 0 pages | Last updated: YYYY-MM-DD`

But no op file specifies who must bump the counter when pages are added or removed:

- `ops/ingest.md` Step 8 — "Update `wiki/index.md` with new and modified entries." (no mention of Stats)
- `ops/lint.md` Step 7 — "Apply approved fixes." (no mention of Stats)
- `ops/update.md` Step 7 — "If the change affects the index summary, update `wiki/index.md`." (no mention of Stats)
- `ops/query.md` filing flow Step 3 — "Write to `wiki/pages/analyses/`." (Step 4 appends to index.md but says nothing about Stats)

**Consequence:** A strict agent following the ops files literally will add entry rows to `index.md` without touching the Stats header. `refresh-hot.md` then reads the stale count and writes a stale `Pages: N` into `hot.md`. The first session after that reads a misleading orientation snapshot. Trust in `hot.md`'s orientation value erodes silently.

**Severity:** WARNING — the live wiki still works, but a documented load-bearing field in the orientation snapshot has no documented maintainer. The defect is a coverage gap in the spec, not a bug in any individual file.

**Suggested remediation directions (two viable, trade-offs shown; not applied — audit is read-only):**

- *(a) Make the counter derived, not stored.* Rewrite `refresh-hot.md:9` to derive the page count by counting `^- \[\[` entry lines across all sections instead of reading the Stats line. Benefit: eliminates a manual-maintenance invariant entirely. Cost: the Stats line in `index.md` becomes cosmetic / decorative (or is removed from the template), which is a small Blueprint Sync Rule change touching `setup-guide.md` and potentially `user-guide.md`'s wiki-structure prose.
- *(b) Make the counter explicitly op-maintained.* Add "bump `**Stats:** N pages`" as a sub-step to `ops/ingest.md` Step 8, `ops/lint.md` Step 7, `ops/update.md` Step 7, and `ops/query.md` filing Step 3 (plus deletion paths if any). Also add to `ops/conventions.md` under `## index.md Format`. Benefit: keeps the Stats line as visible human-readable metadata. Cost: four-site spec edit, one more invariant per write op for the agent to remember — ongoing maintenance burden higher than (a).

Recommend (a) — deriving is cheaper than documenting, and the Stats line's only reader is `refresh-hot.md`; there is no third-party consumer that requires a pre-materialized count.

---

### STYLE

**S1. `ops/conventions.md` headroom sits at 2.2%, well under the documented 10% convention.**

`wc -c blueprint/template/scheduled-tasks/ops/conventions.md` → **4,500 bytes**.
`token-reference.md:28` documents `~4,600`.

`token-reference.md:53` — "Headroom convention: Chars column is set to ~110% of measured actual at calibration time, rounded to nearest 100." For a measured 4,500, the target documented value is 4,950 → rounds to 5,000, not 4,600. Every other tracked file's documented value is within ±1 hundred of 110% of its measured size (spot-checked: `CLAUDE.md` 18,952 × 1.1 ≈ 20,800 ✓; `ingest.md` 11,207 × 1.1 ≈ 12,300 ✓; `changelog-monitor.md` 5,585 × 1.1 ≈ 6,100 ✓). `conventions.md` is the only outlier.

**Evidence of the cause:** `conventions.md` grew during v2.0.2 (the `source_hash:` doc expansion to reference §Hash Canonicalization, per CHANGELOG.md:45–48) but was not re-calibrated at that time — the recalibration trigger ("fires when actual *exceeds* documented") was not tripped because 4,500 is still under 4,600, so the bump was skipped.

**Severity:** STYLE — the recalibration rule is technically satisfied (no trigger event), and the headroom convention is a calibration-time target, not a continuous invariant. But the file is 100 bytes from tripping the trigger, which means the next minor edit to `conventions.md` forces an unplanned recalibration. Pre-emptively bumping to 5,000 during the next planned recalibration cycle removes this fragility.

**No fix applied** (read-only audit). If fixed, update only `token-reference.md:28`. The `conventions.md` row does not cascade to cold-start figures in `CLAUDE.md` / `README.md` / `user-guide.md` (those cascade only from `CLAUDE.md` and `memory.md` per current totals), so this is a single-line edit.

---

**S2. Schema-version split between CLAUDE.md footer (X.Y) and CHANGELOG.md headings (X.Y.Z) is implicit, not documented.**

`template/CLAUDE.md:290` footer — `*Schema version: 2.0 | Created: [created-date] | Updated: [updated-date]*`
`CHANGELOG.md:6` — `## v2.0.2 — 2026-04-18`

The footer format `X.Y` (two components) and the CHANGELOG format `X.Y.Z` (three components) are both live and both correct by current convention — patches bump only `CHANGELOG.md`, while major/minor bumps also rewrite the footer. The two v2.0.x patch entries (2.0.1, 2.0.2) have landed without touching the footer, consistent with this split.

**Evidence this is not documented:**

- `CLAUDE.md` Blueprint Sync Rule line 99 — `| Schema version bump | blueprint/CHANGELOG.md (new section documenting the version) …` — says nothing about when the CLAUDE.md footer itself should be bumped.
- `CLAUDE.md` Blueprint Sync Rule line 97 — `| Any schema change | blueprint/template/CLAUDE.md always |` — is about content edits, not about the version-number field specifically.
- `setup-guide.md:170` says to read `Schema version: X.Y` from the footer — confirming the two-component format is load-bearing during setup, but not stating that patches are excluded.

A reader comparing CLAUDE.md's footer (2.0) to the latest CHANGELOG heading (2.0.2) must infer from observation that patches live only in CHANGELOG. This is easy to get wrong when authoring a new change: a patch-level fix that "feels like" a CLAUDE.md schema change (e.g. today's v2.0.2 edits to Blueprint-authoring Mode) would plausibly trigger a footer bump under a literal reading of the Sync Rule.

**Severity:** STYLE — the system works today because a single operator is shepherding the changes by eye. For the blueprint to be self-documenting enough to hand to another operator, the split should be stated explicitly, not inferred.

**Suggested phrasing** (not applied): add a one-line note under the Blueprint Sync Rule "Schema version bump" row — something like "Patch-level bumps (X.Y.Z) update CHANGELOG.md only; the CLAUDE.md footer and hot.md `Schema:` field track X.Y and do not move on patches."

---

## 3. Questions for Clarification

**Q1. Should scheduled-task files carry their own per-file version line?**

`changelog-monitor.md:93` ends with `*Schema: v2.0 | Created: 2026-04-18*`. The file was authored in v2.0.1 (per CHANGELOG.md:72–77) and materially edited in v2.0.2 (CHANGELOG.md:33–38), but the footer's `Schema: v2.0` doesn't move because per S2's implicit convention the global schema version stays at 2.0 across patches.

`refresh-hot.md` has no footer at all. `ops/*.md` files have no footers.

This is consistent (`changelog-monitor.md` is the only file with a footer, and it tracks global schema version, which is static across patches) — but asymmetric. Either (i) all scheduled-task files should carry the same footer for provenance parity, or (ii) `changelog-monitor.md`'s footer should be dropped for symmetry. I am unsure which way the project wants to go — not clearly an error either way, so filing as a clarification rather than a finding.

---

## 4. Verdict

**Blueprint is sound.** Three audits deep, the CRITICAL-severity architecture (canonical hash pipeline, Blueprint-authoring Mode threading, approval-exception taxonomy, Sync Rule matrix) is stable. The remaining surface is WARNING-and-below drift of the kind audits exist to catch: a documentation gap around the Stats counter (W1), a near-trigger file-size row (S1), and one implicit versioning convention worth making explicit (S2). None block operation; each has a cheap, localized remediation.

**Token cost of this audit (estimated, chars ÷ 4):**
- In-scope reads: `README.md` (~1,160) + `setup-guide.md` (~2,760) + `user-guide.md` (~3,770) + `troubleshooting.md` (~5,470) + `CHANGELOG.md` (~3,890) + `LICENSE` (~270) + `.gitignore` (~15) + `template/CLAUDE.md` (~4,740) + `refresh-hot.md` (~940) + `changelog-monitor.md` (~1,400) + 7 ops files (~7,760) = **~32,180 input tokens**.
- Context reads: both prior audit reports (~3,640 tokens combined).
- Total ~35,820 input tokens — above the `~20,000–25,000` envelope in `ops/audit.md:71`. The envelope was written for a pure in-scope read; factoring in the growing audit-report corpus, the envelope may be slightly low and could benefit from an update on the next fix pass.

**If you want to apply any of the above, the recommended priority order is:**
1. W1 — fix option (a) (derive `Pages: N` from entry-line count in `refresh-hot.md`; drop the Stats line from the `setup-guide.md` index template or keep it as decorative with an explicit "not maintained by any op" comment). One real behavioral fix, two spec edits.
2. S2 — one-line clarification to the Blueprint Sync Rule. Near-zero cost, non-zero clarity gain for future operators.
3. S1 — one-line recalibration of `ops/conventions.md` row in `token-reference.md`. Defers the next recalibration cycle by a comfortable margin.

Blueprint-authoring Mode detected (no `wiki/` at working-folder root) — `wiki/log.md` append and `wiki/hot.md` refresh skipped per `ops/audit.md` Step 5/6 guidance. Read-only audit; no writes applied; no approval flow invoked.
