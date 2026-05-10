# meta:run-session Substantiation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the skeleton `meta/run-session/SKILL.md` with a working three-phase procedure (Open → Work → Close) incorporating the grilling pattern as the pre-work alignment step.

**Architecture:** Single file edit — `meta/run-session/SKILL.md`. Frontmatter bumped to `draft` / `v0.1.0`. Procedure section replaced with fully specified three-phase content. Checklist and anti-patterns expanded to match.

**Tech Stack:** Markdown. No scripts, no tests in the traditional sense. Verification is a manual checklist diff between the spec and the written skill file.

---

### Task 1: Verify current file state and spec coverage

**Files:**
- Read: `meta/run-session/SKILL.md`
- Read: `docs/superpowers/specs/2026-05-10-meta-run-session-design.md`

- [ ] **Step 1: Read the current SKILL.md**

Open `meta/run-session/SKILL.md`. Confirm it is at `status: skeleton`, `version: 0.0.1`, and that the Procedure section contains `*TODO: skeleton.*`.

- [ ] **Step 2: Read the design spec**

Open `docs/superpowers/specs/2026-05-10-meta-run-session-design.md`. Confirm all three phases (Open, Work, Close) are present with their full content.

- [ ] **Step 3: Run the coverage diff (mental checklist)**

Verify the spec contains each of the following — these are the items that must appear in the new SKILL.md:

```
Open phase:
  [ ] Step 1 — Create session file (frontmatter, status: in-progress, Goal section)
  [ ] Step 2 — Read context (GOALS.md, ROADMAP.md, .ai/ACTIVE.md)
  [ ] Step 3 — Pre-work alignment table (5 session types x their pre-work variant)

Work phase:
  [ ] Dispatch table (5 session types x what to do)
  [ ] Mid-session rule: no .ai/wiki/ or lessons/ writes

Close phase:
  [ ] Step 1 — Complete session file body + set status: complete
  [ ] Step 2 — Log decisions to DESIGN_NOTES.md
  [ ] Step 3 — Capture lessons via Memex capture-lesson
  [ ] Step 4 — Propose wiki entries via Memex propose-wiki-entry
  [ ] Step 5 — Update ROADMAP.md and .ai/ACTIVE.md
  [ ] Step 6 — Session-close commit

Checklist:
  [ ] Open section (3 items)
  [ ] Work section (2 items)
  [ ] Close section (6 items)

Anti-patterns:
  [ ] Skipping pre-work alignment
  [ ] No written artifact at session end
  [ ] Writing wiki/lessons mid-session
  [ ] Batching close steps out of order
```

All items should be present. If any are missing from the spec, stop and flag before continuing.

---

### Task 2: Write the new SKILL.md

**Files:**
- Modify: `meta/run-session/SKILL.md` (full rewrite of procedure, checklist, anti-patterns, references; frontmatter bump)

- [ ] **Step 1: Update the frontmatter**

Change the following fields only — leave `id`, `slug`, `name`, `type`, `owner`, `created` untouched:

```yaml
status: draft
version: 0.1.0
updated: 2026-05-10
sources:
- wiki:grilling-pattern
- wiki:adr-selectivity-threshold
```

- [ ] **Step 2: Keep Purpose, When to use, Inputs, Outputs unchanged**

These sections are accurate and don't need editing. The Outputs section references `wiki/` — update that reference to `.ai/wiki/` since dogfood replacement is complete:

```markdown
## Outputs

- Session file in `sessions/notes/`.
- Decisions in `DESIGN_NOTES.md`.
- Proposed wiki entries (status `proposed`) in `.ai/wiki/`.
- Lessons in `lessons/inbox/` (AI) or `lessons/feedback/` (user).
- Updated `ROADMAP.md` and `.ai/ACTIVE.md`.
```

- [ ] **Step 3: Replace the Procedure section**

Replace everything from `## Procedure` through the end of the old checklist with the new three-phase content. The full replacement text:

````markdown
## Procedure

### Phase 1 — Open

**Step 1 — Create session file.**
Open `sessions/notes/YYYY-MM-DD-<slug>.md` with correct frontmatter per `docs/SESSION_FORMAT.md`. Set `status: in-progress`. Write the Goal section immediately — even a rough sentence. This is the commitment that the session produces something.

**Step 2 — Read context.**
Read `GOALS.md`, `ROADMAP.md`, `.ai/ACTIVE.md`. Read any sources or prior session files the user or roadmap references. If the answer is in the files, read it — do not ask the user for information the codebase already contains.

**Step 3 — Pre-work alignment (type-conditional).**

| Session type | Pre-work step |
|---|---|
| **Design** | Full grilling per `wiki:grilling-pattern` — one question at a time, recommended answer with each, stop only when the design decision tree is fully resolved. "Let's just start" is not an acceptable stopping condition. |
| **Review** | Full grilling — establish what is being reviewed, what criteria apply, and what a good outcome looks like before reading the target. |
| **Research** | Scoping step — establish the research question and success criteria before opening any sources. One or two questions max. |
| **Experiment** | Scoping step — establish the hypothesis and what a conclusive result looks like. One or two questions max. |
| **Reflection** | Minimal opener — one question: "What are we reflecting on, and why now?" Sufficient to anchor the session. |

---

### Phase 2 — Work

Dispatch table. `meta:run-session` does not define the work content; it delegates to the right skill or approach.

| Session type | What to do |
|---|---|
| **Design** | Invoke `superpowers:brainstorming`. Return to Phase 3 when the spec is approved and committed. |
| **Research** | Invoke `meta:ingest-source` for each source in scope. Return to Phase 3 when all sources are analyzed. |
| **Review** | Read the target (skill, spec, session, wiki entry). Write critique and findings directly in the session file under a `## Review` section. |
| **Experiment** | Run the experiment. Document results, surprises, and what was learned in the session file under `## Results`. |
| **Reflection** | Free-form discussion. Document the key insights that emerged in the session file under `## Insights`. |

**Rule:** Do not write to `.ai/wiki/` or `lessons/` mid-session. All wiki entries and lessons queue for Phase 3.

---

### Phase 3 — Close

**Step 1 — Complete the session file body.**
Write or finalize all sections per `docs/SESSION_FORMAT.md`: Goal, Inputs, Discussion, Decisions, Proposed wiki entries, Lessons captured, Next. Set `status: complete`.

**Step 2 — Log decisions to `DESIGN_NOTES.md`.**
Any decision that meets the ADR threshold (`wiki:adr-selectivity-threshold`) gets a `DESIGN_NOTES.md` entry. Update the session file's `decisions-logged` frontmatter field.

**Step 3 — Capture lessons.**
Invoke the Memex `capture-lesson` skill for any lessons from this session. AI-noticed observations → `lessons/inbox/`. User-stated feedback → `lessons/feedback/`. Update the session file's `lessons-captured` frontmatter field.

**Step 4 — Propose wiki entries.**
Invoke the Memex `propose-wiki-entry` skill for any entries this session surfaced. Do not write directly to `.ai/wiki/` — the propose/review gate is not optional. Update the session file's `wiki-entries-proposed` frontmatter field.

**Step 5 — Update roadmap and active focus.**
Mark completed items in `ROADMAP.md`. Add any new items that emerged. Update `.ai/ACTIVE.md` to reflect the new current focus.

**Step 6 — Commit.**
Commit the session file, `DESIGN_NOTES.md` changes, lesson files, proposed wiki entries, and roadmap changes together as a single session-close commit.

## Checklist

**Open:**
- [ ] Session file created with correct frontmatter and `status: in-progress`.
- [ ] `GOALS.md`, `ROADMAP.md`, `.ai/ACTIVE.md` read.
- [ ] Pre-work alignment complete for session type.

**Work:**
- [ ] Delegated to appropriate skill or approach for session type.
- [ ] No wiki or lesson files written mid-session.

**Close:**
- [ ] Session file body complete; `status: complete`.
- [ ] Decisions logged to `DESIGN_NOTES.md`.
- [ ] Lessons captured via Memex `capture-lesson`.
- [ ] Wiki entries proposed via Memex `propose-wiki-entry`.
- [ ] `ROADMAP.md` and `.ai/ACTIVE.md` updated.
- [ ] Session-close commit made.

## Anti-patterns

- **Skipping pre-work alignment under pressure.** "Let's just start" is the #1 failure mode — grilling is the work.
- **No written artifact at session end.** If `sessions/notes/` has no file, the session did not happen.
- **Writing wiki entries or lessons mid-session.** All wiki and lesson work queues for Phase 3.
- **Batching the close steps out of order.** Each Phase 3 step depends on the previous — do them in sequence.
````

- [ ] **Step 4: Update the References section**

Replace the old References section with:

```markdown
## References

- `FOUNDATION.md` (principle 6) — every session ends with a written artifact.
- `docs/SESSION_FORMAT.md` — session file format and lifecycle.
- `wiki:grilling-pattern` — pre-work alignment discipline for design/review sessions.
- `wiki:adr-selectivity-threshold` — governs which decisions get logged to `DESIGN_NOTES.md`.
- Memex `capture-lesson` skill — close-phase lesson capture.
- Memex `propose-wiki-entry` skill — close-phase wiki entry proposal.
```

- [ ] **Step 5: Commit**

```
git add meta/run-session/SKILL.md
git commit -m "feat: substantiate meta:run-session — three-phase procedure v0.1.0"
```

---

### Task 3: Post-write verification

**Files:**
- Read: `meta/run-session/SKILL.md` (after edit)

- [ ] **Step 1: Re-run the coverage checklist from Task 1 Step 3**

Read the updated SKILL.md. Tick off each item in the coverage checklist. Every item must be present. If any are missing, edit the file and re-verify before committing.

- [ ] **Step 2: Verify frontmatter**

Confirm:
```yaml
status: draft
version: 0.1.0
updated: 2026-05-10
sources:
- wiki:grilling-pattern
- wiki:adr-selectivity-threshold
```

- [ ] **Step 3: Verify no skeleton remnants**

Search the file for `TODO`, `skeleton`, `*TODO`. None should appear. If any remain, remove them.

- [ ] **Step 4: Confirm commit is clean**

Run `git status` in the worktree. Only `meta/run-session/SKILL.md` should be staged/modified. No other files.

---

## Notes for the implementer

- This is a single markdown file edit. There is no code to run, no tests to execute in the traditional sense. The "test" is the coverage checklist in Task 1 Step 3, re-run after writing in Task 3 Step 1.
- The worktree is `C:\Users\Howard\Documents\Skills\skill-atelier\.claude\worktrees\festive-ellis-ce7238`. All paths are relative to that root.
- Do not edit any other `meta/` skill files. This change is scoped to `run-session` only.
- The design spec is at `docs/superpowers/specs/2026-05-10-meta-run-session-design.md` in the second-brain-blueprint repo — read it if any procedure detail is unclear.
