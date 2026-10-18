"""Back-office reports."""

from collections import Counter

from shop.models import Status
from shop.money import fmt


def revenue(store):
    cents = sum(o.subtotal for o in store.orders if o.status is Status.PAID)
    return fmt(cents)


def best_sellers(store, n=5):
    counts = Counter()
    for order in store.orders:
        if order.status is Status.PAID:
            for line in order.lines:
                counts[line.sku] += line.qty
    return counts.most_common(n)
