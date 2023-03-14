from Domain.Models.Enums import Contract

class Nurse:
    def __init__(self, id, grade, contract):
        self.id = id
        self.grade = grade
        self.contract = contract
        self.assignedShiftPattern = None

    def assignShiftPattern(self, shiftPattern): # A bit representation of ether (day, night) or (early, late, night)
        self.assignedShiftPattern = shiftPattern

    def print(self):
        print(str(self.id) + " is of grade: " + str(self.grade))

    def __eq__(self, other): 
        if not isinstance(other, Nurse):
            # don't attempt to compare against unrelated types
            return False

        return  (self.id == other.id and 
                 self.grade == other.grade)
