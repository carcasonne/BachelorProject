from itertools import combinations
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuShiftType import TabuShiftType


class TabuNurse:
    def __init__(self, nurse):
        self.id = nurse.id
        self.contract = nurse.contract
        self.grade = nurse.grade
        self.PC = 0
        self.feasibleShiftPatterns = []
        self.assignedShiftPattern = TabuShiftPattern([0] * 7, [0] * 7)

        self.findShiftPatterns()

    def assignShiftPattern(self, shiftPattern):  # A bit representation of ether (day, night) or (early, late, night)
        if len(shiftPattern) != 14:
            raise Exception("Shift pattern format is invalid")
        self.assignedShiftPattern = TabuShiftPattern(shiftPattern[0], shiftPattern[1])

    def shiftIsCovered(self, shift): # 1 = shift pattern covers the shift, 0 = shift pattern does not cover the shift
        pass

    def calcPC(self, fromMove, toMove):
        return self.PC

    def findShiftPatterns(self):
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
                    self.feasibleShiftPatterns.append((bitstring, [0] * 7))
                else:
                    self.feasibleShiftPatterns.append(([0] * 7, bitstring))
            counter += 1

    def print(self):
        print("... To Be Continued ...")
        print(self.feasibleShiftPatterns)