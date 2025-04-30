import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum
import heapq

class Buildings(Enum):
    ECS = 1
    SGMH = 2
    MH = 3
    TSU = 4
    KHS = 5

def draw_map(start, end):
    G = nx.Graph()

    G.add_edge(Buildings.ECS.value, Buildings.SGMH.value, weight=10)
    G.add_edge(Buildings.ECS.value, Buildings.MH.value, weight=7)
    G.add_edge(Buildings.ECS.value, Buildings.KHS.value, weight=12)
    G.add_edge(Buildings.SGMH.value, Buildings.MH.value, weight=5)
    G.add_edge(Buildings.MH.value, Buildings.TSU.value, weight=4)
    G.add_edge(Buildings.TSU.value, Buildings.KHS.value, weight=6)
    G.add_edge(Buildings.SGMH.value, Buildings.TSU.value, weight=11)
    G.add_edge(Buildings.KHS.value, Buildings.MH.value, weight=4)

    # explicitly set positions
    pos = {
        Buildings.ECS.value: (0, 0),
        Buildings.SGMH.value: (-1, 0.3),
        Buildings.MH.value: (2, 0.17),
        Buildings.TSU.value: (4, 0.255),
        Buildings.KHS.value: (5, 0.03)
    }

    options = {
        "font_size": 14,
        "node_size": 2000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 2,
        "width": 2,
    }

    labels = {
        1: "ECS",
        2: "SGMH",
        3: "MH",
        4: "TSU",
        5: "KHS"
    }
    
    path, total_distance = dijkstra(G, start.value, end.value)

    path_edges = list(zip(path, path[1:]))

    edge_colors = []
    for u, v in G.edges():
        if (u, v) in path_edges or (v, u) in path_edges:
            edge_colors.append('red')
        else:
            edge_colors.append('black')

    
    nx.draw_networkx(G, pos, labels=labels, edge_color=edge_colors, **options)

    edges_lables = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edges_lables)

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()

def dijkstra(graph, start, end):
    dist = {}
    prev = {}

    for node in graph.nodes():
        dist[node] = float('inf')
        prev[node] = None

    dist[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue
        for v in graph.neighbors(u):
            edge_weight = graph[u][v]['weight']
            new_dist = current_dist + edge_weight

            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))
    
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = prev[node]
    
    path.reverse()
    return path, dist[end]


draw_map(Buildings.ECS, Buildings.KHS)
