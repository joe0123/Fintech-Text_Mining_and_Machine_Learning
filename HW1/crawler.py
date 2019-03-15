import sys
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import urllib.request as url
from selenium import webdriver
import time


df = pd.read_csv(sys.argv[1])
#list of all etfs' symbol names
ETFs = df["Symbol"].values
#files downloaded will be stored in ./download
os.mkdir("download")

def html_code(url):
    try:
        r = requests.get(url)
    except:
        print("\"" + url + "\"", "is not found")
        return "FAIL" 
    assert r.status_code == requests.codes.ok
    #handle html code with BeautifulSoup
    soup = bs(r.text, 'html.parser')
    return soup 

def bs_dl(homepage, head, value, target, filename):
    soup = html_code(homepage)
    if soup == "FAIL":
        return
    #loading point
    ldp = head + soup.find("a", string=value).get(target)
    try:
        url.urlretrieve(ldp, "./download/" + filename)
    except:
        print("Downloading", "\"" + ldp + "\"", "fails")
        return

#initialization for webdriver (downloaded file with original name will be stored in ./tmp)
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd() + '\\tmp'}
options.add_experimental_option('prefs', prefs)
options.add_argument("user-agent={}".format('Googlebot/2.1 (+http://www.google.com/bot.html)'))
#reference# https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers/User-Agent
driver = webdriver.Chrome(chrome_options=options)


def sele_dl(homepage, key, value, filename):
    driver.get(homepage)
    try:
        if key == "xpath":
            driver.find_element_by_xpath(value).click()
        else:
            driver.find_element_by_link_text(value).click()
    except:
        print("Downloading", "\"" + key + "\"", "in", "\"" + homepage + "\"", "fails")
    time.sleep(3)
    
    #file to be renamed was stored in ./tmp
    old_fn = os.listdir("./tmp")
    os.rename("./tmp/" + old_fn[0], "./download/" + filename)
    os.rmdir("./tmp")


for etf in ETFs:
#Find url of Homepage
    soup = html_code("https://www.etf.com/" + etf)
    if soup is None:
        continue
    homepage = soup.find("a", string="Fund Home Page").get("href")
    #DEBUG# print(etf, homepage)

#Download data
    #the url of ETF's family (like iShares, SPDR...)
    family = homepage.split('/')[2]
    if family == "www.ishares.com":
        bs_dl(homepage, "https://" + family, "Download", "href", etf + ".xls")
    elif family == "www.proshares.com":
        bs_dl(homepage, "", "NAV History", "href", etf + ".csv")
    elif family == "us.spdrs.com":
        sele_dl(homepage, "text", "Most Recent NAV / NAV History XLS", etf + ".xls")
    elif family == "www.invesco.com":
        sele_dl(homepage, "text", "Historical NAVs", etf + ".csv")
    elif family == "dws.com":
        sele_dl(homepage, "text", "NAV History (CSV)", etf + ".csv")
    elif family == "www.vaneck.com":
        sele_dl(homepage, "xpath", "/html/body/div[5]/section/section[2]/div/div[6]/div/div[8]/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td[8]/a", etf + ".xls")
    else:
        continue
    
driver.close()
        

