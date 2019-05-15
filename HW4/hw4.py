import sys
from datetime import datetime
import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import fsolve

from YahooFinance_Crawler import YahooFinanceCrawler

def get_return(table):
	return (table[1:,:] - table[:-1,:]) / table[:-1,:]

def ASSR(table, r, delta_t):
	mu = np.mean(table, axis=0)
	sigma = np.sqrt(np.var(table, axis=0,ddof=1))
	SR = (mu-r)/sigma*np.sqrt(delta_t)
	skew = stats.skew(table, axis=0)

	return SR * np.sqrt(1 + 2 / 3 * skew * SR)

def Sharpe_Omega(table, r):
	omega=[]
	for t in table.T:
		hist, bins = np.histogram(t, bins=np.arange(np.min(t), np.max(t) + 1e-3,1e-3),density=True)
		interval=np.diff(bins)
		pdf=hist*interval
		cdf=np.cumsum(pdf)
		index=np.searchsorted(bins,r)-1
		omega.append((np.max(t) - r - np.sum(interval[index:] * cdf[index:])) / np.sum(interval[:index] * cdf[:index]))
		
	return np.array(omega)-1

def riskiness(table, r):
	def f1(x, *args):
		return np.sum(np.exp(-args[0] * x)) - args[0].size
	
	Q = []
	table -= r
	for t in table.T:
		guess = 10
		while guess < 1e6:
			ag = fsolve(f1, guess, args=(t))[0]
			if ag != guess:
				break
			guess *= 10
		Q.append(np.exp(-ag))
	return np.array(Q)

def ETF_evaluation(etf_list, frequency, method, download_dir='tmp', has_download=False, **kwargs):
	'''@parameters:
		frequency: 'month', 'week', 'day'
		method:    function(array, rate)
	@return: pd.df: the ranking of ETFs '''
	crawler = YahooFinanceCrawler(download_dir=download_dir, has_download=has_download)
	df, _ = crawler.get_etf_df(etf_list, 'Adj Close', frequency)
	#print(df)
	if kwargs:
		result = method(get_return(df.values), 0.0243, **kwargs)
	else:
		result = method(get_return(df.values), 0.0243)

	order = result.argsort()[::-1]
	df = pd.DataFrame(etf_list[order].reshape(-1, 1), columns=['ETF_Symbol'], index=np.arange(1, result.shape[0] + 1))
	df.index.name = 'Ranking'
	return df
	

###read etf list
df = pd.read_csv(sys.argv[1])
date=datetime.today().date()
etf_list = df["Symbol"][df['Inception'] <= '%d/%d/%d' % (date.year-3, date.month, date.day)].values
#print(etf_list)
has_download = True

ASSR_month_df=ETF_evaluation(etf_list,'month',ASSR, download_dir='ASSR_month',has_download=has_download,delta_t=1/12)
print('ASSR month',ASSR_month_df.head(20),sep='\n')


ASSR_week_df = ETF_evaluation(etf_list,'week',ASSR,download_dir='ASSR_week',has_download=has_download,delta_t=1/52)
print('ASSR week',ASSR_week_df.head(20),sep='\n')


Omega_month_df = ETF_evaluation(etf_list, 'month', Sharpe_Omega, download_dir='Omega_month',has_download=has_download)
print('Omega month',Omega_month_df.head(20),sep='\n')


Omega_week_df = ETF_evaluation(etf_list, 'week', Sharpe_Omega,download_dir='Omega_week',has_download=has_download)
print('Omega week',Omega_week_df.head(20),sep='\n')


riskiness_month_df = ETF_evaluation(etf_list, 'month', riskiness, download_dir='riskiness_month',has_download=has_download)
print('riskiness month',riskiness_month_df.head(20),sep='\n')


riskiness_week_df = ETF_evaluation(etf_list, 'week', riskiness,download_dir='riskiness_week',has_download=has_download)
print('riskiness week',riskiness_week_df.head(20),sep='\n')
