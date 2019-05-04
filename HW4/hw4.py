import os,glob,sys,time
from datetime import datetime
from YahooFinance_Crawler import YahooFinanceCrawler
import pandas as pd
import numpy as np
from scipy import stats
def get_return(table):
	return (table[:-1,:] - table[1:,:]) / table[1:,:]

def ASKSR(table, r):
	#print(table)
	mu = np.mean(table, axis=0)
	sigma = np.sqrt(np.var(table, axis=0))
	K = stats.kurtosis(table, axis=0)
	S = stats.skew(table, axis=0)
	print(mu,sigma,K,S,sep='\n')
	
	k4s9 = 3 * K - 4 * S ** 2 - 9
	k5s9 = 3 * K - 5 * S ** 2 - 9
	print(k4s9,k5s9,sep='\n')
	
	alpha = 3 * np.sqrt(k4s9) / sigma ** 2 / k5s9
	beta = 3 * S / sigma / k5s9
	eta = mu - 3 * S * sigma / k4s9
	delta = 3 * sigma * np.sqrt(k5s9) / k4s9
	a_star = beta + alpha * (eta - r) / np.sqrt(delta ** 2 + (eta - r)** 2)

	#print('\n',alpha,beta,eta,delta,a_star,sep='\n')

	return np.sqrt(2 * a_star * (eta - r) - delta * (np.sqrt(alpha ** 2 - beta ** 2) - np.sqrt(alpha ** 2 - (beta - a_star)** 2)))

def ETF_evaluation(etf_list, frequency, method, download_dir='tmp', has_download=False):
	'''@parameters:
		frequency: 'month', 'week', 'day'
		method:    function(array, rate)
	@return: pd.df: the ranking of ETFs '''
	crawler = YahooFinanceCrawler(download_dir=download_dir)
	df, _ = crawler.get_etf_df(etf_list, 'Adj Close', frequency, has_download)
	#print(df)
	result = method(get_return(df.values), 0.0005)
	order = result.argsort()[::-1]
	df = pd.DataFrame(etf_list[order].reshape(-1, 1), columns=['ETF_Symbol'], index=np.arange(1, result.shape[0] + 1))
	df.index.name = 'Ranking'
	return df
	

###read etf list
df = pd.read_csv(sys.argv[1])
date=datetime.today().date()
etf_list = df["Symbol"][df['Inception'] <= '%d/%d/%d' % (date.year-3, date.month, date.day)].values
#print(etf_list)

month_df=ETF_evaluation(etf_list,'month',ASKSR, has_download= True)
print(month_df.head(20))


week_df = ETF_evaluation(etf_list,'week',ASKSR,download_dir='tmp_week',has_download=True)
print(week_df.head(20))
