import copy
import unittest

from Domain.Models.Network.NetworkSchedule import NetworkSchedule
from NetworkFlow.FlowNetworkGraph import FlowNetwork
from NetworkFlow.NetworkFlow import NetworkFlow
from Tests.test_networkflow.TestNetworkFlowData import TestNetworkFlowData


class test_flowNetwork(unittest.TestCase):

    def setUp(self) -> None:
        self.schedule = copy.deepcopy(TestNetworkFlowData().schedule)
        self.tabuSchedule = copy.deepcopy(TestNetworkFlowData().tabuSchedule)
        self.networkSchedule = NetworkSchedule(self.tabuSchedule, self.schedule)
        network = FlowNetwork(self.networkSchedule, False)
        node_0 = network.createNode()
        node_1 = network.createNode()
        network.source = node_0
        network.sink = node_1
        node_2 = network.createNode()
        node_3 = network.createNode()
        node_4 = network.createNode()
        node_5 = network.createNode()
        node_6 = network.createNode()
        network.createDirectedPath(node_0, node_2, 1, 0, 1)
        network.createDirectedPath(node_2, node_6, 1, 0, 1)
        network.createDirectedPath(node_6, node_1, 1, 0, 1)
        network.createDirectedPath(node_0, node_3, 0, 0, 1)
        network.createDirectedPath(node_3, node_4, 1, 0, 1)
        network.createDirectedPath(node_4, node_5, 2, 0, 1)
        network.createDirectedPath(node_5, node_0, 0, 0, 1)
        network.createDirectedPath(node_5, node_1, 1, 0, 1)
        network.createDirectedPath(node_1, node_4, 0, 0, 1)
        self.basicGraph = network

    def tearDown(self) -> None:
        self.schedule = copy.deepcopy(TestNetworkFlowData().schedule)
        self.tabuSchedule = copy.deepcopy(TestNetworkFlowData().tabuSchedule)
        self.networkSchedule = NetworkSchedule(self.tabuSchedule, self.schedule)
        self.basicGraph = None

    def test_finds_shortest_path_simple_network_returns_correct_path(self):
        expectedPath = [0, 2, 6, 1]
        shortestPath = self.basicGraph.findShortestPath()
        actualPath = [self.basicGraph.source.nodeId]  # should ALWAYS start at source

        for edge in shortestPath:
            actualPath.append(edge.toNode.nodeId)

        self.assertListEqual(expectedPath, actualPath)

    # This is the same as test_finds_shortest_path_simple_network_returns_correct_path
    # Except that the old shortest path is no longer feasible, since its capacity is full
    def test_finds_shortest_path_capacity_counted_returns_correct_path(self):
        sourceEdges = self.basicGraph.source.edges
        # Fill up the edge going to node 2. This should force another shortest path
        for edge in sourceEdges:
            if edge.toNode.nodeId == 2:
                edge.flow = edge.capacity

        expectedPath = [0, 3, 4, 5, 1]
        shortestPath = self.basicGraph.findShortestPath()
        actualPath = [self.basicGraph.source.nodeId]  # should ALWAYS start at source

        for edge in shortestPath:
            actualPath.append(edge.toNode.nodeId)

        self.assertListEqual(expectedPath, actualPath)

    # If there is no possible path, due to capacity being reached, None should be returned
    def test_finds_shortest_path_capacity_counted_returns_none(self):
        sourceEdges = self.basicGraph.source.edges
        # Fill up the edge going to node 2. This should force another shortest path
        for edge in sourceEdges:
            edge.flow = edge.capacity

        actualPath = self.basicGraph.findShortestPath()

        self.assertIsNone(actualPath)

    # A network, where there does not exist a path from source to sink
    def test_finds_shortest_path_disjoint_network_returns_cannot_find_path_returns_none(self):
        disjointGraph = FlowNetwork(self.schedule, False)
        disjointGraph.source = disjointGraph.createNode()
        disjointGraph.sink = disjointGraph.createNode()

        actualPath = disjointGraph.findShortestPath()

        self.assertIsNone(actualPath)
