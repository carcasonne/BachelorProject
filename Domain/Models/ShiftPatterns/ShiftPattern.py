from abc import ABC, abstractmethod

class ShiftPattern(ABC):
    def __init__(self):
        self.night = None

class StandardShiftPattern(ShiftPattern):
    def __init__(self):
        super().__init__()
        self.early = None
        self.late = None

class TabuShiftPattern(ShiftPattern):
    def __init__(self):
        super().__init__()
        self.day = None