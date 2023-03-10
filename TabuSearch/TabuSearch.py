# Based on this article https://towardsdatascience.com/optimization-techniques-tabu-search-36f197ef8e25
import sys
import random
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
                        print(str(weekday*2+counter))
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