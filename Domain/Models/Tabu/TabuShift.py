from Domain.Models.Enums.Grade import Grade


class TabuShift:
    def __init__(self, coverRequirements, tabuShiftType, shiftDay):
        # coverRequirements: R(k, r) = the minimum acceptable number of nurses of grade r or above for shift k
        self.coverRequirements = coverRequirements
        self.assignedNurses = {Grade.ONE: set(), Grade.TWO: set(), Grade.THREE: set()}
        self.shiftType = tabuShiftType
        self.shiftDay = shiftDay

    def _addNurse(self, nurse):
        for grade in self.assignedNurses.keys():
            if nurse.grade.value <= grade.value:
                if nurse.id in self.assignedNurses[grade]:
                    raise Exception("Add Nurse Error: Nurse is already assigned to this shift")
                self.assignedNurses[grade].add(nurse.id)

    def _removeNurse(self, nurse):
        for grade in self.assignedNurses.keys():
            if nurse.grade.value <= grade.value:
                if nurse.id not in self.assignedNurses[grade]:
                    raise Exception("Remove Nurse Error: Nurse is not assigned to this shift")
                self.assignedNurses[grade].remove(nurse.id)
    
    def __str__(self):
        return f"Tabu Shift: {self.shiftDay}, {self.shiftType}"
