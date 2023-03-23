import copy
import unittest

from Domain.Models.Tabu.TabuSchedule import TabuSchedule
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
        newCC = self.ts.randomDecent(self.schedule)
        self.assertTrue(oldCC < newCC)


if __name__ == '__main__':
    unittest.main()