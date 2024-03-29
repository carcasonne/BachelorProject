import copy

from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.ShiftType import TabuShiftType
from Domain.Models.Network.NetworkSchedule import NetworkSchedule
from Domain.Models.Schedule import Schedule
from Domain.Models.ShiftPatterns.ShiftPattern import StandardShiftPattern
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from NetworkFlow.NetworkFlowGraph import NetworkFlowGraph


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


def runNetworkFlow(schedule: Schedule, tabuSchedule: TabuSchedule):
    networkSchedule = NetworkSchedule(tabuSchedule, schedule)
    flowNetwork = NetworkFlowGraph(networkSchedule)
    flowNetwork.fillOutMinFlows()
    # flow = EdmondsKarp(flowNetwork)
    solution = buildFinalSchedule(schedule, tabuSchedule, flowNetwork)
    return solution


# Manipulates the input network to add the min-cost flow to edges
# Also returns the flow created in the network
def EdmondsKarp(network: NetworkFlowGraph):
    flow = 0
    continueSearching = True
    residualNetwork = network
    residualNetwork.addReverseEdges()

    while continueSearching:
        if residualNetwork.criticalBoundsSatisfied():
            continueSearching = False
            continue

        shortestPath = residualNetwork.findShortestPath()
        if shortestPath is None:
            continueSearching = False
            continue

        # Finds the max flow which will fit in the entire path
        df = float('inf')
        for edge in shortestPath:
            df = min(df, edge.capacity - edge.flow)

        for edge in shortestPath:
            edge.flow = edge.flow + df
            edge.reverseEdge.flow = edge.reverseEdge.flow - df

        flow = flow + df

    if not network.criticalBoundsSatisfied():
        raise Exception("BIG problem!!!... infeasible early/late allocation found ")

    for edge in network.edges:
        flow = edge.flow
        if edge.reverseEdge.flow != -edge.flow:
            raise Exception(f"{edge.flow} != -{edge.reverseEdge.flow}! Constraints broken")

    return flow


# Build the final solution
# Takes shifts and nurses from schedule
# Takes nurses working night from tabuSchedule
# Takes nurses working early/late from flowNetwork
def buildFinalSchedule(schedule: Schedule, tabuSchedule: TabuSchedule, networkFlow: NetworkFlowGraph):
    solutionShifts = copy.deepcopy(schedule.shifts)
    solutionNurses = copy.deepcopy(schedule.nurses)

    nightNurseIds = set([n.id for n in tabuSchedule.nurses if n.worksNight])

    # Make sure all nurses have the shift patterns determined from the tabu search
    for tabuNurse in tabuSchedule.nurses:
        if tabuNurse.worksNight:
            solutionNurse = solutionNurses[tabuNurse.id]
            solutionNurse.assignedShiftPattern = StandardShiftPattern([0] * 7, [0] * 7, tabuNurse.shiftPattern.night)

    # Assign all nurses working late from tabu schedule to new schedule
    for tabuShift in tabuSchedule.shifts:
        if tabuShift.shiftType == TabuShiftType.NIGHT:
            index = (tabuShift.shiftDay.value - 1) * 3 + 2
            solutionShift = solutionShifts[index]
            solutionShift.assignedNurses = tabuShift.assignedNurses

    # Assign all nurses working day to either early or late
    dayAssignment = networkFlow.nurseAssignment()
    for nurse in networkFlow.schedule.nurses:
        if nurse.id not in nightNurseIds:
            solutionNurse = solutionNurses[nurse.id]
            earlyPattern = [0] * 7
            latePattern = [0] * 7
            for day in Days:
                dayIndex = (day.value - 1) * 3  # The index of the first shift in the day (early)
                nurseAssignment = dayAssignment[nurse][day]
                if nurseAssignment == -1:  # Nurse not working this day
                    continue
                elif nurseAssignment == 0:  # Nurse assigned late
                    latePattern[day.value - 1] = 1
                    solutionShifts[dayIndex + 1].addNurse(solutionNurse)
                elif nurseAssignment >= 1:  # Nurse assigned early
                    earlyPattern[day.value - 1] = 1
                    solutionShifts[dayIndex].addNurse(solutionNurse)
            solutionNurse.assignedShiftPattern = StandardShiftPattern(earlyPattern, latePattern, [0] * 7)

    return Schedule(solutionShifts, solutionNurses)
