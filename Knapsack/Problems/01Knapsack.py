

class ZeroOneKnapsack:
    # xs: List of KnapsackItems
    # c: The capacity of the knapsack
    def __init__(self, xs, c):
        self.xs = xs
        self.c = c
        self.N = len(xs)
        
        # Make sure items are sorted
        self.xs.sort()

