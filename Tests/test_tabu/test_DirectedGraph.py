import copy
import unittest

from Domain.Models.ShiftPatterns.ShiftPattern import TabuShiftPattern
from Domain.Models.Tabu.TabuSchedule import TabuSchedule
from TabuSearch.DirectedGraph import DirectedGraph
from TabuSearch.DirectedGraph import Edge
from TabuSearch.StaticMethods import evaluateCC
from Tests.test_tabu.TestTabuData import TestTabuData
from TabuSearch.TabuSearch_SIMPEL import TabuSearch_SIMPLE


class Test_DirectedGraph(unittest.TestCase):

    def setUp(self) -> None:
        self.graph = DirectedGraph()
        self.graph.addNode(0)
        self.graph.addNode(1)
        self.graph.addNode(2)
        self.graph.addNode(3)

        self.graph.addEdge(0, 1, 0, 0)
        self.graph.addEdge(0, 2, 0, -10)
        self.graph.addEdge(0, 3, 0, 10)
        self.graph.addEdge(1, 2, 0, 10)
        self.graph.addEdge(1, 3, 0, -10)
        self.graph.addEdge(2, 3, 0, -20)

    def tearDown(self) -> None:
        self.graph = DirectedGraph()
        self.graph.addNode(0)
        self.graph.addNode(1)
        self.graph.addNode(2)
        self.graph.addNode(3)
        self.graph.addNode(4)

        self.graph.addEdge(0, 1, 0, 0)
        self.graph.addEdge(0, 2, 0, -10)
        self.graph.addEdge(0, 3, 0, 10)
        self.graph.addEdge(1, 2, 0, 10)
        self.graph.addEdge(1, 3, 0, -10)
        self.graph.addEdge(2, 3, 0, -20)

    # ----------------------- addEdge(self, nFrom, nTo, id, weight) ---------------------------
    def test_addEdge_replaces_current_edge_if_new_weight_is_lower_than_current(self):
        oldEdge = self.graph._findEdge(0, 1)
        self.graph.addEdge(0, 1, 1, -10)
        newEdge = self.graph._findEdge(0, 1)

        self.assertEqual(0, oldEdge.weight)
        self.assertEqual(0, oldEdge.nurseId)
        self.assertEqual(-10, newEdge.weight)
        self.assertEqual(1, newEdge.nurseId)
        self.assertTrue(oldEdge.weight > newEdge.weight)

    def test_addEdge_does_not_replace_current_edge_if_new_weight_is_higher_than_current(self):
        oldEdge = self.graph._findEdge(0, 1)
        self.graph.addEdge(0, 1, 1, 10)
        newEdge = self.graph._findEdge(0, 1)

        self.assertEqual(0, oldEdge.weight)
        self.assertEqual(0, oldEdge.nurseId)
        self.assertEqual(0, newEdge.weight)
        self.assertEqual(0, newEdge.nurseId)
        self.assertTrue(oldEdge == newEdge)

    # ----------------------- search(self, source, sink) ---------------------------
    def test_search_for_path_between_0_3_returns_all_possible_paths(self):
        expectedPaths = [[0, 3], [0, 1, 3], [0, 2, 3], [0, 1, 2, 3]]
        self.graph.search(0, 3)
        actualPaths = self.graph.solutions
        self.assertEqual(len(expectedPaths), len(actualPaths))
        for path in expectedPaths:
            self.assertTrue(path in actualPaths)

    def test_search_for_path_between_0_4_returns_no_possible_paths(self):
        expectedPaths = []
        self.graph.search(0, 4)
        actualPaths = self.graph.solutions
        self.assertEqual(len(expectedPaths), len(actualPaths))

    def test_search_for_path_between_0_3_two_times_in_a_row_returns_only_all_possible_paths_one_time(self):
        expectedPaths = [[0, 3], [0, 1, 3], [0, 2, 3], [0, 1, 2, 3]]
        self.graph.search(0, 3)
        self.graph.search(0, 3)
        actualPaths = self.graph.solutions
        self.assertEqual(len(expectedPaths), len(actualPaths))
        for path in expectedPaths:
            self.assertTrue(path in actualPaths)

    def test_search_for_path_between_0_3_returns_0_2_3(self):
        expected = self.graph._pathToEdges([0, 2, 3], 3)
        actual = self.graph.search(0, 3)
        self.assertEqual(expected, actual)

    def test_search_for_path_between_0_2_returns_0_2(self):
        expected = self.graph._pathToEdges([0, 2], 2)
        actual = self.graph.search(0, 2)
        self.assertEqual(expected, actual)

    def test_search_for_path_between_3_0_returns_nothing(self):
        expected = self.graph._pathToEdges([], 0)
        actual = self.graph.search(3, 0)
        self.assertEqual(expected, actual)

    # ----------------------- _pathToEdges(self, path, goal) ---------------------------
    def test_path_to_edges_between_0_3_returns_path_in_edges(self):
        path = [0, 2, 3]
        expected = []
        for edge in self.graph.graph[0]:
            if edge.toNode == 2:
                expected.append(edge)
        for edge in self.graph.graph[2]:
            if edge.toNode == 3:
                expected.append(edge)

        actual = self.graph._pathToEdges(path, 3)
        for i in range(2):
            self.assertEqual(expected[i].nurseId, actual[i].nurseId)

    def test_path_to_edges_between_0_2_returns_path_in_edges(self):
        path = [0, 2]
        expected = []
        for edge in self.graph.graph[0]:
            if edge.toNode == 2:
                expected.append(edge)

        actual = self.graph._pathToEdges(path, 2)
        self.assertEqual(expected[0].nurseId, actual[0].nurseId)
        self.assertEqual(expected[0].fromNode, actual[0].fromNode)
        self.assertEqual(expected[0].toNode, actual[0].toNode)
        self.assertEqual(expected[0].weight, expected[0].weight)




if __name__ == '__main__':
    unittest.main()