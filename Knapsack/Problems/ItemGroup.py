#from Knapsack.Problems.KnapsackItem import KnapsackItem
from functools import total_ordering

# Represents a bounded group in a bounded knapsack
# items: The items in this group
# upperBound: The highest number of items which can be selected
# lowerBound: The smallest number of items which can be selected
@total_ordering
class ItemGroup:
    def __init__(self, itemProfit:int, itemWeight: int, upperBound:int):
        self.itemProfit = itemProfit
        self.itemWeight = itemWeight
        self.upperBound = upperBound

    # Overwrite these methods to ensure sorting is correct
    # Sort such that p_1 / w_1 > p_2 / w_2 > p_3 / w_3...
    # Note that is should be sorted descendingly  
    def __lt__(self, obj):
        return ((self.itemProfit / self.itemWeight) > (obj.itemProfit / obj.itemWeight))
  
    def __gt__(self, obj):
        return ((self.itemProfit / self.itemWeight) < (obj.itemProfit / obj.itemWeight))
  
    def __le__(self, obj):
        return ((self.itemProfit / self.itemWeight) >= (obj.itemProfit / obj.itemWeight))
  
    def __ge__(self, obj):
        return ((self.itemProfit / self.itemWeight) <= (obj.itemProfit / obj.itemWeight))
  
    def __eq__(self, obj):
        return ((self.itemProfit / self.itemWeight) == (obj.itemProfit / obj.itemWeight))
  
    def __repr__(self):
        return str(f"""Knapsack Item Group; 
                    ItemProfit: {self.itemProfit}, 
                    ItemWeight: {self.itemWeight}, 
                    Ratio: {self.itemProfit / self.itemWeight}, 
                    UpperBound: {self.upperBound}, 
                    LowerBound: {self.lowerBound}""")