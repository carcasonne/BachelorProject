import math
from dataclasses import dataclass, field
from typing import Any
import queue

from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Network.NetworkSchedule import NetworkSchedule


class Node:
    def __init__(self, nodeId):
        self.nodeId = nodeId
        self.edges = []  # list of all edges going out of this node
        self.inEdges = []
        # Special case for day nodes
        self.day = None
        self.grade = None

    def __repr__(self):
        return f"Node {self.nodeId}"


class DirectedEdge:
    def __init__(self, edgeId, fromNode: Node, toNode: Node, cost: int, lowerBound: int, upperBound: int):
        self.edgeId = edgeId
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = 0 + cost
        self.requiredFlow = lowerBound
        self.capacity = upperBound + 0
        self.flow = 0
        self.reverseEdge = None

    def __repr__(self):
        return f"Edge {self.edgeId} from node {self.fromNode.nodeId} to node {self.toNode.nodeId}"

@dataclass(order=True)
class PrioritizedNode:
    priority: int
    item: Node = field(compare=False)


class BoundedNetworkFlow:
    def __init__(self, networkSchedule: NetworkSchedule, initialize: bool = True):
        self.source = None
        self.sink = None
        self.schedule = networkSchedule
        self.nurseIdToNodeId = {}  # nurse id to the node representing this nurse
        self.dayToNodeId = {}  # day to grade to int (nodeId) dictionary
        self.nodes = []  # item at index 'i' should have nodeId 'i'
        self.edges = []  # item at index 'i' should have edgeId 'i'
        self.reverseEdges = []  # item at index 'i' is the reverse edge of edgeId 'i'

        for day in Days:
            self.dayToNodeId[day] = {
                Grade.ONE: -1,
                Grade.TWO: -1,
                Grade.THREE: -1,
            }

        if initialize:
            self.initNetwork()

    def initNetwork(self):
        self.source = self.createNode()
        self.sink = self.createNode()

        # Make nodes for each nurse
        # Connect these nodes to the source
        for nurse in self.schedule.nurses:
            nurseNode = self.createNode()
            self.nurseIdToNodeId[nurse.id] = nurseNode.nodeId
            self.createDirectedPath(self.source, nurseNode, 0, nurse.LB, nurse.UP)

        # Make nodes for each day
        for day in Days:
            dayNode_grade_1 = self.createNode()
            dayNode_grade_2 = self.createNode()
            dayNode_grade_3 = self.createNode()
            dayNode_grade_1.day = day
            dayNode_grade_1.grade = Grade.ONE
            dayNode_grade_2.day = day
            dayNode_grade_2.grade = Grade.TWO
            dayNode_grade_3.day = day
            dayNode_grade_3.grade = Grade.THREE
            self.dayToNodeId[day][Grade.ONE] = dayNode_grade_1.nodeId
            self.dayToNodeId[day][Grade.TWO] = dayNode_grade_2.nodeId
            self.dayToNodeId[day][Grade.THREE] = dayNode_grade_3.nodeId

            (requiredEarly_1, requiredLate_1) = self.schedule.getRequiredForDay(day, Grade.ONE)
            (requiredEarly_2, requiredLate_2) = self.schedule.getRequiredForDay(day, Grade.TWO)
            (requiredEarly_3, requiredLate_3) = self.schedule.getRequiredForDay(day, Grade.THREE)
            nursesOnDay_1 = self.schedule.getNursesWorkingDay(day, Grade.ONE)
            nursesOnDay_2 = self.schedule.getNursesWorkingDay(day, Grade.TWO)
            nursesOnDay_3 = self.schedule.getNursesWorkingDay(day, Grade.THREE)

            lowerBound_1 = requiredEarly_1
            upperBound_1 = len(nursesOnDay_1) - requiredLate_1
            lowerBound_2 = requiredEarly_2
            upperBound_2 = len(nursesOnDay_2) - requiredLate_2
            lowerBound_3 = requiredEarly_3
            upperBound_3 = len(nursesOnDay_3) - requiredLate_3

            # Make day chain, from grade 1 to 2 to 3 to sink
            self.createDirectedPath(dayNode_grade_1, dayNode_grade_2, 0, lowerBound_1, upperBound_1)
            self.createDirectedPath(dayNode_grade_2, dayNode_grade_3, 0, lowerBound_2, upperBound_2)
            self.createDirectedPath(dayNode_grade_3, self.sink, 0, lowerBound_3, upperBound_3)

        # Connect the nurse nodes to day nodes
        for nurse in self.schedule.nurses:
            if not nurse.worksNight:
                nurseNodeId = self.nurseIdToNodeId[nurse.id]
                nurseNode = self.nodes[nurseNodeId]
                for day in Days:
                    if nurse.worksDay(day):
                        dayNodeId = self.dayToNodeId[day][nurse.grade]
                        dayNode = self.nodes[dayNodeId]
                        cost = nurse.shiftPreference[day.value - 1]
                        # Get rid of negative weights as stated in the paper
                        if cost < 0:
                            self.createDirectedPath(nurseNode, dayNode, 0, 1, 1)
                            self.createDirectedPath(dayNode, nurseNode, -cost, 0, 1)
                        else:
                            self.createDirectedPath(nurseNode, dayNode, cost, 0, 1)

        # Relax restrictions for nurses working more than 3 days

    def fillOutMinFlows(self):
        # Fill out all the required flows
        # Only consider edges going out of nurse nodes to begin with
        nurseNodeIds = self.nurseIdToNodeId.values()
        for nodeId in nurseNodeIds:
            node = self.nodes[nodeId]
            for edge in node.edges:
                edge.flow = edge.requiredFlow

        balanced = False
        # self._correctFlow()
        # self._correctFlow()
        # self._correctFlow()
        """while not balanced:
            self._correctFlow()
            stop = True
            for node in self.nodes:
                if node != self.source and node != self.sink:
                    flowIn = 0
                    flowOut = 0
                    for edge in node.edges:
                        flowOut = flowOut + edge.flow
                    for edge in node.inEdges:
                        flowIn = flowIn + edge.flow
                    if flowIn != flowOut:
                        stop = False
                        break
            balanced = stop"""

    def _correctFlow(self):
        # Find the edges, wherein the flow is not balanced
        for node in self.nodes:
            if node != self.source and node != self.sink:
                flowIn = 0
                flowOut = 0
                for edge in node.edges:
                    flowOut = flowOut + edge.flow
                for edge in node.inEdges:
                    flowIn = flowIn + edge.flow
                if flowIn == flowOut:
                    continue

                if flowIn > flowOut:
                    eligibleEdges = []
                    for edge in node.edges:
                        if edge.flow < edge.capacity:
                            residualCapacity = edge.capacity - edge.flow
                            eligibleEdges.append((edge, residualCapacity))

                    neededFlow = flowIn - flowOut
                    for (edge, capacity) in eligibleEdges:
                        if capacity > neededFlow:
                            edge.flow = edge.flow + neededFlow
                            neededFlow = 0
                            break
                        else:
                            edge.flow = edge.flow + capacity
                            neededFlow = neededFlow - capacity
                        if neededFlow == 0:
                            break
                elif flowIn < flowOut:
                    eligibleEdges = []
                    for edge in node.inEdges:
                        if edge.flow < edge.capacity:
                            residualCapacity = edge.capacity - edge.flow
                            eligibleEdges.append((edge, residualCapacity))
                    neededFlow = flowOut - flowIn
                    for (edge, capacity) in eligibleEdges:
                        if capacity > neededFlow:
                            edge.flow = edge.flow + neededFlow
                            neededFlow = 0
                            break
                        else:
                            edge.flow = edge.flow + capacity
                            neededFlow = neededFlow - capacity
                        if neededFlow == 0:
                            break

    def transformIntoUnbounded(self):
        # Create the new source and sink
        newSource = self.createNode()
        newSink = self.createNode()

        originalEdges = self.edges.copy()

        for node in self.nodes:
            if node != self.source and node != self.sink:
                # First connect the new source to this node
                # Capacity is the sum of all lower bounds going into node
                capacity = 0
                for edge in originalEdges:  # would be smarter to preprocess this, i no longer care
                    if edge.toNode == node:
                        capacity = capacity + edge.requiredFlow

                self.createDirectedPath(newSink, node, 0, 0, capacity)

                # Now connect this node to the new sink
                # Capacity is sum of lower bounds of edges going out of this node
                capacity = 0
                for edge in node.edges:
                    capacity = capacity + edge.requiredFlow

                self.createDirectedPath(node, newSource, 0, 0, capacity)

        for edge in originalEdges:
            edge.capacity = edge.capacity - edge.requiredFlow

        # Connect old sink to old source
        self.createDirectedPath(self.sink, self.source, 0, 0, float('inf'))
        # Update source and sinks
        self.source = newSource
        self.sink = newSink

    # For every edge, add a reverse edge with capacity 0
    def addReverseEdges(self):
        # Copying the list, otherwise self.create... would add a new edge to the same list. infinite loop
        # only copy the list itself, element references must remain the same
        copiedList = self.edges.copy()
        for edge in copiedList:
            reverseEdge = self.createDirectedPath(edge.toNode, edge.fromNode, 0, 0, 0)
            reverseEdge.flow = -edge.flow
            reverseEdge.reverseEdge = edge
            edge.reverseEdge = reverseEdge

    # Finds the shortest path (by cost) from source to sink
    # Dijkstra's algorithm using bread first search
    # Note that this DOES NOT impact flow. It just finds the shortest path by cost
    def findShortestPath(self):
        distance = [float('inf')] * len(self.nodes)
        previous = [None] * len(self.nodes)  # Stores the edge used to go to node with index i
        distance[self.source.nodeId] = 0

        Q = queue.PriorityQueue()
        Q.put(PrioritizedNode(0, self.source))
        foundSink = False

        while Q.qsize() != 0 and not foundSink:
            pi = Q.get()
            visiting = pi.item

            # Return once we get to the sink
            if visiting == self.sink:
                foundSink = True
                continue

            for edge in visiting.edges:
                if edge.flow == edge.capacity:
                    continue

                neighborId = edge.toNode.nodeId
                newDistance = distance[visiting.nodeId] + edge.cost  # Current cost + cost of moving to neighbor

                if newDistance < distance[neighborId]:
                    distance[neighborId] = newDistance
                    previous[neighborId] = edge
                    Q.put(PrioritizedNode(newDistance, edge.toNode))

        # Extract the path into a list for itself
        # If no path was found, return None
        if previous[self.sink.nodeId] is None:
            return None

        path = []
        edge = previous[self.sink.nodeId]
        while edge is not None:
            path.insert(0, edge)  # Reverse order, so the list starts with edge going out of the source
            edge = previous[edge.fromNode.nodeId]

        return path

    # Creates a new node, and adds it to the network
    # Returns the node object
    def createNode(self):
        newId = len(self.nodes)
        node = Node(newId)
        self.nodes.append(node)
        return node

    # Creates a directed path from a node to another, and adds the edge to the network
    # Returns the edge object
    def createDirectedPath(self, fromNode: Node, toNode: Node, cost: int, lowerBound: int, upperBound: int):
        newId = len(self.edges)
        dirEdge = DirectedEdge(newId, fromNode, toNode, cost, lowerBound, upperBound)
        fromNode.edges.append(dirEdge)  # add to edges going out of fromNode
        toNode.inEdges.append(dirEdge)  # add to edges going into toNode
        self.edges.append(dirEdge)

        return dirEdge

    # Returns if the critical edges (from day to sink) are within the required bounds
    # These edges are critical, because they determine feasibility of the solution as a whole
    def criticalBoundsSatisfied(self):
        for day in Days:
            for grade in Grade:  # must be feasible for all grades
                dayNodeId = self.dayToNodeId[day][grade]
                edge = self.nodes[dayNodeId].edges[0]  # Only 1 edge, which goes to sink

                if edge.flow < edge.requiredFlow:
                    return False

        return True

    # This is meant to be called after a flow has been created
    def nurseAssignment(self):
        nurseToDayToFlow = {}
        for nurse in self.schedule.nurses:
            nurseToDayToFlow[nurse] = {}
            for day in Days:
                nurseToDayToFlow[nurse][day] = -1

        for nurse in self.schedule.nurses:
            nodeId = self.nurseIdToNodeId[nurse.id]
            node = self.nodes[nodeId]
            for edge in node.edges:
                if edge.toNode.day is None or edge.toNode.day is None:
                    continue
                nurseToDayToFlow[nurse][edge.toNode.day] = edge.flow

        return nurseToDayToFlow
