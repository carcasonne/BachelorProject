

def evaluationFunction(tabuSchedule, schedule):
    result = 0
    for tabuNurse in tabuSchedule.nurses:
        if tabuNurse.worksNight is False:
            for day in range(7):
                if tabuNurse.shiftPattern.day[day] == 1:
                    if schedule.nurses[tabuNurse.id].undesiredShifts[2][day] == 1:
                        result += 10
    return result
