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
        self.day = day
        self.merged = []
        counter = 0
        while counter < 7:
            self.merged.append(day[counter])
            self.merged.append(night[counter])
            counter += 1

    def __str__(self):
        return f"TabuShiftPattern: ({self.day}, {self.night})"

    def __eq__(self, other):
        if not isinstance(other, TabuShiftPattern):
            # don't attempt to compare against unrelated types
            return False

        if self.day == [0] * 7 and other.day == [0] * 7 and self.night != [0] * 7 and other.night != [0] * 7:
            return True
        elif self.night == [0] * 7 and other.night == [0] * 7 and self.day != [0] * 7 and other.day != [0] * 7:
            return True
        else:
            return False