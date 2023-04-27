from colorama import Fore, Back
from tabulate import tabulate

from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Tabu.TabuSchedule import TabuSchedule


class Schedule:
    def __init__(self, shifts, nurses):
        if len(shifts) != 21:
            raise TypeError("Must be exactly 21 shifts")

        self.shifts = shifts
        self.nurses = nurses

    def getPenaltyScore(self):
        PC = 0
        for nurse in self.nurses:
            PC = PC + nurse.calculatePenalty(nurse.assignedShiftPattern)
        return PC

    def shiftsRequirementsMet(self):
        for shift in self.shifts:
            for grade in Grade:
                shiftRequirements = shift.coverRequirements[grade]
                assignedNurses = len(shift.assignedNurses[grade])
                if shiftRequirements > assignedNurses:
                    return False
        return True
    def nursesFulfillContract(self):
        valid = True
        # Are nurses assigned to more or fewer shifts than contractually obliged to?
        for nurse in self.nurses:
            assignedEarlies = sum(nurse.assignedShiftPattern.early)
            assignedLates = sum(nurse.assignedShiftPattern.late)
            assignedNights = sum(nurse.assignedShiftPattern.night)
            worksNight = nurse.assignedShiftPattern.night != [0] * 7
            if worksNight:
                if assignedNights != nurse.contract.nights:
                    valid = False
                    break
            else:
                if assignedEarlies + assignedLates != nurse.contract.days:
                    valid = False
                    break
        return valid

    def getScheduleRequirementsAsString(self):
        string = "\n \n \n"
        string += "                  SHIFT REQUIREMENTS/COVERAGE                 \n"
        shifts = []
        for shift in self.shifts:
            basicColor = Fore.RESET
            coverString = ""
            assignedString = ""
            for key, value in shift.coverRequirements.items():
                coverString += f"{str(key)}:    {str(value)}\n"
            for key, value in shift.assignedNurses.items():
                color = None
                if len(value) > shift.coverRequirements[key]:
                    color = Fore.YELLOW
                elif len(value) == shift.coverRequirements[key]:
                    color = Fore.GREEN
                else:
                    color = Fore.RED
                assignedString += f"{str(key)}:     {color + str(len(value)) + basicColor}\n"
            item = [shift.shiftDay, shift.shiftType, coverString, assignedString]
            shifts.append(item)
        string += tabulate(shifts, headers=["Day", "ShiftType", "Requirements", "Assigned"], tablefmt='fancy_grid',
                           showindex="always")
        string += f"\n \n                 PC/Nurse Score: To be implemented\n"

        return string + "\n"

    def getNursePatternsAsString(self):
        # COLUMNS: DAYS
        # ROWS: SHIFTS
        # CELLS: IDS OF NURSES WORKING SHIFT ON DAY

        string = "\n \n \n"
        string += "                                             NURSE WORK PATTERNS\n\n"
        # rows = [str(typ) for typ in TabuShiftType]
        earlyRow = [None] * 8
        earlyRow[0] = "Early"
        lateRow = [None] * 8
        lateRow[0] = "Late"
        nightRow = [None] * 8
        nightRow[0] = "Night"

        earlyNurses = []
        lateNurses  = []
        nightNurses = []

        colors = [Back.RED, Back.GREEN, Back.BLUE, Back.WHITE, Back.YELLOW, Back.MAGENTA, Back.CYAN, Back.WHITE,
                  Back.LIGHTRED_EX, Back.LIGHTGREEN_EX, Back.LIGHTYELLOW_EX, Back.LIGHTBLUE_EX,
                  Back.LIGHTMAGENTA_EX, Back.LIGHTCYAN_EX, Back.LIGHTWHITE_EX]
        resetColor = Back.RESET

        idToColor = {}

        for i in range(len(self.nurses)):
            nurse = self.nurses[i]
            idToColor[nurse.id] = colors[i % len(colors)]

        rows = [earlyRow]

        for nurse in self.nurses:
            item = [""] * 8
            item[0] = f"Nurse ID: {nurse.id}"
            pattern = nurse.assignedShiftPattern
            if pattern.early != [0] * 7:
                for i in range(len(pattern.early)):
                    day = pattern.early[i]
                    if day == 1:
                        item[i + 1] = "X"
                earlyNurses.append(item)

        rows = rows + earlyNurses
        rows = rows + [lateRow]

        for nurse in self.nurses:
            item = [""] * 8
            item[0] = f"Nurse ID: {nurse.id}"
            pattern = nurse.assignedShiftPattern
            if pattern.late != [0] * 7:
                for i in range(len(pattern.late)):
                    day = pattern.late[i]
                    if day == 1:
                        item[i + 1] = "X"
                lateNurses.append(item)

        rows = rows + lateNurses
        rows = rows + [nightRow]

        for nurse in self.nurses:
            item = [""] * 8
            item[0] = f"Nurse ID: {nurse.id}"
            pattern = nurse.assignedShiftPattern
            if pattern.night != [0] * 7:
                for i in range(len(pattern.night)):
                    night = pattern.night[i]
                    if night == 1:
                        item[i + 1] = "X"
                nightNurses.append(item)

        rows = rows + nightNurses

        headers = [""]
        days = [str(day) for day in Days]
        headers = headers + days
        string += tabulate(rows, headers=headers, tablefmt='fancy_grid')
        return string
