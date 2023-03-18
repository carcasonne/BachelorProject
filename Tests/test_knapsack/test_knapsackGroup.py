import unittest
import random

from Knapsack.Problems.KnapsackItem import KnapsackItem
from Knapsack.Problems.ItemGroup import ItemGroup
from Knapsack.Problems.BoundedKnapsack import BoundedKnapsack
#from Knapsack.Problems.ZeroOneKnapsack import ZeroOneKnapsac
from Knapsack.BranchAndBound.BranchAndBound_MODERN import BranchAndBound_MODERN

class TestKnapsackItemProperties(unittest.TestCase):
    def test_converted_correctly_to_zeroOneKnapsack_efficient(self):
        expectedProfits = [10, 20, 30, 15, 30, 15, 11, 11]
        expectedWeights = [1,   2,  3,  3,  6,  3,  5,  5]
        expectedItems = _generate_knapsack_items(expectedProfits, expectedWeights)

        c = 10 # Not important for test, but needed to create instances

        mockItems = self._get_mock_items_sorted()

        boundedProblem = BoundedKnapsack(mockItems, c)
        zeroOneProblem = boundedProblem.asZeroOne_efficient()

        actualItems = zeroOneProblem.items

        self.assertListEqual(expectedItems, actualItems)

    def test_converted_correctly_to_zeroOneKnapsack_simple(self):
        expectedProfits = [10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 11, 11]
        expectedWeights = [1,   1,  1,  1,  1,  1,  3,  3,  3,  3,  5,  5]
        expectedItems = _generate_knapsack_items(expectedProfits, expectedWeights)

        c = 10 # Not important for test, but needed to create instances

        mockItems = self._get_mock_items_sorted()

        boundedProblem = BoundedKnapsack(mockItems, c)
        zeroOneProblem = boundedProblem.asZeroOne_simple()

        actualItems = zeroOneProblem.items

        self.assertListEqual(expectedItems, actualItems)
    
    def test_item_groups_sorted_correctly(self):
        expectedItems = self._get_mock_items_sorted()
        randomItems = self._get_mock_items_random_order()

        actualItems = randomItems.copy()
        actualItems.sort()

        self.assertListEqual(expectedItems, actualItems)
    
    def test_bounded_to_zeroOne_simple_and_efficient_get_same_solutions(self):
        items = self._get_mock_items_sorted()
        c = 10

        # Smart version
        efficientBoundedProblem = BoundedKnapsack(items, c)
        efficientZeroOneProblem = efficientBoundedProblem.asZeroOne_efficient()
        
        efficientBAB = BranchAndBound_MODERN(efficientZeroOneProblem)
        efficientBAB.startSearch()

        efficientResult = efficientBAB.bestSolution
        
        # Stupid version
        simpleBoundedProblem = BoundedKnapsack(items, c)
        simpleZeroOneProblem = simpleBoundedProblem.asZeroOne_simple()
        
        simpleBAB = BranchAndBound_MODERN(simpleZeroOneProblem)
        simpleBAB.startSearch()

        simpleResult = simpleBAB.bestSolution

        self.assertEqual(simpleResult.Z, efficientResult.Z)
        self.assertEqual(simpleResult.U, efficientResult.U)
        # we cant check for items, since the two knapsacks have different items to represent the same problem
        #self.assertListEqual(simpleResult.items, efficientResult.items)

    # Get the random items in the expected, sorted order
    def _get_mock_items_sorted(self):
        firstProfit = 10
        firstWeight = 1
        firstBound = 6

        secondProfit = 15
        secondWeight = 3
        secondBound = 4

        thirdProfit = 11
        thirdWeight = 5
        thirdBound = 2

        firstGroup  = ItemGroup(firstProfit, firstWeight, firstBound)
        secondGroup = ItemGroup(secondProfit, secondWeight, secondBound)
        thirdGroup  = ItemGroup(thirdProfit, thirdWeight, thirdBound)

        items = [firstGroup, secondGroup, thirdGroup]

        return items
    
    # Returns the mock items in random order
    def _get_mock_items_random_order(self):
        items = self._get_mock_items_sorted()
        random.shuffle(items)
        return items

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