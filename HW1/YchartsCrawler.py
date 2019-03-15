from sys import stderr
import requests
from lxml import html
from bs4 import BeautifulSoup as bs

class YchartsCrawler(object):
	def __init__(self):
		login_url = 'https://ycharts.com/login'
		self.s=requests.Session()
		r = self.s.get(login_url)
		#print(r.text)
		tree = html.fromstring(r.content)
		csrftoken = tree.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
		header = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Content-Length': '154',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Cookie': 'hblid=iCUWEtrzvuoSaBSE1y8Lx0Ho6LjzaBA0; olfsk=olfsk24654799029854524; hubspotutk=9473b10f9f6dc66a916324bd17e66739; _cb_ls=1; _cb=GF5G0DpwmFOBNFFvE; __utmc=69688216; _okdetect=%7B%22token%22%3A%2215526127484850%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22ycharts.com%22%7D; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; _ok=1228-592-10-8601; __hssrc=1; BL_D_PROV=; BL_T_PROV=; 33e807c05af9078f6b2ed01ced5fc28d5c8f52f4=1; __utmz=69688216.1552623000.5.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); wcsid=avzniafQ1ALBWESE1y8Lx0HjkrA6az0B; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1552633253117%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; __utma=69688216.1390050295.1552410129.1552634554.1552637930.7; __hstc=165832289.9473b10f9f6dc66a916324bd17e66739.1552410130564.1552634554141.1552637931671.7; _cb_svref=null; \
			csrftoken='+csrftoken+'; __utmt=1; ycsessionid=4nes43ohtrx3xg6wx3kh9zpyon5sqp91; page_view_ctr=35; mp_bd6455515e9730c7dc2f008755a4ddfe_mixpanel=%7B%22distinct_id%22%3A%20%2216972dab16d62b-08497d6f1c1291-9333061-144000-16972dab16ea56%22%2C%22%24device_id%22%3A%20%2216972dab16d62b-08497d6f1c1291-9333061-144000-16972dab16ea56%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24user_id%22%3A%20%2216972dab16d62b-08497d6f1c1291-9333061-144000-16972dab16ea56%22%7D; __utmb=69688216.12.10.1552637930; __hssc=165832289.12.1552637931671; _chartbeat2=.1552410130639.1552639260775.101.CjS4DTBcAWAGC4azV9GUacZDTDvUD.6; _oklv=1552639744895%2CavzniafQ1ALBWESE1y8Lx0HjkrA6az0B',
			'Host': 'ycharts.com',
			'Origin': 'https://ycharts.com',
			'Referer': 'https://ycharts.com/login',
			'Upgrade-Insecure-Requests': '1',
			'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 72.0 .3626 .121 Safari / 537.36'
		}
		payload = {'username': 'dayipoxice@mail-pro.info', 'password': 'seqpBGisd3bdNqH', 'csrfmiddlewaretoken': csrftoken,'next':'','partner':'None','partner_username':'None'}
		r = self.s.post(login_url, data=payload, headers=header)
		assert (r.status_code != '200')
	
	def getETF(self, etf_name, start_date='12/31/2015', end_date='12/31/2018'):
		nav=dict()
		last_page_num=int(self.s.get('https://ycharts.com/companies/' + etf_name + '/net_asset_value.json', params={'endDate': end_date, 'pageNum': '1', 'startDate': start_date}).json()['last_page_num'])
		for i in range(1,last_page_num+1):
			r = self.s.get('https://ycharts.com/companies/' + etf_name + '/net_asset_value.json', params={'endDate': end_date, 'pageNum': str(i), 'startDate': start_date})
			assert (r.status_code != '200')
			
			table = dict(r.json())['data_table_html']
			soup = bs(table, 'html.parser')
			
			first = soup.tr
			while True:
				first = first.find_next('td')
				if first is None:
					break
				val = first.find_next('td')
				nav[first.string] = val.string.strip()
				first=val
		return nav
		
def main():
	crawler=YchartsCrawler()
	hyld = crawler.getETF('HYLD')
	print(hyld)

if __name__ == "__main__":
	main()