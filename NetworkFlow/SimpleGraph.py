class DirectedNetworkGraph:
    def __init__(self):
        self.source = Node(0, None)
        self.sink = Node(1, None)
        self.nodeList = [self.source, self.sink]
        self.graph = [[],  # Source Node
                      []]  # Sink Node
        self.V = 2  # Number of vertexes in the graph
        self.E = 0

    def addNode(self, obj):
        index = len(self.graph)
        self.nodeList.append(Node(index, obj))
        self.graph.append([])
        self.V += 1

    def addEdge(self, fromNode, toNode, lowerBound, upperBound, cost):
        self.graph[fromNode].append(Edge(fromNode, toNode, lowerBound, upperBound, cost))
        self.E += 1

    def searching_algo_BFS(self, s, t, parent):
        visited = [False] * self.V
        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)
            next = (-1, 9999, 9999)
            for ind, val in enumerate(self.graph[u]):
                if not visited[val.nTo] and val.flow < val.UB:
                    if next[1] < (val.LB - val.flow):
                        next = ind, val.LB - val.flow, val.cost
                    elif next[1] == (val.LB - val.flow) and val.cost < next[3]:
                        next = ind, val.Lb - val.flow, val.cost
            if next[0] != -1:
                queue.append(ind)
                visited[ind] = True
                parent[ind] = u
        return True if visited[t] else False

    def maxflow(self):
        pass


class Edge:
    def __init__(self, fromNode, toNode, lowerBound, upperBound, cost):
        self.nFrom = fromNode
        self.nTo = toNode
        self.LB = lowerBound
        self.UB = upperBound
        self.cost = cost
        self.flow = 0

    def __str__(self):
        return f"From: {self.nFrom} To: {self.nTo} (l,u,c): ({self.LB},{self.UB},{self.cost})"


class Node:
    def __init__(self, index, obj):
        self.index = index
        if obj is None:
            self.ref = None
        else:
            self.ref = obj.__class__.__name__, obj.id

    def __str__(self):
        if self.ref is None:
            return f"id: {self.id} Ref: (Source/Sink)"
        else:
            return f"id: {self.id} Ref: ({self.ref[0]}, {self.ref[1]})"


g = DirectedNetworkGraph()
for _ in range(4):
    g.addNode(None)

# From source to nurses
g.addEdge(0, 2, 1, 2, 0)
g.addEdge(0, 3, 0, 2, 0)
# From nurses to days
g.addEdge(2, 4, 1, 1, 0)
g.addEdge(4, 2, 0, 1, 1)
g.addEdge(2, 5, 0, 1, 2)
g.addEdge(3, 4, 0, 1, 0)
g.addEdge(3, 5, 0, 1, 1)
# From days to sink
g.addEdge(4, 1, 1, 1, 0)
g.addEdge(5, 1, 0, 1, 0)

source = 0
sink = 1

print(f"Search path is: {str(g.searching_algo_BFS(source, sink, [-1]))}")
