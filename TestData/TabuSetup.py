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
    nurses.append(Nurse(1 + (x*12), Grade.ONE, Contract.FIVEORFOUR))
    nurses.append(Nurse(2 + (x*12), Grade.ONE, Contract.THREEORTWO))
    nurses.append(Nurse(3 + (x*12), Grade.ONE, Contract.FOURORTHREE))
    nurses.append(Nurse(4 + (x*12), Grade.ONE, Contract.THREEORTHREE))
    nurses.append(Nurse(5 + (x*12), Grade.TWO, Contract.FIVEORFOUR))
    nurses.append(Nurse(6 + (x*12), Grade.TWO, Contract.THREEORTWO))
    nurses.append(Nurse(7 + (x*12), Grade.TWO, Contract.FOURORTHREE))
    nurses.append(Nurse(8 + (x*12), Grade.TWO, Contract.THREEORTHREE))
    nurses.append(Nurse(9 + (x*12), Grade.THREE, Contract.FIVEORFOUR))
    nurses.append(Nurse(10 + (x*12), Grade.THREE, Contract.THREEORTWO))
    nurses.append(Nurse(11 + (x*12), Grade.THREE, Contract.FOURORTHREE))
    nurses.append(Nurse(12 + (x*12), Grade.THREE, Contract.THREEORTHREE))

schedule = Schedule(shifts, nurses)