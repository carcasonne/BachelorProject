from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Nurse import Nurse
from Domain.Models.Schedule import Schedule
from Domain.Models.Shift import Shift
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuSchedule import TabuSchedule


class NurseChainTestData:
    def __init__(self):
        self.shifts = []
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.EARLY, Days.MONDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.LATE, Days.MONDAY))
        self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.NIGHT, Days.MONDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.EARLY, Days.TUESDAY))
        self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.LATE, Days.TUESDAY))
        self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.NIGHT, Days.TUESDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.EARLY, Days.WEDNESDAY))
        self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.LATE, Days.WEDNESDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.NIGHT, Days.WEDNESDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.EARLY, Days.THURSDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.LATE, Days.THURSDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.NIGHT, Days.THURSDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.EARLY, Days.FRIDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.LATE, Days.FRIDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.NIGHT, Days.FRIDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.EARLY, Days.SATURDAY))
        self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.LATE, Days.SATURDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.NIGHT, Days.SATURDAY))
        self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.EARLY, Days.SUNDAY))
        self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.LATE, Days.SUNDAY))
        self.shifts.append(Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 0}, ShiftType.NIGHT, Days.SUNDAY))

        self.nurses = []
        # Almost minimal amount of nurses:
        self.nurses.append(Nurse(0, Grade.ONE, Contract(5, 4)))
        self.nurses.append(Nurse(1, Grade.ONE, Contract(5, 4)))
        self.nurses.append(Nurse(2, Grade.ONE, Contract(5, 4)))

        self.schedule = Schedule(self.shifts, self.nurses)
        self.tschedule = TabuSchedule(self.schedule)

        nurses = self.tschedule.nurses
        nurses[0].undesiredShifts.night[3] = 1
        self.tschedule.assignPatternToNurse(nurses[0], TabuShiftPattern([1, 1, 1, 1, 1, 0, 0], [0] * 7))
        self.tschedule.assignPatternToNurse(nurses[1], TabuShiftPattern([1, 0, 1, 1, 1, 0, 1], [0] * 7))
        self.tschedule.assignPatternToNurse(nurses[2], TabuShiftPattern([0] * 7, [0, 0, 1, 1, 1, 1, 0]))
