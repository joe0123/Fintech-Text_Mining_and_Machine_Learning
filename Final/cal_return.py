import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_return(buy_data,net_value):
	buy_data=buy_data.fillna(0).drop('總計',axis=1) #delete the last column

	people = dict()
	notfound=set()
	for tup in buy_data.itertuples(index=False):
		ID, fund_name = tup[0], tup[1]
		money = np.array(tup[2:])
		#print(fund_name)
		if fund_name not in net_value:
			notfound.add(fund_name)
			continue
		book_value = net_value[fund_name] * np.cumsum(np.nan_to_num(money / net_value[fund_name]))
		cum_money=np.cumsum(money)
		return_rate = np.nan_to_num((book_value - cum_money) / cum_money)
		#print(return_rate)
		if np.any(np.abs(return_rate) >= 0.9):
			print(str(ID)+' '+fund_name,return_rate,sep='\n')
		#input('')
		if ID in people:
			people[ID].append((return_rate, cum_money))
		else:
			people[ID] = [(return_rate, cum_money)]

	#print(notfound)
	#average return of people
	return {p: np.ma.average([tup[0] for tup in people[p]], axis=0, weights=[tup[1] for tup in people[p]]).filled(0) for p in people}
	
net_value = pd.read_csv('net_value.csv', encoding='utf-8')
net_value.index = net_value['local']
net_value = net_value.drop('local',axis=1).to_dict('index')
net_value = {n: np.array(list(net_value[n].values())) for n in net_value}

buy_data_dict = pd.read_excel('pure_buy_data.xlsx', sheet_name=None)
buy_data_dict= { sheet_name: get_return(buy_data_dict[sheet_name],net_value) for sheet_name in buy_data_dict}

# for i in buy_data_dict:
# 	print(list(buy_data_dict[i].values())[0])