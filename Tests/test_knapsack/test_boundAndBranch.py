import unittest
import random

from Tests.test_knapsack.test_knapsackItem import TestKnapsackItemProperties
from Knapsack.BranchAndBound.BranchAndBound_MT import BranchAndBound_MT
from Knapsack.BranchAndBound.BranchAndBound_MODERN import BranchAndBound_MODERN
from Knapsack.Problems.KnapsackItem import KnapsackItem
from Knapsack.Problems.ZeroOneKnapsack import ZeroOneKnapsack


class TestBoundAndBranch_MODERN(unittest.TestCase):
    # Based on example 2.2 from the book

    def test_finds_correct_solution(self):
        profits = [70, 20, 39, 37, 7, 5, 10]
        weights = [31, 10, 20, 19, 4, 3, 6]
        c = 50

        items = _generate_knapsack_items(profits, weights)

        expectedItems = []
        expectedItems.append(items[0])
        expectedItems.append(items[3])

        bab = BranchAndBound_MODERN(items, c)
        bab.startSearch()

        actualItems = bab.bestSolution.items

        for i in range(0, len(expectedItems)):
            self.assertEqual(expectedItems[i], actualItems[i])
    
    def test_calculates_correct_upper_bound(self):
        n = 8
        profits = [15, 100, 90, 60, 40, 15, 10, 1]
        weights = [2,  20,  20, 30, 40, 30, 60, 10]
        c = 102
        expected = 280

        items = _generate_knapsack_items(profits, weights)
        
        bab = BranchAndBound_MODERN(items, c)
        actual = bab.bestSolution.U

        self.assertEqual(expected, actual)


        pass

# Incomplete test cases as we moved away from using this implementation
class TestBoundAndBranch_MT(unittest.TestCase):
    def test_finds_critical_item(self):
        profits = [60, 60, 100, 120, 60, 10]
        weights = [10, 10, 20, 30, 20, 9]

        items = _generate_knapsack_items(profits, weights)

        c = 50
        expectedIndex = 4 # 4th item
        problem = ZeroOneKnapsack(items, c)
        bab = BranchAndBound_MT(problem)
        actualIndex = bab.findCriticalItemAndResidualCapacity()[0]

        self.assertEqual(expectedIndex, actualIndex)
    
    # This is based on example 2.1
    def test_finds_critical_item_book(self):
        profits = [15, 100, 90, 60, 40, 15, 10, 1]
        weights = [2,  20,  20, 30, 40, 30, 60, 10]
        c = 102
        expectedIndex = 5 # item 5, index 4

        items = _generate_knapsack_items(profits, weights)
        
        problem = ZeroOneKnapsack(items, c)
        bab = BranchAndBound_MT(problem)
        actualIndex = bab.findCriticalItemAndResidualCapacity()[0]

        self.assertEqual(expectedIndex, actualIndex)
    
    # This is based on example 2.1
    def test_calculates_correct_upper_bound(self):
        profits = [15, 100, 90, 60, 40, 15, 10, 1]
        weights = [2,  20,  20, 30, 40, 30, 60, 10]
        c = 102
        expected = 285

        items = _generate_knapsack_items(profits, weights)
        
        problem = ZeroOneKnapsack(items, c)
        bab = BranchAndBound_MT(problem)
        actual = bab.optimalSolutionValue()

        self.assertEqual(expected, actual)

    def test_min_initialized_correctly(self):
        profits = [15, 100, 90, 60, 40, 15, 10, 1]
        weights = [2,  20,  20, 30, 40, 30, 60, 10]
        c = 102
        expected = [2, 10,  10, 10, 10, 10, 10, 10]

        items = _generate_knapsack_items(profits, weights)

        problem = ZeroOneKnapsack(items, c)
        bab = BranchAndBound_MT(problem)
        mins = bab.M
        actual = []
        # get rid of mock item
        for i in range(1, len(mins)):
            actual.append(mins[i])


        self.assertListEqual(expected, actual)

        pass

def _generate_knapsack_items(profits, weights):
    items = []

    for i in range(len(profits)):
        p = profits[i]
        w = weights[i]
        item = KnapsackItem(p, w, 0)
        items.append(item)

    return items

if __name__ == '__main__':
    unittest.main()
