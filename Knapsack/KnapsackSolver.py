from Domain.Models.Schedule import Schedule
#from Domain.Models.Shift import Shift
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Enums.Contract import Contract

from Knapsack.Problems.ItemGroup import ItemGroup

from Knapsack.BranchAndBound.BranchAndBound_MODERN import Node

# The KnapsackSolver takes a schedule and determines if it is feasible.
# If it is not, it adds bank nurses untill it is
class KnapsackSolver:
    # schedule: The schedule to be solved
    # E: The amount of night shifts which need to be worked
    # D: The amount of days shifts which need to be worked
    # upperBounds: The amount of nurses working each contract (N_i in the article)
    def __init__(self, schedule: Schedule):
        self.schedule = Schedule(schedule.shifts.copy(), schedule.nurses.copy())
        self.E = sum(shift.coverRequirements[Grade.THREE] for shift in self.schedule.shifts if shift.shiftType == ShiftType.NIGHT)
        self.D = sum(shift.coverRequirements[Grade.THREE] for shift in self.schedule.shifts if shift.shiftType != ShiftType.NIGHT)
        self.upperBounds = None
        self.boundedItemGroups = self.createBoundedKnapsack()


    def solve(self):
        pass

    def createBoundedKnapsack(self):
        # This is a 'dirty' way to do it. Should be based on which kind of contracts the given nurses have
        contract1 = Contract(4, 5)
        contract2 = Contract(3, 4)
        contract3 = Contract(3, 2)

        self.upperBounds = {
            contract1: 0,
            contract2: 0,
            contract3: 0
        }

        for nurse in self.schedule.nurses:
            contract = nurse.contract
            if contract.__eq__(contract1):
                self.upperBounds[contract1] += 1
            elif contract.__eq__(contract2):
                self.upperBounds[contract2] += 1
            elif contract.__eq__(contract3):
                self.upperBounds[contract3] += 1

        contracts = [contract1, contract2, contract3]
        boundedItemGroups = []

        # Represent the problem in bounded knapsack item groups
        for contract in contracts:
            profit = contract.nights
            weight = contract.days
            upperBound = self.upperBounds[contract]

            itemGroup = ItemGroup(profit, weight, upperBound)
            boundedItemGroups.append(itemGroup)

        return boundedItemGroups

    # Returns the number of shifts needed to be covered for each grade
    def requiredForGrade(self, Grade, night):
        return sum(shift.coverRequirements[Grade.THREE] for shift in self.schedule.shifts if (shift.shiftType == ShiftType.NIGHT if night else shift.shiftType != ShiftType.NIGHT))

    # Returns how many nurses of each type should work night (y_i from the paper)
    def getTypesFromSolution(self, solution:Node):
        pass
