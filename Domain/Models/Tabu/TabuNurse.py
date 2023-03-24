from itertools import combinations
from Domain.Models.Nurse import Nurse
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern


class TabuNurse:
    def __init__(self, nurse):
        self.id = nurse.id  # The identification number of the nurse
        self.contract = nurse.contract  # The contract this nurse has: How many days or nights can this nurse work
        self.grade = nurse.grade  # The grade of the nurse: 1= high grade, 2 = medium grade, 3 = low grade
        self.shiftPattern = TabuShiftPattern([0] * 7, [0] * 7)  # The shift pattern that this nurse is currently working
        self.worksNight = None  # True = Nurse works only night shifts, False = Nurse works only day shifts
        self.penalty = 0  # The penalty of the current shift pattern: from 0 (good pattern) to 10 (infeasible pattern)
                          # TODO: Change this description since 0 - 10 does not make a lot of sense anymore.

        # Soft constraints:
        self.consecutiveWorkingDays = nurse.consecutiveWorkingDays
        self.consecutiveDaysOff = nurse.consecutiveDaysOff
        self.undesiredShifts = nurse.undesiredShifts
        self.completeWeekend = nurse.completeWeekend
        self.undesiredWeekend = nurse.undesiredWeekend

    def _assignShiftPattern(self, pattern):
        if pattern.day == [0] * 7:
            self.worksNight = True
        elif pattern.night == [0] * 7:
            self.worksNight = False
        self.shiftPattern = pattern
        self.penalty = self.calculatePenalty(pattern)

    # TODO: Find out some constrains and calculate the penalty based on that. This should be a number from 1 to 10
    def calculatePenalty(self, shiftpattern):
        newPen = 0 # New penalty score
        # Calculating which schedule we should be looking at:
        if shiftpattern.day != [0] * 7:
            pattern = shiftpattern.day
            undesired = self.undesiredShifts[0]
        else:
            pattern = shiftpattern.night
            undesired = self.undesiredShifts[1]

        workList = []
        freeList = []
        work = 0
        free = 0
        # Computation over how many days the nurses work consecutively, and how many days they are free:
        for e in pattern:
            if e == 1:
                freeList.append(free)
                free = 0
                work += 1
            else:
                workList.append(work)
                work = 0
                free += 1
        # Calculation of penalty score for working more/less than the desired consecutive days:
        for e in workList:
            if e > self.consecutiveWorkingDays[1]:
                newPen += 30 * (e - self.consecutiveWorkingDays[1])
            elif e < self.consecutiveWorkingDays[0]:
                newPen += 30 * (self.consecutiveWorkingDays[0] - e)
        # Calculation of penalty score for having more/less days free than the desired amount:
        for e in freeList:
            if e > self.consecutiveDaysOff[1]:
                newPen += 30 * (e - self.consecutiveDaysOff[1])
            elif e < self.consecutiveDaysOff[0]:
                newPen += 30 * (self.consecutiveDaysOff[0] - e)
        # Calculation of the undesired days that the nurse does not want to work:
        for x in range(7):
            if pattern[x] == 1 and undesired[x] == 1:
                newPen += 10
        # Calculation of the penalty score of the nurse not working a complete weekend:
        if pattern[5] != pattern[6] and self.completeWeekend:
            newPen += 30
        # Calculation of the penalty score of a nurse working an undesired weekend:
        if (pattern[5] == 1 or pattern[6] == 1) and self.undesiredWeekend:
            newPen += 30

        return newPen

    def __eq__(self, other):
        if not isinstance(other, TabuNurse):
            # don't attempt to compare against unrelated types
            return False

        return self.id == other.id and self.grade.value == other.grade.value

    def __str__(self):
        return f"TabuNurse - Id: {self.id}, Grade: {self.grade}, {self.shiftPattern}"
