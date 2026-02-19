from itertools import combinations

def is_connected_after_removal(graph, removed_nodes):
    
    # find a start node that is not removed
    remaining_nodes = [node for node in graph.adj if node not in removed_nodes]
    
    if not remaining_nodes:
        return False  # no nodees left = considered disconnected
    
    start = remaining_nodes[0]
    
    visited = set([start])
    index = 0
    queue = [start]

    while index < len(queue):
        current_node = queue[index]
        index += 1

        for neighbour in graph.adj[current_node]:
            if neighbour not in visited and neighbour not in removed_nodes:
                visited.add(neighbour)
                queue.append(neighbour)

    # graph is connected if allremaining nodes are visited
    return len(visited) == len(remaining_nodes)


def k_cutset(graph, k):
    nodes = list(graph.adj.keys())

    # try all combinations of k nodes
    for combo in combinations(nodes, k):
        removed = set(combo)

        if not is_connected_after_removal(graph, removed):
            print("Cutset found:", combo)
            return True

    return False

# test if k=3 cutset exists
print("\nDoes a 3-cutset exist?")
result = k_cutset(graph, 3)
print("Result:", result)
