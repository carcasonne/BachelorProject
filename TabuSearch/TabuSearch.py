# Based on this article https://towardsdatascience.com/optimization-techniques-tabu-search-36f197ef8e25
import sys
import random
from Domain.Models.Tabu.TabuSchedule import TabuSchedule


class TabuSearch:
    def __init__(self, initialSchedule):
        self.currSolution = TabuSchedule(initialSchedule)
        for nurse in self.currSolution.nurses:
            pattern = random.choice(nurse.feasibleShiftPatterns)
            counter = 0
            for full in pattern:
                for dayOrNight in full:
                    if dayOrNight == 1:
                        self.currSolution.shifts[dayOrNight + counter].assignNurse(nurse)
            nurse.assignShiftPattern(pattern)
        self.currSolution.calculatePC()
        self.currSolution.calculateCC()
        self.currSolution.calculateLB()



        self.bestSolution = self.currSolution
        self.dayNightTabuList = []
        self.nurseTabuList = []
        self.dayNightCounter = 0


    def run(self):
        pass
        return self.bestSolution

    # PHASE 1:

    def randomDescent(self):
        if self.currSolution == 0:
            self.storeDetails()
        else:
            pass

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