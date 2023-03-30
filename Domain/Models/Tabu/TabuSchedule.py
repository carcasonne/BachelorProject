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
import colorama
from colorama import Fore


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
        self.LB = evaluateLB(self)  # The lower bound of the schedule - Eq(5)

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
                color = Fore.GREEN if len(value) == shift.coverRequirements[key] else Fore.RED
                assignedString += f"{str(key)}:     {color + str(len(value)) + basicColor}\n"
            item = [shift.shiftDay, shift.shiftType, coverString, assignedString]
            shifts.append(item)
        string += tabulate(shifts, headers=["Day", "ShiftType", "Requirements", "Assigned"], tablefmt='fancy_grid', showindex="always")
        string += f"\n \n                 CC Score: {self.CC}       PC Score: {self.PC}\n"
        return string
    
    def scheduleTable(self):
        # COLUMNS: DAYS
        # ROWS: SHIFTS
        # CELLS: IDS OF NURSES WORKING SHIFT ON DAY

        string = "\n \n \n"
        string += "                  NURSE WORK PATTERNS                 \n"
        rows = [str(typ) for typ in TabuShiftType]
        dayRow = [""] * 7
        nightRow = [""] * 7

        for i in range(7):
            item = []
            rows.append(item)
            shift = self.shifts[i*2]
            ids = shift.assignedNurses[Grade.THREE]
            content = ""
            for idd in ids:
                content += f"{idd}, "      
            nightRow[i] = content
        
        #headers = ["Shoft Type", str(day) for day in Days]

        string += tabulate(rows, headers=[], tablefmt='fancy_grid', showindex="always")


        pass
        
    def scores(self):
        string = f"CC Score: {self.CC} \n"
        string += f"PC Score: {self.PC}"
        return string
