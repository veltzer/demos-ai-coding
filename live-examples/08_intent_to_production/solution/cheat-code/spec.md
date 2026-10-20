# Spec: a secret cheat code (`cheat-code`)

Source: `changes/cheat-code/intent.md`. This is the design to build from.
It describes the change against the system as it is today
(`docs/architecture.md`, `tictactoe/`).

## Summary

Against the computer, typing ↑ ↑ ↓ ↓ ← → ← → B A on the page unlocks a
**steal** for the current game: once per game the player may turn one of
the computer's O squares into an X, and that is the player's move. A win
that used a steal is announced as "You won... with a little help" and
counted in its own score column, never as a normal win.

The browser recognises the code and shows the steal controls. The server
judges every steal. To enforce "one steal per game" without keeping state,
the server signs each game position it hands out (an HMAC **game token**)
and accepts a steal only together with a valid token that says no steal has
been used. Requests without a token behave exactly as today.

## How it works today (the parts this change touches)

- A board is 9 cells, `"X"`, `"O"` or `""`. Whose turn it is follows from
  the counts: `game.turn()` is X when X count == O count. `game.validate()`
  accepts a board only if X count − O count is 0 or 1.
- `POST /api/move` takes the whole board, `cell`, `mode`, `level`. Against
  the computer the player is X and the board must have X to move. The server
  plays `cell`, then the computer's reply, and answers the new board.
- The server trusts nothing: any board that passes `validate()` is accepted.
  It has no idea whether that board came from a real game.
- The score (X wins, O wins, draws) lives in `app.js` until reload.

## New and changed rules

1. **Steal.** In a game against the computer, on the player's turn (X to
   move, game still playing), the player may name one cell that holds `"O"`.
   That cell becomes `"X"`. This is the player's move: the computer then
   replies as usual if the game goes on.
2. **Once per game.** A game has at most one steal. A game is one unbroken
   chain of positions handed out by the server, starting from the empty
   board (see "Game token").
3. **Only against the computer**, at both levels (`easy`, `hard`). Never in
   `friend` mode.
4. **Turn after a steal.** A steal changes a mark without adding one, so the
   counts no longer say whose turn it is. The rule becomes: with `s` steals
   used in the game (0 or 1), X is to move when X count − O count == `s`,
   otherwise O. A valid board has X count − O count equal to `s` or `s + 1`.
   With `s = 0` both rules are exactly today's.
5. **A steal can win at once.** If the stolen square completes a line of X,
   the game is won by X and the computer does not move. A steal never fills
   an empty square, so it cannot cause a draw by itself.
6. **Assisted win.** A game won by X in which a steal was used is an
   *assisted* win. The server says so in every answer (`assisted: true`).
   The page announces it as "You won... with a little help" and counts it
   only in the "With help" column, not in "X wins".
7. After a steal the game goes on normally: the computer (either level)
   plays its best/random move from the new position, and the computer can
   still win or draw. Those are counted as today (O win, draw).
8. **The code.** ↑ ↑ ↓ ↓ ← → ← → B A (`ArrowUp ArrowUp ArrowDown ArrowDown
   ArrowLeft ArrowRight ArrowLeft ArrowRight b a`, B and A in either case).
   The code is recognised by the page only; it unlocks the steal controls
   for the current game. The server does not check the code (see Open
   questions 1).

## Game token (how the server enforces the rules without state)

The server keeps nothing between requests. Instead it signs what it must
trust when the browser sends it back, as `CLAUDE.md` allows.

- **Key.** `TICTACTOE_SECRET` from the environment (UTF-8 bytes) when set
  and not empty; otherwise 32 random bytes from `secrets.token_bytes` made
  once when the process starts. Production sets it through `ops/deploy.sh`
  and keeps it across releases, so tokens survive a deploy. The key is
  never logged, never sent, never put in an error message.
- **Format.** `"<s>.<mac>"`, where `<s>` is the number of steals used (`0`
  or `1`) and `<mac>` is the lowercase hex HMAC-SHA256 of the message
  `tictactoe-game-v1|<level>|<s>|<cells>`, with `<cells>` the 9 cells, each
  written as `X`, `O` or `-`. Example: `"0.3f9a…c1"` (64 hex digits).
  The token binds the board, the level and the steal count together;
  change any of them and it no longer verifies.
- **Checking.** Compare with `hmac.compare_digest`. A token that is not a
  string, has the wrong shape, an `<s>` other than `0`/`1`, or a MAC that
  does not match the request's `board` and `level` is rejected with
  `400 {"error": "the game token does not match this game"}`. This applies
  to any request that carries a `game` field, steal or not.
- **When the server hands one out** (the `game` field of the answer), only
  in `computer` mode and only while the game is still `playing`:
  - the request carried a valid token: the new position gets a token with
    the same `s` (or `s = 1` if this request was the steal);
  - the request had no token and its board was empty (first move of a new
    game): the new position gets a token with `s = 0`;
  - otherwise (no token, board not empty, e.g. a hand-made mid-game board
    or an older page): `game` is `null`. That game plays exactly as today
    and can never steal.
  So a token proves that the position was reached by legal moves through
  this server from an empty board, with `s` steals on the way.
- **Why this stops a second steal, even by hand.** A steal needs a token
  with `s = 0`. The answer to a steal only ever carries `s = 1` tokens, and
  every later answer in that game keeps `s = 1`. A board that has had a
  steal has X − O == 1 on X's turn, which no `s = 0` token can match and
  which `validate()` rejects without a token. Forging an `s = 0` token
  needs the key.
- **Replays.** Because the server is stateless, an old token stays valid.
  A player who kept an `s = 0` token from earlier in the same game can go
  back to that position and steal from there. That is a branch of the game
  (like an undo), and every branch still has at most one steal. Accepted
  (Open questions 3).

## API changes

`POST /api/move` keeps its path, limits (1024-byte body, 411, 413, 404,
405) and every existing field and error. New, all optional in the request:

| Field | Meaning |
|-------|---------|
| `steal` | A cell 0–8 to steal, sent **instead of** `cell`. |
| `game` | The `game` token from the server's previous answer. |

New in every `200` answer (all modes):

| Field | Meaning |
|-------|---------|
| `game` | Token for the new position, or `null` (rules above). |
| `stealable` | Cells the player could steal now: the O cells when this answer has a token with `s = 0`, the game is playing and X is to move; otherwise `[]`. |
| `steal_used` | `true` once a steal has been used in this game (`s = 1`), else `false`. |
| `assisted` | `true` when `status` is `won`, `winner` is `X` and `steal_used` is `true`; else `false`. |

The page uses `stealable`, `steal_used` and `assisted` as given; it never
works out for itself which squares can be stolen or whether a win was
assisted.

### Examples (Hard; tokens shortened)

First move of a new game, no token (the existing request, unchanged):

```json
{"board": ["", "", "", "", "", "", "", "", ""], "cell": 0, "mode": "computer", "level": "hard"}
```

```json
{"board": ["X", "", "", "", "O", "", "", "", ""], "status": "playing",
 "winner": null, "line": null, "turn": "X", "computer_move": 4,
 "game": "0.<64 hex>", "stealable": [4], "steal_used": false, "assisted": false}
```

Next move, sending the token back:

```json
{"board": ["X", "", "", "", "O", "", "", "", ""], "cell": 8, "mode": "computer",
 "level": "hard", "game": "0.<64 hex>"}
```

```json
{"board": ["X", "O", "", "", "O", "", "", "", "X"], "status": "playing",
 "winner": null, "line": null, "turn": "X", "computer_move": 1,
 "game": "0.<64 hex>", "stealable": [1, 4], "steal_used": false, "assisted": false}
```

The steal: taking the centre completes the diagonal 0-4-8.

```json
{"board": ["X", "O", "", "", "O", "", "", "", "X"], "steal": 4, "mode": "computer",
 "level": "hard", "game": "0.<64 hex>"}
```

```json
{"board": ["X", "O", "", "", "X", "", "", "", "X"], "status": "won",
 "winner": "X", "line": [0, 4, 8], "turn": null, "computer_move": null,
 "game": null, "stealable": [], "steal_used": true, "assisted": true}
```

A steal that does not win (stealing cell 1 instead) gets the computer's
reply and an `s = 1` token; X is to move with X − O == 1. (Hard must block
row 0 at cell 2; this reply is the expected one, not recorded from code.)

```json
{"board": ["X", "X", "O", "", "O", "", "", "", "X"], "status": "playing",
 "winner": null, "line": null, "turn": "X", "computer_move": 2,
 "game": "1.<64 hex>", "stealable": [], "steal_used": true, "assisted": false}
```

A friend game answers `game: null, stealable: [], steal_used: false,
assisted: false` in addition to today's fields. A friend request that
carries a `game` token is refused (added in review fixes; see the table).

### New errors (all `400 {"error": "..."}`)

Checked in this order, after today's checks of the body, `board` shape,
`mode` and `level`:

| Case | Message |
|------|---------|
| `game` present in `friend` mode | `the game token is only for games against the computer` |
| `game` present but not valid for this `board` and `level` (any request) | `the game token does not match this game` |
| both `cell` and `steal` present | `send either cell or steal, not both` |
| `steal` in `friend` mode | `you can only steal from the computer` |
| `steal` without `game` | `a steal needs the game token from the last answer` |
| `steal` with a token whose `s` is 1 | `you have already stolen a square in this game` |
| `steal` not a whole number 0–8 (`true` is not a number) | `steal must be a whole number from 0 to 8` |
| game already over | `the game is over` (today's message) |
| the cell is not an O (empty or X) | `you can only steal one of the computer's squares` |

The board check uses the token's `s`: a board with X − O outside
`s`..`s + 1` is rejected with today's message `X moves first and the
players alternate`, and with X − O ≠ `s` against the computer with today's
`against the computer you play X`.

## Logging (to see steals in production)

The intent will judge success by steals in games "we did not set up". The
server has no database, so after every successful steal the request handler
writes one line through `log_message` (stderr, which `ops/deploy.sh` sends
to `production/server.log`, next to the request line with the client
address):

```text
steal level=hard cell=4 status=won assisted=true
```

Nothing else is logged: no token, no key, no board. Because a steal needs a
token chain that started from an empty board, every logged steal happened
in a real game played through the server.

## The page

### Before the code (unchanged)

The page looks and behaves exactly as today: no steal button, no hint, no
"With help" column, no change to labels or status texts. The new elements
exist in `index.html` with `hidden` and are not shown or announced.

### Recognising the code

- `app.js` listens to `keydown` on `document` and keeps the last 10 keys.
  When they equal the code, the code is typed. A sliding window means extra
  keys before it do not matter (↑ ↑ ↑ ↓ ↓ … still works).
- Ignored: events with Ctrl, Alt or Meta held, and auto-repeat
  (`event.repeat`). Keys typed while focus is in a `<select>` are not
  recorded (arrows there change the mode or level, which starts a new game).
- The board's own arrow handling stays as it is: typing the code with the
  focus on the board moves the focus around, which is harmless; arrows never
  play a move.
- The code unlocks only when the mode is `computer` and the game is
  `playing`. Otherwise it does nothing at all (friend mode: no message, no
  hint).
- Unlocking lasts for the current game. A new game (button, mode or level
  change) locks it again; typing the code again unlocks it again.

### After the code

- The status line (`aria-live`) announces: "Cheat unlocked! Once this game,
  you may steal one of the computer's squares." The current status text
  follows after the next move as usual.
- A panel under the status line appears with a **Steal a square** button
  (`aria-pressed`) and the short text "Press Steal, then choose an O. Esc
  cancels." The button is disabled-looking (`aria-disabled="true"`, still
  focusable) when `stealable` is empty, with the reason in the panel text:
  "No O to steal yet" before the computer has moved, "Steal used" after,
  and "Game over" when a game ends without a steal (added in review fixes).
- The score table shows a fourth column **With help** (and keeps showing it
  until the page is reloaded, so the count stays visible).

### Steal mode

- Pressing the button (click, Enter, Space) turns steal mode on, but only
  if `stealable` is not empty. The status line says "Steal: choose one of
  the computer's squares." The focus moves to the lowest stealable square
  (roving `tabindex` as today).
- In steal mode only the squares in `stealable` are active
  (`aria-disabled="false"`, class `stealable` with a visible dashed outline
  that does not rely on colour alone). Their label gains ", can be stolen",
  e.g. "Row 2, column 2, O, can be stolen". Every other square is
  `aria-disabled="true"` and does nothing when chosen.
- Choosing a stealable square (click, tap, Enter, Space) sends
  `{board, steal, mode, level, game}`. Steal mode ends with the answer.
- Esc, or pressing the button again, ends steal mode without a move and
  puts the focus back on the button.
- Outside steal mode, clicking an O does nothing, as today.

### After a steal

- The status line says "You stole row R, column C." when the game goes on
  (then the usual "Your turn (X)" once the next answer arrives; moving the
  focus with the arrow keys keeps the message), and "You won... with
  a little help" when the steal or a later move wins with `assisted: true`.
- Score: `assisted: true` adds 1 to **With help** and nothing to X wins.
  A computer win or a draw after a steal counts as today.
- The panel says "Steal used" and the button stays disabled-looking.

### Small screens

The panel and the four-column score table must fit 320 px wide with no
horizontal scroll: the column headings are short ("X wins", "O wins",
"Draws", "With help") and the button is at least 44 px tall. The code
needs a keyboard, so phones without one cannot unlock it (Open questions 2).

## Modules

| File | Change |
|------|--------|
| `game.py` | `turn(board, steals=0)`, `validate(board, steals=0)`, `play(board, cell, steals=0)` follow rule 4. New `steal(board, cell, steals) -> list[str]`: checks and errors from the table above (already stolen, cell type, game over, not X's turn, not an O); returns a new board, never changes its input. New `check_cells(board)`: only the shape and cell checks of `validate` (which now calls it), so the server can check a board's shape before it knows the token's `s`. `outcome()` and `legal_moves()` do not change. |
| `ai.py` | `choose_move(board, level, rng=None, *, steals=0)`; `best_move` and `value` take `steals` too (still cached), so the search uses the right turn after a steal. With `steals=0` the moves are exactly today's. |
| new `signing.py` | The key (env or random at import, as above), `sign(board, level, steals) -> str`, `verify(token, board, level) -> int` (returns `s`, raises `IllegalMoveError`). Nothing else imports `os.environ`. |
| `server.py` | `handle_move` reads `game` and `steal`, verifies, plays the move or the steal, then the computer's reply with the right `steals`, and adds `game`, `stealable`, `steal_used`, `assisted`. `describe()` takes `steals`. `do_POST` writes the steal log line. Signature `handle_move(request)` stays. |
| `static/index.html` | Hidden cheat panel (button + text) under the status line; hidden "With help" column in the score table. |
| `static/app.js` | Code recognition, unlock state per game, steal mode, sending `game` back with every move, the new status texts, the fourth score counter. |
| `static/style.css` | `.stealable` outline, panel layout, small-screen fit. |
| `docs/architecture.md` | Updated in phase 3: the token, the new fields and errors, the turn rule, `signing.py`, the page's cheat. |

## What must keep working exactly as before

- Every request without `steal` and without `game` gets the same `board`,
  `status`, `winner`, `line`, `turn`, `computer_move` and the same errors
  as today; the only difference is the four added fields.
- Hard is unchanged for `steals=0` and never loses to fair play
  (`test_hard_never_loses` passes untouched). Easy is unchanged.
- Friend mode, `/health` (`200 ok`), the assets, 404/405/411/413, the
  1024-byte limit, the keyboard model of the board and its labels.
- All existing tests pass without change.

## How each line of the intent will be checked

| Intent line | Check |
|-------------|-------|
| Code unlocks one steal for that game; computer's mark becomes the player's; counts as the move | Unit (`game.steal`, `handle_move`) and system test: play a game over HTTP with tokens, steal, see the cell become X and the computer reply. Preview: type the code, steal with mouse and with keyboard. |
| One steal per game | Unit and system: a second steal with the returned token → 400 "already stolen". |
| Never shown or hinted at until the code; then clear how to use it | Preview: page before the code is identical to today (no button, no column, no label change); after the code the panel, text and announcement appear. |
| The code is ↑↑↓↓←→←→BA | Preview: the exact code unlocks; a wrong key in the middle does not; the sliding window works; uppercase B A works. |
| Won with a steal is announced differently and counted separately | Unit/system: `assisted: true` only for X wins with a steal. Preview: "You won... with a little help", "With help" goes up, "X wins" does not. |
| Only against the computer, both levels, not friend | Unit/system: steal works at easy and hard; friend → 400. Preview: the code does nothing in friend mode. |
| Without the code, exactly as today; Hard never loses to fair play | Existing unit and system tests untouched and passing; new unit test that tokenless answers equal today's fields; `test_hard_never_loses`. |
| On the page, nobody can steal without the code | Preview: clicking or pressing Enter on an O does nothing before the code. (The server cannot know about keys; see Open questions 1.) |
| Nobody can steal twice, even by hand | Unit and system: second steal → 400; steal without token, with a token for another board, another level, a hand-edited `0.`/`1.` prefix, a malformed token → 400; a hand-made mid-game board without token gets `game: null`. |
| Live in production, old game unchanged | Phase 9: `ops/deploy.sh`, then `curl` `/health`, the page, and one tokenless move whose old fields match today's answer. |
| We see steals in games we did not set up | The `steal …` log line in `production/server.log`; system test checks the server prints it on a steal and never prints the key or token. After launch, Product reads the log (client addresses are in the request lines). |

## Open questions (with the decision taken)

1. **Should the server check the code?** No. The code is meant to be
   shared, so anyone sending requests by hand knows it anyway; making the
   browser send it would add nothing. "Nobody can steal without the code"
   is a promise about the page, kept by the page. The server enforces what
   it can: computer mode only, a real game, at most one steal.
2. **Phones and tablets without a keyboard?** Out of scope: the intent says
   "typed on the keyboard". No touch gesture is added. Product can ask for
   one as a separate change.
3. **Replaying an older token to steal in a different branch of the same
   game?** Allowed: it cannot be stopped without server state, and each
   branch still has at most one steal. Equivalent to starting over and
   replaying the same moves.
4. **Tokens for games already running when this ships?** Those pages run
   the old `app.js` and never send `game`; they play on as today and cannot
   steal. After a reload they get tokens.
5. **Development restarts.** Without `TICTACTOE_SECRET`, a restart makes a
   new key, so a game in progress gets 400 "the game token does not match"
   on its next move. Accepted for development; the page shows its usual
   error and New game fixes it. Production keeps its key across releases.
6. **Is an assisted win also an X win in the API?** Yes: `status: "won"`,
   `winner: "X"` as today, plus `assisted: true`. Only the page's score
   counts it separately. Keeps old clients and `status` unchanged.
7. **Can the computer still win after a steal?** Yes, and that is counted
   as a normal O win; a draw after a steal is a normal draw. Only X wins
   are "with help".
8. **Token after the game ends?** `null`: there is nothing left to play.
9. **Where the code lives in `app.js`.** Plain in the source. It is a
   shared secret by design; hiding it would be theatre.
