"""Nightly reconciliation job."""

from ledger.export import to_csv
from ledger.importer import from_csv


def reconcile(payments, path):
    with open(path, "w", newline="") as f:
        f.write(to_csv(payments))
    with open(path, newline="") as f:
        imported = from_csv(f.read())
    missing = [p for p in payments if p not in imported]
    return {"exported": len(payments), "imported": len(imported), "missing": missing}
