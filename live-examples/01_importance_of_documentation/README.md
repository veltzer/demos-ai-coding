# Demo 01: documentation

```bash
./run.sh          # interactive, pauses between steps so you can talk
./run.sh --yes    # unattended dry run
```

## What happens

Two copies of a small shop backend (`app/`) with **identical code**. B also
gets `docs-only/` copied on top: `CLAUDE.md`, `docs/architecture.md` and
`docs/business-rules.md`, about 75 lines in total. Both get the same request:

> Add a loyalty discount: customers who already have 5 or more orders get 10% off.

`acceptance/check.py` scores both against the business rules, and every FAIL
names the doc that had the answer. The scoreboard shows time, tokens and cost.

## The traps: knowledge that lives outside the code

| Trap | What the code suggests | What the docs say |
|------|------------------------|-------------------|
| `shop/legacy/pricing_v1.py` has a ready-made `loyalty_discount()` with a "TODO: port" | reuse or port it | frozen: serves the v1 API, never import or edit |
| "5 or more orders" | `store.orders_for()`: all orders, like `WELCOME` uses | paid orders only (`orders.paid_orders()`); WELCOME is a deliberate exception |
| a `GIFT-50` line in the order | 10% of the whole subtotal | percentage discounts never apply to gift cards (legal) |
| 10% of 19.99 | `round()` gives 2.00 | round down to 1.99 (`money.percent_of`) |
| LOYALTY + BULK on one order | `price_order` adds discounts up | never stack, best single discount wins; summing is a known bug |
| tests | none required | every behaviour change comes with a test |

## Talking points

- Show the `diff -rq` at the start: the code is the same, so any difference
  in the result comes from the docs.
- A is a good engineer: it often works out "paid orders only" from the
  `paid_orders()` helper, and "round down" from `money.percent_of`'s test.
  Where the code has a hint, a strong model finds it. Where it has none
  (gift cards are a legal matter, stacking is a known bug), A copies what
  the code does, and the code is a record of what was done, not what was meant.
- Read A's summary out loud: it ends with "decisions for you to check".
  Without docs the AI has to guess and then ask; with docs it already knows.
- The legacy trap is the most visual one: the code literally says
  "TODO: port to the new pricing module". Only the docs say why not.
- Docs also save exploration: B knows where things live, so it reads
  fewer files. In rehearsals B used 17-48% fewer input tokens. That number
  varies between runs; the correctness gap is the steady part.
- About 75 lines of markdown, written once, read by every AI session and every
  new colleague. That is the cheapest context you can give.

## Files

- `app/`: the shop, copied fresh on every run (originals never change)
- `docs-only/`: what B gets on top of `app/`
- `acceptance/check.py`: the hidden scoring
