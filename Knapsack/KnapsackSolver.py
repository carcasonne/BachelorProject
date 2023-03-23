from Domain.Models.Schedule import Schedule
from Domain.Models.Nurse import Nurse
#from Domain.Models.Shift import Shift
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Enums.Contract import Contract

from Knapsack.Problems.KnapsackItem import KnapsackItem
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
        self.globalC = 0

        # This is a 'dirty' way to do it. Should be based on which kind of contracts the given nurses have
        # TODO: dont hardcode this
        contract1 = Contract(5, 4)
        contract2 = Contract(4, 3)
        contract3 = Contract(3, 2)

        self.contracts = [contract1, contract2, contract3]
        # paper doesn't mention contract of bank nurses...
        # paper doesn't mention grade of bank nurses...
        self.bankNurseContract = contract3
        self.bankNurseGrade = Grade.ONE
        self.bankNurseCount = 0

    # Strategy consists of 3 parts:
    # 1. Find the first feasible solution above lower bound E (feasible for all grades)
    # 2. Define a new problem only accounting for grade 1 and 2, using the Z of previous solution as lower bound
    # 3. Define a new problem only accounting for grade 1 using the Z of previous solution as lower bound
    # When a feasible solution has been found for all steps, it is known for there to be a feasible solution
    # If any solution has no feasible solutions, add bank nurses
    # TODO: Also account for prefered level of coverage
    def solve(self):
        # TODO: VERY IMPORTANT! MAKE SOLUTION 2 AND 1 FINDERS ABLE TO ADD BANK NURSES AS NEEDED

        # A feasible solution for grade 3
        # Important note: Solution to this search only shows how many grade 3 nurses should work nightshift
        SEARCH_3 = self.getOverallSolution()

        # A feasible solution for grade 2
        # Important note: Solution to this search only shows how many grade 2 nurses should work nightshift
        feasible_grade_2_solution_exists = False
        while not feasible_grade_2_solution_exists:
            prevSolution = SEARCH_3.bestSolution
            SEARCH_2 = self.getGradeTwoSolution(prevSolution)
            solution = SEARCH_2.bestSolution

            # If no solution could be found, we backtrack to grade 3 tree, 
            # and find the next feasible grade 3 solution
            if solution.level == -1:
                SEARCH_3.startSearch(True)

                # If we find a new solution
                if SEARCH_3.bestSolution != prevSolution:
                    #feasible_grade_2_solution_exists = True
                    continue
                # Otherwise add bank nurse and try again
                else:
                    self.addBankNurse()
                    SEARCH_3 = self.getOverallSolution()
            else:
                feasible_grade_2_solution_exists = True


        # A feasible solutino for grade 2
        # Important note: Solution to this search only shows how many grade 1 nurses should work nightshift
        feasible_grade_1_solution_exists = False
        while not feasible_grade_1_solution_exists:
            prevSolution = SEARCH_2.bestSolution
            SEARCH_1 = self.getGradeOneSolution(prevSolution)
            solution = SEARCH_1.bestSolution

             # If no solution could be found, we backtrack to grade 2 tree, 
            # and find the next feasible grade 2 solution
            if solution.level == -1:
                SEARCH_2.startSearch(True)

                # If we find a new solution
                if SEARCH_2.bestSolution != prevSolution:
                    #feasible_grade_2_solution_exists = True
                    continue
                # Otherwise add bank nurse and try again
                # We add a bank nurse the the previous search's best solution
                else:
                    bankNurseProfit = self.bankNurseContract.nights
                    bankNurseWeight = self.bankNurseContract.days
                    bankNurseItem = KnapsackItem(bankNurseProfit, bankNurseWeight, 2)
                    prevSolution.items.append(bankNurseItem)
                    self.addBankNurse()
                    SEARCH_2 = self.getGradeTwoSolution(prevSolution)
                    print("hej")
            else:
                feasible_grade_1_solution_exists = True

        return SEARCH_1   

    def getOverallSolution(self):
        # Find a feasible solution for grade 3
        branchAndSearch = None
        grade_three_solution_exists = False
        
        while not grade_three_solution_exists:
            upperBounds = self.getOverallUpperBounds()
            boundedItemGroups = self.createBoundedItemGroups(upperBounds)
            C_3 = self.costForBounds(upperBounds, self.D)
            lowerBound = self.E

            # If the upper bound is smaller then lower bound, the problem is infeasible
            # Therefor we add a bank nurse to the solution and try again
            if(C_3 <= lowerBound):
                self.addBankNurse()
                continue

            self.globalC = C_3

            boundedKnapsack = BoundedKnapsack(boundedItemGroups, C_3)
            zeroOneKnapsack = boundedKnapsack.asZeroOne_simple()
            branchAndSearch = BranchAndBound_MODERN(zeroOneKnapsack, lowerBound)

            branchAndSearch.startSearch(True)
            solution = branchAndSearch.bestSolution

            # If solution.level is -1, then no feasible solution exists
            # Else we have found a solution and exit the while loop
            if solution.level == -1:
                # Add nurses equivelant to difference between lower and upper bound
                bankN = C_3 - lowerBound
                for _ in range(bankN):
                    self.addBankNurse()
            else:
                grade_three_solution_exists = True
        
        return branchAndSearch
    
    def addBankNurse(self):
        bankContract = self.bankNurseContract
        bankGrade = self.bankNurseGrade
        bankNurse = Nurse(1000 + self.bankNurseCount, bankGrade, bankContract)
        self.globalC += bankContract.days
        self.schedule.nurses.append(bankNurse)
        self.bankNurseCount += 1

    def getGradeTwoSolution(self, previousSolution):
        Q_3 = self.getTypesFromSolution(previousSolution)
        E_2 = self.requiredForGrade(Grade.TWO, True)
        D_2 = self.requiredForGrade(Grade.TWO, False)

        N_I_G = self.getContractToGrade()

        upperBounds = {
            self.contracts[0]: 0,
            self.contracts[1]: 0,
            self.contracts[2]: 0
        }

        #lowerBound = previousSolution.Z
        lowerBound = E_2

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

        #C_2 = self.costForBounds(upperBounds, D_2)

        # Represent the problem in bounded knapsack item groups
        items = []
        for contract in self.contracts:
            profit = contract.nights
            weight = contract.days
            upperBound = upperBounds[contract]

            itemGroup = ItemGroup(profit, weight, upperBound)
            items.append(itemGroup)
        
        # There is something wrong with upper bounds
        # It works if we're judt kinda ignoring the upper bound
        # TODO: figure it out
        #C_2 = 20

        # Find a feasible solution for grade 2
        boundedKnapsack = BoundedKnapsack(items, self.globalC)
        zeroOneKnapsack = boundedKnapsack.asZeroOne_simple()
        branchAndSearch = BranchAndBound_MODERN(zeroOneKnapsack, lowerBound)

        branchAndSearch.startSearch(True)

        return branchAndSearch
    
    def getGradeOneSolution(self, previousSolution):
        # Nurses of type i working contract, chosen from prev solution
        Q_2 = self.getTypesFromSolution(previousSolution)
        # Grade 1 shifts needing to be covered
        E_1 = self.requiredForGrade(Grade.ONE, True)
        # Grade 1 shifts needing to be covered
        D_1 = self.requiredForGrade(Grade.ONE, False)

        #lowerBound = previousSolution.Z
        lowerBound = E_1

        # Number of nurses of grade G working contract I
        N_I_G = self.getContractToGrade()

        upperBounds = {
            self.contracts[0]: 0,
            self.contracts[1]: 0,
            self.contracts[2]: 0
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
        
        # TODO: figure out the stuff with upper bound
        #C_1 = self.costForBounds(upperBounds, D_1)

        # Find a feasible solution for grade 2
        boundedKnapsack = BoundedKnapsack(items, self.globalC)
        zeroOneKnapsack = boundedKnapsack.asZeroOne_simple()
        branchAndSearch = BranchAndBound_MODERN(zeroOneKnapsack, lowerBound)

        branchAndSearch.startSearch(True)
        
        return branchAndSearch
    
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
            contract = nurse.contract
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
    def costForBounds(self, upperBounds: dict, D:int):
        C = 0
        for i in range(len(self.contracts)):
            contract = self.contracts[i]
            d = contract.days
            n = upperBounds[contract]
            C += d * n

        C = C - D
        return C

    # Returns the number of shifts needed to be covered for each grade
    def requiredForGrade(self, Grade, night):
        return sum(shift.coverRequirements[Grade] for shift in self.schedule.shifts if (shift.shiftType == ShiftType.NIGHT if night else shift.shiftType != ShiftType.NIGHT))

    # Returns how many nurses of each type should work night (y_i from the paper)
    def getTypesFromSolution(self, solution:Node):
        contractToType = {
            self.contracts[0]: 0,
            self.contracts[1]: 0,
            self.contracts[2]: 0
        }

        for item in solution.items:
            key = item.itemType
            contract = self.contracts[key]
            contractToType[contract] += 1

        return contractToType
