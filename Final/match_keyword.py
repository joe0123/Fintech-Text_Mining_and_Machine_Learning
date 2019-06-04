from selenium import webdriver
import time
import csv

class crawl_name():
    def __init__(self):
    #initialization for webdriver
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0}
        options.add_experimental_option('prefs', prefs)
        options.add_argument("user-agent={}".format('Googlebot/2.1 (+http://www.google.com/bot.html)'))
        #reference# https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers/User-Agent
        self.driver = webdriver.Chrome(chrome_options=options)
    #initialization for name list
        self.nmlist = []

    def __del__(self):
        self.driver.close()

    def get_name(self, page=1):
        while True:
            self.driver.get("https://fund.cnyes.com/search/?fundName=%E9%87%8E%E6%9D%91&order=displayNameLocal&page="+str(page))
            names = self.driver.find_elements_by_partial_link_text("野村")
            if not names:
                break
            else:
                self.nmlist += [i.text for i in names]
                page += 1
        fw = open("remote_nm.txt", "a", encoding="utf-8")
        fw.writelines([i+"\n" for i in self.nmlist])
        fw.close()
        return self.nmlist

class match():
    def __init__(self, del_set):
    #initialization for local_set{str:set(str)}
        self.local_list = list()
        fr = open("local_nm.txt", "r", encoding="utf-8")
        for line in fr.readlines():
            self.local_list.append(line.strip())
        fr.close()
        self.local_set = {i:(set(i.replace("臺", "台")) - del_set) for i in self.local_list}
    #initialization for remote_set{str:set(str)}
        try:
            self.remote_list = list()
            fr = open("remote_nm.txt", "r", encoding="utf-8")
            for line in fr.readlines():
                self.remote_list.append(line.strip())
            fr.close()
        except:
            self.remote_list = crawl_name().get_name()
        self.remote_set = {i:(set(i.replace("臺", "台")) - del_set) for i in self.remote_list}

    def compare_set(self):
        fit = list()
        for ik, iv in self.local_set.items():
            fit.append([ik, [], 0])
            for jk, jv in self.remote_set.items():
                ratio = len(iv & jv) / len(iv | jv) 
                if ratio >= fit[-1][2]:
                    fit[-1][1:] = [jk, ratio]
                if ratio == 1:
                    break
        fit.insert(0, ["local", "remote", "ratio"])
        with open("match.csv", "w", encoding="utf-8", newline='') as fw:
            fcsv = csv.writer(fw)
            fcsv.writerows(fit)

if __name__ == '__main__':
    match(set("野村基金類型-之 ?()計價類")).compare_set()
