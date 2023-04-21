import copy
import unittest

from Domain.Models.Network.NetworkSchedule import NetworkSchedule
from NetworkFlow.StaticMethods import *
from Tests.test_networkflow.TestNetworkFlowData import TestNetworkFlowData
from Tests.test_networkflow.TestNetworkFlowData_Simple import TestNetworkFlowData_Simple
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

    def test_bullshit(self):
        networkSchedule = self.networkSchedule
        solution = runNetworkFlow(self.schedule, self.tabuSchedule)
        print(solution.getNursePatternsAsString())
        print(solution.getScheduleRequirementsAsString())

        valid = solution.isValid()
        print(f"All nurses are working as many shifts as contract says: {valid}")
        hej = 1


    def test_EdmondsKarp_on_network_finds_flow(self):
        network = BoundedNetworkFlow(self.networkSchedule)
        flow = EdmondsKarp(network)

        self.assertTrue(flow > 0)

    def test_EdmondsKarp_finds_optimal_solution_for_simple_schedule(self):
        (schedule, tabuSchedule, networkSchedule) = self._get_network_2_nurses_2_days_schedule()
        networkSchedule.nurses[0].undesiredShifts[1] = 2
        network = BoundedNetworkFlow(networkSchedule)
        flow = EdmondsKarp(network)

        # Only 1 nurse should work early
        #self.assertEqual(1, flow)

        # See if nurses are working early or late
        assignment = network.nurseAssignment()

        # Optimal solution is when:
        # nurse 0 works early monday, late tuesday: 1, 0
        # nurse 1 works late monday, late tuesday:  0, 0
        nurse_0 = networkSchedule.nurses[0]
        nurse_1 = networkSchedule.nurses[1]

        self.assertEqual(assignment[nurse_0][Days.MONDAY], 1)
        self.assertEqual(assignment[nurse_0][Days.TUESDAY], 0)
        self.assertEqual(assignment[nurse_1][Days.MONDAY], 0)
        self.assertEqual(assignment[nurse_1][Days.TUESDAY], 0)

        solutionSchedule = buildFinalSchedule(schedule, tabuSchedule, network)

        hej = 1

    def _get_network_2_nurses_2_days_schedule(self):
        schedule = copy.deepcopy(TestNetworkFlowData_Simple().schedule)
        tabuSchedule = copy.deepcopy(TestNetworkFlowData_Simple().tabuSchedule)
        networkSchedule = NetworkSchedule(tabuSchedule, schedule)
        return schedule, tabuSchedule, networkSchedule
