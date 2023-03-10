from Domain.Models.Enums.Grade import Grade


class TabuShift:
    def __init__(self, coverRequirements, tabuShiftType, shiftDay):
        self.coverRequirements = coverRequirements
        self.assignedNurses = [set(), set(), set()]
        self.tabuShiftType = tabuShiftType
        self.shiftDay = shiftDay

    def assignNurse(self, nurse):
        if nurse in self.assignedNurses:
            raise Exception("Nurse is already assigned to this shift")
        self.assignedNurses[nurse.grade.value - 1].add(nurse)

    def removeNurse(self, nurse):
        if nurse not in self.assignedNurses:
            raise Exception("Nurse does not exits")
        self.assignedNurses[nurse.grade].remove(nurse)
        nurse.assignedShiftPattern -= self.ToBit()

    def toBit(self):
        bitShifts = (self.shiftDay - 1)
        return int('1', 2) << bitShifts

    def __str__(self):
        finalString = "ST " + str(self.tabuShiftType) + " CR: " + str(self.coverRequirements[Grade.ONE]) + ", " + \
                      str(self.coverRequirements[Grade.TWO]) + ", " + str(self.coverRequirements[Grade.THREE])
        return finalString
