from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Nurse import Nurse
from Domain.Models.Schedule import Schedule
from Domain.Models.Shift import Shift
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuSchedule import TabuSchedule


class TestNetworkFlowData_Simple:
    def __init__(self):
        self.shifts = []
        for day in Days:
            if day == Days.MONDAY:
                self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.EARLY, day))
                self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 1}, ShiftType.LATE, day))
                self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.NIGHT, day))
            elif day == Days.TUESDAY:
                self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.EARLY, day))
                self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.LATE, day))
                self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.NIGHT, day))
            else:
                self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.EARLY, day))
                self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.LATE, day))
                self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.NIGHT, day))

        self.nurses = []
        # Almost minimal amount of nurses:
        self.nurses.append(Nurse(0, Grade.ONE, Contract(5, 4)))
        self.nurses.append(Nurse(1, Grade.ONE, Contract(3, 2)))

        self.schedule = Schedule(self.shifts, self.nurses)
        nurses = self.schedule.nurses
        nurses[0].undesiredShifts = ([0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        nurses[1].undesiredShifts = ([1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])

        # TabuSchedule and assigning patterns that solves the issue:
        self.tabuSchedule = TabuSchedule(self.schedule)

        nurses = self.tabuSchedule.nurses
        nurses[0].completeWeekend = False
        nurses[0].consecutiveDaysOff = (2, 2)
        nurses[0].consecutiveWorkingDays = (2, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[0], TabuShiftPattern([1, 1, 0, 0, 0, 0, 0], [0] * 7))

        nurses[1].completeWeekend = False
        nurses[1].consecutiveDaysOff = (1, 2)
        nurses[1].consecutiveWorkingDays = (1, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[1], TabuShiftPattern([1, 1, 0, 0, 0, 0, 0], [0] * 7))
