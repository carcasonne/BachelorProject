import copy
import unittest

from Domain.Models.Network.NetworkSchedule import NetworkSchedule
from NetworkFlow.FlowNetworkGraph import FlowNetwork
from NetworkFlow.NetworkFlow import NetworkFlow
from Tests.test_networkflow.TestNetworkFlowData import TestNetworkFlowData

# TODO: Tests that would make sense:
# Is graph initialized correctly when given input? Nodes and edges
class test_flowNetwork(unittest.TestCase):

    def setUp(self) -> None:
        self.schedule = copy.deepcopy(TestNetworkFlowData().schedule)
        self.tabuSchedule = copy.deepcopy(TestNetworkFlowData().tabuSchedule)
        self.networkSchedule = NetworkSchedule(self.tabuSchedule, self.schedule)

    def tearDown(self) -> None:
        self.schedule = copy.deepcopy(TestNetworkFlowData().schedule)
        self.tabuSchedule = copy.deepcopy(TestNetworkFlowData().tabuSchedule)
        self.networkSchedule = NetworkSchedule(self.tabuSchedule, self.schedule)

    def test_finds_shortest_path_simple_network_returns_correct_path(self):
        network = self._get_basic_graph()
        expectedPath = [0, 2, 6, 1]
        shortestPath = network.findShortestPath()
        actualPath = [network.source.nodeId]  # should ALWAYS start at source

        for edge in shortestPath:
            actualPath.append(edge.toNode.nodeId)

        self.assertListEqual(expectedPath, actualPath)

    # This is the same as test_finds_shortest_path_simple_network_returns_correct_path
    # Except that the old shortest path is no longer feasible, since its capacity is full
    def test_finds_shortest_path_capacity_counted_returns_correct_path(self):
        network = self._get_basic_graph()
        sourceEdges = network.source.edges
        # Fill up the edge going to node 2. This should force another shortest path
        for edge in sourceEdges:
            if edge.toNode.nodeId == 2:
                edge.flow = edge.capacity

        expectedPath = [0, 3, 4, 5, 1]
        shortestPath = network.findShortestPath()
        actualPath = [network.source.nodeId]  # should ALWAYS start at source

        for edge in shortestPath:
            actualPath.append(edge.toNode.nodeId)

        self.assertListEqual(expectedPath, actualPath)

    # If there is no possible path, due to capacity being reached, None should be returned
    def test_finds_shortest_path_capacity_counted_returns_none(self):
        network = self._get_basic_graph()
        sourceEdges = network.source.edges
        # Fill up the edge going to node 2. This should force another shortest path
        for edge in sourceEdges:
            edge.flow = edge.capacity

        actualPath = network.findShortestPath()

        self.assertIsNone(actualPath)

    # A network, where there does not exist a path from source to sink
    def test_finds_shortest_path_disjoint_network_returns_cannot_find_path_returns_none(self):
        disjointGraph = FlowNetwork(self.schedule, False)
        disjointGraph.source = disjointGraph.createNode()
        disjointGraph.sink = disjointGraph.createNode()

        actualPath = disjointGraph.findShortestPath()

        self.assertIsNone(actualPath)

    def test_finds_shortest_path_network_with_lower_bounds_finds_correct_path(self):
        network = self._get_graph_with_lower_bounds_along_one_path()
        expectedPath = [0, 3, 4, 5, 1]
        shortestPath = network.findShortestPath()
        actualPath = [network.source.nodeId]  # should ALWAYS start at source

        for edge in shortestPath:
            actualPath.append(edge.toNode.nodeId)

        self.assertListEqual(expectedPath, actualPath)

    def _get_basic_graph(self):
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
        return network

    def _get_graph_with_lower_bounds_along_one_path(self):
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
        network.createDirectedPath(node_0, node_3, 0, 1, 1)
        network.createDirectedPath(node_3, node_4, 0, 1, 1)
        network.createDirectedPath(node_4, node_5, 1, 1, 1)
        network.createDirectedPath(node_5, node_0, 2, 1, 1)
        network.createDirectedPath(node_5, node_1, 1, 0, 1)
        network.createDirectedPath(node_1, node_4, 0, 0, 1)
        return network
