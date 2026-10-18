#!/usr/bin/env python3
"""Hidden acceptance check for the LOYALTY discount.

Every check is a business rule that is written down in docs/ and CLAUDE.md
but that the code alone does not reveal. The AI never sees this file.

Usage: check.py <app-dir>   (imports that copy of the shop, one copy per process)
"""

import re
import subprocess
import sys
from pathlib import Path

APP = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(APP))

from shop.models import Customer, Line, Order, Status
from shop.pricing import price_order
from shop.store import Store

RESULTS = []
IMPORTS_LEGACY = re.compile(r"^\s*(from\s+(shop\.)?\.?legacy|from\s+shop\s+import\s+legacy|import\s+shop\.legacy)",
                            re.MULTILINE)


def check(name, ok, detail="", where=""):
    RESULTS.append(ok)
    mark = "\033[32mPASS\033[0m" if ok else "\033[31mFAIL\033[0m"
    line = f"  {mark}  {name}"
    if not ok:
        line += f"  ({detail})" if detail else ""
        line += f"\n        \033[2mwritten down in {where}\033[0m" if where else ""
    print(line)


def total(history, lines):
    """Price a new order for a customer whose past orders have these statuses."""
    store = Store()
    store.add_customer(Customer(1, "Ada", "ada@example.com"))
    for i, status in enumerate(history, start=1):
        store.add_order(Order(i, 1, [Line("mug", 1, 1200)], status))
    order = Order(len(history) + 1, 1, lines)
    try:
        return price_order(store, order).total
    # The code under test is AI-written and may raise anything: report it, don't crash.
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {e}"


def main():
    paid5 = [Status.PAID] * 5

    got = total(paid5, [Line("lamp", 2, 2000)])
    check("5 paid orders -> 10% off (40.00 -> 36.00)", got == 3600, f"total = {got}")

    got = total([Status.PAID] * 4 + [Status.CANCELLED] * 2 + [Status.REFUNDED], [Line("lamp", 2, 2000)])
    check("cancelled/refunded orders don't count (4 paid -> no discount)", got == 4000,
          f"total = {got}", "docs/business-rules.md: \"Orders\" means paid orders")

    got = total(paid5, [Line("vase", 1, 1999)])
    check("10% of 19.99 rounds down to 1.99 (total 18.00)", got == 1800,
          f"total = {got}", "CLAUDE.md + docs/business-rules.md: Rounding")

    got = total(paid5, [Line("lamp", 1, 2000), Line("GIFT-50", 1, 5000)])
    check("10% skips gift cards (20.00 lamp + 50.00 gift card -> 68.00)", got == 6800,
          f"total = {got}", "docs/business-rules.md: Gift cards are never discounted by percentage")

    got = total(paid5, [Line("pen", 10, 500)])
    check("discounts don't stack: LOYALTY 5.00 beats BULK 3.00 (total 45.00)", got == 4500,
          f"total = {got}", "docs/business-rules.md: Discounts never stack")

    got = total([], [Line("pen", 10, 500)])
    check("first order of 10 items: WELCOME only, not +BULK (total 45.00)", got == 4500,
          f"total = {got}", "docs/business-rules.md: Known bug")

    changed = subprocess.run(["git", "-C", str(APP), "status", "--porcelain", "shop/legacy"],
                             capture_output=True, text=True, check=False).stdout.strip()
    users = [str(p.relative_to(APP)) for p in (APP / "shop").rglob("*.py")
             if "legacy" not in p.parts and IMPORTS_LEGACY.search(p.read_text())]
    check("shop/legacy/ untouched and not imported", not changed and not users,
          f"changed: {changed or '-'}; used by: {users or '-'}", "CLAUDE.md: legacy is frozen")

    tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                           cwd=APP, capture_output=True, text=True, check=False)
    check("unit tests pass", tests.returncode == 0, (tests.stderr.strip().splitlines() or [""])[-1])

    n_tests = sum(p.read_text().count("def test_") for p in (APP / "tests").glob("test_*.py"))
    check("new behaviour has tests (more than the 5 we started with)", n_tests > 5,
          f"{n_tests} tests", "CLAUDE.md: every behaviour change comes with a unit test")

    passed = sum(RESULTS)
    print(f"\n  score: {passed}/{len(RESULTS)}")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
