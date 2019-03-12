import sys
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs

df = pd.read_csv(sys.argv[1])
ETFs = df["Symbol"].values  # list of all etfs' symbol names
whole_name = df["ETF Name"].values  # list of all etfs' whole names

for etf in ETFs:
    r = req.get("https://www.etf.com/" + etf)   # download contents in the website
    if r.status_code == req.codes.ok:   # to check if req.get is successful
        soup = bs(r.text, 'html.parser')    # handle html code with BeautifulSoup
        href = soup.find("a", string="Fund Home Page").get('href')  # find hypertext reference
        #DEBUG# print(etf, href)
        

