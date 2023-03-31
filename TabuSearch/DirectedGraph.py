import copy


class DirectedGraph:
    def __init__(self):
        self.graph = dict()
        self.solutions = []

    def addNode(self, id):
        self.graph.update({id: []})

    def addEdge(self, nFrom, nTo, id, weight):
        edges = self._findEdges(nFrom, nTo)
        if len(edges) < 3:
            self.graph.get(nFrom).append(Edge(id, weight, nTo, nFrom))
        else:
            worst = self._findWorstEdge(nFrom, nTo)
            self._removeEdge(worst.fromNode, worst.toNode, worst.nurseId)
            self.graph.get(nFrom).append(Edge(id, weight, nTo, nFrom))

    def _findEdges(self, nFrom, nTo):
        edges = []
        for edge in self.graph.get(nFrom):
            if edge.toNode == nTo:
                edges.append(edge)
        return edges

    def _findWorstEdge(self, nFrom, nTo):
        worst = None
        for edge in self.graph.get(nFrom):
            if edge.toNode == nTo:
                if worst is None:
                    worst = edge
                elif worst.weight < edge.weight:
                    worst = edge
        return worst

    def _removeEdge(self, nFrom, nTo, id):
        for edge in self.graph.get(nFrom):
            if edge.toNode == nTo and edge.nurseId == id:
                self.graph.get(nFrom).remove(edge)

    def search(self, source, sink):
        visited = {}
        for key in self.graph.keys():
            visited.update({key: False})
        path = []
        self.solutions = []
        self._dfs(source, sink, visited, path)
        return self._findBestValidSolution(sink)

    def _dfs(self, node, goal, visited, path):
        visited[node] = True
        path.append(node)

        if len(path) == 1 and node == goal:
            visited[node] = False

        if node == goal and len(path) > 1:
            self.solutions.append(copy.copy(path))
        else:
            for neighbour in self._findNeighbours(node):
                if not visited[neighbour]:
                    self._dfs(neighbour, goal, visited, path)

        path.pop()
        visited[node] = False

    def _findNeighbours(self, node):
        neighbours = []
        for edge in self.graph.get(node):
            neighbours.append(edge.toNode)
        return neighbours


    def _findBestValidSolution(self, goal):
        bestSolution = [], 1
        for path in self.solutions:
            if len(path) <= 5:
                calculatedPath = self._calcPathWeight(path, goal)
                if calculatedPath[1] < bestSolution[1]:
                    bestSolution = calculatedPath
        return bestSolution[0]


    def _calcPathWeight(self, path, goal):
        usedIds = set()
        accWeight = 0
        next = 1
        edgePath = []

        for node in path:
            if node == goal and len(edgePath) > 0:
                return edgePath, accWeight
            else:
                bestEdge = None
                for edge in self._findEdges(node, path[next]):
                    if edge.nurseId not in usedIds:
                        if bestEdge is None:
                            bestEdge = edge
                            usedIds.add(bestEdge.nurseId)
                            edgePath.append(edge)

                        elif bestEdge.weight > edge.weight:
                            bestEdge = edge
                            usedIds.add(bestEdge.nurseId)
                            edgePath.append(edge)

                    else:
                        return [], 1000 # Not a valid solution.

                accWeight += bestEdge.weight
                next += 1


    def __str__(self):
        string = ""

        for node in self.graph.keys():
            string += str(node) + ":  "
            for edge in self.graph.get(node):
                string += str(edge) + "  -  "
            string += "\n"

        return string


class Edge:
    def __init__(self, nurseId, weight, toNode, fromNode):
        self.nurseId = nurseId
        self.weight = weight
        self.toNode = toNode
        self.fromNode = fromNode

    def __str__(self):
        return f"To: {self.toNode}  Nurse: {self.nurseId}   W: {self.weight}"
