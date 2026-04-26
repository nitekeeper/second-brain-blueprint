# Design: AUD-2026-04-25-010 Fixes

**Date:** 2026-04-25
**Audit Report:** `audits/AUD-2026-04-25-010.md`
**Approach:** Audit recommendations verbatim — three targeted edits, one audit report update, single commit.

---

## Scope

| File | Action |
|---|---|
| `template/scheduled-tasks/ops/migrate.md` | Replace confusing v2.1→v2.3 preamble with direct description |
| `template/scheduled-tasks/ops/audit.md` | Replace single-mode token-estimate note with dual-mode bullet block |
| `template/scheduled-tasks/ops/blueprint-sync.md` | Update two cascade table rows |
| `audits/AUD-2026-04-25-010.md` | Mark all three findings RESOLVED; check off action items |

No new files. No Blueprint Sync Rule cascade — all fixes are STYLE corrections to instructional text only.

---

## Finding AUD-2026-04-25-039 — `migrate.md`

**Problem:** The v2.1→v2.3 section opens with "Run all steps from the v2.1→v2.2 migration (listed below)" — that section does not exist. The modification bullets reference "Step 3i / 3j" using a numeric prefix inconsistent with the lettered step scheme (a, b, c … i, j). The steps that follow already incorporate both modifications, so the preamble is simultaneously wrong and redundant.

**Fix:** Replace lines 125–131 (the preamble block) with a single direct description. The "On approval, execute in order" steps and all other content are untouched.

**Replace:**
```
Run all steps from the v2.1 → v2.2 migration (listed below), with two modifications:
- **Step 3i:** write `Schema: v2.3` (not `v2.2`) when patching `hot.md`
- **Step 3j:** append `## [YYYY-MM-DD] migrate | v2.1 → v2.3 — lean cold-start + wiki-first routing`

Because step 3c copies `CLAUDE.md` from `blueprint/template/CLAUDE.md`, which
already contains the v2.3 Query Routing Rule and v2.3 schema footer, the routing
patch and version bump are implicit.
```

**With:**
```
Direct migration path from v2.1 to v2.3 in a single step — no intermediate v2.2 stop required. Step c copies `CLAUDE.md` from `blueprint/template/CLAUDE.md`, which already contains the v2.3 Query Routing Rule and v2.3 schema footer, so no separate routing patch is needed. The steps below are the complete v2.1→v2.3 procedure.
```

---

## Finding AUD-2026-04-25-040 — `audit.md`

**Problem:** The Notes section's token-estimate command uses `scripts/estimate_tokens.py` and `blueprint/` path prefixes — both correct for deployed-user mode but wrong for blueprint-authoring mode (where `scripts/` is absent and files are at repo root). The `chars ÷ 4` manual fallback used by auditors since AUD-007 is undocumented.

**Fix:** Replace the single-line estimate sentence (line 96) with a dual-mode bullet block documenting both paths.

**Replace:**
```
For `!! audit all`, expect ~35,000–45,000 tokens of reads for the tracked files. Run `python scripts/estimate_tokens.py blueprint/README.md blueprint/setup-guide.md blueprint/user-guide.md blueprint/troubleshooting.md blueprint/template/CLAUDE.md blueprint/template/scheduled-tasks/refresh-hot.md blueprint/template/scheduled-tasks/ops/*.md blueprint/skills/sqlite-query/*.md blueprint/skills/claude-code-enhanced/*.md blueprint/docs/audit-report-template.md` for a live estimate. Warn the user up front if the session is already close to context limits.
```

**With:**
```
For `!! audit all`, expect ~35,000–45,000 tokens of reads for the tracked files.
- **Deployed-user mode:** `python scripts/estimate_tokens.py blueprint/README.md blueprint/setup-guide.md blueprint/user-guide.md blueprint/troubleshooting.md blueprint/template/CLAUDE.md blueprint/template/scheduled-tasks/refresh-hot.md blueprint/template/scheduled-tasks/ops/*.md blueprint/skills/sqlite-query/*.md blueprint/skills/claude-code-enhanced/*.md blueprint/docs/audit-report-template.md`
- **Blueprint-authoring mode** (`scripts/` absent): use `chars ÷ 4` as a manual estimate, or run `python template/scripts/estimate_tokens.py README.md setup-guide.md user-guide.md troubleshooting.md template/CLAUDE.md template/scheduled-tasks/refresh-hot.md template/scheduled-tasks/ops/*.md skills/sqlite-query/*.md skills/claude-code-enhanced/*.md docs/audit-report-template.md` from the repo root.

Warn the user up front if the session is already close to context limits.
```

---

## Finding AUD-2026-04-25-041 — `blueprint-sync.md`

**Problem:** Two cascade table rows are stale:
- "New scheduled task" row references `template/CLAUDE.md Directory Structure` (section does not exist in CLAUDE.md) and includes `ops/token-reference.md (removed in v2.2; skip)` noise. `ops/reference.md` is absent.
- "New skill bundle added" row omits `ops/reference.md`, which lists individual skill bundles and goes stale when a new one is added.

**Fix:** Update both rows in the cascade table (lines 20–21).

**"New scheduled task" row — replace:**
```
`blueprint/template/scheduled-tasks/<name>.md` + `ops/audit.md` (informational parenthetical) + `ops/token-reference.md` (removed in v2.2; skip) + `setup-guide.md` + `README.md` and `user-guide.md` if user-visible + `template/CLAUDE.md` Directory Structure + `CHANGELOG.md`
```

**With:**
```
`blueprint/template/scheduled-tasks/<name>.md` + `ops/audit.md` (informational parenthetical) + `setup-guide.md` + `README.md` and `user-guide.md` if user-visible + `ops/reference.md` (blueprint/ scheduled-tasks subtree) + `CHANGELOG.md`
```

**"New skill bundle added" row — replace:**
```
`blueprint/skills/<skill>/` + `blueprint/user-guide.md` + `blueprint/setup-guide.md` + `blueprint/ROADMAP.md` + `ops/conventions.md` if skill introduces a new hook contract
```

**With:**
```
`blueprint/skills/<skill>/` + `blueprint/user-guide.md` + `blueprint/setup-guide.md` + `blueprint/ROADMAP.md` + `ops/conventions.md` if skill introduces a new hook contract + `ops/reference.md` (blueprint/ skills subtree)
```

---

## Audit Report Updates — `audits/AUD-2026-04-25-010.md`

For each of the three findings, set `**Status**` field to `RESOLVED` in the finding table.

In the Action Items section, change all three `- [ ]` entries to `- [x]`.

---

## Commit Strategy

Single commit after all four files are updated:

```
fix: resolve AUD-039 through AUD-041 from AUD-2026-04-25-010
```

No wiki log append or hot.md refresh — blueprint-authoring mode, `wiki/` absent.
