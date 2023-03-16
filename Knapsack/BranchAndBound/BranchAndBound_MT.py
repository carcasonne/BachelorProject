import math

from Knapsack.BranchAndBound.SolutionNode import SolutionNode
# Built according to the branch and bound algorithm for 0/1 knapsack problems as defined by Marthello and Toth
# DOESNT WORK :(
class BranchAndBound_MT:
    def __init__(self, zeroOneKnapsack):
        self.items = zeroOneKnapsack.items.copy()
        self.items.insert(0, None)
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

        # maybe make this into 3 separate lists instead..
        # Now it is a list of object SolutionNode, each node containing the 3 important fields
        self.nodes = []

        for i in range(len(self.items)):
            self.nodes.append(SolutionNode())

        self.nodes[1].weight = 0
        self.nodes[1].profit = 0
        self.nodes[1].r = 1 # maybe 0 if some index shit

        # I have no idea why we do this
        # M: List of M[i] corresponding value to items[i]
        # Should be moved to the knapsack class?
        self.M = [0] * len(self.items)
        min = float("inf")
        for i in range(len(self.items)-1, 0, -1):
            thisMin = self.items[i].weight
            if(thisMin < min):
                min = thisMin
            self.M[i] = min

        self.j = 1

        # Possible refactor
        self.markedW = 0
        self.markedP = 0
        self.localR = 0
        self.globalR = self.N
        self.currentSolution = self.bestSolution.copy()
        self.h = 0
        self.i = 0

    def searchTreeWithEarlyExit(self, lowerBound):
        pass

    def beginSearch(self):
        self.buildNewCurrentSolution()
        # try: 
        #     self.buildNewCurrentSolution()
        # except: 
        #     print("stopped :(")

    def buildNewCurrentSolution(self):
        print("building new solution")
        # As long as the weight of item j is bigger than capacity
        jWeight = self.items[self.j].weight
        while(jWeight > self.currentC):
            possibleZ = math.floor(
                self.currentC *
                (self.items[self.j + 1].profit /
                 self.items[self.j + 1].weight)
            )
            if self.bestZ >= possibleZ:
                return self.backTrack()
            else:
                self.j = self.j + 1

        display = self.currentSolution
        possibleRs = []
        jNode = self.nodes[self.j]
        for i in range(jNode.r, self.N+1):
            sum = 0
            for k in range(jNode.r, i):
                print(k)
                item = self.items[k]
                weight = item.weight
                sum += self.items[k].weight
            if(jNode.weight + sum > self.currentC):
                possibleRs.append(i)
                break
        if len(possibleRs) == 0:
            raise Exception("No 'r' value was found!")
        else:
            self.localR = min(possibleRs) 

        profitSum = 0
        weightSum = 0

        for k in range(jNode.r, self.localR-1):
            profitSum += self.items[k].profit
            weightSum += self.items[k].weight

        #p = jNode.profit + profitSum
        #w = jNode.weight + weightSum
        self.markedP = jNode.profit + profitSum
        self.markedW = jNode.weight + weightSum

        # upper bound of this solution
        u = 0
        # Maybe N-1
        if self.localR <= self.N:
            u = self.calcUpperBound(weightSum, self.localR)

        if self.bestZ >= self.currentZ + self.markedP + u:
            return self.backTrack()
        if u == 0:
            return self.updateBestSolution()

        return self.saveCurrentSolution()

    def saveCurrentSolution(self):
        print("saving best solution")
        self.currentC = self.currentC - self.markedW
        self.currentZ = self.currentZ + self.markedP

        display = self.currentSolution

        # TODO: looping?
        for k in range(self.j, self.localR - 1):
            self.currentSolution[k] = 1

        self.nodes[self.j].weight = self.markedW
        self.nodes[self.j].profit = self.markedP
        self.nodes[self.j].r = self.localR

        # TODO: looping? MAYBE HERE R
        for k in range(self.j + 1, self.localR - 1):
            i = k - 1
            self.nodes[k].weight = self.nodes[i].weight - self.items[i].weight
            self.nodes[k].profit = self.nodes[i].profit - self.items[i].profit
            self.nodes[k].r = self.localR

        # TODO: looping?
        for k in range(self.localR, self.globalR):
            self.nodes[k].weight = 0
            self.nodes[k].profit = 0
            self.nodes[k].r = k

        self.globalR = self.localR - 1
        self.j = self.localR + 1

        print("goddag")

        if self.currentC >= self.M[self.j - 1]:
            return self.buildNewCurrentSolution()

        if self.bestZ >= self.currentZ:
            return self.backTrack()

        self.markedP = 0

        return self.updateBestSolution()

    def updateBestSolution(self):
        print("updating best solution")
        # Update best solution
        self.bestZ = self.currentZ + self.markedP
        display = self.currentSolution
        display2 = self.bestSolution

        print("updating from:")
        print(self.bestSolution)
        print("to:")
        print(self.currentSolution)
        

        # TODO: looping?
        # Update evreything up to j to be as current solution
        for k in range(0, self.j - 1):
            self.bestSolution[k] = self.currentSolution[k]
        # Insert every item between j and r
        for k in range(self.j, self.localR - 1):
            self.bestSolution[k] = 1
        # Remove every item after
        for k in range(self.localR, self.N):
            self.bestSolution[k] = 0

        # If our solution value is equal to the optimal value, we have found an optimal assignment
        if self.bestZ == self.U:
            return

        # Otherwise backtrack
        return self.backTrack()

    def backTrack(self):
        print("backtracking")
        # Find latest item inserted into the knapsack
        i = None

        display = self.currentSolution

        for k in range(0, self.N):
            if k < self.j:
                if self.currentSolution[k] == 1:
                    i = k
        # If no items have been inserted in knapsack return
        # Throw exception?
        if i is None:
            print(str(i) + ": is none")
            return

        self.i = i
        iNode = self.items[self.i]

        # remove this item from knapsack
        self.currentC = self.currentC + iNode.weight
        self.currentZ = self.currentZ - iNode.profit
        self.currentSolution[i] = 0
        self.j = self.i + 1 # go to next item

        if self.currentC - iNode.weight >= self.M[self.i]:
            return self.buildNewCurrentSolution()

        self.j = self.i
        self.h = self.i

        return self.try_to_replace_i_with_j()

    # If just python used curly brackets for scopes....
    def try_to_replace_i_with_j(self):
        print("trying to replace i with j")
        self.h = self.h + 1
        hItem = self.items[self.h]
        iItem = self.items[self.i]

        hZ = math.floor(
            self.currentC *
            (hItem.profit / hItem.weight)
        )

        # why?
        if self.bestZ >= self.currentZ + hZ:
            print("backtracking 1")
            return self.backTrack()
        # why?
        if hItem.weight == iItem.weight:
            print("retrying to add")
            return self.try_to_replace_i_with_j()
        # why?
        if hItem.weight > iItem.weight:
            print("hItem weight greater")
            # why?
            if(hItem.weight > self.currentC or self.bestZ >= self.currentZ + hItem.profit):
                return self.try_to_replace_i_with_j()

            self.bestZ = self.currentZ + hItem.profit
            for k in range(0, self.N):
                self.bestSolution[k] = self.currentSolution[k]

            self.bestSolution[self.h] = 1

            if self.bestZ == self.U:
                return

            self.i = self.h

            return self.try_to_replace_i_with_j()
        else:
            print("hItem weight lesser")
            # why?
            if self.currentC - hItem.weight < self.M[self.h]:
                return self.try_to_replace_i_with_j()

            self.currentC = self.currentC - hItem.weight
            self.currentZ = self.currentZ + hItem.profit

            self.currentSolution[self.h] = 1
            self.j = self.h + 1

            hNode = self.nodes[self.h]
            hNode.weight = hItem.weight
            hNode.profit = hItem.profit
            hNode.r = self.h + 1

            # Maybe self.h instead og self.h + 1
            for k in range(self.h + 1, self.globalR):
                node = self.nodes[k]
                node.weight = 0
                node.profit = 0
                node.r = k

            self.globalR = self.h
            return self.buildNewCurrentSolution()

    #As according to...
    # Returns tuple (index, residualCapacity)
    # index: Index of the critical item in self.items
    # residualCapacity: The remaining space in the knapsack after inserting every item before index.
    def findCriticalItemAndResidualCapacity(self):
        items = self.items.copy()
        sum = 0
        counter = 0
        for i in range(1, len(items)):
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
        for i in range(1, self.S):
            sumP += self.items[i].profit

        return self.calcUpperBound(sumP, self.S)

    def calcUpperBound(self, weightSum, r):
        U_0 = 0
        U_1 = 0

        if(len(self.items) < r):
            followingRatio = followingR.profit / followingR.weight
            followingR = self.items[r + 1]
            U_0 = weightSum + math.floor((self.SC * followingRatio))
              
        if(len(self.items) == r):
            r = r -1

        itemR = self.items[r]
        precedingR = self.items[r - 1]
        precedingRatio = precedingR.profit / precedingR.weight
        U_1 = weightSum + math.floor(itemR.profit - (itemR.weight - self.SC) * precedingRatio)

        return max(U_0, U_1)

        pass