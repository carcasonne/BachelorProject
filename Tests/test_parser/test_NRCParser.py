import unittest

from Parser.NurseParser import NurseParser
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Contract import Contract
from Domain.Models.Nurse import Nurse
from Domain.Models.Shift import Shift
from Domain.Models.Schedule import Schedule

class TestNewJsonParser(unittest.TestCase):
    def test_parses_example(self):
        parser = NurseParser()
        scenario = "SimpleScenario"
        actualSchedule = parser.parseScenario(scenario, True)
        expectedSchedule = self.create_example_model()

        self.assertListEqual(expectedSchedule.nurses, actualSchedule.nurses)
        self.assertListEqual(expectedSchedule.shifts, actualSchedule.shifts)
    
    # What is expected from Data/Example/SimpleScenario
    def create_example_model(self):
        fullTime = Contract(5, 4)
        partTime = Contract(4,3)
        halfTime = Contract(3,2)
        nurses = [
            Nurse(0, Grade.ONE, fullTime),
            Nurse(1, Grade.ONE, halfTime),
            Nurse(2, Grade.TWO, halfTime),
            Nurse(3, Grade.TWO, partTime),
            Nurse(4, Grade.TWO, halfTime),
            Nurse(5, Grade.TWO, fullTime),
            Nurse(6, Grade.TWO, partTime),
            Nurse(7, Grade.TWO, halfTime),
            Nurse(8, Grade.TWO, fullTime),
            Nurse(9, Grade.TWO, halfTime),
            Nurse(10, Grade.TWO, fullTime),
            Nurse(11, Grade.TWO, fullTime),
            Nurse(12, Grade.THREE, partTime),
            Nurse(13, Grade.THREE, fullTime),
            Nurse(14, Grade.THREE, halfTime),
        ]

        shifts = [
            Shift({Grade.ONE: 1, Grade.TWO: 4, Grade.THREE: 5}, ShiftType.EARLY, Days.MONDAY),
            Shift({Grade.ONE: 0, Grade.TWO: 6, Grade.THREE: 7}, ShiftType.LATE, Days.MONDAY),
            Shift({Grade.ONE: 0, Grade.TWO: 3, Grade.THREE: 3}, ShiftType.NIGHT, Days.MONDAY),

            Shift({Grade.ONE: 0, Grade.TWO: 3, Grade.THREE: 4}, ShiftType.EARLY, Days.TUESDAY),
            Shift({Grade.ONE: 0, Grade.TWO: 5, Grade.THREE: 6}, ShiftType.LATE, Days.TUESDAY),
            Shift({Grade.ONE: 0, Grade.TWO: 3, Grade.THREE: 4}, ShiftType.NIGHT, Days.TUESDAY),

            Shift({Grade.ONE: 0, Grade.TWO: 3, Grade.THREE: 4}, ShiftType.EARLY, Days.WEDNESDAY),
            Shift({Grade.ONE: 0, Grade.TWO: 5, Grade.THREE: 6}, ShiftType.LATE, Days.WEDNESDAY),
            Shift({Grade.ONE: 0, Grade.TWO: 3, Grade.THREE: 3}, ShiftType.NIGHT, Days.WEDNESDAY),

            Shift({Grade.ONE: 0, Grade.TWO: 4, Grade.THREE: 4}, ShiftType.EARLY, Days.THURSDAY),
            Shift({Grade.ONE: 1, Grade.TWO: 7, Grade.THREE: 7}, ShiftType.LATE, Days.THURSDAY),
            Shift({Grade.ONE: 0, Grade.TWO: 3, Grade.THREE: 4}, ShiftType.NIGHT, Days.THURSDAY),

            Shift({Grade.ONE: 0, Grade.TWO: 4, Grade.THREE: 4}, ShiftType.EARLY, Days.FRIDAY),
            Shift({Grade.ONE: 1, Grade.TWO: 5, Grade.THREE: 5}, ShiftType.LATE, Days.FRIDAY),
            Shift({Grade.ONE: 0, Grade.TWO: 4, Grade.THREE: 4}, ShiftType.NIGHT, Days.FRIDAY),

            Shift({Grade.ONE: 0, Grade.TWO: 0, Grade.THREE: 1}, ShiftType.EARLY, Days.SATURDAY),
            Shift({Grade.ONE: 1, Grade.TWO: 5, Grade.THREE: 7}, ShiftType.LATE, Days.SATURDAY),
            Shift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 2}, ShiftType.NIGHT, Days.SATURDAY),

            Shift({Grade.ONE: 0, Grade.TWO: 1, Grade.THREE: 1}, ShiftType.EARLY, Days.SUNDAY),
            Shift({Grade.ONE: 1, Grade.TWO: 3, Grade.THREE: 5}, ShiftType.LATE, Days.SUNDAY),
            Shift({Grade.ONE: 0, Grade.TWO: 1, Grade.THREE: 2}, ShiftType.NIGHT, Days.SUNDAY),
        ]

        return Schedule(shifts, nurses)


if __name__ == '__main__':
    unittest.main()