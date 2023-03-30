from enum import Enum


class ShiftType(Enum):
    EARLY = 1
    LATE = 2
    NIGHT = 3


class TabuShiftType(Enum):
    DAY = 1
    NIGHT = 2

    def __repr__(self) -> str:
        return str(self.name)
    
    def __str__(self) -> str:
        return str(self.name)