from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import TabuShiftType


# patternCoverShift: a_j_k = 1 if pattern j covers shift k
def patternCoverShift(pattern, shift):  # a_j_k
    if shift.shiftType == TabuShiftType.DAY and pattern.day[shift.shiftDay.value - 1] == 1:
        return 1
    if shift.shiftType == TabuShiftType.NIGHT and pattern.night[shift.shiftDay.value - 1] == 1:
        return 1
    return 0


# nurseWorkPattern: x_i_j = 1 if nurse i works pattern j
def nurseWorksPattern(nurse, pattern):
    if nurse.shiftPattern.merged == pattern.merged:
        return 1
    return 0


# TODO: THIS IS CURRENTLY ONLY BASED ON GRADE THREE
def evaluateCC(schedule):
    CC = 0
    for s in schedule.shifts:
        CC += s.coverRequirements[Grade.THREE] - len(s.assignedNurses[Grade.THREE])
    return max(0, CC)
