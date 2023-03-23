from Domain.Models.Enums.Grade import Grade
from Domain.Models.Tabu.TabuNurse import TabuNurse
from Domain.Models.Tabu.TabuShift import TabuShift
from Domain.Models.Enums.ShiftType import TabuShiftType
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.StaticMethods import evaluatePC
from TabuSearch.StaticMethods import evaluateLB


class TabuSchedule:
    def __init__(self, Schedule):
        self.nurses = list(map(lambda n: TabuNurse(n), Schedule.nurses))
        self.shifts = []
        for x in range(len(Schedule.shifts)):
            if (x + 1) % 3 == 0:
                self.shifts.append(
                    TabuShift(Schedule.shifts[x].coverRequirements, TabuShiftType.NIGHT, Schedule.shifts[x].shiftDay))
            elif (x + 1) % 3 == 2:
                totalGradeOne = Schedule.shifts[x].coverRequirements[Grade.ONE] + \
                                Schedule.shifts[x - 1].coverRequirements[Grade.ONE]
                totalGradeTwo = Schedule.shifts[x].coverRequirements[Grade.TWO] + \
                                Schedule.shifts[x - 1].coverRequirements[Grade.TWO]
                totalGradeThee = Schedule.shifts[x].coverRequirements[Grade.THREE] + \
                                 Schedule.shifts[x - 1].coverRequirements[Grade.THREE]

                requirements = {Grade.ONE: totalGradeOne, Grade.TWO: totalGradeTwo, Grade.THREE: totalGradeThee}
                self.shifts.append(TabuShift(requirements, TabuShiftType.DAY, Schedule.shifts[x].shiftDay))
        if len(self.shifts) != 14:
            raise Exception("Must be exactly 14 shifts")
        self.CC = evaluateCC(self)
        self.PC = evaluatePC(self)
        self.LB = evaluateLB(self)

    # Checks if pattern covers shift - Returns: 1 or 0

    def __eq__(self, other):
        pass
