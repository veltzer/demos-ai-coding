"""Invoice totals."""

from dataclasses import dataclass, field
from decimal import Decimal

from billing.rounding import round_cents

VAT = Decimal("0.17")


@dataclass
class Line:
    description: str
    qty: Decimal
    unit_price: Decimal

    @property
    def total(self):
        return round_cents(self.qty * self.unit_price)


@dataclass
class Invoice:
    lines: list[Line] = field(default_factory=list)

    @property
    def subtotal(self):
        return sum((line.total for line in self.lines), Decimal(0))

    @property
    def vat(self):
        return round_cents(self.subtotal * VAT)

    @property
    def total(self):
        return self.subtotal + self.vat
