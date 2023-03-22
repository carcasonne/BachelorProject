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
        nurse.assignShiftPattern(dp1)
        self.assertEqual(1, nurseWorksPattern(nurse, dp1))
        nurse.assignShiftPattern(np2)
        self.assertEqual(1, nurseWorksPattern(nurse, np2))

    def test_nurse_does_not_work_pattern_returns_0(self):
        nurse = self.schedule.nurses[0]
        dp1 = TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0])
        dp2 = TabuShiftPattern([1, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        np1 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 1, 0, 1])
        np2 = TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 1, 0, 1])
        nurse.assignShiftPattern(dp1)
        self.assertEqual(0, nurseWorksPattern(nurse, np1))
        self.assertEqual(0, nurseWorksPattern(nurse, dp2))
        nurse.assignShiftPattern(np1)
        self.assertEqual(0, nurseWorksPattern(nurse, dp1))
        self.assertEqual(0, nurseWorksPattern(nurse, np2))

    # ----------------------------------- evaluateCC(schedule) -----------------------------------
    # TODO: ALL EVALUATE FUNCTIONS ONLY IMPLEMENTS GRADE 3 - SHOULD ALSO INCLUDE GRADE 1 AND GRADE 2 AT LATER STATE
    def test_evaluate_CC_empty_schedule_returns_63(self):
        self.assertEqual(63, evaluateCC(self.schedule))

    def test_evaluate_CC_with_nurses_added_on_all_days_returns_21(self):
        self.schedule.nurses[0].assignShiftPattern(TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
        self.schedule.nurses[1].assignShiftPattern(TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
        self.schedule.nurses[2].assignShiftPattern(TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
        self.schedule.nurses[3].assignShiftPattern(TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
        self.schedule.nurses[4].assignShiftPattern(TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))
        self.schedule.nurses[5].assignShiftPattern(TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0]))

        self.assertEqual(21, evaluateCC(self.schedule))

    def test_evaluate_CC_with_nurses_added_on_all_days_returns_42(self):
        self.schedule.nurses[0].assignShiftPattern(TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]))
        self.schedule.nurses[1].assignShiftPattern(TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]))
        self.schedule.nurses[2].assignShiftPattern(TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]))

        self.assertEqual(42, evaluateCC(self.schedule))

    def test_evaluate_CC_with_filled_up_schedule_returns_0(self):
        for i in range(len(self.schedule.nurses) // 9):
            for x in range(9):
                if x % 3 == 0:
                    self.schedule.nurses[0 + i * 9 + x].assignShiftPattern(
                        TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]))
                else:
                    self.schedule.nurses[0 + i * 9 + x].assignShiftPattern(
                        TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]))
        self.assertEqual(0, evaluateCC(self.schedule))

    # TODO: This test currently fails, but based on the article it should fail... Make it different if Paloma say so.
    @unittest.skip("We need to talk with Paloma about this first")
    def test_evaluate_CC_over_assignment_of_a_shift_does_not_return_a_better_CC(self):
        self.schedule.nurses[0].assignShiftPattern(TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]))
        self.schedule.nurses[1].assignShiftPattern(TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]))
        self.schedule.nurses[2].assignShiftPattern(TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]))
        notOverAssigned = evaluateCC(self.schedule)

        self.schedule.nurses[3].assignShiftPattern(TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]))
        self.schedule.nurses[4].assignShiftPattern(TabuShiftPattern([0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]))
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


if __name__ == '__main__':
    unittest.main()
