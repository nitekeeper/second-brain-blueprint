# Blueprint Audit Report — 2026-04-19 (#14)

**Scope:** `!! audit all` — fix-verification pass (all audit #13 findings)
**Schema under audit:** v2.0.12 (CHANGELOG entry present and complete)
**Prior audit reviewed:** #13 (`audit-report-2026-04-19-03.md`) — fixes verified against live files
**Role:** Senior Software Architect (fix-verification; no further fixes applied)
**Mode:** Blueprint-authoring (no `wiki/` present at working-folder root; log append and `hot.md` refresh skipped)

---

## 1. Fix Verification — Audit #13 Findings

All three fixes from audit #13 were found applied in the live files.

### W1 — `SKILL.md` "Offered During Setup" named wrong step

**Status: APPLIED ✓**

`SKILL.md` "Offered During Setup" section now reads:
> `` `setup-guide.md` Step 4.5 offers this skill during initial setup. ``

Matches the actual step heading in `setup-guide.md`: `## Step 4.5 — Offer SQLite Query Skill`.

---

### W2 — `query-layer.md` returned glob patterns instead of resolved file paths

**Status: APPLIED ✓**

`query-layer.md` Step 1 `if rows:` branch now uses `subprocess.run(["find", pages_dir, "-name", "<slug>.md"])` to resolve each slug to a concrete path. Only paths that `find` locates are appended to `candidate_paths`; missing slugs produce no output and are silently skipped. The glob-pattern approach (`wiki/pages/**/<slug>.md`) is fully removed.

Inline comment documents the reason: "Python's `open()` and the Read tool do not expand globs; unmatched bash globs return the literal pattern string rather than empty."

`ops/conventions.md` Query Layer Hook Contract output spec updated:
> "Paths must be fully resolved (e.g. `wiki/pages/concepts/slug.md`) — do NOT return glob patterns such as `wiki/pages/**/slug.md`. … Use `find wiki/pages -name "<slug>.md"` (via `subprocess.run`) to resolve slugs to concrete paths."

---

### W3 — `ingest-hook.md` error message directed to `!! lint` for DB desync

**Status: APPLIED ✓**

`ingest-hook.md` exception handler now reads:
> `"…wiki.db may be out of sync. To repair: say '!! install sqlite-query' and choose yes to the backfill offer, or '!! uninstall sqlite-query' to revert to grep."`

`SKILL.md §Fallback Behaviour` updated with a "DB desync recovery" paragraph covering the same repair path.

---

## 2. Recalibration Verification

`query-layer.md` grew from 1,962 → 2,533 chars, firing the hard recalibration trigger (2,533 > 2,500 documented). Recalibrated at 125%: 2,533 × 1.25 = 3,166 → **~3,200 / ~800**. `token-reference.md` skill row updated.

Per-file headroom spot-check on all modified files:

| File | Measured (`wc -c`) | Doc. Chars | Headroom | Flag |
|---|---:|---:|---:|:---:|
| `SKILL.md` | 4,185 | ~4,700 | 12.3% | ok |
| `query-layer.md` | 2,533 | ~3,200 | 26.4% | ok |
| `ingest-hook.md` | 2,746 | ~3,300 | 20.1% | ok |
| `ops/conventions.md` | 6,741 | ~8,000 | 18.7% | ok |
| `ops/token-reference.md` | 6,796 | ~8,300 | 22.1% | ok |
| `CHANGELOG.md` | 62,089 | ~69,100 | 11.3% | ok |

No hard or soft triggers active post-fix.

Envelope sum after recalibration:

| Group | Tokens |
|---|---:|
| Blueprint-doc (unchanged) | 33,435 |
| Template-side (unchanged) | 20,470 |
| Skill rows: SKILL.md (1,180) + query-layer (800) + ingest-hook (830) | 2,810 |
| **Total** | **56,715** |

Cushion: 58,000 − 56,715 = **1,285 tokens (2.2%)**. Above the 2% floor (1,160 tokens). No envelope widening required.

---

## 3. Non-findings (re-verified from audit #13)

- All audit #13 non-findings carry forward unchanged. ✓
- Q1 (desync recovery documentation) resolved by W3 fix — `SKILL.md §Fallback Behaviour` now documents the repair path. ✓
- All architectural invariants (#1–#11) from audit #13 carry forward. ✓
- Invariant #11 (sqlite-query follows hook contracts) now fully satisfied: W2 fix brings query-layer.md into compliance with the Query Layer Hook Contract output spec. ✓

---

## 4. Verdict

**All three audit #13 findings (W1, W2, W3) are applied and verified. Schema is v2.0.12. No new findings.**

No CRITICAL, WARNING, or STYLE issues identified in this verification pass. The blueprint is clean. Envelope cushion 2.2% — above the 2% floor; monitor at next calibration.

Fix-verification audit complete. No further fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
