import unittest
import random

from Knapsack.BranchAndBound.BranchAndBound_MT import BranchAndBound_MT
from Knapsack.BranchAndBound.BranchAndBound_MODERN import BranchAndBound_MODERN
from Knapsack.Problems.KnapsackItem import KnapsackItem
from Knapsack.Problems.ZeroOneKnapsack import ZeroOneKnapsack


class TestBoundAndBranch_MODERN(unittest.TestCase):
    # Based on example 2.2 from the book
    def test_finds_optimal_solution(self):
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

        for i in range(0, len(actualItems)):
            self.assertEqual(expectedItems[i], actualItems[i])
    
    # Branch and Bound relies on items recieved to be given in sorted order
    # This checks if the algorithm finds a suboptimal solution if given items in a wrong order
    def test_given_unsorted_items_gives_suboptimal_solution(self):
        profits = [70, 20, 39, 37, 7, 5, 10]
        weights = [31, 10, 20, 19, 4, 3, 6]
        c = 50

        items = _generate_knapsack_items(profits, weights)

        # Make items be in random order
        random.shuffle(items)

        # The test can randomly fail if the items are randomly set to be in sorted order :D
        # This makes sure that aint the case
        sortedItems = items.copy()
        sortedItems.sort()
        notSorted = False

        while not notSorted:
            for i in range(len(items)):
                current = items[i]
                sortedItem = sortedItems[i]

                if current != sortedItem:
                    notSorted = True

        bab = BranchAndBound_MODERN(items, c)
        bab.startSearch()

        optimalItems = []
        optimalItems.append(items[0])
        optimalItems.append(items[3])

        bab = BranchAndBound_MODERN(items, c)
        bab.startSearch()

        actualItems = bab.bestSolution.items

        # TODO: would make a lot of sense to compare both solutions Z value
        # If not same length, BAB has found an incorrect solution
        if len(optimalItems) != len(actualItems):
            self.assertTrue(True)
            return

        # Check if actual and optimalItems differ by any 1 item
        equality = [0] * len(optimalItems)
        for i in range(len(optimalItems)):
            actual = actualItems[i]
            equality[i] = actual in optimalItems
        
        self.assertTrue(0 in equality)
    
    def test_calculates_correct_upper_bound(self):
        profits = [15, 100, 90, 60, 40, 15, 10, 1]
        weights = [2,  20,  20, 30, 40, 30, 60, 10]
        c = 102
        expected = 280

        items = _generate_knapsack_items(profits, weights)
        
        bab = BranchAndBound_MODERN(items, c)
        actual = bab.bestSolution.U

        self.assertEqual(expected, actual)

    def test_exits_early_when_given_lower_bound(self):
        profits = [70, 20, 39, 37, 7, 5, 10]
        weights = [31, 10, 20, 19, 4, 3, 6]
        c = 50
        lowerBound = 50

        items = _generate_knapsack_items(profits, weights)

        # The first item in the list has profit > lowerBound, so only first item should be inserted
        expectedItems = []
        expectedItems.append(items[0])

        self.assert_lower_bound_search(items, c, lowerBound, expectedItems)

        # This tests if the lower bound constraints doesn't pick infeasible solutions (too big weight)
        profits = [70,  20,  39,  37, 7, 5, 10]
        weights = [310, 100, 200, 19, 4, 3, 6]
        c = 50
        lowerBound = 20

        items = _generate_knapsack_items(profits, weights)

        expectedItems = []
        expectedItems.append(items[3])

        self.assert_lower_bound_search(items, c, lowerBound, expectedItems)
    
    def assert_lower_bound_search(self, items, c, lowerBound, expectedItems):
        bab = BranchAndBound_MODERN(items, c)
        bab.startSearchWithEarlyExit(lowerBound)

        actualItems = bab.bestSolution.items

        for i in range(0, len(actualItems)):
            self.assertEqual(expectedItems[i], actualItems[i])

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
