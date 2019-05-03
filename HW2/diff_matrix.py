#coding:utf-8
import sys
import pandas as pd

def csv_to_data(csv_fn):
    df = pd.read_csv(csv_fn, encoding="utf-8")
    nm_list = df["label_headers"].values
    co_matrix = df.drop(columns=["label_headers"]).values
    return nm_list, co_matrix

nm_list, co_matrix1 = csv_to_data(sys.argv[1])
nm_list, co_matrix2 = csv_to_data(sys.argv[2])

diff_matrix = co_matrix1 - co_matrix2
dt = pd.DataFrame(data=diff_matrix)
dt.columns = nm_list
dt.insert(0, column='label_headers', value = nm_list)
dt.to_csv(sys.argv[3], index=False, encoding="utf-8")
