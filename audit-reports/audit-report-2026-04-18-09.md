# Blueprint Audit Report — 2026-04-18 (#9)

**Scope:** `!! audit all` — every file under `/sessions/practical-nifty-bardeen/mnt/Library/blueprint/`
**Schema under audit:** v2.0.8
**Prior audits reviewed:** #1 through #8 (audit-report-2026-04-18.md → audit-report-2026-04-18-08.md)
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**
- `blueprint/README.md` (4,644 chars)
- `blueprint/setup-guide.md` (12,204 chars)
- `blueprint/user-guide.md` (15,076 chars)
- `blueprint/troubleshooting.md` (25,348 chars)
- `blueprint/CHANGELOG.md` (43,457 chars)
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
- `blueprint/template/scheduled-tasks/ops/audit.md` (6,482 chars)
- `blueprint/template/scheduled-tasks/ops/token-reference.md` (6,095 chars)

**Prior audit reports (catch-up context)**
- `audit-report-2026-04-18.md` through `audit-report-2026-04-18-08.md`

**Not in audit scope (ignored):** `blueprint/.gitignore`, `blueprint/.git/`, `blueprint/.DS_Store`, `blueprint/template/.DS_Store`, `blueprint/template/scheduled-tasks/.DS_Store`.

### 1.2 Verification that audit-#8 fixes landed in v2.0.8

| Fix | Claim | Verified |
|---|---|---|
| W1 | `user-guide.md` cost table shows `!! wrap` ~2,800 and `!! ready` ~2,825 | ✓ lines 216–217 |
| W2 | `template/CLAUDE.md:58` reads "three documented exceptions" with three bullets (`!! wrap`, `!! ready`, `!! audit`) | ✓ lines 58–71 |
| S1 | `token-reference.md` row for `ops/audit.md` reads `~7,200 | ~1,800` | ✓ (calibrated pre-emptively) |

All three audit-#8 fixes are correctly landed.

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Chars column convention: ~110% of measured actual at calibration, rounded to nearest 100. Freshly-calibrated headroom lands around 9–11%.

| File | Measured | Doc. Chars | Doc. Tokens | Headroom | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,644 | 5,100 | 1,280 | 9.82% | ok |
| `setup-guide.md` | 12,204 | 13,400 | 3,350 | 9.80% | ok |
| `user-guide.md` | 15,076 | 16,600 | 4,150 | 10.11% | ok |
| `troubleshooting.md` | 25,348 | 27,900 | 6,980 | 10.07% | ok |
| **`CHANGELOG.md`** | **43,457** | **44,000** | **11,000** | **1.25%** | **⚠** |
| `LICENSE` | 1,067 | 1,200 | 300 | 12.47% | ok |
| `template/CLAUDE.md` | 19,875 | 21,900 | 5,475 | 10.19% | ok |
| `refresh-hot.md` | 3,966 | 4,400 | 1,100 | 10.94% | ok |
| `changelog-monitor.md` | 5,542 | 6,100 | 1,530 | 10.07% | ok |
| `ingest.md` | 14,247 | 15,500 | 3,880 | 8.79% | minor drift |
| `lint.md` | 2,243 | 2,500 | 630 | 11.46% | ok |
| `query.md` | 1,901 | 2,100 | 530 | 10.47% | ok |
| `update.md` | 1,305 | 1,400 | 350 | 7.28% | minor drift |
| `conventions.md` | 4,500 | 5,000 | 1,250 | 11.11% | ok |
| `ops/audit.md` | 6,482 | 7,200 | 1,800 | 11.08% | ok |
| `token-reference.md` | 6,095 | 6,800 | 1,700 | 11.57% | ok |

None of the files has exceeded its documented Chars value (the formal recalibration trigger per `token-reference.md:72`), so no automatic trigger has fired. However, `CHANGELOG.md` at 1.25% headroom is in the same drift class as the v2.0.5 S2 / v2.0.7 W1 / v2.0.8 S1 pre-emptive findings — see §2.

### 1.4 Envelope check (Recalibration Rule Step 5)

Re-summed from the documented Tokens column in `token-reference.md`:

Blueprint-doc rows:
`README (1,280) + setup-guide (3,350) + user-guide (4,150) + troubleshooting (6,980) + CHANGELOG (11,000) + LICENSE (300) = 27,060`

Template-side rows:
`CLAUDE (5,475) + refresh-hot (1,100) + changelog-monitor (1,530) + ingest (3,880) + lint (630) + query (530) + update (350) + conventions (1,250) + audit (1,800) + token-reference (1,700) = 18,245`

**Total = 45,305 tokens**, still inside the documented `~30,000–48,000` envelope quoted at `ops/audit.md:71` (cushion ≈ 2,695 tokens ≈ 5.9% of the upper bound). No envelope edit required.

Note: the `!! audit all` envelope figure in `user-guide.md:94`, `user-guide.md:215`, and `ops/audit.md:71` are all consistent at `~30,000–48,000` tokens.

### 1.5 Architectural invariants re-verified

| Invariant | Source | Status |
|---|---|---|
| Hash canonicalization pipeline (6 steps: preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]) | `ops/ingest.md` §Hash Canonicalization | ✓ intact |
| Rerun-proof ingest Step 0 (hash-first short-circuit) | `ops/ingest.md` §Step 0 | ✓ intact |
| Atomic ingest ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 write source page | `ops/ingest.md` | ✓ intact |
| Derived `Pages: N` counter (count `^- [[` lines; not stored) | `scheduled-tasks/refresh-hot.md` | ✓ intact |
| Detector-only changelog monitor (read-only; Slack DM sole side-effect) | `scheduled-tasks/changelog-monitor.md` | ✓ intact |
| Blueprint-authoring Mode guard (skip log append and hot.md refresh when `wiki/` absent) | `template/CLAUDE.md:110–114`; `ops/audit.md` step 5 | ✓ intact |
| Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only | `template/CLAUDE.md:102` | ✓ intact |
| Three documented Approval-Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) | `template/CLAUDE.md:58–71` | ✓ intact |
| `token-reference.md` is source of truth; `ops/audit.md:71` derives envelope from it rather than hand-tuning | `ops/audit.md:71`, `token-reference.md:10` | ✓ intact |
| Approval-exception generic `memory | …` wording for log entries | `template/CLAUDE.md` §Session Memory Commands | ✓ intact |

No architectural regressions detected.

### 1.6 Cross-reference sanity checks

- `CLAUDE.md:9` quotes `~5,475` for itself → matches `token-reference.md` row. ✓
- `user-guide.md:14` cold-start quote `~5,530` = 5,475 (CLAUDE.md) + 55 (hot.md). ✓
- `user-guide.md:216–217` realistic `!! wrap` / `!! ready` costs match `token-reference.md:54`. ✓
- `token-reference.md:54` references `~1,100` (refresh-hot.md), `~200` (wiki/index.md), `~625` (log.md tail), `~750` (memory.md), `~100` (log append) — all consistent with the Tokens column above. ✓
- `ops/audit.md:71` envelope `~30,000–48,000` is consistent with the re-derived 45,305 + cushion. ✓
- `CHANGELOG.md` v2.0.8 section documents the three audit-#8 fixes (W1/W2/S1). ✓
- No dangling xrefs; all prior-audit cleanup (ingest.md:64 dead xref from audit #6 W3, setup-guide dead xref from audit #4 C1, user-guide.md:216–217 stale costs from audit #8 W1) remain fixed.

---

## 2. Findings

### CRITICAL

None.

### WARNING

None.

### STYLE

**S1 — `CHANGELOG.md` headroom drift to 1.25%; pre-emptive recalibration recommended.**

*Symptom.* `CHANGELOG.md` measures 43,457 chars against a documented Chars value of 44,000 — only 543 chars (1.25%) of headroom remain. The 110% convention targets ~10% headroom at calibration; the file has consumed all but a sliver of it. Any single sub-point added to a future version section (typically ~500–2,000 chars for a patch entry) would likely exceed the documented bound and hard-fire the Recalibration Rule.

*Why it matters.* The formal trigger at `token-reference.md:72` fires only when measured > documented. But prior audits (v2.0.5 S2, v2.0.7 W1, v2.0.8 S1) established a "same drift class" pre-emptive pattern: recalibrate now, while the delta is small, rather than wait for the trigger to fire mid-patch — which risks surprising a future changelog edit with a simultaneous table bump. Furthermore, `CHANGELOG.md` is the *most churn-prone* file in the blueprint (it receives a new section on every version bump), so it benefits most from early recalibration.

*Recommended fix.* In the next patch (v2.0.9):
- Recalibrate `CHANGELOG.md` per Recalibration Rule Step 2: `1.1 × 43,457 = 47,803`, rounded to nearest 100 = **47,800 chars → ~11,950 tokens** (rounded to nearest 10).
- Step 4 cascade: `CHANGELOG.md` does not appear in cold-start or `!! audit all` user-facing quotes in `CLAUDE.md`, `README.md`, `user-guide.md`, or `setup-guide.md`, so no prose-level propagation is needed.
- Step 5 envelope re-sum: blueprint-doc rows move from 27,060 to 28,010; new template-side remains 18,245; new total **46,255**, still inside the `~48,000` upper bound (cushion shrinks from 2,695 to 1,745 ≈ 3.6%). That remains within the documented `~1,500–3,000 cushion` band per `token-reference.md:79`, so no envelope edit is required — but note the cushion has been consumed from ~5.9% down to ~3.6%, which is worth tracking for the *next* CHANGELOG recalibration (at which point widening the envelope may be necessary).
- Step 6 calibration-date touch: update the header to the patch date.
- Add a v2.0.9 CHANGELOG entry documenting the recalibration (Recalibration-Rule Step 5 exercised; cushion now ~3.6%).

*Severity rationale.* STYLE rather than WARNING because the trigger has not actually fired, the cushion is still inside the documented band, no invariant is broken, and the fix is purely mechanical table maintenance.

---

### Non-findings (considered and dismissed)

- **`update.md` at 7.28% headroom** — below the ~10% target but still well above any trigger. Delta since last calibration is ~33 chars (~2.6% growth). Not a flag-worthy drift at this level; will naturally fold into the next routine post-ingest recalibration pass.
- **`ingest.md` at 8.79% headroom** — similar story: within the rounding-tolerance band of the 110% convention. Not flag-worthy in isolation. (If multiple low-headroom files were clustered near a simultaneous trigger, that would change the analysis.)
- **`README.md` 9.82%, `setup-guide.md` 9.80%** — essentially at-calibration given rounding-to-nearest-100; no drift.

---

## 3. Questions for Clarification

**Q1 — Introduce a "soft" recalibration threshold to the Rule itself?**

Three consecutive audits (#7 W1, #8 S1, #9 S1) have each caught a single file drifting past ~2% headroom and flagged it as a pre-emptive STYLE finding. This pattern is effectively the audit layer *acting as* a soft threshold that the written rule doesn't encode. Should `token-reference.md`'s Recalibration Rule be amended to state the soft rule explicitly — e.g., *"Additionally fire when any file's headroom drops below 3%, not only when it's fully consumed"* — so routine maintenance catches these earlier without requiring an audit pass? (Counter-consideration: making the trigger tighter means `!! ingest` and `!! wrap` operations would need to re-measure more aggressively, which adds per-operation cost. The status quo — let audits catch it — may be the right call; but the pattern is now documented enough to make the decision deliberate.)

**Q2 — Envelope cushion tracking?**

As the table grows and documented Chars columns recalibrate upward, the `~48,000` envelope's cushion shrinks even when each individual file stays within its own headroom. Right now cushion is ~5.9%; after the proposed `CHANGELOG.md` recalibration it would be ~3.6%. At what lower bound should the envelope itself be widened, independent of the Recalibration Rule's "exceeds upper bound" trigger? Candidate rule of thumb: widen when cushion drops below ~2% of the upper bound (e.g., below ~1,000 tokens on a 48,000 envelope). Worth codifying in the Recalibration Rule's Step 5 prose alongside the existing "exceeds upper bound" language.

Neither question is a blocker; both are in the category of "make the discipline that audits already enforce explicit in the written rule."

---

## 4. Architectural Invariants Verified

All invariants below were checked against the source files during this audit and remain intact:

1. Hash canonicalization is the 6-step pipeline (preamble-strip → CRLF-normalize → whitespace-collapse → blank-line-collapse → trim → SHA-256 first 8 chars). Consumers reference the single canonicalizer; no call site has reimplemented the pipeline inline.
2. Ingest is rerun-proof: Step 0 computes the canonical hash before any write and short-circuits if already indexed.
3. Ingest is atomic in the v2.0.4+ ordering: `ts` is pre-computed in Step 5, the inbox→raw move happens in Step 6 before any page write in Step 7, and partial-failure recovery is the documented manual procedure in `troubleshooting.md`.
4. `Pages: N` is a derived counter (count of `^- [[` lines in the index), computed on demand by `refresh-hot.md`, never stored.
5. `changelog-monitor.md` is detector-only: it reads four upstream sources, compares cached hashes, and DMs the user via Slack; it performs no `!! ingest`-style writes to the wiki.
6. Blueprint-authoring Mode is respected consistently: `template/CLAUDE.md:110–114` documents the mode, and `ops/audit.md` step 5 explicitly skips the log append and `hot.md` refresh when `wiki/` is absent.
7. Versioning discipline holds: `CLAUDE.md` footer and `hot.md` `Schema:` field carry `X.Y`; `CHANGELOG.md` alone carries `X.Y.Z`. v2.0.8 does not move the footer (correct — it is a patch bump).
8. Approval Rule exceptions are enumerated identically in `template/CLAUDE.md` (lines 58, 68–71) and `README.md` (bullet list); both list all three (`!! wrap`, `!! ready`, `!! audit`). No drift since audit #8.
9. `token-reference.md` remains the single source of truth for cost estimates. `ops/audit.md:71` and `user-guide.md:94,215` derive their envelope figures from its Tokens column rather than hand-tuning.
10. Approval-exception log entries use the generic `memory | …` shape; `!! wrap` and `!! ready` do not require a separate token-reference read per `token-reference.md:54`.

---

## 5. Verdict

**The v2.0.8 blueprint is sound.** All three audit-#8 fixes are correctly landed, no architectural invariants have regressed, no dangling cross-references remain, and the `!! audit all` envelope continues to fit inside its documented bound (45,305 / 48,000 = 94.4% utilization; 5.9% cushion).

One STYLE finding (S1: `CHANGELOG.md` headroom drift to 1.25%) is recommended as a pre-emptive recalibration in v2.0.9. The two Questions for Clarification are discretionary improvements to the written Recalibration Rule — neither is required for correctness.

No CRITICAL or WARNING issues.

**Recommendation:** Land S1 as a minor patch (v2.0.9) the next time the CHANGELOG is edited anyway (e.g., as part of any other v2.0.9 change), folding the recalibration into the same commit rather than shipping it as a standalone patch.
