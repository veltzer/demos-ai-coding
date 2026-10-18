"""Accounting feed parser."""

import csv
import io

from ledger.models import Payment
from ledger.money import parse


def from_csv(text):
    rows = list(csv.reader(io.StringIO(text)))[1:]
    return [Payment(date, customer, parse(amount), memo) for date, customer, amount, memo in rows]
