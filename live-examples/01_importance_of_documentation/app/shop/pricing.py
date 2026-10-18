"""Turn an order into a price quote."""

from dataclasses import dataclass, field

from shop.discounts import RULES


@dataclass
class Quote:
    subtotal: int
    discount: int
    total: int
    applied: list[str] = field(default_factory=list)


def price_order(store, order):
    subtotal = order.subtotal
    applied, discount = [], 0
    for code, fn in RULES:
        amount = fn(store, order)
        if amount:
            applied.append(code)
            discount += amount
    discount = min(discount, subtotal)
    return Quote(subtotal, discount, subtotal - discount, applied)
