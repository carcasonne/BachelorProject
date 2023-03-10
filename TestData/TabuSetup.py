from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Nurse import Nurse
from Domain.Models.Schedule import Schedule
from Domain.Models.Shift import Shift
from random import randint

RANDOMIZEDDATA = True

shifts = []
for x in range(7):
    if RANDOMIZEDDATA:
        shifts.append(Shift({Grade.ONE: randint(1, 2), Grade.TWO: randint(0, 3), Grade.THREE: randint(4, 7)}, ShiftType.EARLY, x))
        shifts.append(Shift({Grade.ONE: randint(1, 2), Grade.TWO: randint(0, 4), Grade.THREE: randint(4, 8)}, ShiftType.LATE, x))
        shifts.append(Shift({Grade.ONE: randint(1, 2), Grade.TWO: randint(0, 2), Grade.THREE: randint(3, 6)}, ShiftType.NIGHT, x))
    else:
        shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.EARLY, x))
        shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.LATE, x))
        shifts.append(Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, ShiftType.NIGHT, x))

nurses = []

if RANDOMIZEDDATA:
    for x in range(randint(30, 42)):

        randVal = randint(1, 100)
        if randVal < 12:
            grade = Grade.ONE
        elif randVal < 30:
            grade = Grade.TWO
        else:
            grade = Grade.THREE

        randVal = randint(1, 100)
        if randVal < 10:
            contract = Contract(3, 2)
        elif randVal < 20:
            contract = Contract(3, 3)
        elif randVal < 35:
            contract = Contract(4, 3)
        else:
            contract = Contract(5, 4)

        nurses.append(Nurse(x, grade, contract))


else:
    for x in range(3):
        nurses.append(Nurse(1 + (x*12), Grade.ONE, Contract(5, 4)))
        nurses.append(Nurse(2 + (x*12), Grade.ONE, Contract(3, 2)))
        nurses.append(Nurse(3 + (x*12), Grade.ONE, Contract(4, 3)))
        nurses.append(Nurse(4 + (x*12), Grade.ONE, Contract(3, 3)))
        nurses.append(Nurse(5 + (x*12), Grade.TWO, Contract(5, 4)))
        nurses.append(Nurse(6 + (x*12), Grade.TWO, Contract(3, 2)))
        nurses.append(Nurse(7 + (x*12), Grade.TWO, Contract(4, 3)))
        nurses.append(Nurse(8 + (x*12), Grade.TWO, Contract(3, 3)))
        nurses.append(Nurse(9 + (x*12), Grade.THREE, Contract(5, 4)))
        nurses.append(Nurse(10 + (x*12), Grade.THREE, Contract(3, 2)))
        nurses.append(Nurse(11 + (x*12), Grade.THREE, Contract(4, 3)))
        nurses.append(Nurse(12 + (x*12), Grade.THREE, Contract(3, 3)))

schedule = Schedule(shifts, nurses)