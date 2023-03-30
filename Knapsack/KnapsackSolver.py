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
        self.globalC = 0
        self.bankNurseContract = Contract(1, 1)
        self.contracts = self.extractContracts(self.schedule.nurses)
        self.bankNurseGrade = Grade.ONE
        self.bankNurseCount = 0
        self.originalNurses = len(schedule.nurses)

    # Strategy consists of 3 parts:
    # 1. Find the first feasible solution above lower bound E (feasible for all grades)
    # 2. Define a new problem only accounting for grade 1 and 2, using the Z of previous solution as lower bound
    # 3. Define a new problem only accounting for grade 1 using the Z of previous solution as lower bound
    # When a feasible solution has been found for all steps, it is known for there to be a feasible solution
    # If any solution has no feasible solutions, add bank nurses
    # TODO: Also account for prefered level of coverage
    def solve(self):
        # TODO: VERY IMPORTANT! MAKE SOLUTION 2 AND 1 FINDERS ABLE TO ADD BANK NURSES AS NEEDED

        print("Starting knapsack search")

        # A feasible solution for grade 3
        # Important note: Solution to this search only shows how many grade 3 nurses should work nightshift
        SEARCH_3 = self.getOverallSolution()

        print("Found grade 3 solution with items: ")
        print(SEARCH_3.bestSolution.items)

        # A feasible solution for grade 2
        # Important note: Solution to this search only shows how many grade 2 nurses should work nightshift
        feasible_grade_2_solution_exists = False
        while not feasible_grade_2_solution_exists:
            prevSolution = SEARCH_3.bestSolution
            SEARCH_2 = self.getGradeTwoSolution(prevSolution)
            solution = SEARCH_2.bestSolution

            if solution.level == -1:
                SEARCH_3.startSearch(True)

                # If we find a new solution
                if SEARCH_3.bestSolution != prevSolution:
                    #feasible_grade_2_solution_exists = True
                    continue
                # Otherwise add bank nurse and try again
                else:
                    self.addBankNurse(Grade.TWO)
                    SEARCH_3 = self.getOverallSolution()
            else:
                feasible_grade_2_solution_exists = True

        print("Found grade 2 solution with items: ")
        print(SEARCH_2.bestSolution.items)

        # A feasible solutino for grade 2
        # Important note: Solution to this search only shows how many grade 1 nurses should work nightshift
        feasible_grade_1_solution_exists = False
        while not feasible_grade_1_solution_exists:
            prevSolution = SEARCH_2.bestSolution
            SEARCH_1 = self.getGradeOneSolution(prevSolution)
            solution = SEARCH_1.bestSolution

            if solution.level == -1:
                SEARCH_2.startSearch(True)

                # If we find a new solution
                if SEARCH_2.bestSolution != prevSolution:
                    continue
                # Otherwise add bank nurse and try again
                # We add a bank nurse the the previous search's best solution
                else:
                    bankNurseProfit = self.bankNurseContract.nights
                    bankNurseWeight = self.bankNurseContract.days
                    index = self.contracts.index(self.bankNurseContract)
                    bankNurseItem = KnapsackItem(bankNurseProfit, bankNurseWeight, index)
                    prevSolution.items.append(bankNurseItem)
                    self.addBankNurse(Grade.ONE)
                    SEARCH_2 = self.getGradeTwoSolution(prevSolution)
            else:
                feasible_grade_1_solution_exists = True

        print("Found grade 1 solution with items: ")
        print(SEARCH_1.bestSolution.items)

        return SEARCH_1   

    def getOverallSolution(self):
        # Find a feasible solution for grade 3
        branchAndSearch = None
        grade_three_solution_exists = False
        
        while not grade_three_solution_exists:
            upperBounds = self.getOverallUpperBounds()
            boundedItemGroups = self.createBoundedItemGroups(upperBounds)
            cost = self.costForBounds(upperBounds, self.D)
            lowerBound = self.E

            # If the upper bound is smaller than lower bound, the problem is infeasible
            if(cost < lowerBound):
                print("-------------")
                print("There are insufficent grade 3 nurses to cover all requirements")
                n = lowerBound - cost + 1
                #n //= self.bankNurseContract.nights       
                print(f"Adding {n} nurses")      
                for _ in range(n):
                    self.addBankNurse(Grade.THREE)
                print("-------------")
                continue

            self.globalC = cost

            boundedKnapsack = BoundedKnapsack(boundedItemGroups, cost)
            zeroOneKnapsack = boundedKnapsack.asZeroOne_simple()
            branchAndSearch = BranchAndBound_MODERN(zeroOneKnapsack, lowerBound)

            branchAndSearch.startSearch(True)
            solution = branchAndSearch.bestSolution

            # If solution.level is -1, then no feasible solution exists
            # Else we have found a solution and exit the while loop
            if solution.level == -1:
                # Add nurses equivelant to difference between lower and global upper bound
                bankN = cost - lowerBound
                for _ in range(bankN):
                    self.addBankNurse(Grade.THREE)
                continue
            else:
                grade_three_solution_exists = True
        
        return branchAndSearch

    def getGradeTwoSolution(self, previousSolution):
        Q_3 = self.getTypesFromSolution(previousSolution)
        E_2 = self.requiredForGrade(Grade.TWO, True)
        D_2 = self.requiredForGrade(Grade.TWO, False)

        upperBounds = {}
        typeToCount = {}
        for contract in self.contracts:
            upperBounds[contract] = 0
            typeToCount[contract] = 0

        lowerBound = E_2
        isFeasible = False
        while not isFeasible:
            N_I_G = self.getContractToGrade()
            for contract in self.contracts:
                Q_i = Q_3[contract]
                N_I_3 = N_I_G[contract][Grade.THREE]
                N_I_2 = N_I_G[contract][Grade.TWO]
                N_I_1 = N_I_G[contract][Grade.ONE]
                typeToCount[contract] = N_I_1 + N_I_2

                if Q_i <= N_I_3:
                    upperBounds[contract] = N_I_1 + N_I_2
                else:
                    sub = Q_i - N_I_3
                    upperBounds[contract] = N_I_1 + N_I_2 - sub
                    lowerBound = E_2 - sub
                
                if Q_i < upperBounds[contract]:
                    upperBounds[contract] = Q_i
            
            cost = self.costForBounds(typeToCount, D_2)

            if cost < lowerBound:
                print("-------------")
                print("There are insufficent grade 2 nurses to cover all requirements")
                nursesNeeded = lowerBound - cost
                print(f"Adding {nursesNeeded} nurses") 
                for _ in range(nursesNeeded):
                    self.addBankNurse(Grade.TWO)
                continue
            else:
                isFeasible = True

        # Represent the problem in bounded knapsack item groups
        items = self.createBoundedItemGroups(typeToCount)
        boundedKnapsack = BoundedKnapsack(items, cost)
        zeroOneKnapsack = boundedKnapsack.asZeroOne_simple()
        branchAndSearch = BranchAndBound_MODERN(zeroOneKnapsack, lowerBound)

        branchAndSearch.startSearch(True)

        return branchAndSearch
    
    def getGradeOneSolution(self, previousSolution):
        Q_2 = self.getTypesFromSolution(previousSolution)
        E_1 = self.requiredForGrade(Grade.ONE, True)
        D_1 = self.requiredForGrade(Grade.ONE, False)

        upperBounds = {}
        typeToCount = {}
        for contract in self.contracts:
            upperBounds[contract] = 0
            typeToCount[contract] = 0

        lowerBound = E_1
        N_I_G = self.getContractToGrade()

        isFeasible = False
        while not isFeasible:
            N_I_G = self.getContractToGrade()
            for contract in self.contracts:
                Q_i = Q_2[contract]
                N_I_2 = N_I_G[contract][Grade.TWO]
                N_I_1 = N_I_G[contract][Grade.ONE]
                typeToCount[contract] = N_I_1

                if Q_i <= N_I_2:
                    upperBounds[contract] = N_I_1
                else:
                    sub = Q_i - N_I_2
                    upperBounds[contract] = N_I_1 - sub 
                    lowerBound = E_1 - sub
                if Q_i < upperBounds[contract]:
                    upperBounds[contract] = Q_i

            cost = self.costForBounds(typeToCount, D_1)

            if cost < lowerBound:
                print("-------------")
                print("There are insufficent grade 1 nurses to cover all requirements")
                nursesNeeded = lowerBound - cost
                print(f"Adding {nursesNeeded} nurses") 
                for _ in range(nursesNeeded):
                    self.addBankNurse(Grade.ONE)
                continue
            else:
                isFeasible = True

        # Represent the problem in bounded knapsack item groups
        items = self.createBoundedItemGroups(typeToCount)
        boundedKnapsack = BoundedKnapsack(items, cost)
        zeroOneKnapsack = boundedKnapsack.asZeroOne_simple()
        branchAndSearch = BranchAndBound_MODERN(zeroOneKnapsack, lowerBound)

        branchAndSearch.startSearch(True)
        
        return branchAndSearch
    
    def addBankNurse(self, grade:Grade):
        bankContract = self.bankNurseContract
        bankGrade = grade
        bankNurse = Nurse(self.originalNurses + self.bankNurseCount, bankGrade, bankContract)
        self.globalC += bankContract.days
        self.schedule.nurses.append(bankNurse)
        self.bankNurseCount += 1
    
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
        upperBounds = {}
        for contract in self.contracts:
            upperBounds[contract] = 0
        
        for nurse in self.schedule.nurses:
            upperBounds[nurse.contract] += 1

        return upperBounds

    # Represent the problem in bounded knapsack item groups
    def createBoundedItemGroups(self, upperBounds):
        boundedItemGroups = []
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
        for contract in self.contracts:
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
        contractToType = {}
        for contract in self.contracts:
            contractToType[contract] = 0

        for item in solution.items:
            key = item.itemType
            contract = self.contracts[key]
            contractToType[contract] += 1
        return contractToType
    
    def extractContracts(self, nurses):
        contracts = {self.bankNurseContract}
        nContracts = {nurse.contract for nurse in nurses}
        contracts = contracts.union(nContracts)
        return list(contracts)