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

    def test_random_kick_changes_one_pattern_for_one_nurse(self):
        oldSchedule = copy.deepcopy(self.schedule)
        scheduleWasChanged = False
        self.schedule = self.ts.randomKick(self.schedule)[0]
        for nurse in self.schedule.nurses:
            if nurse.shiftPattern != oldSchedule.nurses[nurse.id].shiftPattern:
                scheduleWasChanged = True
                break
        self.assertTrue(scheduleWasChanged)

    # ----------------------------------- balanceRestoring(self, schedule) -----------------------------------
    def test_balance_restoring_with_undercovered_days_returns_move_with_more_day_nurses(self):
        for nurse in self.schedule.nurses:
            if nurse.id < len(self.schedule.nurses):
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))

        oldSchedule = copy.deepcopy(self.schedule)
        oldWorksNight = 0
        oldWorksDay = 0
        for nurse in oldSchedule.nurses:
            if nurse.worksNight is True:
                oldWorksNight += 1
            else:
                oldWorksDay += 1

        newSchedule = self.ts.balanceRestoring(self.schedule, False)[0]
        newWorksNight = 0
        newWorksDay = 0
        for nurse in newSchedule.nurses:
            if nurse.worksNight is True:
                newWorksNight += 1
            else:
                newWorksDay += 1
        self.assertTrue(oldWorksDay < newWorksDay, "New schedule does not have more day nurses")
        self.assertTrue(oldWorksNight > newWorksNight, "New schedule does not have more night nurses")
        self.assertTrue(oldSchedule.CC > newSchedule.CC, "CC was not better")
        self.assertEqual(oldWorksDay+1, newWorksDay)
        self.assertEqual(oldWorksNight-1, newWorksNight)

    def test_balance_restoring_with_undercovered_nights_returns_move_with_more_night_nurses(self):
        for nurse in self.schedule.nurses:
            if nurse.id < len(self.schedule.nurses):
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))

        oldSchedule = copy.deepcopy(self.schedule)
        oldWorksNight = 0
        oldWorksDay = 0
        for nurse in oldSchedule.nurses:
            if nurse.worksNight is True:
                oldWorksNight += 1
            else:
                oldWorksDay += 1

        newSchedule = self.ts.balanceRestoring(self.schedule, False)[0]
        newWorksNight = 0
        newWorksDay = 0
        for nurse in newSchedule.nurses:
            if nurse.worksNight is True:
                newWorksNight += 1
            else:
                newWorksDay += 1
        self.assertTrue(oldWorksDay > newWorksDay, "New schedule does not have more day nurses")
        self.assertTrue(oldWorksNight < newWorksNight, "New schedule does not have more night nurses")
        self.assertTrue(oldSchedule.CC > newSchedule.CC, "CC was not better")
        self.assertEqual(oldWorksDay - 1, newWorksDay)
        self.assertEqual(oldWorksNight + 1, newWorksNight)

    def test_balance_restoring_with_covered_nights_and_days_returns_none(self):
        for nurse in self.schedule.nurses:
            if nurse.id < len(self.schedule.nurses)//2:
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))
            else:
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))

        self.assertEqual(None, self.ts.balanceRestoring(self.schedule, False))

    def test_balance_restoring_with_undercovered_nights_and_days_returns_none(self):
        self.assertEqual(None, self.ts.balanceRestoring(self.schedule, False))

    def test_balance_restoring_does_not_make_a_tabu_configuration_that_exists(self):
        tabuset = set()
        counter = True
        for n in self.schedule.nurses:
            if n.id < len(self.schedule.nurses) // 2:
                self.schedule.assignPatternToNurse(n, TabuShiftPattern([1, 0, 0, 0, 0, 0, 0], [0] * 7))
                tabuset.add(n.id)
            else:
                if counter:
                    tabuset.add(n.id)
                    counter = False
                self.schedule.assignPatternToNurse(n, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))

        self.ts.dayNightTabuList.append(tabuset)
        self.ts.makeMove((self.schedule, True))
        self.ts.makeMove(self.ts.balanceRestoring(self.schedule, False))
        self.assertNotEqual(tabuset, self.ts.dayNightTabuList[0], "Tabuset should not be able to be chossen")
        counter = 0
        for s in self.ts.dayNightTabuList:
            if s == tabuset:
                counter += 1
        self.assertEqual(1, counter)

    def test_balance_restoring_relaxed_takes_nurse0_even_though_it_is_in_the_tabu_list(self):
        for n in self.schedule.nurses:
            self.schedule.assignPatternToNurse(n, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))

        nurse = self.schedule.nurses[0]
        patternBefore = nurse.shiftPattern
        ccBefore = evaluateCC(self.schedule)
        self.ts.dayNightTabuList.append(set().add(nurse.id))
        schedule = self.ts.balanceRestoring(self.schedule, True)
        patternAfter = nurse.shiftPattern
        ccAfter = evaluateCC(schedule)

        self.assertEqual(schedule is not None)
        self.assertNotEqual(patternBefore, patternAfter, "Did not update pattern for nurse 0")
        self.assertTrue(ccBefore > ccAfter)

    # ----------------------------------- balanceSwap(self, schedule) -----------------------------------
    #def test_balance_swap_swaps_two_nurses


if __name__ == '__main__':
    unittest.main()