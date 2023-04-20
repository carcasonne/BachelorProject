import json
import time

from Domain.Models.Network.NetworkSchedule import NetworkSchedule
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from NetworkFlow.StaticMethods import runNetworkFlow
from Parser.NurseParser import NurseParser
from Knapsack.KnapsackSolver import KnapsackSolver
from Spinner import Spinner
from TabuSearch.DirectedGraph import DirectedGraph
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy

with Spinner():
    start_time = time.time()

    parser = NurseParser()
    schedule_parsed = parser.parseScenario("n030w4")
    schedule_artificial = copy.deepcopy(TestTabuData().schedule)
    schedule = schedule_parsed

    end_parser_time = time.time()

    # schedule_parsed.shifts = schedule_artificial.shifts
    # schedule_parsed.nurses = schedule_artificial.nurses

    solver = KnapsackSolver(schedule)
    solver.solve()

    tabuSchedule = TabuSchedule(solver.schedule)

    end_knapsack_time = time.time()

    search = TabuSearch_SIMPLE(tabuSchedule)
    search.initSchedule()
    search.debug = False
    search.run(1, False, False)
    end_tabu_time = time.time()

    solutionSchedule = runNetworkFlow(schedule, search.bestSolution)
    end_network_time = time.time()


print(solutionSchedule.getNursePatternsAsString())
print(solutionSchedule.getScheduleRequirementsAsString())

time_parser_lapsed = end_parser_time - start_time
time_knapsack_lapsed = end_knapsack_time - end_parser_time
time_tabu_lapsed = end_tabu_time - end_knapsack_time
time_network_lapsed = end_network_time - end_tabu_time

print(f"Parser parsing time: {time_parser_lapsed} seconds")
print(f"Knapsack computation time: {time_knapsack_lapsed} seconds")
print(f"Tabu search computation time: {time_tabu_lapsed} seconds")
print(f"Network flow computation time: {time_network_lapsed} seconds")
