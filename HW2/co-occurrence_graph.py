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

def usage_error():
    print("Usage: python co-occurrence_graph.py -r (rank) [-t (threshold)] [-d (rank-rank)] [-dt (d_threshold)] [-k (keyword)]")
    exit()


cmd_dict = {"-r":"", "-t":"0", "-d":"", "-dt":"0", "-k":""}
if len(sys.argv) % 2 == 0:
    usage_error()
for i in range(1, len(sys.argv), 2):
    if sys.argv[i] in cmd_dict:
        cmd_dict[sys.argv[i]] = sys.argv[i + 1]
        #print(sys.argv[i], cmd_dict[sys.argv[i]])
    else:
        usage_error()

df_comatrix = pd.read_csv("co-occurrence_matrix_"+cmd_dict["-r"]+".csv", index_col="label_headers", encoding="utf-8")
df_freq = pd.read_csv("co-occurrence_matrix_diag_"+cmd_dict["-r"]+".csv", index_col="label_headers", encoding="utf-8")
#draw only these specific nodes into graph
spec_nodes = [i for i in df_comatrix.index.values if i.find(cmd_dict["-k"]) != -1]

G = nx.DiGraph()
for i in spec_nodes:
    for j in df_comatrix.columns.values:
#condition
        if i != j and df_comatrix.ix[i, j] >= float(cmd_dict["-t"]):
            G.add_edge(i, j)

if cmd_dict["-d"] != "":
    df_diffmatrix = pd.read_csv("diff_matrix_"+cmd_dict["-d"]+".csv", index_col="label_headers", encoding="utf-8")
    sub_edge = []
    if cmd_dict["-d"].find(cmd_dict["-r"]) == 0:
        for i in spec_nodes:
            for j in G.nodes:
                if i != j and df_diffmatrix.ix[i, j] >= float(cmd_dict["-dt"]):
                    sub_edge.append((i, j))
                    #print(i, j, df_comatrix.ix[i, j])
    else:
        for i in spec_nodes:
            for j in G.nodes:
                if i != j and df_diffmatrix.ix[i, j] <= float(cmd_dict["-dt"]):
                    sub_edge.append((i, j))
                    #print(i, j, df_comatrix.ix[i, j])
    H = G.edge_subgraph(sub_edge)
    drawing_graph(H, [df_freq.ix[u, "freq"] for u in H.nodes], [df_comatrix.ix[u, v]*2 for u, v in H.edges])
else:
    drawing_graph(G, [df_freq.ix[u, "freq"] for u in G.nodes], [df_comatrix.ix[u, v]*2 for u, v in G.edges])
