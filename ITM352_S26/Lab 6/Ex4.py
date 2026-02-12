def is_leap_year(year):
    """
    Determine if a year is a leap year using if-statements.
    Returns "Leap year" or "Not a leap year"
    """
    # Check divisibility by 400 first (highest priority)
    if year % 400 == 0:
        return "Leap year"
    
    # Check divisibility by 100 (overrides divisibility by 4)
    if year % 100 == 0:
        return "Not a leap year"
    
    # Check divisibility by 4 (lowest priority)
    if year % 4 == 0:
        return "Leap year"
    
    # All other years are not leap years
    return "Not a leap year"


def test_is_leap_year(test_func):
    """Test the is_leap_year function with comprehensive test cases."""
    
    # Test case 1: Divisible by 400 -> Leap year
    assert test_func(2000) == "Leap year", "Test case 1 failed: 2000 (divisible by 400)"
    
    # Test case 2: Divisible by 100 but not 400 -> Not a leap year
    assert test_func(1900) == "Not a leap year", "Test case 2 failed: 1900 (divisible by 100)"
    
    # Test case 3: Divisible by 4 but not 100 -> Leap year
    assert test_func(2004) == "Leap year", "Test case 3 failed: 2004 (divisible by 4)"
    
    # Test case 4: Not divisible by 4 -> Not a leap year
    assert test_func(2001) == "Not a leap year", "Test case 4 failed: 2001 (not divisible by 4)"
    
    # Test case 5: Another divisible by 400 -> Leap year
    assert test_func(2400) == "Leap year", "Test case 5 failed: 2400 (divisible by 400)"
    
    print("All tests passed!")


# Run the tests
print("Testing is_leap_year function:")
test_is_leap_year(is_leap_year)

# Additional examples
print("\nAdditional examples:")
birth_year = 2005
closest_leap = 2004

print(f"{birth_year} is a leap year? {is_leap_year(birth_year)}")
print(f"{closest_leap} is a leap year? {is_leap_year(closest_leap)}")

print("\n=== Design Considerations ===")
print("1. ORDER OF CONDITIONALS (CRITICAL):")
print("   - Check divisibility by 400 FIRST (most specific rule)")
print("   - Then check divisibility by 100 (overrides the /4 rule)")
print("   - Then check divisibility by 4 (least specific)")
print("   - Wrong order would produce incorrect results!")
print()
print("2. USE OF EARLY RETURN:")
print("   - Each if-statement returns immediately when condition is true")
print("   - Avoids need for complex nested if-else chains")
print("   - More readable: no need to track a variable through multiple levels")
print("   - Better performance: stops checking once result is determined")
print()
print("3. IF-STATEMENTS VS IF-ELSE:")
print("   - Used flat if-statements instead of if-elif-else")
print("   - Each condition is independent due to early returns")
print("   - Final return statement handles the default case")
print("   - Simpler and cleaner than nested if-elif-else chains")
