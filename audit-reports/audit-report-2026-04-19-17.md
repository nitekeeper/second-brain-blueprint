# Blueprint Audit Report — 2026-04-19 (#27)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.23 (per Non-cascade exception text in template/CLAUDE.md; CHANGELOG.md out of scope)  
**Prior audit reviewed:** #26 (`audit-report-2026-04-19-16.md`) — read in full before this pass per user instruction  
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)  
**Mode:** Live wiki present (wiki/ exists at working-folder root; log append and hot.md refresh apply if fixes are applied)  
**Note:** Audit reports directory (`audit-reports/`) excluded from scope per standing user instruction.

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**

- `README.md` (4,671 chars)
- `setup-guide.md` (10,564 chars)
- `user-guide.md` (14,219 chars)
- `troubleshooting.md` (22,670 chars)
- `LICENSE` (1,067 chars)
- `.gitignore` (65 chars)

**Template**

- `template/CLAUDE.md` (21,112 chars)
- `template/scheduled-tasks/refresh-hot.md` (3,966 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,877 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/query.md` (2,586 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,741 chars)
- `template/scheduled-tasks/ops/audit.md` (5,908 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,746 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (4,185 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (2,533 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,838 chars)

**Not in audit scope:** `ROADMAP.md` (planning doc, no logic content). `CHANGELOG.md` formally out of scope per v2.0.21. `audit-reports/` excluded per standing user instruction.

---

### 1.2 Files changed since audit #26

One file changed. All others (17 tracked files) are byte-for-byte identical to audit #26.

| File | Audit #26 bytes | This audit bytes | Delta | Cause |
|---|---:|---:|---:|---|
| `template/CLAUDE.md` | 20,641 | 21,112 | +471 | Non-cascade exception text added (v2.0.22/v2.0.23 patches) |

---

### 1.3 v2.0.22 / v2.0.23 changes verified

The Non-cascade exception block now appears in `template/CLAUDE.md` under the Blueprint Sync Rule:

> *"For startup or schema changes that are agent-internal with no user-facing behavioral impact, the listed cascade files may require no content update. Document any deliberate non-cascade in `CHANGELOG.md` with explicit justification. (Pattern established by v2.0.22; formalized by v2.0.23.)"*

The live `CLAUDE.md` (working folder root) contains the identical text — template and live are in sync. ✓

Per the Versioning Split rule, patch-level bumps (X.Y.Z) do not update the footer or hot.md Schema field. `template/CLAUDE.md` footer still reads `Schema version: 2.0`. ✓ `wiki/hot.md` still reads `Schema: v2.0`. ✓

The non-cascade rule allows these patches to skip cascade to blueprint docs — each requires documentation in `CHANGELOG.md` (out of audit scope) as justification. The rule's own application is self-consistent: it declares agent-internal changes can skip cascading, applies that to itself, and mandates CHANGELOG documentation. No circular logic failure.

---

### 1.4 Per-file headroom check (Recalibration Rule Steps 1–2)

Convention: ~125% of measured actual at calibration, rounded to nearest 100. Soft trigger: headroom below ~10% of measured actual. Hard trigger: measured ≥ documented.

| File | Measured (`wc -c`) | Doc. Chars | Headroom % | 10% Soft Floor | Flag |
|---|---:|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | 467 | ok |
| `setup-guide.md` | 10,564 | ~13,200 | 24.9% | 1,056 | ok |
| `user-guide.md` | 14,219 | ~17,800 | 25.2% | 1,422 | ok |
| `troubleshooting.md` | 22,670 | ~28,300 | 24.8% | 2,267 | ok |
| `LICENSE` | 1,067 | ~1,400 | 31.2% | 107 | ok |
| `template/CLAUDE.md` | 21,112 | ~25,800 | 22.2% | 2,111 | ok |
| `refresh-hot.md` | 3,966 | ~5,100 | 28.6% | 397 | ok |
| `ops/ingest.md` | 15,877 | ~19,800 | 24.7% | 1,588 | ok |
| `ops/lint.md` | 2,507 | ~3,100 | 23.7% | 251 | ok |
| `ops/query.md` | 2,586 | ~3,300 | 27.6% | 259 | ok |
| `ops/update.md` | 1,881 | ~2,400 | 27.6% | 188 | ok |
| `ops/conventions.md` | 6,741 | ~8,400 | 24.6% | 674 | ok |
| `ops/audit.md` | 5,908 | ~8,200 | 38.8% | 591 | ok |
| `ops/token-reference.md` | 6,746 | ~8,500 | 26.0% | 675 | ok |
| `skills/sqlite-query/SKILL.md` | 4,185 | ~5,200 | 24.2% | 419 | ok |
| `skills/sqlite-query/query-layer.md` | 2,533 | ~3,200 | 26.3% | 253 | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,838 | ~3,500 | 23.3% | 284 | ok |

No hard triggers. No soft triggers. `template/CLAUDE.md` gained 471 bytes but headroom (22.2% / 4,688 chars) remains well above the 10% soft floor (2,111 chars). No recalibration required. `ops/audit.md` over-calibration (38.8%) from audit #26 persists — still not a trigger and will self-correct on next routine recalibration pass.

---

### 1.5 Envelope check (Recalibration Rule Step 5)

No rows in `token-reference.md` changed. Token-reference CLAUDE.md row still documents ~25,800 / ~6,450 (the +471-byte growth in template/CLAUDE.md consumed headroom but did not exceed the documented chars). Table sum remains 40,820 tokens; envelope `~30,000–43,000`; cushion 2,180 tokens (5.07% of 43,000 — above the 2% floor of ~860). No envelope widening required.

---

### 1.6 Cross-reference sanity checks

All cross-references verified in audit #26 re-verified, with additional checks on the new Non-cascade exception text:

- `template/CLAUDE.md` cold-start self-cost `~6,450` — matches token-reference CLAUDE.md row. ✓
- `template/CLAUDE.md` cold-start total `~6,530` — 6,450 (CLAUDE.md) + 80 (hot.md). ✓
- `user-guide.md:9` CLAUDE.md startup cost `~6,450 tokens`. ✓
- `user-guide.md:94` audit-all `~30,000–43,000`. ✓
- `user-guide.md:201` audit-all cost table `~30,000–43,000`. ✓
- `ops/audit.md:71` envelope `~30,000–43,000`. ✓
- `ops/token-reference.md` Step 5 `(currently ~30,000–43,000)`. ✓
- `ops/token-reference.md` floor note `(~860 tokens on a 43,000-token envelope)` — 43,000 × 2% = 860. ✓
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:71–74`, `README.md:73`, and `user-guide.md:175`. ✓
- Blueprint Sync Rule 12-row matrix — intact; Non-cascade exception correctly appended as a `>` note, not a table row. ✓
- Versioning split (`Schema version: 2.0` in template footer) — consistent with patch-only bumps v2.0.22/v2.0.23. ✓
- Non-cascade exception text — identical in live `CLAUDE.md` and `template/CLAUDE.md`. ✓
- `ops/audit.md` scope list — `blueprint/CHANGELOG.md` not present (correctly removed in v2.0.21). ✓
- `SKILL.md` "Offered During Setup" → "Step 4.5" — matches `setup-guide.md` heading. ✓
- Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv` → Step 7 page write. ✓
- Hash canonicalization 6-step pipeline — intact. ✓
- `Pages: N` derived from `^- [[` entries — `refresh-hot.md` awk pipeline unchanged. ✓
- Blueprint-authoring mode guard — present in template/CLAUDE.md and audit.md:43. ✓
- Hook contracts (query-layer and ingest-hook) — consistent across conventions.md, ingest.md, update.md, query-layer.md, ingest-hook.md, SKILL.md. ✓

---

## 2. Findings

### CRITICAL

None.

### WARNING

None.

### STYLE

None.

---

## 3. Non-findings (considered and dismissed)

- **`template/CLAUDE.md` +471 bytes (Non-cascade exception text).** Growth is legitimate patch content (v2.0.22/v2.0.23). No headroom trigger fires. The new text is internally consistent: it adds a documented opt-out path from the Blueprint Sync Rule cascade, requires CHANGELOG documentation as the audit trail, and applies the opt-out to itself (both patches were non-cascading). No circular logic failure — the rule's own non-cascade application is a valid use of the rule it defines. ✓
- **Non-cascade patches not verifiable against CHANGELOG.md.** CHANGELOG.md is out of audit scope since v2.0.21. The Non-cascade exception text references v2.0.22 and v2.0.23 as being documented there. Cannot verify, but the requirement is imposed on the user/author, not the files in audit scope. Not a finding against tracked files.
- **`audit-reports/` directory not listed in Directory Structure.** This is a generated/operational folder, not a template distribution artifact. Directory Structure in CLAUDE.md is representative of the template layout, not exhaustive. Not a defect.
- **`ops/audit.md` over-calibrated headroom (38.8%).** Persists from audit #26 as a known non-defect. Will self-correct on next routine ingest recalibration pass. Not a trigger.
- **Envelope arithmetic.** Table sum 40,820 tokens; cushion 2,180 (5.07% of 43,000 — above 2% floor). ✓ template/CLAUDE.md growth consumed headroom within the CLAUDE.md row but did not change the token count used in the sum (token-reference.md was not updated, correctly, since no hard/soft trigger fired). ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently in all three locations. ✓
- **sqlite-query skill integrity** — DB schema, upsert pattern, bidirectional-relation INSERT OR IGNORE, query-layer find-based path resolution, ingest-hook exception handler — all unchanged and correct. ✓
- **`refresh-hot.md` awk portability** — 1-argument `match()` form only. ✓
- **`!! ready` mid-session guard** — present in template/CLAUDE.md, troubleshooting.md, user-guide.md; all consistent. ✓
- **`!! wrap` pre-write safeguard and TRUNCATED_ACKNOWLEDGED handling** — consistent across template/CLAUDE.md and troubleshooting.md. ✓
- **Cold-start total `~6,530`** — 6,450 (CLAUDE.md) + 80 (hot.md). ✓
- **`!! ready` total `~7,480`** — 6,530 + 950 (memory.md full). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — derivable from current token-reference component values. ✓

---

## 4. Questions for Clarification

None. All findings are self-contained.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11–#26 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in `index.md`), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in `template/CLAUDE.md` and `ops/audit.md:43`. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and `hot.md` Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < ~10% of measured actual), envelope cushion floor (cushion < ~2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. Non-cascade exception now documented as an opt-out path requiring CHANGELOG justification. ✓
11. sqlite-query skill follows Query Layer Hook Contract (`find`-based path resolution, no glob patterns) and Ingest Hook Contract (non-fatal errors, consistent repair messaging). ✓

---

## 6. Verdict

**The v2.0.23 blueprint has no CRITICAL, WARNING, or STYLE findings.**

Since audit #26, one file changed: `template/CLAUDE.md` grew +471 bytes (20,641 → 21,112) to add the Non-cascade exception text, introduced by patches v2.0.22 and v2.0.23. The change is internally consistent — the non-cascade rule correctly opts out of cascading to blueprint docs (since it's agent-internal), applies to itself, and mandates CHANGELOG documentation as the audit trail. All 11 architectural invariants hold. Headroom healthy across all 17 tracked files; no hard or soft recalibration triggers; token envelope unchanged at 40,820 / 43,000 cushion.

Read-only audit complete. No fixes applied.
