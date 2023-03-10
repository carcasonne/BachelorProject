from Domain.Models.Tabu.TabuNurse import *
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TestData.TabuSetup import *

ts = TabuSchedule(schedule)
print(str(ts))
print(str(ts.calculateCC()))
