"""
Tabu Search Class
"""
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from Domain.Models.Enums.Grade import Grade
from TabuSearch.StaticMethods import *
from copy import *

# TODO: THIS SOLUTION IS ONLY BASED ON GRADE THREE

class TabuSearch_SIMPLE:
    def __init__(self, initialSolution): # (initialSolution, solutionEvaluator, neighborOperator, aspirationCriteria, acceptableScoreThreshold, tabuTenure)
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
        self.evaluate = None
        self.aspirationCriteria = None
        self.neighborOperator = None
        self.acceptableScoreThreshold = None
        self.tabuTenure = None

        self.shiftRequirements = findShiftTypeRequirements(initialSolution)

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

    # TODO: Random decent after PC and LB
    def randomDecent(self, schedule):
        """
        Step 1.1 (Random decent). Carry out random decent by accepting the first neighbourhood move that satisfies
        non-tabu conditions 1 - 3 and improves CC and does not increase PC. Repeat until no satisfactory move exists.
        :param schedule:
        :return move:
        """
        for nurse in schedule.nurses:
            if nurse.id not in self.tabuList:
                for pattern in self.feasiblePatterns[nurse.id]:
                    if (nurse.worksNight and pattern(0) == [0] * 7) or (not nurse.worksNight and pattern(0) != [0] * 7):
                        neighbour = copy.deepcopy(schedule)
                        n_nurse = neighbour.nurses[nurse.id]
                        n_nurse.assignShiftPattern(pattern)
                        neighbour.CC = evaluateCC(neighbour)
                        neighbour.PC = evaluatePC(neighbour)
                        if neighbour.CC < schedule.CC: #and neighbour.PC <= schedule.PC:
                            self.tabuList.append(nurse.id)
                            return neighbour
        return None

    def balanceRestoring(self, schedule:TabuSchedule):
        """
        Step 1.2 (Balance days and nights). Check for balance by lower bound (Eq(5)). if
        :param schedule:
        :return:
        """
        pass
        
    
    def findBalanceRestoringCandidateList(self, schedule:TabuSchedule):
        types = [TabuShiftType.DAY, TabuShiftType.NIGHT]
        # Find out if solution is unbalanced for any grade for any type

        for type in types:
                # Get all nurses working this type of pattern
                typeNurses = [nurse for nurse in schedule.nurses if nurse.worksNights]
                # Find number of shifts worked by all nurses of this grade and this type
                shifts = 0
                for nurse in typeNurses:
                    pattern = nurse.shiftPattern.day if type == TabuShiftType.DAY else nurse.shiftPattern.night
                    shifts += sum(pattern)

                # Fewer shifts worked than is required?
                if shifts < self.shiftRequirements[type][Grade.THREE]:
                    
                    pass

        # This is for considering all grades
        # for grade in Grade:
        #     # Get all nurses of this grade. This can technically be done in a single for-loop, possible optimization
        #     gradeNurses = [nurse for nurse in schedule.nurses if nurse.grade == grade]
        #     for type in types:
        #         # Get all nurses working this type of pattern
        #         typeNurses = [nurse for nurse in gradeNurses if nurse.worksNights]
        #         # Find number of shifts worked by all nurses of this grade and this type
        #         shifts = 0
        #         for nurse in typeNurses:
        #             pattern = nurse.shiftPattern.day if type == TabuShiftType.DAY else nurse.shiftPattern.night
        #             shifts += sum(pattern)

        #         # Fewer shifts worked than is required?
        #         if shifts < self.shiftRequirements[type][grade]:
                    
        #             pass


