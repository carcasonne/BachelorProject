import math

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
    def __init__(self, items, C):
        self.items = items
        self.C = C
        self.N = len(self.items)
        self.PQ = Priority_Queue()

        self.v = Node(-1, 0, 0)
        self.v.U = BranchAndBound_MODERN.get_bound(self.v, self.items, self.C, self.N)
        self.nodeCount = 1
        self.PQ.insert(self.v, self.items, self.C, self.N)

        self.bestSolution = self.v

    def startSearch(self):
        while self.PQ.length != 0:
            v = self.PQ.remove()

            # Ignore node if upper bound falls too low
            # Branches by making 2 solutions: 1 where we insert the item, 1 where we do not
            if v.U > self.bestSolution.Z: 
                # Make new node in tree
                newLevel = v.level + 1
                item = self.items[newLevel]
                prevSolutionZ = v.Z + item.profit
                prevSolutionC = v.usedC + item.weight

                includeItemSolution = Node(newLevel, prevSolutionZ, prevSolutionC)
                self.nodeCount += 1

                # Add all items in current solution, then add the new item
                includeItemSolution.items = v.items.copy()
                includeItemSolution.items.append(item)


                # Update best known solution if solution weight fits, and solution value is better
                if  (includeItemSolution.usedC <= self.C and 
                    includeItemSolution.Z > self.bestSolution.Z): 
                    self.bestSolution = includeItemSolution

                includeItemSolution.U = BranchAndBound_MODERN.get_bound(includeItemSolution, self.items, self.C, self.N)
                
                # If the new solution could potentiall be better, add it to PQ
                if includeItemSolution.U > self.bestSolution.Z:
                    self.PQ.insert(includeItemSolution, self.items, self.C, self.N)

                # Generate another solution corresponding to not inserting the item
                excludeItemSolution = Node(newLevel, v.Z, v.usedC)
                self.nodeCount += 1

                excludeItemSolution.items = v.items.copy()
                excludeItemSolution.U = BranchAndBound_MODERN.get_bound(excludeItemSolution, self.items, self.C, self.N)

                # If solution value is greater than upper bound, even without adding the item, then add to PQ
                if excludeItemSolution.U > self.bestSolution.Z:
                    self.PQ.insert(excludeItemSolution, self.items, self.C, self.N)



    def get_bound(node, items, totalC, N):
        if node.usedC >= totalC:
            return 0
        else:
            sumZ = node.Z
            sumC = node.usedC
            # The critical item, s
            s = None

            for i in range(node.level + 1, N):
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

class Priority_Queue:
    def __init__(self):
        self.pqueue = []
        self.length = 0
    
    def insert(self, node, items, totalC, N):
        j = 0
        for i in range(len(self.pqueue)):
            if self.pqueue[i].U > node.U:
                j = i
                break

        self.pqueue.insert(j, node)
        self.length += 1

                    
    def remove(self):
        try:
            result = self.pqueue.pop()
            self.length -= 1
        except: 
            raise Exception("Priority queue cannot be popped when its empty")
        else:
            return result