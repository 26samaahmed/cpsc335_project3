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

    G.add_edge(Buildings.ECS.value, Buildings.SGMH.value)
    G.add_edge(Buildings.ECS.value, Buildings.MH.value)
    G.add_edge(Buildings.ECS.value, Buildings.KHS.value)
    G.add_edge(Buildings.SGMH.value, Buildings.MH.value)
    G.add_edge(Buildings.MH.value, Buildings.TSU.value)
    G.add_edge(Buildings.TSU.value, Buildings.KHS.value)

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

    path = []
    for i in range(len(Buildings)):
        pass
    
    edge_colors = []
    
    nx.draw_networkx(G, pos, labels=labels, **options)

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()




draw_map(1, 2)
