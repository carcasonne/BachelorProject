import unittest
import random

from Tests.test_knapsack.test_knapsackItem import TestKnapsackItemProperties
from Knapsack.BranchAndBound.BranchAndBound import BranchAndBound
from Knapsack.Problems.KnapsackItem import KnapsackItem

class BoundAndBranchTest(unittest.TestCase):
    def test_finds_critical_item(self):
        instance = TestKnapsackItemProperties()
        items = instance._get_mock_items_sorted()

        c = 50
        expectedIndex = 3 # 4th item

        problem = BranchAndBound(items, c)
        actualIndex = problem.findCriticalItem()[0]

        self.assertEqual(expectedIndex, actualIndex)
    
    # This is based on example 2.1
    def test_finds_critical_item_book(self):
        profits = [15, 100, 90, 60, 40, 15, 10, 1]
        weights = [2,  20,  20, 30, 40, 30, 60, 10]
        c = 102
        expectedIndex = 4 # item 5, index 4

        items = []

        for i in range(len(profits)):
            p = profits[i]
            w = weights[i]
            item = KnapsackItem(p, w, 0)
            items.append(item)
        
        problem = BranchAndBound(items, c)
        actualIndex = problem.findCriticalItemAndResidualCapacity()[0]

        self.assertEqual(expectedIndex, actualIndex)
    
    # This is based on example 2.1
    def test_calculates_correct_upper_bound(self):
        profits = [15, 100, 90, 60, 40, 15, 10, 1]
        weights = [2,  20,  20, 30, 40, 30, 60, 10]
        c = 102
        expected = 285

        items = []

        for i in range(len(profits)):
            p = profits[i]
            w = weights[i]
            item = KnapsackItem(p, w, 0)
            items.append(item)
        
        problem = BranchAndBound(items, c)
        actual = problem.optimalSolutionValue()

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()