import json

from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from Knapsack.KnapsackSolver import KnapsackSolver
from TabuSearch.DirectedGraph import DirectedGraph
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy

#schedule = copy.deepcopy(TestTabuData().schedule)

#solver = KnapsackSolver(schedule)
#solver.solve()

#schedule = TabuSchedule(solver.schedule)

#search = TabuSearch_SIMPLE(schedule)
#search.initSchedule()

#search.shiftChain(schedule)


#print(str(search.bestSolution))
#search.run()
#print(str(search.bestSolution))

graph = DirectedGraph()
graph.addNode(0)
graph.addNode(1)
graph.addNode(2)
graph.addNode(3)

graph.addEdge(0, 1, 0, 0)
graph.addEdge(0, 2, 0, -10)
graph.addEdge(0, 3, 0, 10)
graph.addEdge(1, 2, 0, 10)
graph.addEdge(1, 3, 0, -10)
graph.addEdge(2, 3, 0, -20)
graph.addEdge(1, 0, 0, -20)
graph.addEdge(2, 1, 0, -20)
graph.addEdge(3, 1, 0, -20)

graph.search(0, 3)