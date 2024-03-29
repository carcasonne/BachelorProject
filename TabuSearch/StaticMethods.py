from itertools import combinations
import random

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


def evaluateCC(schedule):
    """
    evaluateCC: CC - Evaluates the covering cost of a schedule
    :param schedule:
    :return 0 or CC > 0:
    """
    CC = 0
    for s in schedule.shifts:
        CC += max(0, s.coverRequirements[Grade.ONE] - len(s.assignedNurses[Grade.ONE]))
        CC += max(0, s.coverRequirements[Grade.TWO] - len(s.assignedNurses[Grade.TWO]))
        CC += max(0, s.coverRequirements[Grade.THREE] - len(
            s.assignedNurses[Grade.THREE]))  # TODO: Max in here instead of in the end
    return CC


def calculateDifferenceCC(schedule, nurse, pattern):
    """
    calculateDifferenceCC: Returns the difference in CC for the schedule if nurse is shifted to pattern
    :param schedule:
    :param nurse:
    :param pattern:
    :return CC difference if move is chosen:
    """
    diffCC = 0
    for i in range(14):
        newMergedPattern = pattern.merged
        oldMergedPattern = nurse.shiftPattern.merged
        if newMergedPattern[i] != oldMergedPattern[i]:
            for grade in schedule.shifts[0].assignedNurses.keys():
                if nurse.grade.value <= grade.value:
                    currentShiftCoverage = schedule.shifts[i].coverRequirements[grade] - len(
                        schedule.shifts[i].assignedNurses[grade])
                    if newMergedPattern[i] == 1:
                        # If covering requirement is higher than the assigned nurses it will decrease the CC to add nurse
                        if currentShiftCoverage > 0:
                            diffCC -= 1
                    if oldMergedPattern[i] == 1:
                        # If covering requirement is higher than the assigned nurses it will increase in CC to remove nurse
                        if currentShiftCoverage >= 0:
                            diffCC += 1
    return diffCC


def calculateDifferenceDuoCC(schedule, nurse1, nurse2, pattern1, pattern2):
    """
    calculateDifferenceDuoCC: Returns the difference in CC for the schedule if nurse1 and nurse2 is shifted to pattern1
    and pattern2
    :param schedule:
    :param nurse1:
    :param nurse2:
    :param pattern1:
    :param pattern2:
    :return CC difference:
    """
    diffCC = 0
    for i in range(14):
        newMergedPattern1 = pattern1.merged
        oldMergedPattern1 = nurse1.shiftPattern.merged
        newMergedPattern2 = pattern2.merged
        oldMergedPattern2 = nurse2.shiftPattern.merged
        for grade in schedule.shifts[0].assignedNurses.keys():
            changeForN1 = newMergedPattern1[i] != oldMergedPattern1[i]
            changeForN2 = newMergedPattern2[i] != oldMergedPattern2[i]
            if nurse1.grade.value > grade.value:
                changeForN1 = False
            if nurse2.grade.value > grade.value:
                changeForN2 = False

            currentShiftCoverage = schedule.shifts[i].coverRequirements[grade] - len(
                schedule.shifts[i].assignedNurses[grade])
            if changeForN1 is True and changeForN2 is False:
                if currentShiftCoverage > 0:
                    diffCC -= newMergedPattern1[i]
                if currentShiftCoverage >= 0:
                    diffCC += oldMergedPattern1[i]
            elif changeForN1 is False and changeForN2 is True:
                if currentShiftCoverage > 0:
                    diffCC -= newMergedPattern2[i]
                if currentShiftCoverage >= 0:
                    diffCC += oldMergedPattern2[i]

    return diffCC


def evaluatePC(schedule):
    """
    evaluatePC: Z - Evaluates the penalty cost of a schedule
    :param schedule:
    :return PC:
    """
    PC = 0
    for n in schedule.nurses:
        PC += n.penalty
    return PC


def calculateDifferencePC(nurse, pattern):
    """
    calculateDifferenceCC: Returns the difference in PC for the nurse if nurse is shifted to pattern
    :param nurse:
    :param pattern:
    :return PC difference if move is chosen:
    """
    return nurse.calculatePenalty(pattern) - nurse.penalty


def randomizeConstraints(nurse):
    # Setting random variables for if nurse has any specific preferences, for more variation and "realistic" consistency in constraints:
    hatesNight = False
    if random.randint(1, 4) == 1:
        hatesNight = True
    hatesWeekend = False
    if random.randint(1, 3) == 1:
        hatesWeekend = True
    prefersNight = False
    if random.randint(1, 5) == 1 and not hatesNight:
        prefersNight = True
    prefersWeekend = False
    if random.randint(1, 4) == 1 and not hatesWeekend:
        prefersWeekend = True

    # Calculating minimum for consecutive working days:
    rand = random.randint(1, 7)
    if rand <= 4:
        nurse.consecutiveWorkingDays = 1, nurse.consecutiveWorkingDays[1]
    elif rand <= 6:
        nurse.consecutiveWorkingDays = 2, nurse.consecutiveWorkingDays[1]
    else:
        nurse.consecutiveWorkingDays = 3, nurse.consecutiveWorkingDays[1]

    # Calculating maximum for consecutive working days:
    rand = random.randint(1, 10)
    nurse.consecutiveWorkingDays = nurse.consecutiveWorkingDays[0], 5
    if rand <= 5:
        pass
    elif rand <= 8:
        nurse.consecutiveWorkingDays = nurse.consecutiveWorkingDays[0], 4
    elif rand <= 9:
        nurse.consecutiveWorkingDays = nurse.consecutiveWorkingDays[0], 3
    elif rand == 10 and nurse.consecutiveWorkingDays[0] != 3:
        nurse.consecutiveWorkingDays = nurse.consecutiveWorkingDays[0], 2

    # Calculating minimum for consecutive free days:
    rand = random.randint(1, 7)
    if rand <= 5:
        nurse.consecutiveDaysOff = 1, nurse.consecutiveDaysOff[1]
    else:
        nurse.consecutiveDaysOff = 2, nurse.consecutiveDaysOff[1]

    # Calculating maximum for consecutive free days:
    rand = random.randint(1, 10)
    nurse.consecutiveDaysOff = nurse.consecutiveDaysOff[0], 2
    if rand <= 2 and nurse.consecutiveDaysOff[0] != 2:
        nurse.consecutiveDaysOff = nurse.consecutiveDaysOff[0], 1
    elif rand <= 8:
        pass
    else:
        nurse.consecutiveDaysOff = nurse.consecutiveDaysOff[0], 3

    # Randomly calculating random days that the nurse does not want to work:
    for x in range(14):
        rand = random.randint(1, 10)
        if x <= 6 and rand == 1:
            nurse.undesiredShifts.day[x] = 1
        elif x >= 7 and rand == 1:
            nurse.undesiredShifts.night[x - 7] = 1

    # Randomly calculating weekends constraints:
    if random.randint(1, 5) == 1:
        nurse.completeWeekend = True

    # Setting preferences calculated in the beginning:
    if hatesNight:
        nurse.undesiredShifts.night = [1] * 7
    if hatesWeekend:
        nurse.undesiredShifts.day[5] = 1
        nurse.undesiredShifts.day[6] = 1
        nurse.undesiredShifts.night[5] = 1
        nurse.undesiredShifts.night[6] = 1
        nurse.consecutiveDaysOff = 2, nurse.consecutiveDaysOff[1]
        if nurse.consecutiveDaysOff[1] < 2:
            nurse.consecutiveDaysOff = nurse.consecutiveDaysOff[0], 2
    if prefersNight:
        nurse.undesiredShifts.day = [1] * 7
    if prefersWeekend:
        nurse.undesiredShifts.day[5] = 0
        nurse.undesiredShifts.day[6] = 0
        nurse.undesiredShifts.night[5] = 0
        nurse.undesiredShifts.night[6] = 0
        nurse.completeWeekend = True


def evaluateLB(schedule, feasibleShiftPatterns):
    """
    evaluateLB: LB - The sum of the minimal penalty cost for all nurses in the schedule with the current partition.
    :param feasibleShiftPatterns:
    :param schedule:
    :return LB:
    """
    LB = schedule.PC
    for nurse in schedule.nurses:
        nurseLowestPC = calculateDifferencePC(nurse, nurse.shiftPattern)
        for pattern in feasibleShiftPatterns[nurse.id]:
            if nurse.worksNight and pattern.day == [0]*7:
                nurseLowestPC = min(nurseLowestPC, calculateDifferencePC(nurse, pattern))
            if nurse.worksNight is False and pattern.night == [0]*7:
                nurseLowestPC = min(nurseLowestPC, calculateDifferencePC(nurse, pattern))
        LB += nurseLowestPC
    return LB


# TODO: There is properly a smarter way to do this
def checkBalance(schedule):  # This balance check is based on Eq (5) in the article
    balancedDays = True
    balancedNights = True
    totalDaysAssigned = [0, 0, 0]
    totalDaysRequired = [0, 0, 0]
    totalNightsAssigned = [0, 0, 0]
    totalNightsRequired = [0, 0, 0]
    for shift in schedule.shifts:
        for grade in shift.coverRequirements.keys():
            if shift.shiftType == TabuShiftType.DAY:
                totalDaysAssigned[grade.value - 1] += len(shift.assignedNurses[grade])
                totalDaysRequired[grade.value - 1] += shift.coverRequirements[grade]
            if shift.shiftType == TabuShiftType.NIGHT:
                totalNightsAssigned[grade.value - 1] += len(shift.assignedNurses[grade])
                totalNightsRequired[grade.value - 1] += shift.coverRequirements[grade]
    for x in range(3):
        if totalDaysAssigned[x] - totalDaysRequired[x] < 0:
            balancedDays = False
        if totalNightsAssigned[x] - totalNightsRequired[x] < 0:
            balancedNights = False
    return balancedDays, balancedNights


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
