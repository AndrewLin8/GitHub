def determine_progress1(hits, spins):
    if spins == 0:
        return "Get going!"
    
    hits_spins_ratio = hits / spins

    if hits_spins_ratio > 0:
        progress = "On your way!"
        if hits_spins_ratio >= 0.25:
            progress = "Almost there!"
            if hits_spins_ratio >= 0.5:
                if hits < spins:
                    progress = "You win!"
    else:
        progress = "Get going!"

    return progress

def test_determine_progress(progress_function):
    """Test the determine_progress function with comprehensive test cases."""
    
    # Test case 1: spins = 0 returns "Get going!"
    assert progress_function(10, 0) == "Get going!", "Test case 1 failed: spins=0"
    
    # Test case 2: ratio = 0 (hits = 0) returns "Get going!"
    assert progress_function(0, 10) == "Get going!", "Test case 2 failed: ratio=0"
    
    # Test case 3: 0 < ratio < 0.25 returns "On your way!"
    assert progress_function(1, 10) == "On your way!", "Test case 3 failed: 0 < ratio < 0.25"
    
    # Test case 4: 0.25 <= ratio < 0.5 returns "Almost there!"
    assert progress_function(3, 10) == "Almost there!", "Test case 4 failed: 0.25 <= ratio < 0.5"
    
    # Test case 5: ratio >= 0.5 returns "You win!"
    assert progress_function(6, 10) == "You win!", "Test case 5 failed: ratio >= 0.5"
    
    print("All tests passed!")


def determine_progress2(hits, spins):
    """Version without nested if-statements (no elif or else)."""
    if spins == 0:
        return "Get going!"
    
    hits_spins_ratio = hits / spins
    
    if hits_spins_ratio >= 0.5 and hits < spins:
        return "You win!"
    if hits_spins_ratio >= 0.25:
        return "Almost there!"
    if hits_spins_ratio > 0:
        return "On your way!"
    
    return "Get going!"


def determine_progress3(hits, spins):
    """Version using if-elif-else conditions."""
    if spins == 0:
        return "Get going!"
    
    hits_spins_ratio = hits / spins
    
    if hits_spins_ratio >= 0.5 and hits < spins:
        return "You win!"
    elif hits_spins_ratio >= 0.25:
        return "Almost there!"
    elif hits_spins_ratio > 0:
        return "On your way!"
    else:
        return "Get going!"


# Run the tests
print("Testing determine_progress1:")
test_determine_progress(determine_progress1)

print("\nTesting determine_progress2:")
test_determine_progress(determine_progress2)

print("\nTesting determine_progress3:")
test_determine_progress(determine_progress3)

print("\n=== Comparison ===")
print("determine_progress1: Uses nested if-statements (hard to follow)")
print("determine_progress2: Flat if-statements without elif/else (works but less efficient)")
print("determine_progress3: Uses if-elif-else (BEST - clearest intent and most efficient)")
print("\nBEST VERSION: determine_progress3")
print("Reasons:")
print("- Most readable: elif clearly shows mutually exclusive conditions")
print("- Most efficient: Stops checking once a condition matches")
print("- Most maintainable: Easy to understand the flow at a glance")