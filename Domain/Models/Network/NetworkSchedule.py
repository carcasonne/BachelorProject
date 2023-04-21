from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Network.NetworkNurse import NetworkNurse
from Domain.Models.Schedule import Schedule
from Domain.Models.Tabu.TabuNurse import TabuNurse
from Domain.Models.Tabu.TabuSchedule import TabuSchedule


class NetworkSchedule:
    def __init__(self, tabuSchedule: TabuSchedule, schedule: Schedule):
        self.nurses = list(map(lambda n: NetworkNurse(tabuSchedule.nurses[n.id], n), schedule.nurses))
        self.tabuSchedule = tabuSchedule
        if len(self.tabuSchedule.shifts) != 14:
            raise Exception("Must be exactly 14 shifts")
        self.shifts = schedule.shifts
        if len(self.shifts) != 21:
            raise Exception("Must be exactly 21 shifts")

    def assignLateToNurse(self):
        pass

    def assignEarlyToNurse(self):
        pass

    def getRequiredForDay(self, day: Days, grade: Grade):
        dayIndex = day.value - 1
        earlyShift = self.shifts[3 * dayIndex]
        lateShift = self.shifts[3 * dayIndex + 1]

        earlyRequirements = earlyShift.coverRequirements[grade]
        lateRequirements = lateShift.coverRequirements[grade]

        return earlyRequirements, lateRequirements

    def getNursesWorkingDay(self, day: Days, grade: Grade):
        dayIndex = day.value - 1
        dayShifts = self.tabuSchedule.shifts[2 * dayIndex]
        dayNurses = dayShifts.assignedNurses[grade]
        return list(dayNurses)

