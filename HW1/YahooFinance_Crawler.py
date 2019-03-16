import os
import sys
import time
import pandas as pd

from random import randint

from selenium import webdriver

df = pd.read_csv(sys.argv[1])
ETFs = df["Symbol"].values

for ETF in ETFs: 
    targetAsset = ETF
    
    driver = webdriver.Chrome('/anaconda3/bin/chromedriver')
    driver.get('https://finance.yahoo.com/quote/'+targetAsset+'?ltr=1')
    
    #inputElement.submit()
    time.sleep(5)
    
    # Select the subpage of Historical Data.
    items = driver.find_elements_by_css_selector("a span")
    for item in items:
        if item.text == "Historical Data":
            item.click()
            break
    time.sleep(5)

    # Select the dialog.
    arrows = driver.find_elements_by_css_selector(".historical div div span svg")
    arrows[0].click()
    
    time.sleep(5)
    
    # Time period
    driver.find_element_by_name("startDate").clear()
    driver.find_element_by_name("startDate").click()
    driver.find_element_by_name("startDate").send_keys("01/01/2016")

    driver.find_element_by_name("endDate").clear()
    driver.find_element_by_name("endDate").click()
    driver.find_element_by_name("endDate").send_keys("12/31/2018")

    driver.find_element_by_xpath("//button[contains(@class,'Py(9px) Miw(80px)! Fl(start)')]").click()
    time.sleep(2)
    
    # Apply the change.
    driver.find_element_by_xpath("//button[contains(@class,'Py(9px) Fl(end)')]").click()
    time.sleep(2)
    

    # Download the data.
    driver.find_element_by_xpath("//span[contains(text(),'Download Data')]").click()

    time.sleep(5)

    # Close the browser.
    driver.quit()
