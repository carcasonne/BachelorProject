from itertools import combinations

from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import TabuShiftType

# patternCoverShift: a_j_k = 1 if pattern j covers shift k
from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern


def patternCoverShift(pattern, shift):  # a_j_k
    """
    patternCoverShift: a_j_k - Checks if pattern covers shift.
    :param pattern:
    :param shift:
    :return 1 or 0:
    """
    if shift.shiftType == TabuShiftType.DAY and pattern.day[shift.shiftDay.value - 1] == 1:
        return 1
    if shift.shiftType == TabuShiftType.NIGHT and pattern.night[shift.shiftDay.value - 1] == 1:
        return 1
    return 0


# nurseWorkPattern: x_i_j = 1 if nurse i works pattern j
def nurseWorksPattern(nurse, pattern):
    """
    nurseWorkPattern: x_i_j - Checks if nurse works pattern
    :param nurse:
    :param pattern:
    :return 1 or 0:
    """
    if nurse.shiftPattern.merged == pattern.merged:
        return 1
    return 0


# TODO: THIS IS CURRENTLY ONLY BASED ON GRADE THREE. IMPLEMENTED DIFFERENT TO Eq(4).
def evaluateCC(schedule):
    """
    evaluateCC: CC - Evaluates the covering cost of a schedule
    :param schedule:
    :return 0 or CC > 0:
    """
    CC = 0
    for s in schedule.shifts:
        assigned = 0
        for n in schedule.nurses:
            if n.shiftPattern is not None:
                assigned += patternCoverShift(n.shiftPattern, s)
        CC += max(0, s.coverRequirements[Grade.THREE] - assigned)  # TODO: Max in here instead of in the end
    return CC


# TODO: Make implementation for evaluatePC
def evaluatePC(schedule):
    """
    evaluatePC: Z - Evaluates the penalty cost of a schedule
    :param schedule:
    :return PC:
    """
    pass


# TODO: Make implementation for evaluateLB
def evaluateLB(schedule):
    """
    evaluateLB: LB - The sum of the minimal penalty cost for all nurses in the schedule (Both day and night patter)
    :param schedule:
    :return LB:
    """
    pass


def findFeasiblePatterns(nurse):
    """
    findFeasiblePatterns: F(i) - Return all feasible patterns for nurse
    :param nurse:
    :return [] of feasible patterns:
    """
    fp = []
    counter = 0
    while counter != 2:
        if counter == 0:
            combs = combinations(range(7), nurse.contract.days)
        else:
            combs = combinations(range(7), nurse.contract.nights)

        for comb in combs:
            bitstring = [0] * 7
            for i in comb:
                bitstring[i] = 1
            if counter == 0:
                if len(comb) == nurse.contract.days:
                    fp.append(TabuShiftPattern(bitstring, [0] * 7))
            else:
                if len(comb) == nurse.contract.nights:
                    fp.append(TabuShiftPattern([0] * 7, bitstring))
        counter += 1
    return fp

# Returns the number of shifts needed to be covered for each grade
# NOTE: Right now, this only sets for grade 3
def findShiftTypeRequirements(schedule: TabuSchedule, Grade, night):
    Q_t_r = {} 
    types = [TabuShiftType.DAY, TabuShiftType.NIGHT]

    for type in types:
        Q_t_r[type] = {
            Grade.ONE: 0,
            Grade.TWO: 0,
            Grade.THREE: 0
        }
    
    for type in types:
        grade_3_requirements = sum(shift.coverRequirements[Grade] for shift in schedule.shifts if shift.shiftType == type)
        Q_t_r[type][Grade.THREE] = grade_3_requirements
    
    return Q_t_r