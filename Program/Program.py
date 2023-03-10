from Parser.NurseParser import *
from Knapsack.SimpleKnapsackModel import *
from TabuSearch.TabuSearch import *
from NetworkFlow.NetworkFlow import *

tabuSearch = Class1TabuSearch()
networkFlow = Class1NetworkFlow()

print("Beginning")

print("Parsing")

parser = NurseParser()
schedule = parser.parseFromTxt("Hej med dig")

# Print alle de nurses vi har nu
print("Parsed nurses:")

for nurse in schedule.nurses:
    nurse.print()

print("Running through knapsack...")

knapsackModel = SimpleKnapsackModel(schedule)
feasibleNurses = knapsackModel.searchTree()

print("Tabu searching...")
tabuSearch.print()

print("Network flowing...")
networkFlow.print()

print("Done")



