from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Nurse import Nurse
from Domain.Models.Schedule import Schedule
from Domain.Models.Shift import Shift


class TestTabuData:
    def __init__(self):
        self.shifts = []
        for day in Days:
            self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.EARLY, day))
            self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.LATE, day))
            self.shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.NIGHT, day))

        self.nurses = []
        # Minimal amount of nurses:
        for x in range(1):
            self.nurses.append(Nurse(0 + (x * 12), Grade.ONE, Contract(5, 4)))
            self.nurses.append(Nurse(1 + (x * 12), Grade.ONE, Contract(3, 2)))
            self.nurses.append(Nurse(2 + (x * 12), Grade.ONE, Contract(4, 3)))
            self.nurses.append(Nurse(3 + (x * 12), Grade.ONE, Contract(3, 3)))
            self.nurses.append(Nurse(4 + (x * 12), Grade.TWO, Contract(5, 4)))
            self.nurses.append(Nurse(5 + (x * 12), Grade.TWO, Contract(3, 2)))
            self.nurses.append(Nurse(6 + (x * 12), Grade.TWO, Contract(4, 3)))
            self.nurses.append(Nurse(7 + (x * 12), Grade.TWO, Contract(3, 3)))
            self.nurses.append(Nurse(8 + (x * 12), Grade.THREE, Contract(5, 4)))
            self.nurses.append(Nurse(9 + (x * 12), Grade.THREE, Contract(3, 2)))
            self.nurses.append(Nurse(10 + (x * 12), Grade.THREE, Contract(4, 3)))
            self.nurses.append(Nurse(11 + (x * 12), Grade.THREE, Contract(3, 3)))
        self.nurses.append(Nurse(12, Grade.ONE, Contract(4, 3)))
        self.nurses.append(Nurse(13, Grade.TWO, Contract(4, 3)))
        self.nurses.append(Nurse(14, Grade.THREE, Contract(4, 3)))
        self.nurses.append(Nurse(15, Grade.ONE, Contract(3, 3)))
        self.nurses.append(Nurse(16, Grade.TWO, Contract(3, 3)))
        self.nurses.append(Nurse(17, Grade.THREE, Contract(4, 3)))



        self.schedule = Schedule(self.shifts, self.nurses)
