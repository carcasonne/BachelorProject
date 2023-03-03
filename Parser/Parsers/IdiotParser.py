from Domain.Models.Enums.Grade import *
from Domain.Models.Nurse import *
from Domain.Models.Shift import *
from Domain.Models.Schedule import *


class IdiotParser:
    def parse(self):
        nurses = []
        shifts = []

        nurse1 = Nurse(0, Grade.ONE)
        nurse2 = Nurse(1, Grade.TWO)
        nurse3 = Nurse(2, Grade.THREE)

        nurses.append(nurse1)
        nurses.append(nurse2)
        nurses.append(nurse3)

        requirements = {
            Grade.ONE: 1,
            Grade.TWO: 2,
            Grade.THREE: 3
        }
        i = 0
        while i < 21:
            if i % 3 == 0:
                shifts.append(Shift(requirements, True))
            else:
                shifts.append(Shift(requirements, False))

            i += 1

        return Schedule(shifts, nurses)
