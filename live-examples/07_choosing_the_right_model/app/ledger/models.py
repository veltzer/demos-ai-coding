from dataclasses import dataclass


@dataclass
class Payment:
    date: str          # YYYY-MM-DD
    customer: str
    amount_cents: int
    memo: str = ""


@dataclass
class BankPayment:
    routing: str       # 9-digit bank routing number
    account: str
    amount_cents: int  # negative = debit (we collect), positive = credit (we pay)
    name: str
    reference: str = ""
