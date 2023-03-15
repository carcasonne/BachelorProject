from functools import total_ordering

@total_ordering
class KnapsackItem():
    # p: profit
    # w: weight
    def __init__(self, p, w):
        self.p = p
        self.w = w
    
    # Overwrite these methods to ensure sorting is correct
    # Sort such that p_1 / w_1 > p_2 / w_2 > p_3 / w_3...
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