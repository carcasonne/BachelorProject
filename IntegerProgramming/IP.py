from mip import Model, xsum, minimize, BINARY, CBC

# Define the input data
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.ShiftPatterns.ShiftPattern import StandardShiftPattern
from Tests.test_networkflow.TestNetworkFlowData import TestNetworkFlowData


class IntegerProgrammingModel:
    def __init__(self, schedule, tabuSchedule):
        self.tabuSchedule = tabuSchedule
        self.schedule = schedule

    def buildFinalSchedule(self):
        lst = self.run()
        for nurse in self.tabuSchedule.nurses:
            if nurse.worksNight:
                pattern = StandardShiftPattern([0]*7, [0]*7, nurse.shiftPattern.night)
                self.schedule.nurses[nurse.id].assignShiftPattern(pattern)
            else:
                pattern = StandardShiftPattern([0]*7, [0]*7, [0]*7)
                for day in range(7):
                    if nurse.shiftPattern.day[day] == 1:
                        if nurse.id in lst[day]:
                            pattern.early[day] = 1
                        else:
                            pattern.late[day] = 1
                self.schedule.nurses[nurse.id].assignShiftPattern(pattern)

        return self.schedule

    def run(self):
        result = [[], [], [], [], [], [], []]
        nurseList = []
        for nurse in self.tabuSchedule.nurses:
            if not nurse.worksNight:
                nurseList.append(nurse.id)

        for grade in Grade:
            values = self.aux(grade, nurseList, result)
            for i in range(7):
                result[i].extend(values[0][i])
            for id in values[1]:
                if id in nurseList:
                    nurseList.remove(id)
        print(str(result))
        return result

    def aux(self, grade, nurselist, current):
        referenceList = dict()
        days = 7
        workdays = dict()
        penalties = dict()

        counter = 0
        for id in nurselist:
            if not self.tabuSchedule.nurses[id].worksNight and self.tabuSchedule.nurses[id].grade <= grade:
                # Reference List
                referenceList[counter] = self.tabuSchedule.nurses[id].id

                # Work Days
                workdays[counter] = self.tabuSchedule.nurses[id].shiftPattern.day

                # Penalty
                tmp = [0] * 7
                for x in range(7):
                    if self.schedule.nurses[id].undesiredShifts[0][x] != self.schedule.nurses[id].undesiredShifts[1][x]:
                        if self.schedule.nurses[id].undesiredShifts[0][x] == 1:
                            tmp[x] = 1
                        elif self.schedule.nurses[id].undesiredShifts[0][x] == 0:
                            tmp[x] = -1
                penalties[counter] = tmp
                counter += 1

        early_shifts_lower = dict()
        early_shifts_upper = dict()
        for d in range(days):
            currentEarlyRequirement = self.schedule.shifts[d * 3].coverRequirements[grade]
            if grade == Grade.TWO or grade == Grade.THREE:
                currentEarlyRequirement -= len(current[d])
            early_shifts_lower[d] = currentEarlyRequirement

            tmpCounter = 0
            for id in nurselist:
                if self.schedule.nurses[id].grade.value <= grade.value:
                    if self.tabuSchedule.nurses[id].shiftPattern.day[d] == 1:
                        tmpCounter += 1
            early_shifts_upper[d] = tmpCounter - currentEarlyRequirement

        return self.ipSolve(counter, days, penalties, workdays, early_shifts_lower, early_shifts_upper, referenceList)

    def ipSolve(self, nurses, days, penalties, workdays, early_shifts_lower, early_shifts_upper, ref):
        # Create the optimization model
        model = Model(solver_name=CBC)

        # Define the decision variables
        x = [[model.add_var(var_type=BINARY) for j in range(nurses)] for i in range(days)]

        # Define the objective function
        model.objective = minimize(
            xsum(penalties[nurse][day] * x[day][nurse] for day in range(days) for nurse in range(nurses)))

        # Define the constraints
        for day in range(days):
            model += xsum(x[day][nurse] * workdays[nurse][day] for nurse in range(nurses)) >= early_shifts_lower[day]
            model += xsum(x[day][nurse] * workdays[nurse][day] for nurse in range(nurses)) <= early_shifts_upper[day]

        # Solve the optimization problem
        model.optimize()

        # Print the results
        if model.num_solutions:
            print('Total penalty: ', model.objective_value)
            result = []
            remove = set()
            for day in range(days):
                tmpDay = []
                print('Day', day, ': ', end='')
                for nurse in range(nurses):
                    if x[day][nurse].x >= 0.99:
                        print('Nurse', ref[nurse], end=' ')
                        remove.add(ref[nurse])
                        tmpDay.append(ref[nurse])
                print()
                result.append(tmpDay)

            return result, remove
        else:
            print('No solution found.')
            return None