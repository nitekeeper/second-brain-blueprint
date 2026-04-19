# Blueprint Audit Report — 2026-04-19 (#13)

**Scope:** `!! audit all` — every tracked file under the blueprint root  
**Schema under audit:** v2.0.11 (per CHANGELOG.md; no later entry found)  
**Prior audits reviewed:** #11 (`audit-report-2026-04-19-01.md`) and #12 (`audit-report-2026-04-19-02.md`) — read before this audit pass per user instruction  
**Role:** Senior Software Architect (read-only; no fixes applied without subsequent approval)  
**Mode:** Blueprint-authoring (no `wiki/` present at working-folder root; log append and `hot.md` refresh skipped)  
**Note:** Audit reports directory (`audit-reports/`) excluded from scope per standing user instruction.

---

## 1. Chain of Verification

### 1.1 Files read in full

**Blueprint docs**

- `README.md` (4,671 chars)
- `setup-guide.md` (10,564 chars)
- `user-guide.md` (14,219 chars)
- `troubleshooting.md` (21,536 chars)
- `CHANGELOG.md` (59,139 chars)
- `LICENSE` (1,067 chars)
- `.gitignore` (65 chars)

**Template**

- `template/CLAUDE.md` (20,641 chars)
- `template/scheduled-tasks/refresh-hot.md` (3,966 chars)
- `template/scheduled-tasks/ops/ingest.md` (15,852 chars)
- `template/scheduled-tasks/ops/lint.md` (2,507 chars)
- `template/scheduled-tasks/ops/query.md` (2,586 chars)
- `template/scheduled-tasks/ops/update.md` (1,881 chars)
- `template/scheduled-tasks/ops/conventions.md` (6,379 chars)
- `template/scheduled-tasks/ops/audit.md` (6,572 chars)
- `template/scheduled-tasks/ops/token-reference.md` (6,796 chars)

**Skills (`blueprint/skills/`)**

- `blueprint/skills/sqlite-query/SKILL.md` (3,742 chars)
- `blueprint/skills/sqlite-query/query-layer.md` (1,962 chars)
- `blueprint/skills/sqlite-query/ingest-hook.md` (2,639 chars)

**Not in audit scope:** `blueprint/` sub-directory internals (working-folder-level installed files), `ROADMAP.md` (planning doc, no logic content).

### 1.2 Verification that audit #12 findings are clean

Audit #12 was a fix-verification pass confirming all five audit #11 findings (W1–W3, S1–S2) were applied and verified in v2.0.11. Direct re-verification of each:

| Fix | Claim | Re-verified |
|---|---|---|
| W1 | `template/CLAUDE.md:9` now reads `~6,250 tokens` | ✓ confirmed |
| W2 | `blueprint/CHANGELOG.md` row re-added to `token-reference.md` at `~69,100 / ~17,275` | ✓ confirmed |
| W2 cascade | Envelope `~30,000–58,000` in `ops/audit.md:72`, `user-guide.md:94`, `user-guide.md:201` | ✓ confirmed |
| W3 | CHANGELOG v2.0.11 entry present, covering all four undocumented changes | ✓ confirmed |
| S1 | `ops/query.md` `~3,300/~830`, `ops/update.md` `~2,400/~600`, `ops/conventions.md` `~8,000/~2,000` | ✓ confirmed |
| S2 | `template/CLAUDE.md` directory diagram shows skills at `blueprint/skills/` | ✓ confirmed |

No regressions from #12. Schema v2.0.11 findings baseline is clean.

### 1.3 Per-file headroom check (Recalibration Rule Steps 1–2)

Current convention per `token-reference.md`: **~125% of measured actual at calibration**, rounded to nearest 100.

| File | Measured (`wc -c`) | Doc. Chars | Headroom | Flag |
|---|---:|---:|---:|:---:|
| `README.md` | 4,671 | ~6,000 | 28.5% | ok |
| `setup-guide.md` | 10,564 | ~12,800 | 21.2% | ok |
| `user-guide.md` | 14,219 | ~17,100 | 20.3% | ok |
| `troubleshooting.md` | 21,536 | ~27,300 | 26.8% | ok |
| `CHANGELOG.md` | 59,139 | ~69,100 | 16.8% | ok |
| `LICENSE` | 1,067 | ~1,400 | 31.3% | ok |
| `template/CLAUDE.md` | 20,641 | ~25,000 | 21.1% | ok |
| `refresh-hot.md` | 3,966 | ~5,100 | 28.6% | ok |
| `ops/ingest.md` | 15,852 | ~18,600 | 17.3% | ok |
| `ops/lint.md` | 2,507 | ~2,900 | 15.7% | ok |
| `ops/query.md` | 2,586 | ~3,300 | 27.6% | ok |
| `ops/update.md` | 1,881 | ~2,400 | 27.6% | ok |
| `ops/conventions.md` | 6,379 | ~8,000 | 25.4% | ok |
| `ops/audit.md` | 6,572 | ~8,200 | 24.8% | ok |
| `ops/token-reference.md` | 6,796 | ~8,300 | 22.1% | ok |
| `skills/sqlite-query/SKILL.md` | 3,742 | ~4,700 | 25.6% | ok |
| `skills/sqlite-query/query-layer.md` | 1,962 | ~2,500 | 27.4% | ok |
| `skills/sqlite-query/ingest-hook.md` | 2,639 | ~3,300 | 20.1% | ok |

No hard triggers (measured ≥ documented). No soft triggers (headroom < 3% of measured actual). No recalibration required.

### 1.4 Envelope check (Recalibration Rule Step 5)

Documented rows sum from `token-reference.md` (unchanged from audit #12 verification):

| Group | Tokens |
|---|---:|
| Blueprint-doc (README 1,500 + setup-guide 3,200 + user-guide 4,280 + troubleshooting 6,830 + CHANGELOG 17,275 + LICENSE 350) | 33,435 |
| Template-side (CLAUDE 6,250 + refresh-hot 1,280 + ingest 4,650 + lint 730 + query 830 + update 600 + conventions 2,000 + audit 2,050 + token-reference 2,080) | 20,470 |
| Skill rows (SKILL.md 1,180 + query-layer 630 + ingest-hook 830) | 2,640 |
| **Total** | **56,545** |

Cushion: 58,000 − 56,545 = **1,455 tokens (2.5%)**. Above the 2% floor (1,160 tokens). No envelope widening required.

### 1.5 Cross-reference sanity checks

- `template/CLAUDE.md:9` cold-start `~6,250` = token-reference CLAUDE.md row. ✓
- `template/CLAUDE.md:17` cold-start total `~6,330` = 6,250 + 80 (hot.md). ✓
- `template/CLAUDE.md:17` `!! ready` total `~7,280` = 6,330 + 950 (memory.md full). ✓
- `user-guide.md:9` CLAUDE.md cost `~6,250` — matches token-reference row. ✓
- `user-guide.md:14` cold-start prose `~6,330` — consistent with CLAUDE.md line 17. ✓
- `user-guide.md:201` audit all `~30,000–58,000` — matches `ops/audit.md:72`. ✓
- `user-guide.md` realistic `!! wrap` `~3,000` / `!! ready` `~3,300` — derivable from current token-reference component values. ✓
- Three Approval Rule exceptions (`!! wrap`, `!! ready`, `!! audit`) — enumerated consistently in `template/CLAUDE.md:69–72`, `README.md:73`, and `user-guide.md:175`. ✓
- Blueprint Sync Rule 12-row matrix — intact. ✓
- Versioning split (major.minor in footer + hot.md; patches in CHANGELOG only) — documented and consistent. ✓
- Ingest atomic ordering: Step 5 pre-compute `ts` → Step 6 `mv inbox→raw` → Step 7 write source page. ✓
- Hash canonicalization 6-step pipeline intact in `ops/ingest.md §Hash Canonicalization`. ✓
- Blueprint-authoring mode guard present in `template/CLAUDE.md`, `ops/audit.md:44`, and `!! ready` step 5 footnote. ✓
- `SKILL.md` install step 4 file copy targets (`scheduled-tasks/query-layer.md`, `scheduled-tasks/ingest-hook.md`) match `CLAUDE.md` directory structure. ✓
- `SKILL.md` uninstall targets match install targets. ✓

---

## 2. Findings

### CRITICAL

None.

### WARNING

**W1 — `blueprint/skills/sqlite-query/SKILL.md` "Offered During Setup" names wrong step number: says "Step 4," should be "Step 4.5."**

*Evidence.*

`SKILL.md` (final section, "Offered During Setup"):
> `` `setup-guide.md` Step 4 offers this skill during initial setup. Choosing yes runs the install flow above (skipping the backfill step since no pages exist yet). ``

`setup-guide.md` step numbering:
> `## Step 4 — Initialize Wiki Files` (creates `wiki/index.md`, `wiki/log.md`, `wiki/hot.md`, `memory.md`)  
> `## Step 4.5 — Offer SQLite Query Skill` (asks the user, then runs `!! install sqlite-query` if yes)

*Logical failure.* An operator or user reading SKILL.md's "Offered During Setup" note for context — e.g. to understand when and how the skill is offered — would look up "Step 4" in `setup-guide.md` and land on the wrong step (wiki-file initialization). The actual offer is in Step 4.5. The mismatch is minor (the correct step is adjacent) but is a misdirection in documentation specifically intended to help operators trace the setup flow. Same cross-reference drift class as S2 from audit #11 (directory diagram path mismatch).

*Recommended fix.* Update `SKILL.md` "Offered During Setup" from "Step 4" to "Step 4.5". One-word change; no logic impact.

---

**W2 — `blueprint/skills/sqlite-query/query-layer.md` returns glob patterns (`wiki/pages/**/<slug>.md`), not resolved file paths — violates the Query Layer Hook Contract in `ops/conventions.md`.**

*Evidence.*

`ops/conventions.md` §Query Layer Hook Contract:
> **Output:** a list of candidate page file paths for the agent to read, or `None` / empty list to trigger fallback to grep

`query-layer.md` Step 1 (Python, `if rows:` branch):
```python
candidate_paths = [f"wiki/pages/**/{row[0]}.md" for row in rows]
```

`query-layer.md` Step 2:
> **If `candidate_paths` is populated:** read those pages and synthesize the answer. Skip the grep fallback.

`ops/query.md` Step 2:
> If `scheduled-tasks/query-layer.md` exists, read it and follow its instructions to find candidate pages — it returns a list of page paths.

*Logical failure.* The hook contract declares the output must be "candidate page file paths." The implementation returns glob patterns of the form `wiki/pages/**/<slug>.md`. The wiki has four concrete subdirectories (`concepts/`, `entities/`, `sources/`, `analyses/`), none of which is `**`. An agent using the `Read` tool on a path like `wiki/pages/**/cognitive-load.md` would receive a file-not-found error — the glob is never expanded. The agent would then either (a) silently fail the read and return an empty response, (b) fall through to grep without logging a warning, or (c) implicitly expand the glob via bash — but `ops/query.md` Step 4 ("Read the candidate pages") gives no instruction to expand globs before reading.

There is also an internal inconsistency: the comment on the same line says "Return list of (slug, title, summary) tuples to the agent" but the code builds path strings, not tuples — the comment describes the `rows` variable, not `candidate_paths`, but is positioned as if it describes the output.

The fallback path (exception → grep) is correctly wired and absorbs hard failures. But a silent failed read in the non-exception path would produce a wrong answer without triggering the fallback, because no exception is raised from a missing-path read — the agent simply receives no content.

*Recommended fix.* Replace the glob pattern with a direct database lookup of the page type, then construct a concrete path:

```python
rows = conn.execute("""
    SELECT DISTINCT p.slug, p.type, p.title, p.summary
    FROM pages p
    WHERE ...
""", ...).fetchall()

type_to_dir = {
    "concept": "concepts", "entity": "entities",
    "source": "sources", "analysis": "analyses"
}
candidate_paths = [
    f"wiki/pages/{type_to_dir.get(row[1], 'concepts')}/{row[0]}.md"
    for row in rows
]
```

This requires adding `p.type` to the SELECT — `type` is already in the schema — and using a `type_to_dir` mapping. Alternatively, use bash glob expansion in a separate step before passing paths to the read tool. Either way, the output must be concrete paths that the read tool can use without further processing.

*Hook contract update required.* `ops/conventions.md` §Query Layer Hook Contract currently says "file paths"; after this fix the note should add "must be fully resolved (no glob patterns) — the agent reads them directly without expansion."

---

**W3 — `blueprint/skills/sqlite-query/ingest-hook.md` error message directs the user to run `!! lint` to repair `wiki.db` desync; `!! lint` has no DB repair mechanism.**

*Evidence.*

`ingest-hook.md` (exception handler, last line of the except block):
```python
print(f"[sqlite-query] hook error for {slug}: {e} — wiki.db may be out of sync, run !! lint to repair")
```

`ops/lint.md` §Steps (checks performed):
> - Broken `[[wiki links]]`
> - Orphan pages
> - Stale claims
> - Contradictions
> - Missing cross-references
> - Data gaps
> - Missing `related:` field
> - Dangling `related:` slugs
> - Broken bidirectionality

*Logical failure.* `!! lint` checks wiki-page quality against `wiki/pages/` markdown files. It has no step that reads `wiki.db`, compares its rows against the markdown files, or reconciles them. A user following the error message would run `!! lint`, see a clean report (assuming the wiki pages themselves are fine), and conclude the problem is resolved — while `wiki.db` remains out of sync. Subsequent queries via the SQLite layer would then return stale or missing results, silently degrading to grep fallback on every query until the DB is repaired.

The correct recovery is the install-time backfill from `SKILL.md` Step 5: read every page in `wiki/pages/` and re-insert into `wiki.db`. There is no `!! repair` command today; the closest equivalent is re-running `!! install sqlite-query` which re-offers the backfill.

*Recommended fix.* Update the error message to:
```python
print(f"[sqlite-query] hook error for {slug}: {e} — wiki.db may be out of sync. To repair: say '!! install sqlite-query' and choose yes to the backfill offer (or run '!! uninstall sqlite-query' to revert to grep).")
```

Also worth adding a note to the `## Fallback Behaviour` section of `SKILL.md` and the `## Uninstall` section with the same repair guidance, so users who encounter desync through any path (not just ingest-hook exceptions) know the recovery route.

---

### STYLE

None. All files within documented headroom; no recalibration overruns; no envelope pressure.

---

## 3. Non-findings (considered and dismissed)

- **Cold-start total `~6,330`** — 6,250 (CLAUDE.md) + 80 (hot.md). ✓
- **`!! ready` total `~7,280`** — 6,330 + 950 (memory.md full). ✓
- **`!! wrap`/`!! ready` realistic costs `~3,000`/`~3,300`** — derivable from current token-reference component values. ✓
- **Three Approval Rule exceptions** — `!! wrap`, `!! ready`, `!! audit` enumerated consistently. ✓
- **Ingest atomic ordering** — Step 5 pre-compute → Step 6 mv → Step 7 page write. ✓
- **Hash canonicalization 6-step pipeline** — intact. ✓
- **`Pages: N` derived** — refresh-hot.md counts `^- [[` entries; not a stored counter. ✓
- **Blueprint-authoring mode guard** — present in CLAUDE.md, audit.md, `!! ready` step 5. ✓
- **Blueprint Sync Rule 12-row matrix** — intact; no new untriggered changes detected. ✓
- **SKILL.md install/uninstall symmetry** — file targets match; DB-keep option on uninstall correctly defaults to no. ✓
- **sqlite-query DB schema** — `pages` table, `relations` table, four indexes; `type` CHECK constraint; upsert pattern and bidirectional-relation INSERT OR IGNORE all correct. ✓
- **ingest-hook.md `type_` naming** — code uses `type_` (Python reserved-word avoidance); the "Values injected" comment lists `type_` consistently with the code; the Input section says `type` (no underscore) but the rename is clearly intentional and the code is unambiguous. Not flagged.
- **`refresh-hot.md` awk portability** — uses 1-argument `match()` form only; 3-argument GNU-awk form correctly avoided. ✓
- **`.gitignore` scope** — correctly scopes to inside `blueprint/`; setup-guide.md note accurately explains that `wiki/.obsidian/` is outside its reach. ✓
- **`ops/audit.md` scope parenthetical** — "currently `refresh-hot.md`" remains accurate after `changelog-monitor.md` removal (v2.0.11). ✓
- **CHANGELOG.md v2.0.11 envelope arithmetic** — all four row sums and total (56,545) verified correct. ✓
- **`ROADMAP.md`** — planning doc; not in audit scope.
- **`LICENSE`** — MIT; no issues.

---

## 4. Questions for Clarification

**Q1 — Should the `!! install sqlite-query` backfill path in `SKILL.md` Step 5 also be documented as the repair path for `wiki.db` desync?**

Currently the only documented desync recovery is the error message in `ingest-hook.md` (which misdirects to `!! lint`). Adding a "DB desync recovery" note to `SKILL.md §Fallback Behaviour` (which today only describes runtime query fallback) would give operators a single authoritative source for all failure-mode recoveries. Depends on whether W3 is accepted.

---

## 5. Architectural Invariants Verified

All 11 invariants from audits #11 and #12 re-verified:

1. Hash canonicalization: 6-step pipeline (preamble-strip → CRLF→LF → whitespace collapse → blank-line collapse → trim → SHA-256[:8]). Consumers reference the single canonicalizer. ✓
2. Ingest rerun-proof: Step 0 hash check before any write; short-circuits on match. ✓
3. Ingest atomic ordering: Step 5 `ts` pre-compute → Step 6 `mv inbox→raw` → Step 7 source-page write. ✓
4. `Pages: N` is derived (count of `^- [[` lines in index.md), never stored. ✓
5. Blueprint-authoring mode guard: skip log append and `hot.md` refresh when `wiki/` absent; checked in template/CLAUDE.md and ops/audit.md step 5. ✓
6. Versioning split: `X.Y` in CLAUDE.md footer and hot.md Schema; `X.Y.Z` in CHANGELOG only. ✓ (footer reads `Schema version: 2.0`)
7. Three Approval Rule exceptions enumerated identically in `template/CLAUDE.md`, `README.md`, and `user-guide.md`. ✓
8. `token-reference.md` source of truth; `ops/audit.md:72` envelope declared to derive from its Tokens column sum. ✓
9. Recalibration Rule carries three triggers: hard (measured ≥ documented), soft (headroom < 3% of measured actual), envelope cushion floor (cushion < 2% of upper bound). ✓
10. Blueprint Sync Rule 12-row matrix governs downstream propagation; audit-driven edits use `audit | …` log label. ✓
11. sqlite-query skill follows Query Layer Hook Contract and Ingest Hook Contract in `ops/conventions.md` — with the exception flagged as W2 (glob patterns vs. resolved paths). ✗ partially

---

## 6. Verdict

**The v2.0.11 blueprint has three WARNING-class findings and no CRITICAL or STYLE issues. No architectural regressions.**

The ingest pipeline, approval flow, hash canonicalization, Blueprint Sync Rule, and Recalibration Rule are all structurally intact. All prior findings from audits #11 and #12 are clean. Headroom across all 18 tracked files is healthy; no recalibration is due.

The three warnings are all confined to the sqlite-query skill bundle, which was added in v2.0.11 and received its first independent audit in this pass. None of the warnings are regressions from the core schema.

**Priority order for follow-up:**

1. **W2** — Fix `query-layer.md` to return resolved file paths instead of glob patterns; update `ops/conventions.md` Query Layer Hook Contract to explicitly prohibit glob patterns in output. This is the only finding that could cause a silent wrong-answer failure in production use.
2. **W3** — Update `ingest-hook.md` error message to point at the correct repair path (backfill via `!! install sqlite-query`); add desync-recovery note to `SKILL.md §Fallback Behaviour`.
3. **W1** — Update `SKILL.md` "Offered During Setup" from "Step 4" to "Step 4.5". One-word fix.

All three are confined to `blueprint/skills/sqlite-query/` files and `ops/conventions.md`. Blueprint Sync Rule "New skill bundle added" cascade applies to conventions.md edits. A single patch entry (v2.0.12) covers all three.

Read-only audit complete. No fixes applied. No `wiki/log.md` entry, no `hot.md` refresh (blueprint-authoring mode).
