"""Pricing for the v1 API (amounts in dollars)."""


def order_total(lines):
    return round(sum(qty * price for qty, price in lines), 2)


def welcome_discount(order_count):
    return 5.0 if order_count == 0 else 0.0


def loyalty_discount(order_total, order_count):
    # TODO: port to the new pricing module
    if order_count >= 5:
        return round(order_total * 0.10, 2)
    return 0.0


def bulk_discount(item_count):
    return 3.0 if item_count >= 10 else 0.0
