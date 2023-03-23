"""
Tabu Search Class
"""
import copy
import random

from Domain.Models.Enums.Grade import Grade
from TabuSearch.StaticMethods import *

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
        self.maxits = 50
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

    def makeMove(self, move):
        if move is None:
            pass
        else:
            if move[1]: # If move changes the day night split
                dayNurses = []
                for nurse in self.bestSolution: # Find all nurses that works during the day
                    if not nurse.worksNight:
                        dayNurses.append(nurse.id)
                self.dayNightTabuList.append(dayNurses)
                if len(self.dayNightTabuList) == 7:
                    self.dayNightTabuList.pop(6)
                self.dayNightCounter = 0
                self.lowerBound = None  # TODO: Calculate lowerbound Eq.(6)
            else:  # if move does not change the day night split
                self.dayNightCounter += 1
            self.bestSolution = move[0]

    def run(self):
        # Phase 1:
        while self.bestSolution.CC > 0:
            if self.makeMove(self.randomDecent(self.bestSolution)) is None:
                if self.makeMove(self.balanceRestoring(self.bestSolution)) is None:
                    if self.makeMove(self.shiftChain(self.bestSolution)) is None:
                        if self.makeMove(self.nurseChain(self.bestSolution)) is None:
                            if self.makeMove(self.underCovering(self.bestSolution)) is None:
                                self.makeMove(self.randomKick(self.bestSolution))


    # Phase 1 Moves:

    # TODO: Random decent after PC and LB
    def randomDecent(self, schedule):
        """
        Step 1.1 (Random decent). Carry out random decent by accepting the first neighbourhood move that satisfies
        non-tabu conditions 1 - 3 and improves CC and does not increase PC. Repeat until no satisfactory move exists.
        :param schedule:
        :return move, changed day/night:
        """
        print("Running Random Descent...")
        for nurse in schedule.nurses:
            if nurse.id not in self.tabuList:
                for pattern in self.feasiblePatterns[nurse.id]:
                    if (nurse.worksNight and pattern.day == [0] * 7) or (not nurse.worksNight and pattern.day != [0] * 7):
                        neighbour = copy.deepcopy(schedule)
                        n_nurse = neighbour.nurses[nurse.id]
                        neighbour.assignPatternToNurse(n_nurse, pattern)
                        neighbour.CC = evaluateCC(neighbour)
                        neighbour.PC = evaluatePC(neighbour)
                        if neighbour.CC < schedule.CC: #and neighbour.PC <= schedule.PC:
                            self.tabuList = []
                            self.tabuList.append(nurse.id)
                            return neighbour, False
        return None

    def balanceRestoring(self, schedule):
        """
        Step 1.2 (Balance days and nights). Check for balance by lower bound (Eq(5)). if
        :param schedule:
        :return:
        """
        print("Running Balance Restoration...")

    def shiftChain(self, schedule):
        """
        Step 1.3 For each of the grades, attempt to find a chain of moves using Shift Chain Neighbourhood from s_now to s_final, so that CC is reduced and PC does not increase
        :param schedule:
        :return: move
        """
        print("Running Shift Chain...")
        return None

    def nurseChain(self, schedule):
        """
        Step 1.4 For each of the grades, attempt to find a chain of moves from Nurse Chain Neighbourhood s_now to s_final, so that CC is reduced and PC does not increase
        :param schedule:
        :return: move
        """
        print("Running Nurse Chain...")
        return None

    def underCovering(self, schedule):
        """
        Step 1.5 Select the best move according to CC that satisfies non-tabu conditions 1 and 2 that improve the cover for one shift (although makes other worse)
        :param schedule:
        :return: move
        """
        print("Running Under Covering...")
        return None

    def randomKick(self, schedule):
        """
        Step 1.6 Randomly select a move satisfying non-tabu conditions 1-3.
        :param schedule:
        :return: move
        """
        print("Running Random Kick...")
        validMove = False
        while not validMove:
            nurse = schedule.nurses[random.randint(0, len(schedule.nurses))]
            nurseWorkedNight = copy.copy(nurse.worksNight)
            if nurse.id not in self.tabuList:
                pattern = self.feasiblePatterns[nurse.id][random.randint(0, len(self.feasiblePatterns[nurse.id]))]
                neighbour = copy.deepcopy(schedule)
                n_nurse = neighbour.nurses[nurse.id]
                neighbour.assignPatternToNurse(n_nurse, pattern)
                evaluateCC(neighbour)
                evaluatePC(neighbour)
                self.tabuList = []
                self.tabuList.append(nurse.id)
                return neighbour, nurseWorkedNight != n_nurse.worksNight