#cmd: python co-occurrence_graph.py (matrix).csv (matrix_diag).csv [(diff_matrix).csv]

import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import _rebuild
_rebuild()
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
#reference: https://blog.csdn.net/helunqu2017/article/details/78602959

def drawing_graph(G):
    #k = distances between nodes
    pos = nx.spring_layout(G, k = 1, iterations = 20)
    nx.draw(G, pos, with_labels=True, font_size=8, font_weight='bold', node_size=[u[1]['size']  for u in G.nodes.data()],
            width = [G[u][v]['weight'] for u, v in G.edges()], edge_color='#adabab', node_color='#84c5ed')
    plt.show()


df_comatrix = pd.read_csv(sys.argv[1], index_col="label_headers", encoding="utf-8")
df_freq = pd.read_csv(sys.argv[2], index_col="label_headers", encoding="utf-8")
#draw only these specific nodes into graph
spec_nodes = df_comatrix.index.values

G = nx.Graph()
for i in spec_nodes:
    if df_freq.ix[i, "freq"] != 0:
        G.add_node(i, size = df_freq.ix[i, "freq"])
    for j in df_comatrix.columns.values:
        if (i != j and df_comatrix.ix[i, j] > 0):
            assert(df_freq.ix[i, "freq"] != 0 and df_freq.ix[i, "freq"] != 0)
            G.add_edge(i, j, weight = df_comatrix.ix[i, j])

if len(sys.argv) == 4:
    df_diffmatrix = pd.read_csv(sys.argv[3], index_col="label_headers", encoding="utf-8")
    sub_edge = []
    for i in spec_nodes:
        for j in df_diffmatrix.columns.values:
            #condition according to diff_matrix
            if df_diffmatrix.ix[i, j] <= -0.4:
                sub_edge.append((i, j))
    H = G.edge_subgraph(sub_edge)
    drawing_graph(H)
else:
    drawing_graph(G)

