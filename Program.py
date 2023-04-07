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
schedule = parser.parseScenario("n030w4")
schedule.nurses = schedule.nurses[:len(schedule.nurses)//2]
#schedule = copy.deepcopy(TestTabuData().schedule)

end_parser_time = time.time()

solver = KnapsackSolver(schedule)
solver.solve()

schedule = TabuSchedule(solver.schedule)

end_knapsack_time = time.time()

search = TabuSearch_SIMPLE(schedule)
search.initSchedule()
#print(str(search.bestSolution))
#search.shiftChain(schedule)


print(str(search.bestSolution))
search.run()
end_tabu_time = time.time()
#print(str(search.bestSolution))
print(search.bestSolution.nursePatternSchedule())
print(str(search.bestSolution))


#print(search.bestSolution.scheduleTable())
print("Executed Random Descent: " + str(search.steps[0]) + " times.")
print("Executed Balance Restoration: " + str(search.steps[1]) + " times.")
print("Executed Shift Chain: " + str(search.steps[2]) + " times.")
print("Executed Nurse Chain: " + str(search.steps[3]) + " times.")
print("Executed Under Covering: " + str(search.steps[4]) + " times.")
print("Executed Random Kick: " + str(search.steps[5]) + " times.")

print("\n")

time_parser_lapsed = end_parser_time - start_time
time_knapsack_lapsed =  end_knapsack_time - end_parser_time
time_tabu_lapsed = end_tabu_time - end_knapsack_time
time_convert(time_parser_lapsed, "Parser parsing time: ")
time_convert(time_knapsack_lapsed, "Knapsack computation time: ")
time_convert(time_tabu_lapsed, "Tabu search computation time: ")