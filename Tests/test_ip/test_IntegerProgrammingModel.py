import copy
import unittest

from IntegerProgramming.IP import IntegerProgrammingModel
from NetworkFlow.StaticMethods import runNetworkFlow
from Tests.test_networkflow.TestNetworkFlowData import TestNetworkFlowData


class TestIntegerProgrammingModel(unittest.TestCase):
    def setUp(self) -> None:
        data = TestNetworkFlowData()
        self.tabuSchedule = data.tabuSchedule
        self.schedule = data.schedule

    def tearDown(self) -> None:
        data = TestNetworkFlowData()
        self.tabuSchedule = data.tabuSchedule
        self.schedule = data.schedule

    def test_buildFinalSolution_has_better_penalty_score(self):
        before = copy.copy(self.tabuSchedule.PC)
        newSchedule = IntegerProgrammingModel(self.schedule, self.tabuSchedule).buildFinalSchedule()
        after = newSchedule.getPenaltyScore()
        self.assertTrue(before > after)

    def test_ip_vs_network(self):
        ipSchedule = IntegerProgrammingModel(copy.deepcopy(self.schedule),
                                             copy.deepcopy(self.tabuSchedule)).buildFinalSchedule()
        ipPC = ipSchedule.getPenaltyScore()
        networkSchedule = runNetworkFlow(copy.deepcopy(self.schedule), copy.deepcopy(self.tabuSchedule))
        nfPC = networkSchedule.getPenaltyScore()
        print(ipSchedule.getScheduleRequirementsAsString())
        print(networkSchedule.getScheduleRequirementsAsString())
        self.assertTrue(nfPC == ipPC)
