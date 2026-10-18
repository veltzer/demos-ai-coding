# Architecture

| Module | Responsibility |
|--------|----------------|
| `shop/models.py` | `Customer`, `Order`, `Line`, `Status` dataclasses |
| `shop/store.py` | in-memory store, JSON persistence; `orders_for()` returns *all* orders of a customer |
| `shop/orders.py` | order lifecycle (create, pay, cancel, refund); `paid_orders()` |
| `shop/discounts.py` | discount rules, registered with `@rule("CODE")` |
| `shop/pricing.py` | `price_order()` turns an order into a `Quote` |
| `shop/money.py` | cents parsing/formatting, `percent_of()` |
| `shop/settings.py` | every tunable business number |
| `shop/shipping.py`, `inventory.py`, `notifications.py`, `reports.py` | not involved in pricing |
| `shop/legacy/` | frozen v1 API code, see CLAUDE.md |

Adding a discount = one `@rule` function in `discounts.py` + its numbers in
`settings.py` + a test in `tests/test_pricing.py`. Nothing else needs to
change, except for the known bug described in `business-rules.md`.
