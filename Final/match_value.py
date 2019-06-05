from match_keyword import *
import pandas as pd
import time

class match_value():
    def __init__(self, t=1):
    #initialization for webdriver
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0}
        options.add_experimental_option('prefs', prefs)
        options.add_argument("user-agent={}".format('Googlebot/2.1 (+http://www.google.com/bot.html)'))
        #reference# https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers/User-Agent
        self.driver = webdriver.Chrome(chrome_options=options)
        self.time = t
    
    def __del__(self):
        self.driver.close()

    def get_value(self, page_dict, df):
        for i in df.index:
            if i > df.index[0] and df.ix[i, "remote"] == df.ix[i-1, "remote"]:
                df.ix[i, df.columns[2]:df.columns[-1]] = df.ix[i-1, df.columns[2]:df.columns[-1]]
                continue

            if df.ix[i, "remote"][:4] != "http":
                self.driver.get("https://fund.cnyes.com/search/?fundName=%E9%87%8E%E6%9D%91&order=displayNameLocal&page="+str(page_dict[df.ix[i, "remote"]]))
                self.driver.get(self.driver.find_element_by_link_text(df.ix[i, "remote"]).get_attribute("href"))
            else:
                self.driver.get(df.ix[i, "remote"])
            
            end = False
            for target in df.columns[2:]:
                while not end:
                    time.sleep(self.time)
                    dates = [j.text for j in self.driver.find_elements_by_xpath("//*[@id=\"content\"]/div/div/div[2]/div[2]/main[2]/section/div[2]/section[3]/table/tbody/tr/td[@class=\"_1JRsZ\"]")]
                    if int("".join(dates[0].split("/"))) < int("".join(target.split("/"))):
                        print(target, dates[0])
                        break
                    try:
                        found = dates.index(target)
                    except: 
                        try:
                            self.driver.find_element_by_link_text("下一頁").click()
                        except:
                            end = True
                            break
                    else:
                        df.ix[i, target] = self.driver.find_element_by_xpath("//*[@id=\"content\"]/div/div/div[2]/div[2]/main[2]/section/div[2]/section[3]/table/tbody/tr["+str(found+1)+"]/td[2]").text
                        break
                if end:
                    break
        return df

if __name__ == '__main__':
    try:
        fr = open("remote_nm.txt", "r", encoding="utf-8")
    except:
        page_dict = crawl_name().get_name()
    else:
        page_dict = {}
        for line in fr.readlines():
            tmp = line.split(",")
            page_dict[tmp[0]] = tmp[1]
        fr.close()

    try:
        df = pd.read_csv("rematch.csv", encoding="big5")
    except:
       match_word(set("野村基金類型-之 ?()計價類")).compare_set()
       print("\"match_keyword.py\" was just executed. Please refine \"match.csv\" into \"rematch.csv (encoding=big5)\" first. and come back again!")
       exit()

    df = df.sort_values(by="remote")
    df.index = range(len(df))
    for i in ['2018/12/14', '2018/11/15', '2018/10/16', '2018/09/14', '2018/08/15', '2018/07/17', '2018/06/15', '2018/05/15', '2018/04/17', '2018/03/15', '2018/02/09', '2018/01/16']:
        df[i] = [None]*len(df.index)
    df = match_value(2).get_value(page_dict, df.head(1))
    #print(df)
    df.drop("remote", axis=1)
    df.to_csv("net_value.csv", encoding="big5", index=False)
