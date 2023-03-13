from Domain.Models.Tabu.TabuNurse import *
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.TabuSearch import TabuSearch
from TestData.TabuSetup import *

search = TabuSearch(schedule)
for s in search.currSolution.shifts:
    print(str(s))
print("Score: " + str(search.currSolution.CC))