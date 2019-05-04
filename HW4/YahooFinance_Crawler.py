import os,glob,sys,time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YahooFinanceCrawler(object):
	def __init__(self,download_dir='tmp'):
		self.download_dir = download_dir
		if not os.path.exists(download_dir):
			os.mkdir(download_dir)
		
		options = webdriver.ChromeOptions()
		prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.path.join(os.getcwd(),download_dir)}
		options.add_experimental_option('prefs', prefs)
		self.driver = webdriver.Chrome(chrome_options=options)

		date = datetime.now()
		self.start_time = '%d'% (datetime(date.year,date.month,date.day).timestamp()-86400*365*3) #back to 3 years ago
		self.end_time='%d'% datetime(date.year,date.month,date.day).timestamp()

		self.etf_list = []
	
	def __del__(self):
		self.driver.quit()

	def download_etf_csv(self, etf_name,frequency='day'):
		self.driver.get('https://finance.yahoo.com/quote/' + etf_name + '/history?period1=' + self.start_time + '&period2=' + self.end_time + '&interval=1d&filter=history&frequency='+{'month':'1mo','week':'1wk','day':'1d'}[frequency])
		#print('downloading',etf_name)
		try:
			button=WebDriverWait(self.driver,20).until(EC.element_to_be_clickable((By.XPATH,"//span[contains(text(),'Download Data')]")))
			#self.driver.implicitly_wait(1)
			button.click()
			#sometimes the crawler will download the same file twice because of the slow network. Therefore we should eliminate it.
			if len(self.etf_list)==0 or self.etf_list[-1] != etf_name: 
				self.etf_list.append(etf_name)
		except:
			print(etf_name, 'is unreachable.', file=sys.stderr)
	
	def get_etf_df(self, etf_name_list, return_cols=None, frequency='day',has_download=False):
		'''@return: (pd.df, list): etf_df, unreachable_etf_list'''
		unreachable=[]
		if not has_download:
			for etf in etf_name_list:
				if os.path.exists(self.download_dir + '/' + etf + '.csv'):
					os.remove(self.download_dir + '/' + etf + '.csv')
				for _ in range(10):
					self.download_etf_csv(etf, frequency)
					time.sleep(2)
					if os.path.exists(self.download_dir + '/' + etf + '.csv'):
						break
				else:
					print('Unable to download ' + etf, file=sys.stderr)
					unreachable.append(etf)
		else:
			self.etf_list = etf_name_list
		return self.get_downloaded_csvs_df(return_cols), unreachable
	
	def get_date_column(self):
		return pd.read_csv(self.download_dir+'/'+self.etf_list[0]+'.csv')['Date']

	def get_downloaded_csvs_df(self,columns=None):
		if columns is None:
			df = pd.concat([pd.read_csv(self.download_dir + '/' + etf + '.csv') for etf in self.etf_list if os.path.exists(self.download_dir + '/' + etf + '.csv')],axis=1,ignore_index=True)
		else:
			df = pd.concat([pd.read_csv(self.download_dir + '/' + etf + '.csv')[columns] for etf in self.etf_list if os.path.exists(self.download_dir + '/' + etf + '.csv')], axis=1, ignore_index=True)
		df.columns = self.etf_list
		df.index = self.get_date_column()
		return df.dropna()
				

def main():
	df = pd.read_csv(sys.argv[1])
	etf_list = list(df["Symbol"][df['Inception']<='2015/12/31'].values)
	#print(etf_list)
	crawler=YahooFinanceCrawler()
	for etf in etf_list:
		crawler.download_etf_csv(etf)
		time.sleep(1)

	df_list = [pd.read_csv(next(glob.iglob('tmp/*.csv')))['Date']]
	for etf in etf_list:
		if not os.path.exists('tmp/' + etf + '.csv'):
			crawler.download_etf_csv(etf)
		if os.path.exists('tmp/' + etf + '.csv'):  #if it still does not exist, ignore it
			df_list.append(pd.read_csv('tmp/' + etf + '.csv')['Adj Close'])
		else:
			etf_list.remove(etf)
	
	df = pd.concat(df_list, axis=1, ignore_index=True)
	df.columns = ['Date'] + etf_list
	print(df.head())

if __name__ == "__main__":
	main()