from Domain.Models.Enums.Grade import Grade
from Domain.Models.Tabu.TabuShift import TabuShift
from Domain.Models.Tabu.TabuShiftType import TabuShiftType


class TabuSchedule:
    def __init__(self, Schedule):
        self.nurses = Schedule.nurses
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

    def calculateCC(self):
        CC = 0
        for shift in self.shifts:
            for grade in shift.coverRequirements:
                CC += shift.coverRequirements[grade] - len(shift.assignedNurses[grade.value - 1])
        return max(0, CC)

    def calculatePC(self):
        pass

    def __str__(self):
        finalString = ""
        for shift in self.shifts:
            finalString += str(shift) + "\n"

        return finalString