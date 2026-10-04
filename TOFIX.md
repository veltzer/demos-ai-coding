# TOFIX

Findings from a code scan on 2026-10-04.

## Medium

- `README.md:19` - the Building section is out of date: it says Python is checked with `pylint` (no pylint processor exists in `rsconstruct.toml`), that `rsconstruct.toml` is "shared across repos, do not edit here" with overrides in `rsconstruct.local.toml` (no such file; `rsconstruct.toml` is this repo's own config), and that Python rules live in `.pylintrc` / `.mypy.ini` (neither exists; mypy is configured in `pyproject.toml`). Rewrite it to match the current setup.
- `exercises/04_advanced_techniques/01_your_own_mcp_server/my_mcp.json:5` - the server `command` points to `/home/mark/git/veltzer/demos-ai-coding/exercises/12_mcp/math-mcp-service.js`, a path that no longer exists (the file is in `exercises/04_advanced_techniques/01_your_own_mcp_server/`, and the checkout is not under `veltzer/`); use a relative path or a placeholder students replace.
- `exercises/03_software_engineering/04_infrastructure_as_code/code/docker/Dockerfile:38` - the `HEALTHCHECK` imports `requests`, which is not in `requirements.txt` (only `flask` and `gunicorn`), so every probe fails with `ImportError` and the container is always reported unhealthy; use `urllib.request` (and check the status code) or add `requests`.
- `exercises/03_software_engineering/04_infrastructure_as_code/code/docker/docker-compose.yml:10` - bind-mounts `./nginx.conf` and `./ssl`, neither of which is shipped, so the `docker-compose up -d` that `code/README.md` tells students to run starts nginx with Docker-created empty directories and nginx fails; add the files or drop the nginx service.
- `exercises/03_software_engineering/04_infrastructure_as_code/code/docker/requirements.txt:2` - `gunicorn==22.0.0` is pinned without a comment and is affected by the HTTP request-smuggling advisory fixed in 23.0.0 (CVE-2024-6827); bump it (and explain the pins, or drop them).
- `pyproject.toml:42` - the mypy `ignore_missing_imports` override lists `anthropic.*`, but the `anthropic` package ships `py.typed`; remove it so type errors against the SDK are reported.

## Low

- `examples/airline-ticket-agent-py/simple_8.py:19` - `# pylint: disable=...` markers across the examples and exercises (e.g. `simple_3.py:14`, `exercises/03_software_engineering/00_tdd_with_ai/code/tests/test_shopping_cart.py:4`) silence a linter that the build never runs; either add the pylint processor the README promises or drop the dead markers.
- `examples/airline-ticket-agent-py/simple_8.py:14` - docstring says the only modules needed are `passpy` and `anthropic`, but the script also imports `chromadb` (line 29); same in the other `simple_*.py` that use the vector DB.
- `exercises/04_advanced_techniques/01_your_own_mcp_server/test-mcp.sh:84` - tells the user to "Configure VS Code settings as described in README.md", but that directory has no README.md (the instructions are in `exercise.md`).
- `exercises/07_mcp_servers/http_server.py:5` - docstring says to run `python server.py`; the file is `http_server.py`. The `07_mcp_servers` directory also has no `exercise.md` unlike every other exercise folder; move it under an existing category or add the exercise text.
- `pyproject.toml:15` - `pytest` is listed in runtime `dependencies` as well as in the `dev` group; keep it in `dev` only.
- `rsconstruct.toml:45` - comment says "scripts/ is listed for the day it comes back", but `py_dirs` (line 46) does not list `scripts/`; fix the comment. The surrounding comments also keep referring to "the Makefile", which no longer exists.
- `CLAUDE.md:5` - says exercises are files of the form `exercises/*/exercise.md`, but they are one level deeper (`exercises/*/*/exercise.md`).
