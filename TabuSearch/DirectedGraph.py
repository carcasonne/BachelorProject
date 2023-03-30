import copy


class DirectedGraph:
    def __init__(self):
        self.graph = dict()
        self.solutions = []

    def addNode(self, id):
        self.graph.update({id: []})

    def addEdge(self, nFrom, nTo, id, weight):
        edge = self._findEdge(nFrom, nTo)
        if edge is None:
            self.graph.get(nFrom).append(Edge(id, weight, nTo))
        elif edge.weight > weight:
            self._removeEdge(nFrom, nTo)
            self.graph.get(nFrom).append(Edge(id, weight, nTo))

    def _findEdge(self, nFrom, nTo):
        for edge in self.graph.get(nFrom):
            if edge.toNode == nTo:
                return edge
        return None

    def _removeEdge(self, nFrom, nTo):
        for edge in self.graph.get(nFrom):
            if edge.toNode == nTo:
                self.graph.get(nFrom).remove(edge)

    def search(self, source, sink):
        visited = {}
        for key in self.graph.keys():
            visited.update({key: False})
        path = []
        self.solutions = []
        self._dfs(source, sink, visited, path)
        return self._findFirstValidSolution()


    def _dfs(self, node, goal, visited, path):
        visited[node] = True
        path.append(node)

        if node == goal:
            self.solutions.append(copy.copy((path)))
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


    def _findFirstValidSolution(self):
        pass


    def __str__(self):
        string = ""

        for node in self.graph.keys():
            string += str(node) + ":  "
            for edge in self.graph.get(node):
                string += str(edge) + "  -  "
            string += "\n"

        return string


class Edge:
    def __init__(self, nurseId, weight, toNode):
        self.nurseId = nurseId
        self.weight = weight
        self.toNode = toNode

    def __str__(self):
        return f"To: {self.toNode}  Nurse: {self.nurseId}   W: {self.weight}"
