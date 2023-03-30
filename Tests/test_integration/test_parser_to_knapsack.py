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

class ParserToKnapsack(unittest.TestCase):
    def test_parsed_scenario_solved_by_knapsackSolver(self):
        scenario = "n030w4"
        parser = NurseParser()

        schedule = parser.parseScenario(scenario)
        parsedNurses = copy.deepcopy(schedule.nurses)

        n = 0
        for nurse in parsedNurses:
            if nurse.grade == Grade.ONE:
                n += 1

        schedule.shifts[17].coverRequirements[Grade.ONE] = 5

        knapsackSolver = KnapsackSolver(schedule)
        search = knapsackSolver.solve()
        solution = search.bestSolution
        newNurses = knapsackSolver.schedule.nurses

        nightsWorked = 0
        for nurse in newNurses:
            if nurse.grade == Grade.ONE:
                nightsWorked += nurse.contract.nights

        self.assertNotEqual(solution.level, -1)



if __name__ == '__main__':
    unittest.main()