from itertools import combinations

from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import TabuShiftType


# patternCoverShift: a_j_k = 1 if pattern j covers shift k
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern


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


# TODO: THIS IS CURRENTLY ONLY BASED ON GRADE THREE. IMPLEMENTED CORRECTLY BUT DOES NOT MAKE SENSE.
def evaluateCC(schedule):
    CC = 0
    for s in schedule.shifts:
        assigned = 0
        for n in schedule.nurses:
            if n.shiftPattern is not None:
                assigned += patternCoverShift(n.shiftPattern, s)
        CC += s.coverRequirements[Grade.THREE] - assigned
    return max(0, CC)


def evaluatePC(schecule):
    raise NotImplemented


# findFeasablePatterns: F(i) = return all feasible patterns for nurse i
def findFeasablePatterns(nurse):
    fp = []
    counter = 0
    for x in range(2):
        if counter == x:
            combs = combinations(range(7), nurse.contract.days)
        else:
            combs = combinations(range(7),  nurse.contract.nights)

        for comb in combs:
            bitstring = [0] * 7
            for i in comb:
                bitstring[i] = 1
            if counter == 0:
                if len(comb) == nurse.contract.days:
                    fp.append(TabuShiftPattern(bitstring, [0] * 7))
            else:
                if len(comb) == nurse.contract.days:
                    fp.append(TabuShiftPattern([0] * 7, bitstring))
    return fp

