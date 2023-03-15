import unittest
import random

from Tests.test_knapsack.test_knapsackItem import TestKnapsackItemProperties
from Knapsack.BranchAndBound.BranchAndBound import BranchAndBound

class BoundAndBranchTest(unittest.TestCase):
    def test_finds_critical_item(self):
        instance = TestKnapsackItemProperties()
        items = instance._get_mock_items_sorted()

        c = 50
        expectedIndex = 3 # 4th item

        problem = BranchAndBound(items, c)
        actualIndex = problem.findCriticalItem()[0]

        self.assertEqual(expectedIndex, actualIndex)

if __name__ == '__main__':
    unittest.main()