from Knapsack.Problems.KnapsackItem import KnapsackItem
from Knapsack.Problems.ItemGroup import ItemGroup
from Knapsack.Problems.ZeroOneKnapsack import ZeroOneKnapsack

class BoundedKnapsack:
    def __init__(self, itemGroups: list[ItemGroup], C):
        self.itemGroups = itemGroups
        self.C = C

    # Generates the 01 representation of this knapsack problem
    # Method taken from Martello and Toth...
    # This method minimizes the amount of variables in constructing the new knapsack
    def asZeroOne_efficient(self):
        newItems = []

        for i in range(len(self.itemGroups)):
            itemGroup = self.itemGroups[i]
            bound = 0
            k = 1
            while bound != itemGroup.upperBound:
                if bound + k > itemGroup.upperBound:
                    k = itemGroup.upperBound - bound

                profit = k * itemGroup.itemProfit
                weight = k * itemGroup.itemWeight

                newItem = KnapsackItem(profit, weight, i)
                newItems.append(newItem)

                bound = bound + k
                k = k * 2

        zeroOne = ZeroOneKnapsack(newItems, self.C)
        return zeroOne

    # Generates the 01 representation of this knapsack problem
    # "Stupid", it generates itemGroup_size * itemGroup_bound number of variables
    # Using this since it makes it possible to keep track of how many of each type is selected in the end
    def asZeroOne_simple(self):
        newItems = []

        for i in range(len(self.itemGroups)):
            itemGroup = self.itemGroups[i]
            profit = itemGroup.itemProfit
            weight = itemGroup.itemWeight

            for _ in range(itemGroup.upperBound):
                newItem = KnapsackItem(profit, weight, i)
                newItems.append(newItem)

        zeroOne = ZeroOneKnapsack(newItems, self.C)
        return zeroOne