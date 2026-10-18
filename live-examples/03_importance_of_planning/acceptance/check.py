#!/usr/bin/env python3
"""Hidden acceptance check for the `report` feature.

These are the decisions the "product owner" had in mind but never wrote into
the original request. The AI never sees this file: it is run against each
finished work directory only after the AI is done.

Usage: check.py <app-dir>
"""

import re
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

# "<label>  <amount>", tolerating "label:", "$1,200.00" and table pipes. The
# amount must have a decimal point so headers like "September 2026" are skipped.
LINE = re.compile(r"^\s*\|?\s*([A-Za-z][\w ]*?)\s*[:|]?\s+\$?(-?[\d,]*\d\.\d+)\s*\|?\s*$")

EXPECTED = [
    ("rent", Decimal("1200.00")),
    ("food", Decimal("80.00")),
    ("books", Decimal("40.00")),
    ("transport", Decimal("40.00")),
    ("health", Decimal("19.99")),
]
EXPECTED_TOTAL = Decimal("1379.99")


def run(app, *args):
    proc = subprocess.run([sys.executable, "expenses.py", *args], cwd=app,
                          capture_output=True, text=True, timeout=30, check=False)
    return proc.returncode, proc.stdout + proc.stderr


def parse(output):
    """Return ([(category, amount), ...], total-or-None) from report output."""
    rows, total = [], None
    for line in output.splitlines():
        m = LINE.match(line)
        if not m:
            continue
        label, amount = m.group(1).strip().lower(), Decimal(m.group(2).replace(",", ""))
        if "total" in label:
            total = amount
        else:
            rows.append((label, amount))
    return rows, total


def main():
    app = Path(sys.argv[1])
    results = []

    def check(name, ok, detail=""):
        results.append(ok)
        mark = "\033[32mPASS\033[0m" if ok else "\033[31mFAIL\033[0m"
        print(f"  {mark}  {name}" + (f"  ({detail})" if detail and not ok else ""))

    # The flag is one decision; don't let it sink the others. If `--month`
    # is rejected, read the report through a positional month instead.
    code, out = run(app, "report", "--month", "2026-09")
    check("month given as --month, like `list` does", code == 0)
    if code != 0:
        code, out = run(app, "report", "2026-09")
    check("report for 2026-09 runs", code == 0,
          out.strip().splitlines()[-1] if out.strip() else "")
    rows, total = parse(out) if code == 0 else ([], None)
    got = dict(rows)
    names = [n for n, _ in rows]
    wanted = [n for n, _ in EXPECTED]

    check("categories merged ignoring case/spaces (Food, FOOD -> food)",
          len(names) == len(set(names)) and "food" in got,
          f"categories seen: {names}")
    check("refunds are subtracted (food = 80.00)",
          got.get("food") == Decimal("80.00"), f"food = {got.get('food')}")
    check("categories that net to zero are hidden (fun)",
          bool(rows) and "fun" not in got, f"fun = {got.get('fun')}")
    check("sorted by amount desc, ties alphabetically",
          [n for n in names if n in wanted] == wanted, f"order: {names}")
    check("grand total line (1379.99)", total == EXPECTED_TOTAL, f"total = {total}")

    code2, out2 = run(app, "report")
    check("no --month means latest month with data (2026-09)",
          code2 == 0 and parse(out2) == (rows, total) and rows != [],
          "output differs from --month 2026-09")

    code3, out3 = run(app, "list", "--month", "2026-08")
    check("existing `list` command still works", code3 == 0 and "august rent" in out3)

    passed = sum(results)
    print(f"\n  score: {passed}/{len(results)}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
