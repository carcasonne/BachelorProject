from Domain.Models.Schedule import Schedule
from Domain.Models.Enums.Grade import Grade


class SimpleKnapsackModel:
    def __init__(self, schedule):
        self.__schedule = Schedule(schedule.shifts, schedule.nurses)
        self.e = sum(shift.coverRequirements[Grade.THREE] for shift in schedule.shifts if shift.isNightShift())
        self.d = sum(shift.coverRequirements[Grade.THREE] for shift in schedule.shifts if not shift.isNightShift())

        print("Schedule requires: " + str(self.e) + " nurses to work all night shifts")
        print("Schedule requires: " + str(self.d) + " nurses to work all day shifts")

    def searchTree(self):
        return self.__schedule.nurses
