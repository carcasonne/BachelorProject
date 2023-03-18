# Based on this article https://towardsdatascience.com/optimization-techniques-tabu-search-36f197ef8e25
import sys
import random
import numpy as np
import copy

from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuSchedule import TabuSchedule


class TabuSearch:
    def __init__(self, initialSchedule):
        tabuSchedule = TabuSchedule(initialSchedule)
        for nurse in tabuSchedule.nurses:
            pattern = random.choice(nurse.feasibleShiftPatterns)
            counter = 0
            for dayOrNightShifts in pattern:
                for weekday in range(7):
                    if dayOrNightShifts[weekday] == 1:
                        tabuSchedule.shifts[weekday*2+counter].assignNurse(nurse)
                counter += 1
            nurse.assignShiftPattern(pattern)
        tabuSchedule.updateAll()
        self.bestSolution = tabuSchedule
        self.dayNightTabuList = []
        self.nurseTabuList = []
        self.dayNightCounter = 0


    def run(self):
        # Phase 1
        pass
        counter = 0
        while counter < 10:
            move = self.randomDescent()
            if move is None: self.balanceRestoration()
            if move is None: self.shiftChainMoves()
            if move is None: self.nurseChainMoves()
            if move is None: self.moveUnderCovering()
            if move is None: self.randomKick()
            self.makeMove(move)
            counter += 1

        # Phase 2

        pass
        return self.bestSolution

    def makeMove(self, move):
        self.bestSolution = move[0]
        self.nurseTabuList.insert(0, move[1])

    # PHASE 1:
    def randomDescent(self):
        neighbor = copy.copy(self.bestSolution)
        for n in neighbor.nurses:
            if n not in self.nurseTabuList:
                if n.assignedShiftPattern[1] == [0] * 7:
                    p = n.feasibleShiftPatterns
                    for x in range(len(p)//2, len(p)):
                        if neighbor.checkMove(n, p[x]) < 0:
                            return neighbor.singleMove(n, p), n
                else:
                    p = n.feasibleShiftPatterns
                    for x in range(len(p) // 2):
                        if neighbor.checkMove(n, p[x]) < 0:
                            return neighbor.singleMove(n, p), n

        while True:
            nurse = np.random.choice(self.bestSolution.nurses)
            newShiftPattern = nurse.feasibleShiftPatterns[random.randint(0, len(nurse.feasibleShiftPatterns) - 1)]
            print(self.bestSolution.CC)
            neighbor = copy.copy(self.bestSolution)

            neighbor.singleMove(nurse, TabuShiftPattern(newShiftPattern[0], newShiftPattern[1]))
            print(neighbor.CC)
            if neighbor.CC < self.bestSolution.CC: #and neighbor.PC <= self.currSolution.PC:
                return neighbor, nurse

    def balanceRestoration(self):
        pass

    def shiftChainMoves(self):
        pass

    def nurseChainMoves(self):
        pass

    def moveUnderCovering(self):
        pass

    def randomKick(self):
        pass



    # PHASE 2:

    def storeDetails(self):
        pass