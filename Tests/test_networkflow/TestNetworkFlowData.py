from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Nurse import Nurse
from Domain.Models.Schedule import Schedule
from Domain.Models.Shift import Shift
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuSchedule import TabuSchedule


class TestNetworkFlowData:
    def __init__(self):
        self.shifts = []
        for day in Days:
            self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.EARLY, day))
            self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.LATE, day))
            self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.NIGHT, day))

        self.nurses = []
        # Almost minimal amount of nurses:
        self.nurses.append(Nurse(0, Grade.ONE, Contract(5, 4)))
        self.nurses.append(Nurse(1, Grade.ONE, Contract(3, 2)))
        self.nurses.append(Nurse(2, Grade.ONE, Contract(4, 3)))
        self.nurses.append(Nurse(3, Grade.ONE, Contract(3, 3)))
        self.nurses.append(Nurse(4, Grade.TWO, Contract(5, 4)))
        self.nurses.append(Nurse(5, Grade.TWO, Contract(3, 2)))
        self.nurses.append(Nurse(6, Grade.TWO, Contract(4, 3)))
        self.nurses.append(Nurse(7, Grade.TWO, Contract(3, 3)))
        self.nurses.append(Nurse(8, Grade.THREE, Contract(5, 4)))
        self.nurses.append(Nurse(9, Grade.THREE, Contract(3, 2)))
        self.nurses.append(Nurse(10, Grade.THREE, Contract(4, 3)))
        self.nurses.append(Nurse(11, Grade.THREE, Contract(3, 3)))
        self.nurses.append(Nurse(12, Grade.ONE, Contract(4, 3)))
        self.nurses.append(Nurse(13, Grade.TWO, Contract(4, 3)))
        self.nurses.append(Nurse(14, Grade.THREE, Contract(4, 3)))
        self.nurses.append(Nurse(15, Grade.ONE, Contract(3, 3)))
        self.nurses.append(Nurse(16, Grade.TWO, Contract(3, 3)))
        self.nurses.append(Nurse(17, Grade.THREE, Contract(3, 3)))
        self.nurses.append(Nurse(18, Grade.THREE, Contract(3, 3)))
        self.nurses.append(Nurse(19, Grade.ONE, Contract(3, 3)))


        self.schedule = Schedule(self.shifts, self.nurses)
        nurses = self.schedule.nurses
        nurses[0].undesiredShifts = ([0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 1])
        nurses[1].undesiredShifts = ([0, 1, 1, 1, 1, 0, 0], [1, 0, 0, 1, 0, 1, 1], [1, 0, 1, 0, 0, 0, 1])
        nurses[2].undesiredShifts = ([0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        nurses[3].undesiredShifts = ([0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        nurses[4].undesiredShifts = ([0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0])
        nurses[5].undesiredShifts = ([0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1])
        nurses[6].undesiredShifts = ([0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        nurses[7].undesiredShifts = ([0, 0, 0, 0, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0], [1, 0, 0, 0, 0, 0, 1])
        nurses[8].undesiredShifts = ([1, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        nurses[9].undesiredShifts = ([1, 0, 1, 1, 0, 0, 0], [1, 1, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0])
        nurses[10].undesiredShifts = ([0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 1, 0, 1, 1], [0, 0, 0, 1, 0, 1, 1])
        nurses[11].undesiredShifts = ([0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        nurses[12].undesiredShifts = ([0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1])
        nurses[13].undesiredShifts = ([1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1])
        nurses[14].undesiredShifts = ([0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 1])
        nurses[15].undesiredShifts = ([0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 1])
        nurses[16].undesiredShifts = ([1, 0, 1, 1, 1, 0, 1], [1, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0])
        nurses[17].undesiredShifts = ([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 1, 1], [0, 0, 0, 0, 0, 1, 1])
        nurses[18].undesiredShifts = ( [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        nurses[19].undesiredShifts = ( [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1, 1])

        # TabuSchedule and assigning patterns that solves the issue:
        self.tabuSchedule = TabuSchedule(self.schedule)

        nurses = self.tabuSchedule.nurses
        nurses[0].completeWeekend = False
        nurses[0].consecutiveDaysOff = (2, 2)
        nurses[0].consecutiveWorkingDays = (2, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[0], TabuShiftPattern([1, 1, 1, 1, 1, 0, 0], [0] * 7))

        nurses[1].completeWeekend = True
        nurses[1].consecutiveDaysOff = (1, 2)
        nurses[1].consecutiveWorkingDays = (1, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[1], TabuShiftPattern([0] * 7, [0, 1, 0, 0, 1, 0, 0]))

        nurses[2].completeWeekend = True
        nurses[2].consecutiveDaysOff = (1, 2)
        nurses[2].consecutiveWorkingDays = (1, 2)
        self.tabuSchedule.assignPatternToNurse(nurses[2], TabuShiftPattern([1, 0, 1, 0, 0, 1, 1], [0] * 7))

        nurses[3].completeWeekend = False
        nurses[3].consecutiveDaysOff = (1, 2)
        nurses[3].consecutiveWorkingDays = (3, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[3], TabuShiftPattern([0] * 7, [0, 0, 1, 1, 1, 0, 0]))

        nurses[4].completeWeekend = True
        nurses[4].consecutiveDaysOff = (2, 2)
        nurses[4].consecutiveWorkingDays = (2, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[4], TabuShiftPattern([0, 0, 1, 1, 1, 1, 1], [0] * 7))

        nurses[5].completeWeekend = True
        nurses[5].consecutiveDaysOff = (2, 2)
        nurses[5].consecutiveWorkingDays = (1, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[5], TabuShiftPattern([1, 1, 0, 0, 1, 0, 0], [0] * 7))

        nurses[6].completeWeekend = False
        nurses[6].consecutiveDaysOff = (2, 2)
        nurses[6].consecutiveWorkingDays = (1, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[6], TabuShiftPattern([0, 1, 0, 1, 0, 1, 1], [0] * 7))

        nurses[7].completeWeekend = False
        nurses[7].consecutiveDaysOff = (1, 1)
        nurses[7].consecutiveWorkingDays = (1, 4)
        self.tabuSchedule.assignPatternToNurse(nurses[7], TabuShiftPattern( [0] * 7, [0, 1, 0, 1, 0, 1, 0]))

        nurses[8].completeWeekend = True
        nurses[8].consecutiveDaysOff = (1, 1)
        nurses[8].consecutiveWorkingDays = (2, 4)
        self.tabuSchedule.assignPatternToNurse(nurses[8], TabuShiftPattern([0, 1, 1, 1, 0, 1, 1], [0] * 7))

        nurses[9].completeWeekend = False
        nurses[9].consecutiveDaysOff = (1, 2)
        nurses[9].consecutiveWorkingDays = (1, 2)
        self.tabuSchedule.assignPatternToNurse(nurses[9], TabuShiftPattern([1, 0, 1, 0, 0, 1, 0], [0] * 7))

        nurses[10].completeWeekend = False
        nurses[10].consecutiveDaysOff = (2, 2)
        nurses[10].consecutiveWorkingDays = (1, 4)
        self.tabuSchedule.assignPatternToNurse(nurses[10], TabuShiftPattern([1, 1, 1, 0, 1, 0, 0], [0] * 7))

        nurses[11].completeWeekend = False
        nurses[11].consecutiveDaysOff = (1, 3)
        nurses[11].consecutiveWorkingDays = (1, 3)
        self.tabuSchedule.assignPatternToNurse(nurses[11], TabuShiftPattern([0] * 7, [1, 1, 0, 0, 0, 0, 1]))

        nurses[12].completeWeekend = True
        nurses[12].consecutiveDaysOff = (1, 2)
        nurses[12].consecutiveWorkingDays = (2, 3)
        self.tabuSchedule.assignPatternToNurse(nurses[12], TabuShiftPattern([1, 1, 0, 1, 1, 0, 0], [0] * 7))

        nurses[13].completeWeekend = True
        nurses[13].consecutiveDaysOff = (2, 2)
        nurses[13].consecutiveWorkingDays = (2, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[13], TabuShiftPattern([0] * 7, [1, 0, 0, 1, 1, 0, 0]))

        nurses[14].completeWeekend = False
        nurses[14].consecutiveDaysOff = (2, 2)
        nurses[14].consecutiveWorkingDays = (2, 4)
        self.tabuSchedule.assignPatternToNurse(nurses[14], TabuShiftPattern([0] * 7, [0, 0, 1, 1, 1, 0, 0]))

        nurses[15].completeWeekend = False
        nurses[15].consecutiveDaysOff = (2, 2)
        nurses[15].consecutiveWorkingDays = (1, 4)
        self.tabuSchedule.assignPatternToNurse(nurses[15], TabuShiftPattern([0] * 7, [1, 0, 0, 0, 0, 1, 1]))

        nurses[16].completeWeekend = False
        nurses[16].consecutiveDaysOff = (1, 2)
        nurses[16].consecutiveWorkingDays = (1, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[16], TabuShiftPattern([0] * 7, [0, 0, 1, 0, 0, 1, 1]))

        nurses[17].completeWeekend = True
        nurses[17].consecutiveDaysOff = (2, 3)
        nurses[17].consecutiveWorkingDays = (3, 3)
        self.tabuSchedule.assignPatternToNurse(nurses[17], TabuShiftPattern([0, 0, 1, 1, 1, 0, 0], [0] * 7))

        nurses[18].completeWeekend = True
        nurses[18].consecutiveDaysOff = (1, 3)
        nurses[18].consecutiveWorkingDays = (2, 5)
        self.tabuSchedule.assignPatternToNurse(nurses[18], TabuShiftPattern([0, 0, 0, 0, 1, 1, 1], [0] * 7))

        nurses[19].completeWeekend = False
        nurses[19].consecutiveDaysOff = (2, 2)
        nurses[19].consecutiveWorkingDays = (1, 2)
        self.tabuSchedule.assignPatternToNurse(nurses[19], TabuShiftPattern([0, 0, 1, 0, 0, 1, 1], [0] * 7))
