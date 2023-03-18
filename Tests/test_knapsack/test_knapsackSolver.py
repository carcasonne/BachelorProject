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


class TestBoundAndBranch_MODERN(unittest.TestCase):
    # Based on example 2.2 from the book
    def test_finds_grade_three_solution(self):
        schedule = self._get_grade_three_feasible_schedule()
        solver = KnapsackSolver(schedule)

        grade_3_solution = solver.getOverallSolution()

        # If not equal to -1, then a feasible solution exists
        self.assertTrue(grade_3_solution.level != -1)
    
    def test_infeasible_schedule_gets_assigned_bank_nurses(self):
        schedule = self._get_grade_three_infeasible_schedule()
        solver = KnapsackSolver(schedule)

        grade_3_solution = solver.getOverallSolution()

        originalNurses = len(schedule.nurses)
        newNurses = len(solver.schedule.nurses)

        self.assertNotEqual(originalNurses, newNurses)
    
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
    
    def _get_grade_three_infeasible_schedule(self):
        feasibleSchedule = self._get_grade_three_feasible_schedule()

        # I miss c# linq :(
        nightShift = next((shift for shift in feasibleSchedule.shifts if shift.shiftType == ShiftType.NIGHT), None)
        # By adding 1 Grade3 nurse to the night shift requirements, 
        # the schedule will no longer have a feasible solution for Grade3
        nightShift.coverRequirements[Grade.THREE] += 1

        return feasibleSchedule
        

if __name__ == '__main__':
    unittest.main()
