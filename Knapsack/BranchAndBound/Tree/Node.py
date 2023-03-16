
class Node:
    def __init__(self, level, index, profit, bound, weight):
        self.level = level
        self.index = index
        self.profit = profit
        self.bound = bound
        self.weight = weight

    # Returns the variable corresponding to a node
    def f(self):
        pass
    
    # The sequence of values assigned to variables from x_r to x_f(k)
    # Maybe should just be a field
    def path(self):
        pass

    # Should only be called on a leaf
    # Calculates the upper bound of the problem represented by this node
    def calcUpperBound(self):
        pass