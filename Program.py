from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE
from Tests.test_tabu.TestTabuData import TestTabuData
import copy

schedule = TabuSchedule(copy.deepcopy(TestTabuData().schedule))

search = TabuSearch_SIMPLE(schedule)
for s in search.bestSolution.shifts:
    print(str(s))
print("Score: " + str(search.bestSolution.CC))
search.run()
evaluateCC(search.bestSolution)
for s in search.bestSolution.shifts:
    print(str(s))
print("Score: " + str(search.bestSolution.CC))