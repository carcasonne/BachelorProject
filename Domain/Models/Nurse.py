from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Grade import Grade


class Nurse:
    def __init__(self, id, grade:Grade, contract:Contract):
        self.id = id
        self.grade = grade
        self.contract = contract
        self.assignedShiftPattern = None

        # Soft constraints:
        self.consecutiveWorkingDays = (contract.minConsecutiveDays, contract.maxConsecutiveDays)
        self.consecutiveDaysOff = (contract.minConsecutiveDaysOff, contract.maxConsecutiveDaysOff)
        self.undesiredShifts = ([0] * 7, [0] * 7, [0] * 7)
        self.completeWeekend = contract.completeWeekend

    def assignShiftPattern(self, shiftPattern):  # A bit representation of ether (day, night) or (early, late, night)
        self.assignedShiftPattern = shiftPattern

    def print(self):
        print(str(self.id) + " is of grade: " + str(self.grade))

    def __eq__(self, other):
        if not isinstance(other, Nurse):
            # don't attempt to compare against unrelated types
            return False

        return (self.id == other.id and
                self.grade == other.grade)

    def calculatePenalty(self):
        newPen = 0  # New penalty score
        patterns = []
        undesiredShifts = []
        # Calculating which schedule we should be looking at:
        if self.assignedShiftPattern.night != [0] * 7:
            patterns.append(self.assignedShiftPattern.night)
            undesiredShifts.append(self.undesiredShifts[2])
        else:
            patterns.append(self.assignedShiftPattern.early)
            patterns.append(self.assignedShiftPattern.late)
            undesiredShifts.append(self.undesiredShifts[0])
            undesiredShifts.append(self.undesiredShifts[1])

        # Computation over how many days the nurses work consecutively, and how many days they are free:
        for i in range(len(patterns)):
            workList = []
            freeList = []
            work = 0
            free = 0
            pattern = patterns[i]
            undesired = undesiredShifts[i]
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
