# Architecture

```text
browser (static/)                          server (Python, stdlib)
┌───────────────────────┐  POST /api/move  ┌────────────────────────────┐
│ index.html  app.js    │ ───────────────▶ │ server.py  handle_move()   │
│ draws, sends clicks,  │    whole board   │   ├─ game.py  rules        │
│ keeps the score       │ ◀─────────────── │   └─ ai.py    computer     │
└───────────────────────┘   new board +    └────────────────────────────┘
                            outcome
```

The rules live in Python only. The browser never decides whether a move is
legal or who won: it shows what the server answers.

## Modules (`tictactoe/`)

| File | Job |
|------|-----|
| `game.py` | The rules. A board is a list of 9 cells, row by row, each `"X"`, `"O"` or `""`. X moves first, so `turn()` follows from the counts. `validate()` checks a board from outside, `play()` returns a new board (never changes its input) or raises `IllegalMoveError`, `outcome()` says `playing`, `won` (with winner and line) or `draw`. |
| `ai.py` | The computer. `choose_move(board, level)`: **hard** is negamax over the full game tree, cached, lowest cell among equals, so it is deterministic and never loses; **easy** takes a winning move if it sees one, otherwise plays at random. |
| `server.py` | `ThreadingHTTPServer`. Serves a fixed map of assets (no request path reaches the file system), `/health`, and the move API. Keeps no state. |
| `__main__.py` | `python3 -m tictactoe [--host] [--port]`; prints the URL it listens on. |
| `static/` | `index.html`, `style.css`, `app.js`. No build step, no libraries. |

## The move API

`POST /api/move`, a JSON body of at most 1024 bytes:

```json
{"board": ["X", "", "", "", "O", "", "", "", ""], "cell": 2, "mode": "computer", "level": "hard"}
```

- `mode` is `computer` (default) or `friend`; `level` is `easy` or `hard`
  (default), used only against the computer.
- Against the computer the player is always X, so the board must have X
  to move.
- The server plays `cell` for whoever is to move, then, against the
  computer and if the game goes on, the computer's reply as O.

Answer `200`:

```json
{"board": ["X", "", "X", "", "O", "", "", "", "O"], "status": "playing",
 "winner": null, "line": null, "turn": "X", "computer_move": 8}
```

`status` is `playing`, `won` or `draw`; `line` is the three winning cells;
`turn` is `null` once the game is over; `computer_move` is `null` when the
computer did not move.

Errors: `400 {"error": "..."}` for any bad input (bad JSON, impossible
board, taken square, game over, unknown mode or level), `411` without a
`Content-Length`, `413` for a body over 1024 bytes, `404` for other paths,
`405` for `GET /api/move`.

## The page

`app.js` holds the current answer from the server and the score (X wins, O
wins, draws, until the page is reloaded). Each click or Enter/Space on a
square sends one move. The board is one tab stop: arrow keys, Home and End
move between squares (roving `tabindex`), and every square has an
`aria-label` such as "Row 1, column 3, X, winning". The status line is an
`aria-live` region. Changing mode or level starts a new game.

## Tests

- `tests/test_game.py`, `tests/test_ai.py`, `tests/test_server.py`: unit
  tests. `test_hard_never_loses` plays Hard against every possible opponent,
  as X and as O.
- `tests/system/test_http.py`: starts `python3 -m tictactoe --port 0` as a
  process and tests it over HTTP: health, assets, 404s, whole games, errors.
