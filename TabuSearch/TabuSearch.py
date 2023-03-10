# Based on this article https://towardsdatascience.com/optimization-techniques-tabu-search-36f197ef8e25
import sys
import random
from Domain.Models.Tabu.TabuSchedule import TabuSchedule


class TabuSearch:
    def __init__(self, initialSchedule):
        self.currSolution = TabuSchedule(initialSchedule)
        for nurse in self.currSolution.nurses:
            workpattern = random.choice(nurse.feasibleShiftPatterns)
            counter = 0
            for full in workpattern:
                for dayOrNight in full:
                    if dayOrNight == 1:
                        self.currSolution.shifts[dayOrNight + counter].assignNurse(nurse)
            nurse.assignShiftPattern(workpattern)
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

    def StandardMove(self):
        pass

    def SwapMove(self):
        pass

    def ShiftMove(self):
        pass

    def ChainMove(self):
        pass

    def EvaluateCC(self):
        pass

    def EvaluatePC(self):
        pass