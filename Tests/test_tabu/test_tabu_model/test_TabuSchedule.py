import unittest
from numpy.ma.core import copy

from Domain.Models.Enums.Grade import Grade
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuNurse import TabuNurse
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from Tests.test_tabu.TestTabuData import TestTabuData


class Test_TabuSchedule(unittest.TestCase):

    def setUp(self) -> None:
        self.s = TestTabuData().schedule
        self.ts = TabuSchedule(self.s)

    def tearDown(self) -> None:
        s = TestTabuData()
        self.ts = TabuSchedule(s.schedule)

    # ----------------------------------- init(self, schedule) -----------------------------------
    def test_init_nurses_is_set_correct(self):
        for x in range(len(self.ts.nurses)):
            self.assertEqual(TabuNurse(self.s.nurses[x]), self.ts.nurses[x])

    def test_init_shifts_is_converted_correctly(self):
        for i in range(7):
            # Check that days are passed correctly: len(shifts) = 21 -> len(shifts) = 14
            d1 = self.s.shifts[i*3].coverRequirements[Grade.ONE] + self.s.shifts[1 + i*3].coverRequirements[Grade.ONE]
            d2 = self.s.shifts[i*3].coverRequirements[Grade.TWO] + self.s.shifts[1 + i*3].coverRequirements[Grade.TWO]
            d3 = self.s.shifts[i*3].coverRequirements[Grade.THREE] + self.s.shifts[1 + i*3].coverRequirements[Grade.THREE]
            self.assertEqual(d1, self.ts.shifts[i*2].coverRequirements[Grade.ONE])
            self.assertEqual(d2, self.ts.shifts[i*2].coverRequirements[Grade.TWO])
            self.assertEqual(d3, self.ts.shifts[i*2].coverRequirements[Grade.THREE])

            n1 = self.s.shifts[2 + i*3].coverRequirements[Grade.ONE]
            n2 = self.s.shifts[2 + i*3].coverRequirements[Grade.TWO]
            n3 = self.s.shifts[2 + i*3].coverRequirements[Grade.THREE]
            self.assertEqual(n1, self.ts.shifts[1 + i*2].coverRequirements[Grade.ONE])
            self.assertEqual(n2, self.ts.shifts[1 + i*2].coverRequirements[Grade.TWO])
            self.assertEqual(n3, self.ts.shifts[1 + i*2].coverRequirements[Grade.THREE])

    # ----------------------------------- assignNurseToPattern(self, schedule, nurse, pattern) -----------------------------------
    def test_assign_nurse_to_pattern_changes_the_shifts_nurses_assigned_grade_one(self):
        pattern = TabuShiftPattern([1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        nurse = self.ts.nurses[0]
        self.ts.assignPatternToNurse(nurse, pattern)
        self.assertEqual(nurse.shiftPattern, pattern)
        merged = pattern.merged
        for i in range(14):
            if merged[i] == 1:
                self.assertEqual(1, len(self.ts.shifts[i].assignedNurses[Grade.ONE]))
                self.assertEqual(1, len(self.ts.shifts[i].assignedNurses[Grade.TWO]))
                self.assertEqual(1, len(self.ts.shifts[i].assignedNurses[Grade.THREE]))

    def test_assign_nurse_to_pattern_changes_the_shifts_nurses_assigned_grade_two(self):
        pattern = TabuShiftPattern([1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        nurse = self.ts.nurses[0]
        nurse2 = self.ts.nurses[4]
        self.ts.assignPatternToNurse(nurse, pattern)
        self.ts.assignPatternToNurse(nurse2, pattern)
        merged = pattern.merged
        for i in range(14):
            if merged[i] == 1:
                self.assertEqual(1, len(self.ts.shifts[i].assignedNurses[Grade.ONE]))
                self.assertEqual(2, len(self.ts.shifts[i].assignedNurses[Grade.TWO]))
                self.assertEqual(2, len(self.ts.shifts[i].assignedNurses[Grade.THREE]))

    def test_assign_nurse_to_pattern_removes_assigns_from_old_pattern(self):
        pattern = TabuShiftPattern([1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        pattern2 = TabuShiftPattern([0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0])
        nurse = self.ts.nurses[0]
        self.ts.assignPatternToNurse(nurse, pattern)
        oldPattern = nurse.shiftPattern.merged
        self.ts.assignPatternToNurse(nurse, pattern2)
        for i in range(14):
            if oldPattern[i] == 1:
                self.assertEqual(0, len(self.ts.shifts[i].assignedNurses[Grade.ONE]))
                self.assertEqual(0, len(self.ts.shifts[i].assignedNurses[Grade.TWO]))
                self.assertEqual(0, len(self.ts.shifts[i].assignedNurses[Grade.THREE]))


if __name__ == '__main__':
    unittest.main()
