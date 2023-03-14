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

    def test_assignShiftPattern(self):
        # Use the function and check is the shift-pattern was assigned correctly
        newShiftPattern = TabuShiftPattern([0] * 14)
        self.testnurse.assignShiftPattern(newShiftPattern)
        self.assertEqual(newShiftPattern, self.testnurse.assignedShiftPattern)

    def test_assignShiftPattern_not_correct_length(self):
        with pytest.raises(Exception) as exc:
            self.tabunurse.assignedShiftPattern(TabuShiftPattern([0] * 15))

        self.assertEqual('Shift pattern format is invalid', str(exc.value))

    @unittest.skip("not implemented")
    def test_calcPC(self):
        pass

    @unittest.skip("not implemented correctly")
    def test_findShiftPatterns(self):
        # This should find every possible shift-pattern for this nurse.
        self.testnurse.findShiftPatterns()
        self.assertEqual(14, len(self.testnurse.feasibleShiftPatterns))

        self.testnurse.contract = Contract(2, 2)
        self.testnurse.findShiftPatterns()
        self.assertEqual(72, len(self.testnurse.feasibleShiftPatterns))


if __name__ == '__main__':
    unittest.main()
