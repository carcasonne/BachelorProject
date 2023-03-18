from functools import total_ordering

@total_ordering
class KnapsackItem:
    # p (int): profit
    # w (int): weight
    # j (bool): whether this item is in the knapsack 
    def __init__(self, p, w, itemType):
        self.profit = p
        self.weight = w
        self.itemType = itemType
    
    # Overwrite these methods to ensure sorting is correct
    # Sort such that p_1 / w_1 > p_2 / w_2 > p_3 / w_3...
    # Note that is should be sorted descendingly  
    def __lt__(self, obj):
        return ((self.profit / self.weight) > (obj.profit / obj.weight))
  
    def __gt__(self, obj):
        return ((self.profit / self.weight) < (obj.profit / obj.weight))
  
    def __le__(self, obj):
        return ((self.profit / self.weight) >= (obj.profit / obj.weight))
  
    def __ge__(self, obj):
        return ((self.profit / self.weight) <= (obj.profit / obj.weight))
  
    def __eq__(self, obj):
        return ((self.profit / self.weight) == (obj.profit / obj.weight))
  
    def __repr__(self):
        return str(f"KnapsackItem; P: {self.profit}, W: {self.weight}. Ratio: {self.profit / self.weight}")