import Domain.Models.Shift
import Domain.Models.Schedule

class GradeKnapsackModel :
    def __init__(self, schedule):
        self.__schedule = schedule
        self.e = sum(1 for shift in schedule.shifts if shift.isNightShift())
        self.d = sum(1 for shift in schedule.shifts) - self.e

    def searchTree(self):
        raise Exception("Not Implemented")