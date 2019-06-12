import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
def draw(title=None, xlabel=None, ylabel=None, has_legend=False,savefig=False):
	if title is not None:
		plt.title(title)
	if xlabel is not None:
		plt.xlabel(xlabel)
	if ylabel is not None:
		plt.ylabel(ylabel)
	if has_legend:
		plt.legend()
	if savefig is False:
		plt.show()
	else:
		plt.savefig(savefig)
	plt.close()


def get_return(buy_data,net_value, compared_fund):
	buy_data=buy_data.fillna(0).drop('總計',axis=1) #delete the last column

	people = dict()
	people_tot_month_money=dict()
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
			people_tot_month_money[ID]+=money
		else:
			people[ID] = [(return_rate, cum_money)]
			people_tot_month_money[ID]=money

	specific_fund_return=dict()
	for ID in people:
		book_value = net_value[compared_fund] * np.cumsum(np.nan_to_num(people_tot_month_money[ID] / net_value[compared_fund]))
		cum_money = np.cumsum(people_tot_month_money[ID])
		specific_fund_return[ID] = np.nan_to_num((book_value - cum_money) / cum_money)
	
	#print(notfound)
	#average return of people, return of the specific fund
	return {p: np.ma.average([tup[0] for tup in people[p]], axis=0, weights=[tup[1] for tup in people[p]]).filled(0) for p in people}, \
		specific_fund_return
	
	
# init net_value
net_value = pd.read_csv('net_value.csv', encoding='utf-8')
net_value.index = net_value['local']
net_value = net_value.drop('local',axis=1).to_dict('index')
net_value = {n: np.array(list(net_value[n].values())) for n in net_value}

buy_data_dict = pd.read_excel('pure_buy_data.xlsx', sheet_name=None)
ave_return_and_currency_return = {sheet_name: get_return(buy_data_dict[sheet_name], net_value, '野村貨幣市場基金' if sheet_name[1] == '4' else '野村中國機會基金') for sheet_name in buy_data_dict}
ave_return = {sheet_name: ave_return_and_currency_return[sheet_name][0] for sheet_name in ave_return_and_currency_return}
currency_return = {sheet_name: ave_return_and_currency_return[sheet_name][1] for sheet_name in ave_return_and_currency_return}

#print(list(ave_return['R5-1交易'].values())[5:10])

client_vec_4 = pd.read_csv('client_vec_4.csv', encoding='utf-8')
client_vec_4 = dict(zip(client_vec_4['客戶ID'], client_vec_4.iloc[:, 1:].values))
client_vec_5 = pd.read_csv('client_vec_5.csv', encoding='utf-8')
client_vec_5 = dict(zip(client_vec_5['客戶ID'], client_vec_5.iloc[:, 1:].values))

'''
cum_opt = {'A01': 24, 'A02': 31, 'A04': 36, 'A05': 39, 'A08': 46, 'A09': 55, 'A10': 60, 'A11': 65, 'A12': 68,
 'A14': 71, 'B01': 76, 'B02': 81, 'B03': 86, 'B04': 91, 'B05': 96, 'B06': 101, 'B07': 106}'''

expected_return = {sheet_name: {p: [0.015, 0.04, 0.07, 0.105, 0.12][np.argmax(client_vec_4[p][96:101] if sheet_name[1]=='4' else client_vec_5[p][96:101])] for p in ave_return[sheet_name].keys()} for sheet_name in ave_return}
expected_loss={sheet_name: {p: [-0.015, -0.04, -0.07, -0.105, -0.12][np.argmax(client_vec_4[p][101:106] if sheet_name[1]=='4' else client_vec_5[p][96:101])] for p in ave_return[sheet_name].keys()} for sheet_name in ave_return}

return_diff = {sheet_name: np.array([sheet[p][-1] - expected_return[sheet_name][p] for p in sheet]) for sheet_name,sheet in ave_return.items()}
loss_diff = {sheet_name: np.array([np.min(sheet[p]) - expected_loss[sheet_name][p] for p in sheet]) for sheet_name,sheet in ave_return.items()}
currency_diff = {sheet_name: np.array([sheet[p][-1] - currency_return[sheet_name][p][-1] for p in sheet]) for sheet_name,sheet in ave_return.items()}

matplotlib.rcParams['axes.unicode_minus'] = False

for sheet_name in ave_return.keys():
	plt.boxplot([return_diff[sheet_name],loss_diff[sheet_name],currency_diff[sheet_name]],labels=['return','loss','currency'])
	draw(sheet_name)
