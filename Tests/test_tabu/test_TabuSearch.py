import copy
import unittest

from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.StaticMethods import evaluateCC
from Tests.test_tabu.TestTabuData import TestTabuData
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE


class Test_TabuSearch(unittest.TestCase):

    def setUp(self) -> None:
        self.schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))
        self.ts = TabuSearch_SIMPLE(self.schedule)

    def tearDown(self) -> None:
        self.schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))
        self.ts = TabuSearch_SIMPLE(self.schedule)

    # ----------------------------------- init(self, schedule) -----------------------------------
    def test_init_parameters_are_set_correctly(self):
        pass

    # ----------------------------------- makeMove(self, move) -----------------------------------
    def test_make_move_does_not_change_the_day_night_split_increases_day_night_counter(self):
        pass

    # ----------------------------------- run(self) -----------------------------------

    # ----------------------------------- randomDecent(self, schedule) -----------------------------------
    def test_random_decent_returns_schedule_with_better_CC(self):
        oldCC = self.schedule.CC
        newCC = self.ts.randomDecent(self.schedule)[0].CC
        self.assertTrue(oldCC > newCC)

    def test_random_decent_does_not_change_old_schedules_CC(self):
        oldCC = self.schedule.CC
        self.ts.randomDecent(self.schedule)
        newCC = evaluateCC(self.schedule)
        self.assertEqual(oldCC, newCC)

    def test_random_decent_if_no_move_is_found_returns_none(self):
        for i in range(len(self.schedule.nurses) // 9):
            for x in range(9):
                if x % 3 == 0:
                    self.schedule.assignPatternToNurse(self.schedule.nurses[0 + i * 9 + x],
                                                       TabuShiftPattern([1, 1, 1, 1, 1, 1, 1, 1],
                                                                        [0, 0, 0, 0, 0, 0, 0]))
                else:
                    self.schedule.assignPatternToNurse(self.schedule.nurses[0 + i * 9 + x],
                                                       TabuShiftPattern([0, 0, 0, 0, 0, 0, 0],
                                                                        [1, 1, 1, 1, 1, 1, 1, 1]))
        out = self.ts.randomDecent(self.schedule)
        self.assertEqual(None, out)

    def test_ramdom_kick_changes_one_pattern_for_one_nurse(self):
        oldSched = copy.deepcopy(self.schedule)
        schedWasChanged = False
        self.ts.randomKick(self.schedule)
        for nurse in self.schedule.nurses:
            if nurse.shiftPattern != oldSched.nurses[nurse.id].shiftPattern:
                schedWasChanged = True
                break
        self.assertTrue(schedWasChanged)



if __name__ == '__main__':
    unittest.main()