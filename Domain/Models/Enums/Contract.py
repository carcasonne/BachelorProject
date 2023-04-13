class Contract():
    def __init__(self, days, nights):
        self.days = days
        self.nights = nights
        self.minConsecutiveDays = 0
        self.maxConsecutiveDays = 7
        self.minConsecutiveDaysOff = 0
        self.maxConsecutiveDaysOff = 7
        self.completeWeekend = False
    
    def __eq__(self, other): 
        if not isinstance(other, Contract):
            # don't attempt to compare against unrelated types
            return False

        return (self.days == other.days and self.nights == other.nights)

    def __ne__(self, other):
        return not(self == other)

    def __hash__(self):
        return hash(f"{self.days}, {self.nights}")
    
    def __str__(self):
        return f"Contract: {self.days} days, {self.nights} nights"
    
    def __repr__(self):
        return f"Contract: {self.days} days, {self.nights} nights"

