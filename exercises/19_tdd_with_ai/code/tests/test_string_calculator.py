import pytest
from src.string_calculator import StringCalculator

class TestStringCalculator:
    def setup_method(self):
        self.calc = StringCalculator()

    def test_empty_string_returns_zero(self):
        """Empty string should return 0."""
        assert self.calc.add("") == 0

    def test_single_number_returns_that_number(self):
        """Single number should return that number."""
        assert self.calc.add("1") == 1
        assert self.calc.add("5") == 5

    def test_two_numbers_comma_delimited_returns_sum(self):
        """Two numbers separated by comma should return their sum."""
        assert self.calc.add("1,2") == 3
        assert self.calc.add("10,20") == 30

    def test_multiple_numbers_returns_sum(self):
        """Multiple numbers should return their sum."""
        assert self.calc.add("1,2,3") == 6
        assert self.calc.add("1,2,3,4,5") == 15
        assert self.calc.add("10,20,30,40") == 100

    def test_newline_as_delimiter(self):
        """Newlines can be used as delimiters."""
        assert self.calc.add("1\n2,3") == 6
        assert self.calc.add("1\n2\n3") == 6
        assert self.calc.add("10\n20,30") == 60

    def test_negative_numbers_throw_exception(self):
        """Negative numbers should throw exception with the negative number in message."""
        with pytest.raises(ValueError, match="Negatives not allowed: -1"):
            self.calc.add("1,-1,2")

        with pytest.raises(ValueError, match="Negatives not allowed: -1, -2"):
            self.calc.add("1,-1,2,-2")

    def test_numbers_bigger_than_1000_ignored(self):
        """Numbers bigger than 1000 should be ignored."""
        assert self.calc.add("2,1001") == 2
        assert self.calc.add("1000,1001,2") == 1002

    def test_custom_delimiter(self):
        """Support custom delimiter specified in format: //[delimiter]\n[numbers]"""
        assert self.calc.add("//;\n1;2") == 3
        assert self.calc.add("//|\n1|2|3") == 6
        assert self.calc.add("//sep\n1sep2sep3") == 6

# Run tests - they should fail (Red)
