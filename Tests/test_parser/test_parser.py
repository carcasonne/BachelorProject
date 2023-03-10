import unittest

from Parser.NurseParser import *



class TestJsonParser(unittest.TestCase):

    def test_parses_example(self):
        parser = NurseParser()
        exampleFilePath = "Tests/test_parser/CompleteExample.json" 
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
        for i in range(0, 21):
            n = i % 3
            n = n + 1

            shiftType = self.intToShiftType(n)
            isNightshift = shiftType == ShiftType.NIGHT
            shift = Shift(mockCoverRequirements, shiftType, isNightshift)
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

if __name__ == '__main__':
    unittest.main()