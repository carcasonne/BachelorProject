from Domain.Models.Enums.Grade import Grade


class TabuShift:
    def __init__(self, coverRequirements, tabuShiftType, shiftDay):
        self.coverRequirements = (0, 0, 0)
        self.assignedNurses = [set(), set(), set()]
        self.tabuShiftType = tabuShiftType
        self.shiftDay = shiftDay
