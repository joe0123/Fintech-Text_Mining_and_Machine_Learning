# HW2
## 1. 整理風險等級四和五的客戶問卷資料 ([sparse_matrix.py](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/sparse_matrix.py))
(以下以風險等級四為例，將4換成5便可求得風險等級5的資料)  
1. 將問卷資料稍作整理，只保留風險等級4的客戶ID、題目編號、答案等資訊，轉存成`client_list_4.csv`
2. 整理`client_list_4.csv`的資料，將每個客戶的每個題目的答案轉為vector，回答該選項為1，否則為0
3. 將結果轉存為`client_vec_4.csv`

## 2. 得出co-occurrence matrix ([co-occurrence_matrix.ipynb](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/co-occurrence_matrix.ipynb))
(以下以風險等級四為例，將4換成5便可求得風險等級5的資料)  
1. 讀取`client_vec_4.csv`，算出co-occurrence matrix，將結果存至`co-occurrence matrix.csv`
2. 得到熱點圖  

#### rank4:  
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/heatmap_output_4.png)
#### rank5:
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/heatmap_output_5.png)

## 3. 畫出共現圖 `python co-occurrence_graph.py co-occurrence_matrix_4.csv co-occurrence_matrix_diag_4.csv`
(以下以風險等級四為例，將4換成5便可求得風險等級5的資料)  
讀取`co-occurrence_matrix_4.csv`，畫出共現圖  
#### rank4:  
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/graph_4.png)
#### rank5:  
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/graph_5.png)

## 4. 篩出co-occurrence matrix中value較高的edge 
(以下以風險等級四為例，將4換成5便可求得風險等級5的資料)  
1. 執行`python histogram_percentage.py co-occurrence_matrix_4.csv`畫出所有共現值的histogram，選出0.6作為threshold(該處比例的變化較穩定)。  
2. 在改動co-occurrence_graph.py的condition後，執行`python co-occurrence_graph.py co-occurrence_matrix_4.csv co-occurrence_matrix_diag_4.csv`畫出subgraph  

#### rank4 co-occurrence value histogram:
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/histogram_4.png)
#### rank4 co-occurrence subgraph:  
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/graph_4_60.png)
#### rank5 co-occurrence value histogram:
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/histogram_5.png)
#### rank5 co-occurrence subgraph:  
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/graph_5_60.png)

## 5. 比較風險等級4和5共現值 畫出在各matrix中較為顯著的edge
1. 執行`python diff_matrix.py co-occurrence_matrix_4.csv co-occurrence_matrix_5.csv diff_matrix_45.csv`，將co-occurrence_matrix_4減去co-occurrence_matrix_5.csv後存為diff_matrix_45.csv；其中，正值表示該共現值在co-occurrence_matrix_4中大於co-occurrence_matrix_5，負值則相反。  
2. 接著參考第四步，分別畫出diff_matrix_45中所有正值和負值的histogram(記得改動histogram_percentage.py的condition)，選出0.6作為正值、-0.6為負值的threshold。  
(以下以風險等級四為例，將4換成5便可求得風險等級5的資料)  
3. 在改動co-occurrence_graph.py的condition according to diff_matrix，執行`python co-occurrence_graph.py co-occurrence_matrix_4.csv co-occurrence_matrix_diag_4.csv diff_matrix_45.csv`畫出subgraph  

#### rank4 co-occurrence subgraph:(表示這些edge在matrix_4比在matrix_5還顯著)  
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/graph_diff4.png)
#### rank5 co-occurrence subgraph:(表示這些edge在matrix_5比在matrix_4還顯著)  
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/graph_diff5.png)

## 6. 挑出subgraph中所有與年收入相關的edge
(以下以風險等級四為例，將4換成5便可求得風險等級5的資料)  
1. 在改動co-occurrence_graph.py的spec_node設為\[i for i in df_comatrix.index.values if i.find("年收入") != -1\]之後，執行`python co-occurrence_graph.py co-occurrence_matrix_4.csv co-occurrence_matrix_diag_4.csv diff_matrix_45.csv`畫出subgraph  

#### rank4 co-occurrence subgraph:  
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/graph_income4.png)
#### rank5 co-occurrence subgraph:  
![](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW2/graph_income5.png)
