from Knapsack.Problems.KnapsackItem import KnapsackItem

class ZeroOneKnapsack:
    # xs: List of KnapsackItems
    # c: The capacity of the knapsack
    def __init__(self, items: list[KnapsackItem], C:int):
        self.items = items
        self.C = C
        self.N = len(items)
        
        # Make sure items are sorted
        self.items.sort()

