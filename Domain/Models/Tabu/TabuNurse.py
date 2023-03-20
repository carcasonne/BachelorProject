from itertools import combinations
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuShiftType import TabuShiftType

class TabuNurse:
    def __init__(self, nurse):
        self.id = nurse.id
        self.contract = nurse.contract
        self.grade = nurse.grade
        self.feasibleShiftPatterns = []
        self.assignedShiftPattern = TabuShiftPattern([0] * 7, [0] * 7)
