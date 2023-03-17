import unittest
import random

from Knapsack.Problems.KnapsackItem import KnapsackItem

class TestKnapsackItemProperties(unittest.TestCase):
    def test_items_sorted_correctly(self):
        random = self._get_mock_items_random_order()
        sorted = self._get_mock_items_sorted()

        random.sort()
         
        for i in range(len(random)):
            expected = sorted[i]
            actual = random[i]
            self.assertEqual(expected, actual)
  
    # Get the random items in the expected, sorted order
    def _get_mock_items_sorted(self):
        # Ratios 6, 6, 5, 4, 3, 1.11112...
        profits = [100, 60, 60, 100, 120, 60, 10, 1, 1, 2, 100]
        weights = [12,  10, 10, 20,  30,  20, 9,  1, 1, 3, 150]

        items = []

        for i in range(len(profits)):
            p = profits[i]
            w = weights[i]
            item = KnapsackItem(p, w, 0)
            items.append(item)
        
        return items
    
    # Returns the mock items in random order
    def _get_mock_items_random_order(self):
        items = self._get_mock_items_sorted()
        random.shuffle(items)
        return items

if __name__ == '__main__':
    unittest.main()