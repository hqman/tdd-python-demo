"""Command-line interface for calculator."""

import sys


def main(argv=None):
    """Main entry point for the calculator CLI command."""
    if argv is None:
        argv = sys.argv[1:]

    operation = argv[0]
    num1 = int(argv[1])
    num2 = int(argv[2])

    try:
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2

        print(result)
        return 0
    except ZeroDivisionError:
        print('Error: division by zero', file=sys.stderr)
        return 1
