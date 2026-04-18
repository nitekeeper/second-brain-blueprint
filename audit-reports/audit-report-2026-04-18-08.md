# Audit Report — `!! audit all` (eighth pass)

**Date:** 2026-04-18
**Scope:** All tracked files under `blueprint/` (read-only audit per `ops/audit.md` §"If `!! audit all`")
**Mode:** Blueprint-authoring (no `wiki/` at working-folder root — `wiki/log.md` append and `hot.md` refresh skipped per `@template/CLAUDE.md` Blueprint-authoring Mode)
**Schema version under audit:** v2.0.7

Prior audit reports (1–7) were read in full before starting this pass to avoid re-flagging resolved issues. All five v2.0.7 fixes from audit #7 (W1 `token-reference.md:54`, W2+S2 envelope-justification prose, S1 Recalibration Rule Step 5, Q1 per-file footer normalization, and the envelope widen `~30,000–45,000` → `~30,000–48,000`) are verified landed and internally consistent.

---

## Chain of Verification

The blueprint is a CLAUDE.md-centric personal wiki schema distributed as a template directory. Its intended logic:

1. **Startup contract** — agent reads `CLAUDE.md` (~5,475) + `hot.md` (~55) to cold-start at ~5,530 tokens; defers `index.md` / `log.md` / ops files until needed. `!! ready` adds `memory.md` (~750) for a ~6,280-token warm start.
2. **Approval Rule** — every write pauses for user confirmation, with documented exceptions for `!! wrap`, `!! ready`, and `!! audit` (the last being read-only by default; fixes follow the normal flow). Exception entry-shape wording is generic (`memory | …`) so future memory-flow entries don't require re-broadening.
3. **Blueprint Sync Rule** — ten-row matrix maps schema/ops/convention/cost/footer changes to the blueprint files that must be re-propagated. Audit-driven edits use an `audit | …` log label that supersedes `sync | …`.
4. **Ingest** — atomic ordering (Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 source-page write with matching `original_file:` and footnotes) plus Step 0 rerun-proof hash guard. The Hash Canonicalization pipeline (preamble-strip → CRLF/CR→LF → intra-line whitespace collapse → blank-line collapse → trim → SHA-256[0:8]) is shared with `changelog-monitor.md` Step 3 so Clipper/URL/monitor hashes are comparable.
5. **Hot.md** — derived `Pages: N` count (match `^- [[` entries at refresh time, not a stored header), ISO-date-sorted top-5 Hot list, `Gaps:` extracted from the most recent lint entry in `log.md`, total file ≤500 chars.
6. **Changelog monitor** — daily detector; never writes; fail-soft per source; Slack self-DM is the only side effect and the sole audit trail.
7. **Blueprint-authoring Mode** — when `wiki/` is absent at the working-folder root, skip every `wiki/log.md` append and `hot.md` refresh across all ops; announce readiness from `CLAUDE.md` alone.
8. **Versioning split** — X.Y schema version lives in the CLAUDE.md footer and `hot.md`'s `Schema:` field; X.Y.Z patches add a CHANGELOG section only.
9. **Token-reference source-of-truth** — the `File Read Costs` Chars column is canonical; every cost quoted in CLAUDE.md / README.md / user-guide.md / setup-guide.md must be re-derivable from it, and the `!! audit all` envelope is re-summed from the Tokens column per Recalibration Rule Step 5.

Against that intended logic, three defects survive in v2.0.7.

---

## Findings

### WARNING — `user-guide.md:216–217` stale realistic `!! wrap` / `!! ready` costs (W1)

**Evidence:**

`template/scheduled-tasks/ops/token-reference.md:54` (v2.0.7 canonical values):

> Realistic per-command cost when none of those files are already cached is **~2,800 tokens for `!! wrap`** and **~2,825 for `!! ready`** … Quote ~2,800 when asked …

`user-guide.md:216–217`:

```
| `!! wrap` (realistic) | ~2,700 |
| `!! ready` (realistic) | ~2,800 |
```

**Failure:** v2.0.7's W1 entry explicitly bumped the two realistic figures inside `token-reference.md:54` (`!! wrap` ~2,700 → ~2,800, `!! ready` ~2,800 → ~2,825) and recorded the per-file-read arithmetic that produced each. The user-guide cost table duplicates both figures as user-facing planning numbers, but the v2.0.7 cascade stopped at `token-reference.md` and never propagated them out. Consequence: the user-guide quotes a `!! wrap` value 100 tokens lower than the source of truth and a `!! ready` value 25 tokens lower — direct doc-vs-doc contradictions of an invariant the `token-reference.md` header declares in writing ("Any quoted cost in CLAUDE.md, README.md, user-guide.md, or setup-guide.md must be re-derivable from this table — re-propagate when this table changes").

**Class:** Same cascade-miss class as audit #6's W1 (`user-guide.md:14` cold-start not updated after v2.0.5's cascade) and W2 (`user-guide.md:94` envelope prose not updated after v2.0.5's envelope bump). Both were classified WARNING for exactly this reason — a stated source-of-truth invariant was silently violated by an incomplete propagation. Flagging this one the same way is the consistent call.

**Fix (if approved):** Edit `user-guide.md:216–217`:

```
| `!! wrap` (realistic) | ~2,800 |
| `!! ready` (realistic) | ~2,825 |
```

No behavioral change, no other files touched — this is a two-number string replacement.

---

### WARNING — `template/CLAUDE.md:58` "two documented exceptions" contradicts the three-bullet list immediately below (W2)

**Evidence:**

`template/CLAUDE.md:58`:

> **IMPORTANT: Never perform write or edit actions without explicit user approval — with **two documented exceptions** listed below.**

`template/CLAUDE.md:68–71` (the list "below"):

> **Documented exceptions (no separate approval request required):**
> - `!! wrap` — …
> - `!! ready` — …
> - `!! audit` — user invocation runs a read-only audit and needs no approval to *run*. …

**Failure:** Intro says two; list has three. CHANGELOG v1.14 ("README `!! audit` exception drift fixed") documents that the third exception (`!! audit`) was deliberately added to `CLAUDE.md`'s list — but the intro sentence's count was not updated at the same time, and the drift has persisted through every subsequent schema bump. `README.md:65` correctly enumerates all three ("`!! wrap`, `!! ready`, and `!! audit` are the only exceptions"); `user-guide.md:189` correctly enumerates all three ("Documented exceptions (no separate approval prompt): `!! wrap`, `!! ready`, and `!! audit`"). Only `CLAUDE.md`'s own intro sentence still says "two" — and it's inside an **IMPORTANT**-tagged rule the agent reads every cold start, which is the worst possible place for a numeric contradiction to live.

**Class:** Direct intra-file self-contradiction, identical shape to audit #6 W1 (`user-guide.md:14` said `~6,005` while the cost table 195 lines later said `~6,280`). That was classified WARNING. Same call here.

**Fix (if approved):** Edit `CLAUDE.md:58`:

> **IMPORTANT: Never perform write or edit actions without explicit user approval — with **three documented exceptions** listed below.**

Single-word change. No downstream propagation needed — README and user-guide already use fuzzy enumerations that don't depend on a count.

---

### STYLE — `ops/audit.md` headroom at 1.8%, well below 10% convention (S1)

**Evidence:**

`wc -c` snapshot of `ops/audit.md` vs. its documented Chars cap:

| File | Measured actual | Documented Chars | Headroom |
|---|---|---|---|
| `ops/audit.md` | 6,482 | 6,600 | 118 chars (1.8%) |

For reference, the rest of the template-side rows sit at 6.8%–11.1% headroom; `ops/audit.md` is the only file dangerously close to the Recalibration Rule trigger. The `token-reference.md` convention (Recalibration Rule line 70): *"Chars column is set to ~110% of measured actual at calibration time, rounded to nearest 100. …The 10% headroom absorbs small edits so the table doesn't need to move on every change."* Audit #5 flagged the same pattern on the same file as STYLE S2; v2.0.7's W2 + S2 edits (envelope-justification prose and the Note on audit.md:71) have since pushed it from "under headroom" back toward the trigger line.

**Failure (severity STYLE, not WARNING):** The trigger has not yet fired — measured 6,482 is still under the 6,600 cap — so there is no active contradiction and no false figure downstream. But the next non-trivial edit to `ops/audit.md` (e.g. the fix to the two WARNINGs above, if they cascade back into audit.md text, or any future op-specific clarification) will cross the cap and force a mid-flight recalibration. Pre-emptive recalibration of this one row would avoid that and match the pattern the 10% convention was written to support.

**Fix (if approved):** Bump the `ops/audit.md` row in `token-reference.md`:

```
| `ops/audit.md` | ~6,600 | ~1,650 |   →   | `ops/audit.md` | ~7,200 | ~1,800 |
```

(110% of 6,482 = 7,130, rounded up to 7,200; tokens 7,200 ÷ 4 = 1,800.) This adds 150 tokens to the template-side sum (18,095 → 18,245), which combined with the blueprint-doc rows (27,060) gives a new total of ~45,305 — still inside the widened ~48,000 upper bound (cushion drops from ~2,845 to ~2,695, ~5.9%). Per Recalibration Rule Step 5, since the updated sum is still inside the bound, no envelope edit is needed — only the single row, the calibration date header, and a short CHANGELOG v2.0.8 note.

No behavioral change. This is pre-emptive housekeeping, not a bug fix.

---

## Questions for Clarification

None this pass. The v2.0.7 fixes resolved all outstanding items including the long-running Q1 per-file footer asymmetry (carried across audits #3–#7). Prior items from audit #7 that remained open, if any, are absorbed into the three findings above.

---

## Architectural Invariants Verified

Read-only confirmation that the following remain intact in v2.0.7 — no defects found in any of these systems:

- **Rerun-proof ingest (Step 0 hash check).** `ops/ingest.md:61–67` documents the exit path precisely: delete inbox file, print `No change since last ingest — skipped.`, skip Steps 1–13 entirely, no log append, no hot.md refresh, no recalibrate. `!! ingest all`'s B3.6 applies the same guard batch-level before B4 approval.
- **Atomic ingest ordering.** `ops/ingest.md` Steps 5 (pre-compute `ts`) → 6 (mv inbox→raw) → 7 (write source page) are ordered and explained; Step 6's prose spells out the failure mode the ordering fixes.
- **Hash Canonicalization pipeline.** `ops/ingest.md:38–55` documents the six-step normalizer and calls out the code-indentation flattening trade-off. `changelog-monitor.md:29` references the same pipeline so cross-path hashes stay comparable.
- **Derived `Pages: N` counter.** `refresh-hot.md` Step 1 computes the page count from `^- [[` matches at refresh time with explicit "derived, not stored" wording; nothing elsewhere stores a stale copy.
- **Detector-only changelog monitor.** `changelog-monitor.md` Rules section enumerates read-only, autonomous, fail-soft, no-log-entry, and no-hash-caching. Slack message is the sole side effect. v2.0.7 Q1 dropped the stray per-file footer — all template-side files are now footer-free.
- **Blueprint-authoring Mode.** `template/CLAUDE.md:110–114` covers startup defensiveness and skip rules; `ops/audit.md:43` and `:45` explicitly gate log-append and hot.md-refresh on `[ -e wiki/log.md ]`. The audit is called out as the op most likely to run in this mode — correct, and confirmed by this session running exactly that way.
- **Versioning split.** `template/CLAUDE.md:102` is explicit: X.Y in the footer and `hot.md`, X.Y.Z adds CHANGELOG only. v2.0.7 is a patch version (X.Y.Z); footer and hot.md remain `Schema: v2.0`.
- **Blueprint Sync Rule ten-row matrix + audit-label exception.** Matrix at `CLAUDE.md:87–101` plus the audit-edit exception at `:106` are coherent; `ops/audit.md:42–44` re-states the rule locally and cites the audit-label supersession so no double-entry drift.
- **Approval Rule three exceptions and their side-effect scopes.** The generic `memory | …` wording introduced in v1.14 still cleanly covers all memory-flow entry shapes (`Session summary saved`, `Session summary consumed`, `Truncated summary cleared`, `Truncated summary acknowledged`). `!! audit` correctly scoped to "run is free; fixes follow normal flow." Only defect in this region is W2 above — the intro count is stale, but the bullets themselves are correct.
- **Token-reference source-of-truth and Recalibration Rule Step 5.** `token-reference.md:10` states the invariant; Recalibration Rule Step 5 (added in v2.0.7) codifies the envelope-cascade obligation that v2.0.6 caught by editor judgment. I exercised Step 5 during this audit — re-summing blueprint-doc rows (27,060) + template-side rows (18,095) = 45,155 tokens, still under the ~48,000 upper bound with ~6.3% cushion.

---

## Verdict

Three defects surface in v2.0.7. Two are WARNINGs (both doc-vs-doc contradictions: `user-guide.md` realistic `!! wrap` / `!! ready` costs out of sync with `token-reference.md:54`, and `CLAUDE.md:58`'s "two exceptions" lagging the three-bullet list). One is a STYLE pre-emptive recalibration of `ops/audit.md` to restore the 10% headroom convention. No CRITICAL issues; the architectural invariants documented above are all intact. The blueprint remains sound.

If the user wants to apply any of the three fixes, I'll open a normal approval request covering the affected files, token estimate (including the `token-reference.md` ~1,700 self-cost), and the Blueprint Sync Rule rows each fix triggers (W1 = File-size/cost row cascade into user-guide.md; W2 = single-file edit to CLAUDE.md, no sync-table row applies; S1 = File-size/cost row edit to `token-reference.md` only, since cold-start figures don't change and the envelope doesn't move).
