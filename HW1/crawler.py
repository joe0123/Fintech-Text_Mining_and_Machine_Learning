import sys
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import urllib.request as url
from selenium import webdriver
import time

#initialization for webdriver (downloaded file with original name will be stored in ./tmp)
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd() + '\\tmp'}
options.add_experimental_option('prefs', prefs)
options.add_argument("user-agent={}".format('Googlebot/2.1 (+http://www.google.com/bot.html)'))
driver = webdriver.Chrome(chrome_options=options)

#wait# convert xls to csv (module "xlrd" should be installed beforehand)
    #data_xls = pd.read_excel(filename)
    #data_xls.to_csv(filename - "xls" + "csv", encoding='utf-8', index=False)
    #os.remove(filename)

def html_code(url):
    try:
        r = requests.get(url)
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

def fast_dl(homepage, head, value, target, filename):
    #loading point
    soup = html_code(homepage)
    if soup == "FAIL":
        return
    ldp = head + soup.find("a", string=value).get(target)
    if homepage == "www.pimcoetfs.com":
        ldp = ldp.replace("amp;", "")
    download(ldp, filename)

def slow_dl(homepage, key, value, filename):
    driver.get(homepage)
    try:
        if key == "xpath":
            driver.find_element_by_xpath(value).click()
        else:
            driver.find_element_by_link_text(value).click()
    except:
        print("Downloading", "\"" + key + "\"", "in", "\"" + homepage + "\"", "fails")
    time.sleep(3)
    re_name(filename)


df = pd.read_csv(sys.argv[1])
#list of all etfs' symbol names
ETFs = df["Symbol"].values
#reference# https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers/User-Agent

#files downloaded will be stored in ./download
os.mkdir("download")

for etf in ETFs:
#Find url of Homepage
    soup = html_code("https://www.etf.com/" + etf)
    if soup == "FAIL":
        continue
    homepage = soup.find("a", string="Fund Home Page").get("href")
    print(etf, homepage)
#Download data
    #the url of ETF's family (like iShares, SPDR...)
    family = homepage.split('/')[2]
    if family == "www.ishares.com":
        fast_dl(homepage, "https://" + family, "Download", "href", etf + ".xls")
    elif family == "www.proshares.com":
        fast_dl(homepage, "", "NAV History", "href",etf + ".csv")
    elif family == "us.spdrs.com":
        slow_dl(homepage, "text", "Most Recent NAV / NAV History XLS", etf + ".xls")
    elif family == "www.invesco.com":
        slow_dl(homepage, "text", "Historical NAVs", etf + ".csv")
    elif family == "www.pimcoetfs.com":
        fast_dl(homepage, "http://" + family, "NAV History Download", "href", etf + ".xls")
    elif family == "www.wisdomtree.com":
        fast_dl(homepage, "", "View NAV and Premium/Discount History", "data-href" ,etf + ".txt")   #html code will be downloaded
    elif family == "dws.com":
        slow_dl(homepage, "text", "NAV History (CSV)", etf + ".csv")
    elif family == "www.vaneck.com":
        slow_dl(homepage, "xpath", "/html/body/div[5]/section/section[2]/div/div[6]/div/div[8]/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td[8]/a", etf + ".xls")
    else:
        continue
    
driver.close()
        

