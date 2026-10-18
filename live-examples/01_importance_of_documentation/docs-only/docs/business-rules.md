# Business rules

## Discounts

| Code | Rule |
|------|------|
| `WELCOME` | 5.00 off the customer's very first order. It looks at *all* previous orders, any status, on purpose: cancelling and re-ordering must not earn a second welcome. |
| `BULK` | 3.00 off orders with 10 or more items. |

### Discounts never stack

When several rules apply, the customer gets **only the single largest
discount**. `Quote.applied` lists just that one code.

Known bug: `pricing.price_order` currently *adds up* every applicable
discount, so a first order of 10+ items gets WELCOME and BULK together.
Whoever next touches discounts must fix this.

### "Orders" means paid orders

When a rule talks about how many orders a customer has, it means orders
with status `PAID` (`orders.paid_orders()`). Pending, cancelled and refunded
orders do not count. `WELCOME` is the one deliberate exception, see above.

### Gift cards are never discounted by percentage

Gift cards (any line whose SKU starts with `GIFT-`) are a stored
value, not merchandise. By law a percentage discount must not apply to them:
compute it on the non-gift-card part of the subtotal only. Fixed-amount
discounts (WELCOME, BULK) are unaffected.

### Rounding

Percentage discounts are rounded **down** to a whole cent
(`money.percent_of`). 10% of 19.99 is 1.99, not 2.00.
