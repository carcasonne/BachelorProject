from Domain.Models.Enums.Grade import Grade
from Domain.Models.Tabu.TabuNurse import TabuNurse
from Domain.Models.Tabu.TabuShift import TabuShift
from Domain.Models.Tabu.TabuShiftType import TabuShiftType

class TabuSchedule:
    def __init__(self, Schedule):
        self.CC = None
        self.PC = None
        self.LB = None
        self.nurses = list(map(lambda n: TabuNurse(n), Schedule.nurses))
        self.shifts = []
        for x in range(len(Schedule.shifts)):
            if (x+1)%3 == 0:
                self.shifts.append(TabuShift(Schedule.shifts[x].coverRequirements, TabuShiftType.NIGHT, Schedule.shifts[x].shiftDay))
            elif (x+1)%3 == 2:
                totalGradeOne = Schedule.shifts[x].coverRequirements[Grade.ONE] + Schedule.shifts[x-1].coverRequirements[Grade.ONE]
                totalGradeTwo = Schedule.shifts[x].coverRequirements[Grade.TWO] + Schedule.shifts[x-1].coverRequirements[Grade.TWO]
                totalGradeThee = Schedule.shifts[x].coverRequirements[Grade.THREE] + Schedule.shifts[x-1].coverRequirements[Grade.THREE]

                requirements = {Grade.ONE:totalGradeOne, Grade.TWO:totalGradeTwo, Grade.THREE:totalGradeThee}
                self.shifts.append(TabuShift(requirements, TabuShiftType.DAY, Schedule.shifts[x].shiftDay))
        if len(self.shifts) != 14:
            raise Exception("Must be exactly 14 shifts")
        self.updateAll()

    def singleMove(self, nurse, newShiftPattern):
        oldShiftPattern = nurse.assignedShiftPattern.merged
        newMergedShiftPattern = newShiftPattern.merged
        print(oldShiftPattern)
        print(newMergedShiftPattern)
        for x in range(14):
            if oldShiftPattern[x] is not newMergedShiftPattern[x]:
                if oldShiftPattern[x] == 1:
                    self.shifts[x].removeNurse(nurse)
                else:
                    self.shifts[x].assignNurse(nurse)
        nurse.assignedShiftPattern = newShiftPattern
        self.updateAll()
        return self

    def checkMove(self, nurse, newShiftPattern):
        pass

    def calculateCC(self):
        CC = 0
        for shift in self.shifts:
            for grade in shift.coverRequirements:
                diff = shift.coverRequirements[grade] - len(shift.assignedNurses[grade.value - 1])
                if diff > 0:
                    CC += diff
        self.CC = CC

    def calculatePC(self):
        self.PC = -1

    def calculateLB(self):
        self.LB = -1

    def __str__(self):
        finalString = ""
        for shift in self.shifts:
            finalString += str(shift) + "\n"

        return finalString

    def update(self, CC, PC, LB):
        if CC: self.calculateCC()
        if PC: self.calculatePC()
        if LB: self.calculateLB()

    def updateAll(self):
        self.calculateCC()
        self.calculatePC()
        self.calculateLB()
