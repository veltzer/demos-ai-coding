# Demo 03: plan.md first

```bash
./run.sh          # interactive, pauses between steps so you can talk
./run.sh --yes    # unattended dry run (no pauses, prepared decisions)
MODEL=claude-sonnet-5-5 ./run.sh
```

## What happens

One sentence of feature request, two fresh copies of a tiny expense tracker:

- **A, just do it**: the AI codes immediately.
- **B, plan first**: the AI writes `plan.md` only, including an
  *Open questions & assumptions* section. You correct it, then it implements
  the plan.

Both are scored by `acceptance/check.py`, which encodes what the "product
owner" meant but never said. The AI never sees it.

Then **A, round 2** gets the same corrections B got (`decisions.md`), but
as review feedback on code that already exists. The scoreboard shows time,
tokens in/out and cost per step. A's round-2 row, plus the round-1 lines it
throws away, is **the cost of the bad decisions**.

## The traps in the data (`app/expenses.csv`)

| Trap | Intended answer |
|------|-----------------|
| `food`, `Food`, ` FOOD ` | one category |
| negative amounts | refunds, subtract them |
| `fun` nets to 0.00 | hide it |
| `books` and `transport` both 40.00 | ties break alphabetically |
| no `--month` given | latest month *with data*, not today's month |

## Talking points

- At the review step, point out which traps the plan already flagged in its
  open questions. Fixing a sentence takes 30 seconds; finding the same bug in
  A's code means reading a diff.
- A usually scores lower **because it guessed, not because it is a worse
  coder**. The plan turns hidden guesses into visible questions. Often B's
  plan picks the *same* wrong defaults as A, but you can see them in the
  plan and fix them for free.
- Tokens in vs tokens out: every turn re-reads the whole conversation, so
  input tokens grow with each round of rework. That is why late corrections
  cost more than early ones.
- Planning is not overhead: B's total is usually at or below A's total
  once the rework is counted. B also leaves behind `plan.md`, a reviewed
  record of the decisions that a new session (or a colleague) can pick up.
- **The review step tells you what to fix.** A quick check (Haiku, set
  `REVIEW_MODEL=` to change it) compares `plan.md` with `decisions.md` and
  prints lines like
  `- Default month: plan says "defaults to the current month" -> change to "…"`.
  Press `e` (the default) to edit in `$EDITOR`. The check runs again
  and says `✔ plan.md agrees with every decision` once you have covered
  everything. `p` appends `decisions.md` instead; `c` carries on as is.
  The check is a presenter aid and is not counted in the scoreboard.
- **Show the plan file itself.** It is always at
  `/tmp/demo-03_importance_of_planning/B-plan-first/plan.md`, and the script
  prints that path when the plan is written. Open it in another window or your editor at any
  pause.

## Files

- `app/`: the seed app, copied fresh on every run (originals never change)
- `acceptance/check.py`: the hidden scoring
- `decisions.md`: the review corrections appended to `plan.md`
- Work copies go to `/tmp/demo-03_importance_of_planning/` (reset on every
  run): `A-just-do-it/` and `B-plan-first/`. Set `WORKDIR=` to put them elsewhere.
