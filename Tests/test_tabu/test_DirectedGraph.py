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


if __name__ == '__main__':
    unittest.main()