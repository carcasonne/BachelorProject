from Domain.Models.Enums import Contract

class Nurse:
    def __init__(self, grade, contract):
        self.id = id
        self.contract = contract
        self.grade = grade
        self.assignedShiftPattern = None

    def AssignShiftPattern(self, shiftPattern): # A bit representation of ether (day-night) or (early, late, night)
        self.assignedShiftPattern = shiftPattern

    def print(self):
        print(str(self.id) + " is of grade: " + str(self.grade))