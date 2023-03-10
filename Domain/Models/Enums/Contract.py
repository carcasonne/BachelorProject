class Contract():
    def __init__(self, days, nights):
        self.days = days
        self.nights = nights
    
    def __eq__(self, other): 
        if not isinstance(other, Contract):
            # don't attempt to compare against unrelated types
            return False

        return  (self.days == other.days and 
                 self.nights == other.nights)
