from abc import ABC, abstractmethod


class ShiftPattern(ABC):
    def __init__(self, night):
        self.night = night


class StandardShiftPattern(ShiftPattern):
    def __init__(self, early, late, night):
        super().__init__(night)
        self.early = early
        self.late = late


class TabuShiftPattern(ShiftPattern):
    def __init__(self, day, night):
        super().__init__(night)
        self.days = day
        self.merged = []
        counter = 0
        while counter < 7:
            self.merged.append(day[counter])
            self.merged.append(night[counter])
            counter += 1

