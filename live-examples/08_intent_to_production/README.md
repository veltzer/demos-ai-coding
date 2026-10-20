# Demo 08: one feature from intent to production

```bash
./run.sh            # interactive: pauses after every phase
./run.sh --yes      # unattended dry run (nobody signs off the preview, so the deploy may refuse)
PREVIEW_PORT=8087 PROD_PORT=8088 ./run.sh
VIEW=0 ./run.sh     # terminal only, no browser windows
```

## What the audience sees

The browser carries the visuals, the terminal carries the sessions
(`pandoc` and `xdg-open` are required):

- **The pipeline**, before every stage: `pipeline.md` rendered with the
  stages done ticked and the current one highlighted.
- **Each session's prompt**, before it runs: the one line it gets and the
  tools it may use.
- **Each artifact as it lands**: `intent.md`, `spec.md`, `plan.md`,
  `test-report.md` and `review.md`, rendered with code highlighting.
- **The game**: production version 1 at the start, the preview server
  for your sign-off, and production with the cheat at the end.

The rendered pages are snapshots in the work dir's `view/`.

## What happens

**The start is a working product.** `app/` is a tic-tac-toe game for the
browser, with source and documentation. It has a drawn board, a mode
against the computer (Easy, or Hard, which never loses) or against a
friend, a highlighted winning line, a score, and keyboard play. The
repository holds Python rules and computer player, a stateless JSON API,
plain HTML/CSS/JS, 58 unit and system tests, a ruff config, `README.md`,
`docs/architecture.md`, `docs/process.md`, `docs/deploy.md` and the
platform team's `ops/deploy.sh`. The script deploys it to production
(`http://127.0.0.1:8088/`) first. Play it, and fail to beat Hard.

**The change is a cheat hack.** The business hands over `intent.md`, in
business language only. Typing the Konami code (↑ ↑ ↓ ↓ ← → ← → B A)
during a game against the computer unlocks one **steal** per game: one of
the computer's squares becomes yours. A game won that way counts
separately in the score. Without the code nothing changes, and nobody can
steal twice, not even with hand-made requests.

It goes into `app/changes/cheat-code/` and through nine phases. Each phase
is a fresh AI session whose whole prompt is "Do phase N of docs/process.md
for the change in changes/cheat-code/":

| # | Phase | Leaves | The script then checks |
|---|-------|--------|------------------------|
| 1 | Spec | `spec.md` | its outline; no code changed |
| 2 | Plan | `plan.md` | draws the checklist |
| 3 | Implement | code, `docs/architecture.md` | one session per plan phase, boxes tick live; old tests still pass |
| - | Preview (you) | `preview.md` | a **preview server**: try the cheat against the plan's preview list, then type your verdict, which is recorded as the sign-off |
| 4 | Unit tests | `tests/` | whole suite; any code the tests forced to change |
| 5 | System test | `tests/system/`, `test-report.md` | the real server over HTTP |
| 6 | Lint | clean code | ruff before and after, config untouched, no `# noqa` |
| 7 | Code review | `review.md` | the findings; the reviewer changed no code |
| 8 | Review fixes | ticked `review.md` | findings ticked, suite green |
| 9 | Deploy | release 2 | `ops/deploy.sh` gates, releases, smoke-tests; production now has the cheat |

Every phase is a commit (`git log` in the work dir shows the pipeline), and
the scoreboard shows time and cost per phase.

## Talking points

- **Start from a real codebase, not a blank page.** Most work is a change
  to something that runs. The spec phase reads `docs/architecture.md` and
  the code and describes the change against them; the docs are what make a
  one-line prompt enough.
- **Documentation carries the process.** What a spec must cover, what a
  review looks for and how to deploy are written once, in `docs/`. Change
  the process by editing a file, not by retyping prompts.
- **Artifacts are the memory.** No session sees the one before it. The spec,
  plan, test report and review are the hand-offs, and a human can read,
  correct or veto each one before the next phase.
- **The intent hides a design problem.** "Nobody can steal twice, even by
  hand" on a server that keeps no state: the spec has to work out how
  (counting marks on the board is not enough, and the rehearsal reviewer
  showed why with a forged request). `CLAUDE.md` documents the platform's
  `TICTACTOE_SECRET` for signing what the browser sends back. Look at how
  `spec.md` solves it, and whether the review agrees.
- **"Must not change" is a requirement too.** Hard must still never lose to
  fair play. The existing exhaustive test guards it, and the new tests
  should add the cheat's side of it.
- **Separate phases find different things.** Unit tests catch rule bugs,
  the system test catches wiring, lint catches style, and a reviewer who
  did not write the code catches what the author cannot see.
- **A person is one of the gates.** The AI cannot see the page, so the
  plan lists what only a browser shows, you check it at the preview, and
  your answer is committed as `preview.md`. Without that sign-off, the
  rehearsal's reviewer raised a major ("nothing has ever run `app.js`"),
  and the deploy session hit the gate and **refused to tick the finding
  to get through**: it stopped and asked a human. Worth telling.
- **The deploy is code, not trust.** `ops/deploy.sh` reruns every gate
  (tests, ruff, no open blocker or major in any `changes/*/review.md`)
  before production is touched, and rolls back if the smoke test fails.
  Version 1 stays in `production/releases/` for rollback.

## Files

- `app/`: the starting repository, the working game with its docs
- `intent.md`: the change request, copied into
  `app/changes/cheat-code/` once version 1 is live
- Work dir `/tmp/demo-08_intent_to_production/`: `app/` is the repository
  (open `changes/cheat-code/*.md` there during the demo), and `production/`
  holds the releases, the `current` link, `server.log` and `server.pid`.
- Production keeps running after the demo.
  `/tmp/demo-08_intent_to_production/app/ops/deploy.sh --stop` stops it,
  and so does the next run.
