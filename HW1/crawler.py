import sys
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import urllib.request as url
from selenium import webdriver
import time

#initialization for requests
headers = {'user-agent':'Googlebot/2.1 (+http://www.google.com/bot.html)'}
#initialization for webdriver (downloaded file with original name will be stored in ./tmp)
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd() + '\\tmp'}
options.add_experimental_option('prefs', prefs)

#wait# convert xls to csv (module "xlrd" should be installed beforehand)
    #data_xls = pd.read_excel(filename)
    #data_xls.to_csv(filename - "xls" + "csv", encoding='utf-8', index=False)
    #os.remove(filename)

def html_code(url, case):
    try:
        if case == 0:
            r = requests.get(url)
        else:
            r = requests.get(url, headers=headers)
    except:
        print("\"" + url + "\"", "is not found")
        return "FAIL" 
    if r.status_code != requests.codes.ok:
        print("request", "\"" + url + "\"", "fails:", r.status_code)
        return "FAIL"
    #handle html code with BeautifulSoup
    soup = bs(r.text, 'html.parser')
    #debug# print(soup.encode("utf8").decode("cp950", "ignore"))
    return soup 

def download(ldp, filename):
    try:
        url.urlretrieve(ldp, "./download/" + filename)
    except:
        print("Downloading", "\"" + ldp + "\"", "fails")
        return
    #DEBUG# print(filename, "downloaded")

def re_name(new_fn):
    #file to be renamed was stored in ./tmp
    old_fn = os.listdir("./tmp")
    os.rename("./tmp/" + old_fn[0], "./download/" + new_fn)
    os.rmdir("./tmp")

def ishares_dl(homepage, filename):
    #loading point
    soup = html_code(homepage, 0)
    if soup == "FAIL":
        return
    ldp = "https://www.ishares.com" + soup.find("a", string="Download").get("href")
    download(ldp, filename)

def proshares_dl(homepage, filename):
    soup = html_code(homepage, 0)
    if soup == "FAIL":
        return
    ldp = soup.find("a", string="NAV History").get("href")
    download(ldp, filename)

def spdr_dl(homepage, filename):
    soup = html_code(homepage, 1)
    if soup == "FAIL":
        return
    ldps = soup.find_all("div", class_="related-info")
    ldp = ""
    for i in ldps:
        if i.getText().find("Most Recent NAV / NAV History") != -1:
            ldp = "https://us.spdrs.com" + i.a["href"]
            break
    download(ldp, filename)
    
def invesco_dl(homepage, etf):
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(homepage)
    driver.find_element_by_link_text("Historical NAVs").click()
    time.sleep(3)
    driver.close()
    re_name(etf + ".csv")
    #DEBUG# print(etf + ".csv", "downloaded")




df = pd.read_csv(sys.argv[1])
#list of all etfs' symbol names
ETFs = df["Symbol"].values
#reference# https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers/User-Agent

#files downloaded will be stored in ./download
os.mkdir("download")

for etf in ETFs:
#Find url of Homepage
    soup = html_code("https://www.etf.com/" + etf, 0)
    if soup == "FAIL":
        continue
    homepage = soup.find("a", string="Fund Home Page").get("href")
    print(etf, homepage)
#Download data
    #the url of ETF's family (like iShares, SPDR...)
    family = homepage.split('/')[2]
    if family == "www.ishares.com":
        ishares_dl(homepage, etf + ".xls")
    elif family == "www.proshares.com":
        proshares_dl(homepage, etf + ".csv")
    elif family == "us.spdrs.com":
        spdr_dl(homepage, etf + ".xls")
    elif family == "www.invesco.com":
        invesco_dl(homepage, etf)
    else:
        continue
        

