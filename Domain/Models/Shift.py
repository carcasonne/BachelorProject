from Domain.Models.Enums.Grade import Grade
class Shift:
    def __init__(self, coverRequirements, shiftType, shiftDay):
        self.coverRequirements = (0, 0, 0) # (Grade.ONE, Grade.TWO, Grade.THREE)
        self.assignedNurses = [set(), set(), set()]
        self.shiftDay = shiftDay
        self.shiftType = shiftType
    
    def __eq__(self, other): 
        if not isinstance(other, Shift):
            # don't attempt to compare against unrelated types
            return False

        return (self.shiftType == other.shiftType and
                self.shiftDay == other.shiftDay)
