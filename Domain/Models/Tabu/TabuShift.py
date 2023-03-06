from Domain.Models.Enums.Grade import Grade


class TabuShift:
    def __init__(self, coverRequirements, tabuShiftType, shiftDay):
        self.coverRequirements = coverRequirements
        self.tabuShiftType = tabuShiftType
        self.shiftDay = shiftDay

    def ToBit(self):
        bitShifts = (self.shiftDay - 1)
        if self.tabuShiftType.NIGHT:
            bitShifts += 1
        return int('1', 2) <<  bitShifts

    def Print(self):
        finalString = "ST" + self.tabuShiftType + "CR: " + self.coverRequirements[Grade.ONE] + ", " + \
                      self.coverRequirements[Grade.TWO] + ", " + self.coverRequirements[Grade.THREE] + "\n Assigned: "
        return finalString