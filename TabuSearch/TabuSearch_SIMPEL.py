"""
Tabu Search Class
"""
import copy
import random

import networkx as nx
import matplotlib.pyplot as plt

from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from Domain.Models.Enums.Grade import Grade
from TabuSearch.StaticMethods import *


# TODO: THIS SOLUTION IS ONLY BASED ON GRADE THREE

class TabuSearch_SIMPLE:
    def __init__(self,
                 initialSolution):  # (initialSolution, solutionEvaluator, neighborOperator, aspirationCriteria, acceptableScoreThreshold, tabuTenure)
        """
        The next three variables is there to make sure that we hold the 3 tabu criteria:
            1) A move involves the tabu nurse (i.e. the nurse moved last time) from tabuList.
            2) A move results in a tabu configuration on the dayNightTabuList.
            3) The dayNightCounter exceeds maxits and the move does not change the day night split.
        """
        # Tabu criteria 1: tabulist - Nurses involved in earlier moves - This is a fixed length of 1
        self.tabuList = []

        # Tabu criteria 2:dayNightTabuList - Nurses working days - list[set(nurse working days), ...] - Length 6 (binary representation)
        self.dayNightTabuList = []  # TODO: Maybe this should be an array of sets for makeing easy and quick comparisons
        firstTabuSet = set()
        for n in initialSolution.nurses:
            if n.worksNight is False:
                firstTabuSet.add(n.id)
        self.dayNightTabuList.append(firstTabuSet)

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

    def initSchedule(
            self):  # Just assigning the first pattern to every nurse for testing purposes, instead of randomized, since it solves it too fast with a randomized initial solution.
        for nurse in self.bestSolution.nurses:
            randomizeConstraints(nurse)
            # self.bestSolution.assignPatternToNurse(nurse, self.feasiblePatterns[nurse.id][0])
            self.bestSolution.assignPatternToNurse(nurse, self.feasiblePatterns[nurse.id][
                random.randint(0, len(self.feasiblePatterns[nurse.id]) - 1)])

    # TODO: There was a mistake here. We need tests for this also.
    # TODO: This has to take count for TabuList also instead of the methods does it
    def makeMove(self, move):
        if move is None:
            return None
        else:
            if move[1]:  # If move changes the day night split
                dayNurses = set()
                for nurse in move[0].nurses:  # Find all nurses that works during the day
                    if not nurse.worksNight:
                        dayNurses.add(nurse.id)
                self.dayNightTabuList.insert(0, dayNurses)
                if len(self.dayNightTabuList) == 7:
                    self.dayNightTabuList.pop(6)
                self.dayNightCounter = 0
                self.lowerBound = None  # TODO: Calculate lowerbound Eq.(6)
            else:  # if move does not change the day night split
                self.dayNightCounter += 1
            self.bestSolution = move[0]
            return move[0]

    def run(self):
        # Phase 0:
        # self.initSchedule()
        # Phase 1:
        while self.bestSolution.CC > 0:
            if self.makeMove(self.randomDecent(self.bestSolution)) is None:
                if self.makeMove(self.balanceRestoring(self.bestSolution, False)) is None:
                    if self.makeMove(self.shiftChain(self.bestSolution)) is None:
                        if self.makeMove(self.nurseChain(self.bestSolution)) is None:
                            if self.makeMove(self.underCovering(self.bestSolution)) is None:
                                self.makeMove(self.randomKick(self.bestSolution))

    # Phase 1 Moves:
    # TODO: Random decent after PC and LB
    # TODO: Is Tabu criteria 2 taken into count here?
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
                    if (nurse.worksNight and pattern.day == [0] * 7) or (
                            not nurse.worksNight and pattern.day != [0] * 7):
                        if calculateDifferenceCC(schedule, nurse, pattern) < 0 and calculateDifferencePC(nurse,
                                                                                                         pattern) <= 0:
                            neighbour = copy.deepcopy(schedule)
                            n_nurse = neighbour.nurses[nurse.id]
                            neighbour.assignPatternToNurse(n_nurse, pattern)
                            self.tabuList = []
                            self.tabuList.append(nurse.id)
                            print(neighbour.scores())
                            return neighbour, False
        return None

    # TODO: Test this balanceRestoring()
    def balanceRestoring(self, schedule, relaxed):
        """
        Step 1.2.1 (Balance days and nights). Check for balance by using checkBalance (Eq(5)) and return None if nether
        days and nights is satisfied. Attempt to correct the balance by selection the best move satisfying non-tabu
        conditions 1 and 2 using a candidate list given by:
            1. moves that reduce the shortfall on nights without increasing that on days if night are short.
            2. moves that reduce the shortfall on days without increasing that on nights if days are short.
        If no such move exists extend neighbourhood to allow a night and day nurse to swap types subject to improving
        the shortfall of one type without increasing the other. If still not successful relax tabu status and repeat.
        :param schedule:
        :param relaxed:
        :return: move, changed day/night:
        """
        print("Running Balance Restoration...")
        balance = checkBalance(schedule)
        ccAndMove = 0, None
        if balance == (False, False):  # There are not enough nurses on days or nights
            return None
        elif balance == (True, True):  # There are enough nurses on days and nights
            return None
        elif balance == (False, True):  # There are not enough nurses on days
            for nurse in schedule.nurses:
                if nurse.worksNight is True:
                    if nurse.id not in self.tabuList or relaxed:
                        tabuCon = False
                        tabuCheck = copy.copy(self.dayNightTabuList[0])
                        tabuCheck.add(nurse.id)
                        if tabuCheck in self.dayNightTabuList:  # Calculate if the move is making a tabu configuration on the dayNightTabulist
                            tabuCon = True

                        if tabuCon is False or relaxed:
                            for pattern in self.feasiblePatterns[nurse.id]:
                                diffCC = calculateDifferenceCC(schedule, nurse, pattern)
                                if diffCC < ccAndMove[0] and pattern.night == [0] * 7:
                                    ccAndMove = diffCC, (nurse, pattern)
        elif balance == (True, False):  # There are not enough nurses on nights
            for nurse in schedule.nurses:
                if nurse.worksNight is False:
                    if nurse.id not in self.tabuList or relaxed:
                        tabuCon = False
                        tabuCheck = copy.copy(self.dayNightTabuList[0])
                        tabuCheck.add(nurse.id)
                        if tabuCheck in self.dayNightTabuList:  # Calculate if the move is making a tabu configuration on the dayNightTabulist
                            tabuCon = True

                        if tabuCon is False or relaxed:
                            for pattern in self.feasiblePatterns[nurse.id]:
                                diffCC = calculateDifferenceCC(schedule, nurse, pattern)
                                if diffCC < ccAndMove[0] and pattern.day == [0] * 7:
                                    ccAndMove = diffCC, (nurse, pattern)

        if ccAndMove[0] != 0:
            move = ccAndMove[1]
            neighbour = copy.deepcopy(schedule)
            n_nurse = neighbour.nurses[move[0].id]
            neighbour.assignPatternToNurse(n_nurse, move[1])
            self.tabuList = []
            self.tabuList.append(n_nurse.id)
            print(neighbour.scores())
            return neighbour, True
        else:
            return self.balanceSwap(schedule, relaxed)

    def balanceSwap(self, schedule, relaxed):
        """
        Step 1.2.2 (Balance Swap). Allow a night and a day nurse to swap types subjects to improve the shortfall in one
        type without increasing the other.
        :param schedule:
        :param relaxed:
        :return move, with two swapped nurses:
        """
        print("Running Balance Swap...")
        ccAndMove = 0, None
        for nurse1 in schedule.nurses:
            if nurse1.worksNight and (nurse1.id not in self.tabuList or relaxed):
                for nurse2 in schedule.nurses:
                    if not nurse2.worksNight and (nurse2.id not in self.tabuList or relaxed):
                        tabuCon = False
                        tabuCheck = copy.copy(self.dayNightTabuList[0])
                        tabuCheck.add(nurse1.id)
                        if nurse2.id in tabuCheck:
                            tabuCheck.remove(nurse2.id)
                        if tabuCheck in self.dayNightTabuList:  # Calculate if the move is making a tabu configuration on the dayNightTabulist
                            tabuCon = True
                        if tabuCon is False or relaxed:
                            for pattern1 in self.feasiblePatterns[nurse1.id]:
                                if pattern1.night == [0] * 7:
                                    for pattern2 in self.feasiblePatterns[nurse2.id]:
                                        if pattern2.day == [0] * 7:
                                            ccval = calculateDifferenceDuoCC(schedule, nurse1, nurse2, pattern1, pattern2)
                                            if ccval < ccAndMove[0]:
                                                ccAndMove = ccval, (nurse1, nurse2, pattern1, pattern2)

        if ccAndMove[0] != 0:
            moves = ccAndMove[1]
            neighbour = copy.deepcopy(schedule)
            n_nurse1 = neighbour.nurses[moves[0].id]
            n_nurse2 = neighbour.nurses[moves[1].id]
            neighbour.assignPatternToNurse(n_nurse1, moves[2])
            neighbour.assignPatternToNurse(n_nurse2, moves[3])
            self.tabuList = []
            self.tabuList.append(n_nurse1.id)
            self.tabuList.append(n_nurse2.id)
            print(neighbour.scores())
            return neighbour, True
        else:
            if not relaxed:
                print("Relaxing Balance Restoration...")
                self.balanceRestoring(schedule, True)
            else:
                return None


    def shiftChain(self, schedule):
        """
        Step 1.3 For each of the grades, attempt to find a chain of moves using Shift Chain Neighbourhood from s_now to s_final, so that CC is reduced and PC does not increase
        :param schedule:
        :return move, changed day/night:
        """
        print("Running Shift Chain...")
        return None
        overCovered = []
        underCovered = []
        Gday = nx.MultiDiGraph()
        for shift in schedule.shifts:
            if shift.coverRequirements[Grade.ONE] - len(shift.assignedNurses[Grade.ONE]) < 0:
                overCovered.append(shift)
            elif shift.coverRequirements[Grade.ONE] - len(shift.assignedNurses[Grade.ONE]) > 0:
                underCovered.append(shift)

        if len(overCovered) == 0 or len(underCovered) == 0:
            return None

        for nurse in schedule.nurses:
            if not nurse.worksNight:
                for i in range(7):
                    if nurse.shiftPattern.day[i] == 1:
                        for j in range(7):
                            if nurse.shiftPattern.day[j] == 0:
                                patternDay = copy.copy(nurse.shiftPattern.day)
                                patternDay[i] = 0
                                patternDay[j] = 1
                                Gday.add_edge(i, j, weight=calculateDifferencePC(nurse, TabuShiftPattern(patternDay, [0]*7)))
        print(str(Gday))
        nx.draw(Gday)
        plt.show()
        print(list(nx.dfs_edges(Gday, 0, 5)))


    def nurseChain(self, schedule):
        """
        Step 1.4 For each of the grades, attempt to find a chain of moves from Nurse Chain Neighbourhood s_now to s_final, so that CC is reduced and PC does not increase
        :param schedule:
        :return: move, changed day/night:
        """
        print("Running Nurse Chain...")
        return None

    def underCovering(self, schedule):
        """
        Step 1.5 Select the best move according to CC that satisfies non-tabu conditions 1 and 2 that improve the cover for one shift (although makes other worse)
        :param schedule:
        :return: move, changed day/night:
        """
        print("Running Under Covering...")
        return None

    def randomKick(self, schedule):
        """
        Step 1.6 Randomly select a move satisfying non-tabu conditions 1-3.
        :param schedule:
        :return: move, changed day/night:
        """
        print("Running Random Kick...")
        while True:
            nurse = schedule.nurses[random.randint(0, len(schedule.nurses) - 1)]
            nurseWorkedNight = copy.copy(nurse.worksNight)
            if nurse.id not in self.tabuList:
                pattern = self.feasiblePatterns[nurse.id][random.randint(0, len(self.feasiblePatterns[nurse.id]) - 1)]
                neighbour = copy.deepcopy(schedule)
                n_nurse = neighbour.nurses[nurse.id]
                neighbour.assignPatternToNurse(n_nurse, pattern)
                self.tabuList = []
                self.tabuList.append(nurse.id)
                print(neighbour.scores())
                return neighbour, nurseWorkedNight != n_nurse.worksNight
        pass