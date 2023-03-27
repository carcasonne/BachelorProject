"""
Tabu Search Class
"""
import copy
import random

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

        self.shiftRequirements = findShiftTypeRequirements(initialSolution)

    def initSchedule(
            self):  # Just assigning the first pattern to every nurse for testing purposes, instead of randomized, since it solves it too fast with a randomized initial solution.
        for nurse in self.bestSolution.nurses:
            randomizeConstraints(nurse)
            # self.bestSolution.assignPatternToNurse(nurse, self.feasiblePatterns[nurse.id][0])
            self.bestSolution.assignPatternToNurse(nurse, self.feasiblePatterns[nurse.id][
                random.randint(0, len(self.feasiblePatterns[nurse.id]) - 1)])

    def makeMove(self, move):
        if move is None:
            return None
        else:
            if move[1]:  # If move changes the day night split
                dayNurses = []
                for nurse in self.bestSolution.nurses:  # Find all nurses that works during the day
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
            return move[0]

    def run(self):
        # Phase 0:
        # self.initSchedule()
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
    def balanceRestoring(self, schedule):
        """
        Step 1.2 (Balance days and nights). Check for balance by using checkBalance (Eq(5)) and return None if nether
        days and nights is satisfied. Attempt to correct the balance by selection the best move satisfying non-tabu
        conditions 1 and 2 using a candidate list given by:
            1. moves that reduce the shortfall on nights without increasing that on days if night are short.
            2. moves that reduce the shortfall on days without increasing that on nights if days are short.
        If no such move exists extend neighbourhood to allow a night and day nurse to swap types subject to improving
        the shortfall of one type without increasing the other. If still not successful relax tabu status and repeat.
        :param schedule:
        :return: move, changed day/night:
        """
        print("Running Balance Restoration...")
        balance = checkBalance(schedule)
        moveList = []
        match balance:
            case (False, False):  # There are not enough nurses on days or nights
                return None
            case (True, True):  # There are enough nurses on days and nights
                return None
            case (False, True):  # There are not enough nurses on days
                for nurse in schedule.nurses:
                    if nurse.id not in self.tabuList and nurse.worksNight is True:
                        for pattern in self.feasiblePatterns[nurse.id]:
                            diffCC = calculateDifferenceCC(schedule, nurse, pattern)
                            if diffCC < 0 and pattern.night == [0] * 7:
                                # TODO: We need to take tabu criteria 2 into count here
                                moveList.append((diffCC, (nurse, pattern)))
            case (True, False):  # There are not enough nurses on nights
                for nurse in schedule.nurses:
                    if nurse.id not in self.tabuList and nurse.worksNight is False:
                        for pattern in self.feasiblePatterns[nurse.id]:
                            diffCC = calculateDifferenceCC(schedule, nurse, pattern)
                            if diffCC < 0 and pattern.day == [0] * 7:
                                # TODO: We need to take tabu criteria 2 into count here
                                moveList.append((diffCC, (nurse, pattern)))

        if len(moveList) != 0:
            move = (None, None)
            bestCC = 0
            for m in moveList:
                if bestCC > m[0]:
                    move = m[1]

            neighbour = copy.deepcopy(schedule)
            n_nurse = neighbour.nurses[move[0].id]
            neighbour.assignPatternToNurse(n_nurse, move[1])
            self.tabuList = []
            self.tabuList.append(n_nurse.id)
            print(neighbour.scores())
            return neighbour, True
        else:
            # TODO: Make method balanceSwap(): swap nurses to allow for balance restoring.
            return None

    def shiftChain(self, schedule):
        """
        Step 1.3 For each of the grades, attempt to find a chain of moves using Shift Chain Neighbourhood from s_now to s_final, so that CC is reduced and PC does not increase
        :param schedule:
        :return: move, changed day/night:
        """
        print("Running Shift Chain...")
        return None

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

    def findBalanceRestoringCandidateList(self, schedule: TabuSchedule):
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
