import unittest
import copy

from Domain.Models.Schedule import Schedule
from Domain.Models.Enums.Grade import Grade

from Parser.NurseParser import NurseParser

from Knapsack.KnapsackSolver import KnapsackSolver

from Knapsack.Problems.KnapsackItem import KnapsackItem
from Knapsack.Problems.ItemGroup import ItemGroup
from Knapsack.Problems.BoundedKnapsack import BoundedKnapsack
#from Knapsack.Problems.ZeroOneKnapsack import ZeroOneKnapsac
from Knapsack.BranchAndBound.BranchAndBound_MODERN import BranchAndBound_MODERN
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE

class EntireFlow(unittest.TestCase):
    # TODO: Add assert tests. But now we are happy if it doesn't crash
    def test_runs_entire_flow(self):
        scenario = "n030w4"

        parser = NurseParser()
        schedule = parser.parseScenario(scenario)

        knapsackSolver = KnapsackSolver(schedule)
        search = knapsackSolver.solve()

        newSchedule = knapsackSolver.schedule
        search = TabuSearch_SIMPLE(TabuSchedule(newSchedule))

    # TODO: Add assert tests. But now we are happy if it doesn't crash
    def test_runs_entire_flow_with_bank_nurses(self):
        scenario = "n030w4"

        parser = NurseParser()
        schedule = parser.parseScenario(scenario)

        # We delete all nurses
        schedule.nurses = []
        # Knapsack should decide how many bank nurses are necesarry
        knapsackSolver = KnapsackSolver(schedule)
        search = knapsackSolver.solve()

        newSchedule = knapsackSolver.schedule
        
        search = TabuSearch_SIMPLE(TabuSchedule(newSchedule))

if __name__ == '__main__':
    unittest.main()