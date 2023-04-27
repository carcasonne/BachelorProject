from NetworkFlow.NetworkNode import Node


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
