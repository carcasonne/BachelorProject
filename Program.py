import json
import time

from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from Parser.NurseParser import NurseParser
from Knapsack.KnapsackSolver import KnapsackSolver
from TabuSearch.DirectedGraph import DirectedGraph
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy

def time_convert(sec, str):
    print(f"{str}: {sec} seconds")

start_time = time.time()

parser = NurseParser()
schedule_parsed = parser.parseScenario("n030w4")
schedule_artificial = copy.deepcopy(TestTabuData().schedule)

end_parser_time = time.time()

# schedule_parsed.shifts = schedule_artificial.shifts
# schedule_parsed.nurses = schedule_artificial.nurses

solver = KnapsackSolver(schedule_artificial)
solver.solve()

schedule = TabuSchedule(solver.schedule)

end_knapsack_time = time.time()

search = TabuSearch_SIMPLE(schedule)
search.initSchedule()
#print(str(search.currSolution))

search.run()
end_tabu_time = time.time()
print(search.bestSolution.nursePatternSchedule())
print(str(search.bestSolution))

#print(search.currSolution.scheduleTable())
print("Executed P1 Random Descent: " + str(search.stepsP1[0]) + " times.")
print("Executed P1 Balance Restoration: " + str(search.stepsP1[1]) + " times.")
print("Executed P1 Shift Chain: " + str(search.stepsP1[2]) + " times.")
print("Executed P1 Nurse Chain: " + str(search.stepsP1[3]) + " times.")
print("Executed P1 Under Covering: " + str(search.stepsP1[4]) + " times.")
print("Executed P1 Random Kick: " + str(search.stepsP1[5]) + " times.")

print("\n")

print("Executed P2 Random Descent: " + str(search.stepsP2[0]) + " times.")
print("Executed P2 Shift Chain: " + str(search.stepsP2[1]) + " times.")
print("Executed P2 Nurse Chain: " + str(search.stepsP2[2]) + " times.")

print("\n")

print("Executed P3 Search Stuck: " + str(search.stepsP3[0]) + " times.")

print("\n")

print("Total iterations: " + str(sum(search.stepsP1) + sum(search.stepsP2) + sum(search.stepsP3)) + ".")

print("\n")

time_parser_lapsed = end_parser_time - start_time
time_knapsack_lapsed = end_knapsack_time - end_parser_time
time_tabu_lapsed = end_tabu_time - end_knapsack_time
time_convert(time_parser_lapsed, "Parser parsing time: ")
time_convert(time_knapsack_lapsed, "Knapsack computation time: ")
time_convert(time_tabu_lapsed, "Tabu search computation time: ")