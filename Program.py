from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy

schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))

search = TabuSearch_SIMPLE(schedule)
print(str(search.bestSolution))
search.run()
evaluateCC(search.bestSolution)
print(str(search.bestSolution))