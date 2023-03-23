from enum import Enum
from functools import total_ordering

@total_ordering
class Grade(Enum):
    ONE = 1
    TWO = 2
    THREE = 3

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        else:
            return False
