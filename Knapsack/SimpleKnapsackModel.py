from Domain.Models.Schedule import Schedule
from Domain.Models.Enums.Grade import Grade


class SimpleKnapsackModel:
    def __init__(self, schedule):
        self.__schedule = Schedule(schedule.shifts, schedule.nurses)
        # Amount of nurses required to fill all night shifts
        self.E = sum(shift.coverRequirements[Grade.THREE] for shift in schedule.shifts if shift.isNightShift())
        # Amount of nurses required to fill all day shifts 
        self.D = sum(shift.coverRequirements[Grade.THREE] for shift in schedule.shifts if not shift.isNightShift())

        # Target, optimal value for knapsack problem
        self.Z = 0

        

        print("Schedule requires: " + str(self.e) + " nurses to work all night shifts")
        print("Schedule requires: " + str(self.d) + " nurses to work all day shifts")

    def searchTree(self):
        return self.__schedule.nurses
