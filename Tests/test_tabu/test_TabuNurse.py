import unittest
import pytest

from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Nurse import Nurse
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuNurse import TabuNurse


class TabuNurseTests(unittest.TestCase):

    def setUp(self) -> None:
        self.testnurse = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))

    def tearDown(self) -> None:
        self.testnurse = TabuNurse(Nurse(0, Grade.TWO, Contract(1, 1)))

    def test_init(self):
        # Check if every field is converted correctly
        self.nurse = Nurse(0, Grade.ONE, Contract(5, 4))
        self.tabunurse = TabuNurse(self.nurse)

        self.assertEqual(self.nurse.id, self.tabunurse.id)
        self.assertEqual(self.nurse.contract, self.tabunurse.contract)
        self.assertEqual(self.nurse.grade, self.tabunurse.grade)

if __name__ == '__main__':
    unittest.main()
