from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


@dataclass
class Customer:
    id: int
    name: str
    email: str


@dataclass
class Line:
    sku: str
    qty: int
    unit_cents: int

    @property
    def cents(self):
        return self.qty * self.unit_cents


@dataclass
class Order:
    id: int
    customer_id: int
    lines: list[Line] = field(default_factory=list)
    status: Status = Status.PENDING

    @property
    def subtotal(self):
        return sum(line.cents for line in self.lines)

    @property
    def items(self):
        return sum(line.qty for line in self.lines)
