#!/usr/bin/env python3
"""Hidden acceptance check for revenue.sql.

Besides comparing with a reference query, each data quirk gets its own
invariance test: a copy of the database where that quirk is neutralised in
a way a correct query cannot notice (PAID rewritten as paid, test accounts'
orders deleted, refunds folded into the totals, foreign orders converted to
USD). If the query's answer changes on the copy, it got that quirk wrong.
The AI never sees this file.

Usage: check.py <app-dir> <shop.db>
"""

import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

REFERENCE = """
WITH net AS (
    SELECT substr(o.ordered_at, 1, 7) AS month, c.country_code, o.currency,
           o.total_minor - COALESCE((SELECT SUM(r.amount_minor) FROM refunds r WHERE r.order_id = o.id), 0)
               AS net_minor
    FROM orders o JOIN customers c ON c.id = o.customer_id
    WHERE lower(o.status) = 'paid' AND c.kind <> 'staff_test' AND o.ordered_at LIKE '2026-%'
)
SELECT net.month, co.name AS country,
       ROUND(SUM(net_minor / (CASE net.currency WHEN 'JPY' THEN 1.0 ELSE 100.0 END) / fx.rate), 2) AS revenue_usd
FROM net
JOIN fx_rates fx ON fx.currency = net.currency AND fx.month = net.month
JOIN countries co ON co.code = net.country_code
GROUP BY net.month, co.name ORDER BY net.month, co.name
"""

# name -> SQL that neutralises one quirk on a copy of the database
NEUTRALISE = {
    "status 'PAID' (upper case) counts as paid": "UPDATE orders SET status = 'paid' WHERE status = 'PAID'",
    "internal test accounts (kind 'staff_test') are excluded":
        "DELETE FROM orders WHERE customer_id IN (SELECT id FROM customers WHERE kind = 'staff_test')",
    "refunds are subtracted":
        "UPDATE orders SET total_minor = total_minor - COALESCE((SELECT SUM(amount_minor) FROM refunds r "
        "WHERE r.order_id = orders.id), 0); DELETE FROM refunds",
    "JPY has no minor unit (yen, not cents)":
        "UPDATE orders SET total_minor = CAST(ROUND(total_minor * 100.0 / (SELECT rate FROM fx_rates f "
        "WHERE f.currency = 'JPY' AND f.month = substr(orders.ordered_at, 1, 7))) AS INTEGER), currency = 'USD' "
        "WHERE currency = 'JPY'; UPDATE refunds SET amount_minor = CAST(ROUND(amount_minor * 100.0 / "
        "(SELECT rate FROM fx_rates f WHERE f.currency = 'JPY' AND f.month = substr(refunds.refunded_at, 1, 7))) "
        "AS INTEGER) WHERE order_id IN (SELECT id FROM orders WHERE currency = 'USD' AND customer_id IN "
        "(SELECT id FROM customers WHERE country_code = 'JP'))",
    "fx rate is per USD, so convert by dividing (EUR, GBP)":
        "UPDATE refunds SET amount_minor = CAST(ROUND(amount_minor / (SELECT f.rate FROM fx_rates f JOIN orders o "
        "ON o.id = refunds.order_id WHERE f.currency = o.currency AND f.month = substr(o.ordered_at, 1, 7))) "
        "AS INTEGER) WHERE order_id IN (SELECT id FROM orders WHERE currency IN ('EUR', 'GBP')); "
        "UPDATE orders SET total_minor = CAST(ROUND(total_minor / (SELECT rate FROM fx_rates f WHERE f.currency = "
        "orders.currency AND f.month = substr(orders.ordered_at, 1, 7))) AS INTEGER), currency = 'USD' "
        "WHERE currency IN ('EUR', 'GBP')",
}
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(ok)
    mark = "\033[32mPASS\033[0m" if ok else "\033[31mFAIL\033[0m"
    print(f"  {mark}  {name}" + (f"  ({detail})" if detail and not ok else ""))


def run(db_path, sql):
    try:
        con = sqlite3.connect(db_path)
        rows = con.execute(sql).fetchall()
        con.close()
        return [tuple(r) for r in rows]
    except sqlite3.Error as e:
        return f"{type(e).__name__}: {e}"


def same(a, b, tol=0.06):
    if not isinstance(a, list) or not isinstance(b, list) or len(a) != len(b):
        return False
    for ra, rb in zip(a, b, strict=True):
        if len(ra) != 3 or str(ra[0]) != str(rb[0]) or str(ra[1]) != str(rb[1]):
            return False
        if not isinstance(ra[2], (int, float)) or abs(ra[2] - rb[2]) > tol:
            return False
    return True


def total(rows):
    return round(sum(r[2] for r in rows if isinstance(r[2], (int, float))), 2) if isinstance(rows, list) else rows


def main():
    app, db = Path(sys.argv[1]), Path(sys.argv[2])
    sql_file = app / "revenue.sql"
    if not sql_file.exists():
        check("revenue.sql exists", False, "no revenue.sql")
        print(f"\n  score: 0/{len(NEUTRALISE) + 3}")
        return 1
    sql = sql_file.read_text().strip().rstrip(";")
    got, want = run(db, sql), run(db, REFERENCE)

    check("the query runs against shop.db", isinstance(got, list), str(got)[:100])
    check("columns month, country (name), revenue_usd; one row per month and country",
          isinstance(got, list) and len(got) == len(want) and all(len(r) == 3 for r in got)
          and {(str(r[0]), str(r[1])) for r in got} == {(r[0], r[1]) for r in want},
          f"{len(got) if isinstance(got, list) else 0} rows, want {len(want)}; first: {got[:1] if isinstance(got, list) else ''}")

    with tempfile.TemporaryDirectory() as tmp:
        for name, fix in NEUTRALISE.items():
            copy = Path(tmp) / "copy.db"
            shutil.copy(db, copy)
            con = sqlite3.connect(copy)
            con.executescript(fix)
            con.commit()
            con.close()
            after = run(copy, sql)
            # Converting orders rounds each one to a cent, so allow drift of
            # a dollar per row; the mistakes this catches are far bigger.
            check(name, isinstance(got, list) and same(got, after, tol=1.0),
                  f"total changes from {total(got)} to {total(after)} when this is neutralised")

    check("every number matches the reference", same(got, want),
          f"total {total(got)}, want {total(want)}")
    passed = sum(RESULTS)
    print(f"\n  score: {passed}/{len(RESULTS)}")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
