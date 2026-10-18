import unittest
from decimal import Decimal

from billing.rounding import round_cents


class RoundingTest(unittest.TestCase):
    def test_rounds_to_cents(self):
        self.assertEqual(round_cents(Decimal("1.234")), Decimal("1.23"))
        self.assertEqual(round_cents(Decimal("1.236")), Decimal("1.24"))

    def test_ties_round_up(self):
        self.assertEqual(round_cents(Decimal("0.125")), Decimal("0.13"))
        self.assertEqual(round_cents(Decimal("2.665")), Decimal("2.67"))


if __name__ == "__main__":
    unittest.main()
