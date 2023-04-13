

def evaluationFunction(tabuSchedule, schedule):
    """
    This function is used as the
    :param tabuSchedule:
    :param schedule:
    :return the number of undesired late shifts currently:
    """
    result = 0
    for tabuNurse in tabuSchedule.nurses:
        if tabuNurse.worksNight is False:
            for day in range(7):
                if tabuNurse.shiftPattern.day[day] == 1:
                    if schedule.nurses[tabuNurse.id].undesiredShifts[2][day] == 1:
                        result += 1
    return result

def getUpperBound(nurse):
    pass

def getLowerBound(nurse):
    pass

