import os,glob,sys,time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YahooFinanceCrawler(object):
	def __init__(self,download_dir='tmp'):
		options = webdriver.ChromeOptions()
		if not os.path.exists(download_dir):
			os.mkdir(download_dir)
		prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.path.join(os.getcwd(),download_dir)}
		options.add_experimental_option('prefs', prefs)
		self.driver = webdriver.Chrome(chrome_options=options)

		date = datetime.now()
		self.timestamp='%d'% datetime(date.year,date.month,date.day).timestamp()

	def __del__(self):
		self.driver.quit()

	def get_etf_csv(self, etf_name):
		self.driver.get('https://finance.yahoo.com/quote/'+etf_name+'/history?period1=1451577600&period2='+self.timestamp+'&interval=1d&filter=history&frequency=1d')
		#print('downloading',etf_name)
		try:
			button=WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//span[contains(text(),'Download Data')]")))
			#self.driver.implicitly_wait(1)
			button.click()
		except:
			print(etf_name,'is not reachable.',file=sys.stderr)

def main():
	df = pd.read_csv(sys.argv[1])
	etf_list = list(df["Symbol"][df['Inception']<='2015/12/31'].values)
	#print(etf_list)
	crawler=YahooFinanceCrawler()
	for etf in etf_list:
		crawler.get_etf_csv(etf)
		time.sleep(1)

	df_list = [pd.read_csv(next(glob.iglob('tmp/*.csv')))['Date']]
	for etf in etf_list:
		if not os.path.exists('tmp/' + etf + '.csv'):
			crawler.get_etf_csv(etf)
		if os.path.exists('tmp/' + etf + '.csv'):  #if it still does not exist, ignore it
			df_list.append(pd.read_csv('tmp/' + etf + '.csv')['Adj Close'])
		else:
			etf_list.remove(etf)
	
	df = pd.concat(df_list, axis=1, ignore_index=True)
	df.columns = ['Date'] + etf_list
	print(df.head())

if __name__ == "__main__":
	main()