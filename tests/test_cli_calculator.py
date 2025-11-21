"""Tests for the calculator CLI."""

import io
import sys

from tdd_python_demo.cli_calculator import main


def test_cli_calculator_performs_addition():
    """Test that CLI calculator can perform addition."""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    result = main(['add', '2', '3'])

    sys.stdout = sys.__stdout__

    assert result == 0
    output = captured_output.getvalue().strip()
    assert output == '5'


def test_cli_calculator_performs_addition_with_different_numbers():
    """Test that CLI calculator can add different numbers."""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    result = main(['add', '10', '20'])

    sys.stdout = sys.__stdout__

    assert result == 0
    output = captured_output.getvalue().strip()
    assert output == '30'


def test_cli_calculator_handles_negative_numbers():
    """Test that CLI calculator can handle negative numbers."""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    result = main(['add', '-5', '3'])

    sys.stdout = sys.__stdout__

    assert result == 0
    output = captured_output.getvalue().strip()
    assert output == '-2'


def test_cli_calculator_performs_subtraction():
    """Test that CLI calculator can perform subtraction."""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    result = main(['subtract', '10', '3'])

    sys.stdout = sys.__stdout__

    assert result == 0
    output = captured_output.getvalue().strip()
    assert output == '7'


def test_cli_calculator_performs_multiplication():
    """Test that CLI calculator can perform multiplication."""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    result = main(['multiply', '4', '5'])

    sys.stdout = sys.__stdout__

    assert result == 0
    output = captured_output.getvalue().strip()
    assert output == '20'


def test_cli_calculator_performs_division():
    """Test that CLI calculator can perform division."""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    result = main(['divide', '20', '4'])

    sys.stdout = sys.__stdout__

    assert result == 0
    output = captured_output.getvalue().strip()
    assert output == '5.0'


def test_cli_calculator_handles_division_by_zero():
    """Test that CLI calculator handles division by zero gracefully."""
    import sys
    captured_output = io.StringIO()
    captured_error = io.StringIO()
    sys.stdout = captured_output
    sys.stderr = captured_error

    result = main(['divide', '10', '0'])

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    assert result == 1
    error_output = captured_error.getvalue()
    assert 'Error' in error_output or 'division by zero' in error_output.lower()
