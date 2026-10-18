"""Discount rules. Each rule returns the discount in cents (0 if it does not apply)."""

from shop import settings

RULES = []


def rule(code):
    def register(fn):
        RULES.append((code, fn))
        return fn
    return register


@rule("WELCOME")
def welcome(store, order):
    previous = [o for o in store.orders_for(order.customer_id) if o.id != order.id]
    return settings.WELCOME_DISCOUNT_CENTS if not previous else 0


@rule("BULK")
def bulk(store, order):
    return settings.BULK_DISCOUNT_CENTS if order.items >= settings.BULK_MIN_ITEMS else 0
