from Domain.Models.Enums.Grade import Grade


class Shift:
    def __init__(self, coverRequirements, shiftType, shiftDay):
        self.coverRequirements = coverRequirements
        self.assignedNurses = {Grade.ONE: set(), Grade.TWO: set(), Grade.THREE: set()}
        self.shiftDay = shiftDay
        self.shiftType = shiftType

    def __eq__(self, other):
        if not isinstance(other, Shift):
            # don't attempt to compare against unrelated types
            return False

        return (self.shiftType == other.shiftType and
                self.shiftDay == other.shiftDay)
