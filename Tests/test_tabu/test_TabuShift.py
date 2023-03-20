import unittest
import pytest

from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Nurse import Nurse
from Domain.Models.Tabu.TabuNurse import TabuNurse
from Domain.Models.Tabu.TabuShift import TabuShift
from Domain.Models.Tabu.TabuShiftType import TabuShiftType


class TabuShiftTests(unittest.TestCase):

    def setUp(self) -> None:
        self.shiftDay = TabuShift([1, 2, 3], TabuShiftType.DAY, Days.MONDAY)
        self.shiftNight = TabuShift([1, 2, 3], TabuShiftType.NIGHT, Days.MONDAY)
        self.testnurse1 = TabuNurse(Nurse(0, Grade.ONE, Contract(5, 4)))
        self.testnurse2 = TabuNurse(Nurse(1, Grade.TWO, Contract(3, 2)))

    def tearDown(self) -> None:
        self.shiftDay.assignedNurses = [set(), set(), set()]
        self.shiftNight.assignedNurses = [set(), set(), set()]

    def test_init(self):
        pass

if __name__ == '__main__':
    unittest.main()
