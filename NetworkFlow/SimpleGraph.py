class DirectedNetworkGraph:
    def __init__(self):
        self.graph = {Node(0, None): [],  # Source Node
                      Node(1, None): []}  # Sink Node

    def addNode(self, id, obj):
        self.graph.update({Node(id, obj): []})

    def addEdge(self, fromNode, toNode, lowerBound, upperBound, cost):
        self.graph.get(fromNode).append(Edge(fromNode, toNode, lowerBound, upperBound, cost))

    def maxFlow(self):
        pass

    def BFS(self):
        pass


class Edge:
    def __init__(self, fromNode, toNode, lowerBound, upperBound, cost):
        self.nFrom = fromNode
        self.nTo = toNode
        self.LB = lowerBound
        self.UB = upperBound
        self.cost = cost

    def __str__(self):
        return f"From: {self.nFrom} To: {self.nTo} (l,u,c): ({self.LB},{self.UB},{self.cost})"


class Node:
    def __init__(self, id, obj):
        self.id = id
        if obj is None:
            self.ref = None
        else:
            self.ref = obj.__class__.__name__, obj.id

    def __str__(self):
        if self.ref is None:
            return f"id: {self.id} Ref: (Source/Sink)"
        else:
            return f"id: {self.id} Ref: ({self.ref[0]}, {self.ref[1]})"



def max_flow(C, s, t):
    n = len(C)  # C is the capacity matrix
    F = [[0] * n for i in range(n)]
    path = bfs(C, F, s, t)
    #  print path
    while path != None:
        flow = min(C[u][v] - F[u][v] for u, v in path)
        for u, v in path:
            F[u][v] += flow
            F[v][u] -= flow
        path = bfs(C, F, s, t)
    return sum(F[s][i] for i in range(n))


# find path by using BFS
def bfs(C, F, s, t):
    queue = [s]
    paths = {s: []}
    if s == t:
        return paths[s]
    while queue:
        u = queue.pop(0)
        for v in range(len(C)):
            if (C[u][v] - F[u][v] > 0) and v not in paths:
                paths[v] = paths[u] + [(u, v)]
                print(paths)
                if v == t:
                    return paths[v]
                queue.append(v)
    return None


# make a capacity graph
# node   s   o   p   q   r   t
C = [[0, 3, 3, 0, 0, 0],  # s
     [0, 0, 2, 3, 0, 0],  # o
     [0, 0, 0, 0, 2, 0],  # p
     [0, 0, 0, 0, 4, 2],  # q
     [0, 0, 0, 0, 0, 2],  # r
     [0, 0, 0, 0, 0, 3]]  # t

source = 0  # A
sink = 5  # F
max_flow_value = max_flow(C, source, sink)
print ("Edmonds-Karp algorithm")
print ("max_flow_value is: ", max_flow_value)