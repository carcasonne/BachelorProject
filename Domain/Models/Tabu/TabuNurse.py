import itertools
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuShiftType import TabuShiftType


class TabuNurse:
    def __init__(self, nurse):
        self.contract = nurse.contract
        self.grade = nurse.grade
        self.assignedShiftPattern = TabuShiftPattern(int('0000000', 2), int('0000000', 2))

    def AssignShiftPattern(self, shiftPattern):  # A bit representation of ether (day, night) or (early, late, night)
        self.assignedShiftPattern = TabuShiftPattern(shiftPattern.day, shiftPattern.night)

    def ShiftIsCovered(self, shift): # 1 = shift pattern covers the shift, 0 = shift pattern does not cover the shift
        if shift.shiftType == TabuShiftType.DAY:
            DayOrNightPattern = self.assignedShiftPattern.day
        else:
            DayOrNightPattern = self.assignedShiftPattern.night

        return bool(DayOrNightPattern & shift.ToBit())

    def Print(self):
        print("... To Be Continued ...")