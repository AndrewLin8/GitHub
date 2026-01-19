#!/usr/bin/env python3
import argparse
import sys


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number, please try again.")


def compute(a, b, op):
    key = op.strip().lower()
    mapping = {
        '+': '+', 'add': '+',
        '-': '-', 'subtract': '-', 'sub': '-',
        '*': '*', 'x': '*', 'multiply': '*',
        '/': '/', 'divide': '/',
    }
    if key not in mapping:
        return False, "Unknown operation."

    symbol = mapping[key]
    if symbol == '+':
        return True, a + b
    if symbol == '-':
        return True, a - b
    if symbol == '*':
        return True, a * b
    if symbol == '/':
        try:
            return True, a / b
        except ZeroDivisionError:
            return False, "Error: Division by zero is not allowed."


def main():
    print("Simple Calculator")
    a = get_number("Enter first number: ")
    b = get_number("Enter second number: ")

    print("Choose operation:")
    print("  +  Add")
    print("  -  Subtract")
    print("  *  Multiply")
    print("  /  Divide")
    op = input("Operation (+ - * /): ").strip()

    ok, result = compute(a, b, op)
    if not ok:
        print(result)
        return

    print(f"Result: {result}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple calculator: provide two numbers and an operation, or run interactively.")
    parser.add_argument('num1', nargs='?', help='first number')
    parser.add_argument('num2', nargs='?', help='second number')
    parser.add_argument('op', nargs='?', help='operation (e.g. +, -, *, / or add, subtract, multiply, divide)')
    args = parser.parse_args()

    if args.num1 is not None and args.num2 is not None and args.op is not None:
        try:
            a = float(args.num1)
        except ValueError:
            print("Invalid number for first argument")
            sys.exit(2)
        try:
            b = float(args.num2)
        except ValueError:
            print("Invalid number for second argument")
            sys.exit(2)

        ok, result = compute(a, b, args.op)
        if not ok:
            print(result)
            sys.exit(1)
        print(f"Result: {result}")
    else:
        try:
            main()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            sys.exit(0)
