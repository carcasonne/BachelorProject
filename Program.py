from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy

schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))

search = TabuSearch_SIMPLE(schedule)
search.initSchedule()
print(str(search.bestSolution))
# for n in search.bestSolution.nurses: print(str(n.id) + " PC: " + str(n.penalty))
search.run()
print(str(search.bestSolution))
# for n in search.bestSolution.nurses: print(str(n.id) + " PC: " + str(n.penalty))
