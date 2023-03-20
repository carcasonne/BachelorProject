from enum import Enum


class ShiftType(Enum):
    EARLY = 1
    LATE = 2
    NIGHT = 3


class TabuShiftType(Enum):
    DAY = 1
    NIGHT = 2
