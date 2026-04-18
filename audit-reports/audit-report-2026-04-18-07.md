# Audit Report — 2026-04-18 (#7)

**Operation:** `!! audit all` (read-only blueprint-authoring audit)
**Scope:** Every tracked file under `blueprint/` — `README.md`, `setup-guide.md`, `user-guide.md`, `troubleshooting.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore`, and the full `template/` tree (`CLAUDE.md` + `scheduled-tasks/refresh-hot.md`, `changelog-monitor.md`, and `ops/*.md`).
**Mode:** Blueprint-authoring (no `wiki/` present at workspace root — `hot.md` refresh and `log.md` append correctly skipped per `CLAUDE.md` Blueprint-authoring Mode rule).
**Prior audit reports reviewed:** `audit-report-2026-04-18.md` through `audit-report-2026-04-18-06.md` (six prior reports; audit #6's W1–W4 all landed in v2.0.6).

---

## Chain of Verification

1. Read all six prior audit reports end-to-end and recorded the disposition of every CRITICAL / WARNING / STYLE / Question item to avoid re-flagging resolved issues.
2. Read every file in scope in full: `blueprint/README.md`, `setup-guide.md`, `user-guide.md`, `troubleshooting.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore`, `template/CLAUDE.md`, `template/scheduled-tasks/refresh-hot.md`, `changelog-monitor.md`, and all seven `ops/*.md` files (`ingest.md`, `lint.md`, `query.md`, `update.md`, `conventions.md`, `audit.md`, `token-reference.md`).
3. Verified audit #6's W1–W4 are landed:
   - `user-guide.md:14` now reads `~6,280 tokens` (W1 fixed).
   - `user-guide.md:94` now reads `~30,000–45,000 tokens` (W2 fixed).
   - `ingest.md:64` now uses the inline parenthetical as the canonical source with a positive cross-reference to `changelog-monitor.md` Step 3 (W3 fixed).
   - `ops/audit.md:71` now quotes `~30,000–45,000`, cascaded to `user-guide.md:215` (W4 fixed).
4. Ran `wc -c` on every tracked file and recomputed the per-file 110% headroom ratio (documented Chars ÷ measured actual):
   - `refresh-hot.md` 3,966 / 4,400 → 10.9% ✓
   - `token-reference.md` 5,408 / 6,000 → 10.9% ✓
   - `ops/audit.md` 6,207 / 6,600 → 6.3%
   - `ops/ingest.md` 14,247 / 15,500 → 8.8%
   - `CHANGELOG.md` 34,910 / 38,500 → 10.3% ✓
   - All other rows checked — within headroom (no Chars value exceeded).
5. Re-derived the `!! audit all` envelope from the `token-reference.md` Tokens column (per the source-of-truth directive at `ops/audit.md:71`). Blueprint-doc rows: README 1,280 + setup-guide 3,350 + user-guide 4,150 + troubleshooting 6,980 + CHANGELOG **9,620** + LICENSE 300 = **25,680**. Template-side rows: CLAUDE 5,475 + refresh-hot 1,100 + changelog-monitor 1,530 + ingest 3,880 + lint 630 + query 530 + update 350 + conventions 1,250 + audit 1,650 + token-reference 1,500 = **17,895**. **Total: ~43,575 tokens**, inside the new 30,000–45,000 envelope ✓.
6. Verified architectural invariants still hold: rerun-proof ingest (Step 0 hash check), atomic ingest ordering (Step 5 pre-compute `ts` → Step 6 move → Step 7 source-page write), hash canonicalization pipeline (preamble-strip → CRLF/CR→LF → whitespace collapse → blank-line collapse → trim → SHA-256[0:8]) shared by `ingest.md` Step 0 and `changelog-monitor.md` Step 3, derived `Pages:` counter (`^- \[\[` count, not a stored Stats header), detector-only monitor (`!! ingest` as sole writer), Blueprint-authoring Mode guards, versioning split (footer tracks X.Y; patches bump X.Y.Z without moving footer), and Blueprint Sync Rule matrix.
7. Verified every documented exception to the Approval Rule (`!! wrap`, `!! ready`, `!! audit`) is still explicitly listed in `CLAUDE.md`'s Approval Rule section and still matches `user-guide.md` / `README.md`.
8. Grepped the whole blueprint for token-reference cross-file inconsistencies. Found:
   - A single `~1,030` occurrence inside `token-reference.md` itself that contradicts the file's own table row of `~1,100` for `refresh-hot.md` (W1).
   - The v2.0.6 envelope-widening prose in `CHANGELOG.md:48` claims "(≈110% of current documented sum, rounded to nearest 1,000)" — arithmetic does not match (W2).
9. Cross-checked the Recalibration Rule's Step 4 propagation list (`token-reference.md:78`) against the places the `!! audit all` envelope is quoted (`ops/audit.md:71`, `user-guide.md:94`, `user-guide.md:215`, plus the CHANGELOG) — Step 4 mentions only cold-start cascade targets, not envelope targets (S1).
10. Re-examined the v2.0.6 justification phrasing for the 45,000 envelope upper bound (`ops/audit.md:71` and `CHANGELOG.md:48–52`) — the two documents give subtly different explanations of *why* 45,000 (S2).

---

## Findings

### CRITICAL
None. Every architectural invariant from v2.0.2 through v2.0.6 remains intact. No data-loss, approval-bypass, or schema-divergence issue detected.

---

### WARNING

#### W1 — `token-reference.md` contradicts itself on the `refresh-hot.md` read cost

**File:** `blueprint/template/scheduled-tasks/ops/token-reference.md`
**Severity:** WARNING (intra-file self-contradiction)

The File Read Costs table at line 22 documents `refresh-hot.md` as `~4,400 chars / ~1,100 tokens`:

> `scheduled-tasks/refresh-hot.md` | ~4,400 | ~1,100

But the "true session cost" note 32 lines later at line 54 quotes a different value for the same file:

> Both commands also execute the full `hot.md` refresh flow (read `refresh-hot.md` **~1,030** + re-read `wiki/index.md` ~200 + re-read `wiki/log.md` tail ~625) …

`~1,030` appears nowhere else in the blueprint — it is stale inside the same file that documents `~1,100` as the canonical value. Measured actual today is 3,966 chars / ~992 tokens; the 1,100 figure is the 110%-headroom documented value, and 1,030 is a historical measured-actual leftover that was never updated when the table was last recalibrated.

The downstream "~2,700 tokens for `!! wrap` / ~2,800 for `!! ready`" realistic-cost figures in the same paragraph are derived from the 1,030 figure (`1,030 + 200 + 625 + 100 + 600–900 = 2,555–2,855`, midpoint ≈ 2,700). Using the canonical 1,100 gives 2,625–2,925, midpoint ≈ 2,775 → round-up quoted value should be ~2,800 / ~2,825 respectively.

Without a fix, a reader who scans line 22, remembers 1,100, then reads line 54 will wonder whether one of the numbers is wrong. Worse, if an agent is asked "how much does `!! wrap` cost?" the answer depends on which line it reads first.

**Recommended fix:** Reconcile line 54 with line 22 — change `~1,030` → `~1,100`, and update the downstream realistic-cost figures (`~2,700` → `~2,800`, `~2,800` → `~2,825` or similar). Alternatively, if line 54 deliberately uses measured actuals rather than documented-with-headroom values (so that "realistic per-command cost" is genuinely the realistic number, not the conservative one), add an explicit note saying so — but then the 1,030 still drifts against today's measured 992 and should be updated either way.

---

#### W2 — v2.0.6 CHANGELOG prose miscomputes the envelope's "≈110% of documented sum" claim

**File:** `blueprint/CHANGELOG.md:48`
**Severity:** WARNING (prose-arithmetic mismatch in the document that explains *why* the envelope is 45,000)

The v2.0.6 entry justifying the envelope widen says:

> Widened to `~30,000–45,000` (**≈110% of current documented sum, rounded to nearest 1,000**) in `audit.md:71`, cascaded to `user-guide.md:215` and `user-guide.md:94` (W2).

Re-deriving from the same CHANGELOG entry (which on line 62–63 reports the post-v2.0.6 sum as `~43,575`):

- Documented sum: **43,575**
- 110% of sum: 43,575 × 1.10 = **47,933** → rounds to **48,000** at nearest-1,000
- Stated upper bound: **45,000**
- Actual ratio of upper bound to sum: 45,000 / 43,575 = **1.033 ≈ 103.3%**, not 110%

The prose is wrong — the upper bound is the documented sum plus a ~1,425-token (~3.3%) cushion, not the documented sum scaled to 110%. The companion phrasing in `ops/audit.md:71` ("the documented sum plus a small cushion, matching the 110% per-file headroom convention") is narrower and doesn't make the same arithmetic claim, but the CHANGELOG entry will be what a future editor reads when they try to understand whether 45,000 is still the right number.

This is load-bearing because the Recalibration Rule (`token-reference.md:74–79`) tells future editors to re-derive the envelope from the Tokens column. If the editor applies the "≈110% of documented sum" rule literally the next time the sum grows, they will bump the envelope far higher than intended — e.g., if the sum creeps to 48,000 they'll produce a 53,000 upper bound rather than the intended ~50,000.

**Recommended fix:** Change the parenthetical at `CHANGELOG.md:48` to match the `audit.md:71` framing, e.g. "(documented sum ~43,575 plus a ~1,425-token cushion, rounded to nearest 1,000)". Leave the `audit.md:71` prose as-is — it is already the less misleading of the two.

A deeper fix (Option B from audit #6's W4 discussion) is to re-point the source-of-truth directive at measured actuals rather than the documented Tokens column; but audit #6 chose Option A deliberately, and flipping now is its own cascade. Recommended to just repair the CHANGELOG prose.

---

### STYLE

#### S1 — Recalibration Rule Step 4 cascade list does not mention the `!! audit all` envelope

**File:** `blueprint/template/scheduled-tasks/ops/token-reference.md:78`
**Severity:** STYLE (procedural gap — the rule works by implication today but doesn't say so)

The Recalibration Rule Step 4 reads:

> 4. Propagate changes to any cascading cold-start estimates (CLAUDE.md, user-guide.md, README.md)

The `!! audit all` envelope is also derived from the Tokens column (per `ops/audit.md:71`'s source-of-truth directive). When the blueprint-doc or template-side sum changes enough to cross the 45,000 upper bound, Step 4 gives the editor no instruction to re-check the envelope — they'd have to notice the implication themselves. The v2.0.6 entry at `CHANGELOG.md:61–64` actually did the envelope check correctly ("new `!! audit all` envelope total is ~43,575, still inside the widened 30,000–45,000 range"), but that was done by the editor applying their own judgment, not by following Step 4.

The current cushion is small (1,425 tokens / ~3.3%). One more CHANGELOG section or an ingest that lands a large new op file could push the sum over 45,000 without any cascading doc change, and Step 4 as written would not flag it.

**Recommended fix (pick one):**
- **Minimal:** Add a bullet to Step 4 — "also verify the `!! audit all` envelope at `ops/audit.md:71` still contains the updated Tokens-column sum; widen if it doesn't." (≈1 line.)
- **Structural:** Split the Recalibration Rule into two phases — (a) per-file Chars recalibration, (b) aggregate checks (cold-start cascade + envelope). The aggregate phase then owns both cascades explicitly. (≈6 lines; cleaner but larger edit.)

Not a correctness issue today. Flagged as STYLE because the rule is silent on a real cascade the next editor will need to follow.

---

#### S2 — `audit.md:71` and `CHANGELOG.md:48` give subtly different methodologies for the same 45,000 upper bound

**File:** `blueprint/template/scheduled-tasks/ops/audit.md:71` and `blueprint/CHANGELOG.md:48`
**Severity:** STYLE (same number, two explanations — harmless today, a drift risk tomorrow)

`ops/audit.md:71` frames the 45,000 as:

> the ~45,000 upper bound is the documented sum plus a small cushion, matching the 110% per-file headroom convention.

`CHANGELOG.md:48` frames the same number as:

> ≈110% of current documented sum, rounded to nearest 1,000.

These are not the same methodology: "documented sum + small cushion" is additive; "110% of documented sum" is multiplicative. Today 45,000 happens to be a valid output of "additive cushion" only, not of "110% of sum" (see W2), so the CHANGELOG framing is wrong.

Independent of the W2 arithmetic repair, there is a meta-point: keeping two different methodology explanations for the same number in two docs will eventually cause a recalibration to apply one rule in one place and the other rule in the other. The blueprint's Blueprint Sync Rule matrix already has a pattern for this (single source of truth + cascading targets) — the envelope-methodology prose is a natural candidate for that treatment.

**Recommended fix (if touched):** After fixing W2, promote `ops/audit.md:71`'s methodology ("documented sum plus a small cushion") as canonical and have `CHANGELOG.md` either paraphrase it or reference it. No action needed if only W2 is fixed surgically, but worth noting as a convention.

---

## Questions for Clarification

### Q1 — Per-file schema-version footer parity (carried forward from audits #3, #4, #5, #6)

`template/scheduled-tasks/changelog-monitor.md:92` still ends with a `<!-- Schema vX.Y -->`-style footer; `refresh-hot.md` and the seven `ops/*.md` files still do not. Unresolved across four audits.

Two consistent answers are still available:
- **Normalize up:** every template file gets a schema footer (aligns with the "single source of truth" philosophy of the Blueprint Sync Rule).
- **Normalize down:** `changelog-monitor.md` drops its footer (aligns with the fact that the canonical version lives in `CLAUDE.md` and `hot.md`, and per-file footers are a parallel source that must be kept in sync).

If neither normalization is desired, a one-line comment in `CLAUDE.md` or `conventions.md` explaining *why* the asymmetry exists would close the question permanently.

---

## Verdict

**PASS with minor drift.** The blueprint is architecturally sound. All four of audit #6's WARNINGs (W1–W4) landed cleanly in v2.0.6 and propagated to the right downstream docs. The v2.0.6 envelope widen is correctly valued (45,000 comfortably contains the current 43,575 sum), the ingest.md:64 dangling cross-reference is fully repaired with a helpful positive pointer, and the cold-start cascade is fully consistent.

The two new WARNINGs are both low-risk prose-arithmetic defects:
- **W1** is an intra-file inconsistency inside `token-reference.md` (1,030 vs 1,100) — surgical one-line repair, plus optional realistic-cost number refresh.
- **W2** is a prose error in the v2.0.6 CHANGELOG entry ("≈110% of documented sum" is actually 103.3%) — surgical parenthetical rewrite.

The two STYLEs point at real procedural gaps that don't hurt today:
- **S1** — Recalibration Rule doesn't mention the envelope cascade. Small additive fix.
- **S2** — two docs explain the same number with two different formulas. Should be reconciled when W2 is touched.

**Q1** has now survived four audits unresolved. Neither direction (normalize up, normalize down, or document the asymmetry) is hard to land — this is a call that costs more to carry than to close.

**Token cost of this audit pass:** ~43,575 tokens of blueprint reads (per the v2.0.6 envelope) + ~23,000 tokens of prior audit reports + ~1,000 tokens overhead ≈ **~67,000 tokens this session**. Within context budget; no up-front warning was needed.

**Recommended next action:** If you want me to fix, the minimum viable patch is W1 (reconcile `token-reference.md` line 54 with line 22) + W2 (repair the v2.0.6 CHANGELOG parenthetical). Both are single-line string replacements. S1 and S2 are worth doing in the same pass but optional. Q1 needs a direction from you before I can apply anything. Per the audit op's read-only contract, I will wait for explicit approval before touching any file.
