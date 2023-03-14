from Domain.Models.Enums.Grade import Grade


class TabuShift:
    # TODO: This should properly just take at Shift and convert it.
    def __init__(self, coverRequirements, tabuShiftType, shiftDay):
        self.coverRequirements = coverRequirements
        self.assignedNurses = [set(), set(), set()]
        self.tabuShiftType = tabuShiftType
        self.shiftDay = shiftDay

    def assignNurse(self, nurse):
        if nurse in self.assignedNurses[2]: raise Exception("Nurse is already assigned to this shift")
        value = nurse.grade.value - 1
        for x in range(value, 3):
            self.assignedNurses[x].add(nurse)

    def removeNurse(self, nurse):
        if nurse not in self.assignedNurses[2]: raise Exception("Nurse does not exits")
        value = nurse.grade.value - 1
        for x in range(value, 3):
            self.assignedNurses[x].remove(nurse)

    def toBit(self):
        # TODO: Remove this method since it is never used
        bitShifts = (self.shiftDay - 1)
        return int('1', 2) << bitShifts

    def __str__(self):
        finalString = "ST: " + str(self.tabuShiftType) + " CR: " + str(self.coverRequirements[Grade.ONE]) + ", " + \
                      str(self.coverRequirements[Grade.TWO]) + ", " + \
                      str(self.coverRequirements[Grade.THREE]) + " NURSES ASSIGNED: " + str(
            len(self.assignedNurses[Grade.ONE.value - 1])) + ", " + str(
            len(self.assignedNurses[Grade.TWO.value - 1])) + ", " + str(len(self.assignedNurses[Grade.THREE.value - 1]))
        return finalString
