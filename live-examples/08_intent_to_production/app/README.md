# tictactoe

Tic-tac-toe for the website's games corner: a drawn 3x3 board in the
browser, against the computer (Easy or Hard, which never loses) or against
a friend on the same screen. The page keeps a running score and can be
played with the keyboard alone.

```bash
python3 -m tictactoe              # http://127.0.0.1:8000/
python3 -m tictactoe --port 0     # any free port; the URL is printed
python3 -m pytest -q              # unit and system tests
ruff check . && ruff format --check .
./ops/deploy.sh                   # to production, see docs/deploy.md
```

Python 3.12 or newer, standard library only.

## Documentation

- `docs/architecture.md`: modules, the move API, how the page works
- `docs/process.md`: how a change goes from intent to production
- `docs/deploy.md`: production and how to deploy to it
- `changes/<name>/`: one folder per change, with its intent, spec, plan,
  test report and review
