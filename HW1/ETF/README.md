# ETF crawler
In this project, we download all daily adjusted close of ETFs, founded before 2015/12/31, in 'Junk-ETF-list.csv' untill now.
Because there is no any clue found in their homepages, we crawl Yahoo Finance to accomplish our mission.
Enter 

## Crawler Package
We implement **Selenium** as our crawler.  
In collaboration with *driver*, though time-consuming, it's rather more straightforward for general users.  
Moreover, the combination of *requests* and *beautifulsoup* has more detailed setups in the face of https://finance.yahoo.com/.

## Flow Diagram
<img src="https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW1/ETF/Flow_diagram.png" width="70%"/>

### Questions for Novices
1. Syntex error is reported
`=> Make sure you're using python 3`
2. Module not found error is reported  
`=> "pip install" every module imported`
3. Type error is reported
`=> Make sure all modules imported are updated`
4. There is no 'driver' attribute found  
`=> Download Google Chrome!`
5. Index error in *sys.argv[1]* is reported
`=> Execute the program with command "python YahooFinance_Crawler.py Junk-ETF-List.csv"`
6. Historical data is always downloaded incompletely before the suspended process (due to sleep()) continues  
`=> Maybe your network is unstable or the download speed is too slow`
