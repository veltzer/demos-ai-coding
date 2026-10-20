# Code review: `cheat-code`

Phase 7 of `docs/process.md`. Read: `intent.md`, `spec.md`, `plan.md`,
`preview.md`, `test-report.md`, the diff `git diff e174aff HEAD` (the commit
before the spec), and the code around it (`tictactoe/`, `tests/`,
`docs/architecture.md`, `ops/deploy.sh`). At review time, `python3 -m pytest -q`
gave 215 passed, and `ruff check .` and `ruff format --check .` were clean.
No code was changed.

**Blocker:** none. **Major:** none.

- [x] **minor** `tictactoe/server.py:49`: a `game` token is verified and used in `friend` mode too. If you send a computer-game `1.` token with `mode: "friend"`, the friend move uses the after-steal turn rule and the answer says `steal_used: true`. The spec says (lines 182–183) that a friend game answers `steal_used: false`, and `docs/architecture.md` says `level` is "used only against the computer". It can't be exploited: friend mode never issues a token and never allows a steal. But the API breaks its own documented contract, and no test pins this either way. Either refuse or ignore `game` in friend mode, or fix the spec and the architecture doc to describe what happens now. **Fixed:** a `game` token in `friend` mode is now refused with `400 "the game token is only for games against the computer"`, checked right after mode and level (`check_mode` in `server.py`). The page never sends one in friend mode (a mode change starts a new game with `game: null`), so the player sees no change. Spec and `docs/architecture.md` updated. Tests: `test_a_friend_game_refuses_a_token` and a new row in `test_steal_errors_come_in_the_specs_order` (`tests/test_server.py`), and `test_a_friend_game_refuses_a_computer_games_token` (`tests/system/test_cheat.py`).
- [x] **minor** `tictactoe/static/app.js:151`: when a game ends without a steal (the computer wins, or a draw), the panel still says "No O to steal yet" while Os are on the board. The text is also the steal button's `aria-describedby`, so a screen reader gives the player the wrong reason. The spec defines only two reasons ("No O to steal yet" and "Steal used") and doesn't cover a finished game. Something like "Game over" would be correct. **Fixed:** the panel now says "Game over" when a game has ended without a steal ("Steal used" still takes priority once the steal is used). Spec and `docs/architecture.md` updated. **No automated test:** the project can't run `app.js` in a test (standard library only, no browser tests). A person must check this in the preview, like the rest of the page.
- [x] **minor** `docs/architecture.md:3`: the doc no longer describes the whole system. The diagram doesn't show `signing.py`. The "Tests" section (line 173) lists neither `tests/test_signing.py` nor `tests/system/test_cheat.py` and `tests/system/client.py`. `CLAUDE.md` requires a change that adds a module to update this doc. **Fixed:** the diagram shows `signing.py` and the token, and the Tests section lists `tests/test_signing.py`, `tests/system/client.py` and `tests/system/test_cheat.py`. This is a doc fix, so it has no test.
- [ ] **minor** `changes/cheat-code/spec.md:332`: the intent's success check ("steals in games we did not set up") depends on the client addresses in the request lines. The `steal …` log line itself has no address. But `ops/deploy.sh` starts production on `127.0.0.1`, so outside traffic must come through something local. If that is a reverse proxy, every request line shows `127.0.0.1`, and Product can't tell outside steals from the team's own. Before relying on this measure, ask the platform team whether the real client address reaches the log. **Not fixed:** code can't answer this, so it is a question for the platform team. `ops/` is theirs to change, and the address only matters for measuring success, not for the release. Before Product relies on counting steals by address, someone must ask the platform team whether production sits behind a reverse proxy and whether the real client address reaches the log.
- [x] **minor** `changes/cheat-code/test-report.md:5`: the report says the page "was checked by a person in `preview.md`". `preview.md` says the opposite: "Checked by: nobody", "Result: not checked". A reader who trusts the test report would believe the browser behaviour was signed off. **Fixed:** the report now says the page has not been checked by a person, as `preview.md` records. This is a doc fix, so it has no test.

## Verdict

The server side is sound and matches the spec. Every steal is judged on
the server. The HMAC game token binds the board, the level and the steal
count, is compared with `compare_digest`, and is handed out only on a chain
that starts from an empty board, so a second steal, a forged or edited
token, a hand-made board and friend-mode steals are all refused. The key is
never logged or sent. Requests without `game` and `steal` go through exactly
the old code path, Hard is unchanged for `steals=0`, and the unit and system
tests cover every rule, error and "must not change" promise in the spec
(including a 2318-request comparison with the baseline server). The page
works out no rule. None of the findings blocks a release.

Whoever releases must weigh one thing: **nobody has looked at the page.**
`preview.md` records an unattended run, "Checked by: nobody", "Result: not
checked", and the test report wrongly claims otherwise. So none of the
browser behaviour has been seen by a person: that the page is unchanged
before the code is typed, how the code is recognised, steal mode with mouse
and keyboard, the screen-reader announcements, the "With help" column, and
the 320 px layout. The 320 px fit depends on the CSS `:has()` selector, which
older browsers ignore. These parts of the intent's "must not change" promise
("the game behaves exactly as it does today", "nobody can steal without typing
the code" on the page) rest only on reading `app.js`.
