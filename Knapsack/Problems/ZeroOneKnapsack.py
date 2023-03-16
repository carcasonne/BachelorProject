

class ZeroOneKnapsack:
    # xs: List of KnapsackItems
    # c: The capacity of the knapsack
    def __init__(self, items, c):
        self.items = items
        self.c = c
        self.N = len(items)
        
        # Make sure items are sorted
        self.items.sort()

