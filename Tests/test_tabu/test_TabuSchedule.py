import unittest

from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Nurse import Nurse
from Domain.Models.Schedule import Schedule
from Domain.Models.Shift import Shift
from Domain.Models.Tabu.TabuNurse import TabuNurse
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TestData import TabuSetup


class TabuScheduleTests(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_init(self):
        pass


if __name__ == '__main__':
    unittest.main()
