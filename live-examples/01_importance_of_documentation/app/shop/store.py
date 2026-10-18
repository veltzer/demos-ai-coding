"""In-memory store with JSON persistence."""

import json
from pathlib import Path

from shop.models import Customer, Line, Order, Status


class Store:
    def __init__(self):
        self.customers = {}
        self.orders = []
        self.stock = {}

    def add_customer(self, customer):
        self.customers[customer.id] = customer

    def add_order(self, order):
        self.orders.append(order)

    def orders_for(self, customer_id):
        return [o for o in self.orders if o.customer_id == customer_id]

    def next_order_id(self):
        return max((o.id for o in self.orders), default=0) + 1

    def save(self, path):
        data = {
            "customers": [vars(c) for c in self.customers.values()],
            "orders": [{"id": o.id, "customer_id": o.customer_id, "status": o.status.value,
                        "lines": [vars(line) for line in o.lines]} for o in self.orders],
            "stock": self.stock,
        }
        Path(path).write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text())
        store = cls()
        for c in data["customers"]:
            store.add_customer(Customer(**c))
        for o in data["orders"]:
            store.add_order(Order(o["id"], o["customer_id"],
                                  [Line(**line) for line in o["lines"]], Status(o["status"])))
        store.stock = data.get("stock", {})
        return store
