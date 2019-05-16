# HW4

## 1.指標計算方法
請主要參考[ETF指標作法.docx](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW4/ETF%E6%8C%87%E6%A8%99%E4%BD%9C%E6%B3%95.docx?raw=true)。  
其中在實作Omega指標時，fit出pdf後再積分會導致較大誤差，所以我們直接將所有return value相加求平均。  

## 2.分析結果(前20名)
請見[hw4_result](https://github.com/joe0123/Fintech-Text_Mining_and_Machine_Learning/blob/master/HW4/hw4_result)

## 3.討論
### 關於各指標
1. ASSR為調整後的sharpe ratio(sharpe ratio代表多承受一單位的風險會創造多少超額報酬，越高代表績效越好，反之則越差)。而原先的sharpe ratio只有考慮到二階動差，而ASSR多考慮了三階動差。  
2. Omega Ratio表示為資產臨界值(無風險利率)以上之平均收益除以臨界值以下之平均收益。故當Omega ratio越高，此資產的績效越好，反之則越差。  
3. 所有gamble(具有風險的投資商品)收益率g和風險指標R都存在以下關係式: E[exp(-g/R)]=1，但R指標有些限制，唯有符合標準的資產才能計算，因此只能找出最好的排名。於是Q(g)將R指標加以改進(見指標計算方法)，便可找出最好和最壞的排名。

### 關於分析結果
1. 月資料跟週資料的評比結果算是相似，除了一些資產的排名有大幅度跳動，其他的排名大致相同。
2. 各指標之間很明顯差異甚多，各資產的名次在不同指標間相差不少。另外，有許多資產在ASSR和Omega中表現不錯，但在利用Q(g)作為績效指標時，卻連20名都擠不進去。例如: HYLD、 HYZD、 HYGH...
