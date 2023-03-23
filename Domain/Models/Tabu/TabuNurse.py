from itertools import combinations
from Domain.Models.Nurse import Nurse
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern


class TabuNurse:
    def __init__(self, nurse):
        self.id = nurse.id  # The identification number of the nurse
        self.contract = nurse.contract  # The contract this nurse has: How many days or nights can this nurse work
        self.grade = nurse.grade  # The grade of the nurse: 1= high grade, 2 = medium grade, 3 = low grade
        self.shiftPattern = TabuShiftPattern([0]*7, [0]*7)  # The shift pattern that this nurse is currently working
        self.worksNight = None  # True = Nurse works only night shifts, False = Nurse works only day shifts
        self.penalty = None  # The penalty of the current shift pattern: from 0 (good pattern) to 10 (infeasible pattern)

    def assignShiftPattern(self, pattern):
        if pattern.day == [0] * 7:
            self.worksNight = True
        elif pattern.night == [0] * 7:
            self.worksNight = False
        self.shiftPattern = pattern
        self.calculatePenalty()

    # TODO: Find out some constrains and calculate the penalty based on that. This should be a number from 1 to 10
    def calculatePenalty(self):
        self.penalty = 0

    def __eq__(self, other):
        if not isinstance(other, TabuNurse):
            # don't attempt to compare against unrelated types
            return False

        return self.id == other.id and self.grade.value == other.grade.value
    
    def __str__(self):
        return f"Tabu Nurse, id: {self.id}"
