import itertools
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuShiftType import TabuShiftType


class TabuNurse:
    def __init__(self, nurse):
        self.id = nurse.id
        self.contract = nurse.contract
        self.grade = nurse.grade
        self.feasibleWorkPatterns = []
        self.assignedShiftPattern = TabuShiftPattern(int('0000000', 2), int('0000000', 2))

    def assignShiftPattern(self, shiftPattern):  # A bit representation of ether (day, night) or (early, late, night)
        self.assignedShiftPattern = TabuShiftPattern(shiftPattern.day, shiftPattern.night)

    def shiftIsCovered(self, shift): # 1 = shift pattern covers the shift, 0 = shift pattern does not cover the shift
        if shift.shiftType == TabuShiftType.DAY:
            DayOrNightPattern = self.assignedShiftPattern.day
        else:
            DayOrNightPattern = self.assignedShiftPattern.night
        return bool(DayOrNightPattern & shift.ToBit())

    def penalty(self):
        pass

    def findWorkPatterns(self):
        pass

    def print(self):
        print("... To Be Continued ...")