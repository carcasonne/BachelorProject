from Knapsack.Problems.ZeroOneKnapsack import ZeroOneKnapsack
import queue

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

class Node:
    # level: level of node (id)
    # Z: the total value of this solution
    # usedC: the total weight of this solution
    # items: The items in the solution. Items not in this list are not in the knapsack
    # U: upper bound of this solution 
    def __init__(self, level, Z, usedC):
        self.level = level
        self.Z = Z
        self.usedC = usedC
        self.items = []
        self.U = None # Will be set later

class BranchAndBound_MODERN:
    # items: All possible items which can be in the knapsacl
    # C: Total capacity of the knapsack
    # N: Number of items
    # PQ: The priority queue used for expanding new nodes
    # v: The node currently being looked at (dummy node at init)
    # nodeCount: Amount of nodes generated (possible solutions generated)
    # bestSolution: The best solution found so far
    def __init__(self, zeroOneKnapsack: ZeroOneKnapsack, targetValue=None):
        self.items = zeroOneKnapsack.items
        self.C = zeroOneKnapsack.C
        self.N = len(self.items)

        self.v = Node(-1, 0, 0)
        self.v.U = BranchAndBound_MODERN.get_bound(self.v, self.items, self.C, self.N)
        self.nodeCount = 1

        self.bestSolution = self.v
        self.targetValue = targetValue

        self.queue = queue.PriorityQueue()
        self.queue.put(PrioritizedItem(0, self.v))

    def resetSearch(self):
        self.v = Node(-1, 0, 0)
        self.v.U = BranchAndBound_MODERN.get_bound(self.v, self.items, self.C, self.N)
        self.nodeCount = 1
        self.bestSolution = self.v
    
    # targetValue: if not None, any solution must havr Z value greater than targetValue
    # earlyExit: Whether the solution should exit at first found, feasible solution (bound to targetValue)
    def startSearch(self, earlyExit=False):
        while self.queue.qsize() != 0:
            pi = self.queue.get()
            v = pi.item
            
            # Ignore node if upper bound falls too low
            # Branches by making 2 solutions: 1 where we insert the item, 1 where we do not
            if v.U > self.bestSolution.Z: 
                # Make new node in tree
                newLevel = v.level + 1

                # means we have run through all items without finding a feasible solution
                if newLevel >= len(self.items):
                    return

                item = self.items[newLevel]

                newSolutionZ = v.Z + item.profit
                newSolutionC = v.usedC + item.weight

                includeItemSolution = Node(newLevel, newSolutionZ, newSolutionC)
                self.nodeCount += 1

                # Add all items in current solution, then add the new item
                includeItemSolution.items = v.items.copy()
                includeItemSolution.items.append(item)

                includeItemSolution.U = BranchAndBound_MODERN.get_bound(includeItemSolution, self.items, self.C, self.N)

                exit = False

                # Update best known solution if solution weight fits, and solution value is better
                if  includeItemSolution.usedC <= self.C:
                    # If a lower bound is given, we must take into consideration
                    # whether to update the solution or just stop now
                    if self.targetValue is not None:
                        if includeItemSolution.Z >= self.targetValue:
                            if includeItemSolution.Z > self.bestSolution.Z:
                                self.bestSolution = includeItemSolution
                                exit = earlyExit
                    elif includeItemSolution.Z > self.bestSolution.Z:
                        self.bestSolution = includeItemSolution

                # If the new solution could potentiall be better, add it to PQ
                if includeItemSolution.U > self.bestSolution.Z:
                    self.queue.put(PrioritizedItem(-includeItemSolution.U, includeItemSolution))

                # Generate another solution corresponding to not inserting the item
                excludeItemSolution = Node(newLevel, v.Z, v.usedC)
                self.nodeCount += 1

                excludeItemSolution.items = v.items.copy()
                excludeItemSolution.U = BranchAndBound_MODERN.get_bound(excludeItemSolution, self.items, self.C, self.N)

                # If potential to be better than best solution, even without adding the item, then add to PQ
                if excludeItemSolution.U > self.bestSolution.Z:
                    self.queue.put(PrioritizedItem(-excludeItemSolution.U, excludeItemSolution))
                
                if exit: 
                    return

    def get_bound(node, items, totalC, N):
        if node.usedC >= totalC:
            return 0
        else:
            sumZ = node.Z
            sumC = node.usedC
            # The critical item, s
            s = node.level + 1

            for i in range(s, N):
                item = items[i]
                # If the knapsack can fit the item
                if totalC >= sumC + item.weight:
                    sumC = sumC + item.weight
                    sumZ = sumZ + item.profit
                    # continously update the critical item to be the one just before no more space is available
                    s = i 
            
            if s < N:
                ratio = items[s].profit / items[s].weight
                sumZ = sumZ + (totalC - sumC) * ratio

            return sumZ