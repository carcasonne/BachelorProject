class DirectedGraph:
    def __init__(self):
        self.graph = dict()
        self.visited = set()

    def addNode(self, id):
        self.graph.update({id: []})

    def addEdge(self, nFrom, nTo, id, weight):
        exists = False
        for edge in self.graph.get(nFrom):
            if edge.toNode == nTo:
                exists = True
                if edge.weight > weight:
                    self.graph.get(nFrom).remove(edge)
                    self.graph.get(nFrom).append(Edge(id, weight, nTo))
                break
        if not exists:
            self.graph.get(nFrom).append(Edge(id, weight, nTo))

    def search(self, source, sink):
        visited = set()

        def dfs(visited, graph, node):
            if node not in visited:
                print(node)
                visited.add(node)
                for neighbour in graph[node]:
                    dfs(visited, graph, neighbour)


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
