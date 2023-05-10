"""
Tabu Search Class
"""
import copy
import random

from TabuSearch.StaticMethods import *
from TabuSearch.DirectedGraph import DirectedGraph


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
        self.dayNightTabuList = []
        firstTabuSet = set()
        for n in initialSolution.nurses:
            if n.worksNight is False:
                firstTabuSet.add(n.id)
        self.dayNightTabuList.append(firstTabuSet)

        # Tabu criteria 3:
        self.dayNightCounter = 0
        self.maxits = 50
        self.lowerBound = None
        # Feasible shift patterns for nurses is provided in this dict
        self.feasiblePatterns = dict()
        for n in initialSolution.nurses:
            self.feasiblePatterns[n.id] = findFeasiblePatterns(n)

        initialSolution.PC = 1000000  # Sat to a very high value, since it would otherwise be 0, and a best solution would never be found because of this.

        self.currSolution = copy.deepcopy(initialSolution)
        self.bestSolution = copy.deepcopy(initialSolution)
        self.lowerBound = evaluateLB(self.bestSolution, self.feasiblePatterns)

        self.foundOptimalSolution = False

        self.stepsP1 = [0, 0, 0, 0, 0, 0]
        self.stepsP2 = [0, 0, 0]
        self.stepsP3 = [0]
        self.iterations = 0
        self.iterationsNoImprovements = 0
        self.currentPhase = 1

        self.useBalanceSwap = True
        self.debug = False

        self.excelSheet = None

    def initSchedule(self):
        """
        initSchedule. An old method which some tests still rely on, since it is much simpler to let the search ramdomly set patterns
        of all of the nurses in the tests, than it is to initialize knapsack which otherwise does this for the search.
        """
        for nurse in self.currSolution.nurses:
            # randomizeConstraints(nurse)
            self.currSolution.assignPatternToNurse(nurse, self.feasiblePatterns[nurse.id][
                random.randint(0, len(self.feasiblePatterns[nurse.id]) - 1)])

    # TODO: There was a mistake here. We need tests for this also.
    def makeMove(self, move):
        """
        makeMove. Execute the move and calculate if any nurses was moved from day to night or vice versa. Update the
        dayNightTabuList accordingly. Also update dayNightCounter and set maxits accordingly to 5 in case the lowerBound
        is reached, or 50 otherwise. Set the currentSolution to the neighbour the move results in and return the move.
        In case the move was None, return None.
        :param move:
        :return move OR None:
        """
        if move is None:
            return None
        else:
            self.iterations += 1
            self.iterationsNoImprovements += 1
            if move[1]:  # If move changes the day night split
                dayNurses = set()
                for nurse in move[0].nurses:  # Find all nurses that works during the day
                    if not nurse.worksNight:
                        dayNurses.add(nurse.id)
                self.dayNightTabuList.insert(0, dayNurses)
                if len(self.dayNightTabuList) == 7:
                    self.dayNightTabuList.pop(6)
                self.dayNightCounter = 0
                self.lowerBound = evaluateLB(move[0], self.feasiblePatterns)
                if self.lowerBound < move[0].PC:
                    self.maxits = 50
                else:
                    self.maxits = 5
            else:  # if move does not change the day night split
                self.dayNightCounter += 1
            self.currSolution = move[0]
            self._safeMoveToExcel(self.iterations, self.currSolution.CC, self.currSolution.PC, self.currentPhase)
            return move[0]

    def run(self, maxRuns, useBalanceSwap, debugmode, oneKMoves):
        """
        run. Execute Tabu Search with maxRuns amount of runs. Find out which solution is best according to PC and
        return that.
        :return bestSolution:
        """
        self.useBalanceSwap = useBalanceSwap
        self.debug = debugmode

        if oneKMoves:
            self.runOneKMoves()

        runs = 0
        if self.debug:
            print(str(self.currSolution))

        while runs < maxRuns and not self.foundOptimalSolution:
            if runs % 10 == 0:
                print("Initiating run #" + str(runs))
            self._phase1()
            self._phase2(runs)
            if runs + 1 != maxRuns:
                self._phase3()

            runs += 1
        if self.debug:
            print(str(self.bestSolution))
        self._safeMoveToExcel(self.iterations+3, self.bestSolution.CC, self.bestSolution.PC, "Final solution, the best run")
        return self.bestSolution

    def runOneKMoves(self):
        firstRun = True
        runs = 0
        if self.debug:
            print(str(self.currSolution))

        while (self.iterationsNoImprovements < 1000 or firstRun) and not self.foundOptimalSolution:
            if runs % 10 == 0:
                print("Initiating run #" + str(runs))
            self._phase1()
            self._phase2(runs)
            self._phase3()

            runs += 1
            firstRun = False
        if self.debug:
            print(str(self.bestSolution))
        self._safeMoveToExcel(self.iterations + 3, self.bestSolution.CC, self.bestSolution.PC,
                              "Final solution, the best run")
        return self.bestSolution

    def _safeMoveToExcel(self, iteration, CC, PC, phase):
        rowNumber = 1 + iteration
        self.excelSheet[f"A{rowNumber}"] = iteration
        self.excelSheet[f"B{rowNumber}"] = CC
        self.excelSheet[f"C{rowNumber}"] = PC
        self.excelSheet[f"D{rowNumber}"] = phase

    def _phase1(self):
        """
        phase1. Execute the moves in the following order: randomDescent, balanceRestoring, shiftChain, nurseChain,
        underCovering, randomKick.
        """
        self.currentPhase = 1
        while self.currSolution.CC > 0:
            if self.makeMove(self.randomDecent(self.currSolution, 1)) is None:
                if self.makeMove(self.balanceRestoring(self.currSolution, False)) is None:
                    if self.makeMove(self.shiftChain(self.currSolution, 1)) is None:
                        if self.makeMove(self.nurseChain(self.currSolution, 1)) is None:
                            if self.makeMove(self.underCovering(self.currSolution)) is None:
                                self.makeMove(self.randomKick(self.currSolution))
                                self.stepsP1[5] += 1
                                if self.debug:
                                    print(self.currSolution.scores())
                            else:
                                self.stepsP1[4] += 1
                                if self.debug:
                                    print("XXX")
                                    print(self.currSolution.scores())
                        else:
                            self.stepsP1[3] += 1
                            if self.debug:
                                print(self.currSolution.scores())
                    else:
                        self.stepsP1[2] += 1
                        if self.debug:
                            print(self.currSolution.scores())
                else:
                    self.stepsP1[1] += 1
                    if self.debug:
                        print(self.currSolution.scores())
            else:
                self.stepsP1[0] += 1
                if self.debug:
                    print(self.currSolution.scores())

    def _phase2(self, runs):
        """
        phase1. Execute the moves in the following order: randomDescent, shiftChain, nurseChain.
        """
        self.currentPhase = 2
        while self.currSolution.PC > 0:
            if self.makeMove(self.randomDecent(self.currSolution, 2)) is None:
                if self.makeMove(self.shiftChain(self.currSolution, 2)) is None:
                    if self.makeMove(self.nurseChain(self.currSolution, 2)) is not None:
                        self.stepsP2[2] += 1
                        if self.debug:
                            print(self.currSolution.scores())

                    else:
                        if self.currSolution.PC < self.bestSolution.PC:
                            print()
                            print("FOUND A BETTER SOLUTION THAN THE LAST ONE!")
                            print("RUN: " + str(runs) + " PC: FROM: " + str(self.bestSolution.PC) + " TO: " + str(
                                self.currSolution.PC))
                            print()
                            if self.debug:
                                print(str(self.currSolution))
                            self.iterationsNoImprovements = 0
                            self.bestSolution = copy.deepcopy(self.currSolution)
                        print("Iterations: " + str(self.iterations))
                        print("Iterations since last improvement: " + str(self.iterationsNoImprovements))
                        break
                else:
                    self.stepsP2[1] += 1
                    if self.debug:
                        print(self.currSolution.scores())
            else:
                self.stepsP2[0] += 1
                if self.debug:
                    print(self.currSolution.scores())

    def _phase3(self):
        """
        phase1. Execute the move searchStuck.
        """
        self.currentPhase = 3
        if self.makeMove(self.searchStuck(self.currSolution)) is not None:
            self.stepsP3[0] += 1
            if self.debug:
                print(self.currSolution.scores())
        else:
            self.foundOptimalSolution = True
            print(str(self.bestSolution))
            print("***THIS IS THE BEST SOLUTION WE CAN EVER FIND.***")
            print("***THERE IS NO MOVE FOR ANY NURSE AT ALL THAT WOULD EVER DECREASE PC.***")

    # Phase 1 Moves:
    def randomDecent(self, schedule, phase):
        """
        Step 1.1 (Random decent). Carry out random decent by accepting the first neighbourhood move that satisfies
        non-tabu conditions 1 - 3 and improves CC and does not increase PC. Repeat until no satisfactory move exists.
        :param schedule:
        :param phase:
        :return move, changed day/night:
        """
        if self.debug:
            print("Running Random Descent...")
        if self.dayNightCounter >= self.maxits:
            return self.descentDayNightChange(schedule, phase)

        for nurse in schedule.nurses:
            if nurse.id not in self.tabuList:
                for pattern in self.feasiblePatterns[nurse.id]:
                    if (nurse.worksNight and pattern.day == [0] * 7) or (
                            not nurse.worksNight and pattern.day != [0] * 7):
                        if (calculateDifferenceCC(schedule, nurse, pattern) < 0 and calculateDifferencePC(nurse,
                                                                                                          pattern) <= 0 and phase == 1) or (
                                calculateDifferencePC(nurse, pattern) < 0 and calculateDifferenceCC(schedule, nurse,
                                                                                                    pattern) <= 0 and phase == 2):
                            neighbour = copy.deepcopy(schedule)
                            n_nurse = neighbour.nurses[nurse.id]
                            neighbour.assignPatternToNurse(n_nurse, pattern)
                            self.tabuList = []
                            self.tabuList.append(nurse.id)
                            return neighbour, False
        return None

    def descentDayNightChange(self, schedule, phase):
        """
        Step 1.1.2 (Random decent criteria 3). Carry out random decent by accepting the first neighbourhood move that satisfies
        non-tabu conditions 1 - 3 and improves CC and does not increase PC, forced to switch the chosen nurse to a pattern
        opposite of what they are currently working, to satisfy tabu condition 3
        :param schedule:
        :param phase:
        :return move, changed day/night:
        """
        if self.debug:
            print("Forcing Random Descent to make a day to night or night to day...")
        for nurse in schedule.nurses:
            if nurse.id not in self.tabuList:
                tabuCheck = copy.copy(self.dayNightTabuList[0])
                if nurse.worksNight:
                    tabuCheck.add(nurse.id)
                else:
                    if nurse.id in tabuCheck:
                        tabuCheck.remove(nurse.id)
                if tabuCheck not in self.dayNightTabuList:
                    for pattern in self.feasiblePatterns[nurse.id]:
                        if (nurse.worksNight and pattern.night == [0] * 7) or (
                                not nurse.worksNight and pattern.night != [0] * 7):
                            if (calculateDifferenceCC(schedule, nurse, pattern) < 0 and calculateDifferencePC(nurse,
                                                                                                              pattern) <= 0 and phase == 1) or (
                                    calculateDifferencePC(nurse, pattern) < 0 and calculateDifferenceCC(schedule, nurse,
                                                                                                        pattern) <= 0 and phase == 2):
                                neighbour = copy.deepcopy(schedule)
                                n_nurse = neighbour.nurses[nurse.id]
                                neighbour.assignPatternToNurse(n_nurse, pattern)
                                self.tabuList = []
                                self.tabuList.append(nurse.id)
                                return neighbour, True
        return None

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
        if self.debug:
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
                        if nurse.id in tabuCheck:
                            tabuCheck.remove(nurse.id)
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
        if self.useBalanceSwap is False:
            if relaxed:
                return None
            else:
                return self.balanceRestoring(schedule, True)

        if self.debug:
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
                                            ccval = calculateDifferenceDuoCC(schedule, nurse1, nurse2, pattern1,
                                                                             pattern2)
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
            return neighbour, True
        else:
            if not relaxed:
                if self.debug:
                    print("Relaxing Balance Restoration...")
                return self.balanceRestoring(schedule, True)
            else:
                return None

    # TODO: Function is kinda scuffed. Make it better computationally.
    def shiftChain(self, schedule, phase):
        """
        Step 1.3 For each of the grades, attempt to find a chain of moves using Shift Chain Neighbourhood from s_now to s_final, so that CC is reduced and PC does not increase
        :param schedule:
        :param phase:
        :return move, changed day/night:
        """
        if self.debug:
            print("Running Shift Chain...")

        for grade in [Grade.ONE, Grade.TWO, Grade.THREE]:

            utilities = self._shiftChainUtil(schedule, grade, phase)
            if utilities is not None and phase == 1:
                (overCovered, underCovered, dayGraph, nightGraph) = utilities

                for oShift in (overCovered[0] + overCovered[1]):
                    if oShift.shiftType == TabuShiftType.DAY:
                        for uShift in underCovered[0]:
                            if uShift.shiftType == TabuShiftType.DAY:
                                neighbour = copy.deepcopy(schedule)
                                edges = dayGraph.search(oShift.shiftDay.value - 1, uShift.shiftDay.value - 1)
                                if len(edges) > 0:
                                    tempTabuList = []
                                    for edge in edges:
                                        nurse = neighbour.nurses[edge.nurseId]
                                        patternDay = copy.copy(nurse.shiftPattern.day)
                                        patternDay[edge.fromNode] = 0
                                        patternDay[edge.toNode] = 1
                                        neighbour.assignPatternToNurse(nurse, TabuShiftPattern(patternDay, [0] * 7))
                                        tempTabuList.append(nurse.id)
                                else:
                                    return None
                                if schedule.CC > neighbour.CC:
                                    if self.debug:
                                        print("Performing chain operation on day...")
                                    self.tabuList = tempTabuList
                                    return neighbour, False

                    else:
                        for uShift in underCovered[1]:
                            if uShift.shiftType == TabuShiftType.NIGHT:
                                neighbour = copy.deepcopy(schedule)
                                edges = nightGraph.search(oShift.shiftDay.value - 1, uShift.shiftDay.value - 1)
                                if len(edges) > 0:
                                    tempTabuList = []
                                    for edge in edges:
                                        nurse = neighbour.nurses[edge.nurseId]
                                        patternNight = copy.copy(nurse.shiftPattern.night)
                                        patternNight[edge.fromNode] = 0
                                        patternNight[edge.toNode] = 1
                                        neighbour.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, patternNight))
                                        tempTabuList.append(nurse.id)
                                else:
                                    return None
                                if schedule.CC > neighbour.CC:
                                    if self.debug:
                                        print("Performing chain operation on night...")
                                    self.tabuList = tempTabuList
                                    return neighbour, False


            elif phase == 2:
                (fromShifts, toShifts, dayGraph, nightGraph) = utilities

                for shift in fromShifts[0] + fromShifts[1]:
                    if shift.shiftType == TabuShiftType.DAY:
                        neighbour = copy.deepcopy(schedule)
                        edges = dayGraph.search(shift.shiftDay.value - 1, shift.shiftDay.value - 1)
                        if len(edges) > 0:
                            tempTabuList = []
                            for edge in edges:
                                nurse = neighbour.nurses[edge.nurseId]
                                patternDay = copy.copy(nurse.shiftPattern.day)
                                patternDay[edge.fromNode] = 0
                                patternDay[edge.toNode] = 1
                                neighbour.assignPatternToNurse(nurse, TabuShiftPattern(patternDay, [0] * 7))
                                tempTabuList.append(nurse.id)
                        else:
                            continue
                        if schedule.PC > neighbour.PC and schedule.CC == neighbour.CC:
                            if self.debug:
                                print("Performing chain operation on day...")
                            self.tabuList = tempTabuList
                            return neighbour, False

                    else:
                        neighbour = copy.deepcopy(schedule)
                        edges = nightGraph.search(shift.shiftDay.value - 1, shift.shiftDay.value - 1)
                        if len(edges) > 0:
                            tempTabuList = []
                            for edge in edges:
                                nurse = neighbour.nurses[edge.nurseId]
                                patternNight = copy.copy(nurse.shiftPattern.night)
                                patternNight[edge.fromNode] = 0
                                patternNight[edge.toNode] = 1
                                neighbour.assignPatternToNurse(nurse, TabuShiftPattern([0] * 7, patternNight))
                                tempTabuList.append(nurse.id)
                        else:
                            continue
                        if schedule.PC > neighbour.PC and schedule.CC == neighbour.CC:
                            if self.debug:
                                print("Performing chain operation on night...")
                            self.tabuList = tempTabuList
                            return neighbour, False

    def _shiftChainUtil(self, schedule, grade, phase):
        if self.debug:
            print("Checking grade: " + str(grade.value) + "...")
        fromShifts = ([], [])
        toShifts = ([], [])
        dayGraph = DirectedGraph()
        nightGraph = DirectedGraph()

        if phase == 1:

            for shift in schedule.shifts:
                if shift.coverRequirements[grade] - len(shift.assignedNurses[grade]) < 0:
                    if shift.shiftType == TabuShiftType.DAY:
                        fromShifts[0].append(shift)
                    else:
                        fromShifts[1].append(shift)
                elif shift.coverRequirements[grade] - len(shift.assignedNurses[grade]) > 0:
                    if shift.shiftType == TabuShiftType.DAY:
                        toShifts[0].append(shift)
                    else:
                        toShifts[1].append(shift)

                if shift.shiftType == TabuShiftType.NIGHT:
                    nightGraph.addNode(shift.shiftDay.value - 1)
                else:
                    dayGraph.addNode(shift.shiftDay.value - 1)

            if len(fromShifts) == 0 or len(toShifts) == 0:
                return None
            if (fromShifts[0] is [] or toShifts[0] is []) and (fromShifts[1] is [] or toShifts[1] is []):
                return None

        else:

            for shift in schedule.shifts:
                if shift.shiftType == TabuShiftType.DAY:
                    fromShifts[0].append(shift)
                    toShifts[0].append(shift)
                    dayGraph.addNode(shift.shiftDay.value - 1)
                elif shift.shiftType == TabuShiftType.NIGHT:
                    fromShifts[1].append(shift)
                    toShifts[1].append(shift)
                    nightGraph.addNode(shift.shiftDay.value - 1)

        for nurse in schedule.nurses:
            if not nurse.worksNight and nurse.grade == grade:
                for i in range(7):
                    if nurse.shiftPattern.day[i] == 1:
                        for j in range(7):
                            if nurse.shiftPattern.day[j] == 0:
                                patternDay = copy.copy(nurse.shiftPattern.day)
                                patternDay[i] = 0
                                patternDay[j] = 1
                                dayGraph.addEdge(i, j, nurse.id,
                                                 calculateDifferencePC(nurse, TabuShiftPattern(patternDay, [0] * 7)))
            elif nurse.worksNight and nurse.grade == grade:
                for i in range(7):
                    if nurse.shiftPattern.night[i] == 1:
                        for j in range(7):
                            if nurse.shiftPattern.night[j] == 0:
                                patternNight = copy.copy(nurse.shiftPattern.night)
                                patternNight[i] = 0
                                patternNight[j] = 1
                                nightGraph.addEdge(i, j, nurse.id, calculateDifferencePC(nurse,
                                                                                         TabuShiftPattern([0] * 7,
                                                                                                          patternNight)))

        return fromShifts, toShifts, dayGraph, nightGraph

    # TODO: There is an issue with the order of going from sink to source. Right now we are going form source to sink
    def nurseChain(self, schedule, phase):
        """
        Step 1.4 For each of the grades, attempt to find a chain of moves from Nurse Chain Neighbourhood s_now to s_final, so that CC is reduced and PC does not increase
        :param schedule:
        :param phase:
        :return: move, changed day/night:
        """
        if self.debug:
            print("Running Nurse Chain...")

        for grade in [Grade.ONE, Grade.TWO, Grade.THREE]:
            value = self._graphCreatorNurseChainUtil(schedule, grade, phase)
            if value is not None:
                return value

        return None

    def _graphCreatorNurseChainUtil(self, schedule, grade, phase):
        overCovered = []
        underCovered = []
        nurseList = []
        graph = DirectedGraph()
        for source in schedule.nurses:
            if source.grade == grade:
                nurseList.append(source)
                graph.addNode(source.id)

        for nurse1 in nurseList:
            for nurse2 in nurseList:
                if nurse2 != nurse1:
                    if nurse2.worksNight and nurse2.contract.nights == nurse1.contract.nights:
                        graph.addEdge(nurse1.id, nurse2.id, nurse1.id,
                                      calculateDifferencePC(nurse1, nurse2.shiftPattern))
                    elif nurse2.worksNight is False and nurse2.contract.days == nurse1.contract.days:
                        graph.addEdge(nurse1.id, nurse2.id, nurse1.id,
                                      calculateDifferencePC(nurse1, nurse2.shiftPattern))

        if phase == 1:
            for shift in schedule.shifts:
                if shift.coverRequirements[grade] - len(shift.assignedNurses[grade]) < 0:
                    overCovered.append(shift)
                elif shift.coverRequirements[grade] - len(shift.assignedNurses[grade]) > 0:
                    underCovered.append(shift)

            for source in nurseList:
                isSource = False
                for o in overCovered:
                    if patternCoverShift(source.shiftPattern, o):
                        for u in underCovered:
                            if patternCoverShift(source.shiftPattern, u) == 0:
                                isSource = True
                                break
                    if isSource:
                        break

                if isSource:
                    for pattern in self.feasiblePatterns[source.id]:
                        if calculateDifferenceCC(schedule, source, pattern) < 0:
                            for sink in nurseList:
                                if sink.contract == source.contract and sink.id != source.id:
                                    edges = graph.search(source.id, sink.id)
                                    if len(edges) > 0:
                                        pcCounter = 0
                                        for edge in edges:
                                            pcCounter += edge.weight
                                        pcCounter += calculateDifferencePC(
                                            schedule.nurses[edges[len(edges) - 1].toNode], pattern)
                                        if pcCounter <= 0:
                                            neighbour = copy.deepcopy(schedule)
                                            change = False
                                            temptabulist = []
                                            for edge in edges:
                                                fromN = schedule.nurses[edge.fromNode]
                                                toN = schedule.nurses[edge.toNode]
                                                temptabulist.append(edge.fromNode)
                                                if fromN.worksNight != toN.worksNight:
                                                    change = True
                                                neighbour.assignPatternToNurse(neighbour.nurses[fromN.id],
                                                                               toN.shiftPattern)
                                            temptabulist.append(sink.id)
                                            neighbour.assignPatternToNurse(neighbour.nurses[sink.id], pattern)
                                            self.tabuList = temptabulist
                                            return neighbour, change
        elif phase == 2:
            for source in nurseList:
                edges = graph.search(source.id, source.id)
                if len(edges) > 0:
                    pcCounter = 0
                    for edge in edges:
                        pcCounter += edge.weight
                    if pcCounter < 0:
                        neighbour = copy.deepcopy(schedule)
                        change = False
                        temptabulist = []
                        for edge in edges:
                            fromN = schedule.nurses[edge.fromNode]
                            toN = schedule.nurses[edge.toNode]
                            temptabulist.append(edge.fromNode)
                            if fromN.worksNight != toN.worksNight:
                                change = True
                            neighbour.assignPatternToNurse(neighbour.nurses[fromN.id], toN.shiftPattern)
                        self.tabuList = temptabulist
                        return neighbour, change
        return None

    def underCovering(self, schedule):
        """
        Step 1.5 Select the best move according to CC that satisfies non-tabu conditions 1 and 2 that improve the cover for one shift (although makes other worse)
        :param schedule:
        :return: move, changed day/night:
        """
        if self.debug:
            print("Running Under Covering...")
        bestMove = None, None, 0, None

        for nurse in schedule.nurses:
            for pattern in self.feasiblePatterns[nurse.id]:
                if nurse.id not in self.tabuList:
                    tabuCheck = copy.copy(self.dayNightTabuList[0])
                    if nurse.worksNight:
                        tabuCheck.add(nurse.id)
                    else:
                        if nurse.id in tabuCheck:
                            tabuCheck.remove(nurse.id)
                    if tabuCheck not in self.dayNightTabuList:
                        ccDif = calculateDifferenceCC(schedule, nurse, pattern)
                        if ccDif < bestMove[2]:
                            bestMove = nurse.id, pattern, ccDif, nurse.worksNight

        if bestMove[0] is None:
            return None
        else:
            neighbour = copy.deepcopy(schedule)
            n_nurse = neighbour.nurses[bestMove[0]]
            neighbour.assignPatternToNurse(n_nurse, bestMove[1])
            self.tabuList = []
            self.tabuList.append(n_nurse.id)
            return neighbour, bestMove[3] != n_nurse.worksNight

    def randomKick(self, schedule):
        """
        Step 1.6 Randomly select a move satisfying non-tabu conditions 1-3.
        :param schedule:
        :return: move, changed day/night:
        """
        if self.debug:
            print("Running Random Kick...")

        randomNurseList = list(range(0, len(schedule.nurses)))
        random.shuffle(randomNurseList)
        for index in randomNurseList:
            nurse = schedule.nurses[index]
            nurseWorkedNight = copy.copy(nurse.worksNight)
            tabuCheck = copy.copy(self.dayNightTabuList[0])
            if nurse.worksNight:
                tabuCheck.add(nurse.id)
                oldWorksNight = True
            else:
                if nurse.id in tabuCheck:
                    tabuCheck.remove(nurse.id)
                oldWorksNight = False

            if nurse.id not in self.tabuList and tabuCheck not in self.dayNightTabuList:
                pattern = self.feasiblePatterns[nurse.id][random.randint(0, len(self.feasiblePatterns[nurse.id]) - 1)]
                if (((pattern.day == [0] * 7 and not oldWorksNight) or (
                        pattern.night == [0] * 7 and oldWorksNight)) and self.dayNightCounter >= self.maxits) or (
                        self.dayNightCounter < self.maxits):
                    neighbour = copy.deepcopy(schedule)
                    n_nurse = neighbour.nurses[nurse.id]
                    neighbour.assignPatternToNurse(n_nurse, pattern)
                    self.tabuList = []
                    self.tabuList.append(nurse.id)
                    return neighbour, nurseWorkedNight != n_nurse.worksNight

    def searchStuck(self, schedule):
        """
        Step 1.6 (Search stuck - oscillate back into infeasible region). Select the best non-tabu move according to PC.
        :param schedule:
        :return: move, changed day/night:
        """
        if self.debug:
            print("Running Search Stuck...")
        bestMove = None, None, 0, None

        for nurse in schedule.nurses:
            for pattern in self.feasiblePatterns[nurse.id]:
                pcDif = calculateDifferencePC(nurse, pattern)
                if pcDif < bestMove[2]:
                    bestMove = nurse.id, pattern, pcDif, nurse.worksNight

        if bestMove[0] is not None:
            neighbour = copy.deepcopy(schedule)
            n_nurse = neighbour.nurses[bestMove[0]]
            neighbour.assignPatternToNurse(n_nurse, bestMove[1])
            self.tabuList = []
            self.tabuList.append(n_nurse.id)
            return neighbour, bestMove[3] != n_nurse.worksNight
        else:
            return None

    def printStats(self):
        print("Executed P1 Random Descent: " + str(self.stepsP1[0]) + " times.")
        print("Executed P1 Balance Restoration: " + str(self.stepsP1[1]) + " times.")
        print("Executed P1 Shift Chain: " + str(self.stepsP1[2]) + " times.")
        print("Executed P1 Nurse Chain: " + str(self.stepsP1[3]) + " times.")
        print("Executed P1 Under Covering: " + str(self.stepsP1[4]) + " times.")
        print("Executed P1 Random Kick: " + str(self.stepsP1[5]) + " times.")

        print("\n")

        print("Executed P2 Random Descent: " + str(self.stepsP2[0]) + " times.")
        print("Executed P2 Shift Chain: " + str(self.stepsP2[1]) + " times.")
        print("Executed P2 Nurse Chain: " + str(self.stepsP2[2]) + " times.")

        print("\n")

        print("Executed P3 Search Stuck: " + str(self.stepsP3[0]) + " times.")

        print("\n")

        print("Total iterations: " + str(sum(self.stepsP1) + sum(self.stepsP2) + sum(self.stepsP3)) + ".")

        print("\n")
