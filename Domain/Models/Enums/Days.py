from enum import Enum


class Days(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    def __repr__(self) -> str:
        return str(self.name)
    
    def __str__(self) -> str:
        return str(self.name)
