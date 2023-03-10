from Domain.Models.Tabu.TabuNurse import *
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.TabuSearch import TabuSearch
from TestData.TabuSetup import *

search = TabuSearch(schedule)
print("here 1")
print(str(len(search.currSolution.nurses)))
for n in search.currSolution.nurses:
    print("ID:" + str(n.id) + "   Grade: " + str(n.grade) + "   Contract: (" + str(n.contract.days) + ", " + str(n.contract.nights) + ")")