"""
Tabu Search Class
"""
from Domain.Models.Enums.Grade import Grade
from TabuSearch.StaticMethods import *

# TODO: THIS SOLUTION IS ONLY BASED ON GRADE THREE

class TabuSearch_SIMPLE:
    def __init__(self, initialSolution, solutionEvaluator, neighborOperator, aspirationCriteria,
                 acceptableScoreThreshold, tabuTenure):
        """
        The next three variables is there to make sure that we hold the 3 tabu criteria:
            1) A move involves the tabu nurse (i.e. the nurse moved last time) from tabuList.
            2) A move results in a tabu configuration on the dayNightTabuList.
            3) The dayNightCounter exceeds maxits and the move does not change the day night split.
        """
        # Tabu criteria 1: tabulist - Nurses involved in earlier moves - This is a fixed length of 1
        self.tabuList = []
        # Tabu criteria 2:dayNightTabuList - Nurses working days - list[set(nurse working days), ...] - Length 6 (binary representation)
        self.dayNightTabuList = []
        # Tabu criteria 3:
        self.dayNightCounter = 0
        self.maxits = 0
        self.lowerBound = None  # TODO: Calculate Lower Bound
        # Feasible shift patterns for nurses is provided in this dict
        self.feasiblePatterns = dict()
        for n in initialSolution.nurses:
            self.feasiblePatterns[n.id] = findFeasiblePatterns(n)

        self.currSolution = initialSolution
        self.bestSolution = initialSolution
        self.evaluate = solutionEvaluator
        self.aspirationCriteria = aspirationCriteria
        self.neighborOperator = neighborOperator
        self.acceptableScoreThreshold = acceptableScoreThreshold
        self.tabuTenure = tabuTenure

    def makeMove(self, move):
        if None:  # TODO: Change this to: if the move changes the day night split
            self.dayNightTabuList = None  # TODO: the dayNightTabuList is updated
            self.dayNightCounter = 0
            self.lowerBound = None  # TODO: Calculate lowerbound Eq.(6)
        else:  # if move does not change the day night split
            self.dayNightCounter += 1

    def isTerminationCriteriaMet(self):
        # can add more termination criteria
        return self.evaluate(self.bestSolution) < self.acceptableScoreThreshold \
               or self.neighborOperator(self.currSolution) == 0

    def run(self):
        tabuList = {}

        while not self.isTerminationCriteriaMet():
            # get all of the neighbors
            neighbors = self.neighborOperator(self.currSolution)
            # find all tabuSolutions other than those
            # that fit the aspiration criteria
            tabuSolutions = tabuList.keys()
            # find all neighbors that are not part of the Tabu list
            neighbors = filter(lambda n: self.aspirationCriteria(n), neighbors)
            # pick the best neighbor solution
            newSolution = sorted(neighbors, key=lambda n: self.evaluate(n))[0]
            # get the cost between the two solutions
            cost = self.evaluate(self.solution) - self.evaluate(newSolution)
            # if the new solution is better,
            # update the best solution with the new solution
            if cost >= 0:
                self.bestSolution = newSolution
            # update the current solution with the new solution
            self.currSolution = newSolution

            # decrement the Tabu Tenure of all tabu list solutions
            for sol in tabuList:
                tabuList[sol] -= 1
                if tabuList[sol] == 0:
                    del tabuList[sol]
            # add new solution to the Tabu list
            tabuList[newSolution] = self.tabuTenure

        # return best solution found
        return self.bestSolution