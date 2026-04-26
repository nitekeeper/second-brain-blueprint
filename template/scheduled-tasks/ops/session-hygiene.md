# Session Hygiene — Post-Op Soft Block

Read this file when `SESSION_HEAVY` is set and the user issues a `!! command`
(other than `!! wrap`, `!! ready`, `!! proceed`).

---

## Intercept message

Reply with exactly this (substitute `[op]` and `[N]`):

```
⚠️  A !! [op] operation completed earlier in this session. Continuing will
reprocess ~[N] tokens of prior context on every turn.

  💾 !! wrap  — save context now, then start a new session
  🔄 !! ready — restore it next session

Say !! proceed to continue here anyway.
```

- Replace `[op]` with the op that set SESSION_HEAVY (ingest / lint / audit).
- Replace `[N]` with a rough estimate of prior session context tokens (sum of approximate chars typed and received ÷ 4).

---

## Post-op advisory block

Append to the final response of every `!! ingest`, `!! lint`, and `!! audit` op:

```
---
⚠️  Session advisory: This session has completed a !! [op] operation and the
context is now heavy. Starting a new session for follow-up work avoids
reprocessing this history on every turn.

Before you leave:
  💾 Say !! wrap to save a session snapshot.
  🔄 Say !! ready at the start of your next session to restore it.

To continue in this session anyway, say !! proceed.
---
```

Replace `[op]` with the completed op name.

---

## Flag behaviour

| Event | Effect on SESSION_HEAVY |
|---|---|
| `!! ingest` completes | Set |
| `!! lint` completes | Set |
| `!! audit` completes | Set |
| User says `!! proceed` | Clear |
| `!! wrap` or `!! ready` | No change (always allowed regardless of flag) |
| New session | Cleared automatically (flag is in-memory only) |
---
