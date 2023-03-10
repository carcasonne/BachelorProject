from Domain.Models.Enums.Grade import Grade
class Shift:
    def __init__(self, coverRequirements, shiftType, shiftDay):
        self.coverRequirements = coverRequirements
        self.assignedNurses = []
        self.shiftDay = shiftDay
        self.shiftType = shiftType

    def AssignNurse(self, nurse):
        self.assignedNurses.append(nurse)

    def Print(self):
        finalString = "ST" + self.shiftType + "CR: " + self.coverRequirements[Grade.ONE] + ", " + self.coverRequirements[Grade.TWO] + ", " + self.coverRequirements[Grade.THREE] + "\n Assigned: "
        for nurse in self.assignedNurses:
            finalString += nurse.id + ", "
        return finalString
    
    def __eq__(self, other): 
        if not isinstance(other, Shift):
            # don't attempt to compare against unrelated types
            return False

        return  (self.shiftType == other.shiftType and 
                 self.nightShift == other.nightShift)
