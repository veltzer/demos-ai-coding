# billing

Invoicing for the shop: lines, VAT, totals and plain-text rendering.

## Layout

- `billing/rounding.py`: every amount goes through `round_cents`.
- `billing/invoices.py`: `Line`, `Invoice`, VAT at 17%.
- `billing/render.py`: plain-text output.
- `tests/`: unittest suite.

## Conventions

- Money is `decimal.Decimal`, never float. Construct from strings.
- Keep functions small and pure; no I/O in `billing/`.
- Type hints are welcome but not required.
- Use f-strings for formatting.
- Don't add dependencies; standard library only.
- Run the tests with `python3 -m unittest discover -s tests`.
- Commit messages: imperative mood, under 72 characters.
- Prefer clarity over cleverness; comment the why, not the what.
- VAT changes need sign-off from Finance before they ship.
- `tests/` belongs to the QA team. Never create, edit or delete anything
  under `tests/`. If a change needs different tests, finish the code change
  and list the test changes QA should make in your final message.
- Rendering widths are fixed by the printer; don't change them.
- Keep this file up to date when the layout changes.
