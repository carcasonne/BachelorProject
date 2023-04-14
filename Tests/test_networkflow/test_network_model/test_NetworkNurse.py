import copy
import unittest

from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Network.NetworkNurse import NetworkNurse
from Domain.Models.Nurse import Nurse
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuNurse import TabuNurse
from NetworkFlow.StaticMethods import *
from Tests.test_networkflow.TestNetworkFlowData import TestNetworkFlowData
from Tests.test_tabu.TestTabuData import TestTabuData


class Test_NetworkNurse(unittest.TestCase):

    def setUp(self) -> None:
        self.schedule = copy.deepcopy(TestNetworkFlowData().schedule)
        self.tabuSchedule = copy.deepcopy(TestNetworkFlowData().tabuSchedule)
        self.networkNurse0 = NetworkNurse(copy.deepcopy(self.tabuSchedule.nurses[0]),
                                          copy.deepcopy(self.schedule.nurses[0]))
        self.networkNurse1 = NetworkNurse(copy.deepcopy(self.tabuSchedule.nurses[1]),
                                          copy.deepcopy(self.schedule.nurses[1]))
        self.networkNurse2 = NetworkNurse(copy.deepcopy(self.tabuSchedule.nurses[2]),
                                          copy.deepcopy(self.schedule.nurses[2]))

    def tearDown(self) -> None:
        self.schedule = copy.deepcopy(TestNetworkFlowData().schedule)
        self.tabuSchedule = copy.deepcopy(TestNetworkFlowData().tabuSchedule)
        self.networkNurse0 = NetworkNurse(copy.deepcopy(self.tabuSchedule.nurses[0]),
                                          copy.deepcopy(self.schedule.nurses[0]))
        self.networkNurse1 = NetworkNurse(copy.deepcopy(self.tabuSchedule.nurses[1]),
                                          copy.deepcopy(self.schedule.nurses[1]))
        self.networkNurse2 = NetworkNurse(copy.deepcopy(self.tabuSchedule.nurses[2]),
                                          copy.deepcopy(self.schedule.nurses[2]))

    # ----------------------- init(tabuNurse, nurse) ---------------------------
    def test_init_coverts_correct_fields(self):
        nurse = Nurse(0, Grade.ONE, Contract(5, 4))
        nurse.undesiredShifts = ([1, 0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1])
        nurse.completeWeekend = True
        tabuNurse = TabuNurse(nurse)
        tabuNurse.shiftPattern = TabuShiftPattern([0, 1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0])
        tabuNurse.worksNight = False
        networkNurse = NetworkNurse(tabuNurse, nurse)
        self.assertEqual({Days.TUESDAY, Days.WEDNESDAY, Days.THURSDAY, Days.FRIDAY, Days.SATURDAY}, networkNurse.daySet)
        self.assertEqual(networkNurse.id, tabuNurse.id)
        self.assertEqual(networkNurse.id, nurse.id)
        self.assertEqual(True, networkNurse.completeWeekend)
        self.assertEqual(([1, 0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1]), networkNurse.undesiredShifts)
        self.assertEqual([1, 0, 0, -1, 0, 0, 0], networkNurse.shiftPreference)

    # ----------------------- preference(self, day) ---------------------------
    def test_preference_for_nurse0_day_6_returns_negative_1(self):
        result = self.networkNurse0.preference(Days.SUNDAY)
        self.assertEqual(-1, result)

    def test_preference_for_nurse0_day_5_returns_1(self):
        result = self.networkNurse0.preference(Days.SATURDAY)
        self.assertEqual(1, result)

    def test_preference_for_nurse1_day_0_5_6_returns_negative_1(self):
        self.assertEqual(-1, self.networkNurse1.preference(Days.MONDAY))
        self.assertEqual(-1, self.networkNurse1.preference(Days.SATURDAY))
        self.assertEqual(-1, self.networkNurse1.preference(Days.SUNDAY))

    def test_preference_for_nurse1_day_3_returns_0(self):
        self.assertEqual(0, self.networkNurse1.preference(Days.THURSDAY))

    def test_preference_for_nurse2_all_days_returns_0(self):
        self.assertEqual(0, self.networkNurse2.preference(Days.MONDAY))
        self.assertEqual(0, self.networkNurse2.preference(Days.TUESDAY))
        self.assertEqual(0, self.networkNurse2.preference(Days.WEDNESDAY))
        self.assertEqual(0, self.networkNurse2.preference(Days.THURSDAY))
        self.assertEqual(0, self.networkNurse2.preference(Days.FRIDAY))
        self.assertEqual(0, self.networkNurse2.preference(Days.SATURDAY))
        self.assertEqual(0, self.networkNurse2.preference(Days.SUNDAY))

    # ----------------------- calculateUpperBound(self) ---------------------------
    def test_calculate_upper_bound_nurse0_return_5(self):
        self.assertEqual(5, self.networkNurse0.calculateUpperBound())

    def test_calculate_upper_bound_nurse1_return_3(self):
        self.assertEqual(3, self.networkNurse1.calculateUpperBound())

    def test_calculate_upper_bound_nurse2_return_4(self):
        self.assertEqual(4, self.networkNurse2.calculateUpperBound())

    # ----------------------- calculateLowerBound(self) ---------------------------
    def test_calculate_lower_bound_nurse0_return_0(self):
        self.assertEqual(0, self.networkNurse0.calculateLowerBound())

    def test_calculate_lower_bound_nurse1_return_0(self):
        self.assertEqual(0, self.networkNurse1.calculateLowerBound())

    def test_calculate_lower_bound_nurse2_return_0(self):
        self.assertEqual(0, self.networkNurse2.calculateLowerBound())
