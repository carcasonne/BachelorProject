from Domain.Models.Tabu.TabuNurse import *
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.TabuSearch import TabuSearch
from TestData.TabuSetup import *

search = TabuSearch(schedule)
for s in search.bestSolution.shifts:
    print(str(s))
print("Score: " + str(search.bestSolution.CC))
search.run()
for s in search.bestSolution.shifts:
    print(str(s))
print("Score: " + str(search.bestSolution.CC))