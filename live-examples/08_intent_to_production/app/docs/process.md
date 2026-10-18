# How a change goes from intent to production

A change lives in `changes/<name>/`. The business writes `intent.md` there.
Each phase is done by a fresh session that reads the artifacts of the
earlier phases and leaves its own for the next one. The files are the only
memory, so write each artifact for a reader who was not there. Below,
`<change>` stands for `changes/<name>/`.

| # | Phase | Reads | Leaves |
|---|-------|-------|--------|
| 1 | Spec | `<change>/intent.md`, the code, `docs/` | `<change>/spec.md` |
| 2 | Plan | `<change>/spec.md`, the code | `<change>/plan.md` |
| 3 | Implement | `<change>/plan.md`, `<change>/spec.md` | code, `docs/architecture.md` |
| - | Preview (a person) | `## For the preview` in `plan.md` | `<change>/preview.md` |
| 4 | Unit tests | `<change>/spec.md`, the code | `tests/` |
| 5 | System test | `<change>/spec.md`, the code | `tests/system/`, `<change>/test-report.md` |
| 6 | Lint | the code | clean ruff |
| 7 | Code review | everything | `<change>/review.md` |
| 8 | Review fixes | `<change>/review.md` | fixes, ticked `review.md` |
| 9 | Deploy | `docs/deploy.md` | a release in production |

## 1. Spec

Turn the intent into `spec.md`, the design an engineer builds from. No
code. Start from how the system works today (`docs/architecture.md` and the
code) and describe the change against it: the new and changed rules; the
API changes, with request and response examples and every new error; how
the server enforces the rules without keeping state; the page (what shows
when, keyboard and screen-reader use, small screens); which modules change
and how; what must keep working exactly as before; and how each line of the
intent's "How we will know it worked" and "What must not change" will be
checked. End with **Open questions**: each one gets the decision you took,
so nothing blocks the next phase.

## 2. Plan

Turn `spec.md` into `plan.md`, an implementation plan. No code. The first
line is `# Plan: <title>`. Then 2 to 4 phases, each a heading
`## Phase N: <name>` followed only by task lines `- [ ] <task>`, 3 to 6
tasks each. Each phase ends with a task that verifies it by running
something, and leaves the game working. Verification uses what every
session has: `python3` (the tests, a throwaway script, a server started
with `--port 0` and driven with `urllib`) and `ruff`. No browser and no
other tools: how the page looks and feels is checked by a person at the
preview after phase 3, so list those checks under a final heading
`## For the preview` as plain bullets, not boxes. Writing new tests is
phase 4 of this process, not part of this plan, but the existing tests
must keep passing after every phase.

## 3. Implement

Implement the first phase of `plan.md` that still has unchecked boxes, and
only that phase. Tick each box (`- [ ]` to `- [x]`) as soon as its task is
done, one edit per task. Follow `spec.md`. If you must depart from it,
update `spec.md` so the two agree. Keep `docs/architecture.md` true. Do not
write new tests yet, but run the existing ones. If a verify task asks for
something you cannot run, do the part you can, tick it, and add what is
left to `## For the preview`.

## Preview (done by a person)

A person runs the change on a preview server, goes through
`## For the preview`, and records the result in `preview.md`: who, when,
and what passed or failed. That file is the sign-off for everything only a
browser can show. Later phases read it; they do not repeat those checks.

## 4. Unit tests

Write pytest tests in `tests/` for every rule in `spec.md`, next to the
existing ones: every new rule, every new error, and every "must not change"
promise of the intent. Call the code directly, not over the network. Run
the whole suite. If a test finds a bug, fix the code and say so in your
final message.

## 5. System test

Test the real system from the outside, extending `tests/system/`: start
`python3 -m tictactoe --port 0` as a process and, over HTTP, play the new
feature end to end, including the attempts the intent says must fail, and
show that the old game still behaves as before. Always stop the server,
even when a test fails. Run the whole suite. Write `test-report.md`: what
was tested, the result, and any bugs found and fixed.

## 6. Lint

Run `ruff check .` and `ruff format --check .`. Fix every finding in the
code, run the tests again, and stop when both are clean and the tests pass.
Never silence a finding (see `CLAUDE.md`).

## 7. Code review

Act as a reviewer who did not write this change. Read the intent, the spec,
the diff of the change (`git diff` against the commit before its spec) and
the code around it. Look for: bugs; gaps between intent, spec, code and
`docs/architecture.md`; rules that are not tested; security (the server
faces the internet and trusts no request); and accessibility. The browser
checks belong to `preview.md`: a problem it reports is a finding, but how
much a sign-off is worth (who looked, how closely) is for whoever releases
to judge, so say it in the verdict, not as a finding. Do not change any
code. Write `review.md`: one line per finding,

```markdown
- [ ] **blocker|major|minor** `path:line`: what is wrong, and why it matters
```

most severe first, then a one-paragraph verdict. If there is nothing to
report at some severity, say so; do not invent findings.

## 8. Review fixes

Fix every blocker and major finding in `review.md`, and the minors that
are cheap. Tick each finding as you fix it. Leave a finding you decide not
to fix unticked, with the reason after it. Add a test for every bug you
fix. Finish with the tests and lint clean.

## 9. Deploy

Follow `docs/deploy.md`.
