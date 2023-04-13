from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.ShiftType import TabuShiftType
from Domain.Models.Tabu.TabuNurse import TabuNurse
from Domain.Models.Tabu.TabuShift import TabuShift
from Domain.Models.Enums.ShiftType import TabuShiftType
from TabuSearch.StaticMethods import evaluateCC
from TabuSearch.StaticMethods import evaluatePC
from TabuSearch.StaticMethods import evaluateLB

from tabulate import tabulate
from colorama import Fore, Back


class TabuSchedule:
    def __init__(self, Schedule):
        self.nurses = list(map(lambda n: TabuNurse(n), Schedule.nurses))
        self.shifts = []
        for x in range(len(Schedule.shifts)):
            if (x + 1) % 3 == 0:
                self.shifts.append(
                    TabuShift(Schedule.shifts[x].coverRequirements, TabuShiftType.NIGHT, Schedule.shifts[x].shiftDay))
            elif (x + 1) % 3 == 2:
                totalGradeOne = Schedule.shifts[x].coverRequirements[Grade.ONE] + \
                                Schedule.shifts[x - 1].coverRequirements[Grade.ONE]
                totalGradeTwo = Schedule.shifts[x].coverRequirements[Grade.TWO] + \
                                Schedule.shifts[x - 1].coverRequirements[Grade.TWO]
                totalGradeThee = Schedule.shifts[x].coverRequirements[Grade.THREE] + \
                                 Schedule.shifts[x - 1].coverRequirements[Grade.THREE]

                requirements = {Grade.ONE: totalGradeOne, Grade.TWO: totalGradeTwo, Grade.THREE: totalGradeThee}
                self.shifts.append(TabuShift(requirements, TabuShiftType.DAY, Schedule.shifts[x].shiftDay))
        if len(self.shifts) != 14:
            raise Exception("Must be exactly 14 shifts")
        self.CC = evaluateCC(self)  # The covering cost of the schedule - Eq(4)
        self.PC = evaluatePC(self)  # The penalty cost of the schedule - Z / Eq(1)
        #self.LB = evaluateLB(self)  # The lower bound of the schedule - Eq(5)

    # TODO: Tests for this one
    def assignPatternToNurse(self, nurse, pattern):
        oldPattern = nurse.shiftPattern.merged
        nurse._assignShiftPattern(pattern)
        newPattern = nurse.shiftPattern.merged
        for x in range(14):
            if oldPattern[x] != newPattern[x] and newPattern[x] == 1:
                self.shifts[x]._addNurse(nurse)
            if oldPattern[x] != newPattern[x] and oldPattern[x] == 1:
                self.shifts[x]._removeNurse(nurse)
        self.CC = evaluateCC(self)
        self.PC = evaluatePC(self)

    # Checks if pattern covers shift - Returns: 1 or 0
    def __eq__(self, other):
        pass

    def __str__(self):
        string = f"TabuSchedule: \n"
        for shift in self.shifts:
            string += f"{str(shift)} \n"
        string += f"CC Score: {self.CC} \n"
        string += f"PC Score: {self.PC}"
        return string
    
    def __str__(self):
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
        string += tabulate(shifts, headers=["Day", "ShiftType", "Requirements", "Assigned"], tablefmt='fancy_grid', showindex="always")
        string += f"\n \n                 CC Score: {self.CC}       PC Score: {self.PC}\n"
        averagePc = self.PC/len(self.nurses)
        string += f"\n \n                 PC/Nurse Score: {averagePc}\n"
        
        return string + "\n"
        
    def nursePatternSchedule(self):
        # COLUMNS: DAYS
        # ROWS: SHIFTS
        # CELLS: IDS OF NURSES WORKING SHIFT ON DAY

        string = "\n \n \n"
        string += "                                             NURSE WORK PATTERNS\n\n"
        #rows = [str(typ) for typ in TabuShiftType]
        dayRow = [None] * 8
        dayRow[0] = "Day"
        nightRow = [None] * 8
        nightRow[0] = "Night"

        dayNurses = []
        nightNurses = []

        colors = [Back.RED, Back.GREEN, Back.BLUE, Back.WHITE, Back.YELLOW, Back.MAGENTA, Back.CYAN, Back.WHITE, Back.LIGHTRED_EX, Back.LIGHTGREEN_EX, Back.LIGHTYELLOW_EX, Back.LIGHTBLUE_EX, Back.LIGHTMAGENTA_EX, Back.LIGHTCYAN_EX, Back.LIGHTWHITE_EX]
        resetColor = Back.RESET

        idToColor = {}

        for i in range(len(self.nurses)):
            nurse = self.nurses[i]
            idToColor[nurse.id] = colors[i % len(colors)]

        rows = [dayRow]
        
        for nurse in self.nurses:
            item = [""] * 8
            item[0] = f"Nurse ID: {nurse.id}"

            if nurse.shiftPattern.day != [0] * 7:
                for i in range(len(nurse.shiftPattern.day)):
                    day = nurse.shiftPattern.day[i]
                    if day == 1:
                        item[i + 1] = "X"
                dayNurses.append(item)
        
        rows = rows + dayNurses
        rows = rows + [nightRow]

        for nurse in self.nurses:
            item = [""] * 8
            item[0] = f"Nurse ID: {nurse.id}"

            if nurse.shiftPattern.day == [0] * 7:
                for i in range(len(nurse.shiftPattern.night)):
                    night = nurse.shiftPattern.night[i]
                    if night == 1:
                        item[i + 1] = "X"
                nightNurses.append(item)
        
        rows = rows + nightNurses
        
        headers = [""]
        days = [str(day) for day in Days]
        headers = headers + days
        string += tabulate(rows, headers=headers, tablefmt='fancy_grid')
        return string
        

    def scores(self):
        string = f"CC Score: {self.CC} \n"
        string += f"PC Score: {self.PC}"
        return string
