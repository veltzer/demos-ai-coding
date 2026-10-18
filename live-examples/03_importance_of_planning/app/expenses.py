#!/usr/bin/env python3
"""A tiny expense tracker. Expenses live in expenses.csv next to this file."""

import argparse
import csv
import sys
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["date", "category", "amount", "note"]


def load():
    with DATA_FILE.open(newline="") as f:
        return list(csv.DictReader(f))


def save(rows):
    with DATA_FILE.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def cmd_add(args):
    rows = load()
    rows.append({"date": args.date, "category": args.category,
                 "amount": args.amount, "note": args.note})
    save(rows)
    print(f"added {args.amount} to {args.category}")


def cmd_list(args):
    for row in load():
        if args.month and not row["date"].startswith(args.month):
            continue
        print(f"{row['date']}  {row['category']:<12} {row['amount']:>9}  {row['note']}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="expenses")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="record an expense")
    p_add.add_argument("date", help="YYYY-MM-DD")
    p_add.add_argument("category")
    p_add.add_argument("amount", help="e.g. 12.50, negative for a refund")
    p_add.add_argument("note", nargs="?", default="")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list expenses")
    p_list.add_argument("--month", help="YYYY-MM")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
