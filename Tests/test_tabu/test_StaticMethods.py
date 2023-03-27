import copy
import unittest

from Domain.Models.Enums.Contract import Contract
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.StaticMethods import *
from Tests.test_tabu.TestTabuData import TestTabuData


class Test_StaticMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))

    def tearDown(self) -> None:
        self.schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))

    # ----------------------------------- patternCoverShift(pattern, shift) -----------------------------------
    def test_pattern_covers_shift_returns_1(self):
        s1 = self.schedule.shifts[0]
        s2 = self.schedule.shifts[1]
        p1 = TabuShiftPattern([1, 0, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        p3 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 1, 0, 1])
        self.assertEqual(1, patternCoverShift(p1, s1))
        self.assertEqual(1, patternCoverShift(p3, s2))

    def test_pattern_does_not_cover_shift_returns_0(self):
        s1 = self.schedule.shifts[0]
        s2 = self.schedule.shifts[1]
        p1 = TabuShiftPattern([1, 0, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        p2 = TabuShiftPattern([0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        p3 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 1, 0, 1])
        p4 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1])
        self.assertEqual(0, patternCoverShift(p2, s1))
        self.assertEqual(0, patternCoverShift(p3, s1))
        self.assertEqual(0, patternCoverShift(p4, s1))
        self.assertEqual(0, patternCoverShift(p1, s2))
        self.assertEqual(0, patternCoverShift(p2, s2))
        self.assertEqual(0, patternCoverShift(p4, s2))

    # ----------------------------------- nurseWorksPattern(nurse, pattern) -----------------------------------
    def test_nurse_works_pattern_returns_1(self):
        nurse = self.schedule.nurses[0]
        dp1 = TabuShiftPattern([1, 0, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        np2 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 1, 0, 1])
        nurse._assignShiftPattern(dp1)
        self.assertEqual(1, nurseWorksPattern(nurse, dp1))
        nurse._assignShiftPattern(np2)
        self.assertEqual(1, nurseWorksPattern(nurse, np2))

    def test_nurse_does_not_work_pattern_returns_0(self):
        nurse = self.schedule.nurses[0]
        dp1 = TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0])
        dp2 = TabuShiftPattern([1, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        np1 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 1, 0, 1])
        np2 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 1, 0, 1])
        nurse._assignShiftPattern(dp1)
        self.assertEqual(0, nurseWorksPattern(nurse, np1))
        self.assertEqual(0, nurseWorksPattern(nurse, dp2))
        nurse._assignShiftPattern(np1)
        self.assertEqual(0, nurseWorksPattern(nurse, dp1))
        self.assertEqual(0, nurseWorksPattern(nurse, np2))

    # ----------------------------------- evaluateCC(schedule) -----------------------------------
    # TODO: ALL EVALUATE FUNCTIONS ONLY IMPLEMENTS GRADE 3 - SHOULD ALSO INCLUDE GRADE 1 AND GRADE 2 AT LATER STATE
    def test_evaluate_CC_empty_schedule_returns_126(self):
        self.assertEqual(126, evaluateCC(self.schedule))

    def test_evaluate_CC_with_nurses_added_on_all_days_returns_42(self):
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[1], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[2], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[3], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[4], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[5], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))

        self.assertEqual(42, evaluateCC(self.schedule))

    def test_evaluate_CC_with_nurses_added_on_all_days_returns_84(self):
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[1], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[2], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]))

        self.assertEqual(84, evaluateCC(self.schedule))

    def test_evaluate_CC_with_filled_up_schedule_returns_0(self):
        for i in range(len(self.schedule.nurses) // 9):
            for x in range(9):
                if x % 3 == 0:
                    self.schedule.assignPatternToNurse(self.schedule.nurses[0 + i * 9 + x], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
                else:
                    self.schedule.assignPatternToNurse(self.schedule.nurses[0 + i * 9 + x], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]))
        self.assertEqual(0, evaluateCC(self.schedule))

    # TODO: This test currently fails, but based on the article it should fail... Make it different if Paloma say so.
    def test_evaluate_CC_over_assignment_of_a_shift_does_not_return_a_better_CC(self):
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[1], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[2], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0]))
        notOverAssigned = evaluateCC(self.schedule)

        self.schedule.assignPatternToNurse(self.schedule.nurses[3], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[4], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0]))
        overAssigned = evaluateCC(self.schedule)

        self.assertFalse(notOverAssigned > overAssigned)
        self.assertEqual(notOverAssigned, overAssigned)

    # ----------------------------------- findFeasiblePatterns(nurse) -----------------------------------
    def test_find_feasible_patterns_returns_only_patterns_based_on_nurse_contract(self):
        nurse = self.schedule.nurses[0]
        for p in findFeasiblePatterns(nurse):
            counter = 0
            for x in p.merged:
                if x == 1:
                    counter += 1
            if p.night == [0]*7:  # If pattern is a day pattern
                self.assertEqual(nurse.contract.days, counter)
            if p.day == [0] * 7:  # If pattern is a night pattern
                self.assertEqual(nurse.contract.nights, counter)

    def test_find_feasible_patterns_with_1_contract_days_and_nights_returns_14_patterns(self):
        nurse = self.schedule.nurses[0]
        nurse.contract = Contract(1, 1)
        self.assertEqual(14, len(findFeasiblePatterns(nurse)))

    def test_find_feasible_patterns_with_2_contract_days_and_nights_returns_42_patterns(self):
        nurse = self.schedule.nurses[0]
        nurse.contract = Contract(2, 2)
        self.assertEqual(42, len(findFeasiblePatterns(nurse)))

    def test_find_feasible_patterns_with_contract_5_days_and_2_nights_returns_42_patterns(self):
        nurse = self.schedule.nurses[0]
        nurse.contract = Contract(5, 2)
        self.assertEqual(42, len(findFeasiblePatterns(nurse)))

    def test_find_feasible_patterns_returns_only_TabuShiftPatterns(self):
        for nurse in self.schedule.nurses:
            for p in findFeasiblePatterns(nurse):
                self.assertIsInstance(p, TabuShiftPattern, "given object is not instance of TabuShiftPattern")

    # ----------------------------------- calculateDifferenceCC(schedule, nurse, pattern) -----------------------------------
    def test_calculate_differenceCC_calculates_same_difference_as_changing_the_schedule_day_pattern(self):
        pattern = TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0])
        nurse = self.schedule.nurses[0]
        beforeCC = self.schedule.CC
        result = calculateDifferenceCC(self.schedule, nurse, pattern)
        self.schedule.assignPatternToNurse(nurse, pattern)
        afterCC = evaluateCC(self.schedule)

        self.assertEqual(afterCC-beforeCC, result)

    def test_calculate_differenceCC_calculates_same_difference_as_changing_the_schedule_night_pattern(self):
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1])
        nurse = self.schedule.nurses[1]
        beforeCC = self.schedule.CC
        result = calculateDifferenceCC(self.schedule, nurse, pattern)
        self.schedule.assignPatternToNurse(nurse, pattern)
        afterCC = evaluateCC(self.schedule)

        self.assertEqual(afterCC - beforeCC, result)

    def test_calculate_differenceCC_returns_positive_differance(self):
        pattern = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1])
        pattern2 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 0, 1, 1])
        nurse = self.schedule.nurses[0]
        self.schedule.assignPatternToNurse(nurse, pattern)
        result = calculateDifferenceCC(self.schedule, nurse, pattern2)

        self.assertTrue(result > 0)
        self.assertEqual(6, result)

    def test_calculate_differenceCC_for_over_covered_shift_returns_only_decrease_in_CC(self):
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[1], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[2], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[3], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1]))
        CC = self.schedule.CC

        pattern = TabuShiftPattern([0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0])
        result = calculateDifferenceCC(self.schedule, self.schedule.nurses[0], pattern)
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], pattern)

        self.assertTrue(CC > self.schedule.CC)
        self.assertEqual(self.schedule.CC - CC, result)

    def test_calculate_differenceCC_for_semi_covered_shifts_returns_no_decrease_or_increase_in_CC(self):
        self.schedule.assignPatternToNurse(self.schedule.nurses[8], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[9], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[10], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1]))
        self.schedule.assignPatternToNurse(self.schedule.nurses[11], TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1]))
        CC = self.schedule.CC

        pattern = TabuShiftPattern([0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0])
        result = calculateDifferenceCC(self.schedule, self.schedule.nurses[8], pattern)

        self.assertEqual(CC, self.schedule.CC)
        self.assertEqual(0, result)

    # ----------------------------------- calculateDifferencePC(nurse, pattern) -----------------------------------
    def test_calculate_difference_pc_changing_pattern_returns_negative_60(self):
        nurse = self.schedule.nurses[0]
        nurse.undesiredWeekend = True
        nurse.completeWeekend = True
        self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0]*7, [0, 1, 0, 1, 0, 1, 0]))

        self.assertEqual(-60, calculateDifferencePC(nurse, TabuShiftPattern([0]*7, [0, 1, 0, 1, 1, 0, 0])))

    # ----------------------------------- evaluatePC(nurse, pattern) -----------------------------------
    def test_evaluate_pc_adding_new_shift_pattern_to_nurse_decrease_pc_with_60(self):
        nurse = self.schedule.nurses[0]
        nurse.undesiredWeekend = True
        nurse.completeWeekend = True
        self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0]*7, [0, 1, 0, 1, 0, 1, 0]))
        oldPC = self.schedule.PC
        self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0]*7, [0, 1, 0, 1, 1, 0, 0]))
        newPC = self.schedule.PC

        self.assertEqual(oldPC-60, newPC)

    # ----------------------------------- checkBalance(schedule) -----------------------------------
    # TODO: checkBalance() Tests...
    def test_check_with_satisfied_balance_returns_true_true(self):
        for nurse in self.schedule.nurses:
            if nurse.id < len(self.schedule.nurses)//2:
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0]*7, [1, 1, 1, 1, 1, 1, 1]))
            else:
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))

        self.assertEqual((True, True), checkBalance(self.schedule))

    def test_check_with_unsatisfied_day_balance_returns_false_true(self):
        for nurse in self.schedule.nurses:
            if nurse.id < len(self.schedule.nurses):
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0]*7, [1, 1, 1, 1, 1, 1, 1]))

        self.assertEqual((False, True), checkBalance(self.schedule))

    def test_check_with_unsatisfied_night_balance_returns_true_false(self):
        for nurse in self.schedule.nurses:
            if nurse.id < len(self.schedule.nurses):
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))

        self.assertEqual((True, False), checkBalance(self.schedule))

    def test_check_with_unsatisfied_day_and_night_balance_returns_false_false(self):
        self.assertEqual((False, False), checkBalance(self.schedule))

    def test_check_balance_with_one_unsatisfied_with_enough_nurses_the_other_days_returns_true_true(self):
        for nurse in self.schedule.nurses:
            if nurse.id < len(self.schedule.nurses) // 2:
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
            else:
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([1, 1, 1, 0, 1, 1, 1], [0] * 7))
        self.assertEqual((False, True), checkBalance(self.schedule))

    def test_check_balance_with_one_unsatisfied_with_enough_nurses_the_other_night_returns_false_true(self):
        for nurse in self.schedule.nurses:
            if nurse.id < len(self.schedule.nurses) // 2:
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 0, 1]))
            else:
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))
        self.assertEqual((True, False), checkBalance(self.schedule))


if __name__ == '__main__':
    unittest.main()
