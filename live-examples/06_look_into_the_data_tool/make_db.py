#!/usr/bin/env python3
"""Build shop.db, a replica of a (fictional) production database.

The schema is exactly what app/schema.sql says. The surprises are in the
data, where only someone who looks will find them:
- an old importer wrote status 'PAID' in upper case;
- internal test accounts have kind 'staff_test';
- JPY has no minor unit, so its total_minor is whole yen, not cents;
- fx_rates.rate is units of the currency per 1 USD (EUR 0.92, JPY 150),
  so converting to USD means dividing.

Usage: make_db.py <path/to/shop.db>
"""

import random
import sqlite3
import sys
from pathlib import Path

SCHEMA = (Path(__file__).parent / "app" / "schema.sql").read_text()
RNG = random.Random(2026)

COUNTRIES = [("US", "United States"), ("DE", "Germany"), ("FR", "France"), ("GB", "United Kingdom"),
             ("JP", "Japan"), ("IL", "Israel")]
CURRENCY = {"US": "USD", "DE": "EUR", "FR": "EUR", "GB": "GBP", "JP": "JPY", "IL": "USD"}
# units of currency per 1 USD, by month
BASE_RATE = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 150.0}
MONTHS = [f"2026-{m:02d}" for m in range(1, 10)]


def main():
    path = Path(sys.argv[1])
    path.unlink(missing_ok=True)
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    db.executemany("INSERT INTO countries VALUES (?, ?)", COUNTRIES)
    for cur, base in BASE_RATE.items():
        for i, month in enumerate(MONTHS):
            rate = 1.0 if cur == "USD" else round(base * (1 + 0.01 * ((i * 7) % 5 - 2)), 4)
            db.execute("INSERT INTO fx_rates VALUES (?, ?, ?)", (cur, month, rate))

    customers = []
    for cid in range(1, 241):
        country = RNG.choice([c for c, _ in COUNTRIES])
        kind = RNG.choices(["retail", "business", "staff_test"], weights=[70, 22, 8])[0]
        domain = "quillstack.io" if kind == "staff_test" else RNG.choice(["gmail.com", "outlook.com", "corp.example"])
        db.execute("INSERT INTO customers VALUES (?, ?, ?, ?)", (cid, f"user{cid}@{domain}", country, kind))
        customers.append((cid, country))

    oid = 0
    for month in MONTHS:
        for _ in range(RNG.randint(140, 180)):
            oid += 1
            cid, country = RNG.choice(customers)
            cur = CURRENCY[country]
            major = RNG.choice([19, 29, 49, 99, 149, 249, 499]) + RNG.choice([0, 0.5, 0.99])
            total_minor = round(major * BASE_RATE[cur]) if cur == "JPY" else round(major * BASE_RATE[cur] * 100)
            status = RNG.choices(["paid", "PAID", "refunded", "cancelled", "pending"], weights=[66, 12, 8, 8, 6])[0]
            day = RNG.randint(1, 28)
            ordered_at = f"{month}-{day:02d}T{RNG.randint(0, 23):02d}:{RNG.randint(0, 59):02d}:00Z"
            db.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", (oid, cid, ordered_at, status, cur, total_minor))
            if status.lower() == "paid" and RNG.random() < 0.12:
                db.execute("INSERT INTO refunds (order_id, refunded_at, amount_minor) VALUES (?, ?, ?)",
                           (oid, ordered_at, total_minor // RNG.choice([2, 4, 1])))
    db.commit()
    n = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    print(f"{path.name}: {len(customers)} customers, {n} orders")


if __name__ == "__main__":
    main()
