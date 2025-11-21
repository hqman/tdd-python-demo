import pytest
from tdd_python_demo.calculator import Calculator


class TestCalculator:
    def test_add_two_positive_numbers(self):
        calc = Calculator()
        result = calc.add(2, 3)
        assert result == 5

    def test_add_negative_numbers(self):
        calc = Calculator()
        result = calc.add(-2, -3)
        assert result == -5

    def test_add_float_numbers(self):
        calc = Calculator()
        result = calc.add(2.5, 3.7)
        assert result == 6.2

    def test_subtract_two_positive_numbers(self):
        calc = Calculator()
        result = calc.subtract(5, 3)
        assert result == 2

    def test_subtract_negative_numbers(self):
        calc = Calculator()
        result = calc.subtract(5, -3)
        assert result == 8

    def test_multiply_two_positive_numbers(self):
        calc = Calculator()
        result = calc.multiply(4, 5)
        assert result == 20

    def test_multiply_by_zero(self):
        calc = Calculator()
        result = calc.multiply(5, 0)
        assert result == 0

    def test_multiply_negative_numbers(self):
        calc = Calculator()
        result = calc.multiply(-3, 4)
        assert result == -12

    def test_divide_two_positive_numbers(self):
        calc = Calculator()
        result = calc.divide(10, 2)
        assert result == 5

    def test_divide_by_zero_raises_error(self):
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        calc = Calculator()
        result = calc.divide(-10, 2)
        assert result == -5
