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
    def test_finds_grade_three_solution(self):
        schedule = self._get_grade_three_feasible_schedule()
        solver = KnapsackSolver(schedule)

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution

        # If not equal to -1, then a feasible solution exists
        self.assertTrue(grade_3_solution.level != -1)
        self.assertTrue(grade_3_solution.Z > 0)
    
    def test_infeasible_schedule_grade_3_gets_assigned_bank_nurses(self):
        schedule = self._get_grade_three_infeasible_schedule()
        originalNurses = len(schedule.nurses)

        solver = KnapsackSolver(schedule)

        # Nurses are added to the solver as a side-effect
        grade_3_search = solver.getOverallSolution()
        newNurses = len(solver.schedule.nurses)

        self.assertNotEqual(originalNurses, newNurses)
    
    def test_finds_feasible_grade_three_solution_for_feasible_grade_two_schedule(self):
        schedule = self._get_grade_two_feasible_schedule()
        solver = KnapsackSolver(schedule)

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution

        # If not equal to -1, then a feasible solution exists
        self.assertTrue(grade_3_solution.level != -1)
        self.assertTrue(grade_3_solution.Z > 0)

    def test_finds_grade_two_solution(self):
        schedule = self._get_grade_two_feasible_schedule()
        solver = KnapsackSolver(schedule)

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution
        grade_2_search = solver.getGradeTwoSolution(grade_3_solution)
        grade_2_solution = grade_2_search.bestSolution

        # If not equal to -1, then a feasible solution exists
        self.assertTrue(grade_2_solution.level != -1)
        self.assertTrue(grade_2_solution.Z > 0)
    
    # Not implemented yet
    # When no feasible solution exists at level 2, the tree should continue its search at level 3
    def test_infeasible_schedule_grade_2_gets_assigned_bank_nurses(self):
        pass

    def test_finds_grade_one_solution(self):
        schedule = self._get_grade_one_feasible_schedule()
        solver = KnapsackSolver(schedule)

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution
        grade_2_search = solver.getGradeTwoSolution(grade_3_solution)
        grade_2_solution = grade_2_search.bestSolution
        grade_1_search = solver.getGradeOneSolution(grade_2_solution)
        grade_1_solution = grade_1_search.bestSolution

        # If not equal to -1, then a feasible solution exists
        self.assertTrue(grade_1_solution.level != -1)
        self.assertTrue(grade_1_solution.Z > 0)
    
    def test_solves_feasible_grade_one_schedule(self):
        schedule = self._get_grade_one_feasible_schedule()
        solver = KnapsackSolver(schedule)

        branchAndBound = solver.solve()
        feasibleSolution = branchAndBound.bestSolution

        # If not equal to -1, then a feasible solution exists
        # self.assertTrue(grade_1_solution.level != -1)
        # self.assertTrue(grade_1_solution.Z > 0)

        self.assertTrue(feasibleSolution.level != -1)

        pass

    def test_schedule_with_no_nurses_gets_bank_nurse_solution(self):
        nurselessSchedule = self._get_schedule_with_no_nurses()
        solver = KnapsackSolver(nurselessSchedule)

        # Make sure no nurses are in schedule
        self.assertEqual(0, len(nurselessSchedule.nurses))

        grade_3_search = solver.getOverallSolution()
        grade_3_solution = grade_3_search.bestSolution
        grade_2_search = solver.getGradeTwoSolution(grade_3_solution)
        grade_2_solution = grade_2_search.bestSolution
        grade_1_search = solver.getGradeOneSolution(grade_2_solution)
        grade_1_solution = grade_1_search.bestSolution

        nurses = solver.schedule.nurses

        # A feasible solution should have been generated
        self.assertTrue(len(nurses) > 0)
        self.assertTrue(grade_1_solution.level != -1)
        self.assertTrue(grade_1_solution.Z > 0)

     # Not implemented yet
    # When no feasible solution exists at level 2, the tree should continue its search at level 3
    def test_infeasible_grade_2_search_finds_no_solution(self):
        pass

    # Not implemented yet
    # When no feasible solution exists at level 1, the tree should continue its search at level 2
    def test_infeasible_grade_3_search_finds_no_solution(self):
        pass
    
    # Tests if the solver's .requiredForGrade() functions as expected
    def test_solver_gets_correct_shiftRequirements_for_grade(self):
        schedule = self._get_grade_three_feasible_schedule()

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
    def _get_grade_three_feasible_schedule(self):
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
        schedule = self._get_grade_three_feasible_schedule()
        schedule.nurses = []
        return schedule
    
    def _get_grade_three_infeasible_schedule(self):
        feasibleSchedule = self._get_grade_three_feasible_schedule()

        # I miss c# linq :(
        nightShift = next((shift for shift in feasibleSchedule.shifts if shift.shiftType == ShiftType.NIGHT), None)
        # By adding 1 Grade3 nurse to the night shift requirements, 
        # the schedule will no longer have a feasible solution for Grade3
        nightShift.coverRequirements[Grade.THREE] += 1

        return feasibleSchedule
    
    # Returns a schedule, which is only feasible for grade 2 and 3 nurses
    # The schedule will have:
    # Day shift requirements:  Grade1: 3, Grade2: 6, Grade3: 8
    # Night shift requiremnts: Grade1: 1, Grade2: 2, Grade3: 4
    # 
    # Day nurse potential coverage: Grade1: 0, Grade2: 14, Grade3: 14
    # Night nurse potential coverage: Grade1: 0, Grade2: 11, Grade3: 11
    def _get_grade_two_feasible_schedule(self):
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
    
    def _get_grade_two_infeasible_schedule(self):
        feasibleSchedule = self._get_grade_two_feasible_schedule()

        # I miss c# linq :(
        nightShift = next((shift for shift in feasibleSchedule.shifts if shift.shiftType == ShiftType.NIGHT), None)
        # By adding 1 Grade3 nurse to the night shift requirements, 
        # the schedule will no longer have a feasible solution for Grade3
        nightShift.coverRequirements[Grade.TWO] += 3
        nightShift.coverRequirements[Grade.TWO] += 3

        return feasibleSchedule
    
    # Returns a schedule, which is only feasible for grade 2 and 3 nurses
    # The schedule will have:
    # Day shift requirements:  Grade1: 3, Grade2: 6, Grade3: 8
    # Night shift requiremnts: Grade1: 1, Grade2: 2, Grade3: 4
    # 
    # Day nurse potential coverage: Grade1: 14, Grade2: 14, Grade3: 14
    # Night nurse potential coverage: Grade1: 11, Grade2: 11, Grade3: 11
    def _get_grade_one_feasible_schedule(self):
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

        nurses = [nurse1, nurse2, nurse3]

        return Schedule(shifts, nurses)
        

if __name__ == '__main__':
    unittest.main()
