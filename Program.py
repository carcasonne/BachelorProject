import json

from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.DirectedGraph import DirectedGraph
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy

# schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))

# search = TabuSearch_SIMPLE(schedule)
# search.initSchedule()

# search.shiftChain(schedule)


# print(str(search.bestSolution))
# search.run()
#print(str(search.bestSolution))

g = DirectedGraph()

g.addNode(0)
g.addNode(1)
g.addNode(2)
g.addNode(3)

g.addEdge(0, 1, 0, 5)
g.addEdge(0, 2, 0, 3)
g.addEdge(1, 2, 1, -3)
g.addEdge(2, 1, 1, -5)
g.addEdge(3, 1, 2, -5)
g.addEdge(3, 2, 2, 15)

print(str(g))