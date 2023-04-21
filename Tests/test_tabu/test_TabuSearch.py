import copy
import unittest

from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.StaticMethods import evaluateCC
from Tests.test_tabu.TestTabuData import TestTabuData
from Tests.test_tabu.NurseChainTestData import NurseChainTestData
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
        newCC = self.ts.randomDecent(self.schedule, 1)[0].CC
        self.assertTrue(oldCC > newCC)

    def test_random_decent_does_not_change_old_schedules_CC(self):
        oldCC = self.schedule.CC
        self.ts.randomDecent(self.schedule, 1)
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
        out = self.ts.randomDecent(self.schedule, 1)
        self.assertEqual(None, out)

    # ----------------------------------- randomKick(self, schedule) -----------------------------------
    def test_random_kick_changes_one_pattern_for_one_nurse(self):
        oldSchedule = copy.deepcopy(self.schedule)
        scheduleWasChanged = False
        for nurse in self.schedule.nurses:
            self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
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
        tmpDayNightTabuList = set()
        for nurse in self.schedule.nurses:
            if nurse.id < len(self.schedule.nurses):
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))
                tmpDayNightTabuList.add(nurse.id)

        self.ts.dayNightTabuList.insert(0, tmpDayNightTabuList)
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
        tmpDayNightTabuList = set()
        for nurse in self.schedule.nurses:
            if nurse.id < len(self.schedule.nurses)//2:
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))
                tmpDayNightTabuList.add(nurse.id)
            else:
                self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
        self.ts.dayNightTabuList.insert(0, tmpDayNightTabuList)
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
        self.ts.tabuList.append(nurse.id)
        schedule = self.ts.balanceRestoring(self.schedule, True)[0]
        patternAfter = self.schedule.nurses[0]
        ccAfter = evaluateCC(schedule)

        self.assertTrue(schedule is not None)
        self.assertNotEqual(patternBefore, patternAfter, "Did not update pattern for nurse 0")
        self.assertTrue(ccBefore > ccAfter)

    def test_balance_restoring_relaxed_takes_nurse0_even_though_it_is_in_the_day_night_list(self):
        for n in self.schedule.nurses:
            self.schedule.assignPatternToNurse(n, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))

        nurse = self.schedule.nurses[0]
        patternBefore = nurse.shiftPattern
        ccBefore = evaluateCC(self.schedule)
        self.ts.dayNightTabuList.append(set().add(nurse.id))
        schedule = self.ts.balanceRestoring(self.schedule, True)[0]
        patternAfter = self.schedule.nurses[0]
        ccAfter = evaluateCC(schedule)

        self.assertTrue(schedule is not None)
        self.assertNotEqual(patternBefore, patternAfter, "Did not update pattern for nurse 0")
        self.assertTrue(ccBefore > ccAfter)

    # ----------------------------------- balanceSwap(self, schedule) -----------------------------------
    def test_balance_swap_swaps_two_nurses(self):
        for n in self.schedule.nurses:
            self.schedule.assignPatternToNurse(n, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
        oldPattern = TabuShiftPattern([1, 0, 0, 0, 0, 0, 0], [0] * 7)
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], oldPattern)
        schedule = self.ts.balanceSwap(self.schedule, False)[0]
        counter = 0
        tmpnurse = None
        for nurse in schedule.nurses:
            if nurse.worksNight is False:
                tmpnurse = nurse.id
                counter += 1
        self.assertEqual(1, counter)
        self.assertNotEqual(0, tmpnurse)
        self.assertEqual(True, schedule.nurses[0].worksNight)

    def test_balance_swap_swaps_two_nurses_with_relaxed_false_does_not_use_tabu_nurse(self):
        for n in self.schedule.nurses:
            self.schedule.assignPatternToNurse(n, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
        oldPattern = TabuShiftPattern([1, 0, 0, 0, 0, 0, 0], [0] * 7)
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], oldPattern)
        self.ts.tabuList.append(self.schedule.nurses[2].id)
        schedule = self.ts.balanceSwap(self.schedule, False)[0]
        counter = 0
        tmpnurse = None
        for nurse in schedule.nurses:
            if not nurse.worksNight:
                tmpnurse = nurse.id
                counter += 1
        self.assertEqual(1, counter)
        self.assertNotEqual(2, tmpnurse)
        self.assertEqual(True, schedule.nurses[0].worksNight)

    def test_balance_swap_swaps_two_nurses_with_relaxed_true_uses_tabu_nurse(self):
        for n in self.schedule.nurses:
            self.schedule.assignPatternToNurse(n, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
        oldPattern = TabuShiftPattern([1, 0, 0, 0, 0, 0, 0], [0] * 7)
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], oldPattern)
        self.ts.tabuList.append(self.schedule.nurses[2].id)
        schedule = self.ts.balanceSwap(self.schedule, True)[0]
        counter = 0
        tmpnurse = None
        for nurse in schedule.nurses:
            if not nurse.worksNight:
                tmpnurse = nurse.id
                counter += 1
        self.assertEqual(1, counter)
        self.assertEqual(2, tmpnurse)
        self.assertEqual(True, schedule.nurses[0].worksNight)

    def test_balance_swap_swaps_two_nurses_with_relaxed_false_should_not_result_in_tabu_configuration(self):
        for n in self.schedule.nurses:
            self.schedule.assignPatternToNurse(n, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
        oldPattern = TabuShiftPattern([0, 1, 0, 0, 0, 0, 0], [0] * 7)
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], oldPattern)
        tmpset = set()
        tmpset.add(self.schedule.nurses[2].id)
        self.ts.dayNightTabuList.append(tmpset)
        schedule = self.ts.balanceSwap(self.schedule, False)[0]
        counter = 0
        tmpnurse = None
        for nurse in schedule.nurses:
            if not nurse.worksNight:
                tmpnurse = nurse.id
                counter += 1
        self.assertEqual(1, counter)
        self.assertNotEqual(2, tmpnurse)
        self.assertEqual(True, schedule.nurses[0].worksNight)

    def test_balance_swap_swaps_two_nurses_with_relaxed_true_results_in_tabu_configuration(self):
        for n in self.schedule.nurses:
            self.schedule.assignPatternToNurse(n, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
        oldPattern = TabuShiftPattern([1, 0, 0, 0, 0, 0, 0], [0] * 7)
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], oldPattern)
        tmpset = set()
        tmpset.add(self.schedule.nurses[2].id)
        self.ts.dayNightTabuList.append(tmpset)
        schedule = self.ts.balanceSwap(self.schedule, True)[0]
        counter = 0
        tmpnurse = None
        for nurse in schedule.nurses:
            if not nurse.worksNight:
                tmpnurse = nurse.id
                counter += 1
        self.assertEqual(1, counter)
        self.assertEqual(2, tmpnurse)
        self.assertEqual(True, schedule.nurses[0].worksNight)

    # ----------------------------------- shiftChain(self, schedule) -----------------------------------
    def test_shift_chain_on_an_only_night_schedule_returns_decrease_in_cc_and_pc(self):
        self.ts.initSchedule()
        for n in self.schedule.nurses:
            self.schedule.assignPatternToNurse(n, TabuShiftPattern([0] * 7, [1, 0, 1, 1, 1, 1, 1]))

        newSchedule = copy.deepcopy(self.schedule)
        newSchedule = self.ts.shiftChain(newSchedule, 1)[0]
        self.assertTrue(newSchedule.CC < self.schedule.CC)
        self.assertTrue(newSchedule.PC <= self.schedule.PC)

    def test_shift_chain_on_an_only_day_schedule_returns_decrease_in_cc_and_pc(self):
        self.ts.initSchedule()
        for n in self.schedule.nurses:
            self.schedule.assignPatternToNurse(n, TabuShiftPattern([1, 0, 1, 1, 1, 1, 1], [0] * 7))

        newSchedule = copy.deepcopy(self.schedule)
        newSchedule = self.ts.shiftChain(newSchedule, 1)[0]
        self.assertTrue(newSchedule.CC < self.schedule.CC)
        self.assertTrue(newSchedule.PC <= self.schedule.PC)

    def test_shift_chain_on_an_only_day_schedule_updates_tabu_list(self):
        for n in self.schedule.nurses:
            self.schedule.assignPatternToNurse(n, TabuShiftPattern([1, 1, 0, 1, 1, 1, 1], [0] * 7))
        self.schedule.assignPatternToNurse(self.schedule.nurses[0], TabuShiftPattern([0] * 7, [1, 1, 0, 1, 1, 1, 1]))
        self.ts.balanceRestoring(self.schedule, False)
        oldTabuList = copy.deepcopy(self.ts.tabuList)
        self.ts.shiftChain(self.schedule, 1)
        self.assertNotEqual(oldTabuList, self.ts.tabuList)

    def test_shift_chain_on_an_strict_little_undercovered_day_pattern_does_not_return_pc_increase(self):
        nurses = self.schedule.nurses
        self.schedule.assignPatternToNurse(nurses[0], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))
        self.schedule.assignPatternToNurse(nurses[1], TabuShiftPattern([1, 0, 1, 1, 1, 1, 1], [0] * 7))
        self.schedule.assignPatternToNurse(nurses[2], TabuShiftPattern([1, 0, 0, 0, 0, 0, 0], [0] * 7))
        self.schedule.assignPatternToNurse(nurses[3], TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
        self.schedule.assignPatternToNurse(nurses[4], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))
        self.schedule.assignPatternToNurse(nurses[5], TabuShiftPattern([0, 1, 1, 1, 1, 1, 1], [0] * 7))
        self.schedule.assignPatternToNurse(nurses[6], TabuShiftPattern([0, 1, 0, 0, 0, 0, 0], [0] * 7))
        self.schedule.assignPatternToNurse(nurses[7], TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
        self.schedule.assignPatternToNurse(nurses[8], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))
        self.schedule.assignPatternToNurse(nurses[9], TabuShiftPattern([1, 1, 1, 1, 1, 1, 1], [0] * 7))
        self.schedule.assignPatternToNurse(nurses[10], TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
        self.schedule.assignPatternToNurse(nurses[11], TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))

        self.assertEqual(None, self.ts.shiftChain(self.schedule, 1))

    # ----------------------------------- nurseChain(self, schedule, phase) -----------------------------------
    def test_nurse_chain_phase_2_on_an_with_one_nurse_having_weekend_penalty_returns_schedule_with_decrease_in_covering_and_penalty(self):
        nurses = self.schedule.nurses
        for i in range(len(self.schedule.nurses) // 9):
            for x in range(9):
                if x % 3 == 0:
                    self.schedule.assignPatternToNurse(self.schedule.nurses[0 + i * 9 + x], self.ts.feasiblePatterns[self.schedule.nurses[0 + i * 9 + x].id][0])
                else:
                    self.schedule.assignPatternToNurse(self.schedule.nurses[0 + i * 9 + x], self.ts.feasiblePatterns[self.schedule.nurses[0+i*9+x].id][23])

        newSchedule = copy.copy(self.schedule)
        newSchedule = self.ts.nurseChain(newSchedule, 1)[0]
        self.assertTrue(self.schedule.CC > newSchedule.CC)
        self.assertTrue(self.schedule.PC >= newSchedule.PC)

    def test_nurse_chain_phase_1_with_random_init_function(self):
        self.ts.initSchedule()
        self.schedule = self.ts.currSolution
        newSchedule = copy.deepcopy(self.schedule)
        newSchedule = self.ts.nurseChain(newSchedule, 1)[0]
        self.assertTrue(self.schedule.CC > newSchedule.CC)
        self.assertTrue(self.schedule.PC >= newSchedule.PC)

    def test_nurse_chain_10_iterations_of_nurse_chain_does_not_increase_PC_or_CC(self):
        self.ts.initSchedule()
        counter = 0
        while counter < 5:
            CC = copy.copy(self.ts.currSolution.CC)
            PC = copy.copy(self.ts.currSolution.PC)
            self.ts.makeMove(self.ts.nurseChain(self.ts.currSolution, 2))
            self.assertTrue(CC >= self.ts.currSolution.CC)
            self.assertTrue(PC >= self.ts.currSolution.PC)
            counter += 1

    def test_nurse_chain_on_a_very_restricted_schedule_should_return__CC_equal_to_0(self):
        schedule = NurseChainTestData().tschedule
        newschedule = self.ts.nurseChain(copy.deepcopy(schedule), 1)[0]
        self.assertTrue(schedule.CC > newschedule.CC)
        self.assertTrue(schedule.PC >= newschedule.PC)

    def test_nurse_chain_on_a_very_restricted_with_phase_2_schedule_should_return__None(self):
        schedule = NurseChainTestData().tschedule
        newschedule = self.ts.nurseChain(copy.deepcopy(schedule), 2)
        self.assertEqual(newschedule, None)

    def test_nurse_chain_phase_2_should_return_decrease_in_PC(self):
        schedule = NurseChainTestData().tschedule
        schedule = self.ts.nurseChain(copy.deepcopy(schedule), 1)[0]
        schedule.nurses[1].undesiredShifts.day[3] = 1
        schedule.assignPatternToNurse(schedule.nurses[1], schedule.nurses[1].shiftPattern)
        newSchedule = self.ts.nurseChain(copy.deepcopy(schedule), 2)[0]

        self.assertTrue(schedule.PC > newSchedule.PC)
        self.assertTrue(schedule.CC == newSchedule.CC)
        self.assertEqual(newSchedule.CC, 0)
        self.assertEqual(newSchedule.PC, 0)

    # ----------------------------------- underCovering(self, schedule) -----------------------------------
    def test_under_covering_always_decreases_cc_if_possible(self):
        for nurse in self.schedule.nurses:
            self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))

        oldSchedule = copy.deepcopy(self.schedule)

        self.schedule = self.ts.underCovering(self.schedule)[0]

        self.assertTrue(oldSchedule.CC > self.schedule.CC)

    def test_under_covering_always_returns_best_cc_score_that_it_can_find(self):
        for nurse in self.schedule.nurses:
            self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))

        oldSchedule = copy.deepcopy(self.schedule)

        self.schedule = self.ts.underCovering(self.schedule)[0]

        self.assertEqual(oldSchedule.CC - 15, self.schedule.CC)

    def test_under_covering_does_not_choose_tabu_nurses(self):
        for nurse in self.schedule.nurses:
            self.schedule.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, [1, 1, 1, 1, 1, 1, 1]))
            self.ts.tabuList.append(nurse.id)

        returnvalue = self.ts.underCovering(self.schedule)

        self.assertIsNone(returnvalue)

    def test_under_covering_does_not_choose_end_up_with_day_night_tabu_coverage(self):
        for nurse in self.schedule.nurses:
            if nurse.id != 0:
                self.schedule.nurses.remove(nurse)

        self.ts.dayNightTabuList.append(set().add(0))

        returnvalue = self.ts.underCovering(self.schedule)

        self.assertIsNone(returnvalue)



if __name__ == '__main__':
    unittest.main()