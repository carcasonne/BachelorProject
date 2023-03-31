from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Grade import Grade


class Nurse:
    def __init__(self, id, grade:Grade, contract:Contract):
        self.id = id
        self.grade = grade
        self.contract = contract
        self.assignedShiftPattern = None

        # Soft constraints:
        self.consecutiveWorkingDays = (contract.minConsecutiveDays, contract.maxConsecutiveDays)
        self.consecutiveDaysOff = (contract.minConsecutiveDaysOff, contract.maxConsecutiveDaysOff)
        self.undesiredShifts = ([0] * 7, [0] * 7, [0] * 7)
        self.completeWeekend = contract.completeWeekend
        self.undesiredWeekend = False

    def assignShiftPattern(self, shiftPattern):  # A bit representation of ether (day, night) or (early, late, night)
        self.assignedShiftPattern = shiftPattern

    def print(self):
        print(str(self.id) + " is of grade: " + str(self.grade))

    def __eq__(self, other):
        if not isinstance(other, Nurse):
            # don't attempt to compare against unrelated types
            return False

        return (self.id == other.id and
                self.grade == other.grade)
