# Blueprint Audit Report — 2026-04-18 (#10 — final audit)

**Scope:** `!! audit all` — every tracked file under `/sessions/determined-quirky-planck/mnt/Library/blueprint/`
**Schema under audit:** v2.0.9
**Prior audits reviewed:** #1 through #9 (`audit-report-2026-04-18.md` → `audit-report-2026-04-18-09.md`)
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)
**Mode:** Blueprint-authoring (no `wiki/` present at working-folder root; log append and `hot.md` refresh skipped per `template/CLAUDE.md` Blueprint-authoring Mode)
**User note:** user explicitly framed this run as "the last audit."

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**

- `blueprint/README.md` (4,644 chars)
- `blueprint/setup-guide.md` (12,204 chars)
- `blueprint/user-guide.md` (15,076 chars)
- `blueprint/troubleshooting.md` (25,348 chars)
- `blueprint/CHANGELOG.md` (48,613 chars)
- `blueprint/LICENSE` (1,067 chars)

**Template**

- `blueprint/template/CLAUDE.md` (19,875 chars)
- `blueprint/template/scheduled-tasks/refresh-hot.md` (3,966 chars)
- `blueprint/template/scheduled-tasks/changelog-monitor.md` (5,542 chars)
- `blueprint/template/scheduled-tasks/ops/ingest.md` (14,247 chars)
- `blueprint/template/scheduled-tasks/ops/lint.md` (2,243 chars)
- `blueprint/template/scheduled-tasks/ops/query.md` (1,901 chars)
- `blueprint/template/scheduled-tasks/ops/update.md` (1,305 chars)
- `blueprint/template/scheduled-tasks/ops/conventions.md` (4,500 chars)
- `blueprint/template/scheduled-tasks/ops/audit.md` (6,511 chars)
- `blueprint/template/scheduled-tasks/ops/token-reference.md` (6,664 chars)

**Prior audit reports (catch-up context)**

- `audit-report-2026-04-18.md` through `audit-report-2026-04-18-09.md`

**Not in audit scope (ignored):** `blueprint/.gitignore` (65 chars; VCS-adjacent metadata, no logic content), `blueprint/.git/`, `blueprint/.DS_Store` variants.

### 1.2 Verification that audit-#9 fixes landed in v2.0.9

| Fix | Claim | Verified |
|---|---|---|
| S1 | `CHANGELOG.md` row recalibrated: `~51,500 / ~12,880` | ✓ `token-reference.md:35` |
| Q1 | Recalibration Rule amended with soft 3% headroom trigger | ✓ `token-reference.md:72` ("fire pre-emptively when any file's remaining headroom drops below ~3%") |
| Q2 | Envelope cushion floor (~2% of upper bound) codified in Step 5 | ✓ `token-reference.md:79` ("widen the envelope when the cushion … drops below ~2%") |
| Cascaded | Envelope widened from `~30,000–48,000` to `~30,000–50,000` | ✓ `ops/audit.md:71`, `user-guide.md:94`, `user-guide.md:215` |
| Cascaded | `token-reference.md` row self-recalibrated (v2.0.9 added ~370 chars of rule text) | ✓ row reads `~7,300 / ~1,830`; `CLAUDE.md:9`, `README.md`, `user-guide.md`, `setup-guide.md` self-cost quotes (~1,830) all consistent |
| Cascaded | `ops/audit.md` row recalibrated to `~7,200 / ~1,800` (v2.0.9 added rationale text) | ✓ `token-reference.md:29` |
| Documented | v2.0.9 CHANGELOG entry documents the recalibration, widen, and rule amendments | ✓ `CHANGELOG.md:45–88` |

All v2.0.9 fixes are correctly landed and cross-referenced.

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Chars column convention: ~110% of measured actual at calibration, rounded to nearest 100. Post-v2.0.9 the soft trigger fires at headroom < 3% of measured actual; hard trigger fires when measured ≥ documented.

| File | Measured | Doc. Chars | Doc. Tokens | Headroom | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,644 | 5,100 | 1,280 | 9.82% | ok |
| `setup-guide.md` | 12,204 | 13,400 | 3,350 | 9.80% | ok |
| `user-guide.md` | 15,076 | 16,600 | 4,150 | 10.11% | ok |
| `troubleshooting.md` | 25,348 | 27,900 | 6,980 | 10.07% | ok |
| `CHANGELOG.md` | 48,613 | 51,500 | 12,880 | 5.94% | ok (above 3%) |
| `LICENSE` | 1,067 | 1,200 | 300 | 12.47% | ok |
| `template/CLAUDE.md` | 19,875 | 21,900 | 5,475 | 10.19% | ok |
| `refresh-hot.md` | 3,966 | 4,400 | 1,100 | 10.94% | ok |
| `changelog-monitor.md` | 5,542 | 6,100 | 1,530 | 10.07% | ok |
| `ingest.md` | 14,247 | 15,500 | 3,880 | 8.79% | ok |
| `lint.md` | 2,243 | 2,500 | 630 | 11.46% | ok |
| `query.md` | 1,901 | 2,100 | 530 | 10.47% | ok |
| `update.md` | 1,305 | 1,400 | 350 | 7.28% | ok |
| `conventions.md` | 4,500 | 5,000 | 1,250 | 11.11% | ok |
| `ops/audit.md` | 6,511 | 7,200 | 1,800 | 10.58% | ok |
| `token-reference.md` | 6,664 | 7,300 | 1,830 | 9.55% | ok |

Neither the hard trigger (measured ≥ documented) nor the newly-codified soft trigger (headroom < 3%) has fired on any file. `CHANGELOG.md` at 5.94% is the closest to the soft threshold — nearly double the trigger value — so no flag. Down from 1.25% pre-v2.0.9, the recalibration landed exactly where the 110% convention targets it.

### 1.4 Envelope check (Recalibration Rule Step 5)

Re-summed from the documented Tokens column in `token-reference.md`:

Blueprint-doc rows:
`README (1,280) + setup-guide (3,350) + user-guide (4,150) + troubleshooting (6,980) + CHANGELOG (12,880) + LICENSE (300) = 28,940`

Template-side rows:
`CLAUDE (5,475) + refresh-hot (1,100) + changelog-monitor (1,530) + ingest (3,880) + lint (630) + query (530) + update (350) + conventions (1,250) + audit (1,800) + token-reference (1,830) = 18,375`

**Total = 47,315 tokens**, inside the documented `~30,000–50,000` envelope quoted at `ops/audit.md:71`, `user-guide.md:94`, and `user-guide.md:215`. Cushion = 50,000 − 47,315 = **2,685 tokens ≈ 5.37% of the upper bound** — above the newly-codified 2% cushion floor (~1,000 tokens on a 50,000 envelope). No envelope edit required.

The documented sum (47,315) matches the CHANGELOG v2.0.9 entry at `CHANGELOG.md:68` exactly — the cascade is arithmetically consistent.

### 1.5 Architectural invariants re-verified

| Invariant | Source | Status |
|---|---|---|
| Hash canonicalization pipeline (6 steps: preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]) | `ops/ingest.md` §Hash Canonicalization | ✓ intact |
| Rerun-proof ingest Step 0 (hash-first short-circuit; no state change on no-op) | `ops/ingest.md` §Step 0 | ✓ intact |
| Atomic ingest ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 write source page | `ops/ingest.md` Steps 5–7 | ✓ intact |
| Derived `Pages: N` counter (count `^- [[` lines; not stored) | `scheduled-tasks/refresh-hot.md` | ✓ intact |
| Detector-only changelog monitor (read-only; Slack DM sole side-effect) | `scheduled-tasks/changelog-monitor.md` | ✓ intact |
| Blueprint-authoring Mode guard (skip log append and `hot.md` refresh when `wiki/` absent) | `template/CLAUDE.md:110–114`; `ops/audit.md` step 5 | ✓ intact |
| Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only | `template/CLAUDE.md:102` | ✓ intact (v2.0.9 patch did not move the footer) |
| Three documented Approval-Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) | `template/CLAUDE.md:58–71` | ✓ intact |
| `token-reference.md` is source of truth; envelope at `ops/audit.md:71` derives from its Tokens column | `ops/audit.md:71`, `token-reference.md:10` | ✓ intact |
| B3 cache / per-file refresh ordering for `!! ingest all` (log tail cached; index re-read per file) | `ops/ingest.md` B3, B5 | ✓ intact |
| Blueprint Sync Rule (10-row matrix); audit-driven edits use `audit | …` log label | `template/CLAUDE.md` §Blueprint Sync Rule; `ops/audit.md` step 5 | ✓ intact |
| Recalibration Rule's hard trigger (measured ≥ documented) and soft trigger (headroom < 3%) | `token-reference.md:72` | ✓ intact (both present; soft codified in v2.0.9) |
| Envelope Step 5 widen rule + 2% cushion floor | `token-reference.md:79` | ✓ intact (cushion floor codified in v2.0.9) |

No architectural regressions detected.

### 1.6 Cross-reference sanity checks

- `CLAUDE.md:9` quotes `~5,475` for itself → matches `token-reference.md:18`. ✓
- `user-guide.md:14` cold-start quote `~6,280` = 5,475 (CLAUDE) + 55 (hot) + 750 (memory when full). ✓
- `user-guide.md:215–217` realistic `!! wrap` ~2,800 / `!! ready` ~2,825 match `token-reference.md:54`. ✓
- `token-reference.md:54` component reads (~1,100 refresh + ~200 index + ~625 log tail + ~750 memory + ~100 log append) sum to the documented realistic costs. ✓
- `ops/audit.md:71` envelope `~30,000–50,000` is consistent with re-derived 47,315 + cushion. ✓
- CHANGELOG v2.0.9 section documents all three audit-#9 follow-ons (S1/Q1/Q2 → recalibration + two rule amendments + envelope widen). ✓
- No dangling xrefs; all prior-audit cleanup remains in place (setup-guide dead xref from audit #4 C1; `ingest.md:64` dangling xref from audit #6 W3; `user-guide.md` realistic-cost stale figures from audit #8 W1). ✓
- Prior STYLE-level pre-emptive recalibration pattern (audits #5 S2, #7 W1, #8 S1, #9 S1) is now baked into the rule as the 3% soft trigger — future instances of the same drift class should be caught by the rule rather than by the audit layer.

---

## 2. Findings

### CRITICAL

None.

### WARNING

**W1 — `changelog-monitor.md` Step 1 slug lookup is under-specified pre-fetch and fragile against realistic ingest-time slug divergence.**

*Evidence (specific quotes).*

`blueprint/template/scheduled-tasks/changelog-monitor.md:24–27` (Step 1):

> 1. **Read the wiki's stored hashes.** For each monitored source:
>    - Look up the corresponding source page under `wiki/pages/sources/` (slug-matched — reuse the same slug derivation rules as `ops/ingest.md` Step 0).
>    - If the source page exists, read its `source_hash:` frontmatter into memory.
>    - If the source page does not exist, record the source as UNINGESTED and skip the hash lookup.

`blueprint/template/scheduled-tasks/ops/ingest.md:64` (the referenced Step 0 slug rule):

> - Derive the expected source-page slug (lowercase-hyphenated from the H1 or filename stem; for URL ingest reuse the U2 slug).

`blueprint/template/scheduled-tasks/ops/ingest.md:10` (U2 slug rule):

> U2. Derive a slug from the page title (lowercase-hyphenated); fall back to the URL's last path segment if the title is unusable.

*Logical failure.* The monitor's Step 1 executes **before** the fetch in Step 2, yet the slug-derivation rule it points to requires either an H1, a filename stem, or a page title — none of which are available to the monitor pre-fetch. The monitor only has two pre-fetch inputs: the URL and the `Source Title` column of the `## Monitored Sources` table. Neither is specified in Step 0's rule as a valid slug source. The instruction "reuse the same slug derivation rules" is therefore literally unexecutable in this call site.

In practice, a monitor implementation would have to silently improvise — either using the URL's last path segment or the `Source Title` column, lowercase-hyphenated. For the four currently-monitored sources this happens to produce a slug that matches the URL last-segment (e.g., `sp-api-release-notes`), which is *probably* what the ingest-time Clipper or URL-ingest path produced too. But that coincidence is not guaranteed: a URL-ingested page takes its slug from the fetched page title, which can differ from the URL last-segment (e.g., page title "Selling Partner API: Release Notes" → `selling-partner-api-release-notes` vs URL last-segment `sp-api-release-notes`). Clipper-ingested pages take their slug from filename or H1, again not necessarily equal to the URL last-segment.

*Impact.* When the monitor's computed slug diverges from the ingest-time slug:

1. **Silent misclassification.** The monitor reports 🆘 UNINGESTED for a source that is in fact ingested. No state corruption — the monitor is read-only — but the signal is wrong.
2. **Duplicate-page risk if the user acts on the false 🆘.** The Slack message tells the user to run `!! ingest <URL>` to bootstrap. Following that instruction would create a **second** source page under the monitor's computed slug, while the original page persists under the ingest-time slug. Result: a silently-duplicated source that `!! lint` would eventually flag, but only after the duplicate has been threaded into the concept/entity graph.
3. **Latent, not manifest.** The current four monitored URLs happen to have URL last-segments that match ingest-time slug conventions, so the bug is not observably triggered in production. But the *specification* gap is real and will bite the next time a source is added whose fetched title doesn't round-trip through `lowercase-hyphenated` to equal the URL's last segment.

This is a bona-fide specification defect, not a style nitpick: the instruction references a rule that has no valid inputs at the call site.

*Recommended fix (two complementary edits).*

**Edit 1 — make `source_url:` a mandatory frontmatter field on every source page.**

- `ops/ingest.md` Step 7 currently requires `source_hash:` and `original_file:` but not `source_url:`. U3 prepends `source_url:` only for URL ingest. Clipper ingest may or may not preserve the URL from the Clipper's own preamble.
- Amend Step 7 (and the Notes bullet at line 100) to require `source_url:` on every source page. For Clipper-sourced files: pull the URL from the Clipper preamble if present; otherwise fall back to a `source_url: unknown` placeholder and emit a warning — the user can fix it post-ingest.
- This gives the monitor a reliable, **exact** join key independent of slug derivation.

**Edit 2 — rewrite `changelog-monitor.md` Step 1 as a `source_url:` reverse-lookup.**

- Replace the slug-matched instruction with: *"For each monitored source: enumerate `wiki/pages/sources/*.md`, read each file's `source_url:` frontmatter, and find the file whose `source_url:` equals the monitored URL. If exactly one match is found, read its `source_hash:`. If no match, record UNINGESTED. If more than one match, record AMBIGUOUS and continue (this should not occur absent wiki corruption, but failing loudly here is cheaper than silent miscomparison)."*
- Remove the cross-reference to `ops/ingest.md` Step 0 slug rules — that rule never made sense pre-fetch.
- Optionally cache the URL → slug map once per monitor run to avoid re-reading every source page for every monitored URL, but with only four monitored sources this is premature optimization.

**Blueprint Sync Rule cascade for these edits.** Applying them would touch: `ops/ingest.md` Step 7 and Notes; `changelog-monitor.md` Step 1; `troubleshooting.md` (new entry covering the AMBIGUOUS case); `CHANGELOG.md` (v2.0.10 entry documenting the invariant change). Token-reference recalibration would fire on `ingest.md` and `changelog-monitor.md` if the edits push either file past its documented Chars; based on the current 8.79% and 10.07% headroom, the edits should fit with room to spare.

*Severity rationale.* WARNING rather than CRITICAL because:
- The monitor is read-only — no data corruption can result directly.
- The failure mode is latent (doesn't fire on current monitored URLs).
- The downstream duplicate-page scenario requires the user to act on a false 🆘, which is recoverable.

But not STYLE because:
- The specification references a rule with no valid inputs at the call site — the instruction is literally unexecutable as written.
- It is an architectural gap that will bite on the next source addition with a non-trivial title.

### STYLE

None.

---

## 3. Non-findings (considered and dismissed)

- **`CHANGELOG.md` at 5.94% headroom** — nearly double the 3% soft trigger. Fresh off its v2.0.9 recalibration from 1.25% to this level, so no drift concern. Will routinely grow again; next hard/soft trigger fires on schedule.
- **`update.md` at 7.28% headroom** — below the 10% calibration target but well above the 3% soft trigger. File has not been edited recently; no drift pressure.
- **`ingest.md` at 8.79% headroom** — similar story. Inside rounding-tolerance of the 110% convention.
- **Headroom inhomogeneity across files (7.28% to 12.47%)** — an artifact of rounding documented Chars to the nearest 100 at different file sizes (small files like `LICENSE` have larger rounding cushion). Not a bug; the convention is explicit about nearest-100 rounding.
- **Envelope cushion dropped from 5.37% to … nothing yet** — the v2.0.9 widen gave the envelope a healthy cushion. Next cushion-floor trigger (2%) won't fire until the documented sum reaches ~49,000 tokens.
- **Three consecutive patches (v2.0.7, v2.0.8, v2.0.9) all recalibrated `CHANGELOG.md`'s drift class** — but v2.0.9 codified the soft 3% trigger precisely to stop this pattern from recurring as audit-driven findings. The rule now owns the detection.

---

## 4. Questions for Clarification

None. The written Recalibration Rule now codifies all three invariants that prior audits had been catching manually (hard trigger, soft 3% trigger, envelope 2% cushion floor). The audit layer should now be a quiet backstop rather than the primary driver of recalibration.

---

## 5. Architectural Invariants Verified

All invariants below were checked against the source files during this audit and remain intact:

1. Hash canonicalization is the 6-step pipeline (preamble-strip → CRLF-normalize → whitespace-collapse → blank-line-collapse → trim → SHA-256 first 8 chars). Consumers reference the single canonicalizer; no call site has reimplemented the pipeline inline.
2. Ingest is rerun-proof: Step 0 computes the canonical hash before any write and short-circuits if already indexed — no inbox file write, no approval request, no log entry, no `hot.md` refresh, no recalibration.
3. Ingest is atomic in the v2.0.4+ ordering: `ts` is pre-computed in Step 5, inbox→raw move happens in Step 6 **before** the source page is written in Step 7, and partial-failure recovery is the documented manual procedure in `troubleshooting.md`.
4. `Pages: N` is a derived counter (count of `^- [[` lines in the index), computed on demand by `refresh-hot.md`, never stored.
5. `changelog-monitor.md` is detector-only: it reads four upstream sources, compares hashes to stored `source_hash:` values, and DMs the user via Slack; it performs no `!! ingest`-style writes to the wiki. (W1 above is a specification gap in *how* the lookup is described, not a violation of the detector-only invariant itself.)
6. Blueprint-authoring Mode is respected consistently: `template/CLAUDE.md:110–114` documents the mode, and `ops/audit.md` step 5 explicitly skips the log append and `hot.md` refresh when `wiki/` is absent. This audit ran in that mode; no log entry or `hot.md` mutation was attempted.
7. Versioning discipline holds: `CLAUDE.md` footer and `hot.md` `Schema:` field carry `X.Y`; `CHANGELOG.md` alone carries `X.Y.Z`. The v2.0.9 patch correctly did not move the footer.
8. Approval Rule exceptions are enumerated identically in `template/CLAUDE.md` (lines 58, 68–71) and `README.md`; both list all three (`!! wrap`, `!! ready`, `!! audit`). No drift since audit #8.
9. `token-reference.md` remains the single source of truth for cost estimates. `ops/audit.md:71` and `user-guide.md:94,215` all quote `~30,000–50,000` derived from the Tokens column sum (47,315 + 2,685 cushion, rounded to nearest 1,000).
10. Approval-exception log entries use the generic `memory | …` shape; `!! wrap` and `!! ready` do not require a separate token-reference read per `token-reference.md:54`; `!! audit` uses the superseding `audit | …` label per `ops/audit.md` step 5 and `template/CLAUDE.md` Blueprint Sync Rule.
11. Recalibration Rule (v2.0.9) carries three triggers: hard (measured ≥ documented), soft (headroom < 3% of measured actual, codifying the pattern from audits #5, #7, #8, #9), and envelope cushion floor (cushion < 2% of upper bound). All three have precise, arithmetic, re-derivable conditions.
12. Blueprint Sync Rule (10-row matrix in `template/CLAUDE.md`) governs downstream propagation for every schema/startup/operation/conventions edit, and audit-driven edits use the superseding `audit | …` log label instead of a separate `sync | …` entry.

---

## 6. Verdict

**The v2.0.9 blueprint is sound with one latent specification gap.**

All audit-#9 fixes (S1 CHANGELOG.md recalibration, Q1 3% soft trigger, Q2 2% cushion floor) landed correctly and are arithmetically consistent across the token-reference table, the envelope quotes, and the CHANGELOG v2.0.9 entry. No architectural invariants have regressed. No dangling cross-references. All twelve checked invariants hold.

The single WARNING (W1) is a long-standing specification gap in `changelog-monitor.md` Step 1: the cross-reference to `ops/ingest.md` Step 0's slug-derivation rule is literally unexecutable because the monitor runs pre-fetch and has no access to H1, filename stem, or page title. The fix is two-part (make `source_url:` mandatory frontmatter; rewrite Step 1 as a URL reverse-lookup) and would cascade through the Blueprint Sync Rule.

No CRITICAL findings. No STYLE findings. No Questions for Clarification — the written rule now owns every detection the audit layer had been manually backstopping.

**Recommendation:** Land W1 as v2.0.10 the next time the ingest/monitor pair is touched anyway. The fix is mechanically straightforward (one new required frontmatter field; one rewritten Step 1) but touches enough downstream docs that batching with other monitor-related work would minimize churn. Until W1 lands, the monitor will continue to function correctly for the four current sources (URL last-segments happen to match ingest-time slugs for all of them) but should be viewed as slightly fragile against a fifth source whose fetched title diverges from its URL last-segment.

---

## 7. Closing — on "the last audit"

The user framed this as the final audit in the series. That framing is reasonable. Over ten audits across v2.0 → v2.0.9, the pattern of findings has converged:

- Audits #1–#4 caught real architectural defects (missing monitor file, atomic ordering, dead cross-references, hash divergence).
- Audits #5–#8 caught cascade-miss errors (envelope drift, stale cost quotes, approval-exception undercount, file-row recalibration).
- Audit #9 generalized the cascade-miss pattern into explicit rule amendments (soft headroom trigger, envelope cushion floor).
- This audit (#10) found one remaining specification gap that predates all prior audits and was not exercised by any of them — a pre-fetch slug-derivation reference that the monitor silently improvises around.

The blueprint has reached a state where the written rules largely own their own maintenance. Once W1 is addressed, the audit layer should be a rarely-fired backstop rather than a routine tool. If future audits become necessary, they will most likely be triggered by structural changes (new op added, new monitored-source class, new invariant introduced) rather than by drift inside the current invariants.

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode). If the user wishes to land W1, a normal approval request should follow.
