from mip import Model, xsum, minimize, BINARY, CBC

# Define the input data
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.ShiftPatterns.ShiftPattern import StandardShiftPattern
from Tests.test_networkflow.TestNetworkFlowData import TestNetworkFlowData

nurses = 5
days = 7

# nurse reference numbers
ref = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E'
}

nurse_grades = [1, 2, 3, 1, 2]


# range of early shifts each nurse is allowed to work each day
early_shift_requirements = [
    [1, 1, 1],  # 1, 0, 0
    [1, 1, 2],  # 1, 0, 1
    [1, 2, 2],  # 1, 1, 0
    [0, 2, 2],  # 0, 2, 0
    [0, 2, 2],  # 0, 2, 0
    [0, 2, 2],  # 0, 2, 0
    [0, 2, 2]]  # 0, 2, 0

early_shifts_upper = [
    [1, 2, 3],  # 1, 1, 1
    [1, 1, 2],  # 1, 0, 1
    [1, 2, 2],  # 1, 1, 0
    [2, 3, 3],  # 2, 1, 0
    [1, 2, 3],  # 1, 1, 1
    [1, 3, 4],  # 1, 2, 1
    [1, 2, 2]]  # 1, 1, 0


# penalties for assigning a nurse to a shift
penalties = {
    0: [2, 3, 1, 3, 2, 3, 1],
    1: [2, 3, 1, 3, 2, 3, 1],
    2: [2, 3, 1, 3, 2, 3, 1],
    3: [2, 3, 1, 3, 2, 3, 1],
    4: [2, 3, 1, 3, 2, 3, 1]
}

# number of early shifts each nurse is required to work each day
workdays = {
    0: [1, 1, 1, 1, 0, 0, 0],  # Grade 1
    1: [0, 0, 1, 1, 1, 1, 0],  # Grade 2
    2: [1, 1, 0, 0, 1, 1, 0],  # Grade 3
    3: [0, 0, 0, 1, 1, 1, 1],  # Grade 1
    4: [1, 0, 0, 0, 0, 1, 1]   # Grade 2
}

# Create the optimization model
model = Model(solver_name=CBC)

# Define the decision variables
x = [[model.add_var(var_type=BINARY) for j in range(nurses)] for i in range(days)]

# Define the objective function
model.objective = minimize(
    xsum(penalties[nurse][day] * x[day][nurse] for day in range(days) for nurse in range(nurses)))

# Define the constraints
for day in range(days):
    model += xsum(x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] == 1) for nurse in range(nurses)) >= early_shift_requirements[day][0]
    model += xsum(x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] <= 2) for nurse in range(nurses)) >= early_shift_requirements[day][1]
    model += xsum(x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] <= 3) for nurse in range(nurses)) >= early_shift_requirements[day][2]
    model += xsum(x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] == 1) for nurse in range(nurses)) <= early_shifts_upper[day][0]
    model += xsum(x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] <= 2) for nurse in range(nurses)) <= early_shifts_upper[day][1]
    model += xsum(x[day][nurse] * workdays[nurse][day] * (nurse_grades[nurse] <= 3) for nurse in range(nurses)) <= early_shifts_upper[day][2]


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
else:
    print('No solution found.')