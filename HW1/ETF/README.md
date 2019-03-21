# ETF crawler
In this project, we download all daily adjusted close of ETFs in 'Junk-ETF-list.csv' from the last trading day in 2015 untill now.
Because there is no any clue found in their homepages, we crawl Yahoo Finance to accomplish our mission.


## Crawler Package
We implement **Selenium** as our crawler.  
In collaboration with _driver_, though time-consuming, it's rather more straightforward for general users.  
Moreover, the combination of **requests** and **beautifulsoup** is supposed to set more detailed nuts and bolts in the face of https://finance.yahoo.com/.

## Flow Diagram
