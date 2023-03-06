from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Shift import Shift


class TabuSchedule:
    def __init__(self, Schedule):
        self.nurses = Schedule.nurses
        self.shifts = []
        for x in range(len(Schedule.shifts)):
            if (x+1)%3 == 0:
                self.shifts.append(Shift(Schedule.shifts[x].coverRequirements, ShiftType.NIGHT, True))
            elif (x+1)%3 == 2:
                totalGradeOne = Schedule.shifts[x].coverRequirements[Grade.ONE] + Schedule.shifts[x-1].coverRequirements[Grade.ONE]
                totalGradeTwo = Schedule.shifts[x].coverRequirements[Grade.TWO] + Schedule.shifts[x-1].coverRequirements[Grade.TWO]
                totalGradeThee = Schedule.shifts[x].coverRequirements[Grade.THREE] + Schedule.shifts[x-1].coverRequirements[Grade.THREE]

                requirements = {Grade.ONE:totalGradeOne, Grade.TWO:totalGradeTwo, Grade.THREE:totalGradeThee}
                self.shifts.append(Shift(requirements, ShiftType.DAY, False))
        if len(self.shifts) != 14:
            raise Exception("Must be exactly 14 shifts")

    def CalculateCC(self):
        pass

    def CalculatePC(self):
        pass

    def __str__(self):
        finalString = ""
        for shift in self.shifts:
            finalString = str(shift) + "\n"