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
        self.undesiredShifts = TabuShiftPattern(self.combineDayShiftRequests(nurse.undesiredShifts[0], nurse.undesiredShifts[1]), nurse.undesiredShifts[2])
        self.completeWeekend = nurse.completeWeekend

    def combineDayShiftRequests(self, undesiredEarlyShifts, undesiredLateShifts):
        composite = [0] * 7
        for i in range(7):
            r1 = undesiredEarlyShifts[i]
            r2 = undesiredLateShifts[i]

            if r1 == 1 or r2 == 1:
                composite[i] == 1
        
        return composite

    def _assignShiftPattern(self, pattern):
        if pattern.day == [0] * 7:
            self.worksNight = True
        elif pattern.night == [0] * 7:
            self.worksNight = False
        self.shiftPattern = pattern
        self.penalty = self.calculatePenalty(pattern)

    # TODO: We need documentation for this function
    def calculatePenalty(self, shiftpattern):
        newPen = 0  # New penalty score
        # Calculating which schedule we should be looking at:
        if shiftpattern.day != [0] * 7:
            pattern = shiftpattern.day
            undesired = self.undesiredShifts.day
        else:
            pattern = shiftpattern.night
            undesired = self.undesiredShifts.night

        workList = []
        freeList = []
        work = 0
        free = 0
        # Computation over how many days the nurses work consecutively, and how many days they are free:
        count = 0
        for e in pattern:
            if e == 1:
                if free != 0:
                    freeList.append(free)
                    free = 0
                work += 1
            if e == 0:
                if work != 0:
                    workList.append(work)
                    work = 0
                free += 1
            if count == 6:
                if e == 0:
                    freeList.append(free)
                if e == 1:
                    workList.append(work)
            count += 1


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

        return newPen

    def __eq__(self, other):
        if not isinstance(other, TabuNurse):
            # don't attempt to compare against unrelated types
            return False

        return self.id == other.id and self.grade.value == other.grade.value

    def __str__(self):
        return f"TabuNurse - Id: {self.id}, Grade: {self.grade}, {self.shiftPattern}"
    
    def __repr__(self):
        return f"TabuNurse - Id: {self.id}, Grade: {self.grade}, {self.shiftPattern}"
