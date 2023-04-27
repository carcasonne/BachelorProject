import operator


class Node:
    def __init__(self, nodeId):
        self.nodeId = nodeId
        self.edges = []  # list of all edges going out of this node
        self.inEdges = []
        # Special case for day nodes
        self.day = None
        self.grade = None

    # Note that if network is typed, we will run into a circular import error
    def isBalanced(self, network):
        if self != network.source and self != network.sink:
            flowIn = 0
            flowOut = 0
            for edge in self.edges:
                flowOut = flowOut + edge.flow
            for edge in self.inEdges:
                flowIn = flowIn + edge.flow
            if flowIn != flowOut:
                return False
        return True

    def balanceFlowInNode(self):
        flowIn = 0
        flowOut = 0
        for edge in self.edges:
            flowOut = flowOut + edge.flow
        for edge in self.inEdges:
            flowIn = flowIn + edge.flow
        if flowIn == flowOut:
            return

        if flowIn > flowOut:
            neededFlow = flowIn - flowOut
            self._pushFlowThroughEdges(self.edges, neededFlow)
        elif flowIn < flowOut:
            neededFlow = flowOut - flowIn
            self._pushFlowThroughEdges(self.inEdges, neededFlow)

    def _pushFlowThroughEdges(self, edges, neededFlow):
        eligibleEdges = []
        for edge in edges:
            if edge.flow < edge.capacity:
                residualCapacity = edge.capacity - edge.flow
                eligibleEdges.append((edge, residualCapacity))

        eligibleEdges.sort(key=lambda x: (-x[0].requiredFlow, x[0].cost))

        for (edge, capacity) in eligibleEdges:
            if capacity > neededFlow:
                edge.flow = edge.flow + neededFlow
                neededFlow = 0
                return
            else:
                edge.flow = edge.flow + capacity
                neededFlow = neededFlow - capacity
            if neededFlow == 0:
                return

    def __repr__(self):
        return f"Node {self.nodeId}"
