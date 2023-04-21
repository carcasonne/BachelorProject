from Domain.Models.Enums.Grade import Grade


class Shift:
    def __init__(self, coverRequirements, shiftType, shiftDay):
        self.coverRequirements = coverRequirements
        self.assignedNurses = {Grade.ONE: set(), Grade.TWO: set(), Grade.THREE: set()}
        self.shiftDay = shiftDay
        self.shiftType = shiftType

    def addNurse(self, nurse):
        for grade in self.assignedNurses.keys():
            if nurse.grade.value <= grade.value:
                if nurse.id in self.assignedNurses[grade]:
                    raise Exception("Add Nurse Error: Nurse is already assigned to this shift")
                self.assignedNurses[grade].add(nurse.id)

    def removeNurse(self, nurse):
        for grade in self.assignedNurses.keys():
            if nurse.grade.value <= grade.value:
                if nurse.id not in self.assignedNurses[grade]:
                    raise Exception("Remove Nurse Error: Nurse is not assigned to this shift")
                self.assignedNurses[grade].remove(nurse.id)

    def __eq__(self, other):
        if not isinstance(other, Shift):
            # don't attempt to compare against unrelated types
            return False

        return (self.shiftType == other.shiftType and
                self.shiftDay == other.shiftDay)
