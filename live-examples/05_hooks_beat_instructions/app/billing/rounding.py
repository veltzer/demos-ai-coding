"""Money rounding. Every amount on an invoice goes through round_cents."""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def round_cents(amount):
    """Round an amount to whole cents."""
    return Decimal(amount).quantize(CENT, rounding=ROUND_HALF_UP)
