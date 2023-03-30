class DirectedGraph:
    def __init__(self):
        self.graph = dict()

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
        self.dfs(set(), source, sink)

    def dfs(self, visited, node, goal):
        if node not in visited:
            visited.add(node)
            for neighbour in self.findNeighbours(node):
                self.dfs(visited, self.graph, neighbour)

    def findNeighbours(self, node):
        neighbours = []
        for edge in self.graph.get(node):
            neighbours.append(edge.toNode)
        return  neighbours


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
