

class ZeroOneKnapsack:
    # N: Number of items to choose between
    # xs: List of items
    def __init__(self, N, xs):
        self.N = N
        self.xs = xs

        if  N != len(xs):
            raise ValueError("One or more lists has incorrect size")
        
        # Make sure items are sorted

