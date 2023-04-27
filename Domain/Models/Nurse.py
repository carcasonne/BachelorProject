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
        self.worksNight = None
        self.completeWeekend = contract.completeWeekend
        self.penalty = 0

    def assignShiftPattern(self, shiftPattern):  # A bit representation of ether (day, night) or (early, late, night)
        contractdays = 0
        contractnights = 0
        for x in range(7):
            counter = 0
            if shiftPattern.early[x] == 1:
                contractdays += 1
                counter += 1
            if shiftPattern.late[x] == 1:
                contractdays += 1
                counter += 1
            if shiftPattern.night[x] == 1:
                contractnights += 1
                counter += 1
            if counter > 1:
                raise Exception("Nurses can only be assigned to at most one shift per day")
        if contractnights > self.contract.nights or contractdays > self.contract.days or (contractdays > 0 and contractnights > 0):
            raise Exception("Shift pattern infeasible according to the contract")
        if shiftPattern.night != [0]*7:
            self.worksNight = True
        else:
            False
        self.assignedShiftPattern = shiftPattern
        self.penalty = self.calculatePenalty(shiftPattern)

    def print(self):
        print(str(self.id) + " is of grade: " + str(self.grade))

    def __eq__(self, other):
        if not isinstance(other, Nurse):
            # don't attempt to compare against unrelated types
            return False

        return (self.id == other.id and
                self.grade == other.grade)

    def calculatePenalty(self, shiftpattern):
        newPen = 0  # New penalty score
        # Calculating which schedule we should be looking at:
        if shiftpattern.night == [0] * 7:
            composite = [0] * 7
            for i in range(7):
                r1 = shiftpattern.late[i]
                r2 = shiftpattern.early[i]
                if r1 == 1 or r2 == 1:
                    composite[i] = 1
            pattern = composite
        else:
            pattern = shiftpattern.night

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
            if (shiftpattern.late or shiftpattern.early) != [0] * 7:
                if shiftpattern.late[x] == 1 and self.undesiredShifts[1][x] == 1:
                    newPen += 10
                elif shiftpattern.early[x] == 1 and self.undesiredShifts[0][x] == 1:
                    newPen += 10
            elif shiftpattern.night != [0] * 7:
                if shiftpattern.night[x] == 1 and self.undesiredShifts[2][x] == 1:
                    newPen += 10
        # Calculation of the penalty score of the nurse not working a complete weekend:
        if pattern[5] != pattern[6] and self.completeWeekend:
            newPen += 30

        return newPen