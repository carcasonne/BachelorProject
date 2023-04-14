from Domain.Models.Network.NetworkNurse import NetworkNurse
from Domain.Models.Tabu.TabuNurse import TabuNurse


class NetworkSchedule:
    def __init__(self, tabuSchedule, schedule):
        self.nurses = list(map(lambda n: NetworkNurse(tabuSchedule.nurses[n.id], n), schedule.nurses))
        self.tabuShifts = tabuSchedule.shifts
        if len(self.shifts) != 14:
            raise Exception("Must be exactly 14 shifts")
        self.shifts = schedule.shifts
        if len(self.shifts) != 21:
            raise Exception("Must be exactly 21 shifts")

    def assignLateToNurse(self):
        pass

    def assignEarlyToNurse(self):
        pass
