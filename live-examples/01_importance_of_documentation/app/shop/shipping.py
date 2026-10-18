"""Shipping charges."""

from shop import settings


def shipping_cents(quote):
    if quote.total >= settings.FREE_SHIPPING_FROM_CENTS:
        return 0
    return settings.SHIPPING_FLAT_CENTS
