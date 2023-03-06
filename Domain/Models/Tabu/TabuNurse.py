from Domain.Models.Enums import Contract
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern

class TabuNurse:
    def __init__(self, nurse):
        self.contract = nurse.contract
        self.grade = nurse.grade
        self.assignedShiftPattern = int('00000000000000', 2)

    def AssignShiftPattern(self, shiftPattern):  # A bit representation of ether (day, night) or (early, late, night)
        self.assignedShiftPattern = TabuShiftPattern(shiftPattern.day, shiftPattern.night)

    def ShiftIsCovered(self, shift): # 1 = shift pattern covers the shift, 0 = shift pattern does not cover the shift
        if shift.shiftType == ShiftType.DAY:
            self.assignedShiftPattern.day

    def Print(self):
        print(str(self.id) + " is of grade: " + str(self.grade))