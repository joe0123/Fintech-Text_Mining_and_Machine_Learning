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
freq_list = []
with open('co-occurrence_matrix_diagonal.txt', 'r') as f:
    freq_list = [float(i.strip('\n'))*5 for i in f]

G = nx.Graph()
for i in range(len(co_matrix)):
    if freq_list[i] != 0:
        G.add_node(nm_list[i], size = freq_list[i])

for i in range(len(co_matrix)):
    for j in range(len(co_matrix)):
        if (i != j) and (co_matrix[i][j] >= 0.8):
            G.add_edge(nm_list[i], nm_list[j], weight = co_matrix[i][j])

#k = distances between nodes
pos = nx.spring_layout(G, k = 1, iterations = 50)
nx.draw(G, pos, with_labels=True, font_size=8, font_weight='bold', node_size=[u[1]['size']  for u in G.nodes.data()],
        width = [G[u][v]['weight'] for u, v in G.edges()], edge_color='#adabab', node_color='#84c5ed')
plt.show()
