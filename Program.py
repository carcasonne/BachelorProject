import json

from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from Knapsack.KnapsackSolver import KnapsackSolver
from TabuSearch.DirectedGraph import DirectedGraph
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy

schedule = copy.deepcopy(TestTabuData().schedule)

solver = KnapsackSolver(schedule)
solver.solve()

schedule = TabuSchedule(solver.schedule)

search = TabuSearch_SIMPLE(schedule)
search.initSchedule()
#print(str(search.bestSolution))
#search.shiftChain(schedule)

print(str(search.bestSolution))
search.run()
print(str(search.bestSolution))