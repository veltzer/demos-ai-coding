# System test report: `cheat-code`

Phase 5 of `docs/process.md`. The real server was started as production
starts it (`python3 -m tictactoe --port 0`, its own process) and driven over
HTTP only. The page (code recognition, steal mode, labels, score column) is
browser behaviour and is not tested here. It has **not** been checked by a
person: `preview.md` records "Checked by: nobody", "Result: not checked".

## Result

**Whole suite: 215 passed** (`python3 -m pytest -q`, 0.65 s), unit and
system tests together. `ruff check .` and `ruff format --check .` are clean.
No server process is left running afterwards.

**Bugs found: none.** No code in `tictactoe/` was changed in this phase.

## What changed in `tests/system/`

- New `client.py`: `serve()`, a context manager that starts the server on
  port 0, waits for `/health`, yields the base URL and **always** stops the
  process in `finally` (terminate, then kill if it has not stopped after
  5 s), even when a test fails. It can set `TICTACTOE_SECRET` (and always
  removes any inherited value otherwise) and send stderr to a file. Also
  `get()` and `post()`, moved here from `test_http.py`.
- `test_http.py`: now uses `client.py`. Its tests are unchanged.
- New `test_cheat.py`: a module-scoped server started with a known
  `TICTACTOE_SECRET`, as production does, with its log (stderr) written to a
  temporary file.

## What was tested (`test_cheat.py`)

The steal, end to end:

| Test | Shows |
|------|-------|
| `test_the_first_move_of_a_game_gets_a_token` | A tokenless first move from the empty board gets an `s = 0` token; `stealable` is the computer's O. |
| `test_a_steal_that_wins_at_once_is_an_assisted_win` | Hard: X 0, O 4, X 8, O 1, then steal 4. The whole answer is exactly the spec's example: won by X on 0-4-8, no computer move, `game: null`, `steal_used` and `assisted` true. |
| `test_a_steal_is_the_players_move_and_the_computer_replies` | Steal 1 instead: the cell becomes X, the computer replies (blocks at 2, as the spec expected), X to move, `1.` token, `stealable: []`. |
| `test_after_a_steal_the_game_plays_on_to_its_end` | After a steal the game goes on with `1.` tokens to its end; `assisted` is true only if X won. |
| `test_a_steal_works_at_easy` (3 openings) | The steal works at Easy too. |
| `test_the_stealable_squares_are_the_os_on_the_players_turn` | Through a whole game, `stealable` always lists exactly the O cells, and is empty once the game is over. |

Nobody can steal twice, even by hand:

| Test | Request | Answer |
|------|---------|--------|
| `test_a_second_steal_is_refused` | a steal with the `1.` token from the first steal | 400 `you have already stolen a square in this game` |
| `test_a_steal_needs_a_token` | a steal with no token | 400 `a steal needs the game token from the last answer` |
| `test_a_stolen_board_without_its_token_is_refused` | the board after a steal, sent with no token | 400 `against the computer you play X` |
| `test_the_token_is_bound_to_the_board` | a valid token with a different board | 400 `the game token does not match this game` |
| `test_the_token_is_bound_to_the_level` | a valid Hard token with `level: easy` | same 400 |
| `test_editing_the_steal_count_breaks_the_token` | `1.` changed to `0.` by hand (to steal again), and `0.` changed to `1.` | same 400 |
| `test_a_malformed_or_forged_token_is_refused` (10 cases) | `""`, `"0"`, `"0."`, `s = 2`, a zero MAC, an uppercase-hex MAC, the number 0, `true`, a list, an object | same 400 |
| `test_a_hand_made_mid_game_board_gets_no_token` | a tokenless mid-game board | 200 with `game: null`, `stealable: []`, so that game can never steal |
| `test_a_token_survives_a_restart_with_the_same_secret` | a token from this server, sent to a fresh server with the same `TICTACTOE_SECRET` and then to one with a different secret | first accepted (as across a deploy), second refused with the mismatch 400 |

Other refusals: a steal in friend mode (400 `you can only steal from the
computer`); `cell` and `steal` together (400 `send either cell or steal, not
both`); stealing an empty square or an X (400 `you can only steal one of the
computer's squares`); `steal` of 9, -1, `true`, `"4"`, `4.0` (400 `steal must
be a whole number from 0 to 8`).

The old game, unchanged:

- `test_a_friend_game_gets_no_token`: friend answers carry `game: null,
  stealable: [], steal_used: false, assisted: false`.
- `test_a_tokenless_game_against_hard_still_never_lets_x_win`: all 9
  openings for X, played to the end without tokens: X never wins.
- `test_tokenless_errors_are_todays`: today's messages for the wrong turn,
  bad alternation and a bad level.
- All tests in `test_http.py` (health, page and assets, 404s, a whole game
  against Hard, a friend game, bad moves, 413) pass unchanged.

What the server prints:

- `test_a_steal_is_logged_without_the_key_or_any_token`: after a winning
  steal, the server log has `steal level=hard cell=4 status=won
  assisted=true`. Neither the secret nor the token (nor its MAC) appears
  anywhere in the log of the whole test module.

## A comparison with the server before the change (by hand, not in the suite)

To back "the old game behaves exactly as before" with more than the fixed
cases above, the baseline package (commit `09325b7`, before this change) was
pulled from git and run as a second server next to the current one. 2318
tokenless requests were sent to both: 2000 random boards (any mix of X, O
and empty, cells -1 to 9, both modes, Hard), 300 random friend moves, all 9
first moves against Hard, and malformed bodies (`null`, `[]`, `3`, `cell:
true`, no cell, a bad board, a bad mode, a bad level, `game` and `steal` sent
as `null`). Easy was left out because its moves are random.

Result: **0 differences**. 275 of the requests were answered 200, and every
field of the old answer was the same in the new one (the new one only adds
the four new fields). The other 2043 got the same status and the same error
message. This script is not in the suite because it needs the git history.

## Notes for the code review (not bugs)

- A token from a computer game is also accepted in friend mode, as the spec
  says ("any request that carries a `game` field"). With a `1.` token the
  friend move uses the after-steal turn rule and the answer says
  `steal_used: true`, with `game: null`. The page never sends this, and it
  cannot give a second steal or a new token, so it does no harm. Worth a
  look if the reviewer would rather refuse `game` in friend mode.
- Replaying an older `0.` token to steal from an earlier position works, as
  the spec accepts (Open questions 3). No test asserts it either way.
