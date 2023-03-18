from Domain.Models.Schedule import Schedule
from Domain.Models.Nurse import Nurse
#from Domain.Models.Shift import Shift
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Enums.Contract import Contract

from Knapsack.Problems.ItemGroup import ItemGroup
from Knapsack.Problems.BoundedKnapsack import BoundedKnapsack
from Knapsack.BranchAndBound.BranchAndBound_MODERN import BranchAndBound_MODERN

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
        self.E = self.requiredForGrade(Grade.THREE, True) # sum(shift.coverRequirements[Grade.THREE] for shift in self.schedule.shifts if shift.shiftType == ShiftType.NIGHT)
        self.D = self.requiredForGrade(Grade.THREE, False) # sum(shift.coverRequirements[Grade.THREE] for shift in self.schedule.shifts if shift.shiftType != ShiftType.NIGHT)
        #self.upperBounds = None
        #self.boundedItemGroups = None

        # This is a 'dirty' way to do it. Should be based on which kind of contracts the given nurses have
        contract1 = Contract(5, 4)
        contract2 = Contract(4, 3)
        contract3 = Contract(3, 2)

        self.contracts = [contract1, contract2, contract3]

    # Strategy consists of 3 parts:
    # 1. Find the first feasible solution above lower bound E (feasible for all grades)
    # 2. Define a new problem only accounting for grade 1 and 2, using the Z of previous solution as lower bound
    # 3. Define a new problem only accounting for grade 1 using the Z of previous solution as lower bound
    # When a feasible solution has been found for all steps, it is known for there to be a feasible solution
    # If any solution has no feasible solutions, add bank nurses
    # TODO: Also account for prefered level of coverage
    def solve(self):
        # TODO: make solution able to backtrack

        # A feasible solution for grade 3
        SOLUTION_3 = self.getOverallSolution()
        # A feasible solution for grade 2
        SOLUTION_2 = self.getGradeTwoSolution(SOLUTION_3)
        # A feasible solutino for grade 1
        SOLUTION_1 = self.getGradeOneSolution(SOLUTION_2)

        # what now????

        return SOLUTION_1       

    def getOverallSolution(self):
        # Find a feasible solution for grade 3
        SOLUTION_3 = None
        grade_three_solution_exists = False
        
        while not grade_three_solution_exists:
            upperBounds = self.getOverallUpperBounds()
            boundedItemGroups = self.createBoundedItemGroups(upperBounds)
            # The weight of the knapsack is defined by equation 6' in the article
            C_3 = self.costForBounds(upperBounds)
            lowerBound = self.E

            boundedKnapsack = BoundedKnapsack(boundedItemGroups, C_3)
            zeroOneKnapsack = boundedKnapsack.asZeroOne_simple()
            branchAndSearch = BranchAndBound_MODERN(zeroOneKnapsack)

            branchAndSearch.startSearch(lowerBound, False)
            solution = branchAndSearch.bestSolution

            # If solution.level is -1, then no feasible solution exists
            # Else we have found a solution and exit the while loop
            if solution.level == -1:
                # Add nurses equivelant to difference between lower and upper bound
                bankN = C_3 - lowerBound
                # paper doesn't mention contract of bank nurses...
                bankContract = Contract(5, 4)
                # paper doesn't mention grade of bank nurses...
                bankGrade = Grade.ONE

                newNurses = []
                for i in range(bankN):
                    bankNurse = Nurse(1000 + i, bankGrade, bankContract)
                    self.schedule.nurses.append(bankNurse)
            else:
                SOLUTION_3 = solution
                grade_three_solution_exists = True
        
        return SOLUTION_3
    
    def getGradeTwoSolution(self, previousSolution):
        lowerBound = previousSolution.Z

        Q_3 = self.getTypesFromSolution(previousSolution)
        E_2 = self.requiredForGrade(Grade.TWO, True)
        D_2 = self.requiredForGrade(Grade.TWO, False)

        N_I_G = self.getContractToGrade(self)

        # grade_2_props = self.createBoundedItemGroups(Grade.TWO)
        # grade_2_items = grade_2_props[0]
        # grade_2_bounds = grade_2_props[0]

        upperBounds = {
            self.contract1: 0,
            self.contract2: 0,
            self.contract3: 0
        }

        # Defines upper bound for each contract type
        # Some crazy ass shit going on here
        for i in range(len(self.contracts)):
            contract = self.contracts[i]
            Q_i = Q_3[contract]
            N_I_3 = N_I_G[contract][Grade.THREE]

            if Q_i <= N_I_3:
                upperBounds[contract] = N_I_G[contract][Grade.ONE] + N_I_G[contract][Grade.TWO]
            else:
                sub = Q_i - N_I_G[contract][Grade.THREE]
                upperBounds[contract] = N_I_G[contract][Grade.ONE] + N_I_G[contract][Grade.TWO] - sub
                lowerBound = E_2 - sub
            
            if Q_i < upperBounds[contract]:
                upperBounds[contract] = Q_i
        
        # Represent the problem in bounded knapsack item groups
        items = []
        for contract in self.contracts:
            profit = contract.nights
            weight = contract.days
            upperBound = upperBounds[contract]

            itemGroup = ItemGroup(profit, weight, upperBound)
            items.append(itemGroup)
        
        C_2 = self.costForBounds(upperBounds)

        # Find a feasible solution for grade 2
        SOLUTION_2 = None
        grade_two_solution_exists = False
        while not grade_two_solution_exists:
            boundedKnapsack = BoundedKnapsack(items, C_2)
            zeroOneKnapsack = boundedKnapsack.asZeroOne_simple()
            branchAndSearch = BranchAndBound_MODERN(zeroOneKnapsack)

            branchAndSearch.startSearch(lowerBound, False)
            solution = branchAndSearch.bestSolution

            # If solution.level is -1, then no feasible solution exists
            # Else we have found a solution and exit the while loop
            # Maybe also check for solution value = 0 ? 
            if solution.level == -1:
                # add extra (bank) nurses and try again
                pass
            else:
                SOLUTION_3 = solution
                grade_two_solution_exists = True
        
        return SOLUTION_2
    
    def getGradeOneSolution(self, previousSolution):
        lowerBound = previousSolution.Z

        # Nurses of type i working contract, chosen from prev solution
        Q_2 = self.getTypesFromSolution(previousSolution)
        # Grade 1 shifts needing to be covered
        E_1 = self.requiredForGrade(Grade.ONE, True)
        # Grade 1 shifts needing to be covered
        D_1 = self.requiredForGrade(Grade.ONE, False)

        # Number of nurses of grade G working contract I
        N_I_G = self.getContractToGrade(self)

        upperBounds = {
            self.contract1: 0,
            self.contract2: 0,
            self.contract3: 0
        }

        # Defines upper bound for each contract type
        # Some crazy ass shit going on here
        for i in range(len(self.contracts)):
            contract = self.contracts[i]
            Q_i = Q_2[contract]
            N_I_2 = N_I_G[contract][Grade.TWO]

            if Q_i <= N_I_2:
                upperBounds[contract] = N_I_G[contract][Grade.ONE]
            else:
                sub = Q_i - N_I_G[contract][Grade.TWO]
                upperBounds[contract] = N_I_G[contract][Grade.ONE] - sub 
                lowerBound = E_1 - sub
            
            if Q_i < upperBounds[contract]:
                upperBounds[contract] = Q_i
        
        # Represent the problem in bounded knapsack item groups
        items = []
        for contract in self.contracts:
            profit = contract.nights
            weight = contract.days
            upperBound = upperBounds[contract]

            itemGroup = ItemGroup(profit, weight, upperBound)
            items.append(itemGroup)
        
        C_1 = self.costForBounds(upperBounds)

        # Find a feasible solution for grade 2
        SOLUTION_1 = None
        grade_one_solution_exists = False
        while not grade_one_solution_exists:
            boundedKnapsack = BoundedKnapsack(items, C_1)
            zeroOneKnapsack = boundedKnapsack.asZeroOne_simple()
            branchAndSearch = BranchAndBound_MODERN(zeroOneKnapsack)

            branchAndSearch.startSearch(lowerBound, False)
            solution = branchAndSearch.bestSolution

            # If solution.level is -1, then no feasible solution exists
            # Else we have found a solution and exit the while loop
            # Maybe also check for solution value = 0 ? 
            if solution.level == -1:
                # add extra (bank) nurses and try again
                pass
            else:
                SOLUTION_1 = solution
                grade_one_solution_exists = True
        
        return SOLUTION_1
    
    # Returns a (dictionary of (contract to (dictionary of grade to (number of nurses working this contract with this grade))))
    # TODO: this is constant, make it into a self.property 
    def getContractToGrade(self):
        dicti = {}

        for contract in self.contracts:
            dicti[contract] = {
                Grade.ONE: 0,
                Grade.TWO: 0,
                Grade.THREE: 0
            }
        
        for nurse in self.schedule.nurses:
            contract = nurse.contrac
            grade = nurse.grade
            dicti[contract][grade] += 1

        return dicti

    def getOverallUpperBounds(self):
        # Quick and dirty, make it dynamic in future TODO
        upperBounds = {
            self.contracts[0]: 0,
            self.contracts[1]: 0,
            self.contracts[2]: 0
        }

        for nurse in self.schedule.nurses:
            contract = nurse.contract
            if contract.__eq__(self.contracts[0]):
                upperBounds[self.contracts[0]] += 1
            elif contract.__eq__(self.contracts[1]):
                upperBounds[self.contracts[1]] += 1
            elif contract.__eq__(self.contracts[2]):
                upperBounds[self.contracts[2]] += 1
        
        return upperBounds

    def createBoundedItemGroups(self, upperBounds):
        boundedItemGroups = []

        # Represent the problem in bounded knapsack item groups
        for contract in self.contracts:
            profit = contract.nights
            weight = contract.days
            upperBound = upperBounds[contract]

            itemGroup = ItemGroup(profit, weight, upperBound)
            boundedItemGroups.append(itemGroup)

        return boundedItemGroups

    # Returns the knapsack cost for a given grade with given upper bounds for each type of contract
    def costForBounds(self, upperBounds: dict):
        C = 0
        for i in range(len(self.contracts)):
            contract = self.contracts[i]
            d = contract.days
            n = upperBounds[contract]
            C += d * n

        C = C - self.D
        return C

    # Returns the number of shifts needed to be covered for each grade
    def requiredForGrade(self, Grade, night):
        return sum(shift.coverRequirements[Grade] for shift in self.schedule.shifts if (shift.shiftType == ShiftType.NIGHT if night else shift.shiftType != ShiftType.NIGHT))

    # Returns how many nurses of each type should work night (y_i from the paper)
    def getTypesFromSolution(self, solution:Node):
        contractToType = {
            0: 0,
            1: 0,
            2: 0
        }

        for item in solution.items:
            key = item.itemType
            contractToType[key] += 1

        return contractToType
