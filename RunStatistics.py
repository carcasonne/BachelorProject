import json
import time

from Domain.Models.Network.NetworkSchedule import NetworkSchedule
from Domain.Models.Tabu.TabuNurse import TabuNurse
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from NetworkFlow.StaticMethods import runNetworkFlow
from Parser.NurseParser import NurseParser
from Knapsack.KnapsackSolver import KnapsackSolver
from Spinner import Spinner
from TabuSearch.DirectedGraph import DirectedGraph
from TabuSearch.StaticMethods import evaluateCC, randomizeConstraints
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy

runs = 1
counter = 0
runToTime = {}
for i in range(runs):
    runToTime[i] = (0, "")

while counter < runs:
    print()
    print(f"---------- BEGINNING RUN NUMBER {counter + 1} ----------")

    with Spinner():
        start_time = time.time()
        useParser = False

        print("----- Beginning PARSING -----")

        parser = NurseParser()
        schedule_parsed = parser.parseScenario("n030w4")
        schedule_artificial = copy.deepcopy(TestTabuData().schedule)
        schedule = schedule_parsed if useParser else schedule_artificial

        end_parser_time = time.time()

        print("----- Beginning KNAPSACK COMPUTATIONS -----")
        schedule.nurses = schedule.nurses[:len(schedule.nurses)]
        solver = KnapsackSolver(schedule, True)
        solver.solve()
        schedule = solver.schedule

        print(f"Added {solver.bankNurseCount} bank nurses")

        print("----- Beginning TABU SEARCH -----")

        tabuSchedule = TabuSchedule(schedule)
        if not useParser:
            for nurse in tabuSchedule.nurses:
                randomizeConstraints(nurse)

        end_knapsack_time = time.time()
        search = TabuSearch_SIMPLE(tabuSchedule)
        search.initSchedule()
        search.debug = False
        search.run(1, False, False)
        end_tabu_time = time.time()

        print(f"Tabu penalty score: {search.bestSolution.PC}")

        print("----- Beginning NETWORK FLOW -----")

        solutionSchedule = runNetworkFlow(schedule, search.bestSolution)
        end_network_time = time.time()

        debugPenaltyScore = False
        if debugPenaltyScore:
            print("*** PENALTY TEST ***")
            for nurse in solutionSchedule.nurses:
                nurse.debug = True
                normalP = nurse.calculatePenalty(nurse.assignedShiftPattern)
                tabuNurse = search.bestSolution.nurses[nurse.id]
                tabuP = tabuNurse.calculatePenalty(tabuNurse.shiftPattern)
                print(f"Nurse {nurse.id}: New penalty: {normalP}, tabu penalty: {tabuP}")
                print(str(nurse.assignedShiftPattern.early))
                print(str(nurse.assignedShiftPattern.late))
                print(str(nurse.assignedShiftPattern.night))
                print(str(nurse.undesiredShifts))

    print()
    print(f"---------- RUN NUMBER {counter + 1} results ----------")

    print(solutionSchedule.getNursePatternsAsString())
    print(solutionSchedule.getScheduleRequirementsAsString())

    print(f"IS SCHEDULE VALID: {solutionSchedule.nursesFulfillContract()}!!!!!!!!!!!!!!!!!")

    time_parser_lapsed = end_parser_time - start_time
    time_knapsack_lapsed = end_knapsack_time - end_parser_time
    time_tabu_lapsed = end_tabu_time - end_knapsack_time
    time_network_lapsed = end_network_time - end_tabu_time
    total_time_elapsed = end_network_time - start_time

    print(f"Parser parsing time: {time_parser_lapsed} seconds")
    print(f"Knapsack computation time: {time_knapsack_lapsed} seconds")
    print(f"Tabu search computation time: {time_tabu_lapsed} seconds")
    print(f"Network flow computation time: {time_network_lapsed} seconds")

    print(f"Total time elapsed: {total_time_elapsed}")

    print(f"---------- END RUN NUMBER {counter + 1} ----------")
    penalty = solutionSchedule.getPenaltyScore()
    perNurse = penalty / len(solutionSchedule.nurses)
    nurseContractsFulfilled = solutionSchedule.nursesFulfillContract()
    shiftsCovered = solutionSchedule.shiftsRequirementsMet()
    runToTime[counter] = (total_time_elapsed, penalty, perNurse, nurseContractsFulfilled, shiftsCovered)
    counter = counter + 1

print(f"---------- FINAL RESULTS ----------")
for i in range(runs):
    stats = runToTime[i]
    print(f"RUN {i}: \n    "
          f"Penalty score: {stats[1]} \n    "
          f"Penalty score per nurse: {stats[2]} \n    "
          f"Computation Time: {stats[0]} seconds\n    "
          f"All nurse contracts fulfilled: {stats[3]} \n    "
          f"All shifts have minimum cover: {stats[4]}")

print()
print(f"---------- AVERAGE RESULTS ----------")
print(f"Average computation time {sum([stats[0] for stats in runToTime.values()]) / runs}")
print(f"Average penalty score {sum([stats[1] for stats in runToTime.values()]) / runs}")
print(f"Average penalty score per nurse {sum([stats[1] for stats in runToTime.values()]) / len(solutionSchedule.nurses) / runs}")

print()
print(f"---------- BEST RUN ----------")
bestTimeRunId = -1
bestTime = float('inf')
bestPenaltyRunId = -1
bestPenalty = float('inf')
for i in range(runs):
    stats = runToTime[i]
    if stats[0] < bestTime:
        bestTime = stats[0]
        bestTimeRunId = i
    if stats[1] < bestPenalty:
        bestPenalty = stats[1]
        bestPenaltyRunId = i

if bestTimeRunId == bestPenaltyRunId:
    stats = runToTime[bestTimeRunId]
    print(f"Run {bestPenaltyRunId} has the lowest penalty, and was the fastest!")
    print(f"RUN {bestTimeRunId}: \n    "
          f"Penalty score: {stats[1]} \n    "
          f"Penalty score per nurse: {stats[2]} \n    "
          f"Computation Time: {stats[0]} seconds\n    "
          f"All nurse contracts fulfilled: {stats[3]} \n    "
          f"All shifts have minimum cover: {stats[4]}")
else:
    stats = runToTime[bestTimeRunId]
    print(f"RUN {bestTimeRunId} WAS THE FASTEST")
    print(f"RUN {bestTimeRunId}: \n    "
          f"Penalty score: {stats[1]} \n    "
          f"Penalty score per nurse: {stats[2]} \n    "
          f"Computation Time: {stats[0]} seconds\n    "
          f"All nurse contracts fulfilled: {stats[3]} \n    "
          f"All shifts have minimum cover: {stats[4]}")
    print()
    stats = runToTime[bestPenaltyRunId]
    print(f"RUN {bestPenaltyRunId} HAD THE LOWEST PENALTY SCORE")
    print(f"RUN {bestPenaltyRunId}: \n    "
          f"Penalty score: {stats[1]} \n    "
          f"Penalty score per nurse: {stats[2]} \n    "
          f"Computation Time: {stats[0]} seconds\n    "
          f"All nurse contracts fulfilled: {stats[3]} \n    "
          f"All shifts have minimum cover: {stats[4]}")

print(f"Total time for {runs} runs: {sum([stats[0] for stats in runToTime.values()])}")



