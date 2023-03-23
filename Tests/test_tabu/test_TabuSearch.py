import copy
import unittest

from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from Tests.test_tabu.TestTabuData import TestTabuData


class Test_TabuSearch(unittest.TestCase):

    def setUp(self) -> None:
        self.schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))

    def tearDown(self) -> None:
        self.schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))

    # ----------------------------------- init(self, schedule) -----------------------------------
    def test_init_parameters_are_set_correctly(self):
        pass

    # ----------------------------------- makeMove(self, move) -----------------------------------
    def test_make_move_does_not_change_the_day_night_split_increases_day_night_counter(self):
        pass

    # ----------------------------------- run(self) -----------------------------------


if __name__ == '__main__':
    unittest.main()