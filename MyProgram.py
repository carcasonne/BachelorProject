from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from Parser.NurseParser import NurseParser


scenario = "n030w4"
parser = NurseParser()
schedule = parser.parseScenario(scenario)

ts = TabuSchedule(schedule)
print(str(ts))
print(str(ts.CalculateCC()))
