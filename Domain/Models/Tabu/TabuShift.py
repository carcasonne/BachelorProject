from Domain.Models.Enums.Grade import Grade


class TabuShift:
    def __init__(self, coverRequirements, tabuShiftType, shiftDay):
        self.coverRequirements = coverRequirements
        self.assignedNurses = {Grade.ONE: set(), Grade.TWO: set(), Grade.THREE: set()}
        self.shiftType = tabuShiftType
        self.shiftDay = shiftDay

    def addNurse(self, nurse):
        for grade in self.assignedNurses.keys():
            if nurse.grade.value <= grade.value:
                if nurse.id in self.assignedNurses[grade]:
                    raise Exception("Assign Nurse Error: Nurse is already assigned to this shift")
                self.assignedNurses[grade].add(nurse.id)

    def removeNurse(self, nurse):
        for grade in self.assignedNurses.keys():
            if nurse.grade.value <= grade.value:
                if nurse.id not in self.assignedNurses[grade]:
                    raise Exception("Remove Nurse Error: Nurse is not assigned to this shift")
                self.assignedNurses[grade].remove(nurse.id)
