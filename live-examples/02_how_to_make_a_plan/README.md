# Demo 02: a checkbox plan, implemented phase by phase

```bash
./run.sh          # interactive, pauses after the plan and after each phase
./run.sh --yes    # unattended dry run
```

## What happens

Starting from an empty folder, the goal is a terminal Game of Life (`life.py`).

1. **Plan.** The AI writes `plan.md`: 3 to 5 `## Phase N` sections of
   `- [ ]` tasks, each phase ending with a verification task, plus a `Demo:`
   command. The script draws it as a checklist at 0%.
2. **Phases.** A loop starts a fresh AI session per phase: *do the first
   phase with unchecked boxes, tick each box the moment it is done, stop*.
   Each tick shows in the live log as a green `✔`. After every phase the
   checklist is redrawn, the progress bar moves, and the phase is committed.
3. **Run.** With every box ticked, the script runs the plan's `Demo:` command.

The loop stops if a session ticks nothing, or after 8 sessions.

## Talking points

- **The plan is the memory.** Every phase is a brand-new session that has
  never seen the previous one. It picks up the work from `plan.md` and the
  code alone. This is how long tasks survive context limits, crashes and
  "let's continue tomorrow".
- **Checkboxes make progress visible and checkable.** You can see at any
  moment what is done, what is next, and what the AI claims to have verified.
- **Verification is part of the plan.** Each phase ends with a check, so a
  box is ticked only when something passed, not when the AI feels done.
- **Natural review points.** One commit per phase
  (`git log --oneline` in the work dir); you can stop, review, edit the
  remaining plan and continue.
- At the plan step, press `e` to edit `plan.md` live in `$EDITOR`: cut a
  task or add one ("add a --speed option"). The next session follows the
  edited plan.
- Rehearsal numbers: 4 phases, 20 tasks, about 5 minutes and $1.20 in total.

## Files

- `start/`: the nearly empty starting folder
- The project is built in `/tmp/demo-02_how_to_make_a_plan/life/` (reset
  on every run). Open `plan.md` there in an editor during the demo to watch the boxes
  tick. Set `WORKDIR=` to put it elsewhere.
- Shared helpers in `../lib/`: `checklist.py` draws the plan, and
  `stream.py` shows the live ticks.
