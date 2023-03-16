from Domain.Models.Schedule import *
from Domain.Models.Shift import *
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType


class KnapsackSolver:
    def __init__(self, schedule):
        self.schedule = Schedule(schedule.shifts, schedule.nurses)
        # Amount of nurses required to fill all night shifts
        # The lower bound on the entire solution
        self.E = sum(shift.coverRequirements[Grade.THREE] for shift in self.schedule.shifts if shift.shiftType == ShiftType.NIGHT)
        # Amount of nurses required to fill all day shifts 
        self.D = sum(shift.coverRequirements[Grade.THREE] for shift in self.schedule.shifts if shift.shiftType != ShiftType.NIGHT)
        # The total number of nurses of each type. 
        # The upper bound for each type. 
        self.Ns = []
        # The total number of nights worked of each type
        self.Es = []
        # The total number of days worked of each type
        self.Ds = []
        # y_i, the amount of nurses of type i working nights
        self.fractionalVariable = 0

        # Target, optimal value for knapsack problem
        self.Z = 0

        # Make the knapsack items
        for nurse in schedule.nurses:
            # Not sure if this is the mapping
            profit = nurse.contract.nights
            weight = nurse.contract.days

    def requiredForGrade(self, Grade, night):
        return sum(shift.coverRequirements[Grade.THREE] for shift in self.schedule.shifts if (shift.shiftType == ShiftType.NIGHT if night else shift.shiftType != ShiftType.NIGHT))
