import os
import datetime
import urllib.request as url
import pandas as pd

download_dir='download'
if not os.path.exists(download_dir):
	os.mkdir(download_dir)
url.urlretrieve('https://www.quandl.com/api/v3/datasets/FRED/NAPMPRI.csv?api_key=Gy65phJwPp3dpbzSY7sR&collapse=monthly&end_date='+str(datetime.datetime.now().date()),
				'./'+download_dir+'/ISM_Manufacturing.csv')

df = pd.read_csv(download_dir+'/ISM_Manufacturing.csv')
df.columns = ['Date', 'Value']
df = df.reindex(index=df.index[::-1])
df.index=df.index[::-1]
print(df.head(20))