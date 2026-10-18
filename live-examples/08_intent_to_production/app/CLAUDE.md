# tictactoe

The tic-tac-toe game for the website's games corner, live in production.
Read `README.md` and `docs/architecture.md` before changing anything.

Every change goes from intent to production in phases, as described in
`docs/process.md`. Each change has its own folder `changes/<name>/`, where
the business puts `intent.md` and each phase leaves its artifact. Every
request names a phase and a change: read that phase in `docs/process.md`
and do that phase only.

## Engineering standards

- Python 3, **standard library only**: no pip installs, no frameworks, no
  CDNs. The browser side is plain HTML, CSS and JavaScript.
- The rules and the computer player live in Python and are served over the
  JSON API. The browser draws, sends moves and shows the answers. Never
  duplicate a rule in JavaScript.
- The server keeps no state between requests. Everything it needs to judge
  a move arrives with the request, and it trusts nothing that does.
- Everything that ships lives in the package `tictactoe/`. The deploy copies
  only that folder.
- `GET /health` answers `200 ok`. The deploy depends on it.
- Tests use pytest in `tests/` (system tests in `tests/system/`). Never use
  a fixed port: bind to port 0.
- `docs/architecture.md` describes the system as it is: a change that alters
  the API, a module or the page updates it.
- Lint is ruff, configured in `pyproject.toml`: `ruff check .` and
  `ruff format --check .` must both be clean. Fix the code, never the check:
  no `# noqa`, no changes to the ruff configuration.
- `ops/` belongs to the platform team. Do not change it.
- Production is reached only through `ops/deploy.sh`. See `docs/deploy.md`.
