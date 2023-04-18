import copy
import unittest

from Domain.Models.Network.NetworkSchedule import NetworkSchedule
from NetworkFlow.StaticMethods import *
from Tests.test_networkflow.TestNetworkFlowData import TestNetworkFlowData
from Tests.test_tabu.TestTabuData import TestTabuData


class Test_staticMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.schedule = copy.deepcopy(TestNetworkFlowData().schedule)
        self.tabuSchedule = copy.deepcopy(TestNetworkFlowData().tabuSchedule)
        self.networkSchedule = NetworkSchedule(self.tabuSchedule, self.schedule)

    def tearDown(self) -> None:
        self.schedule = copy.deepcopy(TestNetworkFlowData().schedule)
        self.tabuSchedule = copy.deepcopy(TestNetworkFlowData().tabuSchedule)
        self.networkSchedule = NetworkSchedule(self.tabuSchedule, self.schedule)

    def test_evaluation_function_for_initial_schedule_raises_exception(self):
        with self.assertRaises(Exception) as context:
            evaluationFunction(self.networkSchedule)

        self.assertTrue('Nurse 0 works day but are not assigned a StandardShiftPattern', context.exception)

    def test_EdmondsKarp_on_network_finds_min_cost_flow(self):
        pass
