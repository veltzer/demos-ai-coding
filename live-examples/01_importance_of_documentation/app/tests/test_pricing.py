import unittest

from shop.models import Customer, Line, Order, Status
from shop.pricing import price_order
from shop.store import Store


def make_store(*statuses):
    store = Store()
    store.add_customer(Customer(1, "Ada", "ada@example.com"))
    for i, status in enumerate(statuses, start=1):
        store.add_order(Order(i, 1, [Line("mug", 1, 1200)], status))
    return store


class PricingTest(unittest.TestCase):
    def test_welcome_on_first_order(self):
        store = make_store()
        quote = price_order(store, Order(1, 1, [Line("mug", 1, 1200)]))
        self.assertEqual(quote.total, 700)
        self.assertEqual(quote.applied, ["WELCOME"])

    def test_no_welcome_after_first_order(self):
        store = make_store(Status.PAID)
        quote = price_order(store, Order(2, 1, [Line("mug", 1, 1200)]))
        self.assertEqual(quote.total, 1200)

    def test_bulk(self):
        store = make_store(Status.PAID)
        quote = price_order(store, Order(2, 1, [Line("pen", 10, 150)]))
        self.assertEqual(quote.total, 1200)
        self.assertEqual(quote.applied, ["BULK"])


if __name__ == "__main__":
    unittest.main()
