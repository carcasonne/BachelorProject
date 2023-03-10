from Domain.Models.Tabu.TabuNurse import *
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TestData.TabuSetup import *

ts = TabuSchedule(schedule)
print(str(ts))
print(str(ts.calculateCC()))
for n in nurses:
    print("ID:" + str(n.id) + "   Grade: " + str(n.grade) + "   Contract: (" + str(n.contract.days) + ", " + str(n.contract.nights) + ")")