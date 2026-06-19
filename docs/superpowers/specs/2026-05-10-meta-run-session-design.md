# Design: meta:run-session — substantive skill

**Date:** 2026-05-10  
**Repo:** skill-atelier (framework layer)  
**Status:** approved — ready for implementation

---

## Context

`meta:run-session` is the framework meta-skill that governs Skill Atelier collaboration sessions end-to-end. The current file is a skeleton (`status: skeleton`, `version: 0.0.1`). This design replaces it with a working procedure.

Sessions are the unit of forward motion in this framework. If a session ends without a written artifact in `sessions/notes/`, the session did not happen.

---

## Design decisions made during brainstorming

**Pre-work alignment varies by session type.**  
Full grilling (`wiki:grilling-pattern`) applies to design and review sessions. Research and experiment sessions get a lighter scoping step (establish research question + success criteria). Reflection sessions get a single opener question. Uniform grilling across all types would over-constrain lightweight session types.

**Design sessions delegate to `superpowers:brainstorming`; `meta:run-session` owns open and close.**  
The brainstorming skill is fully capable of running a design session end-to-end. `meta:run-session` wraps it: Phase 1 (open + pre-work), then delegate to brainstorming, then Phase 3 (close). The two skills coexist — brainstorming remains standalone.

**Triggered by skill description match, not CLAUDE.md mandate.**  
A mandatory CLAUDE.md entry would fire on every conversation including quick one-off tasks. The skill description is precise enough to match reliably when the user opens a genuine session.

**Session close references Memex skills by name.**  
The framework dogfoods Memex — that dependency is intentional. Abstracting "capture-lesson" and "propose-wiki-entry" into vague verbs would make the procedure harder to follow without adding value.

---

## Structure

Three-phase: **Open → Work → Close**. Open and Close are fully specified and shared across all session types. Work is a dispatch table — one line per type.

---

## Phase 1 — Open

Three steps before any work begins.

### Step 1 — Create session file

Open `sessions/notes/YYYY-MM-DD-<slug>.md` with correct frontmatter per `docs/SESSION_FORMAT.md`. Set `status: in-progress`. Write the Goal section immediately — even a rough sentence. This is the commitment that the session produces something.

### Step 2 — Read context

Read `GOALS.md`, `ROADMAP.md`, `.ai/ACTIVE.md`. Read any sources or prior session files the user or roadmap references. If the answer is in the files, read it — do not ask the user for information the codebase already contains.

### Step 3 — Pre-work alignment (type-conditional)

| Session type | Pre-work step |
|---|---|
| **Design** | Full grilling per `wiki:grilling-pattern` — one question at a time, recommended answer with each, stop only when the design decision tree is fully resolved. "Let's just start" is not an acceptable stopping condition. |
| **Review** | Full grilling — establish what is being reviewed, what criteria apply, and what a good outcome looks like before reading the target. |
| **Research** | Scoping step — establish the research question and success criteria before opening any sources. One or two questions max. |
| **Experiment** | Scoping step — establish the hypothesis and what a conclusive result looks like. One or two questions max. |
| **Reflection** | Minimal opener — one question: "What are we reflecting on, and why now?" Sufficient to anchor the session. |

---

## Phase 2 — Work

Dispatch table. `meta:run-session` does not define the work content; it delegates to the right skill or approach.

| Session type | What to do |
|---|---|
| **Design** | Invoke `superpowers:brainstorming`. Return to Phase 3 when the spec is approved and committed. |
| **Research** | Invoke `meta:ingest-source` for each source in scope. Return to Phase 3 when all sources are analyzed. |
| **Review** | Read the target (skill, spec, session, wiki entry). Write critique and findings directly in the session file under a `## Review` section. |
| **Experiment** | Run the experiment. Document results, surprises, and what was learned in the session file under `## Results`. |
| **Reflection** | Free-form discussion. Document the key insights that emerged in the session file under `## Insights`. |

**Rule across all types:** do not touch `.ai/wiki/` or `lessons/` mid-session. All wiki entries and lessons queue for Phase 3.

---

## Phase 3 — Close

Six steps, in order.

### Step 1 — Complete the session file body

Write or finalize all sections per `docs/SESSION_FORMAT.md`: Goal, Inputs, Discussion, Decisions, Proposed wiki entries, Lessons captured, Next. Set `status: complete`.

### Step 2 — Log decisions to `DESIGN_NOTES.md`

Any decision that meets the ADR threshold (`wiki:adr-selectivity-threshold`) gets a `DESIGN_NOTES.md` entry. Update the session file's `decisions-logged` frontmatter field.

### Step 3 — Capture lessons

Invoke the Memex `capture-lesson` skill for any lessons from this session. AI-noticed observations → `lessons/inbox/`. User-stated feedback → `lessons/feedback/`. Update the session file's `lessons-captured` frontmatter field.

### Step 4 — Propose wiki entries

Invoke the Memex `propose-wiki-entry` skill for any entries this session surfaced. Do not write directly to `.ai/wiki/` — the propose/review gate is not optional. Update the session file's `wiki-entries-proposed` frontmatter field.

### Step 5 — Update roadmap and active focus

Mark completed items in `ROADMAP.md`. Add any new items that emerged. Update `.ai/ACTIVE.md` to reflect the new current focus.

### Step 6 — Commit

Commit the session file, `DESIGN_NOTES.md` changes, lesson files, proposed wiki entries, and roadmap changes together as a single session-close commit.

---

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

---

## Anti-patterns

- **Skipping pre-work alignment under pressure.** "Let's just start" is the #1 failure mode — grilling is the work.
- **No written artifact at session end.** If `sessions/notes/` has no file, the session did not happen.
- **Writing wiki entries or lessons mid-session.** All wiki and lesson work queues for Phase 3.
- **Batching the close steps out of order.** Each Phase 3 step depends on the previous — do them in sequence.

---

## Skill file changes

The target file is `meta/run-session/SKILL.md`. Changes:

- Bump `status` from `skeleton` to `draft`.
- Bump `version` from `0.0.1` to `0.1.0`.
- Replace `*TODO: skeleton.*` procedure with the three-phase procedure above.
- Add the full checklist.
- Expand anti-patterns section.
- Update `sources` frontmatter field to reference `wiki:grilling-pattern` and key wiki entries.

No new files needed. No other `meta/` skills are touched by this change.

---

## References

- `wiki:grilling-pattern` — pre-work alignment discipline for design/review sessions.
- `wiki:adr-selectivity-threshold` — governs which decisions get logged to `DESIGN_NOTES.md`.
- `docs/SESSION_FORMAT.md` — session file format and lifecycle.
- `FOUNDATION.md` principle 6 — every session ends with a written artifact.
- Memex skills: `capture-lesson`, `propose-wiki-entry` — close-phase tooling.
