import math

from Knapsack.BranchAndBound.SolutionNode import SolutionNode

class BranchAndBound:
    def __init__(self, zeroOneKnapsack):
        self.items = zeroOneKnapsack.items.copy()
        self.N = len(self.items)
        self.bestZ = 0
        self.currentZ = 0
        self.totalC = zeroOneKnapsack.c
        self.currentC = self.totalC
        # S: critical item
        # SC: the sum weight of all items untill critical item
        tuple = self.findCriticalItemAndResidualCapacity()
        self.S = tuple[0]
        self.SC = tuple[1]
        self.U = self.optimalSolutionValue()

        # Set every item to be outside the knapsack
        # List of 0/1 where inKnapsack[i] represent if items[i] is inside the knapsack
        self.bestSolution = [0] * len(self.items)

        self.nodes = [SolutionNode()] * len(self.items)
        self.nodes[0].weight = 0
        self.nodes[0].profit = 0
        self.nodes[0].r = 1 # maybe 0 if some index shit

        # I have no idea why we do this
        # M: List of M[i] corresponding value to items[i]
        # Should be moved to the knapsack class?
        self.M = [0] * len(self.items)
        min = float("inf")
        for i in range(len(self.items)-1, -1, -1):
            print("print")
            thisMin = self.items[i].weight
            if(thisMin < min):
                min = thisMin
            self.M[i] = min

        self.j = 0
        self.r = self.N

        # Possible refactor
        self.markedW = 0
        self.markedP = 0
        self.localR = 0
        self.currentSolution = self.bestSolution.copy()

    def searchTreeWithEarlyExit(self, lowerBound):
        pass

    def solve(self):
        pass

    def buildNewCurrentSolution(self):
        # As long as the weight of item j is bigger than capacity
        while(self.items[self.j].weight > self.currentC):
            possibleZ = math.floor(
                self.currentC *
                (self.items[self.j + 1].profit /
                 self.items[self.j + 1].weight)
            )
            if self.z >= possibleZ:
                return self.backTrack()
            else:
                self.j = self.j + 1

        r = None
        # This is a bit modified form source
        # Since we are loking through the i's in ascending order, we can just return the first we find, as it must be the smallest
        for i in range(0, self.N):
            node = self.nodes[i]
            if not node.isNone():
                weight = node.weight
                sum = 0
                for ii in range(node.r, ii):
                    sum += self.items[ii].weight
                if(weight + sum > self.currentC):
                    r = i
                    break
        if r == None:
            raise Exception("No 'r' value was found!")
        else:
            self.localR = r

        jNode = self.nodes[self.j]

        profitSum = 0
        weightSum = 0

        for i in range(jNode.r, r-1):
            profitSum += self.items[i].profit
            weightSum += self.items[i].weight

        #p = jNode.profit + profitSum
        #w = jNode.weight + weightSum
        self.markedP = jNode.profit + profitSum
        self.markedW = jNode.weight + weightSum

        # upper bound of this solution
        u = 0
        # Maybe N-1
        if self.localR <= self.N:
            u = self.calcUpperBound(weightSum, self.localR)

        # One of these two cases must always be met
        if self.bestZ >= self.currentZ + self.markedP + u:
            return self.backTrack()
        if u == 0:
            return self.updateBestSolution(p, r, self.bestSolution)

        return self.saveCurrentSolution()

    def saveCurrentSolution(self):
        self.currentC = self.currentC - self.markedW
        self.currentZ = self.currentZ + self.markedP

        # Maybe some weird python looping here...
        for k in range(self.j, self.localR - 1):
            self.currentSolution[k] = 1

        self.nodes[self.j].weight = self.markedW
        self.nodes[self.j].profit = self.markedP
        self.nodes[self.j].r = self.localR

        for k in range(self.j + 1, self.localR - 1):
            i = k - 1
            self.nodes[k].weight = self.nodes[i].weight - self.items[i].weight
            self.nodes[k].profit = self.nodes[i].profit - self.items[i].profit
            self.nodes[k].r = self.localR

        for k in range(self.localR, self.r):
            self.nodes[k].weight = 0
            self.nodes[k].profit = 0
            self.nodes[k].r = k

        self.r = self.localR - 1
        self.j = self.localR + 1

        if self.currentC >= self.M[self.j-1]:
            return self.buildNewCurrentSolution()

        if self.bestZ >= self.currentZ:
            return self.backTrack()

        self.markedP = 0

        return self.updateBestSolution()

    def updateBestSolution(self):
        # Update best solution
        self.bestZ = self.currentZ + self.markedP

        for k in range(1, self.j-1):
            self.bestSolution[k] = self.currentSolution[k]

        for k in range(self.j, self.localR):
            self.bestSolution[k] = 1

        for k in range(self.localR, self.N):
            self.bestSolution[k] = 0

        # If our solution value is equal to the optimal value, we have found an optimal assignment
        if self.z == self.U:
            return self.nodes[self.j]

        # Otherwise backtrack
        return self.backTrack()

    def backTrack(self):
        pass

    def replace_i_with_j(self):
        pass

    #As according to...
    # Returns tuple (index, residualCapacity)
    # index: Index of the critical item in self.items
    # residualCapacity: The remaining space in the knapsack after inserting every item before index.
    def findCriticalItemAndResidualCapacity(self):
        items = self.items.copy()
        sum = 0
        counter = 0
        for i in range(len(items)):
            item = items[i]
            if(sum + item.weight <= self.totalC):
                sum += item.weight
            else:
                residualCapacity = self.totalC - sum
                return (i, residualCapacity)

        raise Exception("There is no critical item!")

    # As according to Marthello and Toth
    # Returns the optimal value which could be aquired by solving the problem
    def optimalSolutionValue(self):
        sumP = 0
        # Go through every item until just before critical item
        for i in range(self.S):
            sumP += self.items[i].profit

        return self.calcUpperBound(sumP, self.S)

    def calcUpperBound(self, weightSum, r):
        itemR = self.items[r]
        followingR = self.items[r + 1]
        precedingR = self.items[r - 1]
        followingRatio = followingR.profit / followingR.weight
        precedingRatio = precedingR.profit / precedingR.weight

        U_0 = weightSum + math.floor((self.SC * followingRatio))
        U_1 = weightSum + math.floor(itemR.profit - (itemR.weight - self.SC) * precedingRatio)

        return max(U_0, U_1)

        pass