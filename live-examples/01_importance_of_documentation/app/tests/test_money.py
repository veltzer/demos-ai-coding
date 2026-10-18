import unittest

from shop.money import fmt, parse, percent_of


class MoneyTest(unittest.TestCase):
    def test_round_trip(self):
        self.assertEqual(parse("12.30"), 1230)
        self.assertEqual(fmt(1230), "12.30")
        self.assertEqual(fmt(-5), "-0.05")

    def test_percent_of_rounds_down(self):
        self.assertEqual(percent_of(1999, 10), 199)


if __name__ == "__main__":
    unittest.main()
