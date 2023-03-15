import math

class BranchAndBound:
    def __init__(self, items, c):
        self.items = items.copy()
        self.N = len(self.items)
        self.bestZ = 0
        self.currentZ = 0
        self.totalC = c
        self.currentC = self.totalC
        # S: critical item
        # SC: the sum weight of all items untill critical item
        tuple = self.findCriticalItemAndResidualCapacity()
        self.S = tuple[0]
        self.SC = tuple[1]
        self.U = self.optimalSolutionValue()
        # Set every item to be outside the knapsack
        for k in range(self.N):
            self.items[k].k = 0

    # As according to...
    # Returns index of critical item
    def findCriticalItemAndResidualCapacity(self):
        items = self.items.copy()
        sum = 0
        counter = 0
        for i in range(len(items)):
            item = items[i]
            if(sum + item.w <= self.totalC):
                sum += item.w
            else:
                return (i, sum)

        raise Exception("There is no critical item!")
    
    # As according to Marthello and Toth
    # Returns the optimal value which could be aquired by solving the problem
    def optimalSolutionValue(self):
        sumP = 0

        # Go through every item until just before critical item
        for i in range(self.S):
            sumP = self.items[i].p

        itemS = self.items[self.S]
        followingS = self.items[self.S + 1]
        precedingS = self.items[self.S - 1]
        followingRatio = followingS.p / followingS.w
        precedingRatio = precedingS.p / precedingS.w

        U_0 = sumP + math.floor((self.SC * followingRatio))
        U_1 = sumP + math.floor(itemS.p - (itemS.w - self.SC)*precedingRatio)

        return max(U_0, U_1)

    def searchTreeWithEarlyExit(self, lowerBound):
        pass

    def solve(self):
        pass
        
    def buildNewCurrentSolution(self):
        pass

    def saveCurrentSolution(self):
        pass

    def updateBestSolution(self):
        pass

    def replace_i_with_j(self):
        pass
