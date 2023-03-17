import unittest
import json

from Parser.NurseParser import NurseParser, JSONParser
from Domain.Models.Enums import Grade, ShiftType, Days
from Domain.Models import Nurse, Shift, Schedule


class TestOldJsonParser(unittest.TestCase):

    def test_parses_example(self):
        parser = NurseParser()
        exampleFilePath = "Data/Example/CompleteExample.json" 
        actualSchedule = parser.parseFromJSON(exampleFilePath)
        expectedSchedule = self.create_example_model()

        self.assertListEqual(expectedSchedule.nurses, actualSchedule.nurses)
        self.assertListEqual(expectedSchedule.shifts, actualSchedule.shifts)

    def test_fails_on_empty_input(self):
        parser = JSONParser()
        empty_json = json.loads('{}')

        self.assertRaises(ValueError, parser.parse, empty_json)

    def test_fails_on_missing_mandatory_keys(self):
        parser = JSONParser()
        # Missing DurationWeeks, but also elements in the lists
        fake_json = json.loads(
            """{
                "StartDate": "2023-04-01",
                "Nurses": [],
                "Shifts": []
            }"""
        ) 

        self.assertRaises(ValueError, parser.parse, fake_json)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def create_example_model(self):
        nurses = [
            Nurse(1, Grade.ONE, None)
        ]

        mockCoverRequirements = {
            Grade.ONE: 1,
            Grade.TWO: 2,
            Grade.THREE: 2 
        }

        shifts = []
        for i in range(7):
            n = i + 1
            day = self.intToDay(n)

            for i in range(3):
                n = i % 3
                n = n + 1

                shiftType = self.intToShiftType(n)
                shift = Shift(mockCoverRequirements, shiftType, day)
                shifts.append(shift)
        
        return Schedule(shifts, nurses)
    
    def intToShiftType(self, shift):
        match shift:
            case 1:
                return ShiftType.EARLY
            case 2:
                return ShiftType.LATE 
            case 3:
                return ShiftType.NIGHT
            case _:
                raise ValueError(f'{shift} has to be either early, late, or night')
    
    def intToDay(self, i):
        match i:
            case 1:
                return Days.MONDAY
            case 2:
                return Days.TUESDAY
            case 3:
                return Days.WEDNESDAY
            case 4:
                return Days.THURSDAY
            case 5:
                return Days.FRIDAY
            case 6:
                return Days.SATURDAY
            case 7:
                return Days.SUNDAY
            case _:
                raise ValueError(f'{i} not recognized as a valid index for day')


if __name__ == '__main__':
    unittest.main()