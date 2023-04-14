from Domain.Models.Network.NetworkSchedule import NetworkSchedule


class Node:
    def __init__(self, nodeId):
        self.nodeId = nodeId
        self.edges = []     # list of all edges going out of this node
        self.flowIn = 0     # reevaluate later if this is necesarry
        self.flowOut = 0    # reevaluate later if this is necesarry


class DirectedEdge:
    def __init__(self, edgeId, fromNode: Node, toNode: Node):
        self.edgeId = edgeId
        self.fromNode = fromNode
        self.toNode = toNode
        self.capacity = 0
        self.flow = 0


class FlowNetwork:
    def __init__(self, networkSchedule: NetworkSchedule):
        self.source = None
        self.sink = None
        self.schedule = networkSchedule
        self.nurseIdToNodeId = {}   # nurse id to the node representing this nurse
        self.dayToNodeId = {}       # day to the first node in the chain representing this day
        self.nodes = []             # item at index 'i' should have nodeId 'i'
        self.edges = []             # item at index 'i' should have edgeId 'i'

        self.initNetwork()

    def initNetwork(self):
        self.source = self.createNode()
        self.sink = self.createNode()

        # Make nodes for each day
        # Make nodes for each nurse
        # Connect the nodes

    # Creates a new node, and adds it to the network
    # Returns the node object
    def createNode(self):
        newId = len(self.nodes)
        node = Node(newId)
        self.nodes.append(node)
        return node

    # Creates a directed path from a node to another, and adds the edge to the network
    # Returns the edge object
    def createDirectedPath(self, fromNode: Node, toNode: Node, capacity: int):
        newId = len(self.edges)
        dirEdge = DirectedEdge(newId, fromNode, toNode)
        fromNode.edges.append(dirEdge) # add to edges going out of fromNode
        self.edges.append(dirEdge)
        return dirEdge

    # Finds a minimum flow solution in the network
    # Implementation finds the solution, which violates fewest early/late preferences
    def findMinimumCostFlow(self):
        pass
