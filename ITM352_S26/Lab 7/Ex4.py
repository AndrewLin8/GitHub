def check_budget(purchases, budget):
    """
    Check each purchase against a budget and print status messages.
    
    Args:
        purchases (list): List of expense amounts
        budget (float): Budget threshold
    """
    for expense in purchases:
        if expense > budget:
            print("This purchase is over budget!")
        else:
            print("This purchase is within budget")


# Test cases
import unittest

class TestCheckBudget(unittest.TestCase):
    def test_mixed_purchases(self):
        """Test with mixed over and under budget purchases"""
        purchases = [36.13, 23.87, 183.35, 22.93, 11.62]
        budget = 50
        check_budget(purchases, budget)
    
    def test_all_under_budget(self):
        """Test when all purchases are under budget"""
        purchases = [10.00, 20.00, 30.00]
        budget = 50
        check_budget(purchases, budget)
    
    def test_all_over_budget(self):
        """Test when all purchases are over budget"""
        purchases = [100.00, 200.00, 300.00]
        budget = 50
        check_budget(purchases, budget)
    
    def test_empty_list(self):
        """Test with empty purchase list"""
        purchases = []
        budget = 50
        check_budget(purchases, budget)
    
    def test_exact_budget(self):
        """Test when purchase equals budget"""
        purchases = [50.00]
        budget = 50
        check_budget(purchases, budget)


if __name__ == '__main__':
    unittest.main()