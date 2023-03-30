import unittest
import random

from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Enums.Days import Days
from Domain.Models.Shift import Shift
from Domain.Models.Nurse import Nurse
from Domain.Models.Schedule import Schedule

from Knapsack.BranchAndBound.BranchAndBound_MT import BranchAndBound_MT
from Knapsack.BranchAndBound.BranchAndBound_MODERN import BranchAndBound_MODERN
from Knapsack.Problems.KnapsackItem import KnapsackItem
from Knapsack.Problems.ZeroOneKnapsack import ZeroOneKnapsack
from Knapsack.KnapsackSolver import KnapsackSolver


class TestKnapsackSolver(unittest.TestCase):
    def test_finds_grade_3_solution(self):
        schedule = self._get_grade_3_feasible_schedule()
        solver = KnapsackSolver(schedule)

        expectedNurses = len(schedule.nurses)

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution
        actualNurese = len(solver.schedule.nurses)

        # If not equal to -1, then a feasible solution exists
        self.assertTrue(grade_3_solution.level != -1)
        self.assertTrue(grade_3_solution.Z > 0)

        # No bank nurses necesarry, shouldn't have been added
        self.assertEqual(expectedNurses, actualNurese)
    
    def test_finds_grade_2_solution(self):
        schedule = self._get_grade_2_feasible_schedule()
        solver = KnapsackSolver(schedule)

        D = solver.D
        E = solver.E

        expectedNurses = len(schedule.nurses)

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution
        grade_2_search = solver.getGradeTwoSolution(grade_3_solution)
        grade_2_solution = grade_2_search.bestSolution

        actualNurese = len(solver.schedule.nurses)

        # If not equal to -1, then a feasible solution exists
        self.assertTrue(grade_2_solution.level != -1)
        self.assertTrue(grade_2_solution.Z > 0)

        # No bank nurses necesarry, shouldn't have been added
        self.assertEqual(expectedNurses, actualNurese)
    

    def test_finds_grade_1_solution(self):
        schedule = self._get_grade_1_feasible_schedule()
        solver = KnapsackSolver(schedule)

        expectedNurses = len(schedule.nurses)

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution
        grade_2_search = solver.getGradeTwoSolution(grade_3_solution)
        grade_2_solution = grade_2_search.bestSolution
        grade_1_search = solver.getGradeOneSolution(grade_2_solution)
        grade_1_solution = grade_1_search.bestSolution

        actualNurese = len(solver.schedule.nurses)

        self.assertTrue(grade_1_solution.level != -1)
        self.assertTrue(grade_1_solution.Z > 0)

        # No bank nurses necesarry, shouldn't have been added
        self.assertEqual(expectedNurses, actualNurese)
    
    def test_finds_feasible_grade_3_solution_for_feasible_grade_2_schedule(self):
        schedule = self._get_grade_2_feasible_schedule()
        solver = KnapsackSolver(schedule)

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution

        # If not equal to -1, then a feasible solution exists
        self.assertTrue(grade_3_solution.level != -1)
        self.assertTrue(grade_3_solution.Z > 0)

    def test_finds_feasible_grade_3_solution_for_feasible_grade_1_schedule(self):
        schedule = self._get_grade_1_feasible_schedule()
        solver = KnapsackSolver(schedule)

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution

        # If not equal to -1, then a feasible solution exists
        self.assertTrue(grade_3_solution.level != -1)
        self.assertTrue(grade_3_solution.Z > 0)
    
    def test_finds_feasible_grade_2_solution_for_feasible_grade_1_schedule(self):
        schedule = self._get_grade_1_feasible_schedule()
        solver = KnapsackSolver(schedule)

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution
        grade_2_search = solver.getGradeTwoSolution(grade_3_solution)
        grade_2_solution = grade_2_search.bestSolution

        # If not equal to -1, then a feasible solution exists
        self.assertTrue(grade_2_solution.level != -1)
        self.assertTrue(grade_2_solution.Z > 0)

    def test_solves_feasible_grade_3_schedule(self):
        schedule = self._get_grade_3_feasible_schedule()
        solver = KnapsackSolver(schedule)

        branchAndBound = solver.solve()
        feasibleSolution = branchAndBound.bestSolution

        # If not equal to -1, then a feasible solution exists
        # self.assertTrue(grade_1_solution.level != -1)
        # self.assertTrue(grade_1_solution.Z > 0)

        self.assertTrue(feasibleSolution.level != -1)
    
    def test_solves_feasible_grade_2_schedule(self):
        schedule = self._get_grade_2_feasible_schedule()
        solver = KnapsackSolver(schedule)

        branchAndBound = solver.solve()
        feasibleSolution = branchAndBound.bestSolution

        # If not equal to -1, then a feasible solution exists
        # self.assertTrue(grade_1_solution.level != -1)
        # self.assertTrue(grade_1_solution.Z > 0)

        self.assertTrue(feasibleSolution.level != -1)
    
    def test_solves_feasible_grade_1_schedule(self):
        schedule = self._get_grade_1_feasible_schedule()
        solver = KnapsackSolver(schedule)

        branchAndBound = solver.solve()
        feasibleSolution = branchAndBound.bestSolution

        self.assertTrue(feasibleSolution.level != -1)
        self.assertTrue(feasibleSolution.Z > 0)
    
    # Shoul solve it by adding bank nurses
    def test_solves_infeasible_grade_3_schedule(self):
        schedule = self._get_grade_3_infeasible_schedule()
        solver = KnapsackSolver(schedule)
        originalNurseLength = len(solver.schedule.nurses)

        branchAndBound = solver.solve()
        feasibleSolution = branchAndBound.bestSolution

        newNurseLength = len(solver.schedule.nurses)
        
        self.assertTrue(originalNurseLength != newNurseLength)
        self.assertTrue(feasibleSolution.level != -1)
        self.assertTrue(feasibleSolution.Z > 0)

    def test_solves_infeasible_grade_2_schedule(self):
        schedule = self._get_grade_2_infeasible_schedule()
        solver = KnapsackSolver(schedule)
        originalNurseLength = len(solver.schedule.nurses)

        branchAndBound = solver.solve()
        feasibleSolution = branchAndBound.bestSolution

        newNurseLength = len(solver.schedule.nurses)
        
        self.assertTrue(originalNurseLength != newNurseLength)
        self.assertTrue(feasibleSolution.level != -1)
        self.assertTrue(feasibleSolution.Z > 0)

    def test_solves_infeasible_grade_1_schedule(self):
        schedule = self._get_grade_1_infeasible_schedule()
        solver = KnapsackSolver(schedule)
        originalNurseLength = len(solver.schedule.nurses)

        branchAndBound = solver.solve()
        feasibleSolution = branchAndBound.bestSolution

        newNurseLength = len(solver.schedule.nurses)
        
        self.assertTrue(originalNurseLength != newNurseLength)
        self.assertTrue(feasibleSolution.level != -1)
        self.assertTrue(feasibleSolution.Z > 0)
    
    # If the schedule has no nurses, it should find a solution consisting only of bank nurses
    def test_solves_empty_schedule(self):
        emptySchedule = self._get_schedule_with_no_nurses()
        solver = KnapsackSolver(emptySchedule)

        branchAndBound = solver.solve()
        feasibleSolution = branchAndBound.bestSolution

        nurses = len(solver.schedule.nurses)

        self.assertTrue(nurses > 0)
        self.assertTrue(feasibleSolution.level != -1)
        self.assertTrue(feasibleSolution.Z > 0)

    def test_schedule_with_no_nurses_gets_bank_nurse_solution(self):
        nurselessSchedule = self._get_schedule_with_no_nurses()
        solver = KnapsackSolver(nurselessSchedule)

        # Make sure no nurses are in schedule
        self.assertEqual(0, len(nurselessSchedule.nurses))

        search = solver.solve()
        solution = search.bestSolution
        nurses = solver.schedule.nurses

        # A feasible solution should have been generated
        self.assertTrue(len(nurses) > 0)
        self.assertTrue(solution.level != -1)
        self.assertTrue(solution.Z > 0)

    # Grade 3 will always return a feasible schedule, as it implicitly adds bank nurses
    def test_infeasible_grade_3_assigned_bank_nurses(self):
        infeasibleSchedule = self._get_grade_3_infeasible_schedule()
        originalNurses = len(infeasibleSchedule.nurses)

        solver = KnapsackSolver(infeasibleSchedule)

        # Nurses are added to the solver as a side-effect
        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution
        newNurses = len(solver.schedule.nurses)

        self.assertNotEqual(originalNurses, newNurses)

        # Make sure that a solution was found
        self.assertTrue(newNurses > 0)
        self.assertTrue(grade_3_solution.level != -1)
        self.assertTrue(grade_3_solution.Z > 0)

    # Not implemented yet
    # This DOES NOT test the solver. The solver backtracks in previous tree, and adds bank nurses
    # This methods tests that searching an infeasible tree gives no feasible solutions
    def test_infeasible_grade_2_search_finds_no_solution(self):
        infeasibleSchedule = self._get_grade_2_infeasible_schedule()
        solver = KnapsackSolver(infeasibleSchedule)
        
        # Grade 3 solution should exist
        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution
        self.assertTrue(grade_3_solution.level != -1)
        
        # Grade 2 solution should not exist
        grade_2_search = solver.getGradeTwoSolution(grade_3_solution)
        grade_2_solution = grade_2_search.bestSolution

        # TODO: THIS HAS BEEN CHANGED. NOW THERE SHOULD BE A SOLUTION TODO:
        #self.assertTrue(grade_2_solution.level == -1)

    # This DOES NOT test the solver. The solver backtracks in previous tree, and adds bank nurses
    # This methods tests that searching an infeasible tree gives no feasible solutions
    # NOTE: This is depdendent on BankNurse contract being 3 days, 2 nights
    def test_infeasible_grade_1_search_finds_no_solution(self):
        infeasibleSchedule = self._get_grade_1_infeasible_schedule()
        solver = KnapsackSolver(infeasibleSchedule)

        # Grade 3 solution should exist
        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution
        self.assertTrue(grade_3_solution.level != -1)

        # Grade 1 solution should not exist
        # It would probably fail already at grade 2, so we go directly to grade 1 to ensure test
        grade_1_search = solver.getGradeOneSolution(grade_3_solution)
        grade_1_solution = grade_1_search.bestSolution
        
        # TODO: THIS HAS BEEN CHANGED. NOW THERE SHOULD BE A SOLUTION TODO:
        # self.assertTrue(grade_1_solution.level == -1)

    # Tests if the solver's .requiredForGrade() functions as expected
    def test_solver_gets_correct_shiftRequirements_for_grade(self):
        schedule = self._get_grade_3_feasible_schedule()

        # actual values
        solver = KnapsackSolver(schedule)
        D_3 = solver.D
        E_3 = solver.E

        D_2 = solver.requiredForGrade(Grade.TWO, False)
        E_2 = solver.requiredForGrade(Grade.TWO, True)

        D_1 = solver.requiredForGrade(Grade.ONE, False)
        E_1 = solver.requiredForGrade(Grade.ONE, True)

        # expected values
        eD_3 = 8
        eD_2 = 6
        eD_1 = 3
        eN_3 = 4
        eN_2 = 2
        eN_1 = 1

        self.assertEqual(eD_3, D_3)
        self.assertEqual(eD_2, D_2)
        self.assertEqual(eD_1, D_1)
        self.assertEqual(eN_3, E_3)
        self.assertEqual(eN_2, E_2)
        self.assertEqual(eN_1, E_1)
    
    # Returns a schedule, which is only feasible for grade 3 nurses
    # The schedule will have:
    # Day shift requirements:  Grade1: 3, Grade2: 6, Grade3: 8
    # Night shift requiremnts: Grade1: 1, Grade2: 2, Grade3: 4
    # 
    # Day nurse potential coverage: Grade1: 0, Grade2: 0, Grade3: 14
    # Night nurse potential coverage: Grade1: 0, Grade2: 0, Grade3: 11
    def _get_grade_3_feasible_schedule(self):
        # Static
        contract1 = Contract(5, 4)
        contract2 = Contract(4, 3)
        contract3 = Contract(3, 2)

        # Shifts
        ## Days doesn't matter, shiftType only matters if night or day
        requirements1 = {
            Grade.ONE: 1,
            Grade.TWO: 1,
            Grade.THREE: 2
        }
        shift1 = Shift(requirements1, ShiftType.EARLY, Days.MONDAY)

        requirements2 = {
            Grade.ONE: 1,
            Grade.TWO: 2,
            Grade.THREE: 2
        }
        shift2 = Shift(requirements2, ShiftType.LATE, Days.MONDAY)

        requirements3 = {
            Grade.ONE: 1,
            Grade.TWO: 3,
            Grade.THREE: 4
        }
        shift3 = Shift(requirements3, ShiftType.EARLY, Days.MONDAY)

        # Night shift
        requirements4 = {
            Grade.ONE: 1,
            Grade.TWO: 2,
            Grade.THREE: 4
        }
        shift4 = Shift(requirements4, ShiftType.NIGHT, Days.MONDAY)

        shifts = [shift1, shift2, shift3, shift4]

        # there must be exactly 21 shifts...
        noRequirements = {
            Grade.ONE: 0,
            Grade.TWO: 0,
            Grade.THREE: 0
        }
        for _ in range(0, 21 - len(shifts)):
            mockShift = Shift(noRequirements, ShiftType.EARLY, Days.MONDAY)
            shifts.append(mockShift)

        # Nurses
        nurse1 = Nurse(0, Grade.THREE, contract1)
        nurse2 = Nurse(1, Grade.THREE, contract1)
        nurse3 = Nurse(2, Grade.THREE, contract2)

        nurses = [nurse1, nurse2, nurse3]

        return Schedule(shifts, nurses)
    
    def _get_schedule_with_no_nurses(self):
        schedule = self._get_grade_3_feasible_schedule()
        schedule.nurses = []
        return schedule
    
    def _get_grade_3_infeasible_schedule(self):
        feasibleSchedule = self._get_grade_3_feasible_schedule()

        # I miss c# linq :(
        nightShift = next((shift for shift in feasibleSchedule.shifts if shift.shiftType == ShiftType.NIGHT), None)
        # By adding 3 Grade3 nurse to the night shift requirements, 
        # the schedule will no longer have a feasible solution for Grade3
        nightShift.coverRequirements[Grade.THREE] += 3

        return feasibleSchedule
    
    # Returns a schedule, which is only feasible for grade 2 and 3 nurses
    # The schedule will have:
    # Day shift requirements:  Grade1: 3, Grade2: 6, Grade3: 8
    # Night shift requiremnts: Grade1: 1, Grade2: 2, Grade3: 4
    # 
    # Day nurse potential coverage: Grade1: 0, Grade2: 14, Grade3: 14
    # Night nurse potential coverage: Grade1: 0, Grade2: 11, Grade3: 11
    def _get_grade_2_feasible_schedule(self):
        # Static
        contract1 = Contract(5, 4)
        contract2 = Contract(4, 3)
        contract3 = Contract(3, 2)

        # Shifts
        ## Days doesn't matter, shiftType only matters if night or day
        requirements1 = {
            Grade.ONE: 1,
            Grade.TWO: 1,
            Grade.THREE: 2
        }
        shift1 = Shift(requirements1, ShiftType.EARLY, Days.MONDAY)

        requirements2 = {
            Grade.ONE: 1,
            Grade.TWO: 2,
            Grade.THREE: 2
        }
        shift2 = Shift(requirements2, ShiftType.LATE, Days.MONDAY)

        requirements3 = {
            Grade.ONE: 1,
            Grade.TWO: 3,
            Grade.THREE: 4
        }
        shift3 = Shift(requirements3, ShiftType.EARLY, Days.MONDAY)

        # Night shift
        requirements4 = {
            Grade.ONE: 1,
            Grade.TWO: 2,
            Grade.THREE: 4
        }
        shift4 = Shift(requirements4, ShiftType.NIGHT, Days.MONDAY)

        shifts = [shift1, shift2, shift3, shift4]

        # there must be exactly 21 shifts...
        noRequirements = {
            Grade.ONE: 0,
            Grade.TWO: 0,
            Grade.THREE: 0
        }
        for _ in range(0, 21 - len(shifts)):
            mockShift = Shift(noRequirements, ShiftType.EARLY, Days.MONDAY)
            shifts.append(mockShift)

        # Nurses
        nurse1 = Nurse(0, Grade.TWO, contract1)
        nurse2 = Nurse(1, Grade.TWO, contract1)
        nurse3 = Nurse(2, Grade.TWO, contract2)

        nurses = [nurse1, nurse2, nurse3]

        return Schedule(shifts, nurses)
    
    def _get_grade_2_infeasible_schedule(self):
        feasibleSchedule = self._get_grade_2_feasible_schedule()

        # I miss c# linq :(
        nightShift = next((shift for shift in feasibleSchedule.shifts if shift.shiftType == ShiftType.NIGHT), None)
        # By adding 1 Grade3 nurse to the night shift requirements, 
        # the schedule will no longer have a feasible solution for Grade3
        nightShift.coverRequirements[Grade.TWO] += 3
        nightShift.coverRequirements[Grade.TWO] += 3
        nightShift.coverRequirements[Grade.THREE] += 3
        nightShift.coverRequirements[Grade.THREE] += 3

        return feasibleSchedule
    
    # Returns a schedule, which is only feasible for grade 2 and 3 nurses
    # The schedule will have:
    # Day shift requirements:  Grade1: 3, Grade2: 6, Grade3: 8
    # Night shift requiremnts: Grade1: 1, Grade2: 2, Grade3: 4
    # 
    # Day nurse potential coverage: Grade1: 14, Grade2: 14, Grade3: 14
    # Night nurse potential coverage: Grade1: 11, Grade2: 11, Grade3: 11
    def _get_grade_1_feasible_schedule(self):
        # Static
        contract1 = Contract(5, 4)
        contract2 = Contract(4, 3)
        contract3 = Contract(3, 2)

        # Shifts
        ## Days doesn't matter, shiftType only matters if night or day
        requirements1 = {
            Grade.ONE: 1,
            Grade.TWO: 1,
            Grade.THREE: 2
        }
        shift1 = Shift(requirements1, ShiftType.EARLY, Days.MONDAY)

        requirements2 = {
            Grade.ONE: 1,
            Grade.TWO: 2,
            Grade.THREE: 2
        }
        shift2 = Shift(requirements2, ShiftType.LATE, Days.MONDAY)

        requirements3 = {
            Grade.ONE: 1,
            Grade.TWO: 3,
            Grade.THREE: 4
        }
        shift3 = Shift(requirements3, ShiftType.EARLY, Days.MONDAY)

        # Night shift
        requirements4 = {
            Grade.ONE: 1,
            Grade.TWO: 2,
            Grade.THREE: 4
        }
        shift4 = Shift(requirements4, ShiftType.NIGHT, Days.MONDAY)

        shifts = [shift1, shift2, shift3, shift4]

        # there must be exactly 21 shifts...
        noRequirements = {
            Grade.ONE: 0,
            Grade.TWO: 0,
            Grade.THREE: 0
        }
        for _ in range(0, 21 - len(shifts)):
            mockShift = Shift(noRequirements, ShiftType.EARLY, Days.MONDAY)
            shifts.append(mockShift)

        # Nurses
        nurse1 = Nurse(0, Grade.ONE, contract1)
        nurse2 = Nurse(1, Grade.ONE, contract1)
        nurse3 = Nurse(2, Grade.ONE, contract2)
        # nurse4 = Nurse(2, Grade.ONE, contract1)
        # nurse5 = Nurse(2, Grade.ONE, contract1)

        nurses = [nurse1, nurse2, nurse3]

        return Schedule(shifts, nurses)
    
    def _get_grade_1_infeasible_schedule(self):
        feasibleSchedule = self._get_grade_1_feasible_schedule()

        # I miss c# linq :(
        nightShift = next((shift for shift in feasibleSchedule.shifts if shift.shiftType == ShiftType.NIGHT), None)
        # By adding 1 Grade1 nurse to the night shift requirements, 
        # the schedule will no longer have a feasible solution for Grade3
        nightShift.coverRequirements[Grade.ONE] += 4
        nightShift.coverRequirements[Grade.TWO] += 4
        nightShift.coverRequirements[Grade.THREE] += 4

        return feasibleSchedule
        

if __name__ == '__main__':
    unittest.main()
