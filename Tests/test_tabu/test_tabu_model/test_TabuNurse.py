import unittest
import pytest

from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Nurse import Nurse
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuNurse import TabuNurse


class Test_TabuNurse(unittest.TestCase):

    def setUp(self) -> None:
        self.testnurse = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))

    def tearDown(self) -> None:
        self.testnurse = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))

    def test_init_returns_tabu_nurse_with_same_fields_as_parameter_nurse(self):
        # Check if every field is converted correctly
        self.nurse = Nurse(0, Grade.ONE, Contract(5, 4))
        self.tabunurse = TabuNurse(self.nurse)

        self.assertEqual(self.nurse.id, self.tabunurse.id)
        self.assertEqual(self.nurse.contract, self.tabunurse.contract)
        self.assertEqual(self.nurse.grade, self.tabunurse.grade)

    def test_assigning_pattern_changes_field_pattern(self):
        pattern = TabuShiftPattern([1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        self.testnurse.assignShiftPattern(pattern)
        self.assertEqual(pattern.merged, self.testnurse.shiftPattern.merged)

    def test_assigning_day_pattern_changes_worksNight_to_false(self):
        pattern = TabuShiftPattern([1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        self.testnurse.assignShiftPattern(pattern)
        self.assertEqual(False, self.testnurse.worksNight)

    def test_assigning_night_pattern_changes_worksNight_to_true(self):
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0])
        self.testnurse.assignShiftPattern(pattern)
        self.assertEqual(True, self.testnurse.worksNight)

    def test_nurse_eq_nurse_with_same_id_and_grade_returns_true(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        self.assertEqual(True, n == self.testnurse)

    def test_nurse_eq_nurse_with_different_id_and_same_grade_returns_false(self):
        n = TabuNurse(Nurse(1, Grade.TWO, Contract(1, 1)))
        self.assertEqual(False, n == self.testnurse)

    def test_nurse_eq_nurse_with_same_id_and_different_grade_returns_false(self):
        n = TabuNurse(Nurse(0, Grade.ONE, Contract(1, 1)))
        self.assertEqual(False, n == self.testnurse)


if __name__ == '__main__':
    unittest.main()
