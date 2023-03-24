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

    # ----------------------------------- init(self, nurse) -----------------------------------
    def test_init_returns_tabu_nurse_with_same_fields_as_parameter_nurse(self):
        # Check if every field is converted correctly
        self.nurse = Nurse(0, Grade.ONE, Contract(5, 4))
        self.tabunurse = TabuNurse(self.nurse)

        self.assertEqual(self.nurse.id, self.tabunurse.id)
        self.assertEqual(self.nurse.contract, self.tabunurse.contract)
        self.assertEqual(self.nurse.grade, self.tabunurse.grade)

    # ----------------------------------- assignShiftPattern(self, pattern) -----------------------------------
    def test_assigning_pattern_changes_field_pattern(self):
        pattern = TabuShiftPattern([1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        self.testnurse._assignShiftPattern(pattern)
        self.assertEqual(pattern.merged, self.testnurse.shiftPattern.merged)

    def test_assigning_day_pattern_changes_worksNight_to_false(self):
        pattern = TabuShiftPattern([1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        self.testnurse._assignShiftPattern(pattern)
        self.assertEqual(False, self.testnurse.worksNight)

    def test_assigning_night_pattern_changes_worksNight_to_true(self):
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0])
        self.testnurse._assignShiftPattern(pattern)
        self.assertEqual(True, self.testnurse.worksNight)

    def test_nurse_eq_nurse_with_same_id_and_grade_returns_true(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        self.assertEqual(True, n == self.testnurse)

    # ----------------------------------- calculatePenalty(self) -----------------------------------
    # TODO: Make test for calculate penalty
    # consecutiveWorkDays
    def test_calculate_penalty_nurse_works_one_day_too_much_than_what_maximum_consecutive_work_days_returns_30(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0, 0])
        pattern2 = TabuShiftPattern([1, 1, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0])

        n.consecutiveWorkingDays = (1, 1)
        self.assertEqual(30, n.calculatePenalty(pattern))
        self.assertEqual(30, n.calculatePenalty(pattern2))

    def test_calculate_penalty_nurse_no_work_day_consecutive_work_days_returns_0(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))

        n.consecutiveWorkingDays = (1, 1)
        self.assertEqual(0, n.calculatePenalty(n.shiftPattern))

    def test_calculate_penalty_nurse_works_one_day_too_less_consecutive_work_days_refer_returns_30(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 1, 0, 0])
        pattern2 = TabuShiftPattern([1, 1, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0])

        n.consecutiveWorkingDays = (2, 2)
        self.assertEqual(30, n.calculatePenalty(pattern))
        self.assertEqual(30, n.calculatePenalty(pattern2))

    def test_calculate_penalty_nurse_works_one_day_too_less_and_much_consecutive_work_days_refer_returns_60(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 1, 1])
        pattern2 = TabuShiftPattern([1, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0])

        n.consecutiveWorkingDays = (2, 2)
        self.assertEqual(60, n.calculatePenalty(pattern))
        self.assertEqual(60, n.calculatePenalty(pattern2))

    # consecutiveFreeDays
    def test_calculate_penalty_nurse_works_one_day_too_much_than_what_maximum_consecutive_days_off_returns_30(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 1, 1, 0])
        pattern2 = TabuShiftPattern([1, 1, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0])

        n.consecutiveDaysOff = (1, 1)
        self.assertEqual(30, n.calculatePenalty(pattern))
        self.assertEqual(30, n.calculatePenalty(pattern2))

    def test_calculate_penalty_nurse_no_consecutive_days_off_returns_0(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1])
        pattern2 = TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0])

        n.consecutiveDaysOff = (1, 1)
        self.assertEqual(0, n.calculatePenalty(pattern))
        self.assertEqual(0, n.calculatePenalty(pattern2))

    def test_calculate_penalty_nurse_works_one_day_too_less_consecutive_free_days_refer_returns_30(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 0, 0])
        pattern2 = TabuShiftPattern([1, 1, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0])

        n.consecutiveDaysOff = (2, 2)
        self.assertEqual(30, n.calculatePenalty(pattern))
        self.assertEqual(30, n.calculatePenalty(pattern2))

    def test_calculate_penalty_nurse_works_one_day_too_less_and_much_consecutive_days_off_returns_60(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0, 1])
        pattern2 = TabuShiftPattern([1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])

        n.consecutiveDaysOff = (2, 2)
        self.assertEqual(60, n.calculatePenalty(pattern))
        self.assertEqual(60, n.calculatePenalty(pattern2))

    # undesiredShifts
    def test_calculate_penalty_nurse_do_work_1_undesired_shift_returns_10(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0, 1])
        n.undesiredShifts = TabuShiftPattern([0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1])
        self.assertEqual(10, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        n.undesiredShifts = TabuShiftPattern([0, 0, 0, 0, 0, 0, 1], [0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(10, n.calculatePenalty(pattern))

    def test_calculate_penalty_nurse_do_not_work_undesired_shifts_returns_0(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0, 1])
        n.undesiredShifts = TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0, 1, 0, 0, 0, 1, 0])
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0], )
        n.undesiredShifts = TabuShiftPattern([0, 1, 0, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(0, n.calculatePenalty(pattern))

    def test_calculate_penalty_nurse_work_some_undesired_shifts_returns_30(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 1, 1])
        n.undesiredShifts = TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0, 1, 0, 1, 0, 1, 1])
        self.assertEqual(30, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0],)
        n.undesiredShifts = TabuShiftPattern([0, 1, 0, 1, 0, 1, 1], [1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(30, n.calculatePenalty(pattern))

    # completeWeekend
    def test_calculate_penalty_nurse_complete_weekend_true_has_not_complete_weekend_30(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        n.completeWeekend = True

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0, 1])
        self.assertEqual(30, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0],)
        self.assertEqual(30, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 1, 0])
        self.assertEqual(30, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0], )
        self.assertEqual(30, n.calculatePenalty(pattern))

    def test_calculate_penalty_nurse_complete_weekend_has_no_weekends_0(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        n.completeWeekend = True

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0, 0])
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0],)
        self.assertEqual(0, n.calculatePenalty(pattern))

    def test_calculate_penalty_nurse_complete_weekend_false_return_always_0(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        n.completeWeekend = False

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0, 1])
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0],)
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 1, 1])
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0], )
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0])
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0], )
        self.assertEqual(0, n.calculatePenalty(pattern))

    # undesiredWeekend
    def test_calculate_penalty_nurse_undesired_weekend_true_has_weekend_shift_returns_30(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        n.undesiredWeekend = True

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 1, 0, 1])
        self.assertEqual(30, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0], )
        self.assertEqual(30, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 1, 1, 0])
        self.assertEqual(30, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0], )
        self.assertEqual(30, n.calculatePenalty(pattern))

    def test_calculate_penalty_nurse_undesired_weekend_true_has_no_weekends_returns_0(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        n.undesiredWeekend = True

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 1, 0, 0])
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0],)
        self.assertEqual(0, n.calculatePenalty(pattern))

    def test_calculate_penalty_nurse_undesired_weekend_false_return_always_0(self):
        n = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))
        n.undesiredWeekend = False

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1])
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0],)
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 0, 1, 1])
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 0, 1, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0], )
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 0, 0])
        self.assertEqual(0, n.calculatePenalty(pattern))

        pattern = TabuShiftPattern([1, 1, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0], )
        self.assertEqual(0, n.calculatePenalty(pattern))

    # ----------------------------------- __eq__(self, other) -----------------------------------
    def test_nurse_eq_nurse_with_different_id_and_same_grade_returns_false(self):
        n = TabuNurse(Nurse(1, Grade.TWO, Contract(1, 1)))
        self.assertEqual(False, n == self.testnurse)

    def test_nurse_eq_nurse_with_same_id_and_different_grade_returns_false(self):
        n = TabuNurse(Nurse(0, Grade.ONE, Contract(1, 1)))
        self.assertEqual(False, n == self.testnurse)


if __name__ == '__main__':
    unittest.main()
