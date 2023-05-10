import json
import time

from Domain.Models.Network.NetworkSchedule import NetworkSchedule
from Domain.Models.Tabu.TabuNurse import TabuNurse
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from IntegerProgramming.IP import IntegerProgrammingModel
from NetworkFlow.StaticMethods import runNetworkFlow
from Parser.NurseParser import NurseParser
from Knapsack.KnapsackSolver import KnapsackSolver
from Spinner import Spinner
from TabuSearch.DirectedGraph import DirectedGraph
from TabuSearch.StaticMethods import evaluateCC, randomizeConstraints
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy
from openpyxl import Workbook

# Excel stuff
workbook = Workbook()
sheet = workbook.active
sheet.title = "Overview"
sheet["A1"] = "Number of runs"
sheet["A2"] = "Best run id"
sheet["A3"] = "Fastest run id"
sheet["A4"] = "Average run time"
sheet["A5"] = "Average penalty score"
sheet["A6"] = "Average pc/nurse time"

sheet["A8"] = "Run Id"
sheet["B8"] = "Run PC"
sheet["C8"] = "Run PC/Nurse"
sheet["D8"] = "Run Time"
sheet["E8"] = "Contracts Fulfilled"
sheet["F8"] = "Shifts Covered"
sheet["G8"] = "IP better than Network Flow"

overviewStartCell = 9

runs = 10
runsIpBetter = 0
runsIpWorse = 0
counter = 0
runToTime = {}
for i in range(runs):
    runToTime[i] = (0, "")

bestSolution = None

while counter < runs:
    runWorkSheet = workbook.create_sheet(f'RUN {counter}')
    runWorkSheet["A1"] = "Iteration"
    runWorkSheet["B1"] = "CC"
    runWorkSheet["C1"] = "PC"
    runWorkSheet["D1"] = "IsPhase1"

    print()
    print(f"---------- BEGINNING RUN NUMBER {counter + 1} ----------")

    with Spinner():
        start_time = time.time()
        useParser = True

        print("----- Beginning PARSING -----")
        if useParser:
            parser = NurseParser()
            schedule = parser.parseScenario("n005w4")
        else:
            schedule = copy.deepcopy(TestTabuData().schedule)

        end_parser_time = time.time()

        print("----- Beginning KNAPSACK COMPUTATIONS -----")
        schedule.nurses = schedule.nurses[:len(schedule.nurses)]
        solver = KnapsackSolver(schedule, True)
        solver.debug = False
        solver.solve()
        schedule = solver.schedule

        print(f"Added {solver.bankNurseCount} bank nurses")
        print(f"Total nurses: {len(schedule.nurses)}")
        print("----- Beginning TABU SEARCH -----")

        tabuSchedule = TabuSchedule(schedule)
        if not useParser:
            for nurse in tabuSchedule.nurses:
                randomizeConstraints(nurse)

        end_knapsack_time = time.time()
        search = TabuSearch_SIMPLE(tabuSchedule)
        search.initSchedule()
        search.excelSheet = runWorkSheet
        search.run(1, False, False)
        end_tabu_time = time.time()

        print(f"Tabu penalty score: {search.bestSolution.PC}")

        print("----- Beginning INTEGER PROGRAMMING MODEL -----")
        betterSolutionSchedule = IntegerProgrammingModel(copy.deepcopy(schedule),
                                                         copy.deepcopy(search.bestSolution)).buildFinalSchedule()
        end_IP_time = time.time()
        # print(betterSolutionSchedule.getScheduleRequirementsAsString())

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

    print("XOXOX ", str(betterSolutionSchedule.getPenaltyScore()), " vs ", str(solutionSchedule.getPenaltyScore()),
          " XOXOX")

    if bestSolution is None or bestSolution.getPenaltyScore() > solutionSchedule.getPenaltyScore():
        bestSolution = solutionSchedule

    difference = betterSolutionSchedule.getPenaltyScore() - solutionSchedule.getPenaltyScore()
    ipIsBetter = 0
    if difference < 0:
        runsIpWorse = runsIpWorse + 1
        ipIsBetter = -1
    elif difference > 0:
        runsIpBetter = runsIpBetter + 1
        ipIsBetter = 1

    print(f"---------- RUN NUMBER {counter + 1} results ----------")

    # print(solutionSchedule.getNursePatternsAsString())
    # print(solutionSchedule.getScheduleRequirementsAsString())

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
    runToTime[counter] = (total_time_elapsed, penalty, perNurse, nurseContractsFulfilled, shiftsCovered, ipIsBetter)
    counter = counter + 1

    sheet[f"A{overviewStartCell + counter}"] = counter
    sheet[f"B{overviewStartCell + counter}"] = penalty
    sheet[f"C{overviewStartCell + counter}"] = perNurse
    sheet[f"D{overviewStartCell + counter}"] = total_time_elapsed
    sheet[f"E{overviewStartCell + counter}"] = nurseContractsFulfilled
    sheet[f"F{overviewStartCell + counter}"] = shiftsCovered
    sheet[f"G{overviewStartCell + counter}"] = ipIsBetter

print(f"---------- FINAL RESULTS ----------")
for i in range(runs):
    stats = runToTime[i]
    print(f"RUN {i}: \n    "
          f"Penalty score: {stats[1]} \n    "
          f"Penalty score per nurse: {stats[2]} \n    "
          f"Computation Time: {stats[0]} seconds\n    "
          f"All nurse contracts fulfilled: {stats[3]} \n    "
          f"All shifts have minimum cover: {stats[4]} \n    "
          f"IP better than network flow: {stats[5]}")

averageComputationTime = sum([stats[0] for stats in runToTime.values()]) / runs
averagePenaltyScore = sum([stats[1] for stats in runToTime.values()]) / runs
averagePenaltyScorePerNurse = sum([stats[1] for stats in runToTime.values()]) / len(solutionSchedule.nurses) / runs
print()
print(f"---------- AVERAGE RESULTS ----------")
print(f"Average computation time {averageComputationTime}")
print(f"Average penalty score {averagePenaltyScore}")
print(
    f"Average penalty score per nurse {averagePenaltyScorePerNurse}")

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
    print(f"Run {bestPenaltyRunId + 1} has the lowest penalty, and was the fastest!")
    print(f"RUN {bestTimeRunId + 1}: \n    "
          f"Penalty score: {stats[1]} \n    "
          f"Penalty score per nurse: {stats[2]} \n    "
          f"Computation Time: {stats[0]} seconds\n    "
          f"All nurse contracts fulfilled: {stats[3]} \n    "
          f"All shifts have minimum cover: {stats[4]} \n    "
          f"IP better than network flow: {stats[5]}")
else:
    stats = runToTime[bestTimeRunId]
    print(f"RUN {bestTimeRunId + 1} WAS THE FASTEST")
    print(f"RUN {bestTimeRunId + 1}: \n    "
          f"Penalty score: {stats[1]} \n    "
          f"Penalty score per nurse: {stats[2]} \n    "
          f"Computation Time: {stats[0]} seconds\n    "
          f"All nurse contracts fulfilled: {stats[3]} \n    "
          f"All shifts have minimum cover: {stats[4]} \n    "
          f"IP better than network flow: {stats[5]}")
    print()
    stats = runToTime[bestPenaltyRunId]
    print(f"RUN {bestPenaltyRunId + 1} HAD THE LOWEST PENALTY SCORE")
    print(f"RUN {bestPenaltyRunId + 1}: \n    "
          f"Penalty score: {stats[1]} \n    "
          f"Penalty score per nurse: {stats[2]} \n    "
          f"Computation Time: {stats[0]} seconds\n    "
          f"All nurse contracts fulfilled: {stats[3]} \n    "
          f"All shifts have minimum cover: {stats[4]} \n    "
          f"IP better than network flow: {stats[5]}")

print(f"Total time for {runs} runs: {sum([stats[0] for stats in runToTime.values()])}")
print(f"Number of runs: {runs}: \n   "
      f"Runs where IP was better: {runsIpBetter} ({(runsIpBetter / runs) * 100}%) \n   "
      f"Runs where IP was worse: {runsIpWorse} ({(runsIpWorse / runs) * 100}%) \n   "
      f"Runs with same penalty score: {runs - runsIpWorse - runsIpBetter} ({((runs - runsIpWorse - runsIpBetter) / runs) * 100}%)")

print(bestSolution.getNursePatternsAsString())
print(bestSolution.getScheduleRequirementsAsString())
print(f"Total time for {runs} runs: {sum([stats[0] for stats in runToTime.values()])}")
print(f"Added {solver.bankNurseCount} bank nurses")
print("Best solution printed")

# Save everything to excel file
sheet["B1"] = runs
sheet["B2"] = bestPenaltyRunId + 1
sheet["B3"] = bestTimeRunId + 1
sheet["B4"] = averageComputationTime
sheet["B5"] = averagePenaltyScore
sheet["B6"] = averagePenaltyScorePerNurse
workbook.save(filename="RunStatisticsResults.xlsx")
