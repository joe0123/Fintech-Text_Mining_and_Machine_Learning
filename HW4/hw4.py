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
	sigma = np.std(table, axis=0,ddof=1)
	SR = (mu - r * delta_t) / sigma * np.sqrt(delta_t)
	skew = stats.skew(table, axis=0)

	return SR * np.sqrt(1 + 2 / 3 * skew * SR)

def Sharpe_Omega(table, r, delta_t):
	r *= delta_t
	return (np.sum(table, axis=0)-r) / (np.sum(r-table[table <= r], axis=0))
	#return (np.sum(table[table >= r]-r, axis=0)) / (np.sum(r-table[table <= r], axis=0))-1
	

def riskiness(table, r, delta_t):
	def f1(x, *args):
		return np.mean(np.exp(-args[0]*x)) - 1
	table = table.astype(np.longdouble)
	
	Q = []
	table -= r*delta_t
	for t in table.T:
		for i in range(4):
			ag = fsolve(f1, 10**i, args=(t), maxfev=10000)[0]
			if abs(ag) > 1e-5:
				break
		else:
			guess = -1
			while True:
				ag = fsolve(f1, guess, args=(t), maxfev=10000)[0]
				if abs(ag) > 1e-5:
					break
				guess -= 10
		#print(ag, f1(ag,t))
		Q.append(np.exp(-ag))
	return np.array(Q)

def ETF_evaluation(etf_list, frequency, method, download_dir='tmp', has_download=False):
	'''@parameters:
		frequency: 'month', 'week'
		method:    function(array, rate)
	@return: pd.df: the ranking of ETFs '''
	crawler = YahooFinanceCrawler(download_dir=download_dir, has_download=has_download)
	df, _ = crawler.get_etf_df(etf_list, 'Adj Close', frequency)
	#print(df)
	result = method(get_return(df.values), 0.0243, {'month':1/12,'week':1/52}[frequency])

	order = result.argsort()[::-1]
	df = pd.DataFrame(etf_list[order].reshape(-1, 1), columns=['ETF_Symbol'], index=np.arange(1, result.shape[0] + 1))
	df.index.name = 'Ranking'
	return df
	
if __name__ == "__main__":	
	###read etf list
	df = pd.read_csv(sys.argv[1])
	date=datetime.today().date()
	etf_list = df["Symbol"][df['Inception'] <= '%d/%d/%d' % (date.year-3, date.month, date.day)].values
	#print(etf_list)
	if len(sys.argv) > 2:
		has_download = True if sys.argv[2] == 'true' else False
	else:
		has_download = False

	ASSR_month_df=ETF_evaluation(etf_list,'month',ASSR, download_dir='tmp_month',has_download=has_download)
	#print('ASSR month',ASSR_month_df.head(20),sep='\n')


	ASSR_week_df = ETF_evaluation(etf_list,'week',ASSR,download_dir='tmp_week',has_download=has_download)
	#print('ASSR week',ASSR_week_df.head(20),sep='\n')


	Omega_month_df = ETF_evaluation(etf_list, 'month', Sharpe_Omega, download_dir='tmp_month',has_download=True)
	#print('Omega month',Omega_month_df.head(20),sep='\n')


	Omega_week_df = ETF_evaluation(etf_list, 'week', Sharpe_Omega,download_dir='tmp_week',has_download=True)
	#print('Omega week',Omega_week_df.head(20),sep='\n')


	riskiness_month_df = ETF_evaluation(etf_list, 'month', riskiness, download_dir='tmp_month',has_download=True)
	#print('riskiness month',riskiness_month_df.head(20),sep='\n')


	riskiness_week_df = ETF_evaluation(etf_list, 'week', riskiness,download_dir='tmp_week',has_download=True)
	#print('riskiness week',riskiness_week_df.head(20),sep='\n')

	whole = pd.concat((ASSR_month_df, ASSR_week_df, Omega_month_df, Omega_week_df, riskiness_month_df, riskiness_week_df), axis=1)
	whole.columns = ['ASSR_month', 'ASSR_week', 'Omega_month', 'Omega_week', 'riskiness_month', 'riskiness_week']
	print(whole.head(20).to_string())