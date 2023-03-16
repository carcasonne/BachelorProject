import unittest
import random

from Tests.test_knapsack.test_knapsackItem import TestKnapsackItemProperties
from Knapsack.BranchAndBound.BranchAndBound import BranchAndBound
from Knapsack.Problems.KnapsackItem import KnapsackItem
from Knapsack.Problems.ZeroOneKnapsack import ZeroOneKnapsack

class BoundAndBranchTest(unittest.TestCase):
    def test_finds_critical_item(self):
        instance = TestKnapsackItemProperties()
        items = instance._get_mock_items_sorted()

        c = 50
        expectedIndex = 3 # 4th item
        problem = ZeroOneKnapsack(items, c)
        bab = BranchAndBound(problem)
        actualIndex = bab.findCriticalItemAndResidualCapacity()[0]

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
        
        problem = ZeroOneKnapsack(items, c)
        bab = BranchAndBound(problem)
        actualIndex = bab.findCriticalItemAndResidualCapacity()[0]

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
        
        problem = ZeroOneKnapsack(items, c)
        bab = BranchAndBound(problem)
        actual = bab.optimalSolutionValue()

        self.assertEqual(expected, actual)

    def test_min_initialized_correctly(self):
        profits = [15, 100, 90, 60, 40, 15, 10, 1]
        weights = [2,  20,  20, 30, 40, 30, 60, 10]
        c = 102
        expected = [2, 10,  10, 10, 10, 10, 10, 10]

        items = []

        for i in range(len(profits)):
            p = profits[i]
            w = weights[i]
            item = KnapsackItem(p, w, 0)
            items.append(item)

        problem = ZeroOneKnapsack(items, c)
        bab = BranchAndBound(problem)
        actual = bab.M

        self.assertListEqual(expected, actual)

        pass

if __name__ == '__main__':
    unittest.main()