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
            self.graph.get(nFrom).append(Edge(id, weight, nTo, nFrom))
        elif edge.weight > weight:
            self._removeEdge(nFrom, nTo)
            self.graph.get(nFrom).append(Edge(id, weight, nTo, nFrom))

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
        print(self.solutions)
        counter = 0
        while counter < len(self.solutions):
            print("Solution " + str(counter) + " Weight: " + str(self._calcPathWeight(self.solutions[counter], sink)))
            counter += 1
        print("Chosen solution first: " + str(self._findFirstValidSolution(sink)))
        print("Chosen solution best: " + str(self._findBestValidSolution(sink)))
        best = self._findBestValidSolution(sink)
        return self._pathToEdges(best, sink)

    def _dfs(self, node, goal, visited, path):
        visited[node] = True
        path.append(node)

        if node == goal:
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


    def _findFirstValidSolution(self, goal):
        for path in self.solutions:
            if len(path) <= 5:
                calculatedWeight = self._calcPathWeight(path, goal)
                if calculatedWeight <= 0:
                    return path
        return None

    def _findBestValidSolution(self, goal):
        bestSolution = [], 1
        for path in self.solutions:
            if len(path) <= 5:
                calculatedWeight = self._calcPathWeight(path, goal)
                if calculatedWeight < bestSolution[1]:
                    bestSolution = path, calculatedWeight
        return bestSolution[0]

    def _calcPathWeight(self, path, goal):
        accWeight = 0
        next = 1
        for node in path:
            if node == goal:
                return accWeight
            else:
                accWeight += self._findEdge(node, path[next]).weight
                next += 1

    def _pathToEdges(self, path, goal):
        edges = []
        next = 1
        for node in path:
            if node == goal:
                return edges
            else:
                edges.append(self._findEdge(node, path[next]))
                next += 1
        return edges


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
