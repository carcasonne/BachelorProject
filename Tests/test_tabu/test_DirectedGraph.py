import copy
import unittest

from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.StaticMethods import evaluateCC
from Tests.test_tabu.TestTabuData import TestTabuData
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE


class Test_DirectedGraph(unittest.TestCase):

    def setUp(self) -> None:
        self.schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))
        self.ts = TabuSearch_SIMPLE(self.schedule)

    def tearDown(self) -> None:
        self.schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))
        self.ts = TabuSearch_SIMPLE(self.schedule)

    # ----------------------------------- init(self, schedule) -----------------------------------



if __name__ == '__main__':
    unittest.main()