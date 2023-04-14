from Domain.Models.ShiftPatterns.ShiftPattern import StandardShiftPattern


class NetworkNurse:
    def __init__(self, tabuNurse, nurse):
        self.id = nurse.id  # The identification number of the nurse
        self.contract = nurse.contract  # The contract this nurse has: How many days or nights can this nurse work
        self.grade = nurse.grade  # The grade of the nurse: 1= high grade, 2 = medium grade, 3 = low grade
        self.oldPattern = tabuNurse.shiftPattern
        self.shiftPattern = StandardShiftPattern([0] * 7, [0] * 7, tabuNurse.shiftPattern.night)  # The shift pattern that this nurse is currently working
        self.worksNight = tabuNurse.worksNight  # True = Nurse works only night shifts, False = Nurse works only day shifts

        # Soft constraints:
        self.consecutiveWorkingDays = tabuNurse.consecutiveWorkingDays
        self.consecutiveDaysOff = tabuNurse.consecutiveDaysOff
        self.undesiredShifts = nurse.undesiredShifts
        self.shiftPenalty = [0, 0, 0, 0, 0, 0, 0]
        for x in range(7):
            if nurse.undesiredShifts[0][x] != nurse.undesiredShifts[1][x]:
                if nurse.undesiredShifts[0][x] == 1:
                    self.shiftPenalty[x] = -1
                elif nurse.undesiredShifts[0][x] == 0:
                    self.shiftPenalty[x] = 1
        self.completeWeekend = tabuNurse.completeWeekend
        self.LB = self.calculateLowerBound()  # This is the lower bound for the amount of early shifts this nurse can work
        self.UP = self.calculateUpperBound()  # this is the upper bound for the amount of early shifts this nurse can work

    def penalty(self, day):
        return self.shiftPenalty[day]

    def calculateLowerBound(self):
        """
        The amount of times a nurse wants to work early. This is only based on the nurse wanting to work early.
        :return Lower Bound:
        """
        result = 0
        for d in self.shiftPenalty:
            if d < 0:
                result += 1
        return min(result, self.contract.days)

    def calculateUpperBound(self):
        """
        The amount of times it is possible for a nurse to work early. This is based on the nurse wanting to work early
        or having no preference.
        :return Upper Bound:
        """
        result = 0
        for d in self.shiftPenalty:
            if d <= 0:
                result += 1
        return min(result, self.contract.days)
