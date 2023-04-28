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
                self.schedule.assignPatternToNurse(self.schedule.nurses[nurse.id], pattern)
            else:
                pattern = StandardShiftPattern([0]*7, [0]*7, [0]*7)
                for day in range(7):
                    if nurse.shiftPattern.day[day] == 1:
                        if nurse.id in lst[day]:
                            pattern.early[day] = 1
                        else:
                            pattern.late[day] = 1
                self.schedule.assignPatternToNurse(self.schedule.nurses[nurse.id], pattern)

        return self.schedule

    def run(self):
        nurseList = []
        for nurse in self.tabuSchedule.nurses:
            if not nurse.worksNight:
                nurseList.append(nurse.id)

        return self.aux(nurseList)

    def aux(self, nurselist):
        referenceList = dict()
        days = 7
        workdays = dict()
        penalties = dict()
        nurse_grades = []

        counter = 0
        for id in nurselist:
            if not self.tabuSchedule.nurses[id].worksNight:
                # Reference List
                referenceList[counter] = self.tabuSchedule.nurses[id].id

                # Work Days
                workdays[counter] = self.tabuSchedule.nurses[id].shiftPattern.day

                nurse_grades.append(self.tabuSchedule.nurses[id].grade.value)

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

        early_shifts_lower = [0, 0, 0] * 7
        early_shifts_upper = [0, 0, 0] * 7
        for d in range(days):
            early_shifts_lower[d] = self.schedule.shifts[d*3].coverRequirements[Grade.ONE], \
                                    self.schedule.shifts[d*3].coverRequirements[Grade.TWO], \
                                    self.schedule.shifts[d*3].coverRequirements[Grade.THREE]

            g1 = 0
            g2 = 0
            g3 = 0
            for id in nurselist:
                if self.tabuSchedule.nurses[id].shiftPattern.day[d] == 1:
                    if self.schedule.nurses[id].grade == Grade.ONE:
                        g1 += 1
                        g2 += 1
                        g3 += 1
                    elif self.schedule.nurses[id].grade == Grade.TWO:
                        g2 += 1
                        g3 += 1
                    elif self.schedule.nurses[id].grade == Grade.THREE:
                        g3 += 1

            early_shifts_upper[d] = (g1 - self.schedule.shifts[d * 3 + 1].coverRequirements[Grade.ONE]), \
                                    (g2 - self.schedule.shifts[d * 3 + 1].coverRequirements[Grade.TWO]), \
                                    (g3 - self.schedule.shifts[d * 3 + 1].coverRequirements[Grade.THREE])

        return self.ipSolve(counter, days, nurse_grades, penalties, workdays, early_shifts_lower, early_shifts_upper, referenceList)

    def ipSolve(self, nurses, days, nurse_grades, penalties, workdays, early_shifts_lower, early_shifts_upper, ref):
        # Create the optimization model
        model = Model(solver_name=CBC)

        # Define the decision variables
        x = [[model.add_var(var_type=BINARY) for j in range(nurses)] for i in range(days)]

        # Define the objective function
        model.objective = minimize(
            xsum(penalties[nurse][day] * x[day][nurse] for day in range(days) for nurse in range(nurses)))

        # Define the constraints
        for day in range(days):
            model += xsum(
                x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] == 1) for nurse in range(nurses)) >= \
                     early_shifts_lower[day][0]
            model += xsum(
                x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] <= 2) for nurse in range(nurses)) >= \
                     early_shifts_lower[day][1]
            model += xsum(
                x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] <= 3) for nurse in range(nurses)) >= \
                     early_shifts_lower[day][2]
            model += xsum(
                x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] == 1) for nurse in range(nurses)) <= \
                     early_shifts_upper[day][0]
            model += xsum(
                x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] <= 2) for nurse in range(nurses)) <= \
                     early_shifts_upper[day][1]
            model += xsum(
                x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] <= 3) for nurse in range(nurses)) <= \
                     early_shifts_upper[day][2]

        # Solve the optimization problem
        model.optimize()

        # Print the results
        if model.num_solutions:
            print('Total penalty: ', model.objective_value)
            result = []
            for day in range(days):
                tmpDay = []
                print('Day', day, ': ', end='')
                for nurse in range(nurses):
                    if x[day][nurse].x >= 0.99:
                        print('Nurse', ref[nurse], end=' ')
                        tmpDay.append(ref[nurse])
                print()
                result.append(tmpDay)

            return result
        else:
            print('No solution found.')
            return None