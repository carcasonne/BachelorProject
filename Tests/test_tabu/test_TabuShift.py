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

    @unittest.skip("Not implemented correctly")
    def test_init(self):
        # TODO: init is not correct implemented. It should just take a Nurse
        pass

    def test_assignNurse(self):
        self.shiftDay.assignNurse(self.testnurse1)

        self.assertSetEqual(self.shiftDay.assignedNurses[0], {self.testnurse1})
        self.assertSetEqual(self.shiftDay.assignedNurses[1], {self.testnurse1})
        self.assertSetEqual(self.shiftDay.assignedNurses[2], {self.testnurse1})

        self.shiftDay.assignNurse(self.testnurse2)

        self.assertSetEqual(self.shiftDay.assignedNurses[0], {self.testnurse1})
        self.assertSetEqual(self.shiftDay.assignedNurses[1], {self.testnurse1, self.testnurse2})
        self.assertSetEqual(self.shiftDay.assignedNurses[2], {self.testnurse1, self.testnurse2})

    def test_assignNurse_nurse_already_assigned(self):
        self.shiftDay.assignNurse(self.testnurse1)
        with pytest.raises(Exception) as exc:
            self.shiftDay.assignNurse(self.testnurse1)

        self.assertEqual('Nurse is already assigned to this shift', str(exc.value))

    def test_removeNurse(self):
        self.shiftDay.assignNurse(self.testnurse1)
        self.shiftDay.assignNurse(self.testnurse2)

        self.shiftDay.removeNurse(self.testnurse1)
        self.assertSetEqual(self.shiftDay.assignedNurses[0], set())
        self.assertSetEqual(self.shiftDay.assignedNurses[1], {self.testnurse2})
        self.assertSetEqual(self.shiftDay.assignedNurses[2], {self.testnurse2})

        self.shiftDay.removeNurse(self.testnurse2)
        self.assertSetEqual(self.shiftDay.assignedNurses[0], set())
        self.assertSetEqual(self.shiftDay.assignedNurses[1], set())
        self.assertSetEqual(self.shiftDay.assignedNurses[2], set())

    def test_removeNurse_nurse_not_assigned(self):
        with pytest.raises(Exception) as exc:
            self.shiftDay.removeNurse(self.testnurse1)

        self.assertEqual('Nurse does not exits', str(exc.value))


if __name__ == '__main__':
    unittest.main()
