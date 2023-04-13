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
        self.undesiredShifts = tabuNurse.undesiredShifts
        self.shiftPenalty = [0, 0, 0, 0, 0, 0, 0]
        for x in range(7):
            if nurse.undesiredShifts[0][x] != nurse.undesiredShifts[1][x]:
                if nurse.undesiredShifts[0][x] == 1:
                    self.shiftPenalty[x] = -1
                elif nurse.undesiredShifts[0][x] == 0:
                    self.shiftPenalty[x] = 1
        self.completeWeekend = tabuNurse.completeWeekend

    def penalty(self, day):
        return self.shiftPenalty[day]