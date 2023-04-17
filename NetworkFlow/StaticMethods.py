from Domain.Models.Enums.Days import Days


# TODO: Doesn't take into count that a nurse can have an empty a pattern currently... ([0]*7 , [0]*7, [0]*7)
def evaluationFunction(networkSchedule):
    """
    This function is used as the evaluation function for the network flow and will calculate the penalty of the current
    partition of nurses working early and late shifts in the schedule.
    :param networkSchedule:
    :return the number of undesired late shifts currently:
    """
    result = 0
    for nurse in networkSchedule.nurses:
        if nurse.worksNight is False:
            if nurse.shiftPattern.early == [0] * 7 and nurse.shiftPattern.late == [0] * 7:
                raise Exception(f"Nurse {str(nurse.id)} works day but are not assigned a StandardShiftPattern")
            for day in Days:
                if nurse.shiftPattern.early[day.value - 1] == 1:
                    result += abs(nurse.preference(day))
                elif nurse.shiftPattern.late[day.value - 1] == 1:
                    result += abs(nurse.preference(day))
    return result


