#!/usr/bin/env python3
"""Hidden acceptance check for the bank file, one check per rule of the spec.

Compares each part of the AI's output with a reference implementation, on
different data from the visible tests. One mistake fails only its own check:
records are split on CRLF or LF, so a wrong line ending costs one check, not
all of them. The AI never sees this file.

Usage: check.py <app-dir>   (imports that copy of ledger, one copy per process)
"""

import sys
from datetime import date
from pathlib import Path

APP = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(APP))
sys.path.insert(1, str(Path(__file__).parent))

import reference
from ledger.bankfile import export_bank_file
from ledger.models import BankPayment

RESULTS = []
DAY = date(2026, 11, 2)


def check(name, ok, detail=""):
    RESULTS.append(ok)
    mark = "\033[32mPASS\033[0m" if ok else "\033[31mFAIL\033[0m"
    print(f"  {mark}  {name}" + (f"\n          {detail}" if detail and not ok else ""))


def run(fn, payments, company="NORTHWIND1", seq=7):
    # The code under test is AI-written and may raise anything: report it, don't crash.
    try:
        return fn(payments, company, DAY, seq)
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {e}"


def records(text):
    if not isinstance(text, str) or text.startswith(("NotImplementedError", "TypeError")):
        return []
    sep = "\r\n" if "\r\n" in text else "\n"
    return text.split(sep)[:-1] if text.endswith(sep) else text.split(sep)


def field(recs, row, start, end):
    """1-based inclusive positions, like the spec."""
    return recs[row][start - 1:end] if row < len(recs) else None


def compare(name, payments, rows, start, end, **kw):
    got, want = records(run(export_bank_file, payments, **kw)), records(run(reference.export_bank_file, payments, **kw))
    bad = [(r, field(got, r, start, end), field(want, r, start, end)) for r in rows
           if field(got, r, start, end) != field(want, r, start, end)]
    check(name, not bad, "; ".join(f"record {r + 1}: got {g!r}, want {w!r}" for r, g, w in bad[:2]))


def main():
    mixed = [
        BankPayment("026009593", "00112233445566778", 98765, "Åsa Ödegård & Co.", "PAYOUT-2026-11-A"),
        BankPayment("121000358", "4455", -120000, "  o'brien--and   sons, inc.  ", "DD"),
        BankPayment("111000025", "7", 0, "Internationale Handelsgesellschaft mbH", ""),
    ]

    text = run(export_bank_file, mixed)
    raw = text if isinstance(text, str) else ""
    check("every record ends with CRLF, including the last",
          raw.endswith("\r\n") and "\n" not in raw.replace("\r\n", ""), f"output starts {raw[:90]!r}")
    recs = records(text)
    check("every record is exactly 80 characters",
          bool(recs) and all(len(r) == 80 for r in recs), f"lengths {sorted({len(r) for r in recs})}")

    compare("file header (company, date, sequence, spaces)", mixed, [0], 1, 80)
    compare("routing and account fields (account left-justified to 17)", mixed, [1, 2, 3], 2, 27)
    compare("amount: absolute cents, zero-padded, C/D (zero is C)", mixed, [1, 2, 3], 28, 38)
    compare("payee name cleaning (accents, symbols, spaces, 22 chars)", mixed, [1, 2, 3], 39, 60)
    compare("reference: 15 chars, truncated", mixed, [1, 2, 3], 61, 75)
    compare("record sequence numbers start at 1", mixed, [1, 2, 3], 76, 80)
    compare("control record: count and credit/debit totals", mixed, [4], 1, 31)

    many = [BankPayment("999999990", str(i), 100 + i, f"Payee {i}") for i in range(150)]
    compare("entry hash keeps the last 10 digits of a big sum", many, [151], 32, 41)

    eight = [BankPayment("021000021", str(i), 1000, "A") for i in range(8)]
    got = records(run(export_bank_file, eight))
    check("blocking: no filler when the count is already a multiple of 10", len(got) == 10,
          f"{len(got)} records for 8 payments")
    got = records(run(export_bank_file, []))
    check("blocking: an empty batch is padded to 10 with 9-filler",
          len(got) == 10 and got[2:] == ["9" * 80] * 8, f"{len(got)} records")

    bad = run(export_bank_file, [BankPayment("02100002X", "1", 100, "A")])
    check("a routing number that is not 9 digits raises ValueError",
          isinstance(bad, str) and bad.startswith("ValueError"), f"got {str(bad)[:60]!r}")
    bad = run(export_bank_file, [BankPayment("021000021", "1" * 18, 100, "A")])
    check("an account number over 17 characters raises ValueError",
          isinstance(bad, str) and bad.startswith("ValueError"), f"got {str(bad)[:60]!r}")

    passed = sum(RESULTS)
    print(f"\n  score: {passed}/{len(RESULTS)}")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
