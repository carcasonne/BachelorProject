# Based on this article https://towardsdatascience.com/optimization-techniques-tabu-search-36f197ef8e25
import sys
import random
import numpy as np
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

        self.currSolution = tabuSchedule
        self.bestSolution = tabuSchedule
        self.dayNightTabuList = []
        self.nurseTabuList = []
        self.dayNightCounter = 0


    def run(self):
        # Phase 1
        pass
        while self.currSolution.CC != 0:
            move = self.randomDecent()
            if move is None: self.balanceRestoration()
            if move is None: self.shiftChainMoves()
            if move is None: self.nurseChainMoves()
            if move is None: self.moveUnderCovering()
            if move is None: self.randomKick()
            self.makeMove(move)

        # Phase 2

        pass
        return self.bestSolution

    def makeMove(self, move):
        self.bestSolution = move[0]
        self.nurseTabuList.insert(0, move[0])

    # PHASE 1:
    def randomDescent(self):
        while True:
            nurse = np.random.choice(self.currSolution.nurses)
            newShiftPattern = np.random.choice(nurse.feasibleShiftPatterns)
            neighbor = self.currSolution.singleMove(nurse, newShiftPattern)
            if neighbor.CC < self.currSolution.CC and neighbor.PC <= self.currSolution.PC:
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