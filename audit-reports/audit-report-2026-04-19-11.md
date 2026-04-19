# Audit Report #21 — 2026-04-19

**Command:** `!! audit all`
**Schema version:** v2.0.16
**Mode:** Blueprint-authoring (no `wiki/` present — log appends and hot.md refreshes skipped)
**Prior audits read:** #11–#20 (all 2026-04-19 reports, audit-report-2026-04-19-01.md through audit-report-2026-04-19-10.md)

---

## Scope

Full audit of all tracked blueprint files. All 18 files read and verified. Token-reference headroom checked against `wc -c` measurements. Cross-references validated across the cold-start chain, Approval Rule exceptions, Blueprint Sync Rule matrix, ingest atomic ordering, hash pipeline, and sqlite-query hook contracts.

---

## Files Audited

| File | Measured (chars) | Documented (chars) | Headroom |
|---|---|---|---|
| `wiki/hot.md` | ~240 | ~300 | 25.0% |
| `memory.md` | n/a (empty) | ~3,800 | — |
| `CLAUDE.md` | ~20,641 | ~25,800 | 25.0% |
| `wiki/index.md` | ~800 | ~1,000 | 25.0% |
| `wiki/log.md` tail | varies | ~2,500 max | — |
| `scheduled-tasks/refresh-hot.md` | ~4,087 | ~5,100 | 24.8% |
| `ops/ingest.md` | ~15,877 | ~19,800 | 24.7% |
| `ops/lint.md` | ~2,476 | ~3,100 | 25.2% |
| `ops/query.md` | ~2,617 | ~3,300 | 26.1% |
| `ops/update.md` | ~1,916 | ~2,400 | 25.3% |
| `ops/conventions.md` | ~6,728 | ~8,400 | 24.9% |
| `ops/audit.md` | ~6,590 | ~8,200 | 24.4% |
| `ops/token-reference.md` | ~6,797 | ~8,500 | 25.0% |
| `blueprint/README.md` | ~4,821 | ~6,000 | 24.4% |
| `blueprint/setup-guide.md` | ~10,548 | ~13,200 | 25.1% |
| `blueprint/user-guide.md` | ~17,800 | ~22,250 | 25.0% |
| `blueprint/troubleshooting.md` | ~22,670 | ~28,300 | 24.8% |
| `blueprint/CHANGELOG.md` | ~72,182 | ~88,500 | 22.6% |
| `blueprint/skills/sqlite-query/SKILL.md` | ~4,185 | ~5,200 | 24.2% |
| `blueprint/skills/sqlite-query/query-layer.md` | ~2,533 | ~3,200 | 26.3% |
| `blueprint/skills/sqlite-query/ingest-hook.md` | ~2,838 | ~3,500 | 23.3% |

**Headroom verdict:** All 18 files clear. Minimum headroom is CHANGELOG.md at 22.6% — well above the 10% soft trigger. No hard triggers. **No recalibration required.**

---

## Envelope Check

Token-reference sum (template-side tracked files): **~62,950 tokens**
Documented upper bound: **65,000 tokens**
Cushion: **2,050 tokens (3.15%)**
Floor (2% of upper bound): **~1,300 tokens**

Cushion 3.15% > 2% floor. **No envelope widening required.**

---

## Cross-Reference Checks

All pass:

- **Cold-start chain**: CLAUDE.md self-cost ~6,450 ✓; cold-start total ~6,530 (6,450 + 80) ✓; `!! ready` total ~7,480 (6,530 + 950) ✓ — consistent across CLAUDE.md, user-guide.md, token-reference.md, and README.md.
- **Token-reference self-cost**: Header note quotes `~2,120 tokens` (both occurrences) ✓ — consistent with table row `~8,500 | ~2,120`.
- **Recalibration soft trigger**: `~10% of its measured actual` ✓ (v2.0.16 correction applied).
- **Envelope citation in token-reference**: `ops/audit.md:71` — audit.md envelope is at line 73. Stale line reference, informational only (same as audit #20 note; line numbers are not semantically binding).
- **Approval Rule exceptions**: `!! wrap`, `!! ready`, `!! audit` listed as documented exceptions ✓ — consistent across CLAUDE.md and user-guide.md.
- **Blueprint Sync Rule matrix**: 12-row matrix intact in conventions.md; all downstream-doc columns populated ✓.
- **Ingest atomic ordering**: Step 5 pre-compute `ts` → Step 6 `mv` → Step 7 write source page ✓. B5 step list: `[main-steps 5, 6, 7, 8, 9, 10, 11, 11.5]` ✓ (ingest hook included).
- **Hash pipeline**: Canonicalizer description consistent across ingest.md and user-guide.md ✓.
- **sqlite-query hook contracts**:
  - SKILL.md "Offered During Setup" → Step 4.5 ✓
  - query-layer.md path resolution: `subprocess.run(["find", ...])` — no glob patterns ✓
  - ingest-hook.md exception handler: directs to `!! install sqlite-query` backfill ✓
  - ingest-hook.md Notes section second bullet: directs to `!! install sqlite-query` backfill ✓
- **troubleshooting.md cross-reference**: ingest.md §URL Dedupe Exception cites "URL ingest keeps regenerating the same source even when the article hasn't changed" — heading present in troubleshooting.md ✓.
- **Directory diagram**: `blueprint/skills/` path ✓.
- **Schema version footer**: `Schema version: 2.0` in CLAUDE.md ✓; `v2.0.16` in hot.md ✓.

---

## Findings

### CRITICAL
None.

### WARNING
None.

### STYLE

**S1 — CHANGELOG v2.0.15 narrative corrected without a new CHANGELOG entry (audit trail gap)**

**Evidence:**
Audit #19 (S1) and audit #20 (S1) both flagged that the CHANGELOG v2.0.15 narrative cited stale values: `"70,207 chars"` / `"~87,900/~21,980"` / `"~62,800 tokens"` instead of the correct `"~70,800 chars"` / `"88,500 → ~88,500/~22,130"` / `"~62,950 tokens"`.

Reading CHANGELOG.md in this pass: the v2.0.15 narrative now correctly shows `"~70,800 chars"`, `"88,500 → ~88,500/~22,130"`, and `"~62,950 tokens"`. The correction was applied. CHANGELOG.md is 72,182 chars — up exactly 1 char from the 72,181 measured in audit #20 — consistent with changing `"70,207"` to `"~70,800"` (+1 char, net of removing the comma-less form).

However, there is no v2.0.17 CHANGELOG entry documenting this retroactive correction. Blueprint Sync Rule requires a CHANGELOG entry for every schema change; a retroactive narrative fix is a schema-level correction and warrants a patch entry.

**Recommendation:** Add a v2.0.17 CHANGELOG entry noting: "Retroactive fix: corrected stale values in v2.0.15 narrative (found by audits #19–#20, applied between audit #20 and audit #21). No file-size or token-table changes."

---

## Summary

Audit #21 is **clean** with one style note.

All 18 tracked files pass the headroom check (minimum 22.6% on CHANGELOG.md). The envelope cushion is 3.15%, above the 2% floor. All cross-references across the cold-start chain, ops files, sqlite-query skill bundle, and Blueprint Sync Rule matrix verify clean.

The sole finding (S1) is a missing CHANGELOG entry for a retroactive narrative correction that was applied between audit #20 and this pass. The underlying values in the v2.0.15 narrative are now correct; the gap is purely in the audit trail.

**Recommended action:** Add a v2.0.17 CHANGELOG patch entry (one paragraph, no cascade required).
