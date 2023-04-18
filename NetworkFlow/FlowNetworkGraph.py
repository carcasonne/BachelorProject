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


class DirectedEdge:
    def __init__(self, edgeId, fromNode: Node, toNode: Node, cost: int, lowerBound: int, upperBound: int):
        self.edgeId = edgeId
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = cost
        self.requiredCapacity = lowerBound
        self.capacity = upperBound
        self.flow = 0


@dataclass(order=True)
class PrioritizedNode:
    priority: int
    item: Node = field(compare=False)


class FlowNetwork:
    def __init__(self, networkSchedule: NetworkSchedule, initialize: bool = True):
        self.source = None
        self.sink = None
        self.schedule = networkSchedule
        self.nurseIdToNodeId = {}  # nurse id to the node representing this nurse
        self.dayToNodeId = {}  # day to the first node in the chain representing this day
        self.nodes = []  # item at index 'i' should have nodeId 'i'
        self.edges = []  # item at index 'i' should have edgeId 'i'

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
            self.createDirectedPath(self.source, nurseNode, 0, nurse.UP, nurse.LB)

        # Make nodes for each day
        for day in Days:
            dayNode = self.createNode()
            self.dayToNodeId[day] = dayNode.nodeId

            hej = self.schedule.shifts

            # Connect each day to the sink node
            self.createDirectedPath(dayNode, self.sink, 0, 0, 0)

        # Connect the nurse nodes to day nodes

        # Relax restrictions for nurses working more than 3 days

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
        self.edges.append(dirEdge)
        return dirEdge

    # Finds a minimum flow solution in the network
    # Implementation finds the solution, which violates fewest early/late preferences
    def findMinimumCostFlow(self):
        pass

    def getRequirementsForGrade(self, grade: Grade):
        pass
