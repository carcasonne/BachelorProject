import copy
import unittest

from NetworkFlow.StaticMethods import *
from Tests.test_networkflow.TestNetworkFlowData import TestNetworkFlowData
from Tests.test_tabu.TestTabuData import TestTabuData


class Test_staticMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.schedule = copy.deepcopy(TestNetworkFlowData().schedule)
        self.tabuSchedule = copy.deepcopy(TestNetworkFlowData().tabuSchedule)

    def tearDown(self) -> None:
        self.schedule = copy.deepcopy(TestNetworkFlowData().schedule)
        self.tabuSchedule = copy.deepcopy(TestNetworkFlowData().tabuSchedule)

    def test_evaluation_function_for_schedule_returns_not_0(self):
        result = evaluationFunction(self.tabuSchedule, self.schedule)

        self.assertTrue(0 < result)
        self.assertEqual(29*10, result)