from functools import total_ordering

@total_ordering
class KnapsackItem():
    # p (int): profit
    # w (int): weight
    # j (bool): whether this item is in the knapsack 
    def __init__(self, p, w, k):
        self.p = p
        self.w = w
        self.k = k
    
    # Overwrite these methods to ensure sorting is correct
    # Sort such that p_1 / w_1 > p_2 / w_2 > p_3 / w_3...
    # Note that is should be sorted descendingly  
    def __lt__(self, obj):
        return ((self.p / self.w) > (obj.p / obj.w))
  
    def __gt__(self, obj):
        return ((self.p / self.w) < (obj.p / obj.w))
  
    def __le__(self, obj):
        return ((self.p / self.w) >= (obj.p / obj.w))
  
    def __ge__(self, obj):
        return ((self.p / self.w) <= (obj.p / obj.w))
  
    def __eq__(self, obj):
        return ((self.p / self.w) == (obj.p / obj.w))
  
    def __repr__(self):
        return str(f"P: {self.p}, W: {self.w}. Ratio: {self.p/self.w}")