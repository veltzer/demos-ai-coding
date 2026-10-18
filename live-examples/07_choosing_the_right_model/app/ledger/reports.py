"""Simple totals for the dashboard."""

from collections import defaultdict

from ledger.money import fmt


def totals_by_customer(payments):
    totals = defaultdict(int)
    for p in payments:
        totals[p.customer] += p.amount_cents
    return {c: fmt(t) for c, t in sorted(totals.items())}
