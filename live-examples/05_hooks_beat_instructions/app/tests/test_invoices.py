import unittest
from decimal import Decimal

from billing.invoices import Invoice, Line


class InvoiceTest(unittest.TestCase):
    def test_totals(self):
        inv = Invoice([Line("widget", Decimal(3), Decimal("19.99")),
                       Line("setup", Decimal(1), Decimal("50.00"))])
        self.assertEqual(inv.subtotal, Decimal("109.97"))
        self.assertEqual(inv.vat, Decimal("18.69"))
        self.assertEqual(inv.total, Decimal("128.66"))

    def test_half_cent_line_rounds_up(self):
        inv = Invoice([Line("bolts", Decimal(5), Decimal("0.125"))])
        self.assertEqual(inv.lines[0].total, Decimal("0.63"))


if __name__ == "__main__":
    unittest.main()
