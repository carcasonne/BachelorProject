import unittest
import pytest

from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import TabuShiftType
from Domain.Models.Nurse import Nurse
from Domain.Models.Tabu.TabuNurse import TabuNurse
from Domain.Models.Tabu.TabuShift import TabuShift


class Test_TabuShiftTests(unittest.TestCase):

    def setUp(self) -> None:
        self.shiftDay = TabuShift({Grade.ONE.name: 1, Grade.TWO: 2, Grade.THREE: 3}, TabuShiftType.DAY, Days.MONDAY)
        self.shiftNight = TabuShift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, TabuShiftType.DAY, Days.MONDAY)
        self.n1 = TabuNurse(Nurse(0, Grade.ONE, Contract(5, 4)))
        self.n2 = TabuNurse(Nurse(1, Grade.TWO, Contract(3, 2)))

    def tearDown(self) -> None:
        self.shiftDay.assignedNurses = {Grade.ONE: set(), Grade.TWO: set(), Grade.THREE: set()}
        self.shiftNight.assignedNurses = {Grade.ONE: set(), Grade.TWO: set(), Grade.THREE: set()}

    def test_init_sets_all_correct_parameters(self):
        shiftDay = TabuShift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, TabuShiftType.DAY, Days.MONDAY)
        shiftNight = TabuShift({Grade.ONE: 1, Grade.TWO: 2, Grade.THREE: 3}, TabuShiftType.NIGHT, Days.TUESDAY)

        for grade in shiftDay.coverRequirements.keys():
            self.assertEqual(grade.value, shiftDay.coverRequirements.get(grade))
        for grade in shiftNight.coverRequirements.keys():
            self.assertEqual(grade.value, shiftNight.coverRequirements.get(grade))
        self.assertEqual(TabuShiftType.DAY, shiftDay.shiftType)
        self.assertEqual(TabuShiftType.NIGHT, shiftNight.shiftType)
        self.assertEqual(Days.MONDAY, shiftDay.shiftDay)
        self.assertEqual(Days.TUESDAY, shiftNight.shiftDay)

    def test_assign_nurse_grade1_to_shift_changes_field_nurses_assigned(self):
        self.shiftDay.addNurse(self.n1)
        self.assertEqual(True, (self.n1.id in self.shiftDay.assignedNurses[Grade.ONE]))
        self.assertEqual(True, (self.n1.id in self.shiftDay.assignedNurses[Grade.TWO]))
        self.assertEqual(True, (self.n1.id in self.shiftDay.assignedNurses[Grade.THREE]))

    def test_assign_nurse_grade2_to_shift_changes_field_nurses_assigned(self):
        self.shiftDay.addNurse(self.n2)
        self.assertEqual(False, (self.n2.id in self.shiftDay.assignedNurses[Grade.ONE]))
        self.assertEqual(True, (self.n2.id in self.shiftDay.assignedNurses[Grade.TWO]))
        self.assertEqual(True, (self.n2.id in self.shiftDay.assignedNurses[Grade.THREE]))

    def test_remove_nurse_from_shift_changes_field_nurses_assigned(self):
        self.shiftDay.addNurse(self.n1)
        self.shiftDay.removeNurse(self.n1)
        self.assertEqual(False, (self.n1.id in self.shiftDay.assignedNurses[Grade.ONE]))
        self.assertEqual(False, (self.n1.id in self.shiftDay.assignedNurses[Grade.TWO]))
        self.assertEqual(False, (self.n1.id in self.shiftDay.assignedNurses[Grade.THREE]))

    # TODO : Test remove not assigned nurse -> Execption
    # TODO : Test add already assigned nurse -> Exception

if __name__ == '__main__':
    unittest.main()
