from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TestData.TabuSetup import *

ts = TabuSchedule(schedule)
print("hej")
print(str(ts))
print(str(ts.CalculateCC()))
