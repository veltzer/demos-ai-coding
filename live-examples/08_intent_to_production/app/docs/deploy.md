# Deploying to production

Production runs the release that `production/current` points to, one
process, on port 8088 (`PROD_PORT`). `production/` sits next to this
repository (`PROD_DIR` overrides it). Every release is kept under
`production/releases/` for rollback.

## How to deploy

```bash
./ops/deploy.sh
```

That is the only way in. The script:

1. **Gates.** It runs the unit and system tests, `ruff check` and
   `ruff format --check`. Every change folder (`changes/*/`) must have a
   `review.md` with no unticked blocker or major finding. Any failure stops
   the deploy before production is touched.
2. **Release.** It copies `tictactoe/` to `production/releases/<id>/` and
   records the git commit it came from.
3. **Switch.** It stops the running release, points `current` at the new
   one and starts it.
4. **Smoke test.** It waits for `/health` and loads the page. If either
   fails, it rolls back to the previous release and exits non-zero.

`./ops/deploy.sh --status` shows what is running, `--stop` stops it.

## If a gate fails

Fix the cause in the code, the tests or the review, then deploy again. Do
not edit `ops/`, do not skip a gate, do not start a production server by
hand.

## After the deploy

Check it yourself with `curl`: `/health`, the page, and one move through
the API. Report the release id, the URL and what you checked.
