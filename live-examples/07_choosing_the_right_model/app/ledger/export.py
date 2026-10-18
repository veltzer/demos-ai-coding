"""CSV export for the accounting system's nightly import."""

import csv
import io

from ledger.money import fmt

HEADER = ["date", "customer", "amount", "memo"]


def to_csv(payments):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(HEADER)
    for p in payments:
        writer.writerow([p.date, p.customer, fmt(p.amount_cents), p.memo])
    return buf.getvalue()
