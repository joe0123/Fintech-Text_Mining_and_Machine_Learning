import sys
import os
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
import urllib.request as url

def proshares_dl(homepage, filename):
    #loading point
    ldp = soup.find("a", string = "NAV History").get('href')
    try:
        url.urlretrieve(ldp, filename)
    except:
        print("Downloading", ldp, "fails")
        return

#wait# convert xls to csv (module "xlrd" should be installed beforehand)
    #data_xls = pd.read_excel(filename)
    #data_xls.to_csv(filename - "xls" + "csv", encoding='utf-8', index=False)
    #os.remove(filename)

df = pd.read_csv(sys.argv[1])
ETFs = df["Symbol"].values  # list of all etfs' symbol names

for etf in ETFs:
#Find url of Homepage
    try:
        r = req.get("https://www.etf.com/" + etf, headers={'User-Agent': 'Mozilla/5.0'})
    except:
        print("\"https://www.etf.com/" + etf + "\"", "is not found")
        continue
    if r.status_code != req.codes.ok:
        print("a")
        continue
    #handle html code with BeautifulSoup
    soup = bs(r.text, 'html.parser')
    homepage = soup.find("a", string="Fund Home Page").get('href')
    #DEBUG# print(etf, homepage)
    
#Download data
    try:
        r = req.get(homepage)
    except:
        print("\""+homepage+"\"", "is not found")
        continue
    if r.status_code != req.codes.ok:
        continue
    soup = bs(r.text, 'html.parser')
    #the url of ETF's family (like iShares, SPDR...)
    family = homepage.split('/')[2]
    if family == "www.proshares.com":
        proshares_dl(homepage, etf + ".csv")
    else:
        continue

        

