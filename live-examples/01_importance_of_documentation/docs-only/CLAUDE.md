# shop

Order pricing and fulfilment for the web shop.

Before changing pricing or discounts, read `docs/business-rules.md`.
`docs/architecture.md` says where everything lives.

## Rules

- Money is integer cents everywhere. Percentages go through
  `money.percent_of`, which rounds down: the shop never gives away a
  fractional cent.
- Percentage discounts never apply to gift cards (legal requirement, see
  `docs/business-rules.md`).
- Business numbers (thresholds, percentages, amounts) live in
  `shop/settings.py`, never inline, so ops can tune them.
- `shop/legacy/` is frozen. It still serves the v1 mobile API and must keep
  its exact behaviour. Never import from it and never edit it, even when it
  seems to have the function you need.
- Every behaviour change comes with a unit test in `tests/`.
- Run the tests with: `python3 -m unittest discover -s tests`
