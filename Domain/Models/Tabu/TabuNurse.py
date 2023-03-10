from itertools import combinations
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuShiftType import TabuShiftType


class TabuNurse:
    def __init__(self, nurse):
        self.id = nurse.id
        self.contract = nurse.contract
        self.grade = nurse.grade
        self.feasibleWorkPatterns = []
        self.assignedShiftPattern = TabuShiftPattern([0] * 7, [0] * 7)

        self.findWorkPatterns()

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
        counter = 0
        while counter <= 1:
            if counter == 0:
                combs = combinations(range(7), self.contract.days)
            else:
                combs = combinations(range(7), self.contract.nights)

            for comb in combs:
                bitstring = [0] * 7
                for i in comb:
                    bitstring[i] = 1
                if counter == 0:
                    self.feasibleWorkPatterns.append((bitstring, [0] * 7))
                else:
                    self.feasibleWorkPatterns.append(([0] * 7, bitstring))
            counter += 1

    def print(self):
        print("... To Be Continued ...")
        print(self.feasibleWorkPatterns)