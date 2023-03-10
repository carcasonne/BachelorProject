from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Nurse import Nurse
from Domain.Models.Schedule import Schedule
from Domain.Models.Shift import Shift

shifts = []
for x in range(7):
    shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.EARLY, x))
    shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.LATE, x))
    shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.NIGHT, x))

nurses = []
for x in range(3):
    nurses.append(Nurse(Grade.ONE, Contract.FIVEORFOUR))
    nurses.append(Nurse(Grade.ONE, Contract.THREEORTWO))
    nurses.append(Nurse(Grade.ONE, Contract.FOURORTHREE))
    nurses.append(Nurse(Grade.ONE, Contract.THREEORTHREE))
    nurses.append(Nurse(Grade.TWO, Contract.FIVEORFOUR))
    nurses.append(Nurse(Grade.TWO, Contract.THREEORTWO))
    nurses.append(Nurse(Grade.TWO, Contract.FOURORTHREE))
    nurses.append(Nurse(Grade.TWO, Contract.THREEORTHREE))
    nurses.append(Nurse(Grade.THREE, Contract.FIVEORFOUR))
    nurses.append(Nurse(Grade.THREE, Contract.THREEORTWO))
    nurses.append(Nurse(Grade.THREE, Contract.FOURORTHREE))
    nurses.append(Nurse(Grade.THREE, Contract.THREEORTHREE))

schedule = Schedule(shifts, nurses)