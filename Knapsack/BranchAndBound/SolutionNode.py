class SolutionNode:
    # id: id of node
    # upperBound: the upper bound of solution represented by node
    # solutionValue: The total profit of solution represented by node
    # assignment: List of 0/1 of length N where assignment[i] is 0 if item is not in knapsack, 1 if it is
    def __init__(self):
        self.id = None
        self.upperBound = None
        self.solutionValue = None
        self.assignment = None
        self.profit = None
        self.weight = None
        self.r = None
        self.otherR = None

    def isNone(self):
        if (self.weight == None or self.profit == None or self.r == None):
            return True

        return False
