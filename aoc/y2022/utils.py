"""
Utility Functions
"""

import os

INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "inputs")

U = (+1, 0)
D = (-1, 0)
L = (0, -1)
R = (0, 1)
NEIGHBOR4 = U, D, L, R


def load_data(file_name, load_as="text"):
    """Load data"""
    full_path = os.path.join(INPUT_DIR, file_name)
    if load_as == "text":
        with open(full_path) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
        return lines
    elif load_as == "int":
        import numpy as np

        return np.loadtxt(full_path, dtype=np.int32)
    elif load_as == "float":
        import numpy as np

        return np.loadtxt(full_path, dtype=np.float)
    else:
        raise ValueError(f'Unsupported type "{load_as}"')


def bfs(adj, src, dest):
    """bfs
    adj = edges
    src = src node
    dest = dest node
    """

    v = len(adj)
    pred = [0 for _ in range(len(adj))]
    dist = [0 for _ in range(len(adj))]

    # a queue to maintain queue of vertices whose
    # adjacency list is to be scanned as per normal
    # DFS algorithm
    queue = []

    # boolean array visited[] which stores the
    # information whether ith vertex is reached
    # at least once in the Breadth first search
    visited = [False for i in range(v)]

    # initially all vertices are unvisited
    # so v[i] for all i is false
    # and as no path is yet constructed
    # dist[i] for all i set to infinity
    for i in range(v):

        dist[i] = 1000000
        pred[i] = -1

    # now source is first to be visited and
    # distance from source to itself should be 0
    visited[src] = True
    dist[src] = 0
    queue.append(src)

    # standard BFS algorithm
    done = False
    while not done and len(queue) != 0:
        u = queue[0]
        queue.pop(0)
        for i in range(len(adj[u])):

            if visited[adj[u][i]] == False:
                visited[adj[u][i]] = True
                dist[adj[u][i]] = dist[u] + 1
                pred[adj[u][i]] = u
                queue.append(adj[u][i])

                # We stop BFS when we find
                # destination.
                if adj[u][i] == dest:
                    done = True
                    break

        # vector path stores the shortest path
        path = []
        crawl = dest
        path.append(crawl)

        while pred[crawl] != -1:
            path.append(pred[crawl])
            crawl = pred[crawl]

    return path


def dijkstra_algorithm(edges, start_node):
    """unweighted dijkstra"""
    unvisited_nodes = list(edges)

    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
    shortest_path = {}

    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    max_value = float("inf")
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0
    shortest_path[start_node] = 0

    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = edges[current_min_node]
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + 1
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path
