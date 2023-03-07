from Domain.Models.Enums.Grade import Grade

class TabuShift:
    def __init__(self, coverRequirements, tabuShiftType, shiftDay):
        self.coverRequirements = coverRequirements
        self.assignedNurses = [set()]
        self.tabuShiftType = tabuShiftType
        self.shiftDay = shiftDay

    def AssignNurse(self, nurse):
        if nurse in self.assignedNurses:
            raise Exception("Nurse is already assigned to this shift")
        self.assignedNurses[nurse.grade].add(nurse)
        nurse.assignedShiftPattern += self.ToBit()

    def RemoveNurse(self, nurse):
        if nurse in self.assignedNurses:
            raise Exception("Nurse does not exits")
        self.assignedNurses[nurse.grade].remove(nurse)
        nurse.assignedShiftPattern -= self.ToBit()

    def ToBit(self):
        bitShifts = (self.shiftDay - 1)
        return int('1', 2) <<  bitShifts

    def Print(self):
        finalString = "ST" + self.tabuShiftType + "CR: " + self.coverRequirements[Grade.ONE] + ", " + \
                      self.coverRequirements[Grade.TWO] + ", " + self.coverRequirements[Grade.THREE] + "\n Assigned: "
        return finalString