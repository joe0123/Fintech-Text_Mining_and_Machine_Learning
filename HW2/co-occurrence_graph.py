#coding:utf-8
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import _rebuild
_rebuild()
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
#reference: https://blog.csdn.net/helunqu2017/article/details/78602959

df = pd.read_csv("co-occurrence_matrix.csv")
nm_list = df["label_headers"].values
co_matrix = df.drop(columns=["label_headers"]).values
freq_list = [209, 116, 172, 292, 249, 92, 67, 193, 11, 3, 0, 24, 37, 24, 0, 0, 16, 4, 1, 1, 165, 30, 16, 64, 500, 359, 144, 281, 98, 71, 333, 41, 176, 350, 793, 426, 406, 911, 107, 266, 2, 190, 79, 1099, 146, 6, 546, 75, 805, 97, 14, 10, 111, 112, 17, 169, 527, 912, 141, 37, 652, 817, 293, 15, 9, 1373, 311, 101, 29, 20, 17, 31, 77, 305, 678, 695, 71, 17, 53, 442, 1203, 0, 23, 53, 413, 1297, 12, 128, 424, 243, 979, 2, 1, 653, 1080, 50, 5, 105, 445, 580, 651, 47, 193, 351, 437, 758]

G = nx.Graph()
for i in range(len(co_matrix)):
    if freq_list[i] != 0:
        G.add_node(nm_list[i], size = freq_list[i])

for i in range(len(co_matrix)):
    for j in range(len(co_matrix)):
        if (i != j) and (co_matrix[i][j] != 0.0):
            G.add_edge(nm_list[i], nm_list[j], weight = co_matrix[i][j])

pos = nx.spring_layout(G, k = 0.5, iterations = 15)
nx.draw(G, pos, with_labels=True, font_size = 8, font_weight = 'bold', 
        node_size = [u[1]['size']  for u in G.nodes.data()],
        width = [G[u][v]['weight'] for u, v in G.edges()], 
        edge_color = '#adabab', node_color = '#84c5ed')
plt.show()
