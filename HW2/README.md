# HW2
## 1. 整理問卷資料 ([sparse_matrix.py](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/sparse_matrix.py))
1. 將問卷資料稍作整理，只保留客戶ID、題目編號、答案等資訊，轉存成`client_list.csv`
2. 整理`client_list.csv`的資料，將每個客戶的每個題目的答案轉為vector，回答該選項為1，否則為0
3. 將結果轉存為`client_vec.csv`

## 2. 得出co-occurrence matrix ([co-occurrence_matrix.ipynb](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/co-occurrence_matrix.ipynb))
1. 讀取`client_vec.csv`，算出co-occurrence matrix，將結果存至`co-occurrence matrix.csv`
2. 得到熱點圖
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/heatmap_output.png)

## 3. 畫出共現圖 ([co-occurrence_graph.py](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/co-occurrence_graph.py))
讀取`co-occurrence matrix.csv`，畫出共現圖
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/co-occurrence_graph.png)
