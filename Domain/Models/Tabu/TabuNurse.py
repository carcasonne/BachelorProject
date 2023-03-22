from itertools import combinations
from Domain.Models.Nurse import Nurse
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern


class TabuNurse:
    def __init__(self, nurse):
        self.id = nurse.id
        self.contract = nurse.contract
        self.grade = nurse.grade
        self.shiftPattern = None
        self.worksNight = None

    def assignShiftPattern(self, pattern):
        if pattern.day == [0] * 7:
            self.worksNight = True
        elif pattern.night == [0] * 7:
            self.worksNight = False
        self.shiftPattern = pattern

    def __eq__(self, other):
        if not isinstance(other, TabuNurse):
            # don't attempt to compare against unrelated types
            return False

        return self.id == other.id and self.grade.value == other.grade.value
