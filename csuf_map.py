import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from enum import Enum
import heapq
from matplotlib.animation import FuncAnimation

class Buildings(Enum):
    ECS = 1
    SGMH = 2
    MH = 3
    TSU = 4
    KHS = 5
    PL = 6
    VA = 7
    H = 8

# Building names that appear in GUI mapped to Buildings Enum
string_to_enum = {
    "Engineering & Computer Science Building": Buildings.ECS,
    "McCarthy Hall": Buildings.MH,
    "Steven G. Mihaylo Hall": Buildings.SGMH,
    "Titan Student Union": Buildings.TSU,
    "Kinesiology and Health Science Building": Buildings.KHS,
    "Pollak Library": Buildings.PL,
    "Visual Arts Center": Buildings.VA,
    "Humanities Building": Buildings.H
}

def draw_map(start="", end=""):
    if start != "" and end != "":
        # the start and end points for the paths
        start = string_to_enum[start]
        end = string_to_enum[end]

    # create graph for the nodes and edges
    G = nx.Graph()

    # link the nodes together with weights
    G.add_edge(Buildings.H.value, 15, weight=1)
    G.add_edge(Buildings.MH.value, 15, weight=3)
    G.add_edge(15, 14, weight=7)
    G.add_edge(Buildings.ECS.value, 14, weight=4)
    G.add_edge(14, 9, weight=3)
    G.add_edge(Buildings.KHS.value, 9, weight=1)
    G.add_edge(9, 10, weight=5)
    G.add_edge(Buildings.PL.value, 14, weight=2)
    G.add_edge(Buildings.TSU.value, 10, weight=1)
    G.add_edge(Buildings.VA.value, 13, weight=3)
    G.add_edge(Buildings.MH.value, 13, weight=5)
    G.add_edge(Buildings.SGMH.value, 15, weight=7)
    G.add_edge(Buildings.MH.value, 9, weight=9)
    G.add_edge(Buildings.SGMH.value, Buildings.MH.value, weight=5)
    G.add_edge(Buildings.PL.value, Buildings.MH.value, weight=5)
    G.add_edge(Buildings.PL.value, 9, weight=2)
    G.add_edge(Buildings.VA.value, Buildings.TSU.value, weight=3)

    # set position for all nodes on the graph
    pos = {
        Buildings.ECS.value: (390, 170),
        Buildings.SGMH.value: (370, 400),
        Buildings.MH.value: (250, 340),
        Buildings.PL.value: (260, 215),
        Buildings.TSU.value: (110, 210),
        Buildings.KHS.value: (230, 120),
        Buildings.VA.value: (110, 270),
        Buildings.H.value: (330, 290),
        9: (230, 170), # node below KHS
        10: (110, 170), # node above TSU
        11: (260, 170), # node above PL
        12: (240, 30), # node above MH
        13: (150, 340), # node below VA
        14: (290, 170), # node between PL and ECS
        15: (290, 290) # node left of H
    }

    fig, ax = plt.subplots(figsize=(12, 10))
    
    if start != "" and end != "":
        # find the shortest path
        path = dijkstra(G, start.value, end.value, pos, ax)
        path_edges = list(zip(path, path[1:]))

        # find the mst
        mst = prim(G, len(pos), pos, ax, start)
        mst_edges = []
        for u, v, _ in mst:
            mst_edges.append((u, v))

    # draw map image
    img = mpimg.imread("csuf_map.png")
    ax.imshow(img)

    # draw over the map with the default nodes and edges if no start and end is given
    if start == "" and end == "":
        nx.draw_networkx(G, pos, with_labels=False, width=3, edge_color='green', ax=ax)
        ani = ""
    else:
        # combine the mst and shortest path lists
        edges = mst_edges + path_edges

        # animation for the mst plays first and then the shortest path animation
        def animation(i):
            ax.clear()
            ax.imshow(img)

            # draws the nodes
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color='blue', node_size=500)

            # determines if the mst or shortest path color is used for the animation
            if i < len(mst_edges):
                nx.draw_networkx_edges(G, pos, edgelist=edges[:i+1], ax=ax, edge_color='blue', width=3)
            else:
                nx.draw_networkx_edges(G, pos, edgelist=mst_edges, ax=ax, edge_color='blue', width=3)
                nx.draw_networkx_edges(G, pos, edgelist=path_edges[:i + 1 - len(mst_edges)], ax=ax, edge_color='red', width=3)

        # animation variable that will be used in the gui to play the animation
        ani = FuncAnimation(fig, animation, frames=len(mst_edges) + len(path_edges), interval=500, repeat=False)

    ax.set_axis_off()
    ax.margins(0.20)

    return fig, ani

# finds shortest path
def dijkstra(graph, start, end, pos, ax):
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
    return path

# mst
def prim(graph, n, pos, ax, start):
    visited = [False] * (n + 1)
    min_heap = [(0, start.value, -1)]
    mst_edges = []

    while min_heap:
        cost, u, parent = heapq.heappop(min_heap)
        if visited[u]:
            continue
        visited[u] = True

        if parent != -1:
            mst_edges.append((parent, u, cost))

        for v in graph.neighbors(u):
            weight = graph[u][v]['weight']
            if not visited[v]:
                heapq.heappush(min_heap, (weight, v, u))

    return mst_edges
