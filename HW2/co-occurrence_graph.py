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

def drawing_graph(G, nodesize, edgesize):
    #k = distances between nodes
    pos = nx.spring_layout(G, k = 1, iterations = 20)
    nx.draw(G, pos, with_labels=True, font_size=8, font_weight='bold', node_size=nodesize,
            width = edgesize, edge_color='#adabab', node_color='#84c5ed')
    plt.show()

df_comatrix = pd.read_csv(sys.argv[1], index_col="label_headers", encoding="utf-8")
df_freq = pd.read_csv(sys.argv[2], index_col="label_headers", encoding="utf-8")
#draw only these specific nodes into graph
#spec_nodes = [i for i in df_comatrix.index.values]
spec_nodes = [i for i in df_comatrix.index.values if i.find("年收入") != -1]

G = nx.DiGraph()
for i in spec_nodes:
    for j in df_comatrix.columns.values:
#condition
        if i != j and df_comatrix.ix[i, j] >= 0.6:
            G.add_edge(i, j)

if len(sys.argv) == 4:
    df_diffmatrix = pd.read_csv(sys.argv[3], index_col="label_headers", encoding="utf-8")
    sub_edge = []
    for i in spec_nodes:
        for j in G.nodes:
#condition according to diff_matrix
            #if i != j and (df_diffmatrix.ix[i, j] >= 0.6):
            if i != j and (df_diffmatrix.ix[i, j] <= -0.6):
                sub_edge.append((i, j))
                #print(i, j, df_comatrix.ix[i, j])
    H = G.edge_subgraph(sub_edge)
    drawing_graph(H, [df_freq.ix[u, "freq"] for u in H.nodes], [df_comatrix.ix[u, v]*2 for u, v in H.edges])
else:
    drawing_graph(G, [df_freq.ix[u, "freq"] for u in G.nodes], [df_comatrix.ix[u, v]*2 for u, v in G.edges])
