import json
import time

from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from Knapsack.KnapsackSolver import KnapsackSolver
from TabuSearch.DirectedGraph import DirectedGraph
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy

def time_convert(sec, str):
    print(f"{str}: {sec} seconds")

start_time = time.time()

schedule = copy.deepcopy(TestTabuData().schedule)

solver = KnapsackSolver(schedule)
solver.solve()

schedule = TabuSchedule(solver.schedule)

end_knapsack_time = time.time()

search = TabuSearch_SIMPLE(schedule)
search.initSchedule()
#print(str(search.currSolution))

search.run()

end_tabu_time = time.time()

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

time_knapsack_lapsed = end_knapsack_time - start_time
time_tabu_lapsed = end_tabu_time - end_knapsack_time
time_convert(time_knapsack_lapsed, "Knapsack computation time: ")
time_convert(time_tabu_lapsed, "Tabu search computation time: ")