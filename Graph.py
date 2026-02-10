from collections import deque

class Graph:
    def __init__(self):
        self.adj= {}

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = deque()

    def connect_node(self, a, b):
        if a not in self.adj or b not in self.adj:
            return
        if b not in self.adj[a]:
            self.adj[a].append(b)
            self.adj[b].append(a)

# we use index to avoid list.pop(0) which is O(n)
# we can remove elements once the queue is large to reduce memory
def bfs(graph, start):
    visited = set([start])
    index = 0
    queue = [start]
    traversal_order = []

    while index < len(queue):
        current_node = queue[index]
        index += 1
        traversal_order.append(current_node)

        for neighbour in graph.adj[current_node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return traversal_order


graph = Graph()
graph.add_node('A')
graph.add_node('B')
graph.add_node('C')
graph.add_node('D')
graph.add_node('E')
graph.add_node('F')
graph.connect_node('A', 'B')
graph.connect_node('A', 'C')
graph.connect_node('A', 'D')
graph.connect_node('D', 'E')
graph.connect_node('D', 'F')
print('Traversal Order:', bfs(graph, 'A'))